import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from scripts.review.server import ReviewStore

class ReviewStoreTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name);self.page=self.root/'index.html';self.notes=self.root/'Suggestions'
        self.row=dict(id='R001',key='source-key',ko='한국어 /10d',en='English /10d',location='resource',batch='one')
        self.page.write_text('<script id="data" type="application/json">'+json.dumps([self.row])+'</script>')
        self.store=ReviewStore(self.page,self.notes)
        self.data=dict(id='R001',key='source-key',en='English /10d',suggestion='New English /10d\n```text\nexample',explanation='설명 </script>',request_id='a'*32,revision=None)
    def test_markdown_roundtrip_restart_and_idempotency(self):
        result=self.store.save(self.data);again=self.store.save(self.data)
        self.assertEqual(result,again);self.assertEqual(len(list(self.notes.glob('*.md'))),1)
        text=(self.notes/result['filename']).read_text();self.assertIn('## Explanation',text);self.assertIn('설명 </script>',text)
        recovered=ReviewStore(self.page,self.notes)
        self.assertEqual(recovered.latest['R001'],result)
        self.assertEqual(recovered.save(self.data),result)
    def test_new_revision_preserves_old_markdown(self):
        first=self.store.save(self.data)
        second=self.store.save(dict(self.data,request_id='b'*32,revision=first['request_id'],suggestion='Revised'))
        self.assertEqual(len(list(self.notes.glob('*.md'))),2)
        self.assertEqual(ReviewStore(self.page,self.notes).latest['R001'],second)
    def test_stale_revision_rejected_without_overwrite(self):
        self.store.save(self.data)
        with self.assertRaisesRegex(ValueError,'newer suggestion'):
            self.store.save(dict(self.data,request_id='b'*32))
        self.assertEqual(len(list(self.notes.glob('*.md'))),1)
    def test_changed_source_or_english_rejected(self):
        for change in [dict(key='different'),dict(en='updated English')]:
            with self.assertRaisesRegex(ValueError,'entry changed'):self.store.save(dict(self.data,**change))
        self.assertEqual(list(self.notes.iterdir()),[])
    def test_paths_empty_oversized_and_invalid_id_rejected(self):
        for change in [dict(id='../escape'),dict(request_id='../escape'),dict(suggestion='',explanation=' '),dict(suggestion='a'*20001),dict(explanation=[]),dict(request_id=None)]:
            with self.assertRaises(ValueError):self.store.save(dict(self.data,**change))
        self.assertEqual(list(self.notes.iterdir()),[])
    def test_write_failure_does_not_report_save(self):
        with patch('scripts.review.server.os.replace',side_effect=OSError('full')):
            with self.assertRaises(OSError):self.store.save(self.data)
        self.assertEqual(self.store.latest,{});self.assertEqual(list(self.notes.iterdir()),[])

if __name__=='__main__':unittest.main()
