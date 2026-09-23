import hashlib
import json
from pathlib import Path
import tempfile
import unittest
import zipfile
from scripts.package_windows_zip import package

class WindowsZipTests(unittest.TestCase):
 def kit(self, base):
  p=base/'long-source-kit-name';(p/'payload').mkdir(parents=True)
  (p/'payload/manifest.json').write_text(json.dumps({'platform':'steam'}))
  (p/'payload/000.delta').write_bytes(b'payload\x00\xff')
  (p/'Build-Windows.cmd').write_text('echo build')
  return p
 def test_short_paths_preserve_payload_and_notices(self):
  with tempfile.TemporaryDirectory() as t:
   base=Path(t);p=self.kit(base)
   notice=p/'licenses/python/numpy'/('long_'*30+'LICENSE');notice.parent.mkdir(parents=True);notice.write_bytes(b'copyright\r\nlicense')
   (p/'__pycache__').mkdir();(p/'__pycache__/unused.pyc').write_bytes(b'cache')
   out=base/'ZSteam-b2r1.zip';r=package(p,out)
   self.assertLessEqual(r['max_member_utf16_units'],60)
   with zipfile.ZipFile(out) as z:
    self.assertEqual(z.read('ZSteam/payload/000.delta'),b'payload\x00\xff')
    self.assertEqual(z.read('ZSteam/licenses/L001.txt'),notice.read_bytes())
    index=json.loads(z.read('ZSteam/licenses/INDEX.json'))
    self.assertEqual(index[0]['sha256'],hashlib.sha256(notice.read_bytes()).hexdigest())
    self.assertFalse(any('__pycache__' in n for n in z.namelist()))
    self.assertTrue(all(180+1+len(n)<260 for n in z.namelist()))
 def test_long_other_paths_fail_before_zip(self):
  with tempfile.TemporaryDirectory() as t:
   base=Path(t);p=self.kit(base);(p/('x'*65)).write_text('x');out=base/'out.zip'
   with self.assertRaisesRegex(ValueError,'budget'):package(p,out)
   self.assertFalse(out.exists())
 def test_refuses_replacement_and_case_collisions(self):
  with tempfile.TemporaryDirectory() as t:
   base=Path(t);p=self.kit(base);out=base/'out.zip';package(p,out);original=out.read_bytes()
   with self.assertRaises(ValueError):package(p,out)
   self.assertEqual(out.read_bytes(),original)
