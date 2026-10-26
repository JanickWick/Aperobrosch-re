#!/usr/bin/env python3
"""
WICK — Vorbereitungsblatt für die Abteilungssitzungen

  python3 sitzung.py            # PDF nach out/
  python3 sitzung.py --png      # zusätzlich Seiten-PNGs zur Kontrolle

A4 hoch, vier Seiten, zum beidseitigen Drucken auf zwei Blättern.
Kein Anschnitt und keine Schnittmarken — das ist ein internes Arbeitsblatt,
kein Druckauftrag.
"""
import sys, pathlib

ROOT = pathlib.Path(__file__).parent.resolve()
SRC = ROOT / "src" / "sitzung" / "sitzung.html"
OUT = ROOT / "out"
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
PDF = OUT / "wick-sitzung-sortiment.pdf"


def main():
    from playwright.sync_api import sync_playwright
    OUT.mkdir(exist_ok=True)
    png = "--png" in sys.argv
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROME)
        pg = b.new_page(viewport={"width": 1000, "height": 1400})
        fehler = []
        pg.on("pageerror", lambda e: fehler.append(str(e)))
        pg.goto(f"file://{SRC}?mode=print", wait_until="networkidle")
        pg.evaluate("document.fonts.ready")
        pg.wait_for_timeout(700)
        if fehler:
            print("  ✗ " + "\n  ✗ ".join(fehler))
            return 1
        pg.pdf(path=str(PDF), width="210mm", height="297mm", print_background=True,
               margin={"top": "0", "bottom": "0", "left": "0", "right": "0"},
               prefer_css_page_size=True)
        if png:
            for i in range(4):
                pg.evaluate(f"window.scrollTo(0, {i} * 297 * 96/25.4)")
                pg.wait_for_timeout(120)
                pg.screenshot(path=str(OUT / f"sitzung-{i+1}.png"))
        b.close()

    import pymupdf
    d = pymupdf.open(PDF)
    mm = 72 / 25.4
    print(f"\n» Vorbereitungsblatt\n  · {PDF.name}  {PDF.stat().st_size//1024} KB")
    print(f"  · {d.page_count} Seiten, "
          f"{d[0].rect.width/mm:.0f}×{d[0].rect.height/mm:.0f} mm")
    return 0


if __name__ == "__main__":
    sys.exit(main())