"""Baut die überarbeiteten Produktseiten im Broschüren-Design (A3 quer) und tauscht sie
in der 40-seitigen Entwurfs-PDF aus.  Aufruf: python3 broschuere/bauen.py"""
import json, html, pathlib, subprocess, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
B = ROOT / 'broschuere'
S = {p['name']: p for ps in json.load(open(ROOT / 'sortiment/sortiment.json')).values() for p in ps}
e = html.escape
def chf(v): return 'nach Kalkulation' if v is None else f'{v:.2f}'
def K(xref, s): return f'../assets/img/kunde/s{s}-{xref}.jpeg'   # Bild aus dem Entwurf
def W(p): return f'../sortiment/bilder/kand/{p}.jpg'              # Foto aus der Website-Broschüre
PH = None                                                           # Platzhalter «Foto folgt»

# ---------- Bausteine ----------
def tag(t, art='braun'): return f'<span class="tag {art}">{e(t)}</span>'
def tags(*ts): return '<div class="tags">' + ''.join(ts) + '</div>' if ts else ''
def pr(name, einheit, wert, klein=False):
    v = f'<span class="kalk">nach Kalkulation</span>' if wert is None else f'<span class="v">{wert:.2f}</span>'
    return f'<div class="pr{" klein" if klein else ""}"><span class="n">{e(name)}</span><span class="u">{e(einheit)}</span>{v}</div>'
def grp(label, items, klein=True):
    t = ' · '.join(items) if isinstance(items, (list, tuple)) else items
    return f'<div class="grp{" k" if klein else ""}"><b>{e(label)}</b>{e(t)}</div>'
def hand(t, x, y, rot=-6, size=19): return f'<div class="hand" style="left:{x}mm;top:{y}mm;transform:rotate({rot}deg);font-size:{size}pt">{t}</div>'
def img(src, x, y, w, h, cap=None, stil=''):
    if src and src.startswith('../sortiment') and not stil: stil = 'transform:scale(1.12)'   # Randartefakte der Website-Fotos wegschneiden
    inner = (f'<img src="{src}" style="{stil}">' if src else '<div class="ph">Foto folgt</div>')
    capt = f'<div class="cap">{e(cap)}</div>' if cap else ''
    return f'<div class="bild" style="left:{x}mm;top:{y}mm;width:{w}mm;height:{h}mm">{inner}</div>{capt}'
def karte(x, y, w, h, inner, bild=None, bw=None, bh=52.9, by=None, stil=''):
    k = f'<div class="karte{" voll" if bild is False else ""}" style="left:{x}mm;top:{y}mm;width:{w}mm;height:{h}mm"><div class="kt">{inner}</div></div>'
    if bild is not False:
        k = img(bild, x + 4.7, by if by is not None else y - 31.4, bw or w - 9.3, bh, stil=stil) + k
    return k
def icon(n): return f'<img class="ic" src="icons/{n}.png">'
def row(ic, label, text): return f'<div class="row">{icon(ic) if ic else "<span></span>"}<b>{e(label)}</b><span>{text}</span></div>'

def kopf(titel, sub, nr, braun=(64.2,), ghost=''):
    return (f'<div class="kap">KAPITEL 04 / 06</div><h1 class="titel">{e(titel)}</h1><div class="sub">{e(sub)}</div>'
            f'<div class="rule"></div><div class="dot" style="left:12mm;top:31.8mm"></div>' + zeitleiste(57.4, 64, braun) + ghostbox(ghost, 168))
def hero(bild, titel, intro, braun=(132.2,), ghost=''):
    return (f'<div class="hero"><img src="{bild}"><div class="ov"></div></div><div class="kap hell">KAPITEL 04 / 06</div>'
            f'<div class="box"><div>{titel}</div></div><div class="bar" style="left:-3mm;width:17mm"></div><div class="bar" style="left:75mm;width:35mm"></div>'
            f'<div class="intro">{e(intro)}</div>' + zeitleiste(125.4, 132, braun) + ghostbox(ghost, 196))
def zeitleiste(y04, y0, braun):
    h = f'<div class="nr04" style="top:{y04}mm">04</div><div class="vline" style="top:{y0}mm;height:{272 - y0}mm"></div>'
    for y in (64.2, 105.8, 147.1, 188.6, 230.1, 271.5):
        if y < y0 - 1: continue
        h += f'<div class="{"dot b" if y in braun else "dot s"}" style="top:{y}mm"></div>'
    for y in braun:
        if y not in (64.2, 105.8, 147.1, 188.6, 230.1, 271.5): h += f'<div class="dot b" style="top:{y}mm"></div>'
    return h
