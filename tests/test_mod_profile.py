import copy
import json
import unittest
from scripts.mod_profile import PROFILE, apply_profile


class ModProfileTests(unittest.TestCase):
    def setUp(self):
        self.profile = json.loads(PROFILE.read_text())
        self.rows = [dict(id=e['id'], original=e['original'], reference=e['reference'], target=e['base_target']) for e in self.profile['overrides']]

    def test_applies_without_changing_base(self):
        before = copy.deepcopy(self.rows)
        result, profile = apply_profile(self.rows)
        self.assertEqual(self.rows, before)
        self.assertEqual([r['target'] for r in result], [e['target'] for e in profile['overrides']])
        self.assertEqual(len(result), 28)

    def test_stale_base_rejected(self):
        self.rows[0]['target'] = 'Changed base translation'
        with self.assertRaises(ValueError):
            apply_profile(self.rows)

    def test_changed_identity_rejected(self):
        self.rows[0]['reference']['object_id'] = 0
        with self.assertRaises(ValueError):
            apply_profile(self.rows)

    def test_missing_entry_rejected(self):
        with self.assertRaises(ValueError):
            apply_profile(self.rows[1:])
