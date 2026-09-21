"""Audit Korean drafts and rebuild a PRIVATE, non-installable English test stage.

Only Korean-source target strings are applied. No Chinese structural, texture,
font, or metadata edits are imported. Never writes into the source game.
"""
import argparse
from collections import defaultdict
import copy
import gzip
import hashlib
import json
from pathlib import Path
import re
import struct
import sys
import zlib

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from engine.catalog import Catalog
from engine.patch_data import assign
from scripts.check_korean_batch import check, read_rows
from scripts.english_metadata import translate_metadata


def digest(data):
    return hashlib.sha256(data).hexdigest()


def beneath(root, relative):
    path = (root / relative).resolve()
    if root not in path.parents:
        raise ValueError('Path escapes root: ' + str(relative))
    return path


def value_at(tree, path):
    for key in path:
        tree = tree[key]
    return tree


def audit(source, drafts, particle_review=None):
    originals = {r['id']: r for r in source}
    if len(originals) != len(source):
        raise ValueError('Duplicate source IDs')
    errors, warnings = check(drafts, originals)
    for r in drafts:
        s, t = r['original'], r['target']
        if not isinstance(t, str):
            continue
        for pattern in (r'/\d+[a-zA-Z]|/n', r'^\s*', r'\s*$', r'/n(\s*)'):
            if re.findall(pattern, s) != re.findall(pattern, t):
                errors.append(r['id'] + ': ordered controls or whitespace changed')
        # Preserve key icons and other caret controls; only particle removal
        # is a known draft exception, never silently allowed into this stage.
        if re.findall(r'\^(?!p[a-z])\w+', s) != re.findall(r'\^(?!p[a-z])\w+', t):
            errors.append(r['id'] + ': non-particle caret controls changed')
    ids = {r['id'] for r in drafts}
    missing = [r for r in source if r['contains_korean'] and r['id'] not in ids]
    particles = [r['id'] for r in drafts if re.search(r'\^p[a-z]', r['original'])]
    resolved = []
    if particle_review:
        decisions = {r['id']: r for r in particle_review['rows']}
        for r in drafts:
            if r['id'] not in particles or r['id'] not in decisions:
                continue
            decision = decisions[r['id']]
            if (digest(r['original'].encode()) != decision['original_sha256'] or
                    digest(r['target'].encode()) != decision['target_sha256'] or
                    re.search(r'\^p[a-z]', r['target'])):
                errors.append(r['id'] + ': particle review no longer matches translation')
            else:
                resolved.append(r['id'])
        warnings = [w for w in warnings if w.split(':')[0] not in resolved]
    return {
        'translated_occurrences': len(drafts),
        'remaining_aligned_korean_occurrences': len(missing),
        'errors': errors, 'warnings': warnings,
        'particle_drafts_excluded_from_stage': [key for key in particles if key not in resolved],
        'particle_static_review': particle_review if resolved else None,
        'particle_static_reviewed_occurrences': len(resolved),
        'scope': 'Aligned simple string edits only; not a complete game inventory',
        'installable_english_patch': False,
        'unresolved_release_requirements': [
            'Complete remaining Korean translations',
            'Inventory text outside simple patch edits, including IL2CPP literals',
            'Verify Korean particle handling in the renderer',
            'Check original font coverage and English layout',
            'Run the English game from a separate full copy',
        ],
    }


def bundle_crc(data):
    from UnityPy.files import BundleFile
    from UnityPy.streams import EndianBinaryReader

    class CRCBundle(BundleFile):
        def read_fs(self, reader):
            nodes, blocks = super().read_fs(reader)
            self.crc = zlib.crc32(blocks.bytes) & 0xFFFFFFFF
            return nodes, blocks

    return CRCBundle(EndianBinaryReader(data), None).crc