def ghostbox(t, top): return f'<div class="ghostbox"><div class="ghost" style="top:{top}mm">{t}</div></div>' if t else ''
STD = 'Mindestbestellmenge 10 Stück pro Sorte bei Apérogebäck, Canapés, Wraps, Frischkäse-Pralinen und Mini-Pâtisserie. Viertel-Canapés sind nur in Viererschritten bestellbar. Alle Preise in Schweizer Franken.'
ARB = 'Arbeitsstand: «Preis nach Kalkulation» = neue oder geänderte Position, Preis folgt. «Noch offen» = Produkt aus der bisherigen Broschüre, noch nicht bestätigt.'
def fuss(nr, text=STD, arb=True):
    return f'<div class="fuss">{e(text)}{" " + e(ARB) if arb else ""}</div><div class="marke">WICK — APÉRO &amp; CATERING</div><div class="pnr">{nr}</div>'
def seite(inner): return f'<section class="seite">{inner}</section>'

# ---------- Seiten ----------
def s12():
    p = S['Knöpfli gefüllt — Laugen- und Butterknöpfli, mini']
    h = kopf('KNÖPFLI GEFÜLLT', 'Mini-Laugenknöpfli und Mini-Butterknöpfli, verschieden gefüllt — ersetzen die bisherigen gefüllten Brötli.', 12, ghost='KNÖP')
    for i, x in enumerate((222, 223, 224, 225, 226, 227)): h += img(K(x, 12), 19.1 + i * 65.8, 65.9, 52.9, 52.9)
    rows = (row('brot', 'Knöpfli:', 'Laugenknöpfli mini · Butterknöpfli mini') + row('pfeile', 'Fleisch:', 'Fleischkäse · Schinken · Rohschinken · Bündnerfleisch · Salami')
            + row(None, 'Fisch:', 'Lachs · Thon') + row(None, 'Vegetarisch:', 'Käse · Ei · Tomaten &amp; Mozzarella · Kräuterquark')
            + row('korb', 'Mischung:', 'Standardmässig gemischt — auf Wunsch sortenrein.'))
    inner = (f'<div class="tags abs" style="left:17.2mm;top:22mm">{tag("NEU")}{tag("ERSETZT BRÖTLI GEFÜLLT", "beige")}</div><div class="rows" style="top:29.5mm">{rows}</div>'
             f'<div class="abs txt11" style="left:17.1mm;top:150mm;width:250mm"><b>Ideal für Firmenanlässe und Empfänge.</b> Die Knöpfli kommen im Korb, angerichtet und griffbereit — ohne Besteck, ohne Teller, ohne Aufwand vor Ort.</div>'
             f'<div class="abs" style="left:300mm;top:143mm;width:85mm;text-align:right"><div class="lbl">LAUGENKNÖPFLI MINI &nbsp;·&nbsp; BUTTERKNÖPFLI MINI</div>{tag("PREIS NACH KALKULATION", "beige")}</div>')
    h += karte(14.9, 97.9, 390, 170.9, inner, bild=False) + hand('bisher 2.50 / 2.80', 318, 224, -5, 17)
    h += fuss(12, 'Die Fotos zeigen die bisherigen gefüllten Brötli — neue Fotos mit Laugen- und Butterknöpfli folgen. ' + STD)
    return seite(h)

