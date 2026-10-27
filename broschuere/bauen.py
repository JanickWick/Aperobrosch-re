"""Baut die überarbeiteten Produktseiten im Broschüren-Design (A3 quer) und tauscht sie
in der 40-seitigen Entwurfs-PDF aus.  Aufruf: python3 broschuere/bauen.py"""
import json, html, pathlib, subprocess, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
B = ROOT / 'broschuere'
S = {p['name']: p for ps in json.load(open(ROOT / 'sortiment/sortiment.json', encoding='utf-8')).values() for p in ps}
e = html.escape
def chf(v): return 'nach Kalkulation' if v is None else f'{v:.2f}'
def K(xref, s): return f'../assets/img/kunde/s{s}-{xref}.jpeg'   # Bild aus dem Entwurf
def W(p): return f'../sortiment/bilder/kand/{p}.jpg'              # Foto aus der Website-Broschüre
def F(n): return f'../bilder/final/{n}.jpg'                       # freigegebenes Bild
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
def s11alt():
    """Alte Seite 11: Brot & Brötli. Inhalt unverändert, neu mit echten Fotos."""
    h = hero(F('seite-12_hero'), 'BROT &amp;<br>BRÖTLI',
             'Brot ist unser Ursprung. Unsere Teige ruhen bis zu 48 Stunden — das gibt Aroma und macht das Brot bekömmlicher. '
             'Für den Apéro formen wir es zu Trauben, Picknickbroten und Laiben, die man teilt.', ghost='BROT')
    MENGE = ('Menge pro Person', 'Minibrötli (ca. 20 g) 3 Stück · Partybrötli (ca. 30 g) 2 Stück · Bürli (ca. 70 g) 1 Stück')
    PREIS = [('Minibrötli', 'pro Stück', 0.8), ('Partybrötli', 'pro Stück', 0.9), ('Bürli', 'pro Stück', 1.3)]
    h += k3(0, 'TRAUBENBROT', [tag('BELIEBT')], 'Helle, dunkle oder körnige Brötchen, als Traube zusammengefügt.',
            [MENGE], PREIS, bild=F('seite-12_traubenbrot'))
    h += k3(1, 'PICKNICKBROT', [], 'Verschiedene Brötli aneinandergeformt.', [MENGE], PREIS, bild=F('seite-12_picknickbrot'))
    h += k3(2, 'PARTYBROT', [tag('WICK-SIGNATURE', 'beige')], 'Holzofenbrot, dunkel und sehr kräftig gebacken. Auf Wunsch mit Schriftzug auf einem Schild.',
            [('Menge pro Person', '100–150 g pro Person')], [('Partybrot', 'pro kg', 11.0), ('Partybrot', 'pro Stück', 15.0)],
            bild=F('seite-12_partybrot'))
    h += fuss(12, 'Alle Preise in Schweizer Franken.', arb=False)
    return seite(h)

def s12():
    """Alte Seite 12: Brötli gefüllt. Inhalt und Preise wie im Original, neu mit Themenbild."""
    h = hero(F('seite-13_broetli-thema'), 'BRÖTLI<br>GEFÜLLT',
             'Fünf Brotsorten, drei Füllungsgruppen, beliebig kombinierbar. Standardmässig gemischt, auf Wunsch sortenrein. '
             'Die Brötli kommen im Korb, angerichtet und griffbereit.', ghost='BRÖT')
    rows = (row('brot', 'Brotsorten:', 'Weiss · Para · Sonny · Vollkorn · Laugen')
            + row('pfeile', 'Fleisch:', 'Fleischkäse · Schinken · Rohschinken · Bündnerfleisch · Salami')
            + row(None, 'Fisch:', 'Lachs · Thon') + row(None, 'Vegetarisch:', 'Käse · Ei · Tomaten &amp; Mozzarella · Kräuterquark')
            + row('korb', 'Mindestmenge:', '10 Stück pro Sorte. Standardmässig gemischt — auf Wunsch sortenrein.'))
    inner = (f'<div class="rows" style="top:20mm;width:255mm">{rows}</div>'
             f'<div class="abs txt11" style="left:4.7mm;top:88mm;width:255mm"><b>Ideal für Firmenanlässe und Empfänge.</b> Ohne Besteck, ohne Teller, ohne Aufwand vor Ort.</div>'
             f'<div class="abs" style="left:275mm;top:20mm;width:105mm;text-align:right">'
             f'<div class="tags" style="justify-content:flex-end;margin:0">{tag("BELIEBT")}</div>'
             f'<div style="display:flex;gap:5.2mm;justify-content:flex-end;margin-top:12mm">'
             f'<div class="kreis"><div class="lbl">MINIBRÖTLI</div><div class="c">2.50<small>CHF/St.</small></div></div>'
             f'<div class="kreis"><div class="lbl">PARTYBRÖTLI</div><div class="c">2.80<small>CHF/St.</small></div></div></div></div>')
    h += karte(14.9, 138, 390, 130.9, inner, bild=False) + hand('frei kombinierbar', 40, 252, -5, 17)
    h += fuss(13, STD)
    return seite(h)

def s13():
    p = S['Brot am Stück 50 cm / 100 cm']
    h = hero(F('seite-14_hero'), 'BROT<br>XXL', 'Ein Eyecatcher für jedes Buffet: Brot in XXL, gefüllt und geschnitten. Geliefert im Karton, der sich direkt zur Präsentation verwenden lässt.', ghost='XXL')
    for i, n in enumerate(('seite-14_party-brioches', 'seite-14_brot-am-stueck', 'seite-14_zahlenform', 'seite-14_laugenherz')):
        h += img(F(n), 19.4 + i * 98.7, 134.5, 85.0, 52.9)
    links = ''.join(pr(n, u, v) for n, u, v in (('Party Brioches, fünf Lagen', 'pro Stück', 56.0), ('Party Brioches klein, drei Lagen', 'pro Stück', 34.0), ('Brot am Stück, 50 cm', 'pro Stück', 44.0), ('Brot am Stück, 100 cm', 'pro Stück', 64.0), ('Zuschlag geschnitten', 'pro Stück', 6.0), ('Brot am Meter in Zahlenform', 'pro Stück', 70.0), ('Laugenherz / Laugenbrezel am Meter', 'pro Stück', 70.0), ('Zopfherz, gefüllt', 'pro Stück', None)))
    rechts = (row('brot', 'Brotsorten:', ' · '.join(p['brotsorten'])) + row('pfeile', 'Fleisch:', 'Fleischkäse · Schinken · Rohschinken · Bündnerfleisch · Salami') + row(None, 'Fisch:', 'Lachs · Thon')
              + row(None, 'Vegetarisch:', 'Käse · Ei · Tomaten &amp; Mozzarella · Kräuterquark') + row('korb', 'Menge:', 'Znüni 10 cm · Mittagessen 20 cm pro Person — beim Pain Surprise 3 bzw. 5 Stück pro Person'))
    inner = (f'<div class="abs eng13" style="left:17.1mm;top:25mm;width:158mm">{links}<div class="tags">{tag("WICK-SIGNATURE", "beige")}{tag("ZOPFHERZ NEU", "beige")}</div></div>'
             f'<div class="rows eng" style="left:190mm;top:25mm;width:195mm">{rechts}</div><div class="abs txt105" style="left:190mm;top:91mm;width:190mm">Ideal für Geburtstage: Brot am Meter in Zahlenform macht die Jahreszahl zum Mittelpunkt des Buffets.</div>')
    h += karte(14.9, 166.5, 390, 102.4, inner, bild=False) + hand('bis zu fünf<br>Füllungen', 110, 236, -5)
    h += fuss(14, 'Der Pain-Surprise-Turm wird mit bis zu fünf Füllungen belegt; jede Schicht wird in zehn Stücke geteilt. Brot am Stück und Brot am Meter liefern wir auf Wunsch geschnitten. Alle Preise in Schweizer Franken.')
    return seite(h)

def k6(i, titel, ts, desc, gruppen, preise, note=None, bild=None, y=97.9):
    inner = f'<h3>{titel}</h3>{tags(*ts)}<p class="desc">{e(desc)}</p>' + ''.join(grp(*g) for g in gruppen) + '<div class="preise">' + ''.join(pr(*p) for p in preise) + '</div>' + (f'<div class="hand inl">{e(note)}</div>' if note else '')
    return karte(14.9 + i * 65.6, y, 62.2, 124.1, inner, bild=bild, bw=52.9, by=66.5)

def s14():
    bb = S['Belegte Brötli']; aw = S['Apérowrap']; fk = S['Frischkäse-Pralinen']
    h = kopf('BELEGTES, CANAPÉS & FINGERFOOD', 'Von Hand ausgarniert, ohne Sulz. Mindestens 10 Stück pro Sorte, Viertel-Canapés in Viererschritten.', 14, braun=(64.2, 105.8), ghost='CANA')
    h += k6(0, 'BELEGTE BRÖTLI', [tag('BELIEBT')], 'Ein halbes Toastbrot, schön ausgarniert. Ohne Sulz.', [('Fleisch', 'Schinken · Salami · Rohschinken · Bündnerfleisch · Fleischkäse · Tatar'), ('Fisch', 'Thon · Lachs'), ('Vegetarisch', 'Käse · Ei · Spargeln · Kräuterquark · Zigerbrüüt'), ('Mindestmenge', bb['mindestmenge'])], [('Diagonal', 'pro Stück', 3.2), ('Viertel', 'pro Stück', 2.2)], bild=F('seite-15_broetli-diagonal'))
    h += k6(1, 'BELEGTE BRÖTLI RUND', [tag('NOCH OFFEN', 'beige')], 'Eine runde Toastscheibe, schön ausgarniert. Ohne Sulz.', [('Vegetarisch', 'Tomaten · Avocado')], [('Brötli rund', 'pro Stück', 3.9)], note='bleibt oder weg?', bild=F('seite-15_broetli-rund'))
    h += k6(2, 'APÉROWRAP', [tag('GEÄNDERT', 'beige')], 'In zwei Variationen. Neu im kleineren Format, wie für den Circus Knie produziert.', [('Sorten', aw['sorten']), ('Mindestmenge', aw['mindestmenge'])], [('Apérowrap klein', 'pro Stück', None)], note='bisher 2.70 / 2.90 · Couscous-Wrap gestrichen', bild=F('seite-15_aperowrap'))
    h += k6(3, 'FRISCHKÄSE-PRALINEN', [tag('GEÄNDERT', 'beige')], 'In drei Varianten — neu ohne Salzstängeli, nur die Pralinen.', [('Sorten', fk['sorten']), ('Mindestmenge', fk['mindestmenge'])], [('Frischkäse-Praline', 'pro Stück', None)], note='bisher 2.50 mit Salzstängeli', bild=F('seite-15_frischkaese-pralinen'))
    h += k6(4, 'BÄCKERPASTETLI GEFÜLLT', [tag('NOCH OFFEN', 'beige')], 'Mini-Blätterteigpastetli, verschieden gefüllt.', [('Füllungen', 'Rüebli-Sesam (vegan) · Ei · Thon · Quark · Poulet')], [('Bäckerpastetli', 'pro Stück', 2.7)], note='bleibt oder weg?', bild=F('seite-15_baeckerpastetli'))
    h += k6(5, 'BELEGTE BRÖTCHEN ZWIRBELWICK RUSTICO', [tag('NOCH OFFEN', 'beige')], 'Belegte Brötchen, neu interpretiert. Ohne Sulz.', [('Fleisch', 'Salami (pikant) · Bündnerfleisch · Rohschinken · Schinken und Ei'), ('Fisch', 'Lachs'), ('Vegetarisch', 'Tête de Moine · Brie')], [('Brötchen', 'pro Stück', 3.9)], note='bleibt oder weg?', bild=F('seite-15_zwirbelwick-rustico'))
    h += fuss(15)
    return seite(h)

