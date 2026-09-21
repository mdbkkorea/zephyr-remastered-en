"""Extract and check an English working catalog; never writes an install payload."""
import argparse
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / 'localization/en-US/catalog.jsonl'
SOURCE = ROOT / 'payload/patch.json.gz'


def chinese(value):
    return any('\u3400' <= c <= '\u9fff' for c in value)


def leaves(value, path=()):
    if isinstance(value, dict):
        for key, child in value.items():
            yield from leaves(child, path + (key,))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from leaves(child, path + (index,))
    elif isinstance(value, str) and chinese(value):
        yield path, value


def extract():
    patch = json.loads(gzip.decompress(SOURCE.read_bytes()))
    entries = {}
    for path, source in leaves(patch):
        key = hashlib.sha256(source.encode()).hexdigest()
        entry = entries.setdefault(key, dict(id=key, source=source, target='',
                                              status='untranslated', references=[]))
        ref = {'json_path': list(path)}
        if path[0] == 'files':
            item = patch['files'][path[1]]
            ref['file'] = item['path']
            if len(path) > 3 and path[2] == 'changes':
                change = item['changes'][path[3]]
                ref.update(serialized_file=change['sf'], object_id=change['pid'])
        entry['references'].append(ref)
    return entries


def tokens(text):
    # Conservative check of rich-text tags, format fields and printf placeholders.
    return Counter(re.findall(r'<[^>\n]+>|\{[^{}\n]+\}|%(?:\d+\$)?[-+0 #]*\d*(?:\.\d+)?[sdfiu]', text))


def check(rows, expected):
    errors = []
    seen = set()
    for row in rows:
        key = row['id']
        if key in seen:
            errors.append(f'{key}: duplicate ID')
        seen.add(key)
        original = expected.get(key)
        if original is None or any(row.get(k) != original[k] for k in ('source', 'references')):
            errors.append(f'{key}: source or references changed')
        status, target = row.get('status'), row.get('target')
        if status not in ('untranslated', 'draft', 'reviewed') or not isinstance(target, str):
            errors.append(f'{key}: invalid target or status')
            continue
        if bool(target) != (status != 'untranslated'):
            errors.append(f'{key}: status does not match target')
        if target and (chinese(target) or tokens(row['source']) != tokens(target)):
            errors.append(f'{key}: Chinese remains or formatting tokens differ')
    if seen != set(expected):
        errors.append('Catalog IDs do not match this source payload')
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('extract', 'check'))
    args = parser.parse_args()
    expected = extract()
    if args.command == 'extract':
        if CATALOG.exists():
            parser.error('Catalog exists; refusing to overwrite translation work')
        seeds = json.loads((CATALOG.parent / 'menu-drafts.json').read_text(encoding='utf-8'))
        unknown = set(seeds) - {e['source'] for e in expected.values()}
        if unknown:
            parser.error(f'Seed strings missing from source: {sorted(unknown)}')
        for entry in expected.values():
            if entry['source'] in seeds:
                entry.update(target=seeds[entry['source']], status='draft')
        CATALOG.write_text(''.join(json.dumps(e, ensure_ascii=False) + '\n' for e in expected.values()), encoding='utf-8')
    rows = [json.loads(line) for line in CATALOG.read_text(encoding='utf-8').splitlines()]
    errors = check(rows, expected)
    report = dict(source_payload_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
                  unique_strings=len(rows), occurrences=sum(len(e['references']) for e in rows),
                  statuses=dict(Counter(e['status'] for e in rows)), errors=errors,
                  installable_english_patch=False)
    print(json.dumps(report, indent=2))
    if errors:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