def s13():
    p = S['Brot am Stück 50 cm / 100 cm']
    h = hero(K(229, 13), 'BROT<br>XXL', 'Ein Eyecatcher für jedes Buffet: Brot in XXL, gefüllt und geschnitten. Geliefert im Karton, der sich direkt zur Präsentation verwenden lässt.', ghost='XXL')
    for i, x in enumerate((256, 257, 258, 259)): h += img(K(x, 13), 19.4 + i * 98.7, 134.5, 85.0, 52.9)
    links = ''.join(pr(n, u, v) for n, u, v in (('Party Brioches, fünf Lagen', 'pro Stück', 56.0), ('Party Brioches klein, drei Lagen', 'pro Stück', 34.0), ('Brot am Stück, 50 cm', 'pro Stück', 44.0), ('Brot am Stück, 100 cm', 'pro Stück', 64.0), ('Zuschlag geschnitten', 'pro Stück', 6.0), ('Brot am Meter in Zahlenform', 'pro Stück', 70.0), ('Laugenherz / Laugenbrezel am Meter', 'pro Stück', 70.0), ('Zopfherz, gefüllt', 'pro Stück', None)))
    rechts = (row('brot', 'Brotsorten:', ' · '.join(p['brotsorten'])) + row('pfeile', 'Fleisch:', 'Fleischkäse · Schinken · Rohschinken · Bündnerfleisch · Salami') + row(None, 'Fisch:', 'Lachs · Thon')
              + row(None, 'Vegetarisch:', 'Käse · Ei · Tomaten &amp; Mozzarella · Kräuterquark') + row('korb', 'Menge:', 'Znüni 10 cm · Mittagessen 20 cm pro Person — beim Pain Surprise 3 bzw. 5 Stück pro Person'))
    inner = (f'<div class="abs eng13" style="left:17.1mm;top:20mm;width:158mm">{links}<div class="tags">{tag("WICK-SIGNATURE", "beige")}{tag("ZOPFHERZ NEU", "beige")}</div></div>'
             f'<div class="rows eng" style="left:190mm;top:22mm;width:195mm">{rechts}</div><div class="abs txt105" style="left:190mm;top:89mm;width:190mm">Ideal für Geburtstage: Brot am Meter in Zahlenform macht die Jahreszahl zum Mittelpunkt des Buffets.</div>')
    h += karte(14.9, 166.5, 390, 102.4, inner, bild=False) + hand('bis zu fünf<br>Füllungen', 110, 236, -5)
    h += fuss(13, 'Der Pain-Surprise-Turm wird mit bis zu fünf Füllungen belegt; jede Schicht wird in zehn Stücke geteilt. Brot am Stück und Brot am Meter liefern wir auf Wunsch geschnitten. Alle Preise in Schweizer Franken.')
    return seite(h)

def k6(i, titel, ts, desc, gruppen, preise, note=None, bild=None, y=97.9):
    inner = f'<h3>{titel}</h3>{tags(*ts)}<p class="desc">{e(desc)}</p>' + ''.join(grp(*g) for g in gruppen) + '<div class="preise">' + ''.join(pr(*p) for p in preise) + '</div>' + (f'<div class="hand inl">{e(note)}</div>' if note else '')
    return karte(14.9 + i * 65.6, y, 62.2, 124.1, inner, bild=bild, bw=52.9, by=66.5)

def s14():
    bb = S['Belegte Brötli']; aw = S['Apérowrap']; fk = S['Frischkäse-Pralinen']
    h = kopf('BELEGTES, CANAPÉS & FINGERFOOD', 'Von Hand ausgarniert, ohne Sulz. Mindestens 10 Stück pro Sorte, Viertel-Canapés in Viererschritten.', 14, braun=(64.2, 105.8), ghost='CANA')
    h += k6(0, 'BELEGTE BRÖTLI', [tag('BELIEBT')], 'Ein halbes Toastbrot, schön ausgarniert. Ohne Sulz.', [('Fleisch', 'Schinken · Salami · Rohschinken · Bündnerfleisch · Fleischkäse · Tatar'), ('Fisch', 'Thon · Lachs'), ('Vegetarisch', 'Käse · Ei · Spargeln · Kräuterquark · Zigerbrüüt'), ('Mindestmenge', bb['mindestmenge'])], [('Diagonal', 'pro Stück', 3.2), ('Viertel', 'pro Stück', 2.2)], bild=K(264, 14))
    h += k6(1, 'BELEGTE BRÖTLI RUND', [tag('NOCH OFFEN', 'beige')], 'Eine runde Toastscheibe, schön ausgarniert. Ohne Sulz.', [('Vegetarisch', 'Tomaten · Avocado')], [('Brötli rund', 'pro Stück', 3.9)], note='bleibt oder weg?', bild=K(265, 14))
    h += k6(2, 'APÉROWRAP', [tag('GEÄNDERT', 'beige')], 'In zwei Variationen. Neu im kleineren Format, wie für den Circus Knie produziert.', [('Sorten', aw['sorten']), ('Mindestmenge', aw['mindestmenge'])], [('Apérowrap klein', 'pro Stück', None)], note='bisher 2.70 / 2.90 · Couscous-Wrap gestrichen', bild=K(304, 16))
    h += k6(3, 'FRISCHKÄSE-PRALINEN', [tag('GEÄNDERT', 'beige')], 'In drei Varianten — neu ohne Salzstängeli, nur die Pralinen.', [('Sorten', fk['sorten']), ('Mindestmenge', fk['mindestmenge'])], [('Frischkäse-Praline', 'pro Stück', None)], note='bisher 2.50 mit Salzstängeli', bild=K(306, 16))
    h += k6(4, 'BÄCKERPASTETLI GEFÜLLT', [tag('NOCH OFFEN', 'beige')], 'Mini-Blätterteigpastetli, verschieden gefüllt.', [('Füllungen', 'Rüebli-Sesam (vegan) · Ei · Thon · Quark · Poulet')], [('Bäckerpastetli', 'pro Stück', 2.7)], note='bleibt oder weg?', bild=K(305, 16))
    h += k6(5, 'BELEGTE BRÖTCHEN ZWIRBELWICK RUSTICO', [tag('NOCH OFFEN', 'beige')], 'Belegte Brötchen, neu interpretiert. Ohne Sulz.', [('Fleisch', 'Salami (pikant) · Bündnerfleisch · Rohschinken · Schinken und Ei'), ('Fisch', 'Lachs'), ('Vegetarisch', 'Tête de Moine · Brie')], [('Brötchen', 'pro Stück', 3.9)], note='bleibt oder weg?', bild=K(266, 14))
    h += fuss(14)
    return seite(h)