def k3(i, titel, ts, desc, gruppen, preise, note=None, bild=None, stil='', y=166.5, h=102.4, by=135):
    inner = f'<h3 class="gross">{titel}</h3>{tags(*ts)}<p class="desc">{e(desc)}</p>' + ''.join(grp(l, t, False) for l, t in gruppen) + '<div class="preise">' + ''.join(pr(*p) for p in preise) + '</div>' + (f'<div class="hand inl">{e(note)}</div>' if note else '')
    if bild is False: inner = f'<div style="padding:26.6mm 4.8mm 3mm">{inner}</div>'   # Karte ohne Bild braucht den Rand selbst
    return karte(14.9 + i * 131.5, y, 127.3, h, inner, bild=bild, bw=118.3, bh=52.4, by=by, stil=stil)

def s16():
    sp = S['Spiessli']
    h = kopf('SPIESSLI', 'Die Spiessli im trendigen Look — kalt, in mehreren Variationen, dazu saisonal wechselnde Sorten.', 16, ghost='SPIE')
    bilder = ((F('seite-16_spiessli-caprese'), 'Tomaten & Mozzarella'), (F('seite-16_spiessli-kaese-trauben'), 'Käse-Trauben'),
              (F('seite-16_spiessli-melonen-rohschinken'), 'Melonen-Rohschinken'), (F('seite-16_spiessli-antipasti'), 'Antipasti'),
              (F('seite-16_spiessli-frucht-klein'), 'Frucht klein'))
    for i, (src, cap) in enumerate(bilder): h += img(src, 52.0 + i * 65.8, 65.9, 52.9, 52.9) + f'<div class="cap" style="left:{52.0 + i * 65.8}mm;top:120.5mm;width:52.9mm">{e(cap)}</div>'
    rows = (row('huet', 'Sorten:', 'Tomaten &amp; Mozzarella <i>(neu ohne Focaccia)</i> 3.80 · Antipasti 3.80 · Frucht klein 2.00')
            + row('pfeile', 'Neu:', 'Käse-Trauben · Melonen-Rohschinken <i>(saisonal)</i> — Preis nach Kalkulation')
            + row(None, 'Gestrichen:', 'Frucht-Nutella-Spiessli'))
    inner = (f'<div class="rows" style="top:30mm">{rows}</div>'
             f'<div class="abs" style="left:338mm;top:143mm;width:47mm;display:flex;gap:5.2mm;justify-content:flex-end"><div class="kreis"><div class="lbl">SPIESSLI</div><div class="c">3.80<small>CHF/St.</small></div></div><div class="kreis"><div class="lbl">FRUCHT KLEIN</div><div class="c">2.00<small>CHF/St.</small></div></div></div>')
    h += karte(14.9, 97.9, 390, 170.9, inner, bild=False) + hand('Erdbeer-Nutella:<br>bleibt oder weg?', 40, 222, -5) + hand('saisonal<br>ergänzt', 268, 228, -6)
    h += fuss(16, STD)
    return seite(h)

def k4(i, titel, ts, desc, gruppen, preise, note=None, bild=None):
    inner = (f'<h3 class="gross">{titel}</h3>{tags(*ts)}<p class="desc">{e(desc)}</p>' + ''.join(grp(l, t, False) for l, t in gruppen)
             + '<div class="preise">' + ''.join(pr(*p) for p in preise) + '</div>' + (f'<div class="hand inl">{e(note)}</div>' if note else ''))
    return karte(14.9 + i * 98.6, 166.5, 94.4, 102.4, inner, bild=bild, bw=85.0, bh=52.4, by=135)

def k6h(i, titel, ts, desc, gruppen, preise, note=None, bild=None):
    """Sechs Karten unter einem Themenbild."""
    inner = (f'<h3>{titel}</h3>{tags(*ts)}<p class="desc">{e(desc)}</p>' + ''.join(grp(l, t, True) for l, t in gruppen)
             + '<div class="preise">' + ''.join(pr(*p, klein=True) for p in preise) + '</div>'
             + (f'<div class="hand inl">{e(note)}</div>' if note else ''))
    return karte(14.9 + i * 65.6, 156, 62.2, 112.9, inner, bild=bild, bw=52.9, bh=52.9, by=125)

def s17():
    """Alte Seiten 15 und 17 zusammengelegt: alles Warme auf einer Seite.

    Das Chäs-Chüechli «Rüttiberg» steht neu als Sorte bei den Chüechli.
    Mini-Röstitaschen und Brätchögeli im Blätterteig sind gestrichen.
    """
    h = hero(F('seite-17_hero'), 'WARME<br>HÄPPCHEN',
             'Ein warmer Posten verändert einen Apéro. Gebäck aus der eigenen Backstube, Häppchen aus der eigenen Küche — '
             'alles lässt sich vorbereiten und vor Ort in wenigen Minuten regenerieren, auch dort, wo keine Küche steht.', ghost='WARM')
    h += k6h(0, 'CHÜECHLI', [tag('BELIEBT'), tag('VEGETARISCH', 'beige')], 'Aus der eigenen Backstube, kalt oder warm.',
             [('Sorten', 'Chäschüechli · Chäs-Chüechli «Rüttiberg» mit Alpkäse der Käserei Rüttiberg · Saisonales · Pizza · Spinat'),
              ('Mindestmenge', '10 Stück pro Sorte')], [('Chüechli', 'pro Stück', 2.2)], bild=F('seite-17_chuechli'))
    h += k6h(1, 'SCHINKENGIPFEL', [tag('BELIEBT')], 'Blätterteiggipfel mit Schinkenfüllung, kalt oder warm.',
             [('Mindestmenge', '10 Stück pro Sorte')], [('Schinkengipfel', 'pro Stück', 2.2)], bild=F('seite-17_schinkengipfel'))
    h += k6h(2, 'CHILI WÜRSTLI IM<br>BRIOCHESMANTEL', [tag('BELIEBT')], 'Chili Würstli im weichen Briocheteig aus unserer Backstube.',
             [('Mindestmenge', '10 Stück pro Sorte')], [('Chili Würstli', 'pro Stück', 2.8)],
             note='Der einfachste warme Posten in einem sonst kalten Apéro.', bild=F('seite-17_chili-wuerstli'))
    h += k6h(3, 'ÄLPLER-MAGRONEN-<br>TARTELETTE', [tag('NEU'), tag('WICK-SIGNATURE', 'beige'), tag('VEGETARISCH', 'beige')],
             'Mürbeteig-Tartelette mit Älpler Magronen, Bergkäse, Röstzwiebeln und einem Tupfer Apfelmus.',
             [('Format', '2 Bissen · warm')], [('Tartelette', 'pro Stück', None)],
             bild=F('seite-17_magronen-tartelette'))
    h += k6h(4, 'GHACKETS-UND-<br>HÖRNLI-KROKETTE', [tag('NEU'), tag('WICK-SIGNATURE', 'beige')],
             'Knusprige Krokette aus Ghackets und Hörnli, dazu Apfelmus zum Dippen.',
             [('Format', '1–2 Bissen · warm')], [('Krokette', 'pro Stück', None)],
             note='Ideal für Baustellenaufrichtungen und Vereinsanlässe.', bild=F('seite-17_ghackets-krokette'))
    h += k6h(5, 'FALAFEL-BISSEN', [tag('NEU'), tag('VEGAN', 'beige'), tag('KALT ODER WARM', 'beige')],
             'Kleine Falafel mit Ingwer-Karottensauce zum Dippen.',
             [('Format', '1 Bissen · kalt oder warm')], [('Falafel-Bissen', 'pro Stück', None)],
             bild=F('seite-17_falafel'))
    h += fuss(17, 'Älpler Magronen und Ghackets und Hörnli stehen seit Jahren als Menü auf unserer Karte — hier im Kleinformat. '
                  'Mini-Röstitaschen und Brätchögeli im Blätterteig sind gestrichen. Mindestbestellmenge 10 Stück pro Sorte. '
                  'Bei den mit «Neu» gekennzeichneten Positionen folgen Preis und Allergene nach Abschluss der Kalkulation.', arb=False)
    return seite(h)

def s19():
    """Alte Seite 19: Unterwegs. Inhalt unverändert aus dem Original, neu mit echten Fotos."""
    h = hero(F('seite-19_hero'), 'UNTER-<br>WEGS',
             'Sitzung, Seminar, Ausflug oder Sportanlass: Wo keine Küche steht und die Zeit knapp ist, kommt die Verpflegung '
             'fertig gepackt. Jeder Lunchbag enthält Getränk, Hauptkomponente, etwas Süsses und einen Apfel.', ghost='LUNCH')
    bags = (('LUNCHBAG<br>ZÜRICHSEE', [tag('BELIEBT')],
             'Mineralwasser mit oder ohne Kohlensäure 0.5 l · Parisettli gefüllt · Cookie · Apfel', 12.9, 'seite-19_zuerichsee'),
            ('LUNCHBAG<br>HOLZSTEG', [],
             'Mineralwasser mit oder ohne Kohlensäure 0.5 l · Zwirbelwick Rustico gefüllt · hausgemachtes Milch-Brüggeli · Apfel', 13.9, 'seite-19_holzsteg'),
            ('LUNCHBAG<br>ETZEL', [],
             'Shorley 0.5 l · gemischter Salat mit Sauce nach Wahl, French oder Italian · Zwirbelwick Brötli · Mandel- oder Nussgipfel aus Blätterteig · Apfel', 16.9, 'seite-19_etzel'),
            ('LUNCHBAG<br>HEALTHY', [tag('NEU')],
             'Mineralwasser mit oder ohne Kohlensäure 0.5 l · UrDinkel-Parisettli gefüllt · Bircher Müesli · Parabrötli · Apfel', 18.9, 'seite-19_healthy'))
    for i, (titel, ts, items, preis, bild) in enumerate(bags):
        h += k4(i, titel, ts, 'Fertig gepackt in der Papiertüte.' if i == 0 else '',
                [('Je 1 Stück', items)], [('Lunchbag', 'pro Stück', preis)],
                note='Wunschfüllung bei der Bestellung angeben.' if i == 0 else None, bild=F(bild))
    h += fuss(19, 'Wunschfüllung bei der Bestellung angeben. Lunchbags liefern wir auch an Orte ohne Küche und ohne Kühlung. '
                  'Alle Preise in Schweizer Franken.', arb=False)
    return seite(h)

def s18():
    pl = [S[n] for n in ('Platte Fleisch & Käse', 'Platte Käse', 'Platte mit Früchten', 'Platte mit Gemüse und Dips')]
    h = kopf('PLATTEN & SHARING', 'Fertig angerichtet, direkt aufs Buffet. Für zwei bis acht Personen — neu auf silbrigen oder schwarzen Platten.', 18, braun=(105.8,), ghost='PLAT')
    platten = ('seite-18_platte-fleisch-kaese', 'seite-18_platte-kaese', 'seite-18_platte-fruechte', 'seite-18_platte-gemuese')
    for i, n in enumerate(platten): h += img(F(n), 84.9 + i * 65.8, 65.9, 52.9, 52.9)
    tab = '<table class="tab"><tr><th>PLATTEN</th><th>2 PERS.</th><th>4 PERS.</th><th>6 PERS.</th><th>8 PERS.</th></tr>' + ''.join(f'<tr><td>{e(p["name"])}</td>' + ''.join(f'<td>{v:.2f}</td>' for _, _, v in p['preise']) + '</tr>' for p in pl) + '</table>'
    rechts = (row('blatt', 'Dips:', 'Pro Zwei-Personen-Platte kann ein Dip gewählt werden (8 Personen = 4 Dips): Quark · Tartar · Cocktail · Humus (vegan)')
              + row('huet', 'Catering:', 'Für Buffets und gelieferte Caterings kommt die Sauce in separatem Geschirr statt in kleinen Schälchen.')
              + row('person', 'Empfehlung:', 'Zwei Platten decken einen Apéro für acht bis zehn Gäste als Ergänzung zu Häppchen ab.'))
    inner = (f'<div class="abs" style="left:17.1mm;top:25mm;width:195mm">{tab}<p class="txt11" style="margin-top:7mm">Käse unter anderem von der Käserei Rüttiberg in Schänis, Früchte und Gemüse nach Saison. Neu auf silbrigen oder schwarzen Platten statt Palmblatt — klein, mittel und gross nach Personenzahl. Bis die neuen Grössen festgelegt sind, gelten die Preise für 2, 4, 6 und 8 Personen.</p></div>'
             f'<div class="rows eng" style="left:232mm;top:25mm;width:155mm">{rechts}</div>')
    h += karte(14.9, 97.9, 390, 118, inner, bild=False) + hand('zum Teilen gemacht', 40, 201, -5)
    h += fuss(18, 'Alle Preise in Schweizer Franken.')
    return seite(h)

