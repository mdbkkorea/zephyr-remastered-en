"""Validate Korean-source draft identities and formatting, not translation quality."""
import argparse
import hashlib
from collections import Counter
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def approved_linebreak_change(row):
    path = ROOT / 'localization/en-US/linebreak-review.json'
    if not path.exists():
        return False
    digest = lambda text: hashlib.sha256(text.encode()).hexdigest()
    return any(r['id'] == row['id'] and
               r['original_sha256'] == digest(row['original']) and
               r['target_sha256'] == digest(row['target'])
               for r in json.loads(path.read_text()))


def tokens(text):
    # Space-delimited single-angle sign headings are also visible prose.
    # Real tags start immediately after '<' and remain checked verbatim.
    text = re.sub(r'(?<!<)< [^<>\n]+ >(?!>)', '< >', text)
    # Double-angle headings contain visible prose, not rich-text attributes.
    # Preserve their delimiters while allowing the heading itself to translate.
    return Counter(re.findall(r'<<|>>|(?<!<)<[^<>\n]+>|\{[^{}\n]+\}|%(?:\d+\$)?[-+0 #]*\d*(?:\.\d+)?[sdfiu]|/\d+[a-zA-Z]|/n|\n', text))


def check(rows, originals):
    errors, warnings, seen = [], [], set()
    for row in rows:
        key = row['id']
        if key in seen:
            errors.append(f'{key}: duplicate occurrence')
        seen.add(key)
        original = originals.get(key)
        if original is None or any(row.get(k) != v for k, v in original.items()):
            errors.append(f'{key}: original source or reference changed')
            continue
        target = row.get('target')
        if not isinstance(target, str) or not target.strip() or row.get('status') not in ('draft', 'reviewed'):
            errors.append(f'{key}: missing translation or invalid status')
            continue
        source_tokens, target_tokens = tokens(row['original']), tokens(target)
        if approved_linebreak_change(row):
            source_tokens.pop('/n', None)
            target_tokens.pop('/n', None)
        if source_tokens != target_tokens:
            errors.append(f'{key}: formatting or dialogue controls differ')
        # Delay controls disappear on screen; they do not separate words.
        # Resolve explicit line breaks first so /n/20dHello is not a false hit.
        if re.search(r'[A-Za-z0-9](?:/\d+d)+[A-Za-z0-9]', target.replace('/n', '\n')):
            errors.append(f'{key}: missing word space around dialogue delay')
        if re.search(r'[\u3400-\u9fff\uac00-\ud7a3]', target):
            errors.append(f'{key}: Korean or Chinese remains in target')
        particle_codes = re.findall(r'\^p[a-z]', row['original'])
        if particle_codes:
            warnings.append(f'{key}: Korean particle behavior requires runtime verification: {particle_codes}')
            if row['status'] != 'draft' or not any('particle' in note for note in row.get('notes', [])):
                errors.append(f'{key}: particle handling must remain an explicitly flagged draft')
    return errors, warnings


def read_rows(path):
    return [json.loads(line) for line in path.read_text(encoding='utf-8').splitlines()]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('batch', type=Path)
    parser.add_argument('--source', type=Path, default=ROOT / 'private/korean-aligned.jsonl')
    args = parser.parse_args()
    rows = read_rows(args.batch)
    errors, warnings = check(rows, {r['id']: r for r in read_rows(args.source)})
    print(json.dumps({'draft_occurrences': len(rows), 'unique_original_strings': len({r['original'] for r in rows}),
                      'errors': errors, 'warnings': warnings, 'installable_english_patch': False}, indent=2))
    raise SystemExit(bool(errors))
