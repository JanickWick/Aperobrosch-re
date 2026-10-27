# Änderungsprotokoll

Jede Änderung mit Datum, Seite, was geändert wurde und warum.
Neueste Einträge oben.

---

## 2026-10-27 · Reihenfolge korrigiert, neue Inhaltsprüfung

### Fehler
Die Seite «Weitere Locations» stand plötzlich auf Seite 1 und der Umschlag war
weg. Grund: die neue Seite trug den Schlüssel `1` — und `1` ist in `SEITEN` auch
die alte Seite 1, also hat sie den Umschlag ersetzt. Neue Seiten bekommen jetzt
Zahlen, die als alte Seitenzahl nicht vorkommen: `0` für die Gläsli-Seite,
`-1` für die Locations.

### Neu: `broschuere/inhalt_pruefen.py`
Liest die fertige PDF und kontrolliert
- die in der Fusszeile gedruckte Zahl gegen die tatsächliche Position,
- jeden Verweis «Seite N» gegen den Umfang der Broschüre,
- das Inhaltsverzeichnis gegen die Titel der genannten Seiten.

### Stand der Kontrolle
Reihenfolge, Inhaltsverzeichnis und Querverweise stimmen.
**Vier Seiten drucken noch ihre alte Nummer**, weil sie unverändert aus dem
Original kommen:

| steht auf | druckt | Seite |
|---|---|---|
| 32 | 34 | Ihr Anlass komplett |
| 33 | 35 | Getränke |
| 34 | 36 | Material, Personal & Service |
| 37 | 39 | Anfrage |

---

## 2026-10-27 · Seite «Gut zu wissen» gestrichen

Die Seite ist raus. Die Broschüre hat damit wieder **38 Seiten**:
Eventraum 35, Weitere Locations 36, Anfrage 37, Rückseite 38.
Inhaltsverzeichnis und Querverweise sind nachgeführt.

**Was mit der Seite verschwunden ist** — bitte prüfen, ob etwas davon an einer
anderen Stelle stehen muss:

- Beratung: «Sind Fragen offen? Wir beraten.»
- Mindestbestellmenge: steht weiterhin in den Fusszeilen der Produktseiten
- Getränke: werden nach Verbrauch abgerechnet
- Personal: CHF 60.00 pro Person und Stunde — steht auch auf der Eventraum-Seite
- Mietmaterial: Geschirr, Gläser, Besteck
- Kontakt: Telefon und Adresse stehen auf der Anfrage-Seite und auf der Rückseite

---

## 2026-10-27 · Die vier offenen Bilder nachgeholt

fal.ai ist wieder gedeckt — die vier Bilder, die seit gestern offen waren, sind da:

- **Seite 14 · Brot XXL:** Themenbild neu das gefüllte Laugenherz auf der
  schwarzen Platte, nach eurem Referenzfoto.
- **Seite 17 · Chili Würstli im Briochesmantel:** neues Kartenbild nach eurem
  neuen Foto — der gedrehte Briocheteig und die sichtbaren Enden stimmen jetzt.
- **Seite 22 · Klassiker für grosse Runden:** die Seite ist wieder eine
  Hero-Seite. Das Themenbild zeigt die Ausgabe für grosse Runden — vier offene
  Wärmebehälter in einer Reihe, Tellerstapel und Besteck am Ende.
- **Seite 36 · Weitere Locations:** Themenbild aus eurem Entra-Foto, neu ohne
  Leinwand und ohne Getränkekarte. Die drei Location-Karten stehen jetzt unter
  dem Bild und haben ihren Rand zurück.

---

## 2026-10-27 · Seite 20 «Drei Wege» neu gestaltet

Die Vergleichstabelle ist weg. Jeder Weg hat jetzt eine eigene Karte über die
ganze Seitenhöhe: grosse Nummer in Rost, ein Symbol im weissen Kreis, Titel und
Untertitel, die Wenn-Zeile, dann ein Raster mit Ab / Sie wählen / Abgerechnet
und zuunterst das rostfarbene Preisband mit der Spanne.

### Noch offen
Euer neues Chili-Würstli-Foto liegt unter `referenzen/produkte/chili-wuerstli.webp`.
Es konnte **nicht** durch nano banana — fal.ai hat kein Guthaben
(*«User is locked. Reason: Exhausted balance.»*). Auf der Karte steht weiterhin
das bisherige Bild.

---

## 2026-10-27 · Schokokuchen statt Cremeschnitte, Gläsli bei «Für alle»

