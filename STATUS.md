# Stand der Broschüre

Letzte Aktualisierung: 27.10.2026
Projektordner: `Aperobroschuere-GitHub`

Die Broschüre hat 40 Seiten, A3 quer. Grundlage ist `quellen/broschuere-40s.pdf`.
`broschuere/bauen.py` ersetzt einzelne Seiten darin durch neu gesetzte Fassungen.

---

## 1 · Seiten: was fertig ist, was offen

| Seite | Thema | Stand | Bemerkung |
|---|---|---|---|
| 1–5, 7 | Umschlag bis «Was planen Sie?» | unverändert | |
| 6 | Ihr Weg (Inhaltsverzeichnis) | **neu gebaut** | neue Gliederung, Legende |
| 8, 9, 10 | Cateringform · Mengen · Pakete | **neu gebaut** | Verweise nachgeführt |
| **11** | **Apéro im Gläsli** | **neu** | neue Seite, Themenbild |
| 12 | Brot & Brötli *(alt 11)* | **neu gebaut** | Inhalt gleich, echte Fotos |
| 13 | Brötli gefüllt *(alt 12)* | **überarbeitet** | Themenbild, Preise wie im Original |
| 14 | Brot XXL *(alt 13)* | **überarbeitet** | echte Fotos, Zopfherz neu |
| 15 | Belegtes, Canapés & Fingerfood *(alt 14)* | **überarbeitet** | echte Fotos |
| 16 | Spiessli *(alt 16)* | **überarbeitet** | fünf Sorten, Antipasti zurück |
| 17 | Warme Häppchen *(alt 15 und 17)* | **neu gebaut** | Apérogebäck eingegliedert, sechs Karten |
| 18 | Platten & Sharing *(alt 18)* | **überarbeitet** | vier Platten, schwarz |
| 19 | Unterwegs · Lunchbags *(alt 19)* | **neu gebaut** | echte Fotos, Inhalt gleich |
| **20–29** | **Warme Küche bis Süsser Abschluss** | **Neukonzeption** | siehe `KONZEPT-essen-20-31.md` |
| 30 | Torten & Confiserie *(alt 32)* | **neu gebaut** | Hochzeitstorte, Gastgeschenke |
| 31 | Für alle — vegetarisch & vegan *(alt 33)* | **neu gebaut** | Zigerbrüüt-Röllchen gestrichen |
| 32–34 | Anlass komplett, Getränke, Material *(alt 34–36)* | unverändert | |
| 35 | Eventraum *(alt 37)* | **neu gebaut** | 80 Plätze, mit Zelt bis 400 |
| **36** | **Weitere Locations** | **neu** | Entra, Eventhouse, Radio Zürisee Loft |
| 37–38 | Anfrage und Rückseite *(alt 39–40)* | unverändert | |
| ~~Gut zu wissen~~ | *(alt 38)* | **gestrichen** | |

**Stand:** Alle Seiten ab 6 sind nachgebaut. `broschuere/inhalt_pruefen.py`
meldet keine Abweichung mehr — jede gedruckte Seitenzahl stimmt mit der Position
überein. Unverändert aus dem Original kommen nur noch die Seiten 1 bis 5
(Umschlag bis «Ein Haus, viele Handwerke»); dort stimmen die Nummern ohnehin.

**Arbeitsstand-Markierungen in den überarbeiteten Seiten**
«Preis nach Kalkulation» = neue oder geänderte Position, Preis folgt.
«Noch offen» = Produkt aus der bisherigen Broschüre, noch nicht bestätigt.

---

## 2 · Seiten, die Bilder brauchen

### Erledigt

Die Seiten 12 bis 19 sind vollständig bebildert — mit echten Wick-Produktfotos im
Broschüren-Look. Neu erzeugt wurden nur sechs Bilder: das Knöpfli-Themenbild und
die fünf Platten auf schwarzem Grund. Siehe `CHANGELOG.md`.

### Nach der Konzeptentscheidung (Seiten 20–31)

Für den ganzen Essens-Teil existiert **kein einziges echtes Wick-Foto**. Betroffen sind:

| Thema | Seite heute | Bildbedarf |
|---|---|---|
| Suppen | 21 | Suppe in Tasse und im Gläsli |
| Vorspeisen am Teller | 21 | 2–3 angerichtete Teller, kalt und warm |
| Salate am Teller | 22 | 2–3 angerichtete Salatteller |
| Salatbuffet | 22 | Buffetlinie mit mehreren Salatschüsseln |
| Buffets | 23 | 1 Buffetaufbau, möglichst an einem echten Anlass |
| Klassiker | 24 | Gericht im Wärmebehälter und/oder am Teller |
| Eigenes Menü | 25–28 | 1 fertig angerichteter Teller als Beispiel |
| Grillplausch | 29 | Grillplatte roh mariniert, Grill im Einsatz |
| Dessert am Teller | 31 | 2–3 angerichtete Dessertteller |

---

## 3 · Vorhandene Bilder und wo sie liegen

### Im Repo

| Ordner | Inhalt |
|---|---|
| `assets/img/kunde/` | Entwurfsbilder aus der 40-Seiten-Broschüre |
| `sortiment/bilder/kand/` | Kandidaten aus der Website-Broschüre |
| `sortiment/bilder/produkte/` | zugeordnete Produktfotos |
| `broschuere/icons/` | Icons, aus dem Entwurf ausgeschnitten |

### Bildarchiv `OneDrive\Pictures\Claude bilder`

