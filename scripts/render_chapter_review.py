"""Render a standalone, script-free review with same-file section navigation."""
import html
import json
import re
from collections import OrderedDict
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def main():
    source=(ROOT/'private/Zephyr-Translation-Review.html').read_text()
    rows=json.loads(re.search(r'<script id="data" type="application/json">(.*?)</script>',source,re.S).group(1))
    groups=OrderedDict()
    for r in rows:groups.setdefault(r['batch'],[]).append(r)
    esc=html.escape
    sections=[];links=[]
    for n,(batch,items) in enumerate(groups.items(),1):
        title=f'Section {n} of {len(groups)} · {batch}'
        links.append(f'<li><a href="#section-{n:03d}">{esc(title)} — {items[0]["id"]}–{items[-1]["id"]}</a></li>')
        nav='<nav aria-label="Review sections">'
        nav+=f'<a class="button" href="#section-{n-1:03d}">Previous</a>' if n>1 else '<span class="button disabled">Previous</span>'
        nav+=f'<a class="button" href="#section-{n+1:03d}">Next</a>' if n<len(groups) else '<span class="button disabled">Next</span>'
        nav+=f'<span>{n} / {len(groups)}</span></nav>'
        cards=[]
        for r in items:
            cards.append(f'<article><h2>{r["id"]}</h2><div class="texts"><div><b>Korean / 한국어</b><div class="text">{esc(r["ko"])}</div></div><div><b>English / 영어</b><div class="text">{esc(r["en"])}</div></div></div><details><summary>Chinese reference &amp; notes / 참고</summary><p class="text">{esc(r["zh"] or "No direct Chinese reference")}</p><p class="text">{esc(r["notes"])}</p><p class="text">{esc(r["location"])}</p></details></article>')
        sections.append(f'<section class="section" id="section-{n:03d}"><div class="section-head"><b>{esc(title)}</b>{nav}<small>{items[0]["id"]}–{items[-1]["id"]} · {len(items)} entries</small></div>'+''.join(cards)+nav+'</section>')
    css='''body{font:16px/1.6 system-ui,sans-serif;margin:0;background:#f4f3ef;color:#20262b}header{background:white;padding:18px 4%;border-bottom:1px solid #bbb}h1{font-size:24px;margin:0}main{max-width:1250px;margin:20px auto;padding:0 20px}article{background:white;border:1px solid #ccc;border-radius:8px;padding:18px;margin-bottom:18px}.texts{display:grid;grid-template-columns:1fr 1fr;gap:24px}.text{white-space:pre-wrap;overflow-wrap:anywhere}h2{font-size:16px;color:#365c69}summary{cursor:pointer}small{color:#556}.button{display:inline-block;background:#e9e9ec;color:#20262b;padding:8px 16px;margin:8px 8px 8px 0;border-radius:18px;text-decoration:none;font-weight:bold}.disabled{opacity:.4}nav{display:flex;align-items:center;flex-wrap:wrap;gap:4px}.section-head{background:#f4f3ef;padding:8px 0 16px;overflow-wrap:anywhere}.section{display:none}#section-001{display:block}.section:target{display:block}.section:target~#section-001{display:none}@media(max-width:650px){.texts{grid-template-columns:1fr}main{padding:0 16px}header{padding:18px 16px}}'''
    page='<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Zephyr Translation Review — Sections</title><style>'+css+'</style><header><h1>Zephyr · Korean–English review / 번역 검토</h1><p>Korean is authoritative. Chinese is supporting context. Aura Slash revision included.</p><p>Start reading below. <b>Next</b> opens the next review section; no search is required. Sections follow translation batches, not story chapters.</p><details><summary>Choose a section / 구간 선택</summary><ol>'+''.join(links)+'</ol></details><small>Send corrections with the R/M number. Search using your browser’s Find on Page. This version needs no JavaScript.</small></header><main>'+''.join(sections[1:]+sections[:1])+'</main></html>'
    out=ROOT/'private/Zephyr-Translation-Review-Sections.html';out.write_text(page)
    print(f'{out}: {len(rows)} entries, {len(groups)} sections, {out.stat().st_size} bytes')

if __name__=='__main__':main()
