import sys
sys.path.insert(0, sys.argv[1]); out = sys.argv[2]
from common import *
CSS = r"""
body{margin:0}
*{box-sizing:border-box}
button{font:inherit;color:inherit;cursor:pointer;border:0;background:none;padding:0}
.h{font-family:'Bricolage Grotesque','Trebuchet MS',sans-serif;font-weight:800;letter-spacing:-.01em;margin:0}
.cap13{font-size:13px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:#5A5C78}
.btn{display:flex;align-items:center;justify-content:center;min-height:56px;padding:0 22px;border-radius:18px;font-weight:700;font-size:18px;background:#FFC83D;color:#15173A}
.dot{flex:none;width:30px;height:30px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:15px;color:#15173A}
.pill{padding:6px 12px;border-radius:999px;font-size:14px;font-weight:700;color:#15173A}
.nd{position:absolute;top:13px;width:30px;height:30px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:15px;color:#15173A}
"""
def sw(c, name, ink='#15173A', bd=''):
    return '<div style="display:flex;flex-direction:column;gap:4px;font-size:13px;line-height:1.25"><div style="height:52px;border-radius:14px;background:%s;%s"></div><b>%s</b><span style="color:#5A5C78">%s</span></div>' % (c, bd, name, c)
def sample(kind, label, sub):
    # kind: list of (lane, color, locked) nodes, capsule style
    lanes = {'solo': [(0,'#FF93B8')], 'mix': [(0,'#FFC83D'),(1,'#5FE3C0'),(2,'#FF93B8')], 'bonus': [(0,'#FFC83D')], 'lock': [(0,'#9FB6FF'),(1,'#9FB6FF')]}[kind]
    lock = kind == 'lock'
    n = len(lanes); w = (n - 1) * 44 + 42
    cap = 'background:%s;border:%s' % (('transparent','2px dashed #5C64B8') if lock else (('#FFFFFF','2px solid transparent') if kind == 'mix' else ('rgba(255,255,255,.16)','2px solid transparent')))
    s = '<div style="display:flex;flex-direction:column;gap:6px;align-items:flex-start"><div style="position:relative;width:%dpx;height:56px">' % w
    for i, (l, c) in enumerate(lanes):
        s += '<span style="position:absolute;left:%dpx;top:0;width:4px;height:56px;border-radius:2px;background:%s;opacity:%s"></span>' % (19 + i * 44, c if not lock else ['#FFC83D','#9FB6FF'][i], '.35' if lock else '1')
    s += '<span style="position:absolute;left:0;top:8px;width:%dpx;height:40px;border-radius:20px;%s"></span>' % (w, cap)
    for i, (l, c) in enumerate(lanes):
        num = {'solo': 3, 'bonus': 1}.get(kind, i + 1) if not lock else [1, 4][i]
        col = c if not lock else ['#FFC83D','#9FB6FF'][i]
        s += '<span class="nd" style="left:%dpx;background:%s;border:2px solid %s;color:%s">%d</span>' % (6 + i * 44, '#171A45' if lock else col, col, col if lock else '#15173A', num)
    s += '</div><b style="font-size:15px;color:#FFFFFF">%s</b><span style="font-size:13px;color:#C3C8F2;line-height:1.25">%s</span></div>' % (label, sub)
    return s