### Seite 28 · Vegane Dessertvariationen
Statt der Cremeschnitte steht dort jetzt der **Schokokuchen von der Website**.
Das Foto ist nicht durch nano banana gelaufen — ich habe es nur abgedunkelt und
mit einer weichen Vignette versehen, damit es zu den übrigen fünf Karten der
Seite passt. Produkt und Bildinhalt sind unverändert.

### Seite 31 · Für alle — vegetarisch & vegan
Neu zuoberst zwei Zeilen mit den **Gläsli**, direkt aus den Sortimentsdaten
gezogen, damit sie automatisch mitlaufen, wenn sich die Gläsli-Seite ändert:

- **Gläsli vegan:** Hummus · Couscous Orient · Asia-Krautsalat — Seite 11
- **Gläsli vegetarisch:** Ziegenkäse-Crème · Caprese · Quinoa · Griechisch ·
  Ebly · Ziegenkäse-Mousse · Tomaten-Tatar — Seite 11

Die Karte auf der Seite ist dafür höher geworden.

---

## 2026-10-27 · Cremeschnitte bei den veganen Desserts

Die Karte «Vegane Dessertvariationen» auf Seite 28 hat neu ein Bild: unsere
Cremeschnitte, aus dem Onlineshop-Archiv, unverändert übernommen und nur
zugeschnitten.

**Zwei Punkte dazu:**
- Das Foto zeigt die **normale** Cremeschnitte. Falls die vegane anders aussieht,
  braucht es ein eigenes Foto. [Bitte prüfen.]
- Das Bild steht auf weissem Grund und ist damit deutlich heller als die anderen
  fünf Karten der Seite. Auf Wunsch tone ich es etwas ab.

---

## 2026-10-27 · Neues Mini-Pâtisserie-Foto

Euer neues Foto der Mini-Pâtisserie-Platte ist **unverändert übernommen** — nicht
durch nano banana gelaufen, nur zugeschnitten. Es steht jetzt an drei Stellen:

- **Seite 28** als Themenbild der Seite «Der süsse Abschluss»
- **Seite 28** auf der Karte «Mini Pâtisserie assortiert»
- **Seite 30** auf der Karte «Was sonst noch süss ist»

Die «wick»-Schoggiplättchen auf den Stücken bleiben drauf — sie gehören zum
Produkt. Das alte, erzeugte Bild ist ersetzt.

---

## 2026-10-27 · Neue Seite «Weitere Locations», Karten mit Preisband, Korrekturen

Die Broschüre hat jetzt **39 Seiten**.

### Neu: Seite 36 · Weitere Locations
Direkt nach dem Säntisblick. Drei Säle, in die wir regelmässig liefern:
Entra Rapperswil, Eventhouse Rapperswil, Radio Zürisee Loft — je mit Adresse,
Grösse und wofür der Saal passt.
**Die Zahlen stammen aus den öffentlichen Angaben der Locations und sind noch
nicht bei den Betreibern bestätigt.** [FEHLT: Adresse Eventhouse Rapperswil.]
[FEHLT: Fotos — euer Entra-Foto zeigt die Leinwand mit Schriftzug und die
Getränkekarte; beides lässt sich nicht wegschneiden, ohne den Saal zu verlieren.]

### Karten mit Preisband
Die Buffet-Karten (Seite 21) und die Grillplatten (Seite 27) hatten viel Leere in
der Mitte und den Preis lose am unteren Rand. Neu sitzt der Preis in einem
rostfarbenen Band am Kartenfuss — ein Block, der die Karte abschliesst.

### Küche
- **Jasminreis heisst überall Trockenreis** (5 Stellen).
- Das Gemüse-Thai-Curry wird mit Reis serviert — steht so in den Zutaten.

### Menü
- **«Herzstück» heisst neu «Die Proteine»** — auf Seite 23, 24, im
  Inhaltsverzeichnis und auf der Vergleichsseite.
- Die vier Schrittbilder auf Seite 23 sind weg, ebenso das Bild auf Seite 24.
  Seite 23 ist neu eine Kopfseite.

### Bilder
- **Apéro im Gläsli:** neues Themenbild, nah an eurem Anlassfoto — schräg von
  oben, Becher in Reihen auf schwarzen Stufen, echter Raum im Hintergrund.
  Der Studio-Look ist weg.
- **Klassiker für grosse Runden:** das Bild mit dem Wärmebehälter ist raus, die
  Seite ist wieder eine Kopfseite. [FEHLT: neues Themenbild — die Buffetlinie.]
- **Brot XXL:** das Themenbild soll das Laugenherz zeigen. [FEHLT: noch nicht
  erzeugt.]

