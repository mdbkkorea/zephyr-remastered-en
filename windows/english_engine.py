"""Version-locked, journaled local patcher. No uploads and no game launching."""
import argparse,contextlib,gzip,hashlib,json,os,re,shutil,subprocess,sys,uuid
from pathlib import Path
from english_resources import rebuild,safe,sha,windows_long_path
from english_trust import HASHES
from english_platform import state_home as default_state_home, path_key, require_game_stopped, operation_lock
VERSION='0.1.0-playtest3'
def read(p):return json.loads(p.read_text(encoding='utf8'))
def write(p,value):
 p.parent.mkdir(parents=True,exist_ok=True);tmp=p.with_suffix(p.suffix+'.new');tmp.write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf8');os.replace(tmp,p)
def payload_default():return Path(__file__).resolve().parent/'payload'
class Patcher:
 def __init__(self,game,payload=None,state_home=None):
  self.game=Path(game).resolve();self.payload=Path(payload or payload_default()).resolve()
  for n,h in HASHES.items():
   if sha(self.payload/n)!=h:raise ValueError('Embedded English patch data failed verification.')
  self.patch=json.loads((self.payload/'manifest.json').read_text(encoding='utf8'));self.files=self.patch['files'];self.names={r['path'] for r in self.files}
  for name in self.names:
   if not name.startswith('ZephyrRemastered_Data/') or any(x in Path(name).parts for x in ['..']):raise ValueError('Invalid resource path.')
   safe(self.game,name)
  key=hashlib.sha256(path_key(self.game).encode()).hexdigest()[:24]
  home=Path(state_home or default_state_home());self.home=windows_long_path(home.resolve()/key);self.original=self.home/'original';self.statefile=self.home/'state.json';self.journalfile=self.home/'transaction.json'
 def guard_game(self):
  exe=self.game/'ZephyrRemastered.exe'
  if not exe.is_file() or sha(exe)!=self.patch['exe_sha256']:raise ValueError('Select a supported original Zephyr Remastered game folder.')
  for r in self.patch['dependencies']:
   if not safe(self.game,r['path']).is_file() or sha(safe(self.game,r['path']))!=r['sha256']:raise ValueError('Game dependency version mismatch. Restore original files or verify them in Steam.')
 def stopped(self):
  require_game_stopped()
 def state(self):return read(self.statefile) if self.statefile.exists() else None
 def actual(self):return {r['path']:sha(safe(self.game,r['path'])) if safe(self.game,r['path']).is_file() else None for r in self.files}
 def installed_build(self):
  manifest=self.game.parent.parent/'appmanifest_5099430.acf'
  if self.game.parent.name.casefold()!='common' or not manifest.is_file():return None
  text=manifest.read_text(encoding='utf8')
  def value(key):
   match=re.search(r'"'+key+r'"\s+"([^"]+)"',text)
   return match.group(1) if match else None
  if value('appid')!='5099430' or value('installdir')!=self.game.name:return None
  return value('buildid')
 def backup_rows(self):
  # Only hash-verified original files from this install path are eligible.
  return [r for r in self.files if safe(self.original,r['path']).is_file() and sha(safe(self.original,r['path']))==r['before_sha256']]
 def status(self):
  if not (self.game/'ZephyrRemastered.exe').is_file():raise ValueError('Select the folder containing ZephyrRemastered.exe.')
  compatible=True;reason=None
  try:self.guard_game()
  except ValueError as ex:compatible=False;reason=str(ex)
  actual=self.actual();state=self.state();before={r['path']:r['before_sha256'] for r in self.files};after={r['path']:r['after_sha256'] for r in self.files}
  managed=(state or {}).get('installed_files',{})
  matches_managed=bool(managed) and all(actual.get(k)==v for k,v in managed.items()) and all(actual[k]==before[k] for k in actual.keys()-managed.keys())
  if self.journalfile.exists():kind='recovery_required'
  elif not compatible:kind='unsupported_or_modified'
  elif actual==before:kind='original'
  elif matches_managed:
   kind='installed' if state.get('version')==VERSION and actual==after else 'update_available'
  elif actual==after:kind='unmanaged_localization'
  else:kind='unsupported_or_modified'
  backups=self.backup_rows()
  return dict(status=kind,version=VERSION,installed_version=(state or {}).get('version'),game_build=self.patch['game_build'],installed_build=self.installed_build(),compatibility_reason=reason,can_install=kind in ['original','update_available','installed'],can_restore=bool(state) and len(backups)==len(self.files) and kind in ['installed','update_available'],can_force_restore=bool(backups) and kind!='recovery_required',backup_files=len(backups),backup_complete=len(backups)==len(self.files),backup_available=bool(backups))
 def locked(self):return operation_lock(self.home)
 def copy_checked(self,source,target,expected):
  if sha(source)!=expected:raise ValueError('Staged file checksum failed.')
  target.parent.mkdir(parents=True,exist_ok=True);temp=target.with_name(target.name+'.zephyr-patcher.tmp')
  # Only the current transaction owns this narrowly named temporary path.
  if temp.exists():raise ValueError('An unfinished temporary file exists. Recover the previous operation first.')
  shutil.copy2(source,temp)
  if sha(temp)!=expected:raise ValueError('Copy checksum failed.')
  os.replace(temp,target)
  if sha(target)!=expected:raise ValueError('Written file checksum failed.')
 def verify_original(self):
  for r in self.files:
   if sha(safe(self.original,r['path']))!=r['before_sha256']:raise ValueError('Original backup is missing or corrupt. Operation stopped.')
  for r in self.patch['dependencies']:
   if sha(safe(self.original,r['path']))!=r['sha256']:raise ValueError('Original dependency backup is incomplete.')
 def _recover(self):
  self.stopped()
  if not (self.game/'ZephyrRemastered.exe').is_file():raise ValueError('Game folder does not exist.')
  if not self.journalfile.exists():return
  tx=read(self.journalfile);rollback=safe(self.home,tx['rollback']);entries=tx['entries']
  if not {r['path'] for r in entries}.issubset(self.names) or not entries:raise ValueError('Recovery record does not match this patch.')
  for r in entries:
   p=safe(self.game,r['path'])
   if (sha(p) if p.is_file() else None) not in [r['before'],r['after']]:raise ValueError('Game files changed after the interrupted operation. Automatic recovery stopped to preserve those changes.')
   if r['before'] is not None and sha(safe(rollback,r['path']))!=r['before']:raise ValueError('Transaction backup is corrupt.')
  for r in entries:
   self.stopped();p=safe(self.game,r['path']);tmp=p.with_name(p.name+'.zephyr-patcher.tmp')
   if tmp.exists():tmp.unlink()
   if r['before'] is None:p.unlink(missing_ok=True)
   elif not p.is_file() or sha(p)!=r['before']:self.copy_checked(safe(rollback,r['path']),p,r['before'])
  if tx['previous_state'] is None:
   if self.statefile.exists():self.statefile.unlink()
  else:write(self.statefile,tx['previous_state'])
  self.journalfile.unlink()
 def recover(self):
  with self.locked():self._recover()
  return self.status()
 def transaction(self,source,desired,next_state,fail_after=None,selected=None):
  self.stopped();before=self.actual();txid=uuid.uuid4().hex;rollback=self.home/'transactions'/txid/'rollback'
  entries=[dict(path=r['path'],before=before[r['path']],after=desired[r['path']]) for r in (selected if selected is not None else self.files)]
  for r in entries:
   if r['before'] is not None:
    p=safe(rollback,r['path']);p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(safe(self.game,r['path']),p)
    if sha(p)!=r['before']:raise ValueError('Pre-installation backup failed.')
  write(self.journalfile,dict(rollback=rollback.relative_to(self.home).as_posix(),entries=entries,previous_state=self.state()))
  try:
   for i,r in enumerate(entries):
    self.stopped();p=safe(self.game,r['path'])
    if (sha(p) if p.is_file() else None)!=r['before']:raise ValueError('Game files changed during installation.')
    self.copy_checked(safe(source,r['path']),p,r['after'])
    if fail_after is not None and i+1==fail_after:raise RuntimeError('Injected interruption for recovery testing')
   if self.actual()!=desired:raise ValueError('Final installation verification failed.')
   write(self.statefile,next_state);self.journalfile.unlink()
  except Exception:
   self._recover();raise
 def install(self):
  with self.locked():
   self.stopped();self.guard_game()
   if self.journalfile.exists():raise ValueError('Recover the previous operation first.')
   state=self.status()
   if state['status']=='installed':return state
   if state['status'] not in ['original','update_available']:raise ValueError('Files are not a supported original or an installation managed by this English patcher.')
   if not self.original.exists():
    if state['status']!='original':raise ValueError('Original backup is missing. Cannot update.')
    temporary=self.home/('original-'+uuid.uuid4().hex)
    for r in self.files+self.patch['dependencies']:
     src=safe(self.game,r['path']);dst=safe(temporary,r['path']);dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst)
    temporary.rename(self.original)
   # A newer payload may add a previously untouched resource to an old backup.
   for r in self.files:
    dst=safe(self.original,r['path'])
    if not dst.exists():
     src=safe(self.game,r['path'])
     if not src.is_file() or sha(src)!=r['before_sha256']:raise ValueError('A newly patched resource lacks a verified original backup.')
     self.copy_checked(src,dst,r['before_sha256'])
   self.verify_original();stage=self.home/'staging'/uuid.uuid4().hex;rebuild(self.original,stage,self.patch,self.payload)
   desired={r['path']:r['after_sha256'] for r in self.files};next_state=dict(version=VERSION,game_build=self.patch['game_build'],installed_files=desired)
   self.transaction(stage,desired,next_state)
  return self.status()
 def restore(self):
  with self.locked():
   self.stopped();self.guard_game()
   if self.journalfile.exists():raise ValueError('Recover the previous operation first.')
   status=self.status()
   if status['status']=='original':return status
   if not status['can_restore']:raise ValueError('Files changed or are not managed by this patcher. Restoration stopped.')
   self.verify_original();desired={r['path']:r['before_sha256'] for r in self.files};self.transaction(self.original,desired,dict(version=None,game_build=self.patch['game_build'],installed_files={}))
  return self.status()
 def force_restore(self,confirmed=False):
  if not confirmed:raise ValueError('Restoring an old backup requires explicit confirmation.')
  with self.locked():
   self.stopped()
   if not (self.game/'ZephyrRemastered.exe').is_file():raise ValueError('Select the game folder.')
   if self.journalfile.exists():raise ValueError('Recover the previous operation first.')
   rows=self.backup_rows()
   if not rows:raise ValueError('No verified original backup exists. Use Steam file verification.')
   desired=self.actual()
   for r in rows:desired[r['path']]=r['before_sha256']
   self.transaction(self.original,desired,dict(version=None,game_build=self.patch['game_build'],installed_files={}),selected=rows)
  return dict(self.status(),force_restored_files=len(rows),steam_verification_recommended=True)
 def verify(self):
  """Read-only game validation and full reconstruction, useful for release QA."""
  with self.locked():
   self.guard_game()
   if self.status()['status']!='original':raise ValueError('Verification requires supported original game files.')
   before=self.actual();folder=self.home/'verification'/uuid.uuid4().hex
   original=folder/'original'
   for r in self.files+self.patch['dependencies']:
    dst=safe(original,r['path']);dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(safe(self.game,r['path']),dst)
   rebuild(original,folder/'rebuilt',self.patch,self.payload)
   if self.actual()!=before:raise ValueError('Source files changed during verification.')
  return dict(status='verified',files=len(self.files),game_files_changed=False)
def main():
 for stream in (sys.stdout,sys.stderr):
  if hasattr(stream,'reconfigure'):stream.reconfigure(encoding='utf8')
 ap=argparse.ArgumentParser();ap.add_argument('action',choices=['status','install','restore','force_restore','recover','verify']);ap.add_argument('--game',required=True);ap.add_argument('--payload');ap.add_argument('--state-home',help='Optional separate backup directory');ap.add_argument('--confirm-old-backup',action='store_true');args=ap.parse_args()
 try:
  p=Patcher(args.game,args.payload,args.state_home);result=p.force_restore(confirmed=args.confirm_old_backup) if args.action=='force_restore' else getattr(p,args.action)();print(json.dumps(dict(ok=True,**result),ensure_ascii=False))
 except Exception as ex:print(json.dumps(dict(ok=False,error=str(ex)),ensure_ascii=False));sys.exit(1)
if __name__=='__main__':main()
