#!/usr/bin/env python3
"""Sortimentsübersicht → out/wick-sortiment-uebersicht.pdf  (python3 uebersicht.py)"""
import pathlib, sys
from playwright.sync_api import sync_playwright
ROOT = pathlib.Path(__file__).parent.resolve(); OUT = ROOT / 'out'; OUT.mkdir(exist_ok=True)
PDF = OUT / 'wick-sortiment-uebersicht.pdf'
import json
U = ROOT / 'uebersicht'
ref = json.loads((U / 'ref.json').read_text()) if (U / 'ref.json').exists() else {}
(U / 'daten.js').write_text('window.PROD = ' + (U / 'sortiment.json').read_text() + ';\nwindow.REF = ' + json.dumps(ref, ensure_ascii=False) + ';\n')
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path='/opt/pw-browsers/chromium-1243/chrome-linux64/chrome')
    pg = b.new_page(); fehler = []; pg.on('pageerror', lambda e: fehler.append(str(e)))
    pg.goto(f'file://{ROOT}/uebersicht/uebersicht.html', wait_until='networkidle')
    pg.wait_for_function("document.body.dataset.fertig === '1'", timeout=30000)
    pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(600)
    n = pg.evaluate("() => ({ karten: document.querySelectorAll('.karte').length, leer: document.querySelectorAll('.bild.leer').length })")
    pg.pdf(path=str(PDF), format='A4', print_background=True, prefer_css_page_size=True); b.close()
import pymupdf; d = pymupdf.open(PDF)
print(f"» {PDF.name}: {d.page_count} Seiten · {n['karten']} Produkte · {n['leer']} ohne Bild" + ('\n  ✗ ' + '\n  ✗ '.join(fehler) if fehler else ''))
