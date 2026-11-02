"""Baut das Dokument zum Eventraum «Säntisblick» — A4 hoch, vier Seiten.

Aufruf: python3 saentisblick/bauen.py
Ergebnis: out/wick-saentisblick.pdf

Alle Angaben stammen aus der Website (content/eventraum.ts, Stand 21.09.2026)
und aus der Apéro-Broschüre. Was dort nicht steht, steht auch hier nicht.
"""
import html, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
B = ROOT / 'saentisblick'
FOTO = '../assets/img/saentisblick'
e = html.escape

# ---------- Angaben ----------
PLAETZE = '80'
ZELT = '400'
ADRESSE = 'Alte Jonastrasse 77 · 8640 Rapperswil-Jona'
TELEFON = '055 210 15 44'
MAIL = 'info@baeckerei-wick.ch'
WEB = 'baeckerei-wick.ch'

INTRO = ('Heimelig, vielfältig und für jeden Anlass buchbar. Ob Sitzung, Geschäftsessen, Geburtstagsfeier, '
         'Brunch oder Apéro — wir bringen alles unter einen Hut. Raum, Catering und Betreuung aus einer Hand.')

ECKDATEN = ((PLAETZE, 'Sitzplätze im Raum'), (ZELT, 'Personen mit Zeltaufbau'),
            ('450.–', 'Raummiete in Franken'), ('2000.–', 'Konsumation, dann entfällt die Miete'))

NUTZUNG = ('Sitzungen', 'Geschäftsessen', 'Geburtstagsfeiern', 'Brunch', 'Apéro', 'Trauerfeiern')
AUSSTATTUNG = ('Kühlschrank', 'Musikanlage', 'Rattan-Lounge', 'WC-Anlage', 'WiFi', 'TV 86 Zoll Ultra HD')

ZUSATZ = (('TV, 86 Zoll Ultra HD', '', '100.–'),
          ('Zusätzlicher Kühlschrank', 'pro Stück', '30.–'),
          ('Tischgarnitur oder Stehtisch inkl. Tischtuch', 'pro Stück', '30.–'),
          ('Kaffee', 'pro Portion', '3.–'),
          ('Personal vor Ort', 'pro Person und Stunde', '60.–'),
          ('Getränkeservice', '', 'nach effektivem Verbrauch'),
          ('Catering oder Brunch', '', 'nach individueller Offerte'),
          ('Mietgeschirr', '', 'nach individueller Offerte'),
          ('Zeltaufbau vor dem Raum', '', 'nach individueller Offerte'))

BEDINGUNGEN = (('Raummiete', 'CHF 450.– pauschal. Rückgabe am Folgetag bis Mittag.'),
               ('Ab CHF 2000.–', 'Bei einer Konsumation ab CHF 2000.– entfällt die Raummiete.'),
               ('Rückgabe', 'Besenrein. Allfällige Reinigung CHF 200.–.'),
               ('Getränke', 'Werden nach effektivem Verbrauch abgerechnet. Geschlossenes kommt retour.'))

CATERING = (('APÉRO', 'Häppchen aus der eigenen Backstube und Küche — vom kleinen Apéro bis zum Apéro Riche, '
                      'der eine Mahlzeit ersetzt.'),
            ('BRUNCH', 'Zopf, Brötli, Confiserie und Warmes aus dem eigenen Haus.'),
            ('BUFFET ODER MENÜ', 'Vom einfachen Buffet bis zum mehrgängigen Menü, am Tisch serviert oder '
                                 'zum Selbstschöpfen.'),
            ('SÜSSER ABSCHLUSS', 'Mini-Pâtisserie, Desserts im Glas und Torten nach Ihrer Idee.'))

SCHRITTE = (('01', 'ANFRAGEN', 'Anrufen oder schreiben — mit Datum, Anlassart und ungefährer Personenzahl.'),
            ('02', 'BESPRECHEN', 'Wir melden uns und gehen Raum, Essen und Material durch — unverbindlich.'),
            ('03', 'OFFERTE', 'Sie erhalten ein Angebot für Raum und Catering auf einem Blatt.'),
            ('04', 'IHR ANLASS', 'Wir richten ein, bewirten und räumen ab. Sie sind Gast am eigenen Fest.'))


# ---------- Bausteine ----------
def seite(inner, nr):
    return (f'<section class="seite">{inner}'
            f'<div class="marke">WICK — EVENTRAUM «SÄNTISBLICK»</div><div class="pnr">{nr}</div></section>')


def kopf(titel, sub):
    return (f'<div class="kap">WICKS EVENTRAUM</div><h1 class="titel">{e(titel)}</h1>'
            f'<p class="sub">{e(sub)}</p><div class="rule"></div>')


