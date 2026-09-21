"""Check rejection of catalog corruption without requiring game files."""
import copy
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('english_catalog', Path(__file__).resolve().parents[1] / 'scripts/english_catalog.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class CatalogChecks(unittest.TestCase):
    def setUp(self):
        self.expected = {'sample': dict(id='sample', source='<sprite=20> 开启',
                                        references=[{'json_path': ['files', 0]}])}
        self.row = dict(self.expected['sample'], target='<sprite=20> On', status='draft')

    def test_valid_draft(self):
        self.assertEqual(module.check([self.row], self.expected), [])

    def test_missing_tag_rejected(self):
        self.row['target'] = 'On'
        self.assertTrue(module.check([self.row], self.expected))

    def test_changed_reference_rejected(self):
        row = copy.deepcopy(self.row)
        row['references'][0]['json_path'][-1] = 1
        self.assertTrue(module.check([row], self.expected))

    def test_missing_and_duplicate_entries_rejected(self):
        self.assertTrue(module.check([], self.expected))
        self.assertTrue(module.check([self.row, self.row], self.expected))

    def test_untranslated_target_cannot_be_reviewed(self):
        self.row.update(target='', status='reviewed')
        self.assertTrue(module.check([self.row], self.expected))


if __name__ == '__main__':
    unittest.main()
