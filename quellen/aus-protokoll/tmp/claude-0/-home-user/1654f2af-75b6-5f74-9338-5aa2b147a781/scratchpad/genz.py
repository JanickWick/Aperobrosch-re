import json, importlib.util, pathlib, re
spec = importlib.util.spec_from_file_location('b', '/home/user/wick/bilder.py')
b = importlib.util.module_from_spec(spec); spec.loader.exec_module(b)
gr, alle = b.plaetze()
kunde = json.load(open('/tmp/claude-0/-home-user/1654f2af-75b6-5f74-9338-5aa2b147a781/scratchpad/kunde.json'))

# kurz → id: dieselbe Übersetzung wie in plaetze(), nur rückwärts angewandt
from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    br = pw.chromium.launch(executable_path=b.CHROME); pg = br.new_page()
    pg.goto(f"file://{b.SRC}?mode=print", wait_until="networkidle"); pg.wait_for_timeout(500)
    ids = pg.evaluate("() => Object.fromEntries((window.WICK.NEUHEITEN||[])"
                      ".map(n => [n.kurz, n.id]))")
    br.close()
K = {}
for motiv, (datei, size, seite) in kunde.items():
    K[ids.get(motiv, motiv)] = datei

# Stellvertreter für die Plätze, die es vorher nicht gab. Alles echtes
# Wick-Material aus derselben Sammlung, inhaltlich so nah wie möglich.
NEU = {
 'Kürbissuppe im Teller, Aufsicht':          'kunde/04-kuche-im-betrieb-anrichten-fur-ein-catering.jpg S',
 'Bündner Gerstensuppe im Topf':             'kunde/03-verpflegung-am-eidgenossischen-schwing-und-alplerfest-ausgabe-im-betri.jpg S',
 'Suppe im Gläsli als Fingerfood':           'kunde/16-frischkasekugeln-mit-salzstangeli.jpg S',
 'Lachstatar mit Thai-Salsa, angerichtet':   'kunde/16-randen-blini-mit-lachs-zitronenpfeffer-creme-fraiche-und-dill.jpg S',
 'Burrata mit Tomaten und Basilikum':        'kunde/14-belegte-brotli-rund-mit-tomaten-und-avocado.jpg S',
 'Hausgemachte Käseravioli, warm angerichtet':'kunde/17-murbeteig-tartelette-mit-alpler-magronen-bergkase-rostzwiebeln-und-ein.jpg S',
 'Warmes Buffet in Chafing Dishes, Gäste schöpfen, Abendlicht':
                                             'kunde/06-aperobuffet-in-der-ubersicht-glaser-und-platten-weiche-tiefenscharfe.jpg S',
 'Angerichteter Teller wird im Service weitergereicht, Abendlicht':
                                             'kunde/04-hande-beim-garnieren-eines-canapes-makro-dunkler-grund-streiflicht.jpg S',
 'Grillplatte mit mariniertem Fleisch, Aufsicht': 'kunde/22-grillplatte-deluxe-aufsicht.jpg S',
 'Pouletbrust mit saisonaler Füllung, angerichtet':
                                             'kunde/17-kalbsbratchogeli-im-blatterteigmantel-dazu-champignonrahm-zum-dippen.jpg S',
 'Lachsfilet auf dem Teller, Kräuter':       'kunde/16-randen-blini-mit-lachs-zitronenpfeffer-creme-fraiche-und-dill.jpg S',
 'Saisonales Risotto im Teller, Aufsicht':   'kunde/17-knusprige-rostitaschen-mit-krauterquark-unser-menuklassiker-im-kleinfo.jpg S',
 'Hausgemachte Käseravioli mit Bergkäse':    'kunde/17-unser-chaschuechli-mit-alpkase-der-kaserei-ruttiberg-rahm-und-muskat-w.jpg S',
 'Konfierte Entenschenkel, angerichtet':     'kunde/22-grillplatte-deluxe-aufsicht.jpg S',
 'Gebratener Tofu mit Gemüse':               'kunde/25-vegane-happchen-und-gemuseplatte-aufsicht-dunkler-grund.jpg S',
 'Hochzeitstorte mehrstöckig, Detail':       'kunde/24-hochzeitstorte-konditorin-beim-garnieren.jpg',
 'Torte mit Wunschmotiv, Aufsicht':          'kunde/24-cup-cakes-in-pastellfarben.jpg S',
 'Vegane Torte, angeschnitten':              'kunde/23-schwarzwalderschnitte.jpg S',
 'Pralinen von Hand garniert, Confiserie':   'kunde/04-confiserie-pralinen-von-hand-garniert.jpg',
 'Schokoladentafeln aus eigener Herstellung':'kunde/23-mohrenkopf.jpg S',
}

# Welche Motive waren in der alten Tabelle Stellvertreter?
alt_src = pathlib.Path('/home/user/wick/bilder.py').read_text()
alt_S = set(re.findall(r"^ '([^']+)': '[^']* S'", alt_src, re.M))

zeilen, fehlt = [], []
seite = None
for m, o in sorted(gr.items(), key=lambda kv: (kv[1]['p'], kv[1]['m'])):
    if o['p'] != seite:
        seite = o['p']
        zeilen.append(f"\n # --- Seite {seite:02d} " + "-" * (62 - len(str(seite))))
    if m in NEU:
        wert = NEU[m]
    elif m in K:
        wert = K[m] + (' S' if m in alt_S else '')
    else:
        fehlt.append((o['p'], m)); continue
    zeilen.append(f" {m!r}: {wert!r},")

if fehlt:
    print('OHNE ZUORDNUNG:'); [print('  S.%02d %s' % f) for f in fehlt]

neu_block = "Z = {" + "\n".join(zeilen) + "\n}\n"
i = alt_src.index('Z = {'); j = alt_src.index('\n}\n', i) + 3
pathlib.Path('/home/user/wick/bilder.py').write_text(alt_src[:i] + neu_block + alt_src[j:])
print(f'Z neu geschrieben: {len(gr)} Plätze, {sum(1 for z in zeilen if z.startswith(" #"))} Seiten')