MODS = [('wissen','Wissen lesen'),('karten','Lernkarten'),('erkennen','Erkennen'),('zeichnen','Zeichnen'),('messen','Messen'),('schaetzen','Schätzen'),('zeit','Zeitrunde'),('test','Test mit Note'),('duell','Duell')]
RANKS = [('staub','Sternenstaub'),('meteor','Meteor'),('komet','Komet'),('planet','Planet'),('pulsar','Pulsar'),('supernova','Supernova'),('galaxis','Galaxis-Legende')]
BODY = ('<div style="width:768px;height:1120px;position:relative;overflow:hidden;font-family:' + BODYFONT + ';font-size:16px;line-height:1.4;background:#FBF8F1;color:#15173A;padding:28px 32px;display:flex;flex-direction:column;gap:16px">'
 + '<div><span class="cap13">Entwurf E · Stilblatt</span><h1 class="h" style="font-size:36px;line-height:1.05">Flugkarte</h1><p style="margin:4px 0 0;font-size:17px;color:#3D3F63">Ein Grunddesign für alle Fächer: helle Karten für alles zum Lesen und Tippen, eine farbige Bühne für das Thema.</p></div>'
 + '<div style="display:grid;grid-template-columns:repeat(9, minmax(0, 1fr));gap:10px">'
 + sw('#171A45','Nacht') + sw('#FBF8F1','Papier', bd='border:1px solid #CFC8B6') + sw('#15173A','Tinte') + sw('#FFC83D','Sternengelb') + sw('#F47B20','Krabbi')
 + sw('#FFC83D','Paket 1') + sw('#5FE3C0','Paket 2') + sw('#FF93B8','Paket 3') + sw('#9FB6FF','Paket 4') + '</div>'
 + '<div style="display:grid;grid-template-columns:repeat(2, minmax(0, 1fr));gap:16px">'
 + '<div style="background:#FFFFFF;border-radius:20px;padding:14px 18px"><span class="cap13">Überschriften · Bricolage Grotesque</span><div class="h" style="font-size:30px;line-height:1.1;margin-top:4px">Welche Winkelart ist das?</div><span class="cap13" style="display:block;margin-top:10px">Lesetext · Atkinson Hyperlegible</span><p style="margin:4px 0 0;font-size:17px">Der Bogen geht über die gerade Linie hinaus. Gut unterscheidbar: I l 1 · O 0 · rn m</p></div>'
 + '<div style="background:#FFFFFF;border-radius:20px;padding:14px 18px;display:flex;flex-direction:column;gap:10px"><span class="cap13">Knöpfe · mindestens 56 px hoch</span><div style="display:flex;gap:10px"><button type="button" class="btn" style="flex:1">Weiterfliegen</button><button type="button" class="btn" style="flex:1;background:#FFFFFF;border:2px solid #15173A">Noch einmal</button></div><div style="display:flex;gap:10px"><button type="button" class="btn" style="flex:1;background:#15173A;color:#FFFFFF">Weiter</button><button type="button" class="btn" style="flex:1;background:#E4DFD2;color:#5A5C78">Prüfen</button></div></div>'
 + '</div>'
 + '<div style="display:grid;grid-template-columns:repeat(2, minmax(0, 1fr));gap:16px">'
 + '<div style="background:#FFFFFF;border-radius:20px;padding:14px 18px"><span class="cap13">Lernstand · immer als Wort</span><div style="display:grid;grid-template-columns:repeat(2, minmax(0, 1fr));gap:8px;margin-top:8px">'
 + '<div style="display:flex;align-items:center;gap:10px"><span class="dot" style="background:#FFFFFF;border:2px dashed #5A5C78">4</span><b>neu</b></div>'
 + '<div style="display:flex;align-items:center;gap:10px"><span class="dot" style="background:#FF93B8">3</span><b>noch üben</b></div>'
 + '<div style="display:flex;align-items:center;gap:10px"><span class="dot" style="background:#5FE3C0">2</span><b>sicher</b></div>'
 + '<div style="display:flex;align-items:center;gap:10px"><span class="dot" style="background:#FFC83D">1</span><b>wieder dran</b></div></div></div>'
 + '<div style="background:#FFFFFF;border-radius:20px;padding:14px 18px"><span class="cap13">Punkte-Münzen und Rückmeldung</span><div style="display:flex;flex-wrap:wrap;gap:8px;margin-top:8px"><span class="pill" style="background:#FFC83D">volle Punkte</span><span class="pill" style="background:#FFA366">+20 % Bonus</span><span class="pill" style="background:#E4DFD2">wenige Punkte</span><span class="pill" style="background:#FFFFFF;border:2px dashed #5A5C78">keine Punkte</span></div>'
 + '</div>'
 + '</div>'
 + '<div style="background:#171A45;border-radius:20px;padding:14px 20px 16px"><span class="cap13" style="color:#C3C8F2">Zeichen der Flugkarte · Leuchtspur = Paket</span><div style="display:grid;grid-template-columns:repeat(4, minmax(0, 1fr));gap:14px;margin-top:10px">'
 + sample('solo', 'Allein', 'Ein Paket, eine Spur') + sample('mix', 'Gemischt', 'Spuren laufen zusammen') + sample('bonus', 'Nachleuchten', 'Wieder dran, +20 %') + sample('lock', 'Noch zu', 'Sichtbar, nicht überspringbar') + '</div></div>'
 + '<div style="background:#FFFFFF;border-radius:20px;padding:14px 18px"><span class="cap13">Lernformen · Liniensymbol mit Wort</span><div style="display:grid;grid-template-columns:repeat(9, minmax(0, 1fr));gap:6px;margin-top:8px">'
 + ''.join('<div style="display:flex;flex-direction:column;align-items:center;gap:4px;text-align:center;font-size:13px;font-weight:700;line-height:1.2"><span style="width:44px;height:44px;border-radius:14px;background:#F1ECDF;display:flex;align-items:center;justify-content:center">%s</span>%s</div>' % (icon(k, 24), n) for k, n in MODS) + '</div></div>'
 + '<div style="display:grid;grid-template-columns:2.2fr 1fr;gap:16px">'
 + '<div style="background:#171A45;border-radius:20px;padding:14px 16px"><span class="cap13" style="color:#C3C8F2">Ränge im Weltraum</span><div style="display:grid;grid-template-columns:repeat(7, minmax(0, 1fr));gap:4px;margin-top:8px">'
 + ''.join('<div style="display:flex;flex-direction:column;align-items:center;gap:2px;text-align:center;font-size:13px;font-weight:700;line-height:1.15;color:#FFFFFF">%s%s</div>' % (rank(k, 40, '#FFFFFF'), n) for k, n in RANKS) + '</div></div>'
 + '<div style="background:#FFFFFF;border-radius:20px;padding:10px 14px;display:flex;align-items:center;gap:8px">' + krabbi(84, 'none', label='Krabbi ohne Kostüm') + '<div><span class="cap13">Krabbi</span><p style="margin:2px 0 0;font-size:14px;line-height:1.3">Rund, zwei Stielaugen, Scheren. Das Kostüm kommt vom Thema.</p></div></div>'
 + '</div></div>')
JS = "class Component extends DCLogic {\n  renderVals() { return {}; }\n}"
open(out, 'w').write(page('E · Flugkarte · Stilblatt', CSS, BODY, JS, '{"$preview":{"width":768,"height":1120}}'))
