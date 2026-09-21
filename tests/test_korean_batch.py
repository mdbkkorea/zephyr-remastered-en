import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('check_korean_batch', Path(__file__).resolve().parents[1] / 'scripts/check_korean_batch.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class KoreanBatchChecks(unittest.TestCase):
    def test_dropped_dialogue_delay_is_rejected(self):
        source = {'id': 'a', 'original': '/2c안녕/10d/n{0}', 'reference': {'object_id': 1}}
        row = dict(source, target='/2cHello/n{0}', status='draft')
        self.assertTrue(module.check([row], {'a': source})[0])
        row['target'] = '/2cHello/10d/n{0}'
        self.assertEqual(module.check([row], {'a': source})[0], [])

    def test_changing_source_or_duplicate_reference_is_rejected(self):
        source = {'id': 'a', 'original': '안녕', 'reference': {'object_id': 1}}
        row = dict(source, target='Hello', status='draft')
        self.assertTrue(module.check([row, row], {'a': source})[0])
        row['reference'] = {'object_id': 2}
        self.assertTrue(module.check([row], {'a': source})[0])

    def test_particle_removal_is_explicit_and_not_reviewed(self):
        source = {'id': 'a', 'original': '{0}^pd 획득하였다.'}
        row = dict(source, target='Obtained {0}.', status='draft', notes=['Korean particle behavior needs testing.'])
        errors, warnings = module.check([row], {'a': source})
        self.assertEqual(errors, [])
        self.assertEqual(len(warnings), 1)
        row['status'] = 'reviewed'
        self.assertTrue(module.check([row], {'a': source})[0])
