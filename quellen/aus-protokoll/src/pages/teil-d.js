/* ==========================================================================
   WICK — Seiten 25–32
   Der Menü-Baukasten (Weg 03) · Grillplausch · Süsser Abschluss ·
   Dessert am Teller · Torten & Confiserie
   ========================================================================== */

(function () {
  const { IMG, W, N, KAP, kap, add, C, produkt, neuProdukt, neuIMG } = window.__W;
  const B = W.BAUKASTEN;

  /* Eine Spalte des Baukastens: Gruppentitel, dann Name · Gewicht · Preis. */
  const bgruppe = g => `<div class="ghead">${g.k}</div>${C.plist(
    g.items.map(([n2, gr, pr, d]) => [n2, gr, pr, d]), { head: false })}`;

  /* ======================================================================
     25 · Weg 03 — Ihr Menü in vier Schritten
     Die Seite, die den Baukasten erklärt, bevor die Listen kommen. Ohne
     sie sind die folgenden drei Seiten nur Preislisten.
     ====================================================================== */
  add({
    n: 25, chapter: 'Ihr eigenes<br>Menü', chapterCls: 'chapbox--s', ghost: 'Menü',
    chapnum: kap(4), hw: [1], kap: KAP[4].nr,
    band: IMG('Angerichteter Teller wird im Service weitergereicht, Abendlicht'),
    lead: `<b style="font-weight:400">Weg 03 — Sie stellen das Menü selbst zusammen.</b>
      ${B.intro} Vier Schritte, vier Preise, eine Summe. Auf den nächsten drei
      Seiten steht, was in jedem Schritt zur Wahl steht.`,
    body: C.panel(`
      <div style="position:absolute;left:17mm;right:14mm;top:24mm;bottom:8mm;
                  display:grid;grid-template-columns:1.5fr 1fr;column-gap:22mm">
        <div>
          <div class="sect">So gehen Sie vor</div>
          ${C.steps(B.schritte)}
          <div style="margin-top:5mm">${C.irows([
            ['person', 'Mindestmenge:', 'Zehn Personen. Darunter beraten wir Sie '
              + 'gerne persönlich — ein Menü für sechs Gäste ist möglich, aber '
              + 'keine Listenposition.'],
            ['clock', 'Dazu wählbar:', 'Suppe oder Vorspeise vorweg, Salat daneben, '
              + 'Dessert danach. Diese Gänge stehen in ihren eigenen Kapiteln.'],
          ], 'irows--static')}</div>
        </div>
        <div style="display:flex;flex-direction:column;justify-content:center">
          ${C.rechnung(B.beispiel)}
          <p style="margin:4mm 0 0;font-family:var(--font-slab);font-size:10pt;
                    line-height:1.3;color:var(--on-ink-dim)">
            So rechnet sich ein Menü zusammen — Zeile für Zeile, ohne
            Überraschung in der Offerte. Jede der vier Zeilen lässt sich
            tauschen, die Summe verschiebt sich entsprechend.</p>
          ${C.hand('vier Zeilen,\nein Preis',
                   'position:static;display:inline-block;margin:5mm 0 0 6mm')}
        </div>
      </div>`, '', 'height:118mm'),
    note: B.hinweise.join(' ') + ' ' + N.chf,
  });

  /* ======================================================================
     26 · Schritt 01 — Das Herzstück, Fleisch
     ====================================================================== */
  add({
    n: 26, ghost: '01', chapnum: kap(4), chapnumDark: true,
    hw: [1], kap: KAP[4].nr, band: false,
    k: { nr: 'Schritt 01 von 04', titel: 'Das Herzstück &middot; Fleisch',
         lead: 'Rind, Kalb und Schwein. Das Gewicht steht jeweils dabei — so '
             + 'sehen Sie, was auf dem Teller liegt, nicht nur was es kostet.' },
    body: C.panel(`
      <div style="position:absolute;left:17mm;right:14mm;top:9mm;bottom:8mm;
                  display:grid;grid-template-columns:1fr 1fr 1.12fr;column-gap:16mm">
        <div>${bgruppe(B.herzstueck[0])}</div>
        <div>${bgruppe(B.herzstueck[1])}</div>
        <div>${bgruppe(B.herzstueck[2])}</div>
      </div>`, 'panel--tall'),
    note: 'Preise pro Person, Gewicht roh gewogen. Weiter mit Geflügel, Fisch und '
        + 'Vegetarisch auf der nächsten Seite. ' + N.chf,
  });

  /* ======================================================================
     27 · Schritt 01 — Das Herzstück, Geflügel, Fisch und ohne Fleisch
     ====================================================================== */
  add({
    n: 27, ghost: '01', chapnum: kap(4), chapnumDark: true,
    hw: [1], kap: KAP[4].nr, band: false,
    k: { nr: 'Schritt 01 von 04', titel: 'Das Herzstück &middot; Geflügel, Fisch, ohne Fleisch',
         lead: 'Dieselbe Auswahlstufe, nur leichter. Die vegetarischen und veganen '
             + 'Positionen sind vollwertige Hauptgänge, keine Beilagen.' },
    body: C.shots([
      IMG('Pouletbrust mit saisonaler Füllung, angerichtet'),
      IMG('Lachsfilet auf dem Teller, Kräuter'),
      IMG('Saisonales Risotto im Teller, Aufsicht'),
      IMG('Hausgemachte Käseravioli mit Bergkäse'),
      IMG('Konfierte Entenschenkel, angerichtet'),
      IMG('Gebratener Tofu mit Gemüse'),
    ]) + C.panel(`
      <div style="position:absolute;left:17mm;right:14mm;top:24mm;bottom:8mm;
                  display:grid;grid-template-columns:1fr 1fr 1.15fr;column-gap:16mm">
        <div>${bgruppe(B.herzstueck[3])}</div>
        <div>${bgruppe(B.herzstueck[4])}</div>
        <div>${bgruppe(B.herzstueck[5])}
          <div style="margin-top:5mm">${C.irows([
            ['veg', 'Vollwertig:', 'Risotto, Ravioli und Tagliatelle brauchen keine '
              + 'zweite Beilage — hier genügen Schritt 03 und 04.'],
          ], 'irows--static')}</div>
        </div>
      </div>`, '', 'height:118mm'),
    note: 'Preise pro Person, Gewicht roh gewogen. ' + N.chf,
  });

  /* ======================================================================
     28 · Schritte 02 bis 04 — Beilage, Gemüse, Sauce
     ====================================================================== */
  add({
    n: 28, ghost: '02—04', chapnum: kap(4), chapnumDark: true,
    hw: [1], kap: KAP[4].nr, band: false,
    k: { nr: 'Schritt 02 bis 04 von 04', titel: 'Beilage, Gemüse und Sauce',
         lead: 'Die drei Schritte, die aus einem Stück Fleisch ein Menü machen. '
             + 'Aus derselben Auswahl wählen Sie auch die Beilagen zum Grillplausch.' },
    body: C.cols([
      C.col({ fs: 11, cap: '02 &middot; Stärkebeilage',
        body: `${C.plist(B.staerke.items.map(([n2, g, pr, d]) => [n2, g, pr, d]),
                         { head: false })}
          <p style="margin:4mm 0 0;color:var(--on-ink-dim)">Eine Stärkebeilage
          gehört zu jedem Menü — ausser das Herzstück bringt sie schon mit.</p>` }),
      C.col({ fs: 11, cap: '03 &middot; Gemüse',
        body: `${C.plist(B.gemuese.items.map(([n2, g, pr, d]) => [n2, g, pr, d]),
                         { head: false })}
          <p style="margin:4mm 0 0;color:var(--on-ink-dim)">Alles ohne tierische
          Zutaten zubereitet. Saisonales Gemüse heisst: was gerade aus der Region
          kommt.</p>` }),
      C.col({ fs: 11, cap: '04 &middot; Sauce',
        body: `${C.plist(B.saucen.items.map(([n2, g, pr, d]) => [n2, g, pr, d]),
                         { head: false })}` }),
      C.col({ fs: 10.5, cap: 'Und dann?',
        body: `${C.irows([
          ['clock', 'Rechnen:', 'Herzstück plus Beilage plus Gemüse plus Sauce — '
            + 'das ist der Preis pro Person. Das Rechenbeispiel steht auf Seite 25.'],
          ['flame', 'Am Grill:', 'Stärkebeilagen und Gemüse dieser Seite gelten '
            + 'auch für den Grillplausch auf der nächsten Seite.'],
          ['person', 'Service:', 'Am Teller serviert braucht es Personal. Die '
            + 'Ansätze stehen im Kapitel Material und Service.'],
          ['plate', 'Geschirr:', 'Teller, Besteck und Gläser können Sie bei uns '
            + 'mieten — oder Sie stellen Ihr eigenes.'],
        ], 'irows--static')}
        ${C.hand('jetzt steht\nIhr Menü',
                 'position:static;display:inline-block;margin:6mm 0 0 4mm')}` }),
    ], { h: 122 }),
    note: 'Alle Preise pro Person. ' + N.chf,
  });

  /* ======================================================================
     29 · Grillplausch
     ====================================================================== */
  const G = W.GRILL;
  add({
    n: 29, chapter: 'Grill-<br>plausch', chapterCls: 'chapbox--s', ghost: 'Grill',
    chapnum: kap(4), hw: [1], kap: KAP[4].nr,
    band: IMG('Grillplatte mit mariniertem Fleisch, Aufsicht'),
    lead: `<b style="font-weight:400">Mariniert aus unserer Küche, fertig zum
      Auflegen.</b> ${G.intro}`,
    body: C.cols(G.platten.map(pt => C.col({
      fs: 11,
      shot: IMG(`Grillplatte ${pt.name}, Aufsicht`),
      body: produkt({
        name: `Grillplatte ${pt.name}`, klein: true,
        badges: pt.tag === 'veg' ? ['veg'] : undefined,
        body: `<div style="margin-top:3mm">${pt.inhalt.map(x => `&bull; ${x}`).join('<br>')}</div>`,
        preise: pt.preise.map(([k, g, p]) => [k, g + ' pro Person', p]),
      }),
    })).concat([
      C.col({ fs: 10.5, cap: 'Dazu',
        body: `<p style="margin:0 0 3mm">${G.verweis}</p>
          <div class="ghead">Saucen im Portionentöpfli</div>
          ${C.plist(G.saucen, { head: false })}
          <div style="margin-top:4mm">${C.irows([
            ['flame', 'Material:', G.material],
            ['person', 'Menge:', 'Grillplatten ab 20 Personen.'],
          ], 'irows--static')}</div>
          <div style="margin-top:4mm;color:var(--sand-pale)">
            Ideal für Baustellenaufrichtungen, Vereinsanlässe und Geburtstage
            im Freien.</div>` }),
    ]), { h: 118 }),
    note: G.hinweis + ' ' + N.chf,
  });

  /* ======================================================================
     30 · Der süsse Abschluss — fürs Buffet
     ====================================================================== */
  const S = W.SUESSES;
  const mp = S.buffet[0];
  const suessKarte = x => `<div class="pname">${x.name}</div>${
    C.badges((x.badges || []).concat(x.tag ? [x.tag] : []))}
    <div style="font-family:var(--font-slab);font-size:10.5pt;line-height:1.3;
                margin-top:1.5mm">${x.desc || ''}</div>
    ${x.sorten ? `<div style="margin-top:1.8mm;font-family:var(--font-slab);
        font-size:10pt;line-height:1.3;color:var(--on-ink-dim)">${C.dots(x.sorten)}</div>` : ''}
    ${x.basis ? `<div style="margin-top:1.4mm;font-family:var(--font-slab);
        font-size:10pt;color:var(--on-ink-dim)"><b>Basis:</b> ${C.dots(x.basis)}</div>` : ''}
    ${x.preise
      ? `<div style="margin-top:2.2mm">${C.plist(
          x.preise.map(([k, p]) => [k, '', p]), { head: false })}</div>`
      : `<div style="margin-top:2.2mm">${C.plist(
          [[`CHF ${C.chf(x.preis)}`, x.einheit || 'pro Stück', '']], { head: false })}</div>`}`;

  add({
    n: 30, chapter: 'Süsser<br>Abschluss', chapterCls: 'chapbox--s', ghost: 'Süsses',
    chapnum: kap(4), hw: [2, 3], kap: KAP[4].nr,
    band: IMG('Mini-Pâtisserie in Reihen, Aufsicht, Konditorei'),
    lead: `<b style="font-weight:400">Vom Apéro bis zur Torte kommt bei Wick alles
      aus einer Hand.</b> Diese Seite zeigt, was aufs Buffet kommt und aus der
      Hand gegessen wird. Serviert am Platz steht auf der nächsten Seite. Alles
      entsteht in unserer eigenen Konditorei.`,
    body: C.shots([
      IMG('Roulade Zitrone'), IMG('Passionsfruchtmousse'),
      IMG('Schwarzwälderschnitte'), IMG('Cake Pops, Reihe auf Stielen'),
      neuIMG('schoggicornet-bissen'), neuIMG('vermicelles-toertchen'),
    ]) + C.panel(`
      <div style="position:absolute;left:17mm;right:14mm;top:24mm;bottom:8mm;
                  display:grid;grid-template-columns:1.25fr 1fr 1fr 0.92fr;column-gap:14mm">
        <div>
          <div class="pname">${mp.name}</div>${C.badges(mp.badges.concat([mp.tag]))}
          <div style="font-family:var(--font-slab);font-size:10.5pt;line-height:1.3;
                      margin-top:1.5mm">${mp.desc}</div>
          <div style="font-family:var(--font-slab);font-size:10pt;line-height:1.3;
                      margin-top:2mm">
            ${Object.entries(mp.gruppen).map(([k, v]) =>
              `<div style="margin-top:1.6mm"><b>${k}:</b> ${C.dots(v)}</div>`).join('')}
          </div>
          <div style="margin-top:2.4mm">${C.plist(
            [[`CHF ${C.chf(mp.preis)}`, 'pro Stück', '']], { head: false })}</div>
        </div>
        <div>${suessKarte(S.buffet[1])}
          <div style="margin-top:5mm">${suessKarte(S.buffet[2])}</div></div>
        <div>${suessKarte(S.buffet[3])}
          <div style="margin-top:5mm">${suessKarte(S.buffet[4])}</div></div>
        <div>${suessKarte(S.buffet[5])}
          <div style="margin-top:4mm">${C.plist([
            [S.buffet[6].name, 'pro Stück', S.buffet[6].preis],
            [S.buffet[7].name, 'pro Stück', S.buffet[7].preis],
            [S.buffet[8].name, 'pro Portion', S.buffet[8].preis, 'vegan'],
          ], { head: false })}</div>
          <div style="margin-top:4mm"><div class="ghead">${S.vegan.titel}</div>
            <div style="font-family:var(--font-slab);font-size:10pt;line-height:1.3;
                        color:var(--on-ink-dim)">${C.dots(S.vegan.sorten)}</div>
            ${C.plist([[`CHF ${C.chf(S.vegan.preis)}`, S.vegan.einheit, '']],
                      { head: false })}</div>
        </div>
      </div>
      ${C.coins([C.coin(mp.preis, 'CHF/St.')])}`, '', 'height:118mm'),
    note: 'Mindestmenge: ' + S.minText + ' ' + N.neu,
  });

  /* ======================================================================
     31 · Dessert am Teller
     ====================================================================== */
  const DT = S.teller;
  add({
    n: 31, ghost: 'Dessert', chapnum: kap(4), chapnumDark: true,
    hw: [2, 3], kap: KAP[4].nr, band: false,
    k: { nr: 'Kapitel 04 / 06', titel: 'Dessert am Teller',
         lead: 'Wird am Platz serviert und gehört deshalb zum Tellerservice — '
             + 'wie das eigene Menü auf den Seiten 25 bis 28.' },
    body: C.cols([
      C.col({ fs: 11, cap: 'Die Auswahl',
        body: `<p style="margin:0 0 3mm;color:var(--on-ink-dim)">${DT.desc}</p>
          ${C.plist(DT.items.slice(0, 6).map(([n2, pr, d, s]) => [n2, s || '', pr, d]),
                    { head: false })}` }),
      C.col({ fs: 11, cap: 'Fortsetzung',
        body: C.plist(DT.items.slice(6).map(([n2, pr, d, s]) => [n2, s || '', pr, d]),
                      { head: false }) }),
      C.col({ fs: 10.5, cap: 'Was wann passt',
        body: `${C.irows([
          ['person', 'Ab 20 Personen:', 'Unter zwanzig Gästen lohnt sich der '
            + 'Tellerservice nicht — dann empfehlen wir die Mini-Pâtisserie '
            + 'von Seite 30.'],
          ['clock', 'Nach dem Menü:', 'Ein Dessert am Teller schliesst einen Abend '
            + 'ab, an dem auch der Hauptgang serviert wurde. Zum Buffet passt '
            + 'besser ein süsses Buffet.'],
          ['veg', 'Ohne Tierisches:', 'Die Früchtevariation und das Zitronensorbet '
            + 'sind vegan. Weitere vegane Desserts stehen auf Seite 30.'],
          ['cake', 'Statt Dessert:', 'An Hochzeiten und Geburtstagen ersetzt oft '
            + 'die Torte den Dessertgang — siehe nächste Seite.'],
        ], 'irows--static')}
        ${C.hand('der letzte\nEindruck bleibt',
                 'position:static;display:inline-block;margin:6mm 0 0 4mm')}` }),
    ], { h: 118 }),
    note: 'Alle Preise pro Portion, Tellerservice ab 20 Personen. ' + N.chf,
  });

  /* ======================================================================
     32 · Torten & Confiserie
     Cupcakes, Cake Pops und Mousse stehen neu bei den Buffetdesserts —
     diese Seite gehört dem, was andere Caterer zukaufen müssen.
     ====================================================================== */
  add({
    n: 32, chapter: 'Torten &<br>Confiserie', chapterCls: 'chapbox--s', ghost: 'Torten',
    chapnum: kap(4), hw: [2, 3], kap: KAP[4].nr,
    band: IMG('Hochzeitstorte, Konditorin beim Garnieren'),
    lead: `<b style="font-weight:400">Eine Torte kauft man nicht ein, man bespricht
      sie.</b> Konditorei, Tortenhandwerk und Confiserie sind drei der sechs
      Handwerke in unserem Haus — der Teil, den andere Cateringbetriebe zukaufen
      müssen. Was daraus wird, entscheiden Sie mit uns am Tisch.`,
    body: C.shots([
      IMG('Hochzeitstorte mehrstöckig, Detail'),
      IMG('Torte mit Wunschmotiv, Aufsicht'),
      IMG('Vegane Torte, angeschnitten'),
      IMG('Pralinen von Hand garniert, Confiserie'),
      IMG('Schokoladentafeln aus eigener Herstellung'),
      IMG('Cup Cakes in Pastellfarben'),
    ]) + C.panel(`
      <div style="position:absolute;left:17mm;right:14mm;top:24mm;bottom:8mm;
                  display:grid;grid-template-columns:1.1fr 1fr 1fr;column-gap:20mm">
        <div>
          <div class="sect">Torten nach Ihrer Idee</div>
          <div style="font-family:var(--font-slab);font-size:11pt;line-height:1.32">
            ${S.torten.hinweis}</div>
          <div style="margin-top:3.5mm"><div class="ghead">Auch vegan</div>
            <div style="font-family:var(--font-slab);font-size:10.5pt;line-height:1.42">
              ${S.torten.veganeSorten.map(x => `&bull; ${x}`).join('<br>')}</div></div>
          ${C.hand('das Stück, an das\nsich alle erinnern',
                   'position:static;display:inline-block;margin:6mm 0 0 3mm')}
        </div>
        <div>
          <div class="sect">Confiserie</div>
          <div style="font-family:var(--font-slab);font-size:11pt;line-height:1.32">
            Pralinen und Schokolade aus eigener Herstellung, mit GrandCru-Couverture
            von Felchlin. Als Gastgeschenk am Platz, zum Kaffee oder als Dankeschön
            für die Helferinnen und Helfer.</div>
          <div style="margin-top:4mm">${C.irows([
            ['cake', 'Gastgeschenk:', 'Pralinen in kleinen Schachteln, auf Wunsch '
              + 'mit Ihrem Datum oder Ihrem Logo.'],
            ['person', 'Beratung:', 'Motiv, Grösse und Geschmack besprechen wir '
              + 'persönlich — daraus entsteht die Offerte.'],
          ], 'irows--static')}</div>
        </div>
        <div>
          <div class="sect">Was sonst noch süss ist</div>
          <div style="font-family:var(--font-slab);font-size:11pt;line-height:1.32;
                      color:var(--on-ink-dim)">
            Mini-Pâtisserie, Cup Cakes, Cake Pops, Mousse-Schalen und die
            Frucht-Spiessli stehen beim süssen Abschluss auf Seite 30. Die
            Desserts für den Tellerservice auf Seite 31.</div>
          <div style="margin-top:4mm">${C.plist([
            ['Cup Cakes mit Logo oder Wunschdesign', 'pro Stück',
             S.buffet[3].preise[1][1], 'veg'],
            ['Cake Pops mit Alkohol', 'pro Stück', S.buffet[4].preise[1][1]],
          ], { head: false })}</div>
          <div style="margin-top:3mm;font-family:var(--font-slab);font-size:10pt;
                      line-height:1.3;color:var(--on-ink-dim)">
            Für Torten nennt unsere Preisliste bewusst keinen Betrag — Grösse,
            Motiv und Aufwand sind zu verschieden. Sie erhalten eine Offerte.</div>
        </div>
      </div>`, '', 'height:118mm'),
    note: 'Torten fertigen wir nach Offerte. ' + N.chf,
  });
})();