def s30(nr=28):
    """Der süsse Abschluss — sechs Karten unter einem Themenbild."""
    mp, ms, cc, cp = S['Mini Pâtisserie'], S['Mousse-Schale gefüllt'], S['Cup Cakes'], S['Cake Pops']
    h = hero(F('seite-28_hero'), 'DER SÜSSE<br>ABSCHLUSS',
             'Was aufs Buffet kommt und aus der Hand gegessen wird. Alles entsteht in unserer eigenen Konditorei. '
             'Am Platz serviert steht auf der nächsten Seite.', ghost='SÜSS')
    h += k6h(0, 'MINI PÂTISSERIE<br>ASSORTIERT', [tag('BELIEBT'), tag('VEGETARISCH', 'beige')],
             'Ein Querschnitt durch unsere Konditorei, in einem Bissen.',
             [('Sorten', mp['sorten'])],
             [('Mini Pâtisserie', 'pro Stück', 2.6)], bild=F('seite-28_patisserie'))
    h += k6h(1, 'MOUSSE-SCHALE<br>GEFÜLLT', [tag('VEGETARISCH', 'beige')],
             'Eine Geschmacksrichtung, eine Basis — beides wählen Sie. Für 4 bis 8 Personen.',
             [('Sorten', ms['sorten'])],
             [(n, u, v) for n, u, v in ms['preise']], bild=F('seite-28_mousse'))
    h += k6h(2, 'CUP CAKES', [tag('VEGETARISCH', 'beige')],
             'In herzigen Kinder-Sujets oder in zeitlosen Pastellfarben.',
             [('Sorten', cc['sorten']), ('Mindestmenge', cc['mindestmenge'])],
             [('Cup Cake', 'pro Stück', 5.9)], bild=F('seite-28_cupcakes'))
    h += k6h(3, 'CAKE POPS', [tag('VEGETARISCH', 'beige')],
             'Am Stiel, nach Ihren Wünschen ausdekoriert.',
             [('Sorten', cp['sorten']), ('Mit Alkohol', cp['alkoholisch'])],
             [('Cake Pop', 'pro Stück', 4.5)], bild=K(488, 30))
    h += k6h(4, 'DESSERT IM GLÄSLI', [tag('NOCH OFFEN', 'beige')],
             'Im Glas serviert, ohne Teller und ohne Besteck.',
             [('Sorten', 'Panna Cotta · Tobleronemousse · Schoggimousse · Gebrannte Creme')],
             [('Dessert im Gläsli', 'pro Stück', 5.5)], note='bleibt oder weg?', bild=F('seite-28_glaesli'))
    h += k6h(5, 'VEGANE<br>DESSERTVARIATIONEN', [tag('NOCH OFFEN', 'beige'), tag('VEGAN', 'beige')],
             'Aus der eigenen Konditorei, ganz ohne tierische Zutaten.',
             [('Sorten', 'Schokoladenkuchen · Mohnroulade · Kaffeekuchen · Erdbeer-Rhabarber-Torte · Cremeschnitte')],
             [('Vegane Desserts', 'pro Stück', 6.0)], note='bleibt oder weg?', bild=F('seite-28_schokokuchen'))
    def liste_(x): return e(' · '.join(x) if isinstance(x, (list, tuple)) else x)
    h += fuss(nr, 'Mindestmenge: 10 Stück pro Sorte oder 10 Stück gemischt pro Kategorie. Saisonal bei der Mini '
                  'Pâtisserie: ' + liste_(mp['saisonal']) + '. Die Mousse-Schale wählen Sie mit einer Basis: '
                  + liste_(ms['basis']) + '. Alle Preise in Schweizer Franken.')
    return seite(h)

def s32():
    """Alte Seite 32: Torten & Confiserie. Inhalt wie im Original, neu mit echten Bildern."""
    h = hero(F('seite-30_hero'), 'TORTEN &amp;<br>CONFISERIE',
             'Eine Torte kauft man nicht ein, man bespricht sie. Konditorei, Tortenhandwerk und Confiserie sind drei '
             'der sechs Handwerke in unserem Haus — der Teil, den andere Cateringbetriebe zukaufen müssen.', ghost='TORT')
    h += k3(0, 'TORTEN NACH IHRER IDEE', [tag('WICK-SIGNATURE', 'beige')],
            'Motiv, Grösse und Geschmack besprechen wir persönlich. Daraus entsteht die Offerte.',
            [('Auch vegan', 'Kirsch / Schokolade · Mohnroulade · Kaffeekuchen · Erdbeer / Rhabarber'),
             ('Beratung', 'Motiv, Grösse und Geschmack besprechen wir am Tisch')],
            [], note='das Stück, an das sich alle erinnern', bild=F('seite-30_torte'))
    h += k3(1, 'CONFISERIE', [tag('BELIEBT')],
            'Pralinen und Schokolade aus eigener Herstellung, mit Grand-Cru-Couverture von Felchlin.',
            [('Als Gastgeschenk', 'Am Platz, zum Kaffee oder als Dankeschön für die Helferinnen und Helfer'),
             ('Einzeln verpackt', 'Pralinen in kleinen Schachteln, auf Wunsch mit Ihrem Datum oder Ihrem Logo')],
            [], bild=F('seite-30_gastgeschenk'))
    h += k3(2, 'WAS SONST NOCH SÜSS IST', [],
            'Mini-Pâtisserie, Cup Cakes, Cake Pops, Mousse-Schalen und die Frucht-Spiessli stehen beim süssen '
            'Abschluss auf Seite 28. Die Desserts für den Tellerservice auf Seite 29.',
            [('Mit Logo oder Wunschdesign', 'Cup Cakes mit Logo oder Wunschdesign, vegetarisch')],
            [('Cup Cakes mit Logo', 'pro Stück', 7.5), ('Cake Pops mit Alkohol', 'pro Stück', 5.0)],
            bild=F('seite-28_patisserie'))
    h += fuss(30, 'Torten und Confiserie fertigen wir nach Offerte — für Torten nennt unsere Preisliste bewusst '
                  'keinen Betrag, weil Grösse, Motiv und Aufwand zu verschieden sind. '
                  'Alle übrigen Preise in Schweizer Franken.', arb=False)
    return seite(h)

# ---------- Konzept C: Menü-Doppelseite (ersetzt die bisherigen Seiten 25–28) ----------
def sph(t): return f'<div class="sph">{e(t)}</div>'
def liste(gruppen, keys):
    """Preisspalte aus den Gruppen des Sortiments."""
    h = ''
    for k in keys:
        h += sph(k) + '<div class="preise dicht">' + ''.join(pr(n, u or '', v) for n, u, v in gruppen[k]) + '</div>'
    return h

# ---------- Seiten mit Querverweisen (neue Nummerierung) ----------
LEGENDE = (('leg-brot', 'Brotauswahl'), ('leg-blatt', 'Vegetarisch'), ('leg-pfeile', 'Varianten'),
           ('leg-warm', 'Warm'), ('leg-korb', 'Mindestmenge'), ('leg-vegan', 'Vegan'))

def s6():
    """Ihr Weg — Inhaltsverzeichnis. Seitenzahlen nach der neuen Gliederung."""
    def zeilen(*paare): return ''.join(
        f'<div class="ivz"><span>{t}</span><span class="p"></span><span class="s">{n}</span></div>' for t, n in paare)
    sp = [
        ('01 · VERTRAUEN', zeilen(('Wick in Zahlen', 2), ('Referenzen', 3), ('Warum Wick Catering', 4), ('Ein Haus, viele Handwerke', 5))
         + '<h4 class="spaeter">02 · IHR ANLASS</h4>' + zeilen(('Was planen Sie?', 7))),
        ('03 · DIE PASSENDE FORM', zeilen(('Cateringformen', 8), ('Mengen planen', 9))
         + '<h4 class="spaeter">04 · DAS ANGEBOT</h4>' + zeilen(('Apéro-Pakete', 10), ('Apéro im Gläsli', 11), ('Brot &amp; Brötli', 12), ('Brötli gefüllt', 13), ('Brot XXL', 14))),
        ('APÉRO INDIVIDUELL', zeilen(('Belegtes, Canapés &amp; Fingerfood', 15), ('Spiessli', 16), ('Warme Häppchen', 17), ('Platten &amp; Sharing', 18))
         + '<h4 class="spaeter">UNTERWEGS</h4>' + zeilen(('Lunchbags', 19))),
        ('WARME KÜCHE', zeilen(('Drei Wege', 20))
         + '<h4 class="spaeter">WEG 01 · BUFFET</h4>' + zeilen(('Unsere Buffets', 21))
         + '<h4 class="spaeter">WEG 02 · KLASSIKER</h4>' + zeilen(('Für grosse Runden', 22))),
        ('WEG 03 · EIGENES MENÜ', zeilen(('In vier Schritten', 23), ('Die Proteine', 24), ('Beilagen und Saucen', 25))
         + '<h4 class="spaeter">DAZU</h4>' + zeilen(('Suppen und Salate', 26))
         + '<h4 class="spaeter">DRAUSSEN</h4>' + zeilen(('Grillplausch', 27))
         + '<h4 class="spaeter">FÜR ALLE</h4>' + zeilen(('Vegetarisch &amp; vegan', 31))),
        ('SÜSSER ABSCHLUSS', zeilen(('Fürs Buffet', 28), ('Dessert am Teller', 29), ('Torten &amp; Confiserie', 30))
         + '<h4 class="spaeter">05 · ANLASS KOMPLETT</h4>' + zeilen(('Vom Raum zum Fest', 32), ('Getränke', 33), ('Material &amp; Personal', 34), ('Eventraum', 35), ('Weitere Locations', 36))),
        ('06 · ANFRAGE', zeilen(('Erzählen Sie uns davon', 37))
         + '<h4 class="spaeter">AUSZEICHNUNGEN</h4>'
         + '<p class="ivt">Neu — aus der laufenden Sortimentsentwicklung</p>'
         + '<p class="ivt">Beliebt — bewährt und oft bestellt</p>'
         + '<p class="ivt">Wick-Signature — baut auf einem eigenen Wick-Produkt auf</p>'
         + '<p class="ivt">Vegetarisch und Vegan — im ganzen Sortiment gekennzeichnet</p>'
         + '<h4 class="spaeter">HANDWERKSLINIE</h4>'
         + '<p class="ivt">Die braune Linie am Seitenrand zeigt, welches der sechs Handwerke die Seite herstellt.</p>'),
    ]
    h = (f'<div class="vollbild"><img src="{K(116, 6)}"><div class="ov"></div></div>'
         f'<div class="box" style="top:14.9mm">IHR WEG</div><span class="bar" style="left:0;width:17mm"></span><span class="bar" style="left:73mm;width:28mm"></span>'
         f'<p class="intro" style="top:78mm;width:200mm">Diese Broschüre führt Sie in sechs Schritten zum fertigen Anlass — von der Frage, ob wir das können, bis zur Offerte.</p>'
         f'<div class="legk"><h4>LEGENDE</h4><div class="paare">'
         + ''.join(f'<div class="paar"><span class="lk">{icon(i)}</span><span>{t}</span></div>' for i, t in LEGENDE)
         + '</div></div>'
         + '<div class="ivsp">' + ''.join(f'<div class="ivc"><h4>{t}</h4>{inh}</div>' for t, inh in sp) + '</div>')
    h += f'<div class="marke hell">WICK — APÉRO &amp; CATERING</div><div class="pnr hell">6</div>'
    return seite(h)

