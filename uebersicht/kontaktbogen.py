#!/usr/bin/env python3
"""Kontaktbögen: 8 Produkte je Bogen, je 4 Kandidaten → PNG zur Sichtprüfung."""
import json, re, unicodedata, pathlib, html
from playwright.sync_api import sync_playwright
def slug(s):
    s = unicodedata.normalize('NFKD', s); s = ''.join(c for c in s if not unicodedata.combining(c))
    return re.sub(r'[^a-z0-9]+', '-', s.lower().replace('ß', 'ss')).strip('-')[:60]
prod = json.load(open('sortiment.json')); kand = json.load(open('kand.json'))
out = pathlib.Path('ref/boegen'); out.mkdir(exist_ok=True)
seiten = [prod[i:i+8] for i in range(0, len(prod), 8)]
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path='/opt/pw-browsers/chromium-1243/chrome-linux64/chrome')
    pg = b.new_page(viewport={'width': 1100, 'height': 1500})
    for n, block in enumerate(seiten, 1):
        rows = ''
        for p in block:
            s = slug(p['name']); ks = kand.get(s, [])
            bilder = ''.join(f'<div class="k"><img src="../kand/{pathlib.Path(k["datei"]).name}"><span>{i+1}</span></div>' for i, k in enumerate(ks)) or '<i>keine Kandidaten</i>'
            rows += f'<div class="z"><div class="n"><b>{html.escape(p["name"])}</b><br><small>{html.escape(p["such"])}</small></div>{bilder}</div>'
        doc = f'''<html><head><meta charset="utf-8"><style>body{{font-family:sans-serif;margin:10px}} .z{{display:grid;grid-template-columns:200px repeat(4,210px);gap:6px;margin-bottom:8px;align-items:center}}
        .k{{position:relative}} .k img{{width:210px;height:150px;object-fit:cover;display:block}} .k span{{position:absolute;left:4px;top:4px;background:#000;color:#fff;font-weight:bold;padding:1px 7px}} .n{{font-size:13px}} small{{color:#777}}</style></head><body>{rows}</body></html>'''
        f = out / f'bogen-{n:02d}.html'; f.write_text(doc)
        pg.goto(f'file://{f.resolve()}'); pg.wait_for_timeout(400)
        pg.screenshot(path=str(out / f'bogen-{n:02d}.png'), full_page=True)
    b.close()
print(len(seiten), 'Bögen in ref/boegen/')