### Technik
Ein Fehler im Zusammenbau ist korrigiert: der Seitenindex folgte der sortierten
Nummer statt der Reihenfolge in `SEITEN`. Durch die neue Seite mit Schlüssel 1
landete dadurch das Inhaltsverzeichnis an der falschen Stelle.

### Achtung: fal.ai ohne Guthaben
Die drei fehlenden Bilder konnte ich nicht mehr erzeugen —
*«User is locked. Reason: Exhausted balance.»* Sobald das Konto wieder gedeckt
ist, hole ich sie nach.

---

## 2026-10-27 · Süsser Abschluss, Torten, «Für alle» und Eventraum

### Süsser Abschluss (Seite 28)
Neu eine Hero-Seite mit sechs Karten statt vier Spalten. Die Bilder stammen aus
euren Pâtisserie-Fotos: die gefüllte Platte für die Mini Pâtisserie, die runde
Platte für die Cup Cakes, eure Mousse-Schale und das Dessert im Gläsli.
Dazu ein Themenbild aus beiden Platten. Cake Pops und die veganen Desserts haben
weiterhin kein echtes Foto.

### Dessert am Teller (Seite 29)
Ein einziges Themenbild — die Reihe angerichteter Dessertteller von eurer Website.
Die sechs Platzhalter sind weg.

### Torten & Confiserie (Seite 30)
Neu gebaut, Inhalt wie im Original. Themenbild: eure Hochzeitstorte.
Drei Karten — Torten nach Ihrer Idee (die Beeren-Torte), Confiserie (die kleinen
Pralinenschachteln als Gastgeschenk, einzeln verpackt) und Was sonst noch süss ist
(die Mini-Pâtisserie-Platte). Torten und Confiserie stehen neu ohne Preisplakette,
weil beides nach Offerte geht.

### Für alle — vegetarisch & vegan (Seite 31)
Neu gebaut und auf den aktuellen Stand gebracht:
- **Zigerbrüüt-Röllchen gestrichen.**
- **Apéro Wrap Couscous gestrichen** — er ist auch auf Seite 15 weg. Eine vegane
  Alternative ist in Arbeit; der Hinweis steht in der Fusszeile.
- **Falafel-Bissen** neu in der veganen Liste, mit Verweis auf Seite 17.
- Verweise nachgeführt: vegane Torten Seite 30, vegane Suppen Seite 26.
- Bilder: Partybrot, Bäckerpastetli Rüebli-Sesam, Spiessli Frucht klein,
  Falafel-Bissen und Mini Pâtisserie — alles Bilder, die auch sonst in der
  Broschüre stehen.

### Eventraum (Seite 35)
Neu gebaut, mit einem Themenbild aus euren Säntisblick-Fotos.
**Neu 80 Sitzplätze statt 120** — und der Hinweis, dass der Anlass mit Zeltaufbau
auf bis zu 400 Personen wächst. Der Zeltaufbau selbst ist nach Offerte.

### Noch offen
- [FEHLT: Preis] Rüebli-Sesam-Tartelette, Falafel-Bissen pro Stück.
- [FEHLT] Vegane Alternative zum gestrichenen Apéro Wrap Couscous.
- Cake Pops und vegane Desserts haben kein echtes Foto.
- [FEHLT] Preis für den Zeltaufbau vor dem Eventraum.

---

## 2026-10-27 · Echte Referenzfotos, Warme Häppchen zusammengelegt, Kapitel C überarbeitet

### Neue Referenzbilder
Alle Bilder dieser Runde stammen aus euren Katalogfotos im Ordner
«Neue Referenzbilder». Sie liegen im Repo unter `referenzen/produkte/` — **mit
weggeschnittenem Wick-Logo**, damit in den erzeugten Bildern nie Schrift entsteht.
Beim Traubenbrot ist zusätzlich das Namensschild weggeschnitten, bei den
Frischkäsekugeln der Werbetext.

### Seiten des Apéro-Teils
- **Seite 13 heisst wieder «Brötli gefüllt»** statt «Knöpfli gefüllt». Inhalt und
  Preise wie im Original: fünf Brotsorten, drei Füllungsgruppen, Minibrötli 2.50,
  Partybrötli 2.80. Das Themenbild zeigt die echten gefüllten Brötli von eurem
  Tablettfoto.
- **Seite 12 · Brot & Brötli:** Traubenbrot, Picknickbrot und Partybrot neu nach
  euren Fotos.
- **Seite 14 · Brot XXL:** Laugenherz und Brot am Meter in Zahlenform neu nach
  euren Fotos.