def k3(i, titel, ts, desc, gruppen, preise, note=None, bild=None, stil=''):
    inner = f'<h3 class="gross">{titel}</h3>{tags(*ts)}<p class="desc">{e(desc)}</p>' + ''.join(grp(l, t, False) for l, t in gruppen) + '<div class="preise">' + ''.join(pr(*p) for p in preise) + '</div>' + (f'<div class="hand inl">{e(note)}</div>' if note else '')
    return karte(14.9 + i * 131.5, 166.5, 127.3, 102.4, inner, bild=bild, bw=118.3, bh=52.4, by=135, stil=stil)

def s15():
    ag = S['Apérogebäck']
    h = hero(K(271, 15), 'APÉRO-<br>GEBÄCK', 'Alles aus der eigenen Backstube: Chüechli, Gipfel und Würstli im Briochesmantel. Zum kalt oder warm geniessen, mindestens 10 Stück pro Sorte.', ghost='GEBÄ')
    h += k3(0, 'CHÜECHLI', [tag('BELIEBT')], 'Zum kalt oder warm geniessen.', [('Sorten', 'Chäschüechli · Saisonales Chüechli · Pizzachüechli · Spinatchüechli'), ('Mindestmenge', ag['mindestmenge'])], [('Chüechli', 'pro Stück', 2.2)], note='Lässt sich warm und kalt servieren.', bild=K(298, 15), stil='transform:scale(1.7);transform-origin:18% 62%')
    h += k3(1, 'SCHINKENGIPFEL', [tag('BELIEBT')], 'Blätterteiggipfel mit Schinkenfüllung, zum kalt oder warm geniessen.', [('Mindestmenge', ag['mindestmenge'])], [('Schinkengipfel', 'pro Stück', 2.2)], bild=K(298, 15), stil='transform:scale(1.7);transform-origin:78% 40%')
    h += k3(2, 'CHILI WÜRSTLI IM BRIOCHESMANTEL', [tag('BELIEBT')], 'Chili Würstli im weichen Briocheteig aus unserer Backstube.', [('Mindestmenge', ag['mindestmenge'])], [('Chili Würstli', 'pro Stück', 2.8)], note='Ideal als warmer Posten in einem sonst kalten Apéro.', bild=K(299, 15))
    h += fuss(15)
    return seite(h)

def s16():
    sp = S['Spiessli']
    h = kopf('SPIESSLI', 'Die Spiessli im trendigen Look — kalt, in mehreren Variationen, dazu saisonal wechselnde Sorten.', 16, ghost='SPIE')
    bilder = ((W('p13-2'), 'Tomaten & Mozzarella'), (W('p13-3'), 'Antipasti'), (PH, 'Käse-Trauben'), (PH, 'Melonen-Rohschinken'), (PH, 'Saisonal'), (W('p13-1'), 'Frucht klein'))
    for i, (src, cap) in enumerate(bilder): h += img(src, 19.1 + i * 65.8, 65.9, 52.9, 52.9) + f'<div class="cap" style="left:{19.1 + i * 65.8}mm;top:120.5mm;width:52.9mm">{e(cap)}</div>'
    rows = (row('huet', 'Sorten:', 'Tomaten &amp; Mozzarella <i>(neu ohne Focaccia)</i> 3.80 · Antipasti 3.80 · Frucht klein 2.00')
            + row('pfeile', 'Neu:', 'Käse-Trauben · Melonen-Rohschinken <i>(saisonal)</i> · weitere saisonale Spiessli, Sorten noch zu bestimmen — Preis nach Kalkulation')
            + row(None, 'Gestrichen:', 'Frucht-Nutella-Spiessli'))
    inner = (f'<div class="rows" style="top:30mm">{rows}</div>'
             f'<div class="abs" style="left:338mm;top:143mm;width:47mm;display:flex;gap:5.2mm;justify-content:flex-end"><div class="kreis"><div class="lbl">SPIESSLI</div><div class="c">3.80<small>CHF/St.</small></div></div><div class="kreis"><div class="lbl">FRUCHT KLEIN</div><div class="c">2.00<small>CHF/St.</small></div></div></div>')
    h += karte(14.9, 97.9, 390, 170.9, inner, bild=False) + hand('Erdbeer-Nutella:<br>bleibt oder weg?', 40, 222, -5) + hand('saisonal<br>ergänzt', 268, 228, -6)
    h += fuss(16, 'Die Fotos zeigen die bisherigen Spiessli (Tomaten-Mozzarella noch mit Focaccia); Fotos der neuen Sorten folgen. ' + STD)
    return seite(h)

