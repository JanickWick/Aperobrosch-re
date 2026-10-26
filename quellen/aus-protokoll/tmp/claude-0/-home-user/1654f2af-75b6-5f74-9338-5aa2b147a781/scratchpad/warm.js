  /* ======================================================================
     08 · WARME KÜCHE
     Quelle: «Catering & Apéro Broschüre», Wick Catering, S. 11–26.
     Diese Fassung ist die jüngere und vollständigere der beiden Wick-
     Quellen. Wo sie einem Preis der älteren Broschüre widerspricht, gilt
     hier die jüngere — jeder Widerspruch steht in OFFENE-PUNKTE.md und
     muss von Wick einmal bestätigt werden.

     Drei Wege führen zum warmen Essen. Diese Dreiteilung trägt das
     ganze Kapitel:
       A  Buffet      — fertig zusammengestellt, ab 30 Personen
       B  Klassiker   — einzelne Gerichte pro Portion, für grosse Runden
       C  Eigenes Menü — Baukasten in vier Schritten, ab 10 Personen
     ====================================================================== */

  const WEGE = [
    { nr: '01', key: 'buffet', t: 'Unser Buffet',
      unter: 'ab 30 Personen · Pauschalpreis pro Person',
      wann: 'Wenn viele Gäste kommen und die Auswahl für sich sprechen soll.',
      wie:  'Sechs fertig zusammengestellte Buffets. Sie wählen eines aus, wir bringen alles mit.',
      seite: 'buffets' },
    { nr: '02', key: 'klassiker', t: 'Einzelne Klassiker',
      unter: 'Preis pro Portion',
      wann: 'Wenn es unkompliziert und sättigend sein soll — Vereinsanlass, Baustellenfest, Grossveranstaltung.',
      wie:  'Zehn bewährte Gerichte, die in jeder Menge funktionieren. Ein Gericht genügt.',
      seite: 'klassiker' },
    { nr: '03', key: 'menue', t: 'Ihr eigenes Menü',
      unter: 'ab 10 Personen · Preis pro Person',
      wann: 'Wenn am Tisch serviert wird — Hochzeit, Gala, Geschäftsessen.',
      wie:  'Sie stellen Ihr Menü in vier Schritten selbst zusammen. Wir rechnen es Ihnen zusammen.',
      seite: 'baukasten' },
  ];

  /* --- Der Auftakt: Suppen ------------------------------- Quelle: S. 11 */
  const SUPPEN = {
    hinweis: 'Wir liefern die Suppen kalt oder heiss. Auf Wunsch stellen wir '
           + 'Wärmebehälter zur Verfügung.',
    fingerfood: 'Alle Suppen gibt es auch im Gläsli als Fingerfood — dann sind sie '
              + 'Teil des Apéros statt des Menüs.',
    einheit: 'pro Portion',
    gruppen: [
      { k: 'Klassisch', items: [
        ['Tomatencremesuppe', 5.80, 'vegan'],
        ['Rüebli-Ingwersuppe', 5.80, 'vegan'],
        ['Gemüsecremesuppe', 6.00, 'vegan'],
        ['Kartoffelsuppe', 6.20, 'veg'],
        ['Kürbissuppe', 6.50, 'vegan'],
      ] },
      { k: 'Herzhaft', items: [
        ['Linsensuppe', 6.80, 'vegan'],
        ['Rieslingsuppe', 7.20],
        ['Rinds-Consommé', 7.50],
        ['Gulaschsuppe', 8.50],
        ['Bündner Gerstensuppe', null],
      ] },
      { k: 'Saisonal', items: [
        ['Marronisuppe', 7.20, 'vegan'],
        ['Bärlauchsuppe', 7.50, 'veg'],
        ['Pilzsuppe', 7.80, 'veg'],
        ['Spargelsuppe', 8.20, 'veg'],
      ] },
    ],
  };

  /* --- Der Auftakt: Vorspeisen --------------------------- Quelle: S. 14 */
  const VORSPEISEN = {
    intro: 'Für Anlässe, an denen am Tisch serviert wird. Eine Vorspeise eröffnet '
         + 'das Menü und gibt dem Abend seinen Takt.',
    einheit: 'pro Portion',
    gruppen: [
      { k: 'Kalt', items: [
        ['Gemüsetatar', 14.00, 'vegan'],
        ['Vitello Tonnato', 15.50],
        ['Lachstatar mit Thai-Salsa', 16.50],
        ['Burrata mit Tomaten und Basilikum', 17.00, 'veg'],
        ['Beef-Tatar', 18.00],
      ] },
      { k: 'Warm', items: [
        ['Hausgemachte Käseravioli mit Bergkäsefüllung', 16.00, 'veg'],
        ['Grüne Spargeln mit Hollandaise-Espuma', 17.50, 'veg', 'nur im Frühling'],
        ['Morchel-Tagliatelle mit Rahmsauce', 19.50, 'veg'],
      ] },
    ],
  };

  /* --- Salate -------------------------------------- Quelle: S. 12 und 13 */
  const SALATE = {
    teller: {
      titel: 'Am Teller angerichtet',
      desc: 'Als Vorspeise oder als leichte Hauptmahlzeit, sorgfältig angerichtet.',
      einheit: 'pro Portion',
      items: [
        ['Bunter Blattsalat mit Hausdressing', 11.50, 'vegan'],
        ['Gemischter Salat mit saisonalem Gemüse', 12.00, 'vegan'],
        ['Sommersalat mit Melonen und Feta', 14.00, 'veg', 'Sommer'],
        ['Caesar Salad', 14.50, 'veg'],
        ['Winterlicher Nüsslisalat mit Speck, Ei und Croutons', 15.00, null, 'Winter'],
        ['Frühlingssalat mit Spargeln, Orangen und Mandeln', 15.50, 'veg', 'Frühling'],
        ['Herbstsalat mit Kürbis, Feigen, Walnüssen und Ziegenkäse', 16.00, 'veg', 'Herbst'],
      ],
    },
    buffet: {
      titel: 'Salatbuffet',
      desc: 'Sie bestimmen, wie viele Sorten auf dem Buffet stehen. Dazu kommen '
          + 'unsere zwei hausgemachten Saucen, French und Italian.',
      einheit: 'pro Person',
      stufen: [
        ['3 Sorten', 'ab 20 Personen',  8.50],
        ['5 Sorten', 'ab 20 Personen', 10.50],
        ['7 Sorten', 'ab 50 Personen', 12.50],
        ['10 Sorten', 'ab 80 Personen', 14.50],
      ],
      ab: true,
    },
    sorten: {
      titel: 'Die Sorten zur Auswahl',
      gruppen: [
        { nr: '01', k: 'Leicht', items: [
          ['Blattsalat', 'vegan'], ['Tomatensalat', 'vegan'], ['Krautsalat', 'vegan'],
          ['Karottensalat', 'vegan'], ['Maissalat', 'vegan'], ['Broccoli-Salat', 'vegan'],
          ['Fenchel-Orangen-Salat', 'vegan'], ['Gurkensalat mit Dill-Joghurt', 'veg'] ] },
        { nr: '02', k: 'Sättigend', items: [
          ['Grüner Bohnensalat', 'vegan'], ['Mexikanischer Bohnensalat', 'vegan'],
          ['Quinoa-Avocado-Salat', 'vegan'], ['Couscous-Salat', 'vegan'],
          ['Bulgursalat', 'vegan'], ['Linsensalat', 'vegan'],
          ['Kartoffelsalat mit Mayonnaise', 'veg'], ['Tomaten-Mozzarella-Salat', 'veg'],
          ['Griechischer Salat', 'veg'], ['Selleriesalat Waldorf-Art', 'veg'],
          ['Teigwarensalat mit Bauernschinken', null] ] },
        { nr: '03', k: 'Saisonal', items: [
          ['Melonen-Feta-Salat', 'veg'], ['Pfirsich-Mozzarella-Salat', 'veg'] ] },
      ],
    },
  };

  /* --- Weg A · Die Buffets -------------------------------- Quelle: S. 15 */
  const BUFFETS = {
    min: 30,
    intro: 'Sechs Buffets, die sich an hunderten Anlässen bewährt haben. Jedes ist '
         + 'fertig zusammengestellt — Sie wählen aus, wir bringen alles mit.',
    einheit: 'pro Person',
    hinweis: 'Alle Buffets ab 30 Personen. Salatbuffet und Dessert lassen sich '
           + 'dazunehmen.',
    items: [
      { name: 'Züri-Fäscht', preis: 30.00,
        ton: 'Bodenständig und herzhaft',
        inhalt: ['Ghackets mit Hörnli', 'Geschmortes Kalbsgeschnetzeltes',
                 'Hörnli & geröstete Zwiebeln', 'Apfelmus', 'Saisongemüse'] },
      { name: 'Glarner Alpabfahrt', preis: 42.00,
        ton: 'Mit vegetarischem Hauptgang',
        inhalt: ['Vegetarische Gemüselasagne', 'Pouletgeschnetzeltes an Champignonsauce',
                 'Nudeln', 'Salzkartoffeln', 'Marktgemüse', 'Butterkartoffeln'] },
      { name: 'Alpenrose', preis: 45.00,
        ton: 'Der klassische Sonntagsbraten',
        inhalt: ['Schweinsbraten', 'Kartoffelgratin', 'Speckbohnen', 'Rüebli',
                 'Ofengemüse'] },
      { name: 'BBQ Spareribs', preis: 52.00,
        ton: 'Für draussen, zum Zugreifen',
        inhalt: ['Zarte BBQ Spareribs', 'Chicken Wings', 'Hausgemachter Coleslaw',
                 'Ofenkartoffeln mit Sauerrahm', 'Gegrillte Maiskolben', 'Grillgemüse'] },
      { name: 'Matterhorn Exotik', preis: 55.00,
        ton: 'Würzig, auch vegetarisch möglich',
        inhalt: ['Thai Curry mit Poulet, auch vegetarisch', 'Chili con Carne',
                 'Jasminreis', 'Naan-Brot', 'Gedämpftes Gemüse'] },
      { name: 'Rheinfall Genuss', preis: 62.00,
        ton: 'Fisch und Geflügel, das festlichste',
        inhalt: ['Lachsfilet an Zitronen-Dill-Sauce', 'Pouletbrust an Kräutersauce',
                 'Reis-Mix', 'Petersilienkartoffeln', 'Ratatouille', 'Gemüse-Mischung'] },
    ],
  };

  /* --- Weg B · Die Klassiker ------------------------------ Quelle: S. 17 */
  const KLASSIKER = {
    intro: 'Zehn Gerichte, die in jeder Menge funktionieren — ob für dreissig '
         + 'Gäste oder für dreitausend. Ein Gericht genügt, ein zweites gibt '
         + 'den Gästen die Wahl.',
    einheit: 'pro Portion',
    items: [
      { name: 'Warmer Schinken mit Kartoffelsalat', preis: 16.50,
        zutaten: 'Warmer Beinschinken, Kartoffelsalat.' },
      { name: 'Riz Casimir mit Pouletbruststreifen', preis: 19.50,
        zutaten: 'Pouletbruststreifen, fruchtige Currysauce, Reis.' },
      { name: 'Chili sin Carne', preis: 21.00, tag: 'vegan',
        zutaten: 'Veganes Gemüse, Bohnen, Jasminreis.' },
      { name: 'Penne Bolognese', preis: 22.00,
        zutaten: 'Penne, Bolognese-Sauce, Parmesan.' },
      { name: 'Bami Goreng mit Pouletbruststreifen', preis: 22.00,
        zutaten: 'Nudeln, Gemüse, Pouletbruststreifen.' },
      { name: 'Chili con Carne', preis: 23.00,
        zutaten: 'Rindfleisch, Bohnen, Jasminreis.' },
      { name: 'Gemüse-Thai-Curry', preis: 23.00, tag: 'vegan',
        zutaten: 'Veganes Gemüse, cremiges Thai Curry, Jasminreis.' },
      { name: 'Ghackets mit Hörnli', preis: 24.50, badges: ['pop'],
        zutaten: 'Hackfleisch, Hörnli, Röstzwiebeln, Apfelmus, Bergkäse.' },
      { name: 'Poulet-Thai-Curry', preis: 25.00,
        zutaten: 'Poulet, cremiges Thai Curry, Jasminreis.' },
      { name: 'Hausgemachte Rindfleisch-Lasagne', preis: 26.00, badges: ['pop'],
        zutaten: 'Rindfleischragout, Béchamelsauce, Lasagneplatten, Käsekruste.' },
      { name: 'Schmorbraten', preis: 26.00,
        zutaten: 'Schmorbraten, Kartoffelstock, Gemüse.' },
      { name: 'Rindsgeschnetzeltes «Stroganoff»', preis: 28.50,
        zutaten: 'Rindsgeschnetzeltes, Stroganoff-Sauce, Teigwaren, Gemüse.' },
    ],
  };

  /* --- Weg C · Der Menü-Baukasten ------------------- Quelle: S. 18 bis 23 */
  const BAUKASTEN = {
    min: 10,
    intro: 'Am Tisch serviert, Gang für Gang. Sie wählen vier Bausteine, wir '
         + 'rechnen sie zusammen — so wissen Sie vor der Offerte, woran Sie sind.',
    schritte: [
      { nr: '01', k: 'Das Herzstück',
        t: 'Fleisch, Fisch oder eine vegetarische Hauptkomponente. Das Gewicht steht dabei.' },
      { nr: '02', k: 'Die Stärkebeilage',
        t: 'Gratin, Risotto, Teigwaren, Kartoffeln oder Polenta.' },
      { nr: '03', k: 'Das Gemüse',
        t: 'Saisonal, gegrillt oder als einzelne Sorte.' },
      { nr: '04', k: 'Die Sauce',
        t: 'Was die drei Teile zusammenhält.' },
    ],
    beispiel: {
      titel: 'So rechnet sich ein Menü',
      zeilen: [
        ['01', 'Rindsfilet', '180 g', 38.00],
        ['02', 'Kartoffelgratin', '200 g', 6.00],
        ['03', 'Grillgemüse', '140 g', 6.00],
        ['04', 'Pfeffersauce', '', 2.00],
      ],
      total: 52.00,
      totalLabel: 'pro Person',
    },
    hinweise: [
      'Mindestmenge 10 Personen.',
      'Alle Preise pro Person.',
      'Suppe, Vorspeise und Dessert kommen aus den eigenen Kapiteln dazu.',
    ],
    herzstueck: [
      { k: 'Rind', items: [
        ['Rindsburger', '160 g', 25.00], ['Hackbraten', '180 g', 26.00],
        ['Rindsschmorbraten', '200 g', 30.00], ['Rindsfilet Stroganoff', '150 g', 35.00],
        ['Rindsentrecôte', '180 g', 36.00], ['Rindsfilet', '180 g', 38.00],
        ['Rindsfilet Wellington', '200 g', 45.00] ] },
      { k: 'Kalb', items: [
        ['Kalbshackbraten', '180 g', 27.00], ['Kalbsragout', '180 g', 30.00],
        ['Kalbsschmorbraten', '200 g', 33.00], ['Kalbsbäggli', '180 g', 34.00],
        ['Wienerschnitzel', '150 g', 34.00], ['Kalbsschnitzel natur', '150 g', 35.00],
        ['Kalbsossobucco', '300 g', 35.00], ['Kalbsgeschnetzeltes', '150 g', 36.00],
        ['Kalbs-Saltimbocca', '160 g', 37.00], ['Kalbskareebraten', '180 g', 39.00],
        ['Kalbsfilet-Medaillons', '160 g', 42.00] ] },
      { k: 'Schwein', items: [
        ['Schweinsbratwurst', '120 g', 22.00], ['Olma Bratwurst', '120 g', 23.00],
        ['Schweinsragout', '180 g', 25.00], ['Kasseler Schinken', '200 g', 25.00],
        ['Schweinsschmorbraten', '200 g', 26.00], ['Schweinsschnitzel natur', '150 g', 26.00],
        ['Schweinsgeschnetzeltes', '150 g', 27.00], ['Schweinsschnitzel paniert', '150 g', 27.00],
        ['Schweinssteak', '180 g', 28.00], ['Tessinerbraten', '200 g', 28.00],
        ['Schinken im Brotteig', '200 g', 28.00], ['Schweinskotelett', '220 g', 29.00],
        ['Spare Ribs', '400 g', 31.00], ['Schweinsfilet', '160 g', 32.00],
        ['Schweinsfilet im Speckmantel', '180 g', 34.00],
        ['Schweinsfilet im Blätterteig', '200 g', 36.00] ] },
      { k: 'Geflügel', items: [
        ['Pouletgeschnetzeltes', '150 g', 26.00], ['Pouletschenkelsteak', '180 g', 27.00],
        ['Pouletbrust', '160 g', 28.00], ['Poulet Piccata', '150 g', 29.00],
        ['Pouletbrust mit saisonaler Füllung', '180 g', 30.00],
        ['Poulet Saltimbocca', '160 g', 30.00],
        ['Konfierte Entenschenkel', '250 g', 32.00] ] },
      { k: 'Fisch', items: [
        ['Pochierte Forelle', '200 g', 32.00], ['Zanderknusperli', '150 g', 33.00],
        ['Kabeljaufilet', '150 g', 34.00], ['Lachsfilet', '150 g', 35.00],
        ['Eglifilet', '150 g', 36.00], ['Thunfischsteak', '160 g', 38.00],
        ['Riesenkrevetten', '150 g', 39.00] ] },
      { k: 'Vegetarisch & vegan', tag: 'veg', items: [
        ['Tagliatelle', '200 g', 22.00, 'veg'], ['Saisonales Risotto', '250 g', 23.00, 'veg'],
        ['Tofu gebraten', '180 g', 24.00, 'vegan'],
        ['Greenforce-Frikadellen', '150 g', 25.00, 'vegan'],
        ['Beyond Meat Burger', '150 g', 26.00, 'vegan'],
        ['Hausgemachte Käseravioli mit Bergkäse', '200 g', 27.00, 'veg'] ] },
    ],
    staerke: { k: 'Stärkebeilagen', nr: '02', items: [
      ['Nudeln', '180 g', 5.00, 'veg'], ['Reis', '180 g', 5.00, 'vegan'],
      ['Kartoffelstock', '200 g', 5.00, 'veg'], ['Bratkartoffeln', '180 g', 5.50, 'vegan'],
      ['Polenta', '150 g', 5.50, 'veg'], ['Kartoffelgratin', '200 g', 6.00, 'veg'],
      ['Gnocchi', '180 g', 6.00, 'veg'], ['Risotto', '180 g', 6.50, 'veg'] ] },
    gemuese: { k: 'Gemüse', nr: '03', items: [
      ['Karotten', '120 g', 4.50, 'vegan'], ['Brokkoli', '120 g', 5.00, 'vegan'],
      ['Bohnen', '120 g', 5.00, 'vegan'], ['Zucchini', '120 g', 5.00, 'vegan'],
      ['Saisonales Gemüse', '150 g', 5.50, 'vegan'], ['Grillgemüse', '140 g', 6.00, 'vegan'],
      ['Ratatouille', '160 g', 6.50, 'vegan'], ['Spargel', '150 g', 7.00, 'vegan'] ] },
    saucen: { k: 'Saucen', nr: '04', items: [
      ['Kräuterbutter', '', 1.50, 'veg'], ['Tomatensauce', '', 1.50, 'vegan'],
      ['Pfeffersauce', '', 2.00], ['Currysauce', '', 2.00, 'veg'],
      ['Senfsauce', '', 2.00, 'veg'], ['Pilzsauce', '', 2.50, 'veg'],
      ['Hollandaise', '', 2.50, 'veg'], ['Weinsauce', '', 2.50],
      ['Kräuterrahmsauce', '', 2.50, 'veg'], ['Champagnersauce', '', 3.00],
      ['Whisky-Sauce', '', 3.00] ] },
  };

  const BURGER = {
    id: 'burgerplausch', name: 'Burgerplausch',
    desc: 'Saftiges 220-g-Rindfleischpatty im Brioche-Bun.',
    inhalt: ['Salat, Gurken, Tomaten, Zwiebeln', 'Ketchup, Mayo, Tartarsauce'],
    preise: [['Burgerplausch', 18.00]], einheit: 'pro Portion',
    zusatz: [['Bacon', 2.00], ['Käse', 2.00]],
  };