- **Seite 15 · Belegtes:** Belegte Brötli rund nach eurer Canapé-Platte,
  Zwirbelwick Rustico nach den Rustico-Fotos, Frischkäse-Pralinen nach eurem Foto —
  nur die Kugeln, ohne das Drumherum.
- **Seite 16 · Spiessli:** **Antipasti-Spiessli wieder aufgenommen**, Bild nach
  eurer Vorlage. Jetzt fünf Sorten.
- **Seite 17 · Warme Häppchen:** **Apérogebäck und Warme Häppchen sind eine Seite.**
  Sechs Karten — Chüechli, Schinkengipfel, Chili Würstli, Älpler-Magronen-Tartelette,
  Ghackets-Krokette, Falafel. Das **Chäs-Chüechli «Rüttiberg» steht neu als Sorte bei
  den Chüechli** zu 2.20. Dazu ein eigenes Themenbild aus den vier Produkten.
- **Seite 18 · Platten:** **Grissini und Tray of Snacks gestrichen** — es bleiben die
  vier Platten.

### Kapitel C
- **Seite 21 · Buffets:** neue Namen, die zum Essen passen — Chuchi-Klassiker,
  Gartenbeiz, Sonntagsbraten, Grillabend, Weltreise, Festtafel. Die Gerichte sind
  unverändert. Themenbild: euer Buffet von der Website-Cateringseite.
- **Seite 22 · Klassiker für grosse Runden:** ein Themenbild statt sechs Platzhaltern,
  die vier Hinweise als Band am Kartenfuss.
- **Seiten 24 und 25 · Die Auswahl** sind jetzt zwei Seiten: die Proteine auf der
  einen, Stärkebeilagen, Gemüse und Saucen auf der anderen. Die vier Schrittbilder
  (Herzstück, Stärkebeilage, Gemüse, Sauce) stammen aus euren Referenzfotos.
- **Seite 26 · Suppen und Salate:** Bündner Gerstensuppe neu **6.80** statt «nach
  Kalkulation», **Kürbiscremesuppe** bei den saisonalen Suppen ergänzt. Salate am
  Teller und das Salatbuffet stehen neu in einem breiten rostfarbenen Band über die
  ganze Seitenbreite. Als Themenbild steht hier das rohe Gemüse auf dem Brett — das
  angerichtete Salatbuffet sah zu sehr nach KI aus.
- **Seite 27 · Grillplausch:** ein Themenbild nach eurem Grillfoto.

### Seitenzahlen
Durch das Zusammenlegen fällt eine Seite weg, durch die geteilte Auswahl kommt eine
dazu — die Broschüre bleibt bei 38 Seiten. Inhaltsverzeichnis, Querverweise und
Fusszeilen sind nachgeführt.

### Neu: Layoutprüfung
`broschuere/pruefen.py` misst alle Seiten im Browser und meldet Text, der aus seiner
Karte oder aus der Seite herausragt, sowie Bänder, die eine Spalte überdecken.
Aktueller Stand: keine Fundstelle.

### Noch offen
- [FEHLT: Preis] Kürbiscremesuppe. Ist das dasselbe wie die Kürbissuppe (6.50, vegan)
  unter «Klassisch», oder eine eigene Sorte?
- Die belegten Brötli rund stehen in der Broschüre nur mit «Tomaten · Avocado».
  Euer Ordner zeigt zehn Sorten — soll die Liste erweitert werden?
- [FEHLT] Zopfherz gefüllt hat weiterhin kein Bild.

---

## 2026-10-27 · Bilder der alten Seiten 11 bis 18, Warme Häppchen gekürzt

Betroffen sind die alten Seiten 11–18, in der neuen Zählung die Seiten 12–19.
Grundlage sind echte Wick-Produktfotos, die bereits im Broschüren-Look aufbereitet
waren. Neu erzeugt wurde nur, was es als Foto nicht gibt — sechs Bilder.

### Neu gebaute Seiten
- **Seite 12 · Brot & Brötli** (alt 11): Inhalt unverändert aus dem Original
  übernommen, neu als Hero-Seite mit drei Karten und echten Fotos.
- **Seite 18 · Warme Häppchen** (alt 17): **Mini-Röstitaschen und Brätchögeli im
  Blätterteig gestrichen.** Es bleiben vier Häppchen — Chäs-Chüechli «Rüttiberg»,
  Älpler-Magronen-Tartelette, Ghackets-und-Hörnli-Krokette, Falafel-Bissen.
  Einleitung von «sechs» auf «vier» geändert, Fusszeile entsprechend angepasst.

