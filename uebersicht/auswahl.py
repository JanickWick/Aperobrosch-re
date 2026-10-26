#!/usr/bin/env python3
"""Gewählte Kandidaten übernehmen:  python3 auswahl.py wahl.json
   wahl.json = {"<slug>": 2, ...}  (Kandidatennummer 1–4, 0 = kein Bild)"""
import json, sys, shutil, pathlib
kand = json.load(open('kand.json')); wahl = json.load(open(sys.argv[1]))
ref = json.load(open('ref.json')) if pathlib.Path('ref.json').exists() else {}
n = 0
for s, i in wahl.items():
    if not i or not kand.get(s) or i > len(kand[s]): ref.pop(s, None); continue
    k = kand[s][i - 1]; ziel = f'ref/{s}.jpg'; shutil.copy(k['datei'], ziel)
    ref[s] = {**k, 'datei': ziel}; n += 1
json.dump(ref, open('ref.json', 'w'), ensure_ascii=False, indent=1); print(n, 'Bilder übernommen')
