#!/usr/bin/env python3
"""Pro Produkt bis zu 4 Bildkandidaten von Openverse laden (Thumbnails, CC-lizenziert)."""
import json, re, unicodedata, time, urllib.request, urllib.parse, pathlib, sys
UA = 'WickSortiment/1.0 (janickwick8640@hotmail.com)'
STOP = {'with', 'and', 'the', 'for', 'in', 'on', 'of', 'mini', 'party', 'platter', 'appetizer', 'assorted', 'dessert', 'catering', 'plated', 'fresh', 'sliced'}
def slug(s):
    s = unicodedata.normalize('NFKD', s); s = ''.join(c for c in s if not unicodedata.combining(c))
    return re.sub(r'[^a-z0-9]+', '-', s.lower().replace('ß', 'ss')).strip('-')[:60]
def get(url, timeout=40):
    return urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': UA}), timeout=timeout).read()
prod = json.load(open('sortiment.json'))
kand = json.load(open('kand.json')) if pathlib.Path('kand.json').exists() else {}
for p in prod:
    s = slug(p['name'])
    if kand.get(s): continue
    woerter = [w for w in p['such'].lower().split() if w not in STOP]
    # Openverse verknüpft Suchwörter mit UND — lange Anfragen liefern nichts.
    # Darum stufenweise kürzen: ganze Anfrage, dann drei, zwei, ein Wort.
    data = None; teile = p['such'].split()
    for n in (len(teile), 3, 2, 1):
        q = ' '.join(teile[:n])
        url = f"https://api.openverse.org/v1/images/?q={urllib.parse.quote(q)}&license_type=commercial&page_size=20&mature=false"
        for versuch in range(4):
            try: data = json.loads(get(url)); break
            except Exception as e:
                time.sleep(25 * (versuch + 1) if '429' in str(e) else 3)
        if data and data.get('result_count', 0) >= 3: break
        time.sleep(0.6)
    if not data or not data.get('results'): print('  ✗ Suche', p['name'], flush=True); kand[s] = []; continue
    def passt(r):
        txt = (r.get('title') or '').lower() + ' ' + ' '.join(t.get('name', '') for t in (r.get('tags') or [])).lower()
        return sum(w in txt for w in woerter)
    res = [r for r in data.get('results', []) if (r.get('width') or 0) >= 400]
    res.sort(key=lambda r: (-passt(r), -min(r['width'], 2000)))
    liste = []
    for r in res[:8]:
        if len(liste) >= 3: break
        # Originalbild vom Fremdhost zuerst (zählt nicht gegen das Openverse-Limit),
        # das Openverse-Thumbnail nur als Ausweg.
        raw = b''
        for u in (r.get('url'), r.get('thumbnail')):
            try:
                raw = get(u, 60)
                if len(raw) >= 8000: break
            except Exception: raw = b''
        try:
            if len(raw) < 8000: continue
            f = f"ref/kand/{s}-{len(liste)+1}.jpg"; pathlib.Path(f).write_bytes(raw)
            liste.append({'datei': f, 'titel': r.get('title'), 'urheber': r.get('creator'), 'lizenz': (r.get('license') or '') + ' ' + (r.get('license_version') or ''),
                          'quelle': r.get('foreign_landing_url') or r.get('url'), 'treffer': passt(r)})
        except Exception: continue
    kand[s] = liste
    json.dump(kand, open('kand.json', 'w'), ensure_ascii=False, indent=1)
    print(f"  {len(liste)} Kandidaten  {p['name']}", flush=True)
    time.sleep(1.0)
print('fertig:', sum(1 for v in kand.values() if v), 'Produkte mit Kandidaten')
