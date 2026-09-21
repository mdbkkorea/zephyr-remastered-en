import copy
import hashlib
from pathlib import Path
import tempfile
import unittest

from scripts.build_english_stage import ROOT, audit, beneath, stage


def sample(source='안녕/10d/n친구', target='Hello/10d/nfriend'):
    original = dict(id='one', original=source, contains_korean=True,
                    chinese_reference='你好', object_name='fixture', reference={},
                    patch_json_path=[])
    draft = dict(original, target=target, status='draft', notes=[])
    return original, draft


class EnglishStageTests(unittest.TestCase):
    def test_decorative_heading_translates_but_delimiters_and_tags_stay(self):
        original, draft = sample('<< 리브레빌 >>', '<< Libreville >>')
        self.assertEqual(audit([original], [draft])['errors'], [])
        draft['target'] = 'Libreville'
        self.assertTrue(audit([original], [draft])['errors'])

    def test_spaced_single_angle_sign_heading(self):
        original, draft = sample('< 화룡의 굴 >/n위험', "< Fire Dragon's Cave >/nDanger")
        self.assertEqual(audit([original], [draft])['errors'], [])
        draft['target'] = "Fire Dragon's Cave/nDanger"
        self.assertTrue(audit([original], [draft])['errors'])
        original, draft = sample('<b>위험</b>', '<i>Danger</i>')
        self.assertTrue(audit([original], [draft])['errors'])
        original, draft = sample('<color=red>마을</color>', '<color=blue>Town</color>')
        self.assertTrue(audit([original], [draft])['errors'])

    def test_missing_korean_and_particle_drafts_remain_visible(self):
        original, draft = sample('{0}^pd 획득', 'Obtained {0}')
        draft['notes'] = ['particle omission requires runtime verification']
        missing = dict(original, id='two', original='아직 번역하지 않음')
        report = audit([original, missing], [draft])
        self.assertEqual(report['remaining_aligned_korean_occurrences'], 1)
        self.assertEqual(report['particle_drafts_excluded_from_stage'], ['one'])
        self.assertFalse(report['installable_english_patch'])
        self.assertEqual(report['errors'], [])

    def test_particle_review_is_bound_to_exact_source_and_target(self):
        original, draft = sample('{0}^pd 획득', 'Obtained {0}')
        draft['notes'] = ['particle omission statically reviewed']
        proof = {'rows': [{'id': 'one',
                  'original_sha256': hashlib.sha256(original['original'].encode()).hexdigest(),
                  'target_sha256': hashlib.sha256(draft['target'].encode()).hexdigest()}]}
        report = audit([original], [draft], proof)
        self.assertEqual(report['particle_drafts_excluded_from_stage'], [])
        self.assertEqual(report['warnings'], [])
        draft['target'] = 'Found {0}'
        self.assertTrue(audit([original], [draft], proof)['errors'])

    def test_reordered_controls_are_rejected_even_with_equal_counts(self):
        original, draft = sample('안녕/10d/20d', 'Hello/20d/10d')
        self.assertTrue(audit([original], [draft])['errors'])

    def test_key_icon_loss_is_rejected(self):
        original, draft = sample('^k_f10key 회복', 'Restore')
        self.assertTrue(audit([original], [draft])['errors'])

    def test_original_reference_tampering_is_rejected(self):
        original, draft = sample()
        draft['reference'] = {'file': 'other'}
        self.assertTrue(audit([original], [draft])['errors'])

    def test_boundary_and_newline_whitespace_are_checked(self):
        original, draft = sample(' 안녕/n 친구 ', 'Hello/nfriend')
        self.assertTrue(audit([original], [draft])['errors'])

    def test_path_traversal_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                beneath(Path(tmp).resolve(), '../escape')

    def test_source_output_overlap_is_rejected_before_writes(self):
        folder = ROOT / 'private' / 'fixture-no-write'
        with self.assertRaisesRegex(ValueError, 'overlap'):
            stage(folder, folder / 'output', [], [], {}, {'errors': []})
        self.assertFalse(folder.exists())


if __name__ == '__main__':
    unittest.main()
