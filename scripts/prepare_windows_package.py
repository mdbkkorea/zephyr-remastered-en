"""Create a private, self-contained desktop build kit from a validated English stage."""
import argparse
import gzip
import hashlib
import json
import shutil
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def sha(data):
    return hashlib.sha256(data).hexdigest()

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--game', type=Path, required=True)
    parser.add_argument('--stage', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    if output.exists() or (ROOT / 'private').resolve() not in output.parents:
        parser.error('Use a new output directory under private/')
    report = json.loads((args.stage / 'build-report.json').read_text())
    if report['errors'] or report['warnings'] or not report['original_files_unchanged']:
        raise ValueError('Stage validation did not pass.')
    upstream = json.loads(gzip.decompress((ROOT / 'payload/patch.json.gz').read_bytes()))
    if sha((args.game / 'ZephyrRemastered.exe').read_bytes()) != upstream['exe_sha256']:
        raise ValueError('Executable mismatch.')
    output.mkdir(parents=True)
    payload = output / 'payload'
    payload.mkdir()
    manifest = dict(format=1, language='en-US', game_build=upstream['game_build'], exe_sha256=upstream['exe_sha256'], dependencies=upstream['dependencies'], files=[])
    proof = json.loads((ROOT/'localization/en-US/particle-review.json').read_text())
    manifest['dependencies'].append({'path':proof['binary_file'], 'sha256':proof['binary_sha256']})
    if (args.stage/'ZephyrRemastered_Data/StreamingAssets/aa/catalog.hash').exists():
        catalog_hash_path = args.stage/'ZephyrRemastered_Data/StreamingAssets/aa/catalog.hash'
    else:
        catalog_hash_path = next((args.stage/'ZephyrRemastered_Data').rglob('catalog.hash'))
    if catalog_hash_path.read_text().strip() != report['catalog_hash']:
        raise ValueError('Addressables catalog hash changed.')
    expected = {r['file']: r['sha256'] for r in report['outputs']}
    stage_files = sorted(p for p in (args.stage / 'ZephyrRemastered_Data').rglob('*') if p.is_file())
    upstream_hashes = {r['path']:r['before_sha256'] for r in upstream['files']}
    inventory = json.loads((ROOT / 'private/inventory-evidence.json').read_text())['file_hashes']
    for index, path in enumerate(stage_files):
        name = path.relative_to(args.stage).as_posix()
        before = (args.game / name).read_bytes()
        after = path.read_bytes()
        original_hash = upstream_hashes.get(name, inventory.get(name))
        if not original_hash or sha(before) != original_hash:
            raise ValueError('Unverified original: ' + name)
        if name in expected and sha(after) != expected[name]:
            raise ValueError('Stage file changed: ' + name)
        delta = bytes(a ^ b for a,b in zip(before[:len(after)].ljust(len(after),b'\0'), after))
        blob = zlib.compress(delta, 9)
        delta_name = f'{index:03d}.delta'
        (payload / delta_name).write_bytes(blob)
        manifest['files'].append(dict(path=name,before_sha256=sha(before),after_sha256=sha(after),after_size=len(after),delta=delta_name,delta_sha256=sha(blob)))
    for dep in manifest['dependencies']:
        if sha((args.game / dep['path']).read_bytes()) != dep['sha256']:
            raise ValueError('Dependency mismatch.')
    (payload / 'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    for path in (ROOT / 'windows').iterdir():
        if path.is_file(): shutil.copy2(path, output/path.name)
    shutil.copy2(ROOT/'LICENSE',output/'LICENSE')
    (output/'tests').mkdir()
    shutil.copy2(ROOT/'tests/test_windows_patcher.py',output/'tests/test_windows_patcher.py')
    shutil.copy2(ROOT/'tests/test_patcher_platform.py',output/'tests/test_patcher_platform.py')
    mapping = {}
    conflicts = set()
    for catalog in sorted((ROOT/'localization/en-US').glob('korean-batch-*.jsonl')):
        for line in catalog.read_text().splitlines():
            row = json.loads(line)
            key, target = row['original'], row['target']
            if key in mapping and mapping[key] != target: conflicts.add(key)
            mapping[key] = target
    mapping = {k:v for k,v in mapping.items() if k not in conflicts and len(k)<100}
    mapping.update({'시라노':'Cyrano','시라노 번스타인':'Cyrano Bernstein','수련 검사':'Apprentice Swordsman'})
    (payload/'save-names.json').write_text(json.dumps(mapping,ensure_ascii=False))
    hashes = {p.name:sha(p.read_bytes()) for p in payload.iterdir() if p.is_file()}
    (output/'english_trust.py').write_text('HASHES = '+repr(hashes)+'\n')
    shutil.copytree(ROOT/'licenses/python',output/'licenses/python')
    shutil.make_archive(str(output),'zip',root_dir=output.parent,base_dir=output.name)
    print(f'Created {output}.zip with {len(manifest["files"])} deltas. No full game copy included.')

if __name__ == '__main__':
    main()
