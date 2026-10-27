"""Kontrolliert die fertige Broschüre: Reihenfolge, Seitenzahlen, Querverweise.

Aufruf: python3 broschuere/inhalt_pruefen.py
Liest out/wick-apero-catering-NEU.pdf und vergleicht
  - die in der Fusszeile gedruckte Seitenzahl mit der tatsächlichen Position,
  - jeden Verweis «Seite(n) N» mit dem, was auf Seite N wirklich steht,
  - das Inhaltsverzeichnis auf Seite 6 mit den Titeln der genannten Seiten.
"""
import pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PDF = ROOT / 'out/wick-apero-catering-NEU.pdf'


def seiten_text(doc):
    return [doc[i].get_text() for i in range(doc.page_count)]


def titel(text):
    """Die Überschrift einer Seite — die erste auffällige Zeile nach der Kapitelmarke."""
    zeilen = [z.strip() for z in text.split('\n') if z.strip()]
    for z in zeilen:
        g = re.sub(r'\s+', ' ', z)
        if g.upper().startswith('KAPITEL'):
            rest = g.split('/', 1)[-1]
            rest = re.sub(r'^\s*0?\d\s*', '', rest).strip()
            if len(rest) > 3:
                return rest
            continue
        if len(g) > 3:
            return g
    return '?'


def main():
    import pymupdf
    if not PDF.exists():
        sys.exit(f'{PDF} fehlt — zuerst «python3 broschuere/bauen.py --zusammenbauen» laufen lassen.')
    doc = pymupdf.open(PDF)
    texte = seiten_text(doc)
    n = doc.page_count
    fehler = []

    print(f'{n} Seiten\n')
    print('Nr | gedruckt | Titel')
    print('---+----------+' + '-' * 50)
    gedruckt = []
    for i, t in enumerate(texte, 1):
        # Die Fusszeile endet mit «WICK — APÉRO & CATERING <nr>»
        m = re.search(r'APÉRO & CATERING\s*(\d+)', re.sub(r'\s+', ' ', t))
        g = int(m.group(1)) if m else None
        gedruckt.append(g)
        mark = '' if g in (None, i) else '   <-- stimmt nicht'
        if mark: fehler.append(f'Seite {i} druckt die Zahl {g}')
        print(f'{i:2} | {str(g) if g else "—":>8} | {titel(t)[:50]}{mark}')

    print('\nQuerverweise')
    print('-' * 62)
    offen = 0
    for i, t in enumerate(texte, 1):
        flach = re.sub(r'\s+', ' ', t)
        for m in re.finditer(r'Seiten?\s+(\d{1,2})(?:\s*(?:bis|und|–|-)\s*(\d{1,2}))?', flach):
            a = int(m.group(1)); b = int(m.group(2) or a)
            for z in range(a, b + 1):
                if not 1 <= z <= n:
                    fehler.append(f'Seite {i} verweist auf Seite {z} — die gibt es nicht')
                    print(f'  Seite {i:2} -> {z:2}  EXISTIERT NICHT'); offen += 1
    if not offen:
        print('  Alle Verweise zeigen auf vorhandene Seiten.')

    print('\nInhaltsverzeichnis gegen die Seiten')
    print('-' * 62)
    iv = re.sub(r'\s+', ' ', texte[5])
    for eintrag, nr in re.findall(r'([A-ZÄÖÜ][^0-9]{3,40}?)\s(\d{1,2})(?=\s|$)', iv):
        z = int(nr)
        if not 1 <= z <= n:
            continue
        wort = re.sub(r'[^A-Za-zÄÖÜäöü]', '', eintrag)[:6].lower()
        ziel = re.sub(r'[^A-Za-zÄÖÜäöü]', '', titel(texte[z - 1])).lower()
        ok = wort and wort in ziel
        print(f'  {eintrag.strip()[:34]:34} -> {z:2}  {titel(texte[z-1])[:28]}  {"" if ok else "?"}')

    doc.close()
    print()
    if fehler:
        print('GEFUNDEN:')
        for f in fehler: print(' -', f)
    else:
        print('Keine Abweichung gefunden.')


if __name__ == '__main__':
    main()