def sph(t, top=None):
    stil = f' style="position:absolute;left:16mm;top:{top}mm;width:178mm"' if top else ''
    return f'<div class="sph"{stil}>{e(t)}</div>'


def tags(xs):
    return '<div class="tagliste">' + ''.join(f'<span>{e(x)}</span>' for x in xs) + '</div>'


def bild(datei, stil=''):
    return f'<div class="bild" style="{stil}"><img src="{FOTO}/{datei}"></div>'


# ---------- Seiten ----------
def s1():
    h = (f'<div class="titelbild"><img src="{FOTO}/titel.jpg"><div class="ov"></div></div>'
         f'<div class="kap hell">WICKS EVENTRAUM</div>'
         f'<div class="box">SÄNTIS-<br>BLICK</div>'
         f'<p class="titelintro">{e(INTRO)}</p>')
    h += ('<div class="eckband">' + ''.join(
        f'<div><b>{e(g)}</b><span>{e(k)}</span></div>' for g, k in ECKDATEN) + '</div>')
    h += (f'<p class="titelfuss">{e(ADRESSE)}<br>{e(TELEFON)} · {e(MAIL)} · {e(WEB)}</p>')
    return seite(h, 1)


def s2():
    h = kopf('DER RAUM', 'Holz, Wandbilder und Alphütten-Stimmung mitten in Rapperswil-Jona — Platz für '
                         f'{PLAETZE} Gäste an Tischen. Mit Zeltaufbau davor wächst der Anlass auf bis zu '
                         f'{ZELT} Personen.')
    h += (f'<div class="halb"><div>{sph("Wofür der Raum passt")}{tags(NUTZUNG)}</div>'
          f'<div>{sph("Ausstattung")}{tags(AUSSTATTUNG)}</div></div>')
    h += ('<div class="raster">' + bild('raum-1.jpg', 'grid-column:span 2;aspect-ratio:2/1')
          + bild('raum-2.jpg') + bild('raum-3.jpg') + bild('raum-4.jpg') + bild('raum-5.jpg')
          + bild('raum-6.jpg', 'grid-column:span 3;aspect-ratio:4/1') + '</div>')
    h += ('<p class="fuss">Die Bilder zeigen den Raum an verschiedenen Anlässen. '
          'Bestuhlung und Tischstellung richten wir nach Ihrem Anlass ein.</p>')
    return seite(h, 2)


def s3():
    h = kopf('PREISE', 'Klar und ohne Überraschungen. Was Sie nicht brauchen, verrechnen wir nicht.')
    h += ('<div class="rostkarte"><div class="rk1"><span class="rkl">RAUMMIETE</span>'
          '<span class="rkp">CHF 450.–</span><p>Rückgabe am Folgetag bis Mittag.</p></div>'
          '<div class="rk2"><p><b>Ab einer Konsumation von CHF 2000.– entfällt die Raummiete.</b> '
          'Gezählt wird alles, was an Essen und Getränken über uns läuft.</p></div></div>')
    h += sph('Was Sie dazunehmen können', 104)
    h += ('<div class="preisliste">' + ''.join(
        f'<div class="pz"><span class="n">{e(n)}</span><span class="u">{e(u)}</span>'
        f'<span class="v">{e(v if v.startswith("nach") else "CHF " + v)}</span></div>'
        for n, u, v in ZUSATZ) + '</div>')
    h += sph('Gut zu wissen', 202)
    h += ('<div class="bedingungen">' + ''.join(
        f'<div><b>{e(t)}</b><p>{e(x)}</p></div>' for t, x in BEDINGUNGEN) + '</div>')
    h += ('<p class="fuss">Alle Preise in Schweizer Franken. '
          'Catering, Brunch, Mietgeschirr und Zeltaufbau offerieren wir individuell.</p>')
    return seite(h, 3)


def s4():
    h = kopf('CATERING & ANFRAGE', 'Essen kommt aus dem eigenen Haus — Backstube, Konditorei, Confiserie '
                                   'und Küche unter einem Dach.')
    h += ('<div class="catering">' + ''.join(
        f'<div><h3>{e(t)}</h3><p>{e(x)}</p></div>' for t, x in CATERING) + '</div>')
    h += ('<p class="hinweis">Das vollständige Catering-Angebot steht in unserer Apéro- und Catering-Broschüre. '
          'Wir schicken sie Ihnen gerne zu.</p>')
    h += sph('So kommen wir zusammen', 158)
    h += ('<div class="schritte">' + ''.join(
        f'<div><span class="nr">{nr}</span><h3>{e(t)}</h3><p>{e(x)}</p></div>'
        for nr, t, x in SCHRITTE) + '</div>')
    h += (f'<div class="kontakt"><div class="kl">SPRECHEN WIR DARÜBER</div>'
          f'<p class="kt">{e(TELEFON)}</p><p class="km">{e(MAIL)}</p>'
          f'<p class="ka">{e(ADRESSE)}<br>{e(WEB)}</p>'
          f'<p class="kh">Beratung und Offerte sind kostenlos und unverbindlich.</p></div>')
    return seite(h, 4)