def s18():
    pl = [S[n] for n in ('Platte Fleisch & Käse', 'Platte Käse', 'Platte mit Früchten', 'Platte mit Gemüse und Dips')]
    h = kopf('PLATTEN & SHARING', 'Fertig angerichtet, direkt aufs Buffet. Für zwei bis acht Personen — neu auf silbrigen oder schwarzen Platten.', 18, braun=(105.8,), ghost='PLAT')
    for i, x in enumerate((346, 347, 348, 349, 350, 351)): h += img(K(x, 18), 19.1 + i * 65.8, 65.9, 52.9, 52.9)
    tab = '<table class="tab"><tr><th>PLATTEN</th><th>2 PERS.</th><th>4 PERS.</th><th>6 PERS.</th><th>8 PERS.</th></tr>' + ''.join(f'<tr><td>{e(p["name"])}</td>' + ''.join(f'<td>{v:.2f}</td>' for _, _, v in p['preise']) + '</tr>' for p in pl) + '</table>'
    rechts = (row('blatt', 'Dips:', 'Pro Zwei-Personen-Platte kann ein Dip gewählt werden (8 Personen = 4 Dips): Quark · Tartar · Cocktail · Humus (vegan)')
              + row('huet', 'Catering:', 'Für Buffets und gelieferte Caterings kommt die Sauce in separatem Geschirr statt in kleinen Schälchen.')
              + row('auge', 'Grissini / Tray:', 'Grissini mit Rohschinken, ganze Platte à 15 Stück 45.00 · Tray of Snacks 45.00 — <i>noch offen</i>')
              + row('person', 'Empfehlung:', 'Zwei Platten decken einen Apéro für acht bis zehn Gäste als Ergänzung zu Häppchen ab.'))
    inner = (f'<div class="abs" style="left:17.1mm;top:22mm;width:195mm">{tab}<p class="txt11" style="margin-top:7mm">Käse unter anderem von der Käserei Rüttiberg in Schänis, Früchte und Gemüse nach Saison. Neu auf silbrigen oder schwarzen Platten statt Palmblatt — klein, mittel und gross nach Personenzahl. Bis die neuen Grössen festgelegt sind, gelten die Preise für 2, 4, 6 und 8 Personen.</p></div>'
             f'<div class="rows eng" style="left:232mm;top:22mm;width:155mm">{rechts}</div>')
    h += karte(14.9, 97.9, 390, 118, inner, bild=False) + hand('zum Teilen gemacht', 40, 201, -5)
    h += fuss(18, 'Alle Preise in Schweizer Franken.')
    return seite(h)