def s8():
    """Welche Cateringform passt — mit den Verweisen der neuen Nummerierung."""
    h = kopf('WELCHE CATERINGFORM PASST?', 'Acht Formen, acht Rhythmen. Diese Seite ordnet ein — verbindliche Pakete und Preise stehen ab Seite 10.', 8, braun=(64.2,), ghost='FORM')
    def k(i, label, titel, desc, bloecke, rost=False):
        inner = (f'<h3>{titel}</h3><p class="desc">{e(desc)}</p>'
                 + ''.join((f'<div class="sph klein">{e(t)}</div>' if t else '') + f'<p class="txt105">{x}</p>' for t, x in bloecke))
        kk = karte(14.9 + i * 98.2, 97.9, 92.8, 132, f'<div style="padding:26.6mm 4.8mm 0">{inner}</div>', bild=False)
        kk = (f'<div class="kasten{" rost" if rost else ""}" style="left:{19.6 + i * 98.2}mm;top:65.9mm;width:83.4mm">{e(label)}</div>' + kk)
        return kk
    h += k(0, 'APÉRO', 'KLASSISCHER APÉRO', 'Einige Häppchen zum Anstossen, kalt und im Stehen.',
           [(None, 'Einzelprodukte ab Seite 12'), ('APÉRO BASIS', 'Vier Häppchen pro Person, davon eine Einheit süss. Fertig zusammengestellt. — Seite 10'),
            ('APÉRO RICHE', 'Acht Häppchen pro Person, davon zwei süss. Ersetzt eine Mahlzeit. — Seite 10'),
            ('APÉRO IM GLÄSLI', 'Kleine Portionen im Glas, zusätzlich zum Apéro Riche. — Seite 11')])
    h += k(1, 'ESSEN', 'BUFFET', 'Salate, warme Speisen und Desserts zum Selbstschöpfen — frei zusammengestellt.',
           [(None, 'Seiten 20 bis 26'), ('WARMES MENÜ', 'Tellerservice oder Wärmebehälter, vom einfachen Gericht bis zum mehrgängigen Essen. — Seite 23'),
            ('GRILLPLAUSCH', 'Mariniertes Fleisch oder Vegiplatte, Beilagen und Saucen — Sie grillieren selbst. — Seite 27')])
    h += k(2, 'UNTERWEGS', 'LUNCHBAG &amp; MOBILE VERPFLEGUNG', 'Fertig gepackt für unterwegs, Sitzungen und Anlässe ohne Küche.',
           [(None, 'Seite 19'), (None, 'Lunchbags liefern wir auch an Orte ohne Küche und ohne Kühlung.')])
    h += k(3, 'RUNDUM', 'VOLLSTÄNDIGES CATERING MIT SERVICE', 'Geschirr, Mobiliar, Getränke, Aufbau und Betreuung vor Ort — Sie sind Gast am eigenen Anlass.',
           [(None, 'Seiten 32 bis 36'), (None, 'Sie wissen noch nicht, was passt? Rufen Sie an — 055 210 15 44. Die Beratung ist kostenlos und unverbindlich.')], rost=True)
    h += fuss(8, 'Auf Seite 9 steht, wie viel es von jeder Form braucht. Alle Preise in Schweizer Franken.')
    return seite(h)

def kastenkarte(x, b, label, inner, rost=False, y=97.9, h=132, ky=65.9):
    """Karte mit weissem (oder rostfarbenem) Kasten obendrauf, wie auf den Seiten 8 bis 10."""
    return (f'<div class="kasten{" rost" if rost else ""}" style="left:{x + 4.7}mm;top:{ky}mm;width:{b - 9.4}mm">{e(label)}</div>'
            + karte(x, y, b, h, f'<div style="padding:26.6mm 4.8mm 0">{inner}</div>', bild=False))

def s9():
    """Mengen richtig planen — mit der Gläsli-Mindestmenge und neuen Verweisen."""
    h = kopf('MENGEN RICHTIG PLANEN', 'Wie viel es braucht, hängt vom Anlass ab. Diese Seite nennt nur Werte, die sich bei uns bewährt haben.', 9, braun=(64.2,), ghost='MEN')
    frage = lambda f, a: f'<p class="txt105"><b class="hervor">{e(f)}</b><br>{e(a)}</p>'
    c1 = (frage('Wie lange dauert der Anlass?', 'Ein Apéro von zwanzig Minuten braucht andere Mengen als einer, der in den Abend übergeht.')
          + frage('Kommt danach noch ein Essen?', 'Dann reicht der Apéro Basis mit vier Häppchen pro Person.')
          + frage('Oder ersetzt der Apéro die Mahlzeit?', 'Dann rechnen wir mit dem Apéro Riche: acht Häppchen pro Person.')
          + frage('Wie viel davon süss?', 'Beim Apéro Basis eine Einheit, beim Apéro Riche zwei.')
          + '<p class="txt105" style="color:#C9BCA8">Dauer, Getränkemenge und Bissenzahl je Produkt legen wir im Gespräch fest — dafür gibt es keine Faustregel, die für jeden Anlass stimmt.</p>')
    paar = lambda t, x: f'<div class="sph klein">{e(t)}</div><p class="txt105">{e(x)}</p>'
    c2 = (paar('Brötli', 'Minibrötli 3 Stk. · Partybrötli 2 Stk. · Bürli 1 Stk. pro Person')
          + paar('Partybrot', '100–150 g pro Person')
          + paar('Brot am Stück', 'Znüni 10 cm · Mittagessen 20 cm pro Person')
          + paar('Pain Surprise', 'Znüni 3 Stk. · Zmittag 5 Stk. pro Person')
          + paar('Gläsli-Apéros', '1 Gläsli pro Person, zusätzlich zum Apéro Riche'))
    c3 = ('<p class="txt105">Von Hand gefertigte Positionen stellen wir ab zehn Stück pro Sorte her. Das betrifft:</p>'
          + '<div class="punkte">' + '<br>'.join('· ' + t for t in (
              'Apérogebäck und Schinkengipfel', 'Canapés und belegte Brötli', 'Apérowraps',
              'Bäckerpastetli', 'Frischkäse-Pralinen', 'Mini-Pâtisserie, Cup Cakes, Cake Pops')) + '</div>'
          + '<p class="txt105">Viertel-Canapés sind nur in Viererschritten bestellbar. Platten gibt es ab zwei Personen, Grissini und Tray of Snacks nur als ganze Platte.</p>'
          + f'<div class="sph klein">Gläsli-Apéros</div><p class="txt105">Hier gilt eine eigene Mindestmenge: <b class="hervor">15 Stück pro Sorte</b>, und nur zusammen mit einem Apéro Riche. Seite 11.</p>')
    c4 = ('<p class="txt105">40 Gäste, Apéro nach der Trauung, danach Abendessen.</p>'
          + '<p class="txt105">Apéro Basis: 4 Häppchen pro Person, davon eine Einheit süss. Das sind 160 Einheiten, davon 40 süss.</p>'
          + '<p class="txt105">Als fertiges Paket ab CHF 10.50 pro Person — oder frei zusammengestellt aus dem Sortiment ab Seite 12.</p>'
          + '<p class="txt105">Getränke rechnen wir nach effektivem Verbrauch ab. Was ungeöffnet bleibt, kommt zurück.</p>')
    for i, (lab, inner, rost) in enumerate((('VIER FRAGEN', c1, False), ('PRO PERSON', c2, False),
                                            ('MINDESTMENGEN', c3, False), ('RECHENBEISPIEL', c4, True))):
        h += kastenkarte(14.9 + i * 98.2, 92.8, lab, inner, rost, h=150)
    h += fuss(9, 'Alle Preise in Schweizer Franken.')
    return seite(h)

def s10():
    """Apéro-Pakete — mit Verweis auf die Gläsli und neuen Seitenzahlen."""
    h = (f'<div class="rostvoll" style="height:95mm"></div>'
         f'<div class="kap hell" style="left:26mm;top:24mm">KAPITEL 04 / 06 &nbsp;·&nbsp; DAS ANGEBOT</div>'
         f'<h1 class="rosth">Fertig zusammengestellt.<br>Oder ganz nach Ihrem Kopf.</h1>'
         f'<p class="rostt">Zwei Pakete, die sich seit Jahren bewähren — und ab Seite 12 das vollständige Sortiment, aus dem Sie Ihren Apéro Schritt für Schritt selbst aufbauen.</p>'
         + zeitleiste(103, 110, (110,)) + ghostbox('ANG', 168))
    paar = lambda t, x: f'<div class="sph klein">{e(t)}</div><p class="txt105">{x}</p>'
    c1 = ('<p class="txt105" style="color:#C9BCA8">Nach einer Sitzung · Verpflegung zwischendurch · Geburtstag</p>'
          + '<div class="daten2"><span>Häppchen:</span><span>4 Häppchen pro Person</span><span>davon süss:</span><span>1 Einheit süss</span></div>'
          + paar('Variante A — CHF 10.70 pro Person', 'Partybrötli mix gefüllt, Apéro Chiliwürstli im Briochesmantel, Frischkäsekugel, Mini Pâtisserie')
          + paar('Variante B — CHF 10.50 pro Person', 'Apéro Wrap Poulet, Bäckerpastetli, Belegtes Brötli diagonal, Spiessli Frucht'))
    c2 = ('<p class="txt105" style="color:#C9BCA8">Ersetzt eine Mahlzeit · Mittag oder Abend · Firmenanlass · Hochzeit</p>'
          + '<div class="daten2"><span>Häppchen:</span><span>8 Häppchen pro Person</span><span>davon süss:</span><span>2 Einheiten süss</span></div>'
          + paar('Variante A — CHF 22.00 pro Person', 'Partybrötli mix gefüllt, Apéro Schinkengipfel, Frischkäsekugeln, Bäckerpastetli, Spiessli Anti Pasti, Palmblatt Grissini, 2 Stk. Mini Pâtisserie')
          + paar('Variante B — CHF 21.00 pro Person', 'Belegtes Brötchen diagonal, Frischkäsekugeln, Spiessli Frucht, Apéro Chiliwürstli im Briochesmantel, Apéro Wrap Couscous, Apéro Wrap Poulet, 2 Stk. Mini Pâtisserie')
          + f'<div class="hinweis" style="margin-top:4mm"><span class="kreis2">{icon("korb")}</span><p><b>Ergänzen Sie Ihren Apéro Riche mit Gläsli.</b> Kleine Portionen im Glas, 1 Gläsli pro Person — Seite 11.</p></div>')
    seiten = (('12–14', 'Brot, Brötli und Brot XXL'), ('15', 'Belegtes, Canapés und Fingerfood'),
              ('16', 'Spiessli'), ('17', 'Warme Häppchen'), ('18', 'Platten zum Teilen'),
              ('28–29', 'Süsser Abschluss'))
    c3 = ('<p class="txt105">Lieber eigene Sorten? Dann bauen Sie den Apéro aus dem Sortiment zusammen. Die Reihenfolge der folgenden Seiten entspricht dem Aufbau eines Buffets:</p>'
          + '<div class="daten2">' + ''.join(f'<span>{e(a)}</span><span>{e(b)}</span>' for a, b in seiten) + '</div>'
          + '<p class="txt105">Als Richtwert gelten dieselben Mengen wie bei den Paketen: vier Häppchen pro Person vor einem Essen, acht statt eines Essens.</p>')
    for i, (lab, inner, rost) in enumerate((('APÉRO BASIS', c1, False), ('APÉRO RICHE', c2, False),
                                            ('SELBST ZUSAMMENSTELLEN', c3, True))):
        h += kastenkarte(14.9 + i * 131.5, 127.3, lab, inner, rost, y=143, h=126, ky=111)
    h += fuss(10, 'Alle Preise in Schweizer Franken.')
    return seite(h)

