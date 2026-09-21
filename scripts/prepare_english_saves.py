"""Create separate English display-name copies of gzip JSON saves; never overwrite."""
import argparse
import gzip
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIELDS = {'DialogueName', 'FullName', 'JobName'}


def convert(value, mapping, changes):
    if isinstance(value, dict):
        for key, item in value.items():
            if key in FIELDS and isinstance(item, str) and item in mapping:
                target = mapping[item]
                if target != item:
                    changes.append({'field': key, 'original': item, 'target': target})
                    value[key] = target
            else:
                convert(item, mapping, changes)
    elif isinstance(value, list):
        for item in value:
            convert(item, mapping, changes)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    source, output = args.source.resolve(), args.output.resolve()
    if output.exists() or source == output or source in output.parents:
        parser.error('Output must be new and outside source')
    if (ROOT / 'private').resolve() not in output.parents:
        parser.error('Output must be under private/')
    mapping = {}
    conflicts = set()
    for path in sorted((ROOT / 'localization/en-US').glob('korean-batch-*.jsonl')):
        for line in path.read_text().splitlines():
            row = json.loads(line)
            key, target = row['original'], row['target']
            if key in mapping and mapping[key] != target:
                conflicts.add(key)
            mapping[key] = target
    for key in conflicts:
        mapping.pop(key, None)
    mapping.update({'시라노': 'Cyrano', '시라노 번스타인': 'Cyrano Bernstein', '수련 검사': 'Apprentice Swordsman'})
    output.mkdir(parents=True)
    report = []
    for path in sorted(source.rglob('save_*.dat')):
        original = path.read_bytes()
        if not original.startswith(b'\x1f\x8b'):
            continue
        before = json.loads(gzip.decompress(original))
        after = json.loads(json.dumps(before))
        changes = []
        convert(after, mapping, changes)
        if not changes:
            continue
        dest = output / path.relative_to(source)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(gzip.compress(json.dumps(after, ensure_ascii=False, indent=2).encode(), mtime=0))
        assert json.loads(gzip.decompress(dest.read_bytes())) == after
        assert path.read_bytes() == original
        report.append({'file': str(path.relative_to(source)), 'changes': changes})
    (output / 'conversion-report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2))
    print(f'Prepared {len(report)} separate save copies; originals unchanged.')


if __name__ == '__main__':
    main()