def s30():
    mp, ms, cc, cp = S['Mini Pâtisserie'], S['Mousse-Schale gefüllt'], S['Cup Cakes'], S['Cake Pops']
    h = kopf('DER SÜSSE ABSCHLUSS', 'Was aufs Buffet kommt und aus der Hand gegessen wird. Alles entsteht in unserer eigenen Konditorei. Am Platz serviert steht auf der nächsten Seite.', 30, braun=(147.1, 188.6), ghost='SÜSS')
    for i, src in enumerate((K(485, 30), K(486, 30), K(487, 30), K(488, 30), W('p16-4'), W('p15-1'))): h += img(src, 19.1 + i * 65.8, 65.9, 52.9, 52.9)
    def col(x, w, inner): return f'<div class="abs col" style="left:{x}mm;top:25mm;width:{w}mm">{inner}</div>'
    c1 = (f'<h3 class="gross">MINI PÂTISSERIE<br>ASSORTIERT</h3>{tags(tag("BELIEBT"), tag("VEGETARISCH", "beige"))}<p class="desc">Ein Querschnitt durch unsere Konditorei, in einem Bissen. Wir stellen nach Saison zusammen.</p>'
          + grp('Sorten', mp['sorten']) + grp('Saisonal', mp['saisonal']) + grp('Mindestmenge', mp['mindestmenge']) + '<div class="preise">' + pr('Mini Pâtisserie', 'pro Stück', 2.6) + '</div>')
    c2 = (f'<h3 class="gross">MOUSSE-SCHALE<br>GEFÜLLT</h3>{tags(tag("VEGETARISCH", "beige"))}<p class="desc">Eine Geschmacksrichtung, eine Basis — beides wählen Sie. Für 4 bis 8 Personen.</p>'
          + grp('Sorten', ms['sorten']) + grp('Basis', ms['basis']) + '<div class="preise">' + ''.join(pr(n, u, v) for n, u, v in ms['preise']) + '</div>')
    c3 = (f'<h3 class="gross">CUP CAKES</h3>{tags(tag("VEGETARISCH", "beige"))}<p class="desc">In herzigen Kinder-Sujets oder in zeitlosen Pastellfarben.</p>' + grp('Sorten', cc['sorten']) + grp('Mindestmenge', cc['mindestmenge'])
          + '<div class="preise">' + pr('Cup Cake', 'pro Stück', 5.9) + '</div>'
          + f'<h3 class="gross" style="margin-top:7mm">CAKE POPS</h3>{tags(tag("VEGETARISCH", "beige"))}<p class="desc">Am Stiel, nach Ihren Wünschen ausdekoriert.</p>' + grp('Sorten', cp['sorten']) + grp('Mit Alkohol', cp['alkoholisch']) + grp('Mindestmenge', cp['mindestmenge'])
          + '<div class="preise">' + pr('Cake Pop', 'pro Stück', 4.5) + '</div>')
    c4 = (f'<h3 class="gross">DESSERT IM GLÄSLI</h3>{tags(tag("NOCH OFFEN", "beige"))}<p class="desc">Im Glas serviert, ohne Teller und ohne Besteck.</p>' + grp('Sorten', 'Panna Cotta · Tobleronemousse · Schoggimousse · Gebrannte Creme')
          + '<div class="preise">' + pr('Dessert im Gläsli', 'pro Stück', 5.5) + '</div><div class="hand inl">bleibt oder weg?</div>'
          + f'<h3 class="gross" style="margin-top:7mm">VEGANE DESSERTVARIATIONEN</h3>{tags(tag("NOCH OFFEN", "beige"), tag("VEGAN", "beige"))}' + grp('Sorten', 'Schokoladenkuchen · Mohnroulade · Kaffeekuchen · Erdbeer-Rhabarber-Torte · Cremeschnitte')
          + '<div class="preise">' + pr('Vegane Desserts', 'pro Stück', 6.0) + '</div><div class="hand inl">bleibt oder weg?</div>')
    inner = col(17.1, 80, c1) + col(110, 80, c2) + col(203, 80, c3) + col(296, 80, c4)
    h += karte(14.9, 98, 390, 172, inner, bild=False)
    h += fuss(30, 'Mindestmenge: 10 Stück pro Sorte oder 10 Stück gemischt pro Kategorie. Alle Preise in Schweizer Franken.')
    return seite(h)

SEITEN = [(12, s12), (13, s13), (14, s14), (15, s15), (16, s16), (18, s18), (30, s30)]

