"""Render small, script-free HTML and UTF-8 text reviews for mobile file previews."""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'private/Zephyr-Mobile-Review'


def main():
    OUT.mkdir(exist_ok=True)
    rows = []
    for p in sorted((ROOT/'localization/en-US').glob('korean-batch-*.jsonl')) + [ROOT/'localization/en-US/supplemental-display.jsonl']:
        for line in p.read_text().splitlines():
            r = json.loads(line)
            rows.append(dict(id=f'R{len(rows)+1:03d}', batch=p.stem, ko=r['original'], en=r['target'], zh=r.get('chinese_reference') or ''))
    for i, r in enumerate(json.loads((ROOT/'localization/en-US/metadata-drafts.json').read_text()), 1):
        rows.append(dict(id=f'M{i:03d}', batch='metadata', ko=r['original'], en=r['target'], zh=r.get('chinese_reference') or ''))
    profile = json.loads((ROOT/'localization/mods/zephyr-passives-2.4.3.json').read_text())
    for i, r in enumerate(profile['overrides'], 1):
        rows.append(dict(id=f'P{i:03d}', batch='ZephyrPassives 2.4.3 (default settings)', ko=r['original'], en=r['target'], zh=''))
    fullmap = json.loads((ROOT/'localization/mods/zephyr-fullmap-1.8.0.json').read_text())
    for i, r in enumerate(fullmap['rows'], 1):
        rows.append(dict(id=f'F{i:03d}', batch='ZephyrFullmap 1.8.0 English', ko=r['original'], en=r['target'] or '(Destination suffix omitted)', zh=''))
    def page(title, body):
        return '<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+html.escape(title)+'</title><style>body{font:18px/1.6 system-ui,sans-serif;margin:20px;max-width:850px;color:#20262b;background:#fff}article{border-top:2px solid #bcc;padding:14px 0}h1{font-size:24px}h2{font-size:19px}p{white-space:pre-wrap;overflow-wrap:anywhere}small{color:#556}a{color:#165e9e}</style><h1>'+html.escape(title)+'</h1>'+body+'</html>'
    intro = 'Korean → English translation review. Original Korean is authoritative. Chinese is supporting context.\nSend corrections with the R or M number. Aura Slash terminology included.\nControl codes such as /n are preserved literally.\n'
    index = ['<p>'+html.escape(intro)+'</p><p>No JavaScript is required. If your phone does not open links, navigate to the numbered files in this same folder. TXT files work in plain-text previews.</p><ul>']
    all_text = [intro]
    index_text = [intro, 'OPEN A NUMBERED .txt FILE for a small phone-friendly section.\nHTML files contain the same text directly (no scripts).\n']
    for n, start in enumerate(range(0, len(rows), 200), 1):
        chunk = rows[start:start+200]
        stem = f'{n:03d}_{chunk[0]["id"]}-{chunk[-1]["id"]}'
        title = f'Zephyr review {chunk[0]["id"]}–{chunk[-1]["id"]}'
        parts = []; lines = [title+'\n'+intro]
        for r in chunk:
            fields = [('Korean / 한국어', r['ko']), ('English / 영어', r['en'])]
            if r['zh']: fields.append(('Chinese reference / 중국어 참고', r['zh']))
            parts.append('<article id="'+r['id']+'"><h2>'+r['id']+'</h2><small>'+html.escape(r['batch'])+'</small>'+''.join('<p><b>'+label+'</b>\n'+html.escape(value)+'</p>' for label, value in fields)+'</article>')
            lines.append('\n'+r['id']+' — '+r['batch']+'\n'+'\n\n'.join(label+'\n'+value for label, value in fields)+'\n')
        (OUT/(stem+'.html')).write_text(page(title,''.join(parts)),encoding='utf-8')
        (OUT/(stem+'.txt')).write_text('\n'.join(lines),encoding='utf-8')
        all_text.extend(lines)
        index.append('<li><a href="'+stem+'.html">'+title+'</a> · <a href="'+stem+'.txt">TXT</a></li>')
        index_text.append(stem+'.txt')
    (OUT/'START-HERE.html').write_text(page('Zephyr mobile review', ''.join(index)+'</ul>'),encoding='utf-8')
    (OUT/'START-HERE.txt').write_text('\n'.join(index_text)+'\n',encoding='utf-8')
    (OUT/'ALL-TRANSLATIONS.txt').write_text('\n'.join(all_text),encoding='utf-8')
    (OUT/'review-data.json').write_text(json.dumps(rows,ensure_ascii=False),encoding='utf-8')
    print(f'{len(rows)} entries in {n} sections: {OUT}')


if __name__ == '__main__':
    main()