CSS = r'''
@font-face{font-family:'Wick Sans';src:url(../assets/fonts/QGYsz_wNahGAdqQ43Rh_cqDpp_k.woff2) format('woff2');font-weight:100 900;unicode-range:U+0100-02AF,U+1E00-1EFF,U+20A0-20AB,U+20AD-20CF}
@font-face{font-family:'Wick Sans';src:url(../assets/fonts/QGYsz_wNahGAdqQ43Rh_fKDp.woff2) format('woff2');font-weight:100 900}
@font-face{font-family:'Wick Slab';src:url(../assets/fonts/rax8HiqOu8IVPmn7cYxpPDk.woff2) format('woff2');font-weight:100 900;unicode-range:U+0100-02AF,U+1E00-1EFF,U+20A0-20AB,U+20AD-20CF}
@font-face{font-family:'Wick Slab';src:url(../assets/fonts/rax8HiqOu8IVPmn7f4xp.woff2) format('woff2');font-weight:100 900}
@page{size:210mm 297mm;margin:0}
*{box-sizing:border-box;margin:0;padding:0}
body{background:#888}
.seite{width:210mm;height:297mm;position:relative;overflow:hidden;background:#F6F2EA;
  font-family:'Wick Slab',serif;color:#1F1F1F;page-break-after:always;-webkit-print-color-adjust:exact}
.marke{position:absolute;left:16mm;bottom:9mm;font:500 6.6pt 'Wick Sans';letter-spacing:.16em;color:#7A4424}
.pnr{position:absolute;right:16mm;bottom:8.6mm;font:500 9pt 'Wick Sans';color:#1F1F1F}

/* Titelseite */
.titelbild{position:absolute;left:0;top:0;width:210mm;height:206mm;overflow:hidden}
.titelbild img{width:100%;height:100%;object-fit:cover;display:block}
.titelbild .ov{position:absolute;inset:0;
  background:linear-gradient(180deg,rgba(18,17,16,.62) 0%,rgba(18,17,16,.16) 34%,rgba(18,17,16,.1) 56%,rgba(18,17,16,.86) 100%)}
.kap{position:absolute;left:16mm;top:16mm;font:600 7.4pt 'Wick Sans';letter-spacing:.24em;color:#7A4424;z-index:3}
.kap.hell{color:#F2E4D4}
.box{position:absolute;left:16mm;top:28mm;width:72mm;height:52mm;background:#fff;z-index:3;
  display:flex;align-items:center;justify-content:center;text-align:center;
  font:500 17pt 'Wick Sans';letter-spacing:.1em;line-height:8mm;color:#1F1F1F}
.titelintro{position:absolute;left:16mm;top:164mm;width:150mm;z-index:3;
  font-size:11pt;line-height:5.4mm;color:#fff}
.eckband{position:absolute;left:0;top:206mm;width:210mm;background:#7A4424;
  display:grid;grid-template-columns:repeat(4,1fr);gap:6mm;padding:9mm 16mm}
.eckband b{display:block;font:500 17pt 'Wick Sans';line-height:1;color:#fff}
.eckband span{display:block;margin-top:2.4mm;font-size:7.6pt;line-height:3.5mm;color:#F2E4D4}
.titelfuss{position:absolute;left:16mm;top:250mm;width:178mm;font-size:9.5pt;line-height:4.8mm;color:#2A2521}

/* Kopf der Innenseiten */
.titel{position:absolute;left:16mm;top:24mm;font:600 15pt 'Wick Sans';letter-spacing:.1em;color:#1F1F1F}
.sub{position:absolute;left:16mm;top:34mm;width:178mm;font-size:10.5pt;line-height:5mm;color:#2A2521}
.rule{position:absolute;left:16mm;top:52mm;width:178mm;height:.3mm;background:#E6DBCB}
.sph{font:600 7.4pt 'Wick Sans';letter-spacing:.18em;color:#7A4424;
  border-bottom:.2mm solid #E6DBCB;padding-bottom:1.8mm;margin-bottom:4mm}

.halb{position:absolute;left:16mm;top:60mm;width:178mm;display:grid;grid-template-columns:1fr 1fr;gap:10mm}
.tagliste{display:flex;flex-wrap:wrap;gap:2mm}
.tagliste span{border:.25mm solid #CFC3B0;padding:1.6mm 3mm 1.2mm;font-size:8.6pt;line-height:1.2;color:#2A2521}
.raster{position:absolute;left:16mm;top:98mm;width:178mm;display:grid;grid-template-columns:repeat(3,1fr);gap:2mm}
.bild{overflow:hidden;background:#E6DBCB;aspect-ratio:1/1}
.bild img{width:100%;height:100%;object-fit:cover;display:block}
.fuss{position:absolute;left:16mm;bottom:20mm;width:178mm;font-size:8pt;line-height:3.8mm;color:#5A5048}

/* Preise */
.rostkarte{position:absolute;left:16mm;top:60mm;width:178mm;background:#7A4424;color:#fff;
  display:grid;grid-template-columns:.8fr 1.2fr;gap:10mm;padding:9mm 10mm}
.rkl{display:block;font:600 7.4pt 'Wick Sans';letter-spacing:.18em;color:#F2E4D4}
.rkp{display:block;margin-top:3mm;font:500 24pt 'Wick Sans';line-height:1;color:#fff}
.rostkarte p{margin-top:3mm;font-size:9.5pt;line-height:4.6mm;color:#F4E6D8}
.rostkarte .rk2 p{margin-top:0}
.preisliste{position:absolute;left:16mm;top:112mm;width:178mm}
.pz{display:flex;align-items:baseline;gap:4mm;border-bottom:.2mm solid #E6DBCB;padding:2.4mm 0}
.pz .n{flex:1 1 auto;font-size:10pt}
.pz .u{font-size:7.6pt;color:#5A5048;white-space:nowrap}
.pz .v{font:500 10pt 'Wick Sans';white-space:nowrap;min-width:34mm;text-align:right}
.bedingungen{position:absolute;left:16mm;top:210mm;width:178mm;display:grid;grid-template-columns:1fr 1fr;gap:6mm 10mm}
.bedingungen b{display:block;font:600 7.4pt 'Wick Sans';letter-spacing:.14em;color:#7A4424;margin-bottom:1.6mm}
.bedingungen p{font-size:9.5pt;line-height:4.4mm;color:#2A2521}

/* Catering & Anfrage */
.catering{position:absolute;left:16mm;top:60mm;width:178mm;display:grid;grid-template-columns:1fr 1fr;gap:5mm}
.catering>div{background:#1F1F1F;color:#fff;padding:7mm 7mm 8mm}
.catering h3{font:500 9.4pt 'Wick Sans';letter-spacing:.14em;color:#fff}
.catering p{margin-top:2.6mm;font-size:9.2pt;line-height:4.4mm;color:#D6CCBE}
.hinweis{position:absolute;left:16mm;top:142mm;width:178mm;font-size:9.5pt;line-height:4.6mm;color:#2A2521}
.schritte{position:absolute;left:16mm;top:166mm;width:178mm;display:grid;grid-template-columns:repeat(4,1fr);gap:5mm}
.schritte .nr{font:500 15pt 'Wick Sans';line-height:1;color:#7A4424}
.schritte h3{margin-top:3mm;font:500 8pt 'Wick Sans';letter-spacing:.14em;color:#1F1F1F}
.schritte p{margin-top:2mm;font-size:8.4pt;line-height:4mm;color:#2A2521}
.kontakt{position:absolute;left:16mm;top:212mm;width:178mm;background:#1F1F1F;color:#fff;padding:9mm 10mm 10mm}
.kl{font:600 7.4pt 'Wick Sans';letter-spacing:.18em;color:#E6DCCB}
.kt{margin-top:4mm;font:500 20pt 'Wick Sans';line-height:1;color:#fff}
.km{margin-top:2.6mm;font-size:11pt;color:#fff}
.ka{margin-top:4mm;font-size:9.4pt;line-height:4.4mm;color:#C9BCA8}
.kh{margin-top:4mm;font-size:8.6pt;color:#C9BCA8}
'''


def chrome():
    for p in ('/opt/pw-browsers/chromium-1243/chrome-linux64/chrome',
              'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe',
              'C:/Program Files/Google/Chrome/Application/chrome.exe',
              '/usr/bin/chromium', '/usr/bin/google-chrome'):
        if pathlib.Path(p).exists(): return p
    return None


def main():
    html_ = ('<!doctype html><html lang="de"><head><meta charset="utf-8"><style>' + CSS
             + '</style></head><body>' + s1() + s2() + s3() + s4() + '</body></html>')
    (B / 'seiten.html').write_text(html_, encoding='utf-8')
    ziel = ROOT / 'out/wick-saentisblick.pdf'
    ziel.parent.mkdir(parents=True, exist_ok=True)
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=chrome()); pg = b.new_page()
        pg.goto((B / 'seiten.html').as_uri()); pg.wait_for_timeout(600); pg.evaluate('document.fonts.ready')
        pg.pdf(path=str(ziel), width='210mm', height='297mm', print_background=True, prefer_css_page_size=True)
        b.close()
    print(f'» {ziel.name}: 4 Seiten')


if __name__ == '__main__':
    main()
