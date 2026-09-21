import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('english_saves', Path(__file__).resolve().parents[1] / 'scripts/prepare_english_saves.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class SaveDisplayTests(unittest.TestCase):
    def test_only_display_fields_change(self):
        data = {'Units': [{'DialogueName': '시라노', 'FullName': '시라노 번스타인', 'JobName': '수련 검사', 'ID4': '시라노', 'Level': 16, 'CurHp': 721}], 'Quest': '시라노'}
        changes = []
        module.convert(data, {'시라노': 'Cyrano', '시라노 번스타인': 'Cyrano Bernstein', '수련 검사': 'Apprentice Swordsman'}, changes)
        self.assertEqual(len(changes), 3)
        self.assertEqual(data['Units'][0], {'DialogueName': 'Cyrano', 'FullName': 'Cyrano Bernstein', 'JobName': 'Apprentice Swordsman', 'ID4': '시라노', 'Level': 16, 'CurHp': 721})
        self.assertEqual(data['Quest'], '시라노')
        module.convert(data, {'시라노': 'Cyrano'}, changes)
        self.assertEqual(len(changes), 3)

    def test_unknown_names_are_preserved(self):
        data = {'DialogueName': 'custom name', 'FullName': None}
        changes = []
        module.convert(data, {}, changes)
        self.assertEqual(data, {'DialogueName': 'custom name', 'FullName': None})
        self.assertFalse(changes)