CSS = r'''
@font-face{font-family:'Wick Sans';src:url(../assets/fonts/QGYsz_wNahGAdqQ43Rh_cqDpp_k.woff2) format('woff2');font-weight:100 900;unicode-range:U+0100-02AF,U+1E00-1EFF,U+20A0-20AB,U+20AD-20CF}
@font-face{font-family:'Wick Sans';src:url(../assets/fonts/QGYsz_wNahGAdqQ43Rh_fKDp.woff2) format('woff2');font-weight:100 900}
@font-face{font-family:'Wick Slab';src:url(../assets/fonts/rax8HiqOu8IVPmn7cYxpPDk.woff2) format('woff2');font-weight:100 900;unicode-range:U+0100-02AF,U+1E00-1EFF,U+20A0-20AB,U+20AD-20CF}
@font-face{font-family:'Wick Slab';src:url(../assets/fonts/rax8HiqOu8IVPmn7f4xp.woff2) format('woff2');font-weight:100 900}
@font-face{font-family:'Wick Hand';src:url(../assets/fonts/Wnz6HAc5bAfYB2Q7aDYYmg8.woff2) format('woff2');font-weight:400 700;unicode-range:U+0100-02AF,U+1E00-1EFF}
@font-face{font-family:'Wick Hand';src:url(../assets/fonts/Wnz6HAc5bAfYB2Q7ZjYY.woff2) format('woff2');font-weight:400 700}
@page{size:420mm 297mm;margin:0}
*{box-sizing:border-box;margin:0;padding:0}
body{background:#888}
.seite{width:420mm;height:297mm;position:relative;overflow:hidden;background:#F6F2EA;font-family:'Wick Slab',serif;color:#fff;page-break-after:always;-webkit-print-color-adjust:exact}
.abs{position:absolute}
.kap{position:absolute;left:15mm;top:17.6mm;font:600 9pt 'Wick Sans';letter-spacing:.22em;color:#7A4424}
.kap.hell{left:19mm;top:8.2mm;color:#E6DCCB}
.titel{position:absolute;left:54.2mm;top:14.3mm;font:600 19pt 'Wick Sans';letter-spacing:.12em;color:#1F1F1F;white-space:nowrap}
.sub{position:absolute;right:15mm;top:17.2mm;width:200mm;text-align:right;font-size:11pt;line-height:5mm;color:#2A2521}
.rule{position:absolute;left:14.9mm;right:0;top:33.8mm;height:.3mm;background:#E6DBCB}
.dot{position:absolute;left:12mm;width:4.5mm;height:4.5mm;border-radius:50%;background:#794424}
.dot.b{left:7.5mm;width:3.4mm;height:3.4mm}
.dot.s{left:8.3mm;width:1.8mm;height:1.8mm;background:#E6DBCB}
.nr04{position:absolute;left:6.1mm;font:600 9pt 'Wick Sans';letter-spacing:.1em;color:#7A4424}
.vline{position:absolute;left:9.1mm;width:.3mm;background:#E6DBCB}
.hero{position:absolute;left:-3mm;top:-3mm;width:426mm;height:124.1mm;overflow:hidden}
.hero img{width:100%;height:100%;object-fit:cover;display:block}
.hero .ov{position:absolute;inset:0;background:linear-gradient(90deg,rgba(18,17,16,.96) 0%,rgba(18,17,16,.9) 32%,rgba(18,17,16,.35) 52%,rgba(18,17,16,0) 68%)}
.box{position:absolute;left:19.1mm;top:14.9mm;width:51.9mm;height:52.1mm;background:#fff;display:flex;align-items:center;justify-content:center;text-align:center;font:500 19pt 'Wick Sans';letter-spacing:.14em;line-height:7.6mm;color:#1F1F1F}
.bar{position:absolute;top:37.7mm;height:2.2mm;background:#E6DCCB}
.intro{position:absolute;left:19mm;top:74.5mm;width:158mm;font-size:14pt;line-height:7.1mm;color:#fff}
.ghostbox{position:absolute;left:0;top:0;width:420mm;height:272mm;overflow:hidden;z-index:0}
.ghost{position:absolute;left:8mm;font:500 520pt 'Wick Sans';letter-spacing:.06em;color:#fff;line-height:1;white-space:nowrap}
.bild{position:absolute;background:#FAF7F1;z-index:2;overflow:hidden}
.bild img{width:100%;height:100%;object-fit:cover;display:block}
.ph{width:100%;height:100%;display:flex;align-items:center;justify-content:center;font:600 7pt 'Wick Sans';letter-spacing:.2em;color:#B78F76;border:.3mm dashed #E6DBCB}
.cap{position:absolute;z-index:3;text-align:center;font:600 6.6pt 'Wick Sans';letter-spacing:.15em;color:#E6DCCB;text-transform:uppercase}
.karte{position:absolute;background:#1F1F1F;z-index:1}
.kt{position:absolute;left:4.8mm;top:26.6mm;right:4.8mm;bottom:3mm}
.karte.voll .kt{left:0;top:0;right:0;bottom:0}
h3{font:500 11pt 'Wick Sans';letter-spacing:.14em;line-height:4.8mm;color:#fff;text-transform:uppercase}
h3.gross{font-size:13pt;line-height:5.6mm}
.tags{display:flex;flex-wrap:wrap;gap:1.6mm;margin:1.6mm 0 1.2mm}
.tags.abs{margin:0}
.tag{display:inline-block;font:600 6.6pt 'Wick Sans';letter-spacing:.15em;padding:.9mm 1.8mm .7mm;line-height:1;white-space:nowrap}
.tag.braun{background:#794424;color:#fff}
.tag.beige{border:.25mm solid #E6DBCB;color:#E6DCCB}
.desc{font-size:10.5pt;line-height:5mm;margin:1.8mm 0 2.2mm}
.grp{font-size:11pt;line-height:4.7mm;margin-bottom:2mm}
.grp.k{font-size:9.5pt;line-height:3.9mm;margin-bottom:1.6mm}
.grp b{display:block;font-weight:700}
.preise{margin-top:3mm}
.pr{display:flex;flex-wrap:wrap;align-items:baseline;gap:1mm 2mm;line-height:5.8mm}
.pr .n{flex:1 1 auto;font-size:12pt}
.pr .u{font-size:8.5pt;white-space:nowrap}
.pr .v{font-size:12pt;min-width:12mm;text-align:right;font-family:'Wick Sans';font-weight:500}
.pr .kalk{font:600 6.6pt 'Wick Sans';letter-spacing:.12em;border:.25mm solid #E6DBCB;color:#E6DCCB;padding:.8mm 1.5mm .6mm;line-height:1;white-space:nowrap;margin-left:auto}
.hand{position:absolute;font-family:'Wick Hand';font-weight:700;font-size:19pt;line-height:1.05;color:#E6DCCB;z-index:3;white-space:nowrap}
.hand.inl{position:static;font-size:11pt;line-height:4.6mm;margin-top:2.5mm;white-space:normal;transform:none;color:#E6DCCB}
.rows{position:absolute;left:4.7mm;width:375mm}
.row{display:grid;grid-template-columns:9mm 36mm 1fr;column-gap:2mm;align-items:start;font-size:12pt;line-height:5.4mm;margin-bottom:6.8mm}
.rows.eng .row{grid-template-columns:9mm 34mm 1fr;margin-bottom:5.2mm}
.row .ic{width:9mm;height:9mm;margin-top:-1.6mm}
.row b{font-weight:700}
.row i{font-style:italic;color:#E6DCCB}
.txt11{font-size:11pt;line-height:5mm}
.eng13 .pr{line-height:5.3mm}
.txt105{font-size:10.5pt;line-height:4.8mm}
.lbl{font:600 6.6pt 'Wick Sans';letter-spacing:.15em;color:#E6DCCB;margin-bottom:1.6mm;white-space:nowrap}
.kreis{text-align:center}
.kreis .c{width:17.5mm;height:17.5mm;border-radius:50%;background:#E6DBCB;color:#1F1F1F;display:flex;flex-direction:column;align-items:center;justify-content:center;font:500 16pt 'Wick Sans';line-height:1;margin:0 auto}
.kreis .c small{font:400 7pt 'Wick Slab';margin-top:1mm}
.tab{border-collapse:collapse;width:100%}
.tab th{font:400 8.5pt 'Wick Slab';letter-spacing:.1em;color:#E6DCCB;text-align:right;padding:0 0 1.8mm;font-weight:400}
.tab th:first-child,.tab td:first-child{text-align:left}
.tab td{font-size:12pt;line-height:5.2mm;padding:1mm 0;text-align:right;border-top:.2mm solid #3A3836;font-family:'Wick Sans';font-weight:500}
.tab td:first-child{font-family:'Wick Slab';font-weight:400}
.col h3{margin-bottom:.5mm}
.col .grp.k{margin-bottom:1.2mm}
.col .desc{margin:1.4mm 0 1.8mm}
.col .preise{margin-top:2mm}
.fuss{position:absolute;left:15mm;top:277.3mm;width:390mm;font-size:6pt;line-height:2.8mm;color:#2A2521}
.marke{position:absolute;right:14mm;top:286.2mm;font:500 9pt 'Wick Sans';letter-spacing:.12em;color:#7A4424}
.pnr{position:absolute;left:409.3mm;top:285mm;font:500 11pt 'Wick Sans';color:#1F1F1F}
'''

