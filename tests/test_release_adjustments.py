import hashlib
import json
import struct
import unittest
from pathlib import Path
from unittest.mock import patch
from scripts.release_adjustments import patch_reveal, apply_layout
from scripts.check_korean_batch import approved_linebreak_change, check

class ReleaseAdjustmentTests(unittest.TestCase):
    def test_reveal_is_hash_locked_and_only_changes_delay(self):
        original=b'prefix'+bytes.fromhex('c74118295c8f3d')+b'suffix'
        with patch('scripts.release_adjustments.REVEAL_INPUTS', {hashlib.sha256(original).hexdigest():6}):
            result=patch_reveal(original)
            self.assertEqual(result, b'prefix'+bytes.fromhex('c74118')+struct.pack('<f',0.028)+b'suffix')
            with self.assertRaises(ValueError):patch_reveal(original+b'changed')
            with self.assertRaises(ValueError):patch_reveal(result)
    def test_layout_is_specific_and_fails_on_unexpected_label(self):
        data=json.loads(Path('localization/auto-advance-layout.json').read_text());r=data['changes'][0]['reference']
        tree={'m_text':'<sprite=20> Auto-Advance','m_fontSize':22.0,'m_fontSizeBase':22.0}
        self.assertEqual(apply_layout(tree,r['file'],(r['serialized_file'],r['object_id'])),2)
        self.assertEqual(tree['m_fontSize'],16.0)
        with self.assertRaises(ValueError):apply_layout(tree,r['file'],(r['serialized_file'],r['object_id']))
        self.assertEqual(apply_layout(tree,'other',('other',0)),0)
    def test_linebreak_approval_does_not_allow_changed_pause_or_wording(self):
        approved=json.loads(Path('localization/en-US/linebreak-review.json').read_text())[0]
        rows=[json.loads(l) for p in Path('localization/en-US').glob('korean-batch-*.jsonl') for l in p.read_text().splitlines()]
        row=next(r for r in rows if r['id']==approved['id'])
        self.assertTrue(approved_linebreak_change(row))
        changed=dict(row,target=row['target']+'/20d')
        self.assertFalse(approved_linebreak_change(changed))
        self.assertTrue(check([changed],{row['id']:{'id':row['id'],'original':row['original']}})[0])