### Bilder
- **Seite 13 · Knöpfli gefüllt:** statt sechs Einzelbildern **ein Themenbild**.
  Es zeigt gefüllte Mini-Laugenknöpfli und Mini-Butterknöpfli im Korb und auf dem
  Holzbrett, erzeugt aus zwei echten Wick-Fotos der gefüllten Knöpfli.
  Die Seite ist dadurch eine Hero-Seite geworden.
- **Seite 19 · Platten & Sharing:** die vier Platten und die Grissini **neu auf
  mattschwarzen Platten statt Palmblatt** — das Essen ist unverändert aus dem
  echten Foto übernommen, gewechselt hat nur die Unterlage. Damit stimmt das Bild
  mit dem Text «neu auf silbrigen oder schwarzen Platten» überein.
  Tray of Snacks bleibt das echte Foto im orangen Tray.
- **Seiten 14, 15, 16, 18:** alle Entwurfsbilder durch echte Wick-Fotos ersetzt
  (Brot XXL, Belegtes und Canapés, Apérogebäck, Warme Häppchen).
- Bei den Canapés zeigen die Bilder jetzt das passende Produkt: die runden Brötli
  mit Gemüsegarnitur, der Zwirbelwick Rustico mit Lachs, Käse und Schinken.

### Seitenzahlen
Die Fusszeilen trugen noch die alten Nummern. Alle Seiten ab der Gläsli-Seite sind
nachgeführt — die Produktseiten auf 12–19, der Essensteil auf 21–29. Damit stimmen
Fusszeile und Inhaltsverzeichnis überein.

### Dazu, gleicher Tag
- **Seite 16 · Schinkengipfel:** neues Bild, nur noch Schinkengipfel auf dem Brett,
  aus dem echten Foto erzeugt. Vorher standen Chüechli daneben.
- **Seite 20 · Unterwegs** (alt 19) neu gebaut: vier Lunchbags — Zürichsee 12.90,
  Holzsteg 13.90, Etzel 16.90, Healthy 18.90. Inhalt und Preise unverändert aus dem
  Original, Bilder echt.

### Noch offen
- [FEHLT] Preis für Knöpfli gefüllt, Zopfherz, Apérowrap klein, Frischkäse-Pralinen,
  Tray of Snacks — unverändert offen.
- **Zopfherz gefüllt** hat weiterhin kein Bild.

---

## 2026-10-27 · Inhaltsverzeichnis und Verweisseiten neu gebaut

### Seiten 6, 8, 9 und 10
**Warum:** Durch die neue Seite 11 und den gekürzten Essensteil stimmten alle
Seitenzahlen und Querverweise nicht mehr. Diese vier Seiten tragen die meisten davon.

- **Seite 6 · Ihr Weg:** Inhaltsverzeichnis komplett nach der neuen Gliederung,
  sieben Spalten, Legende im Rostkreis. Die sechs Legenden-Icons sind neu aus dem
  Original geschnitten (`icons/leg-*.png`, cremefarbene Scheibe auf Rost).
- **Seite 8 · Cateringformen:** alle Verweise nachgeführt, dazu ein vierter Block
  «Apéro im Gläsli — Seite 11».
- **Seite 9 · Mengen richtig planen:** Verweis auf Seite 12 statt 11; neu steht hier
  die eigene Gläsli-Mindestmenge von 15 Stück pro Sorte, sowohl bei «pro Person»
  als auch bei den Mindestmengen.
- **Seite 10 · Apéro-Pakete:** Seitenliste nachgeführt (12–14 Brot bis 28–29 Süsser
  Abschluss), dazu auf der Apéro-Riche-Karte der Verweis
  *Ergänzen Sie Ihren Apéro Riche mit Gläsli — Seite 11.*

**Korrektur im Original:** Auf Seite 8 verwies «Vollständiges Catering mit Service»
auf die Seiten 26 bis 28 — dort stehen aber die Menüstufen, nicht Material und
Service. Neu zeigt der Verweis auf die Seiten 32 bis 36, also auf das Kapitel
«Ihr Anlass komplett». [Bitte bestätigen, ob das so gemeint war.]

---

## 2026-10-27 · Broschüre zusammengebaut

### Alles in einem Dokument: `out/wick-apero-catering-NEU.pdf`
Aufruf `python broschuere/bauen.py --zusammenbauen`. **38 Seiten statt 40** —
eine Seite kommt dazu (Gläsli), drei fallen im Essensteil weg.