def main():
    nur = [int(a) for a in sys.argv[1:]] or [n for n, _ in SEITEN]
    html_ = '<!doctype html><html lang="de"><head><meta charset="utf-8"><style>' + CSS + '</style></head><body>' + ''.join(f() for n, f in SEITEN if n in nur) + '</body></html>'
    (B / 'seiten.html').write_text(html_)
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path='/opt/pw-browsers/chromium-1243/chrome-linux64/chrome'); pg = b.new_page()
        pg.goto((B / 'seiten.html').as_uri()); pg.wait_for_timeout(600); pg.evaluate('document.fonts.ready')
        pg.pdf(path=str(B / 'seiten.pdf'), width='420mm', height='297mm', print_background=True, prefer_css_page_size=True); b.close()
    import pymupdf
    neu = pymupdf.open(B / 'seiten.pdf'); doc = pymupdf.open(ROOT / 'quellen/broschuere-40s.pdf')
    for k, n in enumerate([n for n, _ in SEITEN if n in nur]):
        doc.delete_page(n - 1); doc.insert_pdf(neu, from_page=k, to_page=k, start_at=n - 1)
    out = ROOT / 'out/wick-apero-catering-ENTWURF.pdf'; doc.save(out, garbage=4, deflate=True)
    print(f'» {out.name}: {doc.page_count} Seiten, ersetzt: {nur}')
if __name__ == '__main__': main()
