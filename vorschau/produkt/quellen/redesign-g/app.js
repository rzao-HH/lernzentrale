class Component extends DCLogic {
  constructor(p) {
    super(p);
    this.state = {
      scr: 'heute', back: 'fach', sheet: null, sp: 3, sv: 'mess',
      h: { 1: 3, 2: 3, 3: 1, 4: 0, 5: 2, 6: 0, 7: 0, 8: 0 }, due: { 1: true }, gained: 0,
      points: 432, done: 1, ziel: 3, doneR: {},
      r: null, ti: 0, sel: -1, inp: '', ph: 'ask', tr: 1, t0: 0, log: [], fastRun: 0, pause: false, me: 0, kr: 0,
      res: null, fsel: [3, 1, 2], fmod: 'messen', lenk: 'ausgewogen', wp: 4, wmode: 'read'
    };
  }

  /* ---------- feste Daten ---------- */
  I() { return __ICON__; }
  PK() {
    return {
      1: { nr: 1, name: 'Spitz & Recht', short: 'Spitz', grp: 'A', col: '#5B8DEF', inD: 0, src: 'AH S. 13–14', goal: 'Ich erkenne spitze Winkel (zwischen 0° und 90°) und rechte Winkel (90°) und kann sie mit dem Geodreieck messen.' },
      2: { nr: 2, name: 'Stumpf & Gestreckt', short: 'Stumpf', grp: 'A', col: '#9B6BE8', inD: 3, src: 'AH S. 13–14', goal: 'Ich erkenne stumpfe Winkel (zwischen 90° und 180°) und gestreckte Winkel (180°) und kann sie messen.' },
      3: { nr: 3, name: 'Überstumpf', short: 'Überstumpf', grp: 'A', col: '#E0567F', inD: 0, src: 'AH S. 13–14', goal: 'Ich erkenne überstumpfe Winkel (zwischen 180° und 360°) und messe sie mit dem Trick „360° minus Innenwinkel“.' },
      4: { nr: 4, name: 'Null, Voll & Grenzfälle', short: 'Grenzfälle', grp: 'A', col: '#239C8E', inD: 0, src: 'AH S. 13–14 · ml S. 39', goal: 'Ich kenne Nullwinkel (0°) und Vollwinkel (360°) und ordne Grenzfälle wie 89°, 91° oder 179° sicher ein.' },
      5: { nr: 5, name: 'Kompass & Kurs', short: 'Kompass', grp: 'B', col: '#D9862A', inD: 0, src: 'ml S. 36–37', goal: 'Ich lese Drehungen am Kompass ab, kenne die Himmelsrichtungen in Grad und bestimme einen Kurs von A nach B.' },
      6: { nr: 6, name: 'Winkel benennen', short: 'Benennen', grp: 'B', col: '#4E9A35', inD: 0, src: 'Infoblätter Der Winkel', goal: 'Ich benenne Scheitel, Schenkel und Winkelbogen und kenne α, β, γ, δ, ε.' },
      7: { nr: 7, name: 'Winkel berechnen', short: 'Berechnen', grp: 'B', col: '#C95A3E', inD: 0, src: 'ml S. 41–42', goal: 'Ich berechne Winkel ohne zu messen: Nebenwinkel, Vollkreis, Scheitelwinkel, Dreieck.' },
      8: { nr: 8, name: 'Senkrechte & Parallelen', short: 'Senkrecht', grp: 'B', col: '#2F8CC4', inD: 0, src: 'Übungsheft Geodreieck', goal: 'Ich erkenne senkrechte und parallele Geraden und zeichne sie durch einen Punkt.' }
    };
  }
  R() {
    const ART = ['Winkelart erkennen'];
    return {
      mess: {
        id: 'mess', tag: 'Weiterkommen', tagBg: '#FFC83D', title: 'Überstumpf selbst messen', mod: 'Messen mit Geodreieck', icon: 'geo', art: 'selbst',
        packs: [3, 1, 2], mix: [[3, 5], [1, 3], [2, 2]], total: 10, min: 6, hk: 'pencil', goal: 'Können-Haken für Paket 3',
        coinSub: 'volle Punkte, +20 % gemischt', coinBg: '#FFE7A3',
        why: 'Überstumpf erkennst du schon. Jetzt misst du selbst, dafür gibt es den Können-Haken. Paket 1 ist wieder dran und kommt gemischt dazu, wie in der Arbeit.',
        pre: [[3, 1], [1, 1], [3, 1], [2, 1], [3, 0], [1, 1], [3, 1], [2, 1]],
        tasks: [
          { p: 3, k: 'num', a: 250, ans: 250, tol: 2, lab: '?', q: 'Wie groß ist der Winkel?', sub: 'Miss mit dem Geodreieck und tippe die Gradzahl ein.', hint: 'Überstumpf heißt: größer als 180°. Miss den kleinen Winkel innen und rechne 360° minus diesen Winkel.', ex: 'Innen sind es 110°. 360° − 110° = 250°. Ein überstumpfer Winkel.' },
          { p: 1, k: 'num', a: 40, ans: 40, tol: 2, lab: '?', q: 'Wie groß ist der Winkel?', sub: 'Miss und tippe die Gradzahl ein.', hint: 'Mitte des Geodreiecks auf den Scheitel, lange Kante auf den unteren Schenkel. An der inneren Skala ablesen.', ex: 'Der Winkel hat 40°. Er ist spitz, also kleiner als 90°.' }
        ]
      },
      neu: {
        id: 'neu', tag: 'Neues Paket', tagBg: '#BDEBE4', title: 'Grenzfälle kennenlernen', mod: ART[0], icon: 'eye', art: 'tippen',
        packs: [4], mix: [[4, 5]], total: 5, min: 4, hk: 'eye', goal: 'Kennen-Haken für Paket 4', wissen: true,
        coinSub: 'volle Punkte, neu', coinBg: '#E6F6F3',
        why: 'Ein neues Paket lernst du zuerst allein kennen: kurz lesen, dann 5 Fragen mit Auswahl. Selbst messen kommt danach.',
        pre: [],
        tasks: [
          { p: 4, k: 'tap', a: 360, lab: '360°', q: 'Welche Winkelart ist das?', sub: 'Der Winkel hat 360°.', opt: ['Nullwinkel', 'Gestreckter Winkel', 'Vollwinkel', 'Überstumpfer Winkel'], ans: 2, ex: 'Einmal ganz herum sind 360°. Das ist ein Vollwinkel.' },
          { p: 4, k: 'tap', a: 0, lab: '0°', q: 'Beide Schenkel liegen genau aufeinander. Wie heißt der Winkel?', sub: '', opt: ['Nullwinkel', 'Spitzer Winkel', 'Vollwinkel', 'Rechter Winkel'], ans: 0, ex: '0° heißt Nullwinkel. Die Schenkel liegen aufeinander.' },
          { p: 4, k: 'tap', a: 89, lab: '89°', q: 'Welche Winkelart hat 89°?', sub: 'Knapp unter 90°.', opt: ['Spitzer Winkel', 'Rechter Winkel', 'Stumpfer Winkel', 'Gestreckter Winkel'], ans: 0, ex: 'Alles unter 90° ist spitz, auch 89°.' },
          { p: 4, k: 'tap', a: 181, lab: '181°', q: 'Welche Winkelart hat 181°?', sub: 'Knapp über 180°.', opt: ['Stumpfer Winkel', 'Gestreckter Winkel', 'Überstumpfer Winkel', 'Vollwinkel'], ans: 2, ex: 'Über 180° ist überstumpf, auch wenn es nur 1° mehr ist.' },
          { p: 4, k: 'tap', a: 179, lab: '179°', q: 'Welche Winkelart hat 179°?', sub: 'Knapp unter 180°.', opt: ['Stumpfer Winkel', 'Gestreckter Winkel', 'Überstumpfer Winkel', 'Rechter Winkel'], ans: 0, ex: 'Zwischen 90° und 180° ist stumpf. 179° ist also noch stumpf.' }
        ]
      },
      blitz: {
        id: 'blitz', tag: 'Spielerisch', tagBg: '#E7DDFF', title: 'Blitz-Duell gegen Krabbi', mod: 'Blitz-Duell', icon: 'bolt', art: 'tippen',
        packs: [1, 2, 3], mix: [[1, 2], [2, 2], [3, 1]], total: 5, min: 3, hk: 'star', goal: 'kein neuer Haken, dafür Spaß', duel: true,
        coinSub: 'wenig, du kennst alles schon', coinBg: '#EEEAF7',
        why: 'Ein Spiel mit Paketen, die du schon kennst. Antippen ist für dich jetzt leicht, darum gibt es hier weniger Punkte.',
        pre: [], kw: [1, 0, 1, 1, 0],
        tasks: [
          { p: 1, k: 'tap', a: 60, lab: '', q: 'Welche Winkelart ist das?', sub: 'Schnell, aber erst hinschauen!', opt: ['Spitz', 'Recht', 'Stumpf', 'Gestreckt'], ans: 0, ex: '60° ist kleiner als 90°: spitz.' },
          { p: 2, k: 'tap', a: 125, lab: '', q: 'Welche Winkelart ist das?', sub: '', opt: ['Spitz', 'Recht', 'Stumpf', 'Überstumpf'], ans: 2, ex: 'Zwischen 90° und 180°: stumpf.' },
          { p: 3, k: 'tap', a: 300, lab: '', q: 'Welche Winkelart ist das?', sub: '', opt: ['Stumpf', 'Gestreckt', 'Überstumpf', 'Voll'], ans: 2, ex: 'Größer als 180°: überstumpf.' },
          { p: 1, k: 'tap', a: 90, lab: '', q: 'Welche Winkelart ist das?', sub: '', opt: ['Spitz', 'Recht', 'Stumpf', 'Gestreckt'], ans: 1, ex: 'Genau 90°: ein rechter Winkel.' },
          { p: 2, k: 'tap', a: 180, lab: '', q: 'Welche Winkelart ist das?', sub: '', opt: ['Stumpf', 'Gestreckt', 'Überstumpf', 'Voll'], ans: 1, ex: 'Eine gerade Linie, 180°: gestreckt.' }
        ]
      }
    };
  }
  MODS() {
    return [
      { id: 'wissen', t: 'Wissen lesen', icon: 'book', art: 'lesen', fit: 'all' },
      { id: 'erkennen', t: 'Winkelart erkennen', icon: 'eye', art: 'tippen', fit: 'A' },
      { id: 'grad', t: 'Gradzahl einordnen', icon: 'tap', art: 'tippen', fit: 'A' },
      { id: 'messen', t: 'Messen mit Geodreieck', icon: 'geo', art: 'selbst', fit: 'A' },
      { id: 'zeichnen', t: 'Winkel zeichnen', icon: 'draw', art: 'selbst', fit: 'A' },
      { id: 'schaetzen', t: 'Schätzen', icon: 'target', art: 'selbst', fit: 'A' },
      { id: 'mission', t: 'Aufgaben-Mission', icon: 'compass', art: 'selbst', fit: 'B' },
      { id: 'blitz', t: 'Blitz-Duell gegen Krabbi', icon: 'bolt', art: 'tippen', fit: 'all' },
      { id: 'test', t: 'Abschlusstest', icon: 'trophy', art: 'test', fit: 'all' }
    ];
  }
  RANKS() { return [['staub', 'Sternenstaub', 0], ['meteor', 'Meteor', 100], ['komet', 'Komet', 250], ['planet', 'Planet', 500], ['pulsar', 'Pulsar', 850], ['supernova', 'Supernova', 1300], ['galaxis', 'Galaxis-Legende', 2000]]; }

  /* ---------- Rechnen ---------- */
  word(h) { return h === 0 ? 'neu' : h >= 3 ? 'sicher' : 'noch üben'; }
  dez(x) { return String(x).replace('.', ','); }
  per(id, art, mixed) {
    const s = this.state, h = s.h[id], base = { tippen: 4, ordnen: 6, selbst: 10 }[art] || 0;
    if (!base) return { v: 0, why: [] };
    let f = 1; const why = [art === 'selbst' ? '10 fürs Selbstmachen' : '4 fürs Antippen'];
    if (h >= 3 && !s.due[id]) { f *= 0.15; why.push('kannst du schon: ×0,15'); }
    else if (h === 0) why.push('neu: volle Punkte');
    else if (s.due[id]) why.push('wieder dran: volle Punkte');
    else why.push('noch üben: volle Punkte');
    if (art === 'tippen' && h >= 2) { f *= 0.5; why.push('Antippen ist für dich leicht: ×0,5'); }
    if (h === 0 && s.lenk !== 'frei') {
      const only = Object.keys(s.h).filter((k) => +k !== id && s.h[k] === 1).length;
      if (only >= 2) { f *= 0.5; why.push('erst ein anderes Paket selbst machen: ×0,5'); }
    }
    if (mixed) { f *= 1.2; why.push('gemischt: +20 %'); }
    f = Math.min(f, 1.5);
    return { v: Math.max(1, Math.round(base * f)), why };
  }
  tok(id, extra) {
    const s = this.state, P = this.PK()[id], h = s.h[id];
    const o = { id, nr: P.nr, name: P.name, short: P.short, col: P.col, word: this.word(h), due: !!s.due[id], aria: 'Paket ' + P.nr + ', ' + P.name + ', ' + this.word(h) + (s.due[id] ? ', wieder dran' : '') };
    [0, 1, 2].forEach((i) => { const on = i < h; o['c' + i] = on ? '#F2B517' : '#A9A396'; o['w' + i] = on ? 6 : 2.5; o['d' + i] = on ? 'none' : '3 4'; });
    return Object.assign(o, extra || {});
  }
  fig(a, W, H, cx, cy, L, r, lab) {
    const rad = (d) => d * Math.PI / 180, x = (d, rr) => (cx + rr * Math.cos(rad(d))).toFixed(1), y = (d, rr) => (cy - rr * Math.sin(rad(d))).toFixed(1);
    let arc = '';
    if (a >= 360) arc = 'M' + (cx + r) + ' ' + cy + 'A' + r + ' ' + r + ' 0 1 0 ' + (cx - r) + ' ' + cy + 'A' + r + ' ' + r + ' 0 1 0 ' + (cx + r) + ' ' + cy + 'Z';
    else if (a > 0) arc = 'M' + cx + ' ' + cy + 'L' + (cx + r) + ' ' + cy + 'A' + r + ' ' + r + ' 0 ' + (a > 180 ? 1 : 0) + ' 0 ' + x(a, r) + ' ' + y(a, r) + 'Z';
    const mid = a >= 360 ? 135 : a / 2, lr = r + 26;
    return { arc, r1: 'M' + cx + ' ' + cy + 'L' + (cx + L) + ' ' + cy, r2: 'M' + cx + ' ' + cy + 'L' + x(a, L) + ' ' + y(a, L), vx: cx, vy: cy, lab: lab || '', lx: x(mid, lr), ly: (+y(mid, lr) + 8).toFixed(1) };
  }
  rankInfo(pts) {
    const R = this.RANKS(); let i = 0; R.forEach((k, j) => { if (pts >= k[2]) i = j; });
    const cur = R[i], nx = R[i + 1], o = { name: cur[1], key: cur[0], idx: i };
    R.forEach((k) => { o['is_' + k[0]] = k[0] === cur[0]; });
    o.pct = nx ? Math.round(100 * (pts - cur[2]) / (nx[2] - cur[2])) + '%' : '100%';
    o.toNext = nx ? 'noch ' + (nx[2] - pts) + ' bis ' + nx[1] : 'höchster Rang';
    return o;
  }
  avgPer(r) {
    const mixed = r.packs.length >= 2; let sum = 0, n = 0;
    r.mix.forEach((m) => { sum += m[1] * this.per(m[0], r.art, mixed).v; n += m[1]; });
    return Math.round(sum / n);
  }
  nextId() { const s = this.state; return ['mess', 'neu', 'blitz'].find((k) => !s.doneR[k]) || null; }

  /* ---------- Ablauf ---------- */
  go(scr) { this.setState({ scr, sheet: null }); }
  startRound(id) {
    const r = this.R()[id];
    if (r.wissen) { this.setState({ scr: 'wissen', wp: r.packs[0], wmode: 'round', r: id, sheet: null }); return; }
    this.begin(id);
  }
  begin(id) {
    this.setState({ scr: 'ueb', r: id, ti: 0, sel: -1, inp: '', ph: 'ask', tr: 1, t0: Date.now(), log: [], fastRun: 0, pause: false, me: 0, kr: 0, sheet: null });
  }
  check() {
    const s = this.state, r = this.R()[s.r], t = r.tasks[s.ti], mixed = r.packs.length >= 2;
    const q = this.per(t.p, r.art, mixed).v;
    if (t.k === 'tap') {
      if (s.sel < 0) return;
      const ok = s.sel === t.ans, fast = Date.now() - s.t0 < 1500;
      const run = fast && !ok ? s.fastRun + 1 : 0;
      const e = { p: t.p, ok: ok ? 1 : 0, fast, pts: ok && !fast ? q : 0 };
      this.setState({ ph: ok ? (fast ? 'fast' : 'ok') : 'no', log: s.log.concat([e]), fastRun: run, me: s.me + (ok ? 1 : 0), kr: s.kr + (r.kw ? r.kw[s.ti] : 0), lastPts: e.pts, lastFast: fast });
      return;
    }
    if (s.inp === '') return;
    const v = +s.inp, ok = Math.abs(v - t.ans) <= t.tol;
    if (ok) {
      const pts = s.tr === 1 ? q : Math.max(1, Math.round(q / 2));
      this.setState({ ph: s.tr === 1 ? 'ok' : 'half', log: s.log.concat([{ p: t.p, ok: s.tr === 1 ? 1 : 0.5, fast: false, pts }]), lastPts: pts });
    } else if (s.tr === 1) {
      this.setState({ ph: 'no', tr: 2, lastPts: 0 });
    } else {
      this.setState({ ph: 'sol', log: s.log.concat([{ p: t.p, ok: 0, fast: false, pts: 0 }]), lastPts: 0 });
    }
  }
  next() {
    const s = this.state, r = this.R()[s.r];
    if (s.fastRun >= 3 && !s.pause) { this.setState({ pause: true }); return; }
    if (s.ti + 1 < r.tasks.length) this.setState({ ti: s.ti + 1, sel: -1, inp: '', ph: 'ask', tr: 1, t0: Date.now() });
    else this.finish();
  }
  finish() {
    const s = this.state, r = this.R()[s.r], PK = this.PK(), mixed = r.packs.length >= 2, I = this.I();
    const all = r.pre.map((e) => ({ p: e[0], ok: e[1], fast: false, pts: e[1] ? this.per(e[0], r.art, mixed).v : 0 })).concat(s.log);
    const by = {}; r.packs.forEach((id) => { by[id] = { n: 0, ok: 0, full: 0, half: 0, fast: 0, all: 0 }; });
    all.forEach((e) => { const b = by[e.p]; b.all++; if (e.fast) { b.fast++; return; } b.n++; if (e.ok === 1) { b.ok++; b.full++; } else if (e.ok === 0.5) { b.ok += 0.5; b.half++; } });
    const totalFast = all.filter((e) => e.fast).length;
    const h = Object.assign({}, s.h), due = Object.assign({}, s.due);
    const lines = [], rows = []; let total = 0, gained = 0;
    r.packs.forEach((id) => {
      const b = by[id], P = PK[id], q = this.per(id, r.art, mixed), hb = s.h[id], acc = b.n ? b.ok / b.n : 0;
      if (b.full) { const v = b.full * q.v; total += v; lines.push({ t: 'Paket ' + P.nr + ': ' + b.full + ' richtig × ' + q.v, s: q.why.join(' · '), v: '+' + v }); }
      if (b.half) { const hv = Math.max(1, Math.round(q.v / 2)), v = b.half * hv; total += v; lines.push({ t: 'Paket ' + P.nr + ': ' + b.half + ' im zweiten Versuch × ' + hv, s: 'zweiter Versuch: halbe Punkte', v: '+' + v }); }
      const row = { id, cnt: b.full + ' von ' + b.all + ' richtig' + (b.half ? ', ' + b.half + ' im zweiten Versuch' : '') + (b.fast ? ', ' + b.fast + ' zu schnell' : ''), hi: false, tag: '', hicon: I.check, text: '', bg: 'transparent' };
      const bonus = (n, txt) => { total += n; lines.push({ t: txt, s: 'einmal je Paket', v: '+' + n }); };
      if (r.art === 'selbst') {
        if (hb === 1) {
          if (b.n >= 4 && acc >= 0.8) { h[id] = 2; gained++; bonus(30, 'Neuer Haken Können · Paket ' + P.nr); Object.assign(row, { hi: true, tag: 'Neuer Haken: Können!', hicon: I.pencil, bg: '#DDF5E7', text: 'Du kannst ' + P.name + ' jetzt selbst messen. Als Nächstes: an einem anderen Tag gemischt, dann ist es sicher.' }); }
          else row.text = 'Für den Können-Haken brauchst du 4 von 5 selbst richtig. Krabbi schlägt dir gleich eine andere Lernform vor, zum Beispiel Zeichnen.';
        } else if (hb >= 3 && due[id]) {
          if (acc >= 0.8) { delete due[id]; bonus(20, 'Aufgefrischt · Paket ' + P.nr); Object.assign(row, { hi: true, tag: 'Aufgefrischt!', hicon: I.loop, bg: '#DDF5E7', text: 'Sitzt noch. Nächstes Mal wieder dran in 4 Tagen.' }); }
          else if (acc < 0.5) { h[id] = 2; row.text = 'Das war schwer. Der Behalten-Haken ist erst einmal weg, mit einer guten Misch-Runde holst du ihn zurück.'; }
          else row.text = 'Fast. Das Paket bleibt wieder dran.';
        } else if (hb >= 3) row.text = 'Kannst du schon. Wenig Punkte, bis es wieder dran ist (in ' + P.inD + ' Tagen). Im Mix hilft es trotzdem.';
        else row.text = 'Gut geübt.';
      } else {
        if (hb === 0) {
          if (totalFast >= 3) row.text = 'Zu viele sehr schnelle Antworten. Diese Runde zählt nicht für den Haken. Probier es gleich noch einmal in Ruhe.';
          else if (b.ok >= 4) { h[id] = 1; gained++; bonus(20, 'Neuer Haken Kennen · Paket ' + P.nr); Object.assign(row, { hi: true, tag: 'Neuer Haken: Kennen!', hicon: I.eye, bg: '#DDF5E7', text: 'Du erkennst die Grenzfälle. Als Nächstes: selbst messen für den Können-Haken.' }); }
          else row.text = b.full + ' in Ruhe richtig. Für den Kennen-Haken brauchst du 4 von 5.';
        } else if (hb === 1) row.text = 'Kennst du schon. Für den Können-Haken: selbst messen.';
        else if (due[id]) row.text = 'Wieder dran. Antippen frischt es nicht auf, dafür brauchst du eine Runde zum Selbstmachen.';
        else row.text = 'Kannst du schon selbst. Antippen bringt dir hier nur wenig.';
      }
      rows.push(Object.assign(row, { tok: null }));
    });
    if (totalFast) lines.push({ t: totalFast + ' × sehr schnell getippt', s: 'Raten bringt keine Punkte', v: '0' });
    const done = s.done + 1;
    if (done === s.ziel) { total += 15; lines.push({ t: 'Tagesziel geschafft', s: 'einmal am Tag', v: '+15' }); }
    const before = this.rankInfo(s.points).idx, after = this.rankInfo(s.points + total).idx;
    const right = all.filter((e) => e.ok > 0).length;
    const head = right / all.length >= 0.8 ? 'Stark gemacht!' : right / all.length >= 0.5 ? 'Gut dran geblieben!' : 'Du hast es versucht!';
    const doneR = Object.assign({}, s.doneR); doneR[r.id] = true;
    this.setState({ h, due, done, doneR, points: s.points + total, gained: s.gained + gained, scr: 'erg', res: { rid: r.id, mod: r.mod, head, right, n: all.length, rows, lines, total, up: after > before } });
  }

  /* ---------- Anzeige ---------- */
  renderVals() {
    const s = this.state, PK = this.PK(), R = this.R(), I = this.I();
    const is = {}; ['heute', 'fach', 'frei', 'ueb', 'wissen', 'erg', 'regeln', 'ich', 'gem'].forEach((k) => { is[k] = s.scr === k; });
    const tabc = {}; ['heute', 'fach', 'gem', 'ich'].forEach((k) => { tabc[k] = 'tab' + (s.scr === k ? ' on' : ''); });
    const rk = this.rankInfo(s.points), left = Math.max(0, s.ziel - s.done);
    const goalStars = []; for (let i = 0; i < s.ziel; i++) goalStars.push({ fill: i < s.done ? '#FFC83D' : '#FFFFFF', dash: i < s.done ? 'none' : '2 2' });
    const goalText = Math.min(s.done, s.ziel) + ' von ' + s.ziel + ' Runden';
    const goalSub = left ? 'noch etwa ' + left * 5 + ' Minuten' : 'Tagesziel geschafft';
    const nid = this.nextId(), nr = nid ? R[nid] : null;
    const coin = (r) => '≈ ' + this.avgPer(r) + ' Punkte je Antwort';
    const pkList = (r) => r.packs.map((id) => 'Paket ' + PK[id].nr).join(' + ');
    const next = nr ? { title: nr.title, line: 'Mathe · ' + nr.mod + ' · ' + pkList(nr) + (nr.packs.length > 1 ? ' gemischt' : ' allein'), goal: nr.goal, coin: coin(nr), icon: I[nr.icon], hicon: I[nr.hk] } : { title: '', line: '', goal: '', coin: '', icon: '', hicon: '' };
    const heuteSay = left === 0 ? 'Dein Tagesziel ist geschafft. Du darfst jetzt aufhören, ich bin stolz auf dich!' : 'Schön, dass du da bist! Noch ' + left + (left === 1 ? ' Runde' : ' Runden') + ' bis zu deinem Tagesziel. Ich hab schon was ausgesucht.';
    const cnt = { neu: 0, ueben: 0, sicher: 0 }; Object.keys(s.h).forEach((k) => { const w = s.h[k]; if (w === 0) cnt.neu++; else if (w >= 3) cnt.sicher++; else cnt.ueben++; });
    const mathLine = (Object.keys(s.due).length ? Object.keys(s.due).length + ' Paket wieder dran · ' : '') + cnt.ueben + ' noch üben';
    const gefuehrt = s.lenk === 'gefuehrt';

    const sugg = ['mess', 'neu', 'blitz'].map((id, i) => {
      const r = R[id];
      return { id, tag: r.tag, tagBg: r.tagBg, title: r.title, mod: r.mod, art: { selbst: 'Selbst machen', tippen: 'Antippen' }[r.art], icon: I[r.icon], hicon: I[r.hk], goal: r.goal,
        toks: r.packs.map((p) => this.tok(p)), mixw: r.packs.length > 1 ? 'gemischt' : 'allein', coin: coin(r) + ' · ' + r.coinSub, coinBg: r.coinBg,
        done: !!s.doneR[id], tip: id === nid, aria: r.tag + ': ' + r.title + ', ' + coin(r),
        open: () => this.setState({ sheet: 'vor', sv: id }) };
    });
    const groups = [['A', 'Winkelarten', 'Paket 1–4'], ['B', 'Winkel im Einsatz', 'Paket 5–8']].map((g) => {
      const ids = Object.keys(PK).map(Number).filter((id) => PK[id].grp === g[0]);
      const c = { neu: 0, ueben: 0, sicher: 0 }; ids.forEach((id) => { const w = s.h[id]; if (w === 0) c.neu++; else if (w >= 3) c.sicher++; else c.ueben++; });
      const sum = [c.sicher ? c.sicher + ' sicher' : '', c.ueben ? c.ueben + ' noch üben' : '', c.neu ? c.neu + ' neu' : ''].filter(Boolean).join(' · ');
      return { t: g[1], sub: g[2], sum, items: ids.map((id) => this.tok(id, { open: () => this.setState({ sheet: 'pkg', sp: id }) })) };
    });

    // Vorschau
    const vr = R[s.sv], vmixed = vr.packs.length >= 2;
    const v = { tag: vr.tag, tagBg: vr.tagBg, title: vr.title, mod: vr.mod, icon: I[vr.icon], hicon: I[vr.hk], art: { selbst: 'Selbst machen', tippen: 'Antippen' }[vr.art],
      count: vr.total + ' Aufgaben · etwa ' + vr.min + ' Minuten', why: vr.why, goal: vr.goal,
      bar: vr.mix.map((m) => ({ w: Math.round(100 * m[1] / vr.total) + '%', col: PK[m[0]].col, t: m[1] + ' × Paket ' + m[0] })),
      pts: vr.packs.map((id) => { const q = this.per(id, vr.art, vmixed); return { tok: this.tok(id), name: 'Paket ' + id + ' · ' + PK[id].name, why: q.why.join(' · '), v: q.v }; }),
      start: () => this.startRound(s.sv) };

    // Paket-Blatt
    const sp = s.sp, sh3 = s.h[sp], grpA = PK[sp].grp === 'A';
    const MODHK = grpA ? [['Winkelart erkennen', 'Gradzahl einordnen', 'Blitz-Duell'], ['Messen', 'Zeichnen', 'Schätzen', 'Konstruieren'], ['jede Misch-Runde', 'Abschlusstest']]
      : [['Wissen-Check', 'Zuordnen'], ['Aufgaben-Mission'], ['Aufgaben-Mission gemischt', 'Abschlusstest']];
    const HK = [['Kennen', 'eye', 'Eine Runde mit 80 % richtig, zum Beispiel mit Antippen.'], ['Können', 'pencil', 'Eine Runde selbst machen mit 80 % richtig, mindestens 4 Aufgaben aus diesem Paket.'], ['Behalten', 'loop', 'An einem anderen Tag gemischt mit anderen Paketen noch 80 % richtig.']];
    const play = { 1: 'mess', 2: 'blitz', 3: 'mess', 4: 'neu' }[sp];
    const pp = { tok: this.tok(sp), src: PK[sp].src, goal: PK[sp].goal,
      hk: HK.map((k, i) => ({ n: k[0], icon: I[k[1]], how: k[2], mods: MODHK[i], cls: i < sh3 ? 'hk' : 'hk off', bg: i < sh3 ? '#F2B517' : '#FFFFFF', state: i < sh3 ? 'geschafft' : i === sh3 ? 'als Nächstes' : 'kommt danach' })),
      read: () => this.setState({ scr: 'wissen', wp: sp, wmode: 'read', sheet: null }),
      canPlay: !!play, noPlay: !play, playT: sh3 >= 3 ? (s.due[sp] ? 'Auffrischen' : 'Trotzdem üben') : sh3 === 0 ? 'Kennenlernen' : 'Nächsten Haken üben',
      play: () => play && this.startRound(play) };

    // Selbst zusammenstellen
    const fsel = s.fsel, fmixed = fsel.length >= 2;
    const frToks = Object.keys(PK).map(Number).map((id) => {
      const on = fsel.includes(id);
      return this.tok(id, { on, bg: on ? '#FFE7A3' : 'transparent', toggle: () => { const a = on ? fsel.filter((x) => x !== id) : (fsel.length >= 6 ? fsel : fsel.concat([id])); this.setState({ fsel: a }); } });
    });
    const ARTL = { lesen: 'Lesen', tippen: 'Antippen', ordnen: 'Ordnen', selbst: 'Selbst machen', test: 'Test mit Note' };
    const frMods = this.MODS().map((m) => {
      const fit = fsel.filter((id) => m.fit === 'all' || PK[id].grp === m.fit);
      const dis = !fsel.length || !fit.length, on = s.fmod === m.id && !dis, mix = fit.length >= 2;
      let pv = '', ps = '', hk = '';
      if (dis) { pv = ''; ps = fsel.length ? (m.fit === 'A' ? 'passt nur zu Paket 1–4' : 'passt nur zu Paket 5–8') : 'erst Pakete wählen'; hk = 'nicht mit dieser Auswahl'; }
      else if (m.art === 'lesen') { pv = '0 Punkte'; ps = 'der Check danach zählt'; hk = 'Grundwissen, immer offen'; }
      else if (m.art === 'test') { pv = 'nach Note'; ps = 'Note 1 = 100 Punkte'; hk = fit.some((id) => s.h[id] === 2) ? 'kann Behalten bringen' : 'zeigt, was du kannst'; }
      else {
        const vs = fit.map((id) => this.per(id, m.art, mix).v), avg = Math.round(vs.reduce((a, b) => a + b, 0) / vs.length);
        pv = '≈ ' + avg + ' je Antwort';
        ps = avg <= 3 ? 'wenig, weil du es schon kannst' : mix ? 'mit +20 % gemischt' : 'volle Punkte';
        const want = m.art === 'selbst' ? [[0, 'Kennen'], [1, 'Können'], [2, 'Behalten']] : [[0, 'Kennen']];
        const hit = []; want.forEach((w) => { fit.forEach((id) => { if (s.h[id] === w[0] && (w[0] !== 2 || mix)) hit.push(w[1] + ' für Paket ' + id); }); });
        hk = hit.length ? 'kann bringen: ' + hit.slice(0, 2).join(', ') : 'bringt keinen neuen Haken';
      }
      return { t: m.t, icon: I[m.icon], art: ARTL[m.art], hk, pv, ps, dis, on, cls: 'mrow' + (on ? ' on' : ''), pick: () => this.setState({ fmod: m.id }) };
    });
    const fmI = this.MODS().findIndex((m) => m.id === s.fmod), fm = this.MODS()[fmI], fmRow = frMods[fmI];
    const fr = { toks: frToks, mods: frMods,
      mixText: fsel.length ? (fsel.length > 1 ? 'Paket ' + fsel.join(' + ') + ' gemischt' : 'Paket ' + fsel[0] + ' allein') : 'noch keine Pakete',
      sum: fsel.length && fmRow && !fmRow.dis ? 'Du übst: ' + fm.t + ' · Paket ' + fsel.join(' + ') : 'Wähle Pakete und eine Lernform',
      sum2: fmRow && !fmRow.dis ? fmRow.pv + ' · ' + fmRow.hk + ' · Im Entwurf startet eine Beispielrunde.' : '',
      noStart: !fmRow || fmRow.dis,
      start: () => {
        if (!fm) return;
        if (fm.art === 'lesen') { this.setState({ scr: 'wissen', wp: fsel[0], wmode: 'read' }); return; }
        if (fm.art === 'tippen') { this.startRound(fsel.length === 1 && fsel[0] === 4 ? 'neu' : 'blitz'); return; }
        this.startRound('mess');
      } };

    // Übung
    let u = { nr: 0, total: 0, dots: [], opts: [], tok: this.tok(1), f: this.fig(0, 1, 1, 0, 0, 0, 0), q: '', sub: '', mod: '' };
    if (s.scr === 'ueb' && s.r) {
      const r = R[s.r], t = r.tasks[s.ti], mixed = r.packs.length >= 2, done = r.pre.length + s.ti;
      const asking = s.ph === 'ask', q = this.per(t.p, r.art, mixed);
      const dots = [];
      const seq = r.pre.map((e) => ({ p: e[0], ok: e[1], fast: false })).concat(s.log);
      for (let i = 0; i < r.total; i++) {
        const fut = r.pre.length + i - r.pre.length; // Index in den Aufgaben
        const pk = i < seq.length ? seq[i].p : (r.tasks[i - r.pre.length] ? r.tasks[i - r.pre.length].p : r.packs[0]);
        const col = PK[pk].col, e = seq[i];
        if (e) dots.push(e.fast ? { bg: '#CFCBE0', bd: '3px solid #1D1B3A', sh: 'none', ok: false } : e.ok > 0 ? { bg: col, bd: '3px solid #1D1B3A', sh: 'none', ok: true } : { bg: '#FFFFFF', bd: '3px dashed #B4500A', sh: 'none', ok: false });
        else if (i === done) dots.push({ bg: '#FFFFFF', bd: '4px solid ' + col, sh: '0 0 0 3px #1D1B3A', ok: false });
        else dots.push({ bg: '#FFFFFF', bd: '3px solid ' + col, sh: 'none', ok: false });
      }
      const opts = (t.opt || []).map((o, i) => {
        let cls = 'ans';
        if (asking) { if (s.sel === i) cls += ' sel'; }
        else if (i === t.ans) cls += ' ok';
        else if (i === s.sel) cls += ' no';
        else cls += ' dim';
        return { t: o, k: 'ABCD'[i], cls, dis: !asking, pick: () => this.setState({ sel: i }) };
      });
      const big = t.a > 180 || t.a === 0;
      const f = big ? this.fig(t.a, 360, 220, 180, 110, 100, 40, t.lab) : this.fig(t.a, 360, 220, 180, 190, 150, 44, t.lab);
      const P = PK[t.p];
      let fbT = '', fbX = '', fbP = '', fbBg = '#DDF5E7', fbBd = '#12704A', fbInk = '#0C5A3A', canRetry = false;
      const PR = ['Genau richtig!', 'Stark!', 'Volltreffer!', 'Richtig!'];
      if (s.ph === 'ok') { fbT = PR[(s.ti + done) % 4]; fbX = t.ex; fbP = '+' + s.lastPts + ' · ' + (r.art === 'selbst' ? 'selbst gemessen' : 'angetippt'); }
      else if (s.ph === 'half') { fbT = 'Richtig, im zweiten Versuch'; fbX = t.ex; fbP = '+' + s.lastPts + ' · halbe Punkte'; }
      else if (s.ph === 'fast') { fbT = 'Richtig, aber sehr schnell getippt'; fbX = 'Lies erst die Frage in Ruhe, dann gibt es Punkte. ' + t.ex; fbP = '0 · zu schnell'; fbBg = '#E3E9FF'; fbBd = '#2B3FA8'; fbInk = '#1F2F86'; }
      else if (s.ph === 'no' && t.k === 'num') { fbT = 'Noch nicht ganz'; fbX = 'Tipp: ' + t.hint; fbP = 'zweiter Versuch: halbe Punkte'; fbBg = '#FFE9D6'; fbBd = '#B4500A'; fbInk = '#8A3D07'; canRetry = true; }
      else if (s.ph === 'no') { fbT = s.lastFast ? 'Das ging sehr schnell' : 'Noch nicht ganz'; fbX = 'Richtig ist: ' + t.opt[t.ans] + '. ' + t.ex; fbP = '0 Punkte'; fbBg = '#FFE9D6'; fbBd = '#B4500A'; fbInk = '#8A3D07'; }
      else if (s.ph === 'sol') { fbT = 'Noch nicht ganz'; fbX = 'Richtig ist ' + t.ans + '°. ' + t.ex; fbP = '0 Punkte'; fbBg = '#FFE9D6'; fbBd = '#B4500A'; fbInk = '#8A3D07'; }
      u = { mod: r.mod, sub: r.packs.map((x) => 'Paket ' + x).join(' + ') + (mixed ? ' gemischt' : ' allein') + ' · ' + q.v + ' Punkte je richtiger Antwort', duel: !!r.duel,
        nr: done + 1, total: r.total, dots, tok: this.tok(t.p), art: r.art === 'selbst' ? 'Selbst machen' : 'Antippen',
        q: t.q, subq: t.sub, hasFig: true, figH: 220, vb: '0 0 360 220', f, figLabel: 'Winkel' + (t.lab && t.lab !== '?' ? ' mit ' + t.lab : ''),
        tap: t.k === 'tap', num: t.k === 'num', opts, inp: s.inp === '' ? '…' : s.inp, inBg: asking ? '#FFFFFF' : '#F3F1FA', locked: !asking,
        asking, noCheck: t.k === 'tap' ? s.sel < 0 : s.inp === '', fb: !asking, fbT, fbX, fbP, fbBg, fbBd, fbInk, canRetry, canNext: !asking && !canRetry,
        nextT: s.ti + 1 < r.tasks.length ? 'Weiter' : 'Zum Ergebnis' };
    }
    const keys = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'].map((k) => ({ t: k, press: () => { if (this.state.ph === 'ask' && this.state.inp.length < 3) this.setState({ inp: this.state.inp + k }); } }));

    // Wissen
    const WF = {
      1: [[40, 'Spitzer Winkel', 'zwischen 0° und 90°'], [90, 'Rechter Winkel', 'genau 90°']],
      2: [[130, 'Stumpfer Winkel', 'zwischen 90° und 180°'], [180, 'Gestreckter Winkel', 'genau 180°, eine gerade Linie']],
      3: [[250, 'Überstumpfer Winkel', 'zwischen 180° und 360°'], [110, 'Trick beim Messen', 'Den Winkel innen messen, dann 360° minus diesen Winkel rechnen.']],
      4: [[0, 'Nullwinkel', '0°: Beide Schenkel liegen aufeinander.'], [360, 'Vollwinkel', '360°: einmal ganz herum.'], [179, 'Grenzfälle', '89° ist noch spitz, 91° schon stumpf. 179° ist stumpf, 181° überstumpf.']]
    };
    const wp = s.wp, wf = WF[wp] || [[null, 'Lernziel', PK[wp].goal]];
    const w = { tok: this.tok(wp), say: s.wmode === 'round' ? 'Lies kurz, dann geht es los. Das Wissen bleibt immer hier, du kannst jederzeit nachschauen.' : 'Hier kannst du immer nachlesen. Lesen bringt keine Punkte, macht die Aufgaben danach aber leichter.',
      facts: wf.map((x) => ({ fig: x[0] !== null, g: (x[0] > 180 || x[0] === 0) ? this.fig(x[0], 200, 140, 100, 70, 62, 24, x[0] + '°') : this.fig(x[0] || 0, 200, 140, 100, 122, 86, 28, x[0] === null ? '' : x[0] + '°'), t: x[1], x: x[2] })),
      note: s.wmode === 'round' ? 'Danach: 5 Fragen mit Auswahl, 4 Punkte je richtiger Antwort.' : 'Wissen und Lernkarten sind immer offen.',
      goT: s.wmode === 'round' ? 'Verstanden, los geht’s' : 'Fertig gelesen',
      go: () => { if (this.state.wmode === 'round') this.begin(this.state.r); else this.setState({ scr: 'fach', sheet: null }); },
      back: () => this.setState({ scr: 'fach' }) };

    // Ergebnis
    let res = { rows: [], lines: [], total: 0, right: 0, n: 0, head: '', mod: '', goalDone: false, goOn: true, nextT: '', up: false };
    if (s.res) {
      const goalDone = s.done >= s.ziel, nn = this.nextId();
      res = Object.assign({}, s.res, { rows: s.res.rows.map((x) => Object.assign({}, x, { tok: this.tok(x.id) })), goalDone, goOn: !goalDone, nextT: nn ? R[nn].title : 'Krabbi sucht aus',
        nextGo: () => { const k = this.nextId(); if (k) this.startRound(k); else this.go('fach'); } });
    }

    const LT = { frei: 'Alles offen. Krabbi schlägt vor, Robin kann alles selbst zusammenstellen, auch beliebig viele neue Pakete anfangen.', ausgewogen: 'Empfohlen. Alles offen, aber ehrlich: Bequemes bringt wenig Punkte, und höchstens zwei Pakete stehen gleichzeitig nur auf „Kennen“.', gefuehrt: 'Robin wählt nur aus Krabbis drei Vorschlägen, dazu sind Wissen und Lernkarten offen. Fast wie ein fester Weg, aber mit Wahl.' };
    const lenkOpts = [['frei', 'Frei'], ['ausgewogen', 'Ausgewogen'], ['gefuehrt', 'Geführt']].map((o) => ({ t: o[1], on: s.lenk === o[0], cls: 'sb' + (s.lenk === o[0] ? ' on' : ''), pick: () => this.setState({ lenk: o[0] }) }));
    const zielOpts = [2, 3, 4].map((n) => ({ t: n + ' Runden', on: s.ziel === n, cls: 'sb' + (s.ziel === n ? ' on' : ''), pick: () => this.setState({ ziel: n }) }));
    const rb = {}; this.RANKS().forEach((k, i) => { rb[k[0]] = i === rk.idx ? '#FFE7A3' : i < rk.idx ? '#F3F1FA' : 'transparent'; });

    return {
      is, tabc, rk, points: s.points, goalStars, goalText, goalSub, next, hasNext: !!nr && left > 0, allDone: left === 0,
      doneText: 'Du hast heute ' + s.done + ' Runden geschafft' + (s.gained ? ' und ' + s.gained + (s.gained === 1 ? ' neuen Haken' : ' neue Haken') + ' bekommen' : '') + '. Morgen ist Paket 3 für den Behalten-Haken dran.',
      heuteSay, mathLine,
      fachSay: gefuehrt ? 'Such dir eins von meinen drei Vorschlägen aus. Alle bringen dich weiter.' : 'Such dir eins aus. Alle drei bringen dich weiter. Oder stell dir unten selbst etwas zusammen.',
      sugg, groups, showFrei: !gefuehrt, gefuehrt, sh: { vor: s.sheet === 'vor', pkg: s.sheet === 'pkg' }, v, pp, fr, u, keys, w, res,
      me: s.me, kr: s.kr, pause: s.pause,
      lenkOpts, zielOpts, lenkText: LT[s.lenk], rb,
      elternStand: cnt.sicher + ' sicher · ' + cnt.ueben + ' noch üben · ' + cnt.neu + ' neu · heute ' + s.gained + (s.gained === 1 ? ' neuer Haken' : ' neue Haken'),
      gemN: 18 + s.gained, gemPct: Math.round(100 * (18 + s.gained) / 30) + '%', gemMe: 4 + s.gained,
      goHeute: () => this.go('heute'), goFach: () => this.go('fach'), goGem: () => this.go('gem'), goIch: () => this.go('ich'),
      goFrei: () => this.go('frei'), goRegeln: () => this.setState({ back: s.scr === 'regeln' ? s.back : s.scr, scr: 'regeln', sheet: null }),
      goBack: () => this.go(s.back || 'fach'),
      goLos: () => { const k = this.nextId(); if (k) this.startRound(k); },
      closeSheet: () => this.setState({ sheet: null }),
      quit: () => this.setState({ scr: 'fach', r: null, pause: false }),
      check: () => this.check(), weiter: () => this.next(), retry: () => this.setState({ ph: 'ask', inp: '' }),
      del: () => { if (this.state.ph === 'ask') this.setState({ inp: this.state.inp.slice(0, -1) }); },
      unpause: () => { this.setState({ pause: false, fastRun: 0 }); setTimeout(() => this.next(), 0); }
    };
  }
}