def sGl():
    """Neue Seite ohne alte Nummer: Apéro im Gläsli, steht neu an elfter Stelle. Nur zusammen mit einem Apéro Riche."""
    gl = S['Gläsli-Apéros']
    ml = gl['mengenlogik']
    h = hero(F('seite-11_glaesli-thema'), 'APÉRO IM<br>GLÄSLI',
             'Kleine Portionen im Glas — mit Gabel oder Löffel gegessen, sättigender als ein Häppchen. Als Ergänzung zum Apéro Riche.', ghost='GLÄS')
    def sorte(s):
        k = f' {tag("VEGAN" if s["kennzeichnung"] == "vegan" else "VEG", "beige")}' if s['kennzeichnung'] else ''
        return f'<div class="gl"><span class="gn">{e(s["sorte"])}{k}</span><p>{e(s["zutaten"])}</p></div>'
    def col(x, kat): return (f'<div class="abs col" style="left:{x}mm;top:18mm;width:85mm">'
                             + sph(kat['name']) + ''.join(sorte(s) for s in kat['sorten']) + '</div>')
    staffel = ('<table class="tab staffel"><tr><th class="l">GÄSTE</th><th>SORTEN</th></tr>'
               + ''.join(f'<tr><td class="l">{e(g)}</td><td>{n}</td></tr>' for g, n in ml['staffelung']) + '</table>')
    regeln = (f'<div class="regelbox"><div class="rb1"><div class="rt">NUR MIT APÉRO RICHE</div>'
              f'<p>{e(gl["regel"])}</p></div>'
              f'<div class="rb1"><div class="rt">MINDESTENS 15 STÜCK PRO SORTE</div>'
              f'<p>Pro Gläsli-Sorte bestellen wir ab 15 Stück. {e(gl["nicht_enthalten"])}</p>'
              f'<div class="tags" style="margin-top:2.5mm">{tag("PREIS NACH KALKULATION", "beige")}</div></div>'
              f'<div class="rb1"><div class="rt">WIE VIEL PRO PERSON</div>'
              f'<p>{e(ml["empfehlung"])} <i>{e(ml["faktor"])}.</i></p></div>'
              f'<div class="rb2">{staffel}</div></div>')
    inner = (''.join(col(15 + i * 95, k) for i, k in enumerate(gl['kategorien']))
             + f'<div class="abs" style="left:15mm;top:95mm;width:370mm">{regeln}</div>')
    h += karte(14.9, 128, 390, 141, inner, bild=False)
    h += fuss(11, 'Gläsli-Apéros gibt es ausschliesslich in Kombination mit einem Apéro Riche. Mindestbestellmenge 15 Stück pro Sorte. Alle Preise in Schweizer Franken.')
    return seite(h)

def c20():
    """Einstieg: die drei Wege, jeder als eigene Karte mit Nummer, Symbol und Preisband."""
    h = kopf('WARME KÜCHE — DREI WEGE',
             'Dieselbe Küche, die am ESAF 80’000 Mahlzeiten produziert hat, kocht auch für dreissig Gäste. '
             'Welcher Weg passt, hängt an der Gästezahl und daran, wie serviert wird.', 20, braun=(44,), ghost='WEGE')
    wege = (
        ('01', 'korb', 'BUFFET', 'Die Gäste schöpfen selbst',
         'Wenn viele Gäste kommen und die Auswahl für sich sprechen soll.',
         (('Ab', '30 Personen'), ('Sie wählen', 'eines von sechs Buffets'), ('Abgerechnet', 'Pauschale pro Person')),
         'CHF 30.00 – 62.00', 'pro Person', 21),
        ('02', 'huet', 'KLASSIKER', 'Ein Gericht für alle',
         'Wenn es unkompliziert und sättigend sein soll — Vereinsanlass, Baustellenfest, Grossveranstaltung.',
         (('Ab', 'keine Mindestmenge'), ('Sie wählen', 'ein Gericht für alle'), ('Abgerechnet', 'pro Portion')),
         'CHF 16.50 – 28.50', 'pro Portion', 22),
        ('03', 'person', 'EIGENES MENÜ', 'Am Tisch serviert, Gang für Gang',
         'Wenn am Tisch serviert wird — Hochzeit, Gala, Geschäftsessen.',
         (('Ab', '10 Personen'), ('Sie wählen', 'Protein, Beilage, Gemüse, Sauce'), ('Abgerechnet', 'pro Person, aus vier Schritten')),
         'Beispiel CHF 52.00', 'pro Person', '23–25'),
    )
    for i_, (nr, ic, titel, unter, wenn, daten, preis, einheit, seite_) in enumerate(wege):
        inner = ('<div class="fuellen" style="padding:0">'
                 f'<div style="padding:9mm 7mm 0">'
                 f'<div class="wegkopf"><span class="wegnr">{nr}</span>{icon(ic)}</div>'
                 f'<h3 class="gross" style="margin-top:6mm">{e(titel)}</h3>'
                 f'<p class="wegsub">{e(unter)}</p>'
                 f'<p class="desc" style="margin-top:4mm">{e(wenn)}</p>'
                 + '<div class="wegdaten">' + ''.join(f'<span>{e(a)}</span><span>{e(b)}</span>' for a, b in daten) + '</div>'
                 f'<p class="wegseite">Steht auf Seite {e(str(seite_))}</p></div>'
                 f'<div class="preisband"><span>{e(einheit).upper()}</span><b>{e(preis)}</b></div></div>')
        h += karte(14.9 + i_ * 131.5, 44, 127.3, 190, inner, bild=False)
    h += (f'<div class="abs txt11" style="left:19.6mm;top:246mm;width:356mm;color:#2A2521">'
          'Suppe, Salat und Dessert wählen Sie unabhängig davon — sie passen zu allen drei Wegen. '
          'Sie stehen auf den Seiten 26 bis 29.</div>')
    h += fuss(20, 'Alle Preise in Schweizer Franken.')
    return seite(h)

def c21():
    """Weg 01 — die sechs Buffets."""
    bu = S['Buffets']
    h = hero(F('seite-21_hero'), 'UNSERE<br>BUFFETS',
             'Weg 01 — fertig zusammengestellt. Sechs Buffets, die sich an hunderten Anlässen bewährt haben. '
             'Sie wählen eines aus, wir bringen alles mit.', ghost='BUFF')
    for i, v in enumerate(bu['varianten']):
        inner = ('<div class="fuellen" style="padding:26.6mm 0 0">'
                 f'<div style="padding:0 4.8mm"><h3>{e(v["name"])}</h3><p class="desc">{e(v["unterzeile"])}</p>'
                 + grp('Inhalt', v['inhalt']) + '</div>'
                 f'<div class="preisband"><span>{e(bu["einheit"]).upper()}</span><b>{v["preis"]:.2f}</b></div></div>')
        h += karte(14.9 + i * 65.6, 166.5, 62.2, 102.4, inner, bild=False)
    h += fuss(21, 'Alle Buffets ab 30 Personen. Salatbuffet und Dessert lassen sich dazunehmen. Preise pro Person. Alle Preise in Schweizer Franken.')
    return seite(h)

def c22():
    """Weg 02 — die Klassiker."""
    kl = S['Klassiker für grosse Runden']
    h = hero(F('seite-22_hero'), 'KLASSIKER<br>FÜR GROSSE<br>RUNDEN',
             'Weg 02 — ein Gericht, eine Menge, ein Preis. Die Form, mit der wir am ESAF 80’000 Mahlzeiten '
             'ausgegeben haben.', ghost='KLAS')
    def gericht(g):
        tg = f' {tag(g["kennzeichnung"].upper(), "beige")}' if g.get('kennzeichnung') else ''
        return (f'<div class="ger"><div class="gz"><span class="gn">{e(g["name"])}{tg}</span>'
                f'<span class="gv">{g["preis"]:.2f}</span></div><p>{e(g["zutaten"])}</p></div>')
    sp = [kl['gerichte'][0:4], kl['gerichte'][4:8], kl['gerichte'][8:12]]
    band = ('<div class="abs salatbox" style="left:4.7mm;top:78mm;width:380.6mm;grid-template-columns:repeat(4,1fr)">'
            + ''.join(f'<div><div class="rt">{e(k.upper())}</div><p>{e(v)}</p></div>' for k, v in kl['hinweise'].items())
            + '</div>')
    inner = (''.join(f'<div class="abs col" style="left:{17.1 + i * 127}mm;top:14mm;width:118mm">{"".join(gericht(g) for g in s)}</div>' for i, s in enumerate(sp))
             + band)
    h += karte(14.9, 138, 390, 130.9, inner, bild=False)
    h += fuss(22, 'Alle Preise pro Portion. Alle Preise in Schweizer Franken.')
    return seite(h)

def c25():
    """Dazu — Suppen und Vorspeisen oben, alles rund um den Salat im eigenen Band."""
    su, vs, st, sb = S['Suppen'], S['Vorspeisen am Teller'], S['Salate am Teller'], S['Salatbuffet']
    h = hero(F('seite-26_hero'), 'SUPPEN<br>UND SALATE',
             'Passt zu allen drei Wegen. Eine Suppe vorweg, eine Vorspeise am Tisch — und alles rund um den Salat '
             'im Band darunter.', ghost='DAZU')
    def col(x, b, inhalt): return f'<div class="abs col" style="left:{x}mm;top:12mm;width:{b}mm">{inhalt}</div>'
    def zeilen(paare):
        return ('<table class="tab staffel">' + ''.join(
            '<tr><td class="l">{}</td><td>{}</td></tr>'.format(e(n), chf(v)) for n, v in paare) + '</table>')
    c1 = liste(su['gruppen'], ('Klassisch',))
    c2 = liste(su['gruppen'], ('Herzhaft',))
    c3 = liste(su['gruppen'], ('Saisonal',))
    c4 = liste(vs['gruppen'], ('Kalt',))
    c5 = liste(vs['gruppen'], ('Warm',))
    staffel = ('<table class="tab staffel"><tr><th class="l">SORTEN</th><th>AB PERS.</th><th>PRO PERS.</th></tr>'
               + ''.join('<tr><td class="l">{}</td><td>{}</td><td>{:.2f}</td></tr>'.format(
                   e(n.split(',')[0]), e(n.split('ab ')[1].replace(' Personen', '')), v) for n, _, v in sb['preise'])
               + '</table>')
    band = ('<div class="abs salatbox" style="left:4.7mm;top:60mm;width:380.6mm;grid-template-columns:1.4fr 1fr .8fr 1fr .62fr;gap:5mm">'
            f'<div><div class="rt">SALATE AM TELLER</div>{zeilen([(n, v) for n, _, v in st["preise"]])}</div>'
            f'<div><div class="rt">SALATBUFFET</div><p>{e(sb["beschreibung"])}</p>{staffel}</div>'
            + ''.join(f'<div><div class="rt">{e(k)}</div><p>{e(" · ".join(x))}</p></div>' for k, x in sb['gruppen'].items())
            + '</div>')
    spalten = ((12, 62, c1), (77, 62, c2), (142, 62, c3), (207, 88, c4), (299, 88, c5))
    inner = ''.join(col(x, b_, c) for x, b_, c in spalten) + band
    h += karte(14.9, 138, 390, 130.9, inner, bild=False)
    h += fuss(26, 'Alle Preise pro Portion, Salatbuffet pro Person. ' + e(su['hinweis']) + ' ' + e(vs['saisonal'])
                  + ' ' + e(sb['hinweis']) + ' Alle Preise in Schweizer Franken.')
    return seite(h)