| Ordner | Anzahl | Was drin ist | Brauchbar für |
|---|---|---|---|
| `Onlineshop` | 240 | Produktfotos auf Weiss (Canapés, Brötli, Confiserie, Torten) + Osterfiguren | Apéro-Teil, Konditorei |
| `Apero` + Unterordner | 45 + 60 | Katalogfotos mit eingebranntem Wick-Logo | Apéro-Teil (Logo muss weg) |
| `Bilder für Website` | 36 | Backstube, Torten, Hochzeitstorten, Säntisblick, **eine Reihe angerichteter Dessertteller** | Kapitel 05, Dessert am Teller |
| `Cakes und Stücksachen` | 11 | Stücksachen | Süsser Abschluss |
| `Schoggispezialitäten` | 11 | Confiserie | Kapitel Torten & Confiserie |
| `Weihnachten 2026` | 9 | Saisonales | — |

**Wichtigster Befund:** Im ganzen Archiv gibt es **keine Fotos von warmen Gerichten,
Suppen, Salaten, Buffets oder vom Grill**. Der Essens-Teil muss komplett neu bebildert
werden – und dafür brauche ich Referenzfotos von euch.

### Bereits von mir aufbereitet und eingesetzt

Die echten Wick-Fotos im Broschüren-Look liegen jetzt in `bilder/final/`, benannt
nach der **alten** Seitenzahl (`seite-14_brot-am-stueck.jpg` usw.). Sie decken die
Seiten 12 bis 19 der neuen Zählung ab. Was dort noch fehlt:

- **Zopfherz gefüllt** hat kein eigenes Bild
- der ganze Essensteil der Seiten 20 bis 29 hat weiterhin kein echtes Wick-Foto;
  die Themenbilder entstehen aus euren Zutaten- und Buffetfotos

Noch nicht eingesetzt, weil die Produkte nicht in der Broschüre stehen: Zwirbelwick-
Crostino, Hummus auf Vollkorn, Rindstatar-Tartelette, Biräbrot mit Alpkäse,
Zigerbrüüt-Röllchen, Apéro-Schnecke, Blätterteig-Stängeli Sbrinz.

## 4 · Offene Punkte

### Preise und Angaben
- [FEHLT: Preis] Knöpfli gefüllt (bisher 2.50 / 2.80)
- [FEHLT: Preis] Zopfherz gefüllt
- [FEHLT: Preis] Apérowrap klein (bisher 2.70 / 2.90)
- [FEHLT: Preis] Frischkäse-Pralinen (bisher 2.50 mit Salzstängeli)
- [FEHLT: Preis] Spiessli Käse-Trauben und Melonen-Rohschinken
- [FEHLT: Preis] Tray of Snacks
- [FEHLT] Neue Plattengrössen klein / mittel / gross — bis dahin gelten 2, 4, 6, 8 Personen
- [ERLEDIGT] Platten zeigen neu schwarze Platten statt Palmblatt
- [FEHLT] In welchen Monaten gibt es Melonen-Rohschinken?

### Entscheide
- «Bleibt oder weg?» auf den überarbeiteten Seiten: Belegte Brötli rund,
  Bäckerpastetli, Brötchen Zwirbelwick Rustico, Erdbeer-Nutella-Spiessli,
  Dessert im Gläsli, Vegane Dessertvariationen
- Vegane Alternative zum gestrichenen Couscous-Wrap
- Apéro im Gläsli: ob und auf welcher Seite
- Konzept für die Seiten 20–31

### Datenlage
- **Küche** ist erfasst: 11 Gruppen, 141 Preiszeilen. **Confiserie** ist weiterhin leer
  (betrifft Seite 32, dort steht ohnehin «nach Offerte»).

### Technik
- `broschuere/pruefen.py` misst alle Seiten und meldet Text, der aus seiner Karte
  oder aus der Seite herausragt. Vor jedem Zusammenbau laufen lassen.
- `broschuere/bauen.py` braucht Python; auf diesem Rechner ist es nicht installiert.
- Das Skript erwartet den Chromium-Pfad der Cloud-Umgebung
  (`/opt/pw-browsers/...`). Für den lokalen Bau muss der Pfad auf den
  installierten Chrome zeigen.

---

## 5 · Erledigt / Offen / Brauche von dir

**Erledigt**
- Bestandsaufnahme Seiten, Bilder, Sortimentsdaten
- Ordner `referenzen/` und `bilder/` angelegt
- `PRODUKTE.md`, `CHANGELOG.md`, `KONZEPT-essen-20-31.md` angelegt
- Seite 16 fertig bebildert, «Saisonal» gestrichen
- Lokaler Bau läuft: Python 3.12 installiert, Encoding und Browserpfad korrigiert,
  fehlende Icons wiederhergestellt

**Gläsli-Apéros — offen**
- [FEHLT: Preis pro Gläsli — ein Preis für alle oder je Kategorie?]
- [FEHLT: Glasgrösse und Portion]
- Neue Mengenlogik bestätigen: 6 Häppchen (davon 2 süss) + 1 Gläsli pro Person
- Danach Seiten 8, 9 und 10 nachführen — dort steht weiterhin «8 Häppchen pro Person»
- Querverweis auf der Apéro-Riche-Karte: «Ergänzen Sie Ihren Apéro Riche mit Gläsli — Seite 11»
- Inhaltsverzeichnis Seite 6 und alle Seitenzahlen ab 11 nachführen

**Offen**
- Umsetzung Konzept **C** für die Seiten 20–31 (entschieden, Zeilen dürfen zusammenrücken)

**Brauche von dir**
- Referenzfotos für den Essensteil, siehe `referenzen/_ANFRAGEN.md` —
  am dringendsten **E5, E6, E7, E10** beim nächsten Catering
- Nichts Dringendes ausser den Fotos — die Küchendaten habe ich aus der bestehenden
  Broschüre übernommen
