"""Sucht Text, der aus seiner Karte oder aus der Seite herausragt.

Aufruf: python3 broschuere/pruefen.py
Baut alle Seiten als HTML, öffnet sie im Browser und misst jedes Textelement.
Gemeldet wird, was mehr als 1 mm über den Rand seiner Karte hinausreicht.
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import bauen as B

MESSEN = """() => {
  const mm = 96 / 25.4, tol = 1.2 * mm, raus = [];
  for (const seite of document.querySelectorAll('.seite')) {
    const nr = (seite.querySelector('.pnr') || {}).textContent || '?';
    const sr = seite.getBoundingClientRect();
    for (const karte of seite.querySelectorAll('.karte')) {
      const kr = karte.getBoundingClientRect();
      for (const el of karte.querySelectorAll('*')) {
        if (!el.textContent.trim()) continue;
        if (el.children.length && getComputedStyle(el).display !== 'inline') continue;
        const r = el.getBoundingClientRect();
        const unten = r.bottom - kr.bottom, rechts = r.right - kr.right;
        if (unten > tol || rechts > tol)
          raus.push({ seite: nr, wo: 'Karte', unten: +(unten / mm).toFixed(1), rechts: +(rechts / mm).toFixed(1),
                      text: el.textContent.trim().slice(0, 60) });
      }
    }
    for (const band of seite.querySelectorAll('.salatbox, .regelbox')) {
      const br = band.getBoundingClientRect();
      for (const sp of seite.querySelectorAll('.col')) {
        const r = sp.getBoundingClientRect();
        const ueber = Math.min(r.bottom, br.bottom) - Math.max(r.top, br.top);
        const quer = Math.min(r.right, br.right) - Math.max(r.left, br.left);
        if (ueber > tol && quer > tol)
          raus.push({ seite: nr, wo: 'Band deckt Spalte', unten: +(ueber / mm).toFixed(1), rechts: 0,
                      text: sp.textContent.trim().slice(0, 60) });
      }
    }
    for (const el of seite.querySelectorAll('.abs, .fuss, .intro, .sub, .titel')) {
      if (!el.textContent.trim()) continue;
      const r = el.getBoundingClientRect();
      const unten = r.bottom - sr.bottom, rechts = r.right - sr.right;
      if (unten > tol || rechts > tol)
        raus.push({ seite: nr, wo: 'Seite', unten: +(unten / mm).toFixed(1), rechts: +(rechts / mm).toFixed(1),
                    text: el.textContent.trim().slice(0, 60) });
    }
  }
  return raus;
}"""


def main():
    liste = B.SEITEN + B.KAPITEL_C
    html = ('<!doctype html><html lang="de"><head><meta charset="utf-8"><style>' + B.CSS
            + '</style></head><body>' + ''.join(f() for _, f in liste) + '</body></html>')
    ziel = B.B / '_pruefen.html'
    ziel.write_text(html, encoding='utf-8')
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=B.chrome())
        pg = b.new_page(viewport={'width': 1600, 'height': 1200})
        pg.goto(ziel.as_uri()); pg.wait_for_timeout(800); pg.evaluate('document.fonts.ready')
        raus = pg.evaluate(MESSEN)
        b.close()
    ziel.unlink(missing_ok=True)
    if not raus:
        print('Kein Text ragt heraus.'); return
    for r in raus:
        print(f"Seite {r['seite']:>3} · {r['wo']} · unten {r['unten']:>5} mm · rechts {r['rechts']:>5} mm · {r['text']}")
    print(f'\n{len(raus)} Stellen.')


if __name__ == '__main__':
    main()
