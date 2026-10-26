
  /* ======================================================================
     20 · Warme Küche  ·  Übergang und Wegweiser
     Diese Seite trägt das ganze Kapitel: Sie sagt dem Kunden, welche der
     drei Formen zu seinem Anlass passt, bevor er eine einzige Preisliste
     sieht.
     ====================================================================== */
  add({
    n: 20, ink: true, ghost: 'Küche', chapnum: false,
    hw: [1], kap: KAP[4].nr, band: {}, scrim: false,
    raw: C.statement({
      eyebrow: 'Kapitel 04 / 06 &nbsp;&middot;&nbsp; Warme Küche',
      title: 'Wir liefern nicht nur Apérogebäck.<br><em>Wir kochen für Ihren Anlass.</em>',
      text: 'Dieselbe Küche, die am ESAF 80’000 Mahlzeiten produziert hat, kocht auch '
          + 'für dreissig Gäste. Drei Wege führen dorthin — welcher passt, hängt an '
          + 'der Gästezahl und daran, wie serviert wird.',
    }).replace('class="statement"', 'class="statement statement--band"'),
    body: C.panel(C.wege(W.WEGE), '', 'height:96mm'),
    note: 'Suppe, Salat und Dessert wählen Sie unabhängig davon — sie passen zu '
        + 'allen drei Wegen. ' + N.chf,
  });

  /* ======================================================================
     21 · Der warme Auftakt — Suppen & Vorspeisen
     ====================================================================== */
  const SU = W.SUPPEN, VS = W.VORSPEISEN;
  add({
    n: 21, chapter: 'Warmer<br>Auftakt', chapterCls: 'chapbox--s', ghost: 'Auftakt',
    chapnum: kap(4), hw: [1], kap: KAP[4].nr,
    band: IMG('Suppentopf wird an der Ausgabe geschöpft, Dampf, Abendlicht'),
    lead: `<b style="font-weight:400">Eine Suppe kostet wenig und verändert viel.</b>
      Sie wärmt Gäste, die draussen gestanden haben, sie überbrückt die Zeit bis zum
      Hauptgang, und sie lässt sich in jeder Menge transportieren. Die Vorspeisen
      daneben sind für Anlässe gedacht, an denen am Tisch serviert wird.`,
    body: C.shots([
      IMG('Kürbissuppe im Teller, Aufsicht'),
      IMG('Bündner Gerstensuppe im Topf'),
      IMG('Suppe im Gläsli als Fingerfood'),
      IMG('Lachstatar mit Thai-Salsa, angerichtet'),
      IMG('Burrata mit Tomaten und Basilikum'),
      IMG('Hausgemachte Käseravioli, warm angerichtet'),
    ]) + C.panel(`
      <div style="position:absolute;left:17mm;right:14mm;top:24mm;bottom:8mm;
                  display:grid;grid-template-columns:1.9fr 1.5fr;column-gap:18mm">
        <div>
          <div class="cap"><span>Suppen</span></div>
          <div style="display:grid;grid-template-columns:1fr 1fr;column-gap:12mm;
                      margin-top:3mm">
            <div>${SU.gruppen.slice(0, 1).map(g =>
              `<div class="ghead">${g.k}</div>${C.plist(
                g.items.map(([n2, pr, d]) => [n2, '', pr === null ? '' : pr, d]),
                { head: false })}`).join('')}</div>
            <div>${SU.gruppen.slice(1).map(g =>
              `<div class="ghead">${g.k}</div>${C.plist(
                g.items.map(([n2, pr, d]) => [n2, '', pr === null ? '' : pr, d]),
                { head: false })}`).join('')}</div>
          </div>
          <div style="margin-top:3.5mm;font-family:var(--font-slab);font-size:10pt;
                      line-height:1.3;color:var(--on-ink-dim)">
            ${SU.hinweis}<br>${SU.fingerfood}</div>
        </div>
        <div>
          <div class="cap"><span>Vorspeisen am Teller</span></div>
          <p style="margin:3mm 0 3mm;font-family:var(--font-slab);font-size:10.5pt;
                    line-height:1.3;color:var(--on-ink-dim)">${VS.intro}</p>
          ${VS.gruppen.map(g =>
            `<div class="ghead">${g.k}</div>${C.plist(
              g.items.map(([n2, pr, d, s]) => [n2, s || '', pr, d]),
              { head: false })}`).join('')}
        </div>
      </div>`, '', 'height:118mm'),
    note: 'Alle Preise pro Portion. Bei der Bündner Gerstensuppe nennt unsere '
        + 'Preisliste keinen Betrag — wir offerieren sie gerne. ' + N.chf,
  });

  /* ======================================================================
     22 · Salate
     ====================================================================== */
  const SA = W.SALATE;
  add({
    n: 22, ghost: 'Salate', chapnum: kap(4), chapnumDark: true,
    hw: [1], kap: KAP[4].nr, band: false,
    k: { nr: 'Kapitel 04 / 06', titel: 'Salate',
         lead: 'Am Teller angerichtet oder als Buffet, bei dem Sie bestimmen, wie '
             + 'viele Sorten daraufkommen.' },
    body: C.cols([
      C.col({ fs: 10.5, cap: SA.teller.titel,
        body: `<p style="margin:0 0 3mm;color:var(--on-ink-dim)">${SA.teller.desc}</p>
          ${C.plist(SA.teller.items.map(([n2, pr, d, s]) => [n2, s || '', pr, d]),
                    { head: false })}
          <p style="margin:3.5mm 0 0;color:var(--on-ink-dim)">Preise pro Portion.
          Die saisonalen Salate gibt es, solange die Zutaten aus der Region
          kommen.</p>` }),
      C.col({ fs: 10.5, cap: SA.buffet.titel,
        body: `<p style="margin:0 0 3mm;color:var(--on-ink-dim)">${SA.buffet.desc}</p>
          ${C.plist(SA.buffet.stufen.map(([n2, ab, pr]) => ({
            n: n2, sub: ab, u: 'ab', p: pr })), { head: false })}
          <p style="margin:3.5mm 0 0;color:var(--on-ink-dim)">Preise pro Person.
          Je mehr Gäste, desto mehr Sorten lassen sich wirtschaftlich
          zubereiten — deshalb die Staffelung.</p>
          ${C.hand('fast immer die\nrichtige Ergänzung',
                   'position:static;display:inline-block;margin:6mm 0 0 4mm')}` }),
      C.col({ fs: 10, cap: SA.sorten.titel, span: 2,
        body: `<div style="column-count:2;column-gap:14mm">
          ${SA.sorten.gruppen.map(g =>
            `<div style="break-inside:avoid"><div class="ghead">${g.nr} &nbsp;${g.k}</div>
             <div style="font-family:var(--font-slab);font-size:10.5pt;line-height:1.5">
               ${g.items.map(([n2, d]) => `${n2}${C.dt(d)}`).join('<br>')}</div></div>`).join('')}
          </div>` }),
    ], { h: 122 }),
    note: 'Zum Salatbuffet servieren wir unsere zwei hausgemachten Saucen, French '
        + 'und Italian. ' + N.chf,
  });

  /* ======================================================================
     23 · Weg 01 — Unsere Buffets
     ====================================================================== */
  const BU = W.BUFFETS;
  add({
    n: 23, chapter: 'Unsere<br>Buffets', chapterCls: 'chapbox--s', ghost: 'Buffet',
    chapnum: kap(4), hw: [1], kap: KAP[4].nr,
    band: IMG('Warmes Buffet in Chafing Dishes, Gäste schöpfen, Abendlicht'),
    lead: `<b style="font-weight:400">Weg 01 — fertig zusammengestellt.</b>
      ${BU.intro} Jedes dieser sechs Buffets ist an Anlässen entstanden, die wir
      wirklich gemacht haben; die Namen erinnern uns daran, wo.`,
    body: C.cols(BU.items.map(b => C.col({ fs: 10.5, body: C.buffetkarte(b) })),
                 { h: 118 }),
    note: BU.hinweis + ' Preise pro Person. ' + N.chf,
  });

  /* ======================================================================
     24 · Weg 02 — Klassiker für grosse Runden
     ====================================================================== */
  const KL = W.KLASSIKER;
  add({
    n: 24, ghost: 'Klassiker', chapnum: kap(4), chapnumDark: true,
    hw: [1], kap: KAP[4].nr, band: false,
    k: { nr: 'Kapitel 04 / 06', titel: 'Klassiker für grosse Runden',
         lead: 'Weg 02 — ein Gericht, eine Menge, ein Preis. Das ist die Form, '
             + 'mit der wir am ESAF 80’000 Mahlzeiten ausgegeben haben.' },
    body: C.shots([
      IMG('Ghackets mit Hörnli und Apfelmus, Teller'),
      IMG('Rindfleisch-Lasagne aus dem Ofen, angeschnitten'),
      IMG('Chili con Carne im Topf, Ausgabe'),
      IMG('Poulet-Thai-Curry mit Jasminreis'),
      IMG('Schmorbraten mit Kartoffelstock'),
      IMG('Warmer Schinken mit Kartoffelsalat'),
    ]) + C.panel(`
      <div style="position:absolute;left:17mm;right:14mm;top:24mm;bottom:8mm;
                  display:grid;grid-template-columns:1fr 1fr 0.78fr;column-gap:16mm">
        <div>${C.plist(KL.items.slice(0, 6).map(it => ({
          n: it.name, sub: it.zutaten, p: it.preis, d: it.tag })), { head: false })}</div>
        <div>${C.plist(KL.items.slice(6).map(it => ({
          n: it.name, sub: it.zutaten, p: it.preis, d: it.tag })), { head: false })}</div>
        <div>${C.irows([
          ['person', 'Menge:', 'Ein Gericht deckt den ganzen Anlass. Zwei Gerichte '
            + 'geben den Gästen die Wahl — dann rechnen wir mit 60 zu 40.'],
          ['flame', 'Ausgabe:', 'Wir liefern im Wärmebehälter oder richten vor Ort '
            + 'an. Beides funktioniert auch, wo keine Küche steht.'],
          ['veg', 'Ohne Fleisch:', 'Chili sin Carne und das Gemüse-Thai-Curry sind '
            + 'vollwertig vegan — keine Beilage, sondern ein Hauptgang.'],
          ['clock', 'Dazu passt:', 'Eine Suppe vorweg, ein Salatbuffet daneben, '
            + 'Mini-Pâtisserie danach.'],
        ], 'irows--static')}
        ${C.hand('in jeder Menge\nerprobt', 'position:static;display:inline-block;margin:5mm 0 0 4mm')}
        </div>
      </div>`, '', 'height:118mm'),
    note: 'Alle Preise pro Portion. ' + N.chf,
  });
})();