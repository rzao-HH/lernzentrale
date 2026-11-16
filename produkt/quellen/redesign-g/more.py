import sys
sys.path.insert(0, sys.argv[1]); out = sys.argv[2]
from common import *

CSS = r"""
.band{position:relative;flex:none;background:#1E2257;color:#FFFFFF;overflow:hidden}
.sb{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:2px;min-height:64px;padding:6px 6px;border:3px solid #1D1B3A;border-radius:14px;background:#FFFFFF;font-weight:700;font-size:15px;text-align:center;line-height:1.15}
.sb b{font-family:'Baloo 2',sans-serif;font-size:20px}
.sb.on{background:#FFC83D;box-shadow:0 4px 0 #1D1B3A}
.tg{display:flex;align-items:center;gap:10px;min-height:56px;padding:6px 12px;border:3px solid #1D1B3A;border-radius:14px;background:#FFFFFF;font-weight:700;font-size:15px;text-align:left;line-height:1.2}
.tg.on{background:#DDE6FF;border-color:#2B3FA8}
.box{width:26px;height:26px;flex:none;border-radius:8px;border:3px solid currentColor;display:flex;align-items:center;justify-content:center}
.line{display:flex;align-items:center;gap:12px;padding:6px 0;border-bottom:2px dotted #C9C3B0;font-size:16px}
"""

def band_stars(w, h, n, seed):
    return '<svg width="%d" height="%d" viewBox="0 0 %d %d" aria-hidden="true" style="position:absolute;left:0;top:0">%s</svg>' % (w, h, w, h, stars_bg(w, h, n, seed))
HORIZON = '<svg width="768" height="34" viewBox="0 0 768 34" aria-hidden="true" style="position:absolute;left:0;bottom:-1px;display:block"><path d="M0 34V22Q384 -8 768 22V34Z" fill="#EEF0FA"></path></svg>'

def seg(hole, cols):
    return ('<div style="display:grid;grid-template-columns:repeat(%d,minmax(0,1fr));gap:8px;margin-top:8px"><sc-for list="{{%s}}" as="o" hint-placeholder-count="%d">'
            '<button type="button" class="{{o.cls}}" onClick="{{o.pick}}" aria-pressed="{{o.on}}"><b>{{o.v}}</b>{{o.t}}</button></sc-for></div>') % (cols, hole, cols)