| neu | Inhalt | bisher |
|---|---|---|
| 1–10 | Umschlag bis Apéro-Pakete | 1–10 |
| **11** | **Apéro im Gläsli** | neu |
| 12–20 | Brot & Brötli bis Unterwegs | 11–19 |
| 21–29 | Warme Küche bis Dessert am Teller | 20–31 |
| 30–38 | Torten bis Rückseite | 32–40 |

### Mengenlogik: Gläsli als Zusatz
Entscheid der Geschäftsleitung: Die acht Häppchen des Apéro Riche bleiben
unverändert, das Gläsli kommt zusätzlich dazu. Damit müssen die Seiten 8, 9 und 10
**nicht** angefasst werden — die bestehende Rechnung bleibt überall gültig.
Auf der Gläsli-Seite steht neu: *Zusätzlich zum Apéro Riche: 1 Gläsli pro Person.*

### Offen: Seitenzahlen und Querverweise
Ab Seite 12 stimmen die **gedruckten Seitenzahlen nicht mehr** — sie stammen aus der
alten Nummerierung. Betroffen sind die zwölf Seiten, die noch das Original sind:
Brot & Brötli, Warme Häppchen, Unterwegs sowie Torten bis Rückseite. Dazu kommen die
Querverweise im Inhaltsverzeichnis auf Seite 6 und auf den Seiten 8 bis 10.
Beides lässt sich nur beheben, indem diese Seiten neu gebaut werden.

---

## 2026-10-27 · Gläsli-Apéros, neue Seite 11

### Neue Seite «Apéro im Gläsli»
**Seite:** neu 11, direkt nach den Apéro-Paketen. Entwurf in `out/vorschau.pdf`,
Aufruf `python broschuere/bauen.py --vorschau 11`.
**Warum dort:** Die Gläsli gibt es nur mit einem Apéro Riche. Diese Abhängigkeit
versteht man nur, wenn die Seite unmittelbar neben der Apéro-Riche-Karte steht.

**Inhalt:** vier Kategorien mit 16 Sorten — Dip & Gemüse (3) · Salat-Gläsli (6) ·
Mousses (3) · Cocktails & Tatare (4). Dazu ein hervorgehobener Block in Rost mit den
beiden Verkaufsregeln und der Mengenstaffelung.

**Kennzeichnung:** nach dem bestehenden System der Broschüre, also nur `VEGAN` und
`VEG`. Fisch und Fleisch bleiben ohne Zeichen — so hält es die Broschüre überall,
auch bei Lachstatar und Beef-Tatar. Keine neuen Symbole eingeführt.

### Mengenlogik geändert — Folge des Entscheids «süsse Gläsli weglassen»
Die freigegebene Variante B ging von 4 Häppchen + 2 Gläsli aus, davon ein süsses
Gläsli für den Dessert-Anteil. Ohne süsse Gläsli müssen die zwei süssen Einheiten
wieder aus Häppchen kommen. Neue Rechnung bei gleichem Faktor
(1 Gläsli = 2 Häppchen) und gleicher Sättigung:

> **Apéro Riche mit Gläsli:** 6 Häppchen pro Person, davon 2 süss, dazu 1 Gläsli.
> 6 + 2 = 8 Häppchen-Einheiten — gleich viel wie heute.

| Gäste | Gläsli-Sorten | Stück pro Sorte |
|---|---|---|
| ab 20 | 1 | 20 |
| ab 30 | 2 | 15 |
| ab 45 | 3 | 15 |
| ab 60 | 4 | 15 |
| ab 80 | 5 | 16 |

Die Mindestmenge von 15 Stück ist in jeder Zeile erfüllt.

**Noch nicht angepasst:** Die bestehende Mengenlogik auf den Seiten 8, 9 und 10 steht
weiterhin auf «8 Häppchen pro Person». Diese drei Seiten sind bisher Original und
müssten dafür neu gebaut werden — mache ich, sobald die neue Rechnung bestätigt ist.
Ebenso der Querverweis auf der Apéro-Riche-Karte.

### Bild
Ein Themenbild statt Einzelfotos, nach den echten Wick-Fotos eines früheren Anlasses
(`referenzen/produkte/glaesli_*.jpeg`): dieselben eckigen Becher, dieselben Löffel,
derselbe gestufte Karton. Geändert wurde der Karton — **schwarz statt violett** — und
der Schriftzug «www.baeckerei-wick.ch» sowie die Namenskärtchen sind weg, weil
gedruckte Schrift sich nicht sauber erzeugen lässt. Verworfene Varianten liegen in
`bilder/entwuerfe/`.

---

## 2026-10-27 · Konzept C, der ganze Essensteil (Entwurf)

