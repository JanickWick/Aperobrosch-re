# Broschüre — direkt weiterarbeiten

`python3 broschuere/bauen.py` baut die überarbeiteten Produktseiten (12, 13, 14, 15, 16, 18, 30)
im Design der 40-seitigen Entwurfs-Broschüre (A3 quer) und tauscht sie in `quellen/broschuere-40s.pdf`
aus → `out/wick-apero-catering-ENTWURF.pdf`. Einzelne Seiten: `python3 broschuere/bauen.py 14 30`.

- Inhalte (Sorten, Füllungen, Preise) kommen aus `sortiment/sortiment.json`.
- Bilder: Entwurfsbilder aus `assets/img/kunde/`, echte Fotos aus `sortiment/bilder/kand/` (Website-Broschüre), sonst «Foto folgt».
- Icons: `broschuere/icons/` (aus dem Entwurf ausgeschnitten).
- Kennzeichnung im Arbeitsstand: «PREIS NACH KALKULATION» = neu/geändert, «NOCH OFFEN» = aus der alten Broschüre, noch nicht bestätigt.
- Seite 11 (Traubenbrot, Picknickbrot, Partybrot) ist inhaltlich unverändert und bleibt das Original.