PUNKTE = (head('G · Punkte-Rechner').replace('%s', CSS, 1)
 + '<div style="width:768px;height:1024px;position:relative;overflow:hidden;background:#EEF0FA;color:#1D1B3A;font-family:\'Atkinson Hyperlegible\',Verdana,sans-serif;font-size:17px;line-height:1.4;display:flex;flex-direction:column">'
 + '<div class="band" style="height:150px;padding:20px 32px 0">' + band_stars(768, 150, 34, 31)
 + '<div style="position:relative;display:flex;align-items:center;gap:16px"><span class="kr" style="display:block">' + krabbi(84, 'Krabbi') + '</span>'
 + '<div><span class="cap" style="color:#C9CCFF">So bekommst du Punkte</span><h1 class="h" style="font-size:38px">Punkte-Rechner</h1><div style="color:#E3E4FF">Tipp an, was du machst. Ich rechne dir vor, was eine richtige Antwort bringt.</div></div></div>' + HORIZON + '</div>'
 + '<div style="flex:1;padding:8px 32px 20px;display:flex;flex-direction:column;gap:12px">'
 + '<div class="card" style="padding:12px 16px"><b style="font-size:18px">1 · Was machst du?</b>' + seg('arts', 4) + '</div>'
 + '<div class="card" style="padding:12px 16px"><b style="font-size:18px">2 · Wie steht das Paket?</b>' + seg('sts', 5) + '</div>'
 + '<div class="card" style="padding:12px 16px"><b style="font-size:18px">3 · Was stimmt noch?</b><div style="display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px;margin-top:8px"><sc-for list="{{tgs}}" as="o" hint-placeholder-count="5">'
 + '<button type="button" class="{{o.cls}}" onClick="{{o.pick}}" aria-pressed="{{o.on}}"><span class="box"><sc-if value="{{o.on}}" hint-placeholder-val="{{ false }}">' + ic('check', 18, 3.4) + '</sc-if></span>{{o.t}}</button></sc-for></div></div>'
 + '<div class="card" style="padding:14px 18px;background:#FFFFFF;display:flex;gap:18px;align-items:stretch">'
 + '<div style="flex:1"><span class="cap muted">So rechne ich</span><sc-for list="{{steps}}" as="l" hint-placeholder-count="3"><div class="line"><span style="flex:1">{{l.t}}</span><b class="h" style="font-size:20px;font-weight:700">{{l.v}}</b></div></sc-for></div>'
 + '<div style="width:220px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4px;padding:10px;border:3px solid #1D1B3A;border-radius:20px;background:{{resBg}};text-align:center">'
 + '<span style="font-size:15px;font-weight:700">eine richtige Antwort</span><span class="h" style="font-size:64px;line-height:1">{{pts}}</span><span style="font-size:16px;font-weight:700">{{ptsWord}}</span>'
 + '<span class="muted" style="font-size:14px">10 richtige: {{pts10}}</span></div></div>'
 + '<div style="display:flex;align-items:flex-end;gap:10px">' + krabbi(56) + '<div class="bubble" style="flex:1">{{say}}</div></div>'
 + '<a class="btn2" href="G-App.dc.html" style="align-self:flex-start">' + ic('back', 22, 3) + 'Zurück zur App</a>'
 + '</div></div>\n</x-dc>\n'
 + '<script type="text/x-dc" data-dc-script data-props=\'{"$preview":{"width":768,"height":1024}}\'>\n' + r"""
class Component extends DCLogic {
  constructor(p) { super(p); this.state = { art: 'selbst', st: 'ueben', kann: false, mix: true, deckel: false, zweit: false, fast: false }; }
  renderVals() {
    const s = this.state, d = (x) => String(x).replace('.', ',');
    const A = [['tippen', 'Antippen', 4], ['ordnen', 'Ordnen', 6], ['selbst', 'Selbst machen', 10], ['lesen', 'Lesen', 0]];
    const S = [['neu', 'neu', 1], ['ueben', 'noch üben', 1], ['dran', 'wieder dran', 1], ['lange', 'lange nicht geübt', 1.2], ['sicher', 'sicher, nicht dran', 0.15]];
    const set = (k, v) => () => this.setState({ [k]: v });
    const arts = A.map((a) => ({ t: a[1], v: a[2], on: s.art === a[0], cls: 'sb' + (s.art === a[0] ? ' on' : ''), pick: set('art', a[0]) }));
    const sts = S.map((a) => ({ t: a[1], v: a[2] === 1 ? '×1' : '×' + d(a[2]), on: s.st === a[0], cls: 'sb' + (s.st === a[0] ? ' on' : ''), pick: set('st', a[0]) }));
    const T = [['kann', 'Ich kann es schon selbst (Können-Haken)'], ['mix', 'Gemischt mit anderen Paketen'], ['deckel', 'Schon die 3. Runde mit dem Paket heute'], ['zweit', 'Erst im zweiten Versuch richtig'], ['fast', 'Sehr schnell getippt, ohne zu lesen']];
    const tgs = T.map((t) => ({ t: t[1], on: !!s[t[0]], cls: 'tg' + (s[t[0]] ? ' on' : ''), pick: () => this.setState({ [t[0]]: !s[t[0]] }) }));
    const a = A.find((x) => x[0] === s.art), st = S.find((x) => x[0] === s.st);
    const steps = []; let pts = 0, say = '', zero = false;
    if (s.art === 'lesen') { zero = true; steps.push({ t: 'Lesen und Lernkarten umdrehen', v: '0' }); say = 'Lesen bringt keine Punkte. Es macht die Aufgaben danach leichter, und der kurze Check danach zählt.'; }
    else if (s.fast && s.art !== 'selbst') { zero = true; steps.push({ t: a[1] + ': ' + a[2], v: a[2] }); steps.push({ t: 'Zu schnell, also geraten', v: '= 0' }); say = 'Raten bringt nichts. Lies die Frage in Ruhe, dann zählt deine Antwort, auch für die Haken.'; }
    else if (s.zweit && s.art !== 'selbst') { zero = true; steps.push({ t: a[1] + ': ' + a[2], v: a[2] }); steps.push({ t: 'Zweiter Versuch beim Antippen', v: '= 0' }); say = 'Beim Antippen bleibt im zweiten Versuch ja fast nur noch Raten übrig. Darum gibt es dafür nichts.'; }
    else {
      let f = 1; steps.push({ t: a[1], v: a[2] });
      if (st[2] !== 1) { f *= st[2]; steps.push({ t: st[0] === 'lange' ? 'lange nicht geübt: Bonus' : 'kannst du schon, nicht wieder dran', v: '× ' + d(st[2]) }); }
      else steps.push({ t: st[1] + ': volle Punkte', v: '× 1' });
      if (s.kann && s.art === 'tippen') { f *= 0.5; steps.push({ t: 'Antippen ist für dich leicht', v: '× 0,5' }); }
      if (s.mix) { f *= 1.2; steps.push({ t: 'gemischt wie in der Arbeit', v: '× 1,2' }); }
      if (s.deckel) { f *= 0.15; steps.push({ t: 'heute schon viel geübt', v: '× 0,15' }); }
      if (f > 1.5) { f = 1.5; steps.push({ t: 'höchstens', v: '× 1,5' }); }
      pts = Math.max(1, Math.round(a[2] * f));
      if (s.zweit) { pts = Math.max(1, Math.round(pts / 2)); steps.push({ t: 'zweiter Versuch: die Hälfte', v: '÷ 2' }); }
      steps.push({ t: 'gerundet, mindestens 1', v: '= ' + pts });
      if (s.fast) say = 'Beim Selbstmachen kann man nicht raten. Schnell sein ist hier in Ordnung.';
      else if (pts >= 10) say = 'Super Wahl! Selbst machen und mischen, so lernst du am meisten.';
      else if (s.deckel) say = 'Heute hast du das schon oft geübt. Morgen gibt es wieder volle Punkte. Probier doch ein anderes Paket!';
      else if (st[0] === 'sicher') say = 'Das kannst du schon. Volle Punkte gibt es wieder, wenn das Paket wieder dran ist.';
      else if (pts <= 3) say = 'Das ist für dich leicht, darum gibt es wenig. Probier es mal selbst, dann gibt es mehr.';
      else say = 'Gut! Noch mehr gibt es, wenn du es selbst machst oder mit anderen Paketen mischst.';
    }
    return { arts, sts, tgs, steps, pts, pts10: (pts * 10) + ' Punkte', ptsWord: pts === 1 ? 'Punkt' : 'Punkte', say, resBg: zero ? '#FFE9D6' : pts >= 10 ? '#DDF5E7' : '#FFF1C7' };
  }
}
""" + '\n</script>\n</body>\n</html>\n')
open(out + '/G-Punkte.dc.html', 'w').write(PUNKTE)

