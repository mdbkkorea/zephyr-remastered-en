"""Combine independently validated base/Passives kits and pinned Fullmap delta."""
import argparse, hashlib, json, shutil, zlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def digest(data):return hashlib.sha256(data).hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument('--base',type=Path,required=True);p.add_argument('--passives',type=Path,required=True);p.add_argument('--fullmap',type=Path,required=True);p.add_argument('--translated-fullmap',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 if a.output.exists() or (ROOT/'private').resolve() not in a.output.resolve().parents:raise ValueError('Use a new private output directory')
 base=json.loads((a.base/'payload/manifest.json').read_text());mod=json.loads((a.passives/'payload/manifest.json').read_text())
 if base['exe_sha256']!=mod['exe_sha256'] or {r['path']:r['before_sha256'] for r in base['files']}!={r['path']:r['before_sha256'] for r in mod['files']}:raise ValueError('Mismatched game versions')
 shutil.copytree(a.base,a.output);payload=a.output/'payload'
 for row in mod['files']:
  old=row['delta'];row['delta']='passives-'+old;shutil.copy2(a.passives/'payload'/old,payload/row['delta'])
 profile=json.loads((ROOT/'localization/mods/zephyr-passives-2.4.3.json').read_text())
 dep=profile['dependency']
 before=a.fullmap.read_bytes();after=a.translated_fullmap.read_bytes()
 if digest(before)!='9c891825ed28212df42a97512c2e6b522304009e2e7dca669a7615f30b199334' or digest(after)!='bf0e14e14f0f6eeef14ca1210e781c00cef65e2ce96502e6b89ea5521cb54fc4':raise ValueError('Unverified Fullmap input')
 blob=zlib.compress(bytes(x^y for x,y in zip(before[:len(after)].ljust(len(after),b'\0'),after)),9);(payload/'fullmap.delta').write_bytes(blob)
 path='BepInEx/plugins/ZephyrFullmap/ZephyrFullmap.dll'
 base['automatic_mods']=[dict(name='ZephyrPassives',version='2.4.3',path=dep['path'],sha256=dep['sha256'],files=mod['files']),dict(name='ZephyrFullmap',version='1.8.0',path=path,sha256=digest(before),translation=dict(path=path,before_sha256=digest(before),after_sha256=digest(after),after_size=len(after),delta='fullmap.delta',delta_sha256=digest(blob)))]
 base['format']=2
 (payload/'manifest.json').write_text(json.dumps(base,indent=2)+'\n')
 for src in (ROOT/'windows').iterdir():
  if src.is_file():shutil.copy2(src,a.output/src.name)
 shutil.copy2(ROOT/'tests/test_auto_mods.py',a.output/'tests/test_auto_mods.py')
 (a.output/'english_trust.py').write_text('HASHES = '+repr({p.name:digest(p.read_bytes()) for p in payload.iterdir() if p.is_file()})+'\n')
 shutil.make_archive(str(a.output),'zip',root_dir=a.output.parent,base_dir=a.output.name)
 print(a.output)
if __name__=='__main__':main()