def c28():
    """Dessert am Teller."""
    de = S['Dessert am Teller']
    h = hero(F('seite-29_hero'), 'DESSERT<br>AM TELLER',
             'Wird am Platz serviert und gehört deshalb zum Tellerservice — wie das eigene Menü.', ghost='DESS')
    hinw = ''.join(row(ic, k + ':', e(v)) for ic, (k, v) in zip(('person', 'korb', 'blatt', 'huet'), de['hinweise'].items()))
    inner = (f'<div class="abs col" style="left:15mm;top:16mm;width:180mm">{sph("Die Auswahl")}<div class="preise dicht">'
             + ''.join(pr(n, '', v) for n, _, v in de['preise']) + '</div>'
             + f'<p class="txt105" style="margin-top:4mm;color:#E6DCCB">{e(de["saisonal"])}</p></div>'
             + f'<div class="rows eng" style="left:215mm;top:16mm;width:170mm">{hinw}</div>')
    h += karte(14.9, 138, 390, 130.9, inner, bild=False)
    h += fuss(29, 'Alle Preise pro Portion, Tellerservice ab 20 Personen. Alle Preise in Schweizer Franken.')
    return seite(h)

def c26():
    """Draussen — Grillplausch und Burgerplausch."""
    gp, bp = S['Grillplausch'], S['Burgerplausch']
    def band(zeilen):
        """Preiszeilen als rostfarbenes Band am Kartenfuss."""
        return ('<div class="preisband mehr">' + ''.join(
            f'<div><span>{e(n).upper()}</span><em>{e(u or "")}</em><b>{v:.2f}</b></div>' for n, u, v in zeilen) + '</div>')
    h = hero(F('seite-27_hero'), 'GRILL-<br>PLAUSCH', e(gp['beschreibung']) + ' Auf Wunsch bringen wir Grill, Zelt und das übrige Material gleich mit.', ghost='GRIL')
    for i, v in enumerate(gp['varianten']):
        ts = [tag(v['kennzeichnung'].upper(), 'beige')] if v.get('kennzeichnung') else []
        inner = ('<div class="fuellen" style="padding:26.6mm 0 0">'
                 f'<div style="padding:0 4.8mm"><h3>{e(v["name"])}</h3>{tags(*ts)}' + grp('Inhalt', v['inhalt']) + '</div>'
                 + band(v['preise']) + '</div>')
        h += karte(14.9 + i * 79.2, 138, 75.8, 130.9, inner, bild=False)
    inner_d = ('<div style="padding:26.6mm 4.8mm 0">' + f'<h3>DAZU</h3><p class="desc">Beilage und Gemüse wählen Sie aus derselben Auswahl wie beim eigenen Menü — Seite 25.</p>'
               + sph('Saucen im Portionentöpfli') + '<div class="preise dicht">' + ''.join(pr(n, u, p) for n, u, p in gp['saucen']) + '</div>'
               + '</div>')
    inner_d = ('<div class="fuellen" style="padding:26.6mm 0 0">' + inner_d.replace('<div style="padding:26.6mm 4.8mm 0">', '<div style="padding:0 4.8mm">')
               + '<div class="preisband" style="display:block"><p style="font-size:9pt;line-height:4mm;color:#F4E6D8">'
                 'Grill, Zelt und Kühlanhänger mieten Sie bei uns.</p></div></div>')
    h += karte(14.9 + 3 * 79.2, 138, 75.8, 130.9, inner_d, bild=False)
    inner_b = ('<div class="fuellen" style="padding:26.6mm 0 0">'
               + f'<div style="padding:0 4.8mm"><h3>BURGER-PLAUSCH</h3><p class="desc">{e(bp["beschreibung"])}</p>'
               + grp('Dazu', bp['inhalt']) + f'<div class="hand inl">{e(bp["hinweis"])}</div></div>'
               + band(bp['preise']) + '</div>')
    h += karte(14.9 + 4 * 79.2, 138, 75.8, 130.9, inner_b, bild=False)
    h += fuss(27, 'Grillplatten ab 20 Personen. Das Fleisch wird gleichmässig verteilt. Alle Preise in Schweizer Franken.')
    return seite(h)

def c27(): return s30(nr=28)   # «Fürs Buffet» steht in der neuen Zählung auf Seite 28

def c23():
    hz = S['Eigenes Menü — Schritt 01, Herzstück']
    sc = S['Eigenes Menü — Schritt 02 bis 04']
    h = kopf('IHR EIGENES MENÜ',
             'Weg 03 — Sie stellen das Menü selbst zusammen. Am Tisch serviert, Gang für Gang. Vier Schritte, vier Preise, eine Summe.', 23, braun=(44,), ghost='MENÜ')
    schritte = ''.join(row(None, nr, f'<b>{t}</b><br>{x}') for nr, t, x in (
        ('01', 'Die Proteine', 'Fleisch, Fisch oder eine vegetarische Hauptkomponente. Das Gewicht steht dabei.'),
        ('02', 'Die Stärkebeilage', 'Gratin, Risotto, Teigwaren, Kartoffeln oder Polenta.'),
        ('03', 'Das Gemüse', 'Saisonal, gegrillt oder als einzelne Sorte.'),
        ('04', 'Die Sauce', 'Was die drei Teile zusammenhält.')))
    tab = ('<table class="tab"><tr><th>SO RECHNET SICH EIN MENÜ</th><th></th><th></th></tr>'
           + ''.join(f'<tr><td>{e(n)}</td><td class="g">{e(u or "")}</td><td>{v:.2f}</td></tr>' for n, u, v in sc['rechenbeispiel'])
           + '</table>')
    inner = (f'<div class="abs" style="left:17.1mm;top:18mm;width:170mm"><div class="sph">SO GEHEN SIE VOR</div>'
             f'<div class="rows eng" style="position:static;width:170mm;margin-top:4mm">{schritte}</div></div>'
             f'<div class="abs" style="left:205mm;top:18mm;width:182mm">{tab}'
             f'<p class="txt11" style="margin-top:5mm">Jede der vier Zeilen lässt sich tauschen, die Summe verschiebt sich entsprechend. So wissen Sie vor der Offerte, woran Sie sind.</p>'
             f'<p class="txt105" style="margin-top:3mm;color:#E6DCCB">Mindestmenge {e(hz["mindestmenge"])} · {e(hz["einheit"])}</p></div>')
    h += karte(14.9, 44, 390, 108, inner, bild=False) + hand('vier Zeilen,<br>ein Preis', 330, 163, -5, 16)
    h += fuss(23, 'Mindestmenge 10 Personen. Alle Preise pro Person. Suppe, Vorspeise und Dessert kommen aus den eigenen Kapiteln dazu. Alle Preise in Schweizer Franken.')
    return seite(h)

def wahlspalte(x, b, inhalt, top=18):
    return f'<div class="abs col" style="left:{x}mm;top:{top}mm;width:{b}mm">{inhalt}</div>'

def c24():
    """Schritt 01 — die Proteine, nach Fleischart geordnet."""
    hz = S['Eigenes Menü — Schritt 01, Herzstück']['gruppen']
    h = kopf('DIE AUSWAHL · SCHRITT 01 — DIE PROTEINE',
             'Eine Hauptkomponente pro Menü. Gewicht roh gewogen, Preise pro Person.', 24, braun=(44,), ghost='PROT')
    inner = (wahlspalte(15, 85, liste(hz, ('Rind', 'Kalb')))
             + wahlspalte(110, 85, liste(hz, ('Schwein',)))
             + wahlspalte(205, 85, liste(hz, ('Geflügel',)))
             + wahlspalte(300, 85, liste(hz, ('Fisch', 'Vegetarisch & vegan'))))
    h += karte(14.9, 44, 390, 215, inner, bild=False)
    h += fuss(24, 'Das Protein bestimmt den Preis des Menüs. Beilagen, Gemüse und Sauce stehen auf der nächsten Seite. '
                  'Preise pro Person, Gewicht roh gewogen. Alle Preise in Schweizer Franken.')
    return seite(h)

def c24b():
    """Schritt 02 bis 04 — Beilage, Gemüse und Sauce, mit den drei Schrittbildern."""
    sc = S['Eigenes Menü — Schritt 02 bis 04']['gruppen']
    h = kopf('DIE AUSWAHL · BEILAGEN UND SAUCEN',
             'Schritt 02 bis 04: eine Stärkebeilage, ein Gemüse, eine Sauce. Preise pro Person.', 25, braun=(44,), ghost='BEIL')
    for i, (cap, n) in enumerate((('02 · Stärkebeilage', 'staerkebeilage'), ('03 · Gemüse', 'gemuese'), ('04 · Sauce', 'sauce'))):
        x = 15 + i * 131.5
        h += img(F(f'seite-23_{n}'), x, 44, 127.3, 52.9) + f'<div class="cap" style="left:{x}mm;top:98.6mm;width:127.3mm">{e(cap)}</div>'
    inner = (wahlspalte(0.1, 127.3, liste(sc, ('02 Stärkebeilage',)), top=66)
             + wahlspalte(131.6, 127.3, liste(sc, ('03 Gemüse',)), top=66)
             + wahlspalte(263.1, 127.3, liste(sc, ('04 Sauce',)), top=66)
             + '<div class="abs txt11" style="left:0.1mm;top:150mm;width:258mm">Jede Zeile lässt sich tauschen, die Summe '
               'verschiebt sich entsprechend. Risotto, Ravioli und Tagliatelle bringen die Stärkebeilage schon mit — '
               'dann entfällt Schritt 02.</div>')
    h += karte(14.9, 44, 390, 175, inner, bild=False) + hand('vier Zeilen,<br>ein Preis', 300, 205, -5, 16)
    h += fuss(25, 'Eine Stärkebeilage gehört zu jedem Menü — ausser das Protein bringt sie schon mit. Risotto, Ravioli und '
                  'Tagliatelle brauchen keine zweite Beilage. Preise pro Person. Alle Preise in Schweizer Franken.')
    return seite(h)