# ---------------- G-Ablauf (statisch) ----------------
def step(n, title, see, act, bg='#FFFFFF'):
    return ('<div class="card" style="display:flex;gap:12px;padding:10px 14px;background:%s;box-shadow:0 3px 0 #1D1B3A">'
            '<span style="display:flex;flex:none;width:40px;height:40px;border-radius:50%%;border:3px solid #1D1B3A;background:#FFC83D;align-items:center;justify-content:center;font-family:\'Baloo 2\';font-weight:800;font-size:20px">%s</span>'
            '<div style="flex:1"><b class="h" style="font-size:19px;font-weight:700">%s</b><div style="font-size:14px;line-height:1.35">%s</div></div>'
            '<span style="flex:none;align-self:center;padding:4px 10px;border:2px solid #1D1B3A;border-radius:12px;background:#FFF1C7;font-size:13px;font-weight:700;max-width:150px;text-align:center">%s</span></div>') % (bg, n, title, see, act)

def arrow():
    return '<div style="display:flex;justify-content:center;height:12px;margin:-4px 0">' + ic('arrow', 18, 3, '#1D1B3A', 'transform:rotate(90deg)') + '</div>'

def htok(nr, col, h, word):
    seg = ''.join('<path d="%s" fill="none" stroke="%s" stroke-width="%s" stroke-dasharray="%s" stroke-linecap="round"></path>' % (ARC[i], '#F2B517' if i < h else '#A9A396', 6 if i < h else 2.5, 'none' if i < h else '3 4') for i in range(3))
    return ('<span style="display:flex;flex-direction:column;align-items:center;font-size:13px;font-weight:700"><svg width="54" height="54" viewBox="0 0 64 64" aria-hidden="true">' + seg
            + '<circle cx="32" cy="32" r="19" fill="%s" stroke="#1D1B3A" stroke-width="2.5"></circle><text x="32" y="39" text-anchor="middle" font-family="Baloo 2, sans-serif" font-weight="800" font-size="20" fill="#FFFFFF" stroke="#1D1B3A" stroke-width="0.8">%s</text></svg>%s</span>') % (col, nr, word)

