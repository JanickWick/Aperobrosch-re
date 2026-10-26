#!/usr/bin/env python3
"""Sortiment nach Abteilungen → out/wick-sortiment.pdf   (python3 sortiment.py)"""
import json, html, pathlib
from playwright.sync_api import sync_playwright
ROOT = pathlib.Path(__file__).parent.resolve(); OUT = ROOT / 'out'; OUT.mkdir(exist_ok=True)
S = json.loads((ROOT / 'sortiment' / 'sortiment.json').read_text())
e = html.escape
def chf(v): return 'nach Kalkulation' if v is None else f'CHF {v:.2f}'
def liste(t, items): return f'<div class="z"><b>{t}</b><span>{" · ".join(e(x) for x in items)}</span></div>' if items else ''
def karte(p):
    h = f'<div class="karte"><div class="ph">Bild folgt</div><div class="text"><h3>{e(p["name"])}</h3><p>{e(p.get("beschreibung", ""))}</p>'
    if p.get('bisher'): h += f'<div class="z"><b>bisher</b><span>{e(p["bisher"])}</span></div>'
    if p.get('ersetzt'): h += f'<div class="z"><b>ersetzt</b><span>{e(p["ersetzt"])}</span></div>'
    if p.get('menge'): h += f'<div class="z"><b>Menge</b><span>{e(p["menge"])}</span></div>'
    if p.get('mindestmenge'): h += f'<div class="z"><b>Mindestmenge</b><span>{e(p["mindestmenge"])}</span></div>'
    h += liste('Varianten', p.get('varianten')) + liste('Brotsorten', p.get('brotsorten')) + liste('Basis', p.get('basis'))
    if p.get('sorten') and isinstance(p['sorten'][0], dict):
        h += '<div class="z"><b>Sorten</b><span>' + '<br>'.join(f'{e(x["sorte"])}{" — " + e(x["hinweis"]) if x.get("hinweis") else ""}: {chf(x.get("preis"))}' for x in p['sorten']) + '</span></div>'
    else: h += liste('Sorten', p.get('sorten'))
    h += liste('Füllungen', p.get('fuellungen')) + liste('Dips', p.get('dips')) + liste('Saisonal', p.get('saisonal')) + liste('Mit Alkohol', p.get('alkoholisch'))
    if p.get('preise'): h += '<div class="z"><b>Preis</b><span>' + '<br>'.join(f'{e(n)}{" · " + e(u) if u else ""}: {chf(v)}' for n, u, v in p['preise']) + '</span></div>'
    for k, t in (('preis_offen', 'Preis offen'), ('gestrichen', 'gestrichen'), ('geaendert', 'geändert'), ('offen', 'offen'), ('produktion', 'Produktion'), ('gefaess', 'Gefäss'), ('hinweis_catering', 'Catering')):
        v = p.get(k)
        if v: h += f'<div class="z note"><b>{t}</b><span>{e(" · ".join(v) if isinstance(v, list) else v)}</span></div>'
    return h + '</div></div>'
teile = ''.join(f'<h2>{e(k)}<small>{len(v)} Produkte</small></h2>' + (''.join(karte(p) for p in v) or '<p class="leer">noch leer</p>') for k, v in S.items())
doc = f'''<!doctype html><html lang="de-CH"><head><meta charset="utf-8"><title>Wick — Sortiment</title><style>
@page {{ size: A4 portrait; margin: 14mm 14mm 16mm; }}
@font-face {{ font-family: 'Wick Sans'; src: url('../assets/fonts/QGYsz_wNahGAdqQ43Rh_cqDpp_k.woff2') format('woff2'); font-weight: 100 900; }}
@font-face {{ font-family: 'Wick Slab'; src: url('../assets/fonts/bitter-latin.woff2') format('woff2'); font-weight: 100 900; }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ font-family: 'Wick Slab', Georgia, serif; color: #1F1F1F; font-size: 9pt; }}
h1 {{ font-family: 'Wick Sans', sans-serif; font-weight: 700; font-size: 22pt; line-height: 1.05; margin-bottom: 2mm; }}
h1 em {{ font-style: normal; color: #7A4424; }}
.intro {{ font-size: 9.5pt; line-height: 1.4; margin-bottom: 5mm; padding-bottom: 3mm; border-bottom: 0.6mm solid #1F1F1F; }}
h2 {{ font-family: 'Wick Sans', sans-serif; font-weight: 600; font-size: 12pt; letter-spacing: .07em; text-transform: uppercase; color: #7A4424; margin: 6mm 0 3mm; padding-bottom: 1.4mm; border-bottom: 0.4mm solid #CFC0A6; break-after: avoid; }}
h2 small {{ float: right; font-weight: 500; font-size: 7.5pt; color: #B78F76; }}
.karte {{ display: grid; grid-template-columns: 26mm 1fr; column-gap: 4mm; break-inside: avoid; border-bottom: 0.2mm solid #E6DCCB; padding: 2.5mm 0; }}
.ph {{ width: 26mm; height: 26mm; background: #F1EADC; display: flex; align-items: center; justify-content: center; font-family: 'Wick Sans', sans-serif; font-size: 6.5pt; color: #B78F76; }}
h3 {{ font-family: 'Wick Sans', sans-serif; font-weight: 600; font-size: 10.5pt; margin-bottom: 1mm; }}
.text p {{ font-size: 8.8pt; line-height: 1.34; color: #3B3733; margin-bottom: 1.6mm; }}
.z {{ display: grid; grid-template-columns: 24mm 1fr; column-gap: 2mm; font-size: 8.3pt; line-height: 1.32; margin-bottom: 0.7mm; }}
.z b {{ font-family: 'Wick Sans', sans-serif; font-weight: 600; font-size: 6.8pt; letter-spacing: .06em; text-transform: uppercase; color: #7A4424; padding-top: 0.5mm; }}
.z.note b {{ color: #9B2C2C; }} .z.note span {{ color: #5a2a2a; }}
.leer {{ font-style: italic; color: #B78F76; margin: 2mm 0 4mm; }}
.fuss {{ position: fixed; bottom: -9mm; left: 0; right: 0; font-family: 'Wick Sans', sans-serif; font-size: 6.5pt; letter-spacing: .06em; text-transform: uppercase; color: #B78F76; display: flex; justify-content: space-between; }}
</style></head><body>
<h1>Unser Sortiment<em> — nach Abteilungen.</em></h1>
<p class="intro">Fünf Abteilungen, jedes Produkt mit den Angaben aus den Vorlagen. «Nach Kalkulation» heisst: neue oder geänderte Position, Preis noch nicht festgelegt. Bilder folgen.</p>
{teile}
<div class="fuss"><span>Wick — Sortiment · Arbeitsstand</span><span>{sum(len(v) for v in S.values())} Produkte</span></div>
</body></html>'''
(ROOT / 'sortiment' / 'sortiment.html').write_text(doc)
PDF = OUT / 'wick-sortiment.pdf'
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path='/opt/pw-browsers/chromium-1243/chrome-linux64/chrome'); pg = b.new_page()
    pg.goto(f'file://{ROOT}/sortiment/sortiment.html', wait_until='networkidle'); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(500)
    pg.pdf(path=str(PDF), format='A4', print_background=True, prefer_css_page_size=True); b.close()
import pymupdf; print(f'» {PDF.name}: {pymupdf.open(PDF).page_count} Seiten · {sum(len(v) for v in S.values())} Produkte')
