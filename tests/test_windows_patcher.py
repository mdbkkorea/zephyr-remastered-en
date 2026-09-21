import contextlib
import hashlib
import importlib.util
import json
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest.mock import patch
import zlib

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'windows'))
sys.modules.setdefault('english_trust',types.SimpleNamespace(HASHES={}))
import english_engine as engine
from english_resources import rebuild, safe, sha


class PortablePatcher(engine.Patcher):
    # Unit tests exercise transaction logic, not Windows process/lock APIs.
    def stopped(self): pass
    @contextlib.contextmanager
    def locked(self): yield


class WindowsPatcherTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        root=Path(self.temp.name);self.game=root/'game';self.payload=root/'payload'
        self.game.mkdir();self.payload.mkdir();(self.game/'ZephyrRemastered.exe').write_bytes(b'executable')
        self.files=[]
        for i,(before,after) in enumerate([(b'original one',b'english text longer'),(b'original two',b'english')]):
            name=f'ZephyrRemastered_Data/{i}.bin';p=self.game/name;p.parent.mkdir(exist_ok=True);p.write_bytes(before)
            delta=zlib.compress(bytes(a^b for a,b in zip(before[:len(after)].ljust(len(after),b'\0'),after)))
            (self.payload/f'{i}.delta').write_bytes(delta)
            self.files.append(dict(path=name,before_sha256=sha(p),after_sha256=hashlib.sha256(after).hexdigest(),after_size=len(after),delta=f'{i}.delta',delta_sha256=hashlib.sha256(delta).hexdigest()))
        self.manifest=dict(files=self.files,dependencies=[],exe_sha256=sha(self.game/'ZephyrRemastered.exe'),game_build='fixture')
        (self.payload/'manifest.json').write_text(json.dumps(self.manifest))
        self.hashes={p.name:sha(p) for p in self.payload.iterdir()}
        self.trust=patch.object(engine,'HASHES',self.hashes);self.trust.start();self.addCleanup(self.trust.stop)
        self.p=PortablePatcher(self.game,self.payload,root/'state')

    def test_install_idempotent_restore(self):
        self.assertEqual(self.p.status()['status'],'original')
        self.assertEqual(self.p.install()['status'],'installed')
        self.assertEqual(self.p.install()['status'],'installed')
        self.assertEqual(self.p.restore()['status'],'original')
        self.assertEqual(self.p.actual(),{r['path']:r['before_sha256'] for r in self.files})

    def test_long_backup_paths_install_and_restore(self):
        deep_home=self.game.parent/('long-state-'+'x'*170)
        import shutil
        from english_resources import windows_long_path
        self.assertTrue(deep_home.resolve().is_relative_to(self.game.parent.resolve()))
        self.addCleanup(shutil.rmtree,windows_long_path(deep_home.resolve()))
        p=PortablePatcher(self.game,self.payload,deep_home)
        self.assertEqual(p.install()['status'],'installed')
        self.assertEqual(p.restore()['status'],'original')

    def test_modified_original_rejected(self):
        (self.game/self.files[0]['path']).write_bytes(b'modified')
        with self.assertRaises(ValueError):self.p.install()
        self.assertEqual((self.game/self.files[0]['path']).read_bytes(),b'modified')

    def test_tampered_payload_rejected(self):
        (self.payload/'0.delta').write_bytes(b'tampered')
        with self.assertRaises(ValueError):PortablePatcher(self.game,self.payload,self.game.parent/'state')

    def test_interruption_rolls_back(self):
        stage=self.game.parent/'stage';rebuild(self.game,stage,self.manifest,self.payload)
        desired={r['path']:r['after_sha256'] for r in self.files}
        with self.assertRaises(RuntimeError):self.p.transaction(stage,desired,{},fail_after=1)
        self.assertEqual(self.p.status()['status'],'original')
        self.assertFalse(self.p.journalfile.exists())

    def test_interrupted_recovery_preserves_later_changes(self):
        stage=self.game.parent/'stage';rebuild(self.game,stage,self.manifest,self.payload)
        with patch.object(self.p,'_recover',side_effect=RuntimeError('simulate process exit')):
            with self.assertRaises(RuntimeError):self.p.transaction(stage,{r['path']:r['after_sha256'] for r in self.files},{},fail_after=1)
        altered=self.game/self.files[0]['path'];altered.write_bytes(b'newer update')
        with self.assertRaises(ValueError):self.p.recover()
        self.assertEqual(altered.read_bytes(),b'newer update')
        self.assertTrue(self.p.journalfile.exists())

    def test_explicit_recovery(self):
        stage=self.game.parent/'stage';rebuild(self.game,stage,self.manifest,self.payload)
        with patch.object(self.p,'_recover',side_effect=RuntimeError('simulate process exit')):
            with self.assertRaises(RuntimeError):self.p.transaction(stage,{r['path']:r['after_sha256'] for r in self.files},{},fail_after=1)
        self.assertEqual(self.p.recover()['status'],'original')

    def test_restore_rejects_updated_files(self):
        self.p.install();(self.game/self.files[0]['path']).write_bytes(b'game update')
        with self.assertRaises(ValueError):self.p.restore()

    def test_paths_cannot_escape(self):
        for name in ['../outside','C:/outside','/outside','..\\outside']:
            with self.assertRaises(ValueError):safe(self.game,name)

class PackagedSaveTests(unittest.TestCase):
    def test_copies_preserve_gameplay_and_original(self):
        import gzip
        from english_saves import prepare_saves
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);source=root/'saves';source.mkdir()
            data={'Units':[{'DialogueName':'시라노','FullName':'시라노 번스타인','JobName':'수련 검사','Level':16,'ID4':'시라노'}]}
            original=gzip.compress(json.dumps(data).encode());path=source/'save_RE_v1_01.dat';path.write_bytes(original)
            output=root/'converted';prepare_saves(source,output,{'시라노':'Cyrano'})
            actual=json.loads(gzip.decompress((output/path.name).read_bytes()))
            self.assertEqual(actual['Units'][0]['DialogueName'],'Cyrano')
            actual['Units'][0]['DialogueName']='시라노'
            self.assertEqual(actual,data);self.assertEqual(path.read_bytes(),original)
            with self.assertRaises(ValueError):prepare_saves(source,output,{})
            with self.assertRaises(ValueError):prepare_saves(source,source/'nested',{})