def stage(game, output, source, drafts, patch, report):
    import UnityPy
    import spooky

    game, output = game.resolve(), output.resolve()
    private = (ROOT / 'private').resolve()
    if private not in output.parents:
        raise ValueError('Test stages must be under this repository\'s ignored private/')
    if game == output or game in output.parents or output in game.parents:
        raise ValueError('Source and output must not overlap')
    if output.exists():
        raise ValueError('Output exists; refusing to overwrite')
    if report['errors']:
        raise ValueError('Invalid draft catalog')

    # Particle-bearing drafts remain original Korean in the experimental stage.
    eligible = [r for r in drafts if r['id'] not in report['particle_drafts_excluded_from_stage']]
    grouped = defaultdict(list)
    for r in eligible:
        grouped[r['reference']['file']].append(r)
    patch_files = {f['path']: f for f in patch['files']}
    catalog_item = next(f for f in patch['files'] if f['kind'] == 'catalog')
    hash_item = next(f for f in patch['files'] if f['kind'] == 'catalog_hash')
    checked = {}
    if report.get('particle_static_review'):
        proof = report['particle_static_review']
        relative = proof['binary_file']
        actual_hash = digest(beneath(game, relative).read_bytes())
        if actual_hash != proof['binary_sha256']:
            raise ValueError('Particle renderer binary hash mismatch')
        checked[relative] = actual_hash

    def verified(relative):
        path = beneath(game, relative)
        data = path.read_bytes()
        expected = patch_files[relative]['before_sha256']
        if digest(data) != expected:
            raise ValueError('Original hash mismatch: ' + relative)
        checked[relative] = digest(data)
        return data

    # Fail before writing anything if the input version or original catalog hash differs.
    catalog_raw = bytearray(verified(catalog_item['path']))
    original_hash = verified(hash_item['path']).decode('ascii')
    if spooky.hash128(bytes(catalog_raw)).to_bytes(16, 'little').hex() != original_hash:
        raise ValueError('Original catalog.hash algorithm check failed')
    entries = Catalog(catalog_raw).bundles()
    by_name = defaultdict(list)
    for e in entries:
        by_name[Path(e['internal_id'].replace('\\', '/')).name].append(e)
    for relative in grouped:
        data = verified(relative)
        if relative.endswith('.bundle'):
            matches = by_name[Path(relative).name]
            if not matches or any(e['crc'] != bundle_crc(data) or e['size'] != len(data) for e in matches):
                raise ValueError('Original bundle CRC/size does not match catalog: ' + relative)
    schema_cache = {}

    def schema(edit):
        spec = edit['schema']
        if not spec:
            return None
        key = (spec['file'], spec['sf'], spec['pid'])
        if key not in schema_cache:
            env = UnityPy.load(verified(spec['file']))
            schema_cache[key] = next(o.serialized_type.node for o in env.objects
                                     if o.assets_file.name == spec['sf'] and o.path_id == spec['pid'])
        return schema_cache[key]

    output.mkdir(parents=True)
    (output / 'NOT-INSTALLABLE.txt').write_text(
        'Private English rebuild experiment. See build-report.json for coverage. '
        'No runtime validation. '
        'Do not copy over the Steam installation.\n', encoding='utf-8')
    outputs = []
    for relative, rows in grouped.items():
        env = UnityPy.load(str(beneath(game, relative)))
        objects = {(o.assets_file.name, o.path_id): o for o in env.objects}
        raw_before = {key: digest(obj.get_raw_data()) for key, obj in objects.items()}
        edits = {(c['sf'], c['pid']): c for c in patch_files[relative]['changes']}
        by_object = defaultdict(list)
        for r in rows:
            by_object[(r['reference']['serialized_file'], r['reference']['object_id'])].append(r)
        expected_trees = {}
        nodes = {}
        for key, object_rows in by_object.items():
            obj, edit = objects[key], edits[key]
            if raw_before[key] != edit['before_raw_sha256']:
                raise ValueError('Original object hash mismatch')
            node = schema(edit)
            tree = obj.read_typetree(nodes=node)
            for r in object_rows:
                path = r['reference']['path']
                if value_at(tree, path) != r['original']:
                    raise ValueError('Korean source differs from live original: ' + r['id'])
                tree = assign(tree, path, r['target'])
            obj.save_typetree(tree, nodes=node)
            expected_trees[key], nodes[key] = copy.deepcopy(tree), node
        destination = beneath(output, relative)
        destination.parent.mkdir(parents=True, exist_ok=True)
        if relative.endswith('.bundle'):
            env.save(pack='lz4', out_path=str(destination.parent))
        else:
            destination.write_bytes(env.file.save())
        result = destination.read_bytes()
        reopened = UnityPy.load(str(destination))
        actual = {(o.assets_file.name, o.path_id): o for o in reopened.objects}
        if set(actual) != set(objects):
            raise ValueError('Object identities changed during rebuild')
        for key, obj in actual.items():
            if key in expected_trees:
                if obj.read_typetree(nodes=nodes[key]) != expected_trees[key]:
                    raise ValueError('Reopened translated object differs from expected tree')
            elif digest(obj.get_raw_data()) != raw_before[key]:
                raise ValueError('Unedited object data changed')
        record = {'file': relative, 'sha256': digest(result), 'size': len(result),
                  'english_occurrences': len(rows), 'object_readback': 'passed'}
        if relative.endswith('.bundle'):
            crc = bundle_crc(result)
            # Hash128 here is a new content-addressed cache identity, not a claim
            # to reproduce Unity's editor build hash. CRC validates bundle data.
            cache_hash = hashlib.md5(result).digest()
            for e in by_name[destination.name]:
                offset = e['hash_offset']
                if offset < 0 or offset + 16 > len(catalog_raw):
                    raise ValueError('Invalid catalog Hash128 offset')
                catalog_raw[offset:offset + 16] = cache_hash
                struct.pack_into('<I', catalog_raw, e['crc_offset'], crc)
                struct.pack_into('<I', catalog_raw, e['size_offset'], len(result))
            record.update(crc=crc, cache_hash128=cache_hash.hex())
        outputs.append(record)
        print('Verified English rebuild: ' + Path(relative).name, flush=True)

    metadata_drafts = json.loads((ROOT / 'localization/en-US/metadata-drafts.json').read_text())
    metadata_files = {r['reference']['file'] for r in metadata_drafts}
    for relative in metadata_files:
        rows = [r for r in metadata_drafts if r['reference']['file'] == relative]
        rebuilt = translate_metadata(verified(relative), rows)
        destination = beneath(output, relative)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(rebuilt)
        if destination.read_bytes() != rebuilt:
            raise ValueError('Metadata readback mismatch')
        outputs.append({'file': relative, 'sha256': digest(rebuilt), 'size': len(rebuilt),
                        'english_literals': len(rows), 'fixed_slot_readback': 'passed'})

    new_entries = Catalog(catalog_raw).bundles()
    for record in outputs:
        if 'crc' not in record:
            continue
        matches = [e for e in new_entries if Path(e['internal_id'].replace('\\', '/')).name == Path(record['file']).name]
        if not matches or any(e['crc'] != record['crc'] or e['size'] != record['size'] for e in matches):
            raise ValueError('Updated catalog round-trip mismatch')
    cat_path = beneath(output, catalog_item['path'])
    cat_path.parent.mkdir(parents=True, exist_ok=True)
    cat_path.write_bytes(catalog_raw)
    cat_hash = spooky.hash128(bytes(catalog_raw)).to_bytes(16, 'little').hex()
    beneath(output, hash_item['path']).write_text(cat_hash, encoding='ascii')
    for relative, original_digest in checked.items():
        if digest(beneath(game, relative).read_bytes()) != original_digest:
            raise ValueError('Original changed during build')
    report.update(staged_occurrences=len(eligible), outputs=outputs,
                  original_files_unchanged=True, catalog_hash=cat_hash,
                  runtime_tested=False, installable_english_patch=False)
    (output / 'build-report.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, default=ROOT / 'private/korean-aligned.jsonl')
    parser.add_argument('--game', type=Path)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--report', type=Path)
    parser.add_argument('--experimental-incomplete-stage', action='store_true',
                        help='Build non-installable private resources; preserve missing Korean and exclude particles')
    args = parser.parse_args()
    source = read_rows(args.source)
    drafts = [r for path in sorted((ROOT / 'localization/en-US').glob('korean-batch-*.jsonl'))
              for r in read_rows(path)]
    supplemental = ROOT / 'localization/en-US/supplemental-display.jsonl'
    if supplemental.exists():
        source += read_rows(ROOT / 'private/supplemental-source.jsonl')
        drafts += read_rows(supplemental)
    proof_path = ROOT / 'localization/en-US/particle-review.json'
    particle_review = json.loads(proof_path.read_text()) if proof_path.exists() else None
    report = audit(source, drafts, particle_review)
    if args.output:
        if not args.experimental_incomplete_stage or not args.game:
            parser.error('Only an explicit experimental stage with --game is supported; no installable build exists yet')
        patch = json.loads(gzip.decompress((ROOT / 'payload/patch.json.gz').read_bytes()))
        if supplemental.exists():
            evidence = json.loads((ROOT / 'private/inventory-evidence.json').read_text())
            files = {f['path']: f for f in patch['files']}
            wanted = {(r['reference']['file'], r['reference']['serialized_file'], r['reference']['object_id'])
                      for r in read_rows(supplemental)}
            for obj in evidence['objects']:
                if (obj['file'], obj['sf'], obj['pid']) not in wanted:
                    continue
                item = files.get(obj['file'])
                if item is None:
                    item = dict(path=obj['file'], kind='unity', before_sha256=evidence['file_hashes'][obj['file']], changes=[])
                    patch['files'].append(item)
                    files[obj['file']] = item
                if item['before_sha256'] != evidence['file_hashes'][obj['file']]:
                    raise ValueError('Supplemental inventory file hash mismatch')
                if not any(c['sf'] == obj['sf'] and c['pid'] == obj['pid'] for c in item['changes']):
                    item['changes'].append({k: v for k, v in obj.items() if k != 'file'})
        report = stage(args.game, args.output, source, drafts, patch, report)
    if args.report:
        target = args.report.resolve()
        if (ROOT / 'private').resolve() not in target.parents:
            parser.error('Reports must be under ignored private/')
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, indent=2))
    return bool(report['errors'])


if __name__ == '__main__':
    raise SystemExit(main())
