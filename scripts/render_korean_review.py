"""Render stable batch-order review numbers without changing translation catalogs."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def escape(text):
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('|', '&#124;').replace('\n', '<br>')


def main():
    number = 0
    links = []
    early = ['# Korean–English review: batches 001–007', '', 'R001–R944. Refreshed from current targets; review numbers preserved.', '', '| Review | Resource / path | Korean | English |', '| --- | --- | --- | --- |']
    for batch in sorted((ROOT / 'localization/en-US').glob('korean-batch-*.jsonl')) + [ROOT / 'localization/en-US/supplemental-display.jsonl']:
        rows = [json.loads(line) for line in batch.read_text().splitlines()]
        start = number + 1
        number += len(rows)
        output = ROOT / 'docs/review' / (batch.stem + '.md')
        lines = [f'# Korean–English review: {batch.stem}', '',
                 f'{len(rows)} draft occurrences, R{start:03d}–R{number:03d}. Korean is authoritative. Chinese was supporting context. Not a runtime-tested patch.', '',
                 'Controls are displayed literally. Exact whitespace and full notes are in the linked catalog entries. Names without glossary approval remain provisional.', '',
                 '| Review | Resource / path | Korean | English |',
                 '| --- | --- | --- | --- |']
        for i, row in enumerate(rows, 1):
            label = f'R{start+i-1:03d}'
            ref = row['reference']
            location = row['object_name'] + ' / ' + json.dumps(ref['path'], ensure_ascii=False)
            lines.append(f'| [{label}](../../localization/en-US/{batch.name}#L{i}) | {escape(location)} | {escape(row["original"])} | {escape(row["target"])} |')
        if batch.stem.startswith('korean-batch-') and int(batch.stem[-3:]) <= 7:
            early.extend(lines[8:])
            continue
        output.write_text('\n'.join(lines) + '\n')
        links.append(f'- [{batch.stem}: R{start:03d}–R{number:03d}]({output.name}) — {len(rows)} entries')
    (ROOT / 'docs/review/korean-english-batches-001-007.md').write_text('\n'.join(early) + '\n')
    index = ROOT / 'docs/review/README.md'
    index.write_text('# Translation review\n\nAll entries remain drafts. Send corrections by review number. Earlier review numbers are preserved.\n\n'
                     '- [Batches 001–007: R001–R944](korean-english-batches-001-007.md) — 944 entries\n'
                     + '\n'.join(links) + f'\n\nTotal: {number} occurrences. Metadata drafts are separate in [metadata-drafts.json](../../localization/en-US/metadata-drafts.json).\n')
    print(f'Rendered review index for {number} occurrences: {index}')


if __name__ == '__main__':
    main()