LEVELS = [('#FFC83D', 'Voreinstellung', 'Ein großer „Los“-Knopf startet Krabbis besten Vorschlag.'),
          ('#FFD86E', 'Kleine Auswahl', 'Drei gute Vorschläge: weiterkommen, Neues oder Wieder-dran, Spielerisches.'),
          ('#FFE7A3', 'Volle Freiheit', '„Selbst zusammenstellen“: alles offen, jede Lernform sagt ehrlich, was sie bringt.'),
          ('#FFF1C7', 'Sanfte Bremsen', 'Ratebremse, halbe Punkte bei Gekonntem, Tagesdeckel, Neugier-Bremse. Nie Sperre, nie Abzug.'),
          ('#F3F1FA', 'Regler für Eltern', 'Frei · Ausgewogen · Geführt, dazu das Tagesziel.')]

ABLAUF = (head('G · Ablauf, Haken und Lenkung').replace('%s', '', 1)
 + '<div style="width:768px;height:1024px;position:relative;overflow:hidden;background:#EEF0FA;color:#1D1B3A;font-family:\'Atkinson Hyperlegible\',Verdana,sans-serif;font-size:16px;line-height:1.4;padding:26px 32px;display:flex;flex-direction:column;gap:12px">'
 + '<div style="display:flex;align-items:center;gap:14px">' + krabbi(64) + '<div><span class="cap muted">Entwurf G auf einen Blick</span><h1 class="h" style="font-size:34px">Frei wählen, richtig lernen</h1></div></div>'
 + '<div style="display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,1fr);gap:16px;flex:1;min-height:0">'
 # links: Weg des Kindes
 + '<div style="display:flex;flex-direction:column;gap:8px"><h2 class="h" style="font-size:22px">Der Weg des Kindes</h2>'
 + step('1', 'Heute', 'Tagesziel als 3 Sterne, ein großer Knopf mit dem besten Vorschlag in Worten.', 'Los')
 + arrow() + step('2', 'Übung', 'Herkunft jeder Aufgabe, Fortschritt in Paketfarben, eine Aufgabe, große Antworten.', 'Prüfen')
 + arrow() + step('3', 'Rückmeldung', 'Richtig mit Erklärung und Punkten. Noch nicht ganz: Tipp, zweiter Versuch. Zu schnell: 0 Punkte.', 'Weiter')
 + arrow() + step('4', 'Ergebnis', 'Je Paket ein Satz und der Haken-Ring. Punkte als Rechnung in Zeilen.', 'Weiter · Andere Wahl · Aufhören')
 + arrow() + step('5', 'Fertig für heute', 'Nach dem Tagesziel ist Aufhören der Hauptknopf. Nichts reißt ab.', 'Für heute fertig', '#DDF5E7')
 + '<div class="card" style="padding:10px 14px;box-shadow:0 3px 0 #1D1B3A;font-size:14px"><b style="font-size:16px">Abzweig Fach-Seite:</b> drei Vorschläge mit Vorschau (Was, Wie, Warum, Haken, Punkte), Regal mit allen Paketen in Gruppen, Paket-Blatt mit Wissen, „Selbst zusammenstellen“.</div>'
 + '</div>'
 # rechts
 + '<div style="display:flex;flex-direction:column;gap:12px">'
 + '<div class="card" style="padding:12px 16px;display:flex;flex-direction:column;gap:8px"><h2 class="h" style="font-size:22px">Drei Haken je Paket</h2>'
 + ''.join('<div style="display:flex;gap:10px;align-items:flex-start">%s<div><b>%s</b> <span style="font-size:14px">%s</span></div></div>' % (ic(i, 24), n, t) for i, n, t in [
     ('eye', 'Kennen', 'erkennt es, auch mit Auswahl'), ('pencil', 'Können', 'macht es selbst: messen, schreiben, zeichnen'), ('loop', 'Behalten', 'an einem späteren Tag gemischt')])
 + '<div style="display:flex;justify-content:space-around;margin-top:4px">' + htok(4, '#239C8E', 0, 'neu') + htok(3, '#E0567F', 1, 'noch üben') + htok(5, '#D9862A', 2, 'noch üben') + htok(1, '#5B8DEF', 3, 'sicher') + '</div></div>'
 + '<div class="card" style="padding:12px 16px;display:flex;flex-direction:column;gap:6px"><h2 class="h" style="font-size:22px">Frei, aber gelenkt</h2>'
 + ''.join('<div style="display:flex;gap:10px;align-items:flex-start;padding:7px 10px;border-radius:12px;background:%s;border:2px solid #1D1B3A"><b style="flex:none;width:22px;font-family:\'Baloo 2\'">%d</b><div><b>%s</b><div style="font-size:14px;line-height:1.3">%s</div></div></div>' % (c, i + 1, t, x) for i, (c, t, x) in enumerate(LEVELS))
 + '</div>'
 + '<div class="card" style="padding:12px 16px;background:#FFFFFF"><h2 class="h" style="font-size:22px">Punkte fürs Selberdenken</h2>'
 + '<div style="display:flex;gap:8px;margin-top:6px">' + ''.join('<span style="flex:1;display:flex;flex-direction:column;align-items:center;padding:4px;border:2px solid #1D1B3A;border-radius:12px;background:%s"><b class="h" style="font-size:24px">%s</b><span style="font-size:13px;font-weight:700">%s</span></span>' % c for c in [('#FFFFFF', '4', 'Antippen'), ('#FFF1C7', '6', 'Ordnen'), ('#FFC83D', '10', 'Selbst'), ('#FFE9D6', '0', 'geraten')])
 + '</div><div style="font-size:14px;margin-top:6px">Wild klicken: etwa 12 Punkte je Runde. Selbst messen, gemischt: etwa 138. In der heutigen App: etwa 50 gegen 90.</div></div>'
 + '</div></div></div>\n</x-dc>\n'
 + '<script type="text/x-dc" data-dc-script data-props=\'{"$preview":{"width":768,"height":1024}}\'>\nclass Component extends DCLogic {\n  renderVals() { return {}; }\n}\n</script>\n</body>\n</html>\n')
open(out + '/G-Ablauf.dc.html', 'w').write(ABLAUF)
print(len(PUNKTE), len(ABLAUF))