### Sieben neue Seiten gebaut
**Bisher 20–31 (zwölf Seiten) → neu neun Seiten.** Entwurf in `out/vorschau.pdf`,
Aufruf `python broschuere/bauen.py --kapitel-c`. Eigene Nummerierung, **noch nicht
in die 40-Seiten-Datei eingebaut.**

| neu | Inhalt | bisher |
|---|---|---|
| 20 | Warme Küche — drei Wege, als Vergleichstabelle | 20 |
| 21 | Weg 01 · Unsere Buffets | 23 |
| 22 | Weg 02 · Klassiker für grosse Runden | 24 |
| 23–24 | Weg 03 · Eigenes Menü, Doppelseite | 25–28 |
| 25 | Dazu — Suppen und Salate | 21 + 22 |
| 26 | Draussen · Grillplausch | 29 | *(noch zu bauen)* |
| 27 | Zum Schluss · Süsser Abschluss | 30 | *(steht schon)* |
| 28 | Zum Schluss · Dessert am Teller | 31 |

Die Reihenfolge folgt jetzt dem, was Seite 20 ankündigt: erst die drei Wege der Reihe
nach, dann was zu allen dreien passt, dann draussen, dann süss. Alle Preise und
Positionen aus der bestehenden Broschüre, nichts ergänzt.

**Bilder:** durchgehend Platzhalter «Foto folgt», wie besprochen.

---

## 2026-10-27 · Konzept C, Menü-Doppelseite (Entwurf)

### Die vier Menüseiten auf zwei
**Seiten:** bisher 25–28 → neu zwei Seiten
**Was:** Entwurf gebaut, liegt als `out/vorschau.pdf`. **Noch nicht in die
40-Seiten-Datei eingebaut** — das ändert die Seitenzahl, und die Einbaulogik ersetzt
bisher Seite für Seite.

- **Linke Seite «Ihr eigenes Menü»:** Hero, vier Platzhalter für die Schrittbilder,
  darunter links die vier Schritte, rechts das Rechenbeispiel mit der Summe.
- **Rechte Seite «Die Auswahl»:** alle **93 Positionen** in vier Spalten —
  Rind/Kalb · Schwein · Geflügel/Fisch/Vegetarisch · Beilage/Gemüse/Sauce.

**Wichtig:** Die freigegebene Möglichkeit, Preiszeilen zusammenzurücken, **brauchte
es nicht**. Jede der 93 Positionen steht einzeln mit Gewicht und Preis, nichts wurde
zusammengefasst. Die Seite geht auch so auf.

**Neue Bauoption:** `python broschuere/bauen.py --vorschau 25 26` baut einzelne Seiten
nach `out/vorschau.pdf`, ohne sie in die 40-Seiten-Datei einzubauen.

### Noch ein Encoding-Fehler behoben
`bauen.py` las `sortiment.json` ohne `encoding='utf-8'`. Unter Windows kamen dadurch
alle Produktnamen mit Umlaut falsch an und die Seiten liessen sich nicht bauen.

---

## 2026-10-27 · Küchendaten erfasst

### Abteilung «Küche» in `sortiment.json` gefüllt
**Seiten:** 21–24, 26–29, 31 (Datenerfassung, an den Seiten selbst nichts geändert)
**Was:** 11 Gruppen mit zusammen 141 Preiszeilen aus der bestehenden Broschüre übernommen:
Suppen · Vorspeisen am Teller · Salate am Teller · Salatbuffet · Buffets ·
Klassiker für grosse Runden · Eigenes Menü Schritt 01 (Herzstück) ·
Eigenes Menü Schritt 02–04 · Grillplausch · Burgerplausch · Dessert am Teller.
**Warum:** Ohne diese Daten lässt sich Konzept C für die Seiten 20–31 nicht bauen.
**Quelle:** `quellen/broschuere-40s.pdf`, über die Wortpositionen ausgelesen, nicht
über den Textfluss — in mehrspaltigen Preistabellen verrutscht der sonst um eine Zeile.
Nichts ergänzt, nichts weggelassen. Die Bündner Gerstensuppe hat weiterhin keinen
Preis, das ist im Datensatz als `preis_offen` vermerkt.

---

## 2026-10-27 · Seite 16 Spiessli

### Fünf Produktbilder neu, im Broschüren-Look
**Seite:** 16
**Was:** Alle fünf Spiessli-Bilder neu erzeugt und in `bilder/final/` abgelegt:
Tomaten & Mozzarella, Antipasti, Käse-Trauben, Melonen-Rohschinken, Frucht klein.
**Warum:** Für Käse-Trauben und Melonen-Rohschinken stand «Foto folgt». Die beiden
bisherigen Fotos (Antipasti, Frucht klein) waren helle Katalogaufnahmen auf weissem
Holz und passten nicht zum dunklen Broschüren-Look.