def s33():
    """Alte Seite 33: Für alle — vegetarisch und vegan. Nachgeführt auf den neuen Stand."""
    h = kopf('FÜR ALLE — VEGETARISCH & VEGAN',
             'Vegetarische und vegane Gäste sollen nicht die Reste essen. Diese Seite fasst zusammen, was rein '
             'pflanzlich ist.', 31, braun=(64.2, 105.8), ghost='VEGA')
    bilder = (('seite-12_partybrot', 'Partybrot'), ('seite-15_baeckerpastetli', 'Bäckerpastetli Rüebli-Sesam'),
              ('seite-16_spiessli-frucht-klein', 'Spiessli Frucht klein'), ('seite-17_falafel', 'Falafel-Bissen'),
              ('seite-28_patisserie', 'Mini Pâtisserie'))
    for i, (n, cap) in enumerate(bilder):
        x = 52.0 + i * 65.8
        h += img(F(n), x, 65.9, 52.9, 52.9) + f'<div class="cap" style="left:{x}mm;top:60.5mm;width:52.9mm;color:#7A4424">{e(cap)}</div>'
    vegan = (('Partybrot', 'pro kg', 11.0), ('Traubenbrötli', 'pro Grösse', 0.8),
             ('Partybrötli leer (Weiss, Para)', 'pro Stück', 0.8), ('Bäckerpastetli Rüebli-Sesam', 'pro Stück', 2.7),
             ('Spiessli Frucht klein', 'pro Stück', 2.0), ('Mini Pâtisserie (Cremeschnitte)', 'pro Stück', 2.6),
             ('Falafel-Bissen, Ingwer-Karottensauce', 'pro Stück', None),
             ('Falafelbällchen, Ingwer-Karottensauce, Gemüsecouscous', 'pro Portion', 15.0),
             ('Veganer Burgerpatty (2× 113 g), Wedges-Kartoffeln, Gemüse', 'pro Portion', 25.5))
    c1 = sph('Vegan im Sortiment') + '<div class="preise dicht">' + ''.join(pr(*v) for v in vegan) + '</div>'
    gl = S['Gläsli-Apéros']
    def glsorten(art):
        return ' · '.join(so['sorte'] for k in gl['kategorien'] for so in k['sorten'] if so['kennzeichnung'] == art)
    rows = (row('leg-vegan', 'Gläsli vegan:', e(glsorten('vegan')) + ' — Seite 11')
            + row('leg-blatt', 'Gläsli vegetarisch:', e(glsorten('vegetarisch')) + ' — Seite 11')
            + row('leg-vegan', 'Vegane Torten:', 'Kirsch / Schokolade · Mohnroulade · Kaffeekuchen · Erdbeer / Rhabarber — Seite 30')
            + row('leg-blatt', 'Vegetarisch:', 'Ein grosser Teil des Sortiments ist vegetarisch — Käse, Ei, Tomaten &amp; Mozzarella, Kräuterquark, Spargeln und Zigerbrüüt.')
            + row('leg-korb', 'Mindestmenge:', '10 Stück pro Sorte')
            + row('leg-warm', 'Suppen:', 'Alle Suppen gibt es auch vegan — Seite 26. Das Sortiment ergänzen wir laufend.'))
    c2 = f'<div class="rows eng" style="position:static;width:100%">{rows}</div>'
    c3 = (f'<h3>RÜEBLI-SESAM-TARTELETTE</h3>{tags(tag("NEU"), tag("VEGAN", "beige"))}'
          '<p class="desc">Veganes Tartelette mit Rüebli-Sesam-Crème, geröstetem Sesam und Kresse.</p>'
          + grp('Format', '1–2 Bissen · kalt', False)
          + '<div class="preise">' + pr('Rüebli-Sesam-Tartelette', 'pro Stück', None) + '</div>'
          '<div class="hand inl">Für einen ausgewogenen Apéro mit zwei bis drei weiteren Sorten kombinieren.</div>')
    def col(x, b, inhalt): return f'<div class="abs col" style="left:{x}mm;top:22mm;width:{b}mm">{inhalt}</div>'
    inner = col(17.1, 150, c1) + col(180, 120, c2) + col(312, 73, c3)
    h += karte(14.9, 97.9, 390, 148, inner, bild=False) + hand('niemand isst die Reste', 40, 258, -5, 17)
    h += fuss(31, 'Der vegane Apéro Wrap Couscous ist gestrichen — eine vegane Alternative ist in Arbeit. '
                  'Mindestbestellmenge 10 Stück pro Sorte bei Apérogebäck, Canapés, Wraps, Pastetli, Frischkäse-Pralinen '
                  'und Mini-Pâtisserie. Mit «Neu» gekennzeichnete Positionen stammen aus der laufenden '
                  'Sortimentsentwicklung; Preis, Mindestmenge und Allergene folgen nach Abschluss der Kalkulation. '
                  'Alle Preise in Schweizer Franken.', arb=False)
    return seite(h)

def s37():
    """Alte Seite 37: Eventraum Säntisblick. Neu 80 Sitzplätze, mit Zelt bis 400 Personen."""
    h = hero(F('seite-35_hero'), 'EVENT-<br>RAUM',
             'Wicks Eventraum «Säntisblick» — bis 80 Sitzplätze, mit Zeltaufbau bis 400 Personen. Heimelig, '
             'vielfältig und buchbar für Ihren persönlichen Anlass. Auf Wunsch mit Catering aus unserem Haus: '
             'Raum, Catering und Betreuung aus einer Hand.', ghost='RAUM')
    preise = (('Raummiete, Rückgabe am Folgetag bis Mittag', '', 450.0), ('TV, 86 Zoll Ultra HD', '', 100.0),
              ('Zusätzlicher Kühlschrank', 'pro Stück', 30.0), ('Tischgarnitur / Stehtisch inkl. Tuch', 'pro Stück', 30.0),
              ('Kaffee', 'pro Portion', 3.0), ('Personal vor Ort', 'pro Person und Stunde', 60.0))
    rows = (row('person', 'Platz:', 'Bis 80 Sitzplätze im Raum. Mit Zeltaufbau davor wächst der Anlass auf bis zu 400 Personen — für Sitzung, Geschäftsessen, Geburtstagsfeier oder Trauerfeier.')
            + row('huet', 'Catering:', 'Catering, Brunch und Mietgeschirr nach Offerte.')
            + row('auge', 'Gut zu wissen:', 'Bei einer Konsumation ab CHF 2000.00 entfällt die Raummiete. Rückgabe besenrein, allfällige Reinigung CHF 200.00.'))
    inner = (f'<div class="abs" style="left:17.1mm;top:18mm;width:180mm"><div class="sph">Was der Raum kostet</div>'
             + '<div class="preise dicht">' + ''.join(pr(*v) for v in preise) + '</div></div>'
             + f'<div class="rows eng" style="left:215mm;top:18mm;width:170mm">{rows}</div>')
    h += karte(14.9, 138, 390, 130.9, inner, bild=False) + hand('Raum, Catering und<br>Betreuung aus einer Hand', 215, 255, -5, 16)
    h += fuss(35, 'Der Zeltaufbau vor dem Eventraum ist nach Offerte. Alle Preise in Schweizer Franken.', arb=False)
    return seite(h)

def sLoc():
    """Neue Seite nach dem Säntisblick: weitere Eventlocations, die wir beliefern.

    Die Zahlen stammen aus den öffentlichen Angaben der Locations und sind noch
    nicht bei den Betreibern bestätigt.
    """
    h = hero(F('seite-36_locations'), 'WEITERE<br>LOCATIONS',
             'Unser Catering bleibt nicht im eigenen Haus. Wir liefern regelmässig in die grossen Säle der Region — '
             'eingespielt mit den Betreibern, mit eigenem Material und eigenem Personal vor Ort.', ghost='LOCA')
    h += k3(0, 'ENTRA RAPPERSWIL', [tag('BELIEBT')],
            'Die grosse Bühne der Region. Saal, Foyer und mehrere Seminarräume unter einem Dach.',
            [('Adresse', 'Obere Bahnhofstrasse 58, 8640 Rapperswil'),
             ('Grösse', 'Saal: Bankett 432 Personen · Apéro 600 Personen · bis 1050 Personen im ganzen Haus'),
             ('Passt für', 'Generalversammlung · Firmenanlass · Konzert · Grossanlass')],
            [], note='Wir waren hier schon mehrfach Cateringpartner.', bild=False)
    h += k3(1, 'EVENTHOUSE RAPPERSWIL', [],
            'Eine ehemalige Industriehalle mitten in Rapperswil-Jona, roh und grosszügig.',
            [('Adresse', '[FEHLT: Adresse]'),
             ('Grösse', 'Halle: bis 600 Gäste · Saal: bis 200 Personen · dazu Foyer und Glaslounge'),
             ('Passt für', 'Hochzeit · Firmenfest · Abendanlass mit Apéro im Foyer')],
            [], bild=False)
    h += k3(2, 'RADIO ZÜRISEE LOFT', [],
            'Das Loft über dem Bahnhof Rapperswil — klein, hell und mitten im Zentrum.',
            [('Adresse', 'Bahnhofplatz 1, 8640 Rapperswil'),
             ('Grösse', '120 m² · Bankett 66 Personen · Apéro 100 Personen · Seminar 30 Personen'),
             ('Passt für', 'Sitzung · Kundenanlass · Apéro riche im kleinen Kreis')],
            [], bild=False)
    h += fuss(36, 'Die genannten Grössen stammen aus den öffentlichen Angaben der Locations und sind unverbindlich — '
                  'massgebend ist die Auskunft der Betreiberin. Miete und Technik rechnen die Locations direkt mit '
                  'Ihnen ab; wir offerieren das Catering. [Bitte bestätigen: Adresse Eventhouse, Fotos der beiden '
                  'übrigen Locations, und ob weitere Säle auf die Seite sollen.]', arb=False)
    return seite(h)

# Schlüssel = alte Seitenzahl. 0 ist die neue Gläsli-Seite, die es im Original noch nicht gibt.
SEITEN = [(0, sGl), (6, s6), (8, s8), (9, s9), (10, s10), (11, s11alt), (12, s12), (13, s13),
          (14, s14), (16, s16), (17, s17), (18, s18), (19, s19), (30, s30), (32, s32), (33, s33), (37, s37), (1, sLoc)]
