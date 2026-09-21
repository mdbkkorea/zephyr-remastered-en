"""Read verified local originals and align simple string edits with their source.

Does not write to the game or produce an installable patch. Non-string and
structural edits are counted explicitly rather than guessed.
"""
import argparse
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path

import UnityPy

ROOT = Path(__file__).resolve().parents[1]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def resolve(root, relative):
    path = (root / relative).resolve()
    if root not in path.parents:
        raise ValueError('Source path escapes game directory')
    return path


def extract(game, destination):
    game = game.resolve()
    destination = destination.resolve()
    if destination == game or game in destination.parents:
        raise ValueError('Output must be outside the original game directory')
    if destination.exists():
        raise ValueError('Output exists; refusing to overwrite')
    payload = (ROOT / 'payload/patch.json.gz').read_bytes()
    patch = json.loads(gzip.decompress(payload))
    rows, files, counts = [], [], Counter()
    for fi, item in enumerate(patch['files']):
        source = resolve(game, item['path'])
        digest = sha(source.read_bytes())
        if digest != item['before_sha256']:
            raise ValueError('Original file hash mismatch: ' + item['path'])
        files.append({'file': item['path'], 'sha256': digest})
        if item['kind'] != 'unity':
            counts['non_unity_files'] += 1
            continue
        env = UnityPy.load(str(source))
        objects = {(o.assets_file.name, o.path_id): o for o in env.objects}
        for ci, change in enumerate(item['changes']):
            obj = objects[(change['sf'], change['pid'])]
            if sha(obj.get_raw_data()) != change['before_raw_sha256']:
                raise ValueError('Original object hash mismatch')
            eligible = [(oi, op) for oi, op in enumerate(change['ops'])
                        if op['kind'] == 'set' and isinstance(op['value'], str)]
            counts['other_operations'] += len(change['ops']) - len(eligible)
            if not eligible:
                continue
            if change['schema']:
                spec = change['schema']
                schema_env = UnityPy.load(str(resolve(game, spec['file'])))
                node = next(o.serialized_type.node for o in schema_env.objects
                            if o.assets_file.name == spec['sf'] and o.path_id == spec['pid'])
                tree = obj.read_typetree(nodes=node)
            else:
                tree = obj.read_typetree()
            for oi, op in eligible:
                original = tree
                for part in op['path']:
                    original = original[part]
                if not isinstance(original, str):
                    counts['non_string_originals'] += 1
                    continue
                reference = {'file': item['path'], 'serialized_file': change['sf'],
                             'object_id': change['pid'], 'path': op['path']}
                identity = json.dumps(reference, sort_keys=True, ensure_ascii=False)
                rows.append({'id': sha(identity.encode()),
                             'original': original,
                             'contains_korean': any('\uac00' <= c <= '\ud7a3' for c in original),
                             'chinese_reference': op['value'],
                             'object_name': tree.get('m_Name', ''),
                             'reference': reference,
                             'patch_json_path': ['files', fi, 'changes', ci, 'ops', oi, 'value']})
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in rows), encoding='utf-8')
    report = {'payload_sha256': sha(payload), 'unitypy_version': UnityPy.__version__,
              'verified_original_files': files, 'aligned_string_occurrences': len(rows),
              'korean_occurrences': sum(r['contains_korean'] for r in rows),
              'unique_korean_strings': len({r['original'] for r in rows if r['contains_korean']}),
              'excluded': dict(counts), 'installable_english_patch': False}
    destination.with_suffix('.report.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps({k: v for k, v in report.items() if k != 'verified_original_files'}, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--game', required=True, type=Path)
    parser.add_argument('--output', type=Path, default=ROOT / 'private/korean-aligned.jsonl')
    args = parser.parse_args()
    extract(args.game, args.output)