**Wie entstanden:** Jedes Bild mit zwei Referenzen erzeugt — erstens das echte
Wick-Foto aus `sortiment/bilder/produkte/` für das Produkt, zweitens eine
Stilreferenz für Licht und Untergrund. Das Produkt bleibt unverändert, geändert
wurden nur Untergrund und Licht. Zwei Ausnahmen, beide bewusst:

- **Tomaten & Mozzarella:** der Focaccia-Sockel ist weg — so, wie das Produkt neu ist.
- **Antipasti:** aus den Plastikbechern und vom orangen Tablett genommen,
  damit kein Schriftzug im Bild steht.

Käse-Trauben und Melonen-Rohschinken gibt es noch nicht als Foto; dort diente das
echte Spiessli-Foto nur als Vorlage für Pick und Bissengrösse.
Verworfene Varianten liegen in `bilder/entwuerfe/`.

### Antipasti-Spiessli gestrichen
**Seite:** 16 · **Was:** Das Antipasti-Spiessli ist ganz aus dem Sortiment und von der
Seite genommen und steht jetzt unter «Gestrichen». Die Bildleiste zeigt noch vier Bilder.
**Warum:** Entscheid der Geschäftsleitung.

### «Saisonal» gestrichen
**Seite:** 16 · **Was:** Die sechste Spiessli-Position «Weitere saisonale Spiessli»
ist aus `sortiment.json` und von der Seite entfernt, die Bildleiste zeigt noch fünf
Bilder und ist mittig gesetzt. **Warum:** Entscheid der Geschäftsleitung — saisonal
ist über Melonen-Rohschinken abgedeckt.

### Lokaler Bau lauffähig gemacht
**Was:**
- `bauen.py`: `write_text(…, encoding='utf-8')`. Ohne das schreibt Windows die
  HTML-Datei in der Systemcodepage und alle Umlaute und Gedankenstriche brechen.
- `bauen.py`: neue Funktion `chrome()` sucht den ersten vorhandenen Browser
  statt den fest verdrahteten Cloud-Pfad. Der Cloud-Pfad steht weiterhin an
  erster Stelle, dort ändert sich nichts.
- `bauen.py`: neue Hilfsfunktion `F()` für freigegebene Bilder aus `bilder/final/`.
- `broschuere/icons/` mit sieben Icons wiederhergestellt. Sie fehlten im Repo, weil
  `.gitignore` alle `*.png` ausschliesst. Ausgeschnitten aus den dunklen Panels der
  Seiten 12 und 18 der Original-PDF und als runde PNGs mit transparentem Rand abgelegt.
- `.gitignore`: `!broschuere/icons/*.png` ergänzt, damit die Icons nicht wieder verloren gehen.

**Offen:** Das Zeichen `huet` (für «Sorten:» und «Catering:») konnte ich im Original
nicht finden — dort steht vorläufig dasselbe Brot-Zeichen wie bei `brot`.

---

## 2026-10-27

### Bestandsaufnahme und Projektdokumentation
**Seiten:** keine — es wurde nichts an der Broschüre geändert.
**Was:** Angelegt wurden `STATUS.md`, `PRODUKTE.md`, `CHANGELOG.md`,
`KONZEPT-essen-20-31.md` sowie die Ordner `referenzen/{produkte,stil,umgebung}`
mit `_ANFRAGEN.md` und `bilder/{final,entwuerfe}`.
**Warum:** Überblick über Seitenstand, Bildbestand und Sortimentsdaten, bevor
etwas verändert wird.

**Befunde:**
- Im Bildarchiv `Pictures\Claude bilder` (rund 430 Bilder) gibt es **kein einziges
  Foto aus der warmen Küche** — keine Suppen, Salate, Buffets, Gerichte oder Grill.
  Der Essensteil muss vollständig neu bebildert werden.
- In `sortiment/sortiment.json` sind die Abteilungen **Küche** und **Confiserie** leer.
- Auf Seite 16 stehen drei Platzhalter «Foto folgt».
- Der lokale Bau läuft noch nicht: Python fehlt auf diesem Rechner, und
  `broschuere/bauen.py` erwartet den Chromium-Pfad der Cloud-Umgebung.

**Nicht verändert:** `sortiment.json`, `bauen.py`, `seiten.html`, alle Bilder,
alle bestehenden Seiten.