# Konzept C: der neue Essensteil. Eigene Nummerierung, noch nicht in die 40 Seiten eingebaut.
KAPITEL_C = [(20, c20), (21, c21), (22, c22), (23, c23), (24, c24), (25, c24b), (26, c25), (27, c26), (28, c27), (29, c28)]

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
.sph{font:600 8pt 'Wick Sans';letter-spacing:.16em;color:#E6DCCB;margin:5mm 0 2mm;border-bottom:.2mm solid #3A3836;padding-bottom:1.6mm}
.col .sph:first-child,.abs>.sph:first-child{margin-top:0}
.preise.dicht{margin-top:0}
.preise.dicht .pr{line-height:4.9mm}
.preise.dicht .pr .n{font-size:10.5pt}
.preise.dicht .pr .u{font-size:7.5pt}
.preise.dicht .pr .v{font-size:10.5pt;min-width:11mm}
.tab td.g{font-family:'Wick Slab';font-weight:400;font-size:8.5pt;color:#E6DCCB}
.tab.verg td,.tab.verg th{vertical-align:top}
.tab.verg td.l,.tab.verg th.l{text-align:left;padding-right:5mm;font-family:'Wick Slab';font-weight:400;font-size:10.5pt;line-height:4.8mm}
.tab.verg th.l{font:600 8pt 'Wick Sans';letter-spacing:.16em;color:#E6DCCB}
.tab.verg td.lbl2{text-align:left;width:28mm;font:600 8pt 'Wick Sans';letter-spacing:.14em;color:#B9A892;padding-right:4mm}
.ger{margin-bottom:4.2mm}
.ger .gz{display:flex;align-items:baseline;gap:2mm}
.ger .gn{flex:1 1 auto;font-size:11pt;line-height:4.8mm;font-weight:700}
.ger .gv{font:500 11pt 'Wick Sans';white-space:nowrap}
.ger p{font-size:8.5pt;line-height:3.8mm;color:#C9BCA8;margin-top:.6mm}
.sph.klein{font-size:7pt;margin:3.5mm 0 1.2mm;border:0;padding:0}
.pr.klein{line-height:4.9mm}
.pr.klein .n{font-size:10.5pt}
.pr.klein .u{font-size:7.5pt}
.pr.klein .v{font-size:10.5pt;min-width:11mm}
.gl{margin-bottom:2.5mm}
.gl .gn{font-size:10.5pt;line-height:4.6mm;font-weight:700}
.gl .gn .tag{margin-left:1.5mm;vertical-align:.4mm}
.gl p{font-size:8.5pt;line-height:3.8mm;color:#C9BCA8;margin-top:.4mm}
.regelbox{display:grid;grid-template-columns:1fr 1fr 1fr .62fr;gap:8mm;background:#7A4424;padding:4.5mm 7mm}
.salatbox{display:grid;grid-template-columns:1.15fr 1fr 1.25fr .62fr;gap:7mm;background:#7A4424;padding:4.5mm 6mm}
.salatbox .rt{font:600 8pt 'Wick Sans';letter-spacing:.16em;color:#fff;margin-bottom:2.2mm}
.salatbox p{font-size:8.5pt;line-height:3.9mm;color:#F4E6D8}
.salatbox .tab.staffel{margin-top:2mm}
.fuellen{height:100%;display:flex;flex-direction:column}
.preise.unten{margin-top:auto}
.preisband{margin-top:auto;background:#7A4424;display:flex;align-items:baseline;justify-content:space-between;padding:3.4mm 4.8mm 3mm}
.preisband span{font:600 7pt 'Wick Sans';letter-spacing:.16em;color:#F2E4D4}
.preisband b{font:500 17pt 'Wick Sans';color:#fff;line-height:1}
.wegkopf{display:flex;align-items:center;justify-content:space-between}
.wegnr{font:500 34pt 'Wick Sans';line-height:1;color:#7A4424}
.wegkopf .ic{width:13mm;height:13mm}
.wegsub{font:400 10.5pt 'Wick Slab';line-height:4.8mm;color:#E6DCCB;margin-top:1.6mm}
.wegdaten{display:grid;grid-template-columns:26mm 1fr;row-gap:2mm;column-gap:3mm;font-size:9.5pt;line-height:4.2mm;margin-top:5mm;border-top:.2mm solid #3A3836;padding-top:4mm}
.wegdaten span:nth-child(odd){font:600 7pt 'Wick Sans';letter-spacing:.14em;color:#B9A892;padding-top:.5mm}
.wegdaten span:nth-child(even){color:#fff}
.wegseite{font:600 7pt 'Wick Sans';letter-spacing:.16em;color:#E6DCCB;margin-top:5mm}
.preisband.mehr{display:block}
.preisband.mehr>div{display:flex;align-items:baseline;gap:2.5mm}
.preisband.mehr>div+div{margin-top:1.6mm}
.preisband.mehr span{flex:0 0 auto}
.preisband.mehr em{flex:1 1 auto;font-style:normal;font:400 7pt 'Wick Slab';color:#E7CBA9;text-align:right}
.preisband.mehr b{font-size:13pt}
.regelbox .rt{font:600 8pt 'Wick Sans';letter-spacing:.16em;color:#fff;margin-bottom:2.2mm}
.regelbox p{font-size:9pt;line-height:4mm;color:#F4E6D8}
.regelbox i{font-style:italic}
.regelbox .tag.beige{border-color:#E7CBA9;color:#F6EADC}
.tab.staffel th,.tab.staffel td{font-size:9pt;padding:.7mm 0;color:#F4E6D8;border-top-color:rgba(255,255,255,.22)}
.tab.staffel th{color:#E7CBA9;font:600 7pt 'Wick Sans';letter-spacing:.14em;padding-bottom:1.4mm}
.tab.staffel td.l,.tab.staffel th.l{text-align:left}
.rostvoll{position:absolute;left:0;right:0;top:0;background:#7A4424}
.rosth{position:absolute;left:26mm;top:40mm;font:600 19pt 'Wick Sans';line-height:9mm;letter-spacing:.01em;color:#fff}
.rostt{position:absolute;left:26mm;top:68mm;width:150mm;font-size:11pt;line-height:5mm;color:#F2E4D4}
.daten2{display:grid;grid-template-columns:34mm 1fr;row-gap:1.8mm;column-gap:3mm;font-size:10pt;line-height:4.4mm;margin:2.5mm 0 3mm}
.daten2 span:nth-child(odd){font-weight:700;color:#fff}
.daten2 span:nth-child(even){color:#DCD3C4}
.kreis2{width:8mm;height:8mm;flex:0 0 auto}
.kreis2 img{width:8mm;height:8mm}
.vollbild{position:absolute;inset:0;overflow:hidden}
.vollbild img{width:100%;height:100%;object-fit:cover;display:block}
.vollbild .ov{position:absolute;inset:0;background:linear-gradient(90deg,rgba(18,17,16,.97) 0%,rgba(18,17,16,.93) 26%,rgba(18,17,16,.62) 52%,rgba(18,17,16,.38) 100%)}
.legk{position:absolute;right:0;top:0;width:152mm;height:106mm;background:#7A4424;border-bottom-left-radius:106mm;padding:16mm 14mm 0 38mm;z-index:4}
.legk h4{font:600 9pt 'Wick Sans';letter-spacing:.2em;color:#fff;margin-bottom:7mm}
.legk .paare{display:grid;grid-template-columns:1fr 1fr;gap:5mm 8mm}
.legk .paar{display:flex;align-items:center;gap:3.5mm}
.legk .lk{width:9mm;height:9mm;flex:0 0 auto}
.legk .lk img{width:9mm;height:9mm}
.legk span{font-size:9.5pt;color:#F6EFE4}
.ivsp{position:absolute;left:14.9mm;top:100mm;width:390mm;display:grid;grid-template-columns:repeat(7,1fr);gap:3.2mm;z-index:3}
.ivc{background:#1F1F1F;padding:6mm 4.6mm;min-height:150mm}
.ivc h4{font:600 7.4pt 'Wick Sans';letter-spacing:.14em;color:#fff;line-height:4mm;margin-bottom:3.5mm}
.ivc h4.spaeter{margin-top:6mm}
.ivz{display:flex;align-items:baseline;gap:1mm;font-size:7.4pt;line-height:3.8mm;color:#D2C9BA;margin-bottom:1.7mm}
.ivz .p{flex:1;border-bottom:.15mm dotted #6A5C51;transform:translateY(-.7mm)}
.ivz .s{color:#fff;font-family:'Wick Sans';font-weight:500}
.ivt{font-size:7pt;line-height:3.6mm;color:#C2B7A6;margin-bottom:2.4mm}
.marke.hell,.pnr.hell{color:#E6DCCB;z-index:5}
.kasten{position:absolute;height:42mm;background:#FBF9F4;border:.25mm solid #EFE7D8;display:flex;align-items:center;justify-content:center;
  font:600 8.6pt 'Wick Sans';letter-spacing:.17em;color:#1F1F1F;z-index:2}
.kasten.rost{background:#7A4424;border-color:#7A4424;color:#fff}
.col h3{margin-bottom:.5mm}
.col .grp.k{margin-bottom:1.2mm}
.col .desc{margin:1.4mm 0 1.8mm}
.col .preise{margin-top:2mm}
.fuss{position:absolute;left:15mm;top:277.3mm;width:390mm;font-size:6pt;line-height:2.8mm;color:#2A2521}
.marke{position:absolute;right:14mm;top:286.2mm;font:500 9pt 'Wick Sans';letter-spacing:.12em;color:#7A4424}
.pnr{position:absolute;left:409.3mm;top:285mm;font:500 11pt 'Wick Sans';color:#1F1F1F}
'''

def chrome():
    """Erster Browser, der auf diesem Rechner vorhanden ist. None = der von Playwright."""
    for p in ('/opt/pw-browsers/chromium-1243/chrome-linux64/chrome',
              'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe',
              'C:/Program Files/Google/Chrome/Application/chrome.exe',
              '/usr/bin/chromium', '/usr/bin/google-chrome'):
        if pathlib.Path(p).exists(): return p
    return None

def zusammenbauen():
    """Setzt die Broschüre neu zusammen: Original + neue Seite 11 + Kapitel C.

    1–10   Original
    11     neu, Apéro im Gläsli
    36     neu, Weitere Locations
    12–19  Original 11–19 ohne die alte 15 — Apérogebäck steht neu bei den Warmen Häppchen
    20–29  Kapitel C, ersetzt die bisherigen Seiten 20–31
    30–38  Original 32–40 ohne die alte 38 — «Gut zu wissen» ist gestrichen
    """
    import pymupdf
    orig = pymupdf.open(ROOT / 'quellen/broschuere-40s.pdf')
    doc = pymupdf.open()

    def neu(seiten, liste, name):
        """Baut die genannten Seiten und gibt sie als PDF zurück."""
        html_ = ('<!doctype html><html lang="de"><head><meta charset="utf-8"><style>' + CSS
                 + '</style></head><body>' + ''.join(f() for n, f in liste if n in seiten) + '</body></html>')
        (B / 'seiten.html').write_text(html_, encoding='utf-8')
        tmp = ROOT / f'out/_teil-{name}.pdf'
        from playwright.sync_api import sync_playwright
        with sync_playwright() as pw:
            b = pw.chromium.launch(executable_path=chrome()); pg = b.new_page()
            pg.goto((B / 'seiten.html').as_uri()); pg.wait_for_timeout(600); pg.evaluate('document.fonts.ready')
            pg.pdf(path=str(tmp), width='420mm', height='297mm', print_background=True, prefer_css_page_size=True); b.close()
        return pymupdf.open(tmp)

    ersetzt = {n for n, _ in SEITEN}
    teil_s = neu(ersetzt, SEITEN, 's')                      # die überarbeiteten Einzelseiten
    teil_c = neu({n for n, _ in KAPITEL_C}, KAPITEL_C, 'c')  # der neue Essensteil
    idx_s = {n: i for i, (n, _) in enumerate(SEITEN)}   # gleiche Reihenfolge wie in neu()

    def hol(nr):
        """Seite nr der alten Nummerierung — überarbeitet, falls vorhanden."""
        if nr in idx_s: doc.insert_pdf(teil_s, from_page=idx_s[nr], to_page=idx_s[nr])
        else: doc.insert_pdf(orig, from_page=nr - 1, to_page=nr - 1)

    for nr in range(1, 11): hol(nr)                     # 1–10
    doc.insert_pdf(teil_s, from_page=idx_s[0], to_page=idx_s[0])     # neue Seite 11: Gläsli
    for nr in range(11, 20):                            # alt 11–19 → neu 12–19
        if nr != 15: hol(nr)                            # alt 15 ist in die Warmen Häppchen gewandert
    doc.insert_pdf(teil_c, from_page=0, to_page=teil_c.page_count - 1)  # Kapitel C
    for nr in range(32, 41):                            # alt 32–40 → neu 30–38
        if nr == 38: continue                           # «Gut zu wissen» ist gestrichen
        hol(nr)
        if nr == 37:                                    # dahinter die neue Seite «Weitere Locations»
            doc.insert_pdf(teil_s, from_page=idx_s[1], to_page=idx_s[1])

    out = ROOT / 'out/wick-apero-catering-NEU.pdf'
    doc.save(out, garbage=4, deflate=True)
    n = doc.page_count
    doc.close(); teil_s.close(); teil_c.close(); orig.close()
    for t in ('s', 'c'): (ROOT / f'out/_teil-{t}.pdf').unlink(missing_ok=True)
    print(f'» {out.name}: {n} Seiten (vorher 40)')

def main():
    args = sys.argv[1:]
    if '--zusammenbauen' in args: zusammenbauen(); return
    # --vorschau: nur die gewählten Seiten nach out/vorschau.pdf, ohne Einbau in die 40 Seiten
    vorschau = '--vorschau' in args
    if vorschau: args.remove('--vorschau')
    # --kapitel-c: der neue Essensteil nach Konzept C, immer als Vorschau
    kapitelc = '--kapitel-c' in args
    if kapitelc: args.remove('--kapitel-c'); vorschau = True
    liste_ = KAPITEL_C if kapitelc else SEITEN
    nur = [int(a) for a in args] or [n for n, _ in liste_]
    html_ = '<!doctype html><html lang="de"><head><meta charset="utf-8"><style>' + CSS + '</style></head><body>' + ''.join(f() for n, f in liste_ if n in nur) + '</body></html>'
    ziel = (ROOT / 'out/vorschau.pdf') if vorschau else (B / 'seiten.pdf')
    ziel.parent.mkdir(parents=True, exist_ok=True)
    (B / 'seiten.html').write_text(html_, encoding='utf-8')
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=chrome()); pg = b.new_page()
        pg.goto((B / 'seiten.html').as_uri()); pg.wait_for_timeout(600); pg.evaluate('document.fonts.ready')
        pg.pdf(path=str(ziel), width='420mm', height='297mm', print_background=True, prefer_css_page_size=True); b.close()
    if vorschau:
        print(f'» {ziel.name}: Vorschau der Seiten {nur}'); return
    import pymupdf
    neu = pymupdf.open(B / 'seiten.pdf'); doc = pymupdf.open(ROOT / 'quellen/broschuere-40s.pdf')
    for k, n in enumerate([n for n, _ in SEITEN if n in nur]):
        doc.delete_page(n - 1); doc.insert_pdf(neu, from_page=k, to_page=k, start_at=n - 1)
    out = ROOT / 'out/wick-apero-catering-ENTWURF.pdf'; doc.save(out, garbage=4, deflate=True)
    print(f'» {out.name}: {doc.page_count} Seiten, ersetzt: {nur}')
if __name__ == '__main__': main()
