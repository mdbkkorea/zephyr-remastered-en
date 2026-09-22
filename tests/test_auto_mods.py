import hashlib,json,shutil,zlib,unittest
from pathlib import Path
import test_windows_patcher as fixtures
from test_windows_patcher import PortablePatcher,sha

class AutoModTests(unittest.TestCase):
 def setUp(self):
  fixtures.WindowsPatcherTests.setUp(self)
  self.passive='BepInEx/plugins/ZephyrPassives/ZephyrPassives.dll'
  self.fullmap='BepInEx/plugins/ZephyrFullmap/ZephyrFullmap.dll'
  before=b'Korean map';after=b'English map'
  blob=zlib.compress(bytes(x^y for x,y in zip(before.ljust(len(after),b'\0'),after)));(self.payload/'map.delta').write_bytes(blob)
  self.maprow=dict(path=self.fullmap,before_sha256=hashlib.sha256(before).hexdigest(),after_sha256=hashlib.sha256(after).hexdigest(),after_size=len(after),delta='map.delta',delta_sha256=hashlib.sha256(blob).hexdigest())
  self.manifest['automatic_mods']=[dict(name='Passives',version='2.4.3',path=self.passive,sha256=hashlib.sha256(b'passives').hexdigest(),files=list(self.files)),dict(name='Fullmap',version='1.8.0',path=self.fullmap,sha256=self.maprow['before_sha256'],translation=self.maprow)]
  (self.payload/'manifest.json').write_text(json.dumps(self.manifest));self.hashes.update({p.name:sha(p) for p in self.payload.iterdir()})
  self.p=PortablePatcher(self.game,self.payload,self.game.parent/'state')
 def put(self,path,data):
  p=self.game/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
 def test_combinations(self):
  for passive,fullmap in [(False,False),(True,False),(False,True),(True,True)]:
   with self.subTest(passive=passive,fullmap=fullmap):
    for path in [self.passive,self.fullmap]:(self.game/path).unlink(missing_ok=True)
    if passive:self.put(self.passive,b'passives')
    if fullmap:self.put(self.fullmap,b'Korean map')
    result=self.p.install();self.assertEqual(result['status'],'installed');self.assertEqual('Passives' in result['translation_profile'],passive)
    if fullmap:self.assertEqual((self.game/self.fullmap).read_bytes(),b'English map')
    self.assertEqual(self.p.restore()['status'],'original')
    if fullmap:self.assertEqual((self.game/self.fullmap).read_bytes(),b'Korean map')
 def test_unknown_falls_back_and_preserves_both_mods(self):
  for unknown in [self.passive,self.fullmap]:
   self.put(self.passive,b'passives');self.put(self.fullmap,b'Korean map');self.put(unknown,b'new version')
   before={p:(self.game/p).read_bytes() for p in [self.passive,self.fullmap]}
   result=self.p.install();self.assertEqual(result['status'],'installed');self.assertIn('fallback',result['translation_profile'])
   self.assertEqual({p:(self.game/p).read_bytes() for p in before},before)
   self.p.restore();self.assertEqual({p:(self.game/p).read_bytes() for p in before},before)
 def test_mod_upgrade_after_managed_install_falls_back(self):
  self.put(self.passive,b'passives');self.put(self.fullmap,b'Korean map');self.p.install()
  self.put(self.fullmap,b'new version');self.assertEqual(self.p.install()['status'],'installed')
  self.p.restore();self.assertEqual((self.game/self.fullmap).read_bytes(),b'new version')
 def test_fallback_still_rejects_modified_game_resources(self):
  self.put(self.passive,b'new version');(self.game/self.files[0]['path']).write_bytes(b'changed resource')
  with self.assertRaises(ValueError):self.p.install()
 def test_already_english_preserved_on_restore(self):
  self.put(self.fullmap,b'English map');self.p.install();self.p.restore();self.assertEqual((self.game/self.fullmap).read_bytes(),b'English map')
 def test_removed_mod_not_recreated(self):
  self.put(self.fullmap,b'Korean map');self.p.install();(self.game/self.fullmap).unlink();self.p.install();self.p.restore();self.assertFalse((self.game/self.fullmap).exists())
 def test_added_mod_after_install(self):
  self.p.install();self.put(self.fullmap,b'Korean map');self.assertEqual(self.p.install()['status'],'installed');self.p.restore();self.assertEqual((self.game/self.fullmap).read_bytes(),b'Korean map')
 def test_relocated_plugin_rejected(self):
  self.put('BepInEx/plugins/elsewhere/ZephyrFullmap.dll',b'Korean map')
  with self.assertRaisesRegex(ValueError,'relocated'):self.p.install()
