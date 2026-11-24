import sys, json
sys.path.insert(0, sys.argv[1]); out = sys.argv[2]
from common import *

CSS = r"""
.tabs{position:absolute;left:20px;right:20px;bottom:16px;height:76px;background:#FFFBF2;border:3px solid #1D1B3A;border-radius:24px;box-shadow:0 5px 0 #1D1B3A;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));overflow:hidden}
.tab{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:3px;font-size:14px;font-weight:700;color:#4F4C6E;text-align:center}
.tab.on{background:#FFC83D;color:#1D1B3A}
.band{position:relative;flex:none;background:#1E2257;color:#FFFFFF;overflow:hidden}
.rk{display:flex;align-items:center;gap:8px;min-height:48px;padding:4px 14px 4px 6px;border:3px solid #1D1B3A;border-radius:999px;background:#FFC83D;color:#1D1B3A;font-weight:700;font-size:15px;box-shadow:0 3px 0 #0E1033}
.sug{position:relative;display:flex;flex-direction:column;gap:8px;padding:14px 14px 14px;min-height:262px;background:#FFFBF2;border:3px solid #1D1B3A;border-radius:22px;box-shadow:0 5px 0 #1D1B3A}
.sug:active{transform:translateY(3px);box-shadow:0 2px 0 #1D1B3A}
.tag{align-self:flex-start;padding:3px 10px;border-radius:999px;border:2px solid #1D1B3A;font-size:13px;font-weight:700}
.tok{display:flex;flex-direction:column;align-items:center;gap:2px;padding:8px 4px;border-radius:16px;text-align:center;position:relative}
.tok:hover{background:rgba(29,27,58,.06)}
.tn{font-size:14px;font-weight:700;line-height:1.15}
.tw{font-size:13px;color:#4F4C6E;line-height:1.15}
.due{position:absolute;top:4px;right:10px;display:flex;align-items:center;gap:3px;padding:1px 7px 1px 4px;border-radius:999px;background:#FFFFFF;border:2px solid #1D1B3A;font-size:11px;font-weight:700}
.sheet{position:absolute;left:0;right:0;bottom:0;max-height:930px;overflow-y:auto;background:#FFFBF2;border-top:3px solid #1D1B3A;border-radius:30px 30px 0 0;padding:22px 32px 30px;display:flex;flex-direction:column;gap:14px}
.scrim{position:absolute;left:0;top:0;width:768px;height:1024px;background:rgba(14,16,51,.55);cursor:default}
.ans{display:flex;align-items:center;gap:12px;min-height:76px;padding:0 20px;border:3px solid #1D1B3A;border-radius:20px;background:#FFFFFF;box-shadow:0 5px 0 #1D1B3A;font-size:21px;font-weight:700;text-align:left}
.ans.sel{background:#DDE6FF;border-color:#2B3FA8;box-shadow:0 5px 0 #2B3FA8}
.ans.ok{background:#DDF5E7;border-color:#12704A;box-shadow:0 5px 0 #12704A;color:#0C5A3A}
.ans.no{background:#FFE9D6;border:3px dashed #B4500A;box-shadow:none;color:#8A3D07}
.ans.dim{opacity:.6;box-shadow:none}
.key{display:flex;align-items:center;justify-content:center;min-height:64px;border:3px solid #1D1B3A;border-radius:16px;background:#FFFFFF;box-shadow:0 4px 0 #1D1B3A;font-family:'Baloo 2',sans-serif;font-weight:800;font-size:28px}
.key:active{transform:translateY(2px);box-shadow:0 2px 0 #1D1B3A}
.fb{position:absolute;left:0;right:0;bottom:0;padding:20px 32px 28px;border-top:3px solid #1D1B3A;display:flex;flex-direction:column;gap:10px}
.dot{width:30px;height:30px;border-radius:50%;display:flex;align-items:center;justify-content:center;flex:none}
.mrow{display:flex;align-items:center;gap:12px;width:100%;min-height:68px;padding:8px 14px;border:3px solid #1D1B3A;border-radius:18px;background:#FFFFFF;box-shadow:0 4px 0 #1D1B3A;text-align:left}
.mrow.on{background:#FFE7A3}
.mrow:disabled{background:transparent;border:3px dashed #8F8BA8;box-shadow:none;color:#4F4C6E}
.seg{display:grid;gap:8px}
.sb{min-height:52px;border:3px solid #1D1B3A;border-radius:14px;background:#FFFFFF;font-weight:700;font-size:16px;text-align:center}
.sb.on{background:#FFC83D;box-shadow:0 4px 0 #1D1B3A}
.line{display:flex;align-items:flex-start;gap:12px;padding:8px 0;border-bottom:2px dotted #C9C3B0}
.hk{display:flex;align-items:center;gap:12px;padding:10px 12px;border-radius:16px;border:2px solid #1D1B3A;background:#FFFFFF}
.hk.off{border-style:dashed;border-color:#8F8BA8;background:transparent}
.scroll{flex:1;min-height:0;overflow-y:auto}
"""

def band_stars(w, h, n, seed):
    return '<svg width="%d" height="%d" viewBox="0 0 %d %d" aria-hidden="true" style="position:absolute;left:0;top:0">%s</svg>' % (w, h, w, h, stars_bg(w, h, n, seed))

PLANET = ('<svg width="150" height="150" viewBox="0 0 150 150" aria-hidden="true" style="position:absolute;right:-30px;top:20px">'
          '<circle cx="75" cy="75" r="46" fill="#7C6CF0" stroke="#0E1033" stroke-width="3"></circle>'
          '<circle cx="60" cy="60" r="9" fill="#9C90FF"></circle><circle cx="92" cy="92" r="6" fill="#9C90FF"></circle>'
          '<ellipse cx="75" cy="78" rx="72" ry="15" transform="rotate(-18 75 78)" fill="none" stroke="#FFC83D" stroke-width="5"></ellipse></svg>')
KOMET = ('<svg width="90" height="40" viewBox="0 0 90 40" aria-hidden="true" class="komet" style="position:absolute;left:0;top:30px">'
         '<path d="M0 30L70 14 74 26Z" fill="#FFE9A8" opacity=".7"></path><circle cx="74" cy="20" r="8" fill="#FFC83D" stroke="#0E1033" stroke-width="2"></circle></svg>')
HORIZON = '<svg width="768" height="34" viewBox="0 0 768 34" aria-hidden="true" style="position:absolute;left:0;bottom:-1px;display:block"><path d="M0 34V22Q384 -8 768 22V34Z" fill="#EEF0FA"></path></svg>'
GROUND = '<svg width="768" height="1024" viewBox="0 0 768 1024" aria-hidden="true" style="position:absolute;left:0;top:0">%s</svg>' % stars_bg(768, 1024, 60, 11, '#8E8BD8', 0.45, False)

def rankchip(act='goIch'):
    return ('<button type="button" class="rk" onClick="{{%s}}" aria-label="Dein Rang: {{rk.name}}, {{points}} Punkte">' % act
            + '<span style="display:block;width:36px;height:36px;border-radius:50%;background:#FFFBF2;border:2px solid #1D1B3A;padding:2px">'
            + ''.join('<sc-if value="{{rk.is_%s}}" hint-placeholder-val="{{ false }}">%s</sc-if>' % (k, rank(k, 28)) for k in RANK_SVG)
            + '</span><span style="display:flex;flex-direction:column;line-height:1.1"><b>{{rk.name}}</b><span style="font-size:13px">{{points}} Punkte</span></span></button>')

def tabs():
    t = [('heute', 'home', 'Heute', 'goHeute'), ('fach', 'grid', 'Fächer', 'goFach'), ('gem', 'people', 'Gemeinsam', 'goGem'), ('ich', 'user', 'Ich', 'goIch')]
    return '<nav class="tabs" aria-label="Hauptbereiche">' + ''.join(
        '<button type="button" class="{{tabc.%s}}" onClick="{{%s}}">%s%s</button>' % (k, act, ic(i, 26), lab) for k, i, lab, act in t) + '</nav>'

def bubble(hole, extra=''):
    return '<div class="bubble" style="flex:1;%s">{{%s}}</div>' % (extra, hole)

# ---------------- HEUTE ----------------
HEUTE = ('<sc-if value="{{is.heute}}" hint-placeholder-val="{{ true }}"><div class="scr">'
 + '<div class="band" style="height:262px;padding:24px 32px 0">' + band_stars(768, 262, 46, 4) + PLANET + KOMET
 + '<div style="position:relative;display:flex;justify-content:space-between;align-items:flex-start;gap:16px">'
 + '<div><span class="cap" style="color:#C9CCFF">Montag, 16. November</span><h1 class="h" style="font-size:40px;margin-top:2px">Hallo Robin!</h1></div>'
 + rankchip() + '</div>'
 + '<div style="position:relative;display:flex;align-items:flex-end;gap:12px;margin-top:14px;padding-right:60px">'
 + '<span class="kr" style="display:block">' + krabbi(92, 'Krabbi im Raumanzug') + '</span>'
 + '<div class="bubble" style="flex:1;color:#1D1B3A;margin-bottom:22px">{{heuteSay}}</div></div>' + HORIZON + '</div>'
 + '<div style="position:relative;flex:1;padding:8px 32px 110px;display:flex;flex-direction:column;gap:14px">'
 # Tagesziel
 + '<div class="card" style="display:flex;align-items:center;gap:16px;padding:12px 18px">'
 + '<div style="flex:1"><span class="cap muted">Dein Tagesziel</span><div class="h" style="font-size:22px">{{goalText}}</div><div class="muted" style="font-size:15px">{{goalSub}}</div></div>'
 + '<div style="display:flex;gap:6px" role="img" aria-label="{{goalText}}"><sc-for list="{{goalStars}}" as="g" hint-placeholder-count="3">'
 + '<svg width="44" height="44" viewBox="0 0 24 24" aria-hidden="true"><path d="%s" fill="{{g.fill}}" stroke="#1D1B3A" stroke-width="1.6" stroke-linejoin="round" stroke-dasharray="{{g.dash}}"></path></svg>' % ICON['star']
 + '</sc-for></div></div>'
 # Als Nächstes / geschafft
 + '<sc-if value="{{hasNext}}" hint-placeholder-val="{{ true }}"><div class="card" style="padding:16px 20px 18px;display:flex;flex-direction:column;gap:10px;border-width:4px;background:#FFFFFF">'
 + '<div style="display:flex;align-items:center;gap:10px"><span class="cap" style="color:#2B3FA8">Als Nächstes</span><span class="chip" style="background:#FFF1C7">Krabbis Tipp</span></div>'
 + '<div style="display:flex;align-items:center;gap:14px"><span style="display:flex;width:56px;height:56px;border-radius:16px;border:3px solid #1D1B3A;background:#FFE7A3;align-items:center;justify-content:center">' + ich('next.icon', 30) + '</span>'
 + '<div style="flex:1"><div class="h" style="font-size:27px">{{next.title}}</div><div class="muted" style="font-size:16px">{{next.line}}</div></div></div>'
 + '<div style="display:flex;gap:8px;flex-wrap:wrap"><span class="chip">' + ich('next.hicon', 18) + '{{next.goal}}</span><span class="chip" style="background:#FFF1C7">{{next.coin}}</span></div>'
 + '<button type="button" class="btn" onClick="{{goLos}}" style="margin-top:4px">Los' + ic('arrow', 24, 3) + '</button></div></sc-if>'
 + '<sc-if value="{{allDone}}" hint-placeholder-val="{{ false }}"><div class="card" style="padding:18px 20px;display:flex;flex-direction:column;gap:10px;background:#DDF5E7;border-color:#12704A;box-shadow:0 5px 0 #12704A">'
 + '<div class="h" style="font-size:27px;color:#0C5A3A">Geschafft für heute!</div><div style="font-size:17px">{{doneText}}</div>'
 + '<div style="display:flex;gap:10px"><button type="button" class="btn2" onClick="{{goFach}}">Trotzdem weiterüben</button></div></div></sc-if>'
 + '<div style="display:flex;gap:8px;align-items:center"><span class="chip" style="background:#FFFFFF">' + ic('clock', 18) + 'Mathe-Arbeit in 6 Tagen</span><span class="muted" style="font-size:15px">Krabbi plant mehr Mischen ein.</span></div>'
 + '<h2 class="h" style="font-size:22px;margin-top:2px">Deine Fächer</h2>'
 + '<div style="display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px">'
 + '<button type="button" class="card" onClick="{{goFach}}" style="display:flex;align-items:center;gap:12px;padding:10px 14px;min-height:72px"><span style="display:flex;width:44px;height:44px;border-radius:50%;background:#1E2257;align-items:center;justify-content:center">' + rank('komet', 30) + '</span><span style="flex:1"><b style="display:block;font-size:17px">Mathe · Winkel-Akademie</b><span class="muted" style="font-size:14px">{{mathLine}}</span></span></button>'
 + ''.join('<div class="card" style="display:flex;align-items:center;gap:12px;padding:10px 14px;min-height:72px;box-shadow:0 3px 0 #1D1B3A"><span style="display:block;width:44px;height:44px;border-radius:50%%;background:%s;border:2px solid #1D1B3A"></span><span style="flex:1"><b style="display:block;font-size:17px">%s</b><span class="muted" style="font-size:14px">%s</span></span></div>' % c for c in [
     ('#2E9C93', 'NWT · Zauberschule', 'neu: Wasserkreislauf'), ('#E86A4E', 'Englisch · Küsten-Crew', 'Unit 3: 2 Pakete wieder dran'), ('#B07A3B', 'Deutsch · Detektiv-Büro', 'alles sicher, prima')])
 + '</div><p class="muted" style="margin:0;font-size:13px">Im Entwurf ist nur Mathe ausgearbeitet.</p>'
 + '</div>' + tabs() + '</div></sc-if>')

# ---------------- FACH ----------------
SUG = ('<sc-for list="{{sugg}}" as="c" hint-placeholder-count="3"><button type="button" class="sug" onClick="{{c.open}}" aria-label="{{c.aria}}">'
 + '<span class="tag" style="background:{{c.tagBg}}">{{c.tag}}</span>'
 + '<sc-if value="{{c.tip}}" hint-placeholder-val="{{ false }}"><span style="position:absolute;top:-14px;right:12px;padding:2px 10px;border-radius:999px;background:#FFC83D;border:2px solid #1D1B3A;font-size:12px;font-weight:700">Krabbis Tipp</span></sc-if>'
 + '<span style="display:flex;align-items:center;gap:8px"><span style="display:flex;width:40px;height:40px;border-radius:12px;border:2px solid #1D1B3A;background:#FFFFFF;align-items:center;justify-content:center">' + ich('c.icon', 24) + '</span><span style="font-size:13px;font-weight:700;line-height:1.2">{{c.mod}}<br><span class="muted" style="font-weight:400">{{c.art}}</span></span></span>'
 + '<b class="h" style="font-size:20px;font-weight:700">{{c.title}}</b>'
 + '<span style="display:flex;gap:2px;align-items:center"><sc-for list="{{c.toks}}" as="t" hint-placeholder-count="2">' + token('t', 34, 14) + '</sc-for><span class="muted" style="font-size:13px;margin-left:4px">{{c.mixw}}</span></span>'
 + '<span style="display:flex;align-items:center;gap:6px;font-size:14px;font-weight:700">' + ich('c.hicon', 18) + '{{c.goal}}</span>'
 + '<span style="margin-top:auto;padding:5px 10px;border-radius:12px;background:{{c.coinBg}};font-size:14px;font-weight:700;border:2px solid #1D1B3A">{{c.coin}}</span>'
 + '<sc-if value="{{c.done}}" hint-placeholder-val="{{ false }}"><span style="display:flex;align-items:center;gap:4px;font-size:13px;font-weight:700;color:#12704A">' + ic('check', 16, 3) + 'heute schon gemacht</span></sc-if>'
 + '</button></sc-for>')

TOKBTN = ('<button type="button" class="tok" onClick="{{t.open}}" aria-label="{{t.aria}}">' + token('t', 64)
 + '<sc-if value="{{t.due}}" hint-placeholder-val="{{ false }}"><span class="due">' + ic('clock', 12, 3) + 'wieder dran</span></sc-if>'
 + '<span class="tn">{{t.name}}</span><span class="tw">{{t.word}}</span></button>')

FACH = ('<sc-if value="{{is.fach}}" hint-placeholder-val="{{ false }}"><div class="scr">'
 + '<div class="band" style="height:150px;padding:20px 32px 0">' + band_stars(768, 150, 30, 8) + KOMET
 + '<div style="position:relative;display:flex;justify-content:space-between;align-items:flex-start;gap:12px">'
 + '<div><span class="cap" style="color:#C9CCFF">Mathe · Weltraum</span><h1 class="h" style="font-size:36px">Winkel-Akademie</h1>'
 + '<div style="display:flex;align-items:center;gap:8px;margin-top:4px;font-size:14px;color:#E3E4FF"><span style="display:block;width:150px;height:10px;border-radius:5px;background:#3A3F86;overflow:hidden"><span style="display:block;height:10px;width:{{rk.pct}};background:#FFC83D"></span></span>{{rk.toNext}}</div></div>'
 + rankchip() + '</div>' + HORIZON + '</div>'
 + '<div class="scroll" style="position:relative;padding:6px 32px 112px;display:flex;flex-direction:column;gap:14px">'
 + '<div style="display:flex;align-items:flex-end;gap:10px"><span class="kr" style="display:block">' + krabbi(70) + '</span>' + bubble('fachSay', 'margin-bottom:10px') + '</div>'
 + '<div style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;margin-top:6px">' + SUG + '</div>'
 + '<div style="display:flex;align-items:baseline;justify-content:space-between;margin-top:8px"><h2 class="h" style="font-size:24px">Deine Pakete</h2>'
 + '<span class="muted" style="font-size:14px">Ring: Kennen · Können · Behalten</span></div>'
 + '<sc-for list="{{groups}}" as="g" hint-placeholder-count="2"><div class="card" style="padding:10px 12px 6px;box-shadow:0 3px 0 #1D1B3A">'
 + '<div style="display:flex;justify-content:space-between;align-items:center;padding:0 6px"><b style="font-size:16px">{{g.t}} <span class="muted" style="font-weight:400">· {{g.sub}}</span></b><span class="muted" style="font-size:14px">{{g.sum}}</span></div>'
 + '<div style="display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:4px"><sc-for list="{{g.items}}" as="t" hint-placeholder-count="4">' + TOKBTN + '</sc-for></div></div></sc-for>'
 + '<div style="display:flex;gap:12px;flex-wrap:wrap">'
 + '<sc-if value="{{showFrei}}" hint-placeholder-val="{{ true }}"><button type="button" class="btn2" onClick="{{goFrei}}">' + ic('sliders', 22) + 'Selbst zusammenstellen</button></sc-if>'
 + '<sc-if value="{{gefuehrt}}" hint-placeholder-val="{{ false }}"><span class="chip" style="white-space:normal;padding:8px 12px">' + ic('info', 18) + 'Deine Eltern haben „Geführt“ eingestellt: Du wählst aus Krabbis drei Vorschlägen.</span></sc-if>'
 + '<button type="button" class="btn2" onClick="{{goRegeln}}">' + ic('star', 22) + 'So bekommst du Punkte</button></div>'
 + '</div>' + tabs()
 # Vorschau
 + '<sc-if value="{{sh.vor}}" hint-placeholder-val="{{ false }}"><button type="button" class="scrim" onClick="{{closeSheet}}" aria-label="Schließen"></button>'
 + '<div class="sheet" role="dialog" aria-label="Vorschau: {{v.title}}">'
 + '<div style="display:flex;justify-content:space-between;align-items:flex-start;gap:12px"><div><span class="tag" style="background:{{v.tagBg}}">{{v.tag}}</span><h2 class="h" style="font-size:30px;margin-top:8px">{{v.title}}</h2></div>'
 + '<button type="button" class="btn2" onClick="{{closeSheet}}" aria-label="Schließen" style="min-height:48px;padding:0 12px">' + ic('close', 22, 3) + '</button></div>'
 + '<div style="display:flex;align-items:center;gap:12px"><span style="display:flex;width:48px;height:48px;border-radius:14px;border:3px solid #1D1B3A;background:#FFE7A3;align-items:center;justify-content:center">' + ich('v.icon', 28) + '</span>'
 + '<div><b style="font-size:18px">{{v.mod}}</b><div class="muted" style="font-size:15px">{{v.art}} · {{v.count}}</div></div></div>'
 + '<div><span class="cap muted">Was kommt dran</span><div style="display:flex;height:40px;margin-top:6px;border:3px solid #1D1B3A;border-radius:12px;overflow:hidden"><sc-for list="{{v.bar}}" as="b" hint-placeholder-count="3"><span style="display:flex;align-items:center;justify-content:center;width:{{b.w}};background:{{b.col}};color:#FFFFFF;font-weight:700;font-size:14px;border-right:2px solid #1D1B3A">{{b.t}}</span></sc-for></div></div>'
 + '<div style="display:flex;align-items:flex-end;gap:10px">' + krabbi(56) + bubble('v.why') + '</div>'
 + '<div class="hk" style="background:#FFF1C7">' + ich('v.hicon', 26) + '<div><b>Möglicher Haken</b><div style="font-size:16px">{{v.goal}}</div></div></div>'
 + '<div><span class="cap muted">Punkte je richtiger Antwort</span><sc-for list="{{v.pts}}" as="q" hint-placeholder-count="3"><div class="line">' + token('q.tok', 36, 14) + '<div style="flex:1"><b style="font-size:16px">{{q.name}}</b><div class="muted" style="font-size:14px">{{q.why}}</div></div><b class="h" style="font-size:22px">{{q.v}}</b></div></sc-for></div>'
 + '<div style="display:flex;gap:12px;margin-top:4px"><button type="button" class="btn" onClick="{{v.start}}" style="flex:1">Starten' + ic('arrow', 24, 3) + '</button><button type="button" class="btn2" onClick="{{closeSheet}}">Andere Wahl</button></div>'
 + '</div></sc-if>'
 # Paket-Blatt
 + '<sc-if value="{{sh.pkg}}" hint-placeholder-val="{{ false }}"><button type="button" class="scrim" onClick="{{closeSheet}}" aria-label="Schließen"></button>'
 + '<div class="sheet" role="dialog" aria-label="Paket {{pp.tok.nr}}: {{pp.tok.name}}">'
 + '<div style="display:flex;gap:14px;align-items:center">' + token('pp.tok', 84, 24) + '<div style="flex:1"><span class="cap muted">Paket {{pp.tok.nr}} · {{pp.tok.word}}</span><h2 class="h" style="font-size:30px">{{pp.tok.name}}</h2><div class="muted" style="font-size:14px">Im Heft: {{pp.src}}</div></div>'
 + '<button type="button" class="btn2" onClick="{{closeSheet}}" aria-label="Schließen" style="min-height:48px;padding:0 12px">' + ic('close', 22, 3) + '</button></div>'
 + '<div class="card" style="padding:12px 16px;box-shadow:none;border-width:2px"><b>Lernziel</b><div style="font-size:17px">{{pp.goal}}</div></div>'
 + '<div><span class="cap muted">Drei Haken, dann ist das Paket sicher</span><div style="display:flex;flex-direction:column;gap:8px;margin-top:6px"><sc-for list="{{pp.hk}}" as="k" hint-placeholder-count="3">'
 + '<div class="{{k.cls}}"><span style="display:flex;width:42px;height:42px;border-radius:50%;border:2px solid #1D1B3A;background:{{k.bg}};align-items:center;justify-content:center">' + ich('k.icon', 24) + '</span>'
 + '<div style="flex:1"><b style="font-size:17px">{{k.n}}</b> <span class="muted" style="font-size:14px">{{k.state}}</span><div style="font-size:15px">{{k.how}}</div><div style="display:flex;gap:6px;flex-wrap:wrap;margin-top:4px"><sc-for list="{{k.mods}}" as="m" hint-placeholder-count="2"><span class="chip" style="font-size:13px;border-width:1.5px">{{m}}</span></sc-for></div></div></div>'
 + '</sc-for></div></div>'
 + '<div style="display:flex;gap:12px"><button type="button" class="btn2" onClick="{{pp.read}}">' + ic('book', 22) + 'Wissen lesen</button>'
 + '<sc-if value="{{pp.canPlay}}" hint-placeholder-val="{{ true }}"><button type="button" class="btn" onClick="{{pp.play}}" style="flex:1">{{pp.playT}}</button></sc-if>'
 + '<sc-if value="{{pp.noPlay}}" hint-placeholder-val="{{ false }}"><span class="muted" style="align-self:center;font-size:14px">Übungen für dieses Paket sind im Entwurf nicht ausgearbeitet.</span></sc-if></div>'
 + '</div></sc-if>'
 + '</div></sc-if>')

# ---------------- FREI ----------------
FREI = ('<sc-if value="{{is.frei}}" hint-placeholder-val="{{ false }}"><div class="scr">'
 + '<div style="flex:none;display:flex;align-items:center;gap:14px;padding:20px 32px 12px;background:#FFFBF2;border-bottom:3px solid #1D1B3A">'
 + '<button type="button" class="btn2" onClick="{{goFach}}" style="min-height:48px;padding:0 14px">' + ic('back', 22, 3) + 'Zurück</button>'
 + '<div><span class="cap muted">Winkel-Akademie</span><h1 class="h" style="font-size:30px">Selbst zusammenstellen</h1></div></div>'
 + '<div class="scroll" style="padding:14px 32px 20px;display:flex;flex-direction:column;gap:12px">'
 + '<div style="display:flex;align-items:flex-end;gap:10px">' + krabbi(56) + '<div class="bubble" style="flex:1">Hier ist alles offen. Bei jeder Lernform steht, was sie dir gerade bringt.</div></div>'
 + '<div style="display:flex;align-items:center;gap:10px"><span style="display:flex;width:34px;height:34px;border-radius:50%;border:3px solid #1D1B3A;background:#FFC83D;align-items:center;justify-content:center;font-family:\'Baloo 2\';font-weight:800">1</span><h2 class="h" style="font-size:22px">Was übst du?</h2><span class="muted" style="font-size:14px">ein Paket oder mehrere, höchstens 6</span></div>'
 + '<div class="card" style="padding:6px;box-shadow:0 3px 0 #1D1B3A;display:grid;grid-template-columns:repeat(8,minmax(0,1fr));gap:2px"><sc-for list="{{fr.toks}}" as="t" hint-placeholder-count="8">'
 + '<button type="button" class="tok" onClick="{{t.toggle}}" aria-pressed="{{t.on}}" aria-label="{{t.aria}}" style="background:{{t.bg}};padding:6px 2px">' + token('t', 52, 18) + '<span class="tw" style="font-weight:700;color:#1D1B3A">{{t.short}}</span><span class="tw">{{t.word}}</span></button></sc-for></div>'
 + '<div style="display:flex;align-items:center;gap:10px;margin-top:4px"><span style="display:flex;width:34px;height:34px;border-radius:50%;border:3px solid #1D1B3A;background:#FFC83D;align-items:center;justify-content:center;font-family:\'Baloo 2\';font-weight:800">2</span><h2 class="h" style="font-size:22px">Wie übst du?</h2><span class="muted" style="font-size:14px">{{fr.mixText}}</span></div>'
 + '<sc-for list="{{fr.mods}}" as="m" hint-placeholder-count="6"><button type="button" class="{{m.cls}}" onClick="{{m.pick}}" disabled="{{m.dis}}" aria-pressed="{{m.on}}">'
 + '<span style="display:flex;width:42px;height:42px;border-radius:12px;border:2px solid currentColor;align-items:center;justify-content:center">' + ich('m.icon', 24) + '</span>'
 + '<span style="flex:1"><b style="display:block;font-size:17px">{{m.t}}</b><span style="font-size:14px">{{m.art}} · {{m.hk}}</span></span>'
 + '<span style="text-align:right;font-size:14px;max-width:190px"><b class="h" style="display:block;font-size:19px;font-weight:700">{{m.pv}}</b>{{m.ps}}</span></button></sc-for>'
 + '</div>'
 + '<div style="flex:none;padding:14px 32px 24px;background:#FFFBF2;border-top:3px solid #1D1B3A;display:flex;align-items:center;gap:16px">'
 + '<div style="flex:1"><b style="font-size:17px">{{fr.sum}}</b><div class="muted" style="font-size:14px">{{fr.sum2}}</div></div>'
 + '<button type="button" class="btn" onClick="{{fr.start}}" disabled="{{fr.noStart}}">Starten' + ic('arrow', 24, 3) + '</button></div>'
 + '</div></sc-if>')

# ---------------- ÜBUNG ----------------
UEB = ('<sc-if value="{{is.ueb}}" hint-placeholder-val="{{ false }}"><div class="scr">'
 + '<div style="flex:none;padding:18px 32px 14px;background:#FFFBF2;border-bottom:3px solid #1D1B3A;display:flex;flex-direction:column;gap:10px">'
 + '<div style="display:flex;align-items:center;gap:14px"><button type="button" class="btn2" onClick="{{quit}}" aria-label="Runde beenden" style="min-height:48px;padding:0 12px">' + ic('close', 22, 3) + '</button>'
 + '<div style="flex:1"><b class="h" style="font-size:22px;font-weight:700">{{u.mod}}</b><div class="muted" style="font-size:14px">{{u.sub}}</div></div>'
 + '<sc-if value="{{u.duel}}" hint-placeholder-val="{{ false }}"><span class="chip" style="font-size:16px;padding:6px 12px;background:#FFF1C7">Du {{me}} : {{kr}} Krabbi</span></sc-if>'
 + '<span class="muted" style="font-size:15px;font-weight:700">Aufgabe {{u.nr}} von {{u.total}}</span></div>'
 + '<div style="display:flex;gap:6px;align-items:center" role="img" aria-label="Fortschritt: Aufgabe {{u.nr}} von {{u.total}}"><sc-for list="{{u.dots}}" as="d" hint-placeholder-count="10">'
 + '<span class="dot" style="background:{{d.bg}};border:{{d.bd}};box-shadow:{{d.sh}}"><sc-if value="{{d.ok}}" hint-placeholder-val="{{ false }}">' + ic('check', 16, 3.4, '#FFFFFF') + '</sc-if></span></sc-for>'
 + '<span class="muted" style="font-size:13px;margin-left:6px">Farbe = Paket</span></div></div>'
 + '<div style="flex:1;min-height:0;padding:18px 32px 0;display:flex;flex-direction:column;gap:12px">'
 + '<div style="display:flex;align-items:center;gap:8px">' + token('u.tok', 34, 14) + '<span style="font-size:15px;font-weight:700">Paket {{u.tok.nr}} · {{u.tok.name}}</span><span class="chip" style="font-size:13px">{{u.tok.word}}</span><span class="chip" style="font-size:13px;background:#FFF1C7">{{u.art}}</span></div>'
 + '<div><h2 class="h" style="font-size:30px;font-weight:700">{{u.q}}</h2><div class="muted" style="font-size:17px;margin-top:2px">{{u.subq}}</div></div>'
 + '<sc-if value="{{u.hasFig}}" hint-placeholder-val="{{ true }}"><div class="card" style="align-self:center;padding:4px 10px;box-shadow:0 3px 0 #1D1B3A;background:#FFFFFF">'
 + '<svg width="360" height="{{u.figH}}" viewBox="{{u.vb}}" role="img" aria-label="{{u.figLabel}}"><path d="{{u.f.arc}}" fill="rgba(255,200,61,.35)" stroke="#E09A00" stroke-width="3"></path><path d="{{u.f.r1}}" stroke="#2B3FA8" stroke-width="5" stroke-linecap="round"></path><path d="{{u.f.r2}}" stroke="#2B3FA8" stroke-width="5" stroke-linecap="round"></path><circle cx="{{u.f.vx}}" cy="{{u.f.vy}}" r="6" fill="#1D1B3A"></circle><text x="{{u.f.lx}}" y="{{u.f.ly}}" text-anchor="middle" font-family="Baloo 2, sans-serif" font-weight="800" font-size="24" fill="#1D1B3A">{{u.f.lab}}</text></svg></div></sc-if>'
 # Antippen
 + '<sc-if value="{{u.tap}}" hint-placeholder-val="{{ false }}"><div style="display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px"><sc-for list="{{u.opts}}" as="o" hint-placeholder-count="4">'
 + '<button type="button" class="{{o.cls}}" onClick="{{o.pick}}" disabled="{{o.dis}}"><span style="display:flex;width:32px;height:32px;border-radius:50%;border:2px solid currentColor;align-items:center;justify-content:center;font-size:16px;flex:none">{{o.k}}</span>{{o.t}}</button></sc-for></div></sc-if>'
 # Zahlen
 + '<sc-if value="{{u.num}}" hint-placeholder-val="{{ false }}"><div style="display:flex;gap:18px;align-items:flex-start">'
 + '<div style="flex:1;display:flex;flex-direction:column;gap:8px"><span class="cap muted">Deine Antwort</span><div style="display:flex;align-items:center;justify-content:center;min-height:84px;border:3px solid #1D1B3A;border-radius:20px;background:{{u.inBg}};font-family:\'Baloo 2\';font-weight:800;font-size:44px">{{u.inp}}°</div>'
 + '<div class="muted" style="font-size:15px">' + ic('geo', 18) + ' Leg dein Geodreieck an den Bildschirm oder nimm das virtuelle.</div></div>'
 + '<div style="width:300px;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px"><sc-for list="{{keys}}" as="k" hint-placeholder-count="10"><button type="button" class="key" onClick="{{k.press}}" disabled="{{u.locked}}">{{k.t}}</button></sc-for>'
 + '<button type="button" class="key" onClick="{{del}}" disabled="{{u.locked}}" aria-label="Löschen">' + ic('del', 28, 2.4) + '</button></div></div></sc-if>'
 + '<sc-if value="{{u.asking}}" hint-placeholder-val="{{ true }}"><button type="button" class="btn" onClick="{{check}}" disabled="{{u.noCheck}}" style="margin-top:6px">Prüfen</button></sc-if>'
 + '</div>'
 # Rückmeldung
 + '<sc-if value="{{u.fb}}" hint-placeholder-val="{{ false }}"><div class="fb" style="background:{{u.fbBg}};border-top-color:{{u.fbBd}}" role="status">'
 + '<div style="display:flex;align-items:center;gap:14px">' + krabbi(64) + '<div style="flex:1"><div class="h" style="font-size:27px;color:{{u.fbInk}}">{{u.fbT}}</div><div style="font-size:17px;margin-top:2px">{{u.fbX}}</div></div>'
 + '<span class="chip" style="font-size:16px;padding:6px 12px;background:#FFFFFF;border-color:{{u.fbBd}}">{{u.fbP}}</span></div>'
 + '<div style="display:flex;gap:12px"><sc-if value="{{u.canRetry}}" hint-placeholder-val="{{ false }}"><button type="button" class="btn" onClick="{{retry}}" style="flex:1">Nochmal versuchen</button></sc-if>'
 + '<sc-if value="{{u.canNext}}" hint-placeholder-val="{{ true }}"><button type="button" class="btn" onClick="{{weiter}}" style="flex:1">{{u.nextT}}</button></sc-if></div></div></sc-if>'
 # Pause
 + '<sc-if value="{{pause}}" hint-placeholder-val="{{ false }}"><div class="scrim"></div><div class="card" role="dialog" aria-label="Kurze Pause" style="position:absolute;left:84px;right:84px;top:260px;padding:26px;display:flex;flex-direction:column;align-items:center;gap:14px;text-align:center">'
 + krabbi(110) + '<div class="h" style="font-size:28px">Lass uns langsamer machen</div><div style="font-size:18px">Du hast dreimal sehr schnell getippt, und es war falsch. Lies die nächste Frage in Ruhe. Ich warte, keine Eile.</div>'
 + '<button type="button" class="btn" onClick="{{unpause}}">Okay, in Ruhe weiter</button></div></sc-if>'
 + '</div></sc-if>')

# ---------------- WISSEN ----------------
WISSEN = ('<sc-if value="{{is.wissen}}" hint-placeholder-val="{{ false }}"><div class="scr">'
 + '<div style="flex:none;display:flex;align-items:center;gap:14px;padding:20px 32px 12px;background:#FFFBF2;border-bottom:3px solid #1D1B3A">'
 + '<button type="button" class="btn2" onClick="{{w.back}}" style="min-height:48px;padding:0 14px">' + ic('back', 22, 3) + 'Zurück</button>'
 + '<div><span class="cap muted">Wissen · Paket {{w.tok.nr}}</span><h1 class="h" style="font-size:30px">{{w.tok.name}}</h1></div></div>'
 + '<div class="scroll" style="padding:18px 32px;display:flex;flex-direction:column;gap:14px">'
 + '<div style="display:flex;align-items:flex-end;gap:10px">' + krabbi(64) + bubble('w.say') + '</div>'
 + '<sc-for list="{{w.facts}}" as="f" hint-placeholder-count="3"><div class="card" style="display:flex;gap:16px;align-items:center;padding:12px 16px;background:#FFFFFF">'
 + '<sc-if value="{{f.fig}}" hint-placeholder-val="{{ true }}"><svg width="150" height="105" viewBox="0 0 200 140" aria-hidden="true" style="flex:none"><path d="{{f.g.arc}}" fill="rgba(255,200,61,.35)" stroke="#E09A00" stroke-width="3"></path><path d="{{f.g.r1}}" stroke="#2B3FA8" stroke-width="5" stroke-linecap="round"></path><path d="{{f.g.r2}}" stroke="#2B3FA8" stroke-width="5" stroke-linecap="round"></path><circle cx="{{f.g.vx}}" cy="{{f.g.vy}}" r="5" fill="#1D1B3A"></circle><text x="{{f.g.lx}}" y="{{f.g.ly}}" text-anchor="middle" font-family="Baloo 2, sans-serif" font-weight="800" font-size="20" fill="#1D1B3A">{{f.g.lab}}</text></svg></sc-if>'
 + '<div><b class="h" style="font-size:22px;font-weight:700">{{f.t}}</b><div style="font-size:18px">{{f.x}}</div></div></div></sc-for>'
 + '</div>'
 + '<div style="flex:none;padding:14px 32px 24px;background:#FFFBF2;border-top:3px solid #1D1B3A;display:flex;gap:12px;align-items:center">'
 + '<div class="muted" style="flex:1;font-size:15px">{{w.note}}</div><button type="button" class="btn" onClick="{{w.go}}">{{w.goT}}</button></div>'
 + '</div></sc-if>')

# ---------------- ERGEBNIS ----------------
ERG = ('<sc-if value="{{is.erg}}" hint-placeholder-val="{{ false }}"><div class="scr">'
 + '<div class="band" style="height:200px;padding:22px 32px 0">' + band_stars(768, 200, 50, 21)
 + '<div style="position:relative;display:flex;align-items:center;gap:18px"><span class="kr" style="display:block">' + krabbi(100, 'Krabbi freut sich') + '</span>'
 + '<div><span class="cap" style="color:#C9CCFF">{{res.mod}}</span><h1 class="h" style="font-size:40px">{{res.head}}</h1><div style="font-size:20px;font-weight:700;color:#FFE9A8">{{res.right}} von {{res.n}} richtig</div></div></div>' + HORIZON + '</div>'
 + '<div class="scroll" style="padding:4px 32px 16px;display:flex;flex-direction:column;gap:12px">'
 + '<div class="card" style="padding:12px 18px"><span class="cap muted">Das hat die Runde gebracht</span><sc-for list="{{res.rows}}" as="w" hint-placeholder-count="3">'
 + '<div class="line" style="background:{{w.bg}};border-radius:14px;padding:8px">' + token('w.tok', 54, 18) + '<div style="flex:1"><b style="font-size:17px">Paket {{w.tok.nr}} · {{w.tok.name}}</b> <span class="muted" style="font-size:14px">{{w.cnt}}</span>'
 + '<sc-if value="{{w.hi}}" hint-placeholder-val="{{ false }}"><div style="display:flex;align-items:center;gap:6px;font-family:\'Baloo 2\';font-weight:800;font-size:20px;color:#0C5A3A">' + ich('w.hicon', 22, 2.8) + '{{w.tag}}</div></sc-if>'
 + '<div style="font-size:16px">{{w.text}}</div></div></div></sc-for></div>'
 + '<div class="card" style="padding:12px 18px;background:#FFFFFF"><div style="display:flex;justify-content:space-between;align-items:baseline"><span class="cap muted">So kommen deine Punkte zustande</span><button type="button" onClick="{{goRegeln}}" style="font-size:15px;font-weight:700;color:#2B3FA8;text-decoration:underline;min-height:44px">Alle Regeln</button></div>'
 + '<sc-for list="{{res.lines}}" as="l" hint-placeholder-count="4"><div class="line" style="align-items:center"><div style="flex:1"><b style="font-size:16px">{{l.t}}</b><div class="muted" style="font-size:14px">{{l.s}}</div></div><b class="h" style="font-size:22px;font-weight:700;min-width:56px;text-align:right">{{l.v}}</b></div></sc-for>'
 + '<div style="display:flex;justify-content:space-between;align-items:center;padding-top:10px"><b style="font-size:18px">Zusammen</b><span class="h" style="font-size:30px">+{{res.total}} Punkte</span></div>'
 + '<div style="display:flex;align-items:center;gap:10px;font-size:15px"><span style="display:block;flex:1;height:12px;border-radius:6px;background:#E4E2EC;overflow:hidden;border:2px solid #1D1B3A"><span style="display:block;height:12px;width:{{rk.pct}};background:#FFC83D"></span></span>{{rk.name}} · {{rk.toNext}}</div>'
 + '<sc-if value="{{res.up}}" hint-placeholder-val="{{ false }}"><div class="chip" style="margin-top:8px;background:#FFC83D;font-size:16px">Neuer Rang: {{rk.name}}!</div></sc-if></div>'
 + '<div style="display:flex;align-items:center;gap:12px"><span class="cap muted">Tagesziel</span><sc-for list="{{goalStars}}" as="g" hint-placeholder-count="3"><svg width="34" height="34" viewBox="0 0 24 24" aria-hidden="true"><path d="%s" fill="{{g.fill}}" stroke="#1D1B3A" stroke-width="1.6" stroke-linejoin="round" stroke-dasharray="{{g.dash}}"></path></svg></sc-for><b>{{goalText}}</b></div>' % ICON['star']
 + '</div>'
 + '<div style="flex:none;padding:14px 32px 24px;background:#FFFBF2;border-top:3px solid #1D1B3A;display:flex;flex-direction:column;gap:10px">'
 + '<sc-if value="{{res.goalDone}}" hint-placeholder-val="{{ false }}"><div style="display:flex;gap:12px"><button type="button" class="btn" onClick="{{goHeute}}" style="flex:1">Für heute fertig</button><button type="button" class="btn2" onClick="{{goFach}}">Noch eine Runde</button></div></sc-if>'
 + '<sc-if value="{{res.goOn}}" hint-placeholder-val="{{ true }}"><div style="display:flex;gap:12px"><button type="button" class="btn" onClick="{{res.nextGo}}" style="flex:1">Weiter: {{res.nextT}}</button><button type="button" class="btn2" onClick="{{goFach}}">Andere Wahl</button></div>'
 + '<button type="button" onClick="{{goHeute}}" style="align-self:center;min-height:44px;font-size:16px;font-weight:700;text-decoration:underline">Für heute aufhören</button></sc-if>'
 + '</div></div></sc-if>')

# ---------------- REGELN ----------------
def rule(n, icon, title, body):
    return ('<div class="card" style="display:flex;gap:14px;padding:14px 18px;background:#FFFFFF">'
            '<span style="display:flex;flex:none;width:52px;height:52px;border-radius:50%%;border:3px solid #1D1B3A;background:#FFE7A3;align-items:center;justify-content:center;font-family:\'Baloo 2\';font-weight:800;font-size:24px">%s</span>'
            '<div style="flex:1"><div class="h" style="font-size:23px;font-weight:700;display:flex;align-items:center;gap:8px">%s%s</div>%s</div></div>') % (n, ic(icon, 24), title, body)

def pts_chip(t, v, bg):
    return '<span style="display:flex;flex-direction:column;align-items:center;padding:6px 14px;border:2px solid #1D1B3A;border-radius:14px;background:%s"><b class="h" style="font-size:26px">%s</b><span style="font-size:14px;font-weight:700">%s</span></span>' % (bg, v, t)

def demo_tok(nr, col, h):
    seg = ''.join('<path d="%s" fill="none" stroke="%s" stroke-width="%s" stroke-dasharray="%s" stroke-linecap="round"></path>' % (ARC[i], '#F2B517' if i < h else '#A9A396', 6 if i < h else 2.5, 'none' if i < h else '3 4') for i in range(3))
    return ('<svg width="58" height="58" viewBox="0 0 64 64" aria-hidden="true" style="flex:none">' + seg
            + '<circle cx="32" cy="32" r="19" fill="%s" stroke="#1D1B3A" stroke-width="2.5"></circle><text x="32" y="39" text-anchor="middle" font-family="Baloo 2, sans-serif" font-weight="800" font-size="20" fill="#FFFFFF" stroke="#1D1B3A" stroke-width="0.8">%s</text></svg>' % (col, nr))

REGELN_BODY = (
 '<div style="display:flex;align-items:flex-end;gap:10px">' + krabbi(70) + '<div class="bubble" style="flex:1;font-size:19px">Punkte gibt es fürs Selberdenken. Raten bringt nichts.</div></div>'
 + rule('1', 'pencil', 'Je mehr du selbst machst, desto mehr Punkte',
        '<div style="font-size:17px">für jede richtige Antwort im ersten Versuch:</div><div style="display:flex;gap:10px;margin-top:8px;flex-wrap:wrap">'
        + pts_chip('Antippen', '4', '#FFFFFF') + pts_chip('Ordnen', '6', '#FFF1C7') + pts_chip('Selbst machen', '10', '#FFC83D')
        + '</div><div class="muted" style="font-size:15px;margin-top:6px">Selbst machen heißt: messen, zeichnen, schreiben, rechnen. Im zweiten Versuch gibt es die Hälfte.</div>')
 + rule('2', 'clock', 'Neues und Wieder-dran bringt volle Punkte',
        '<div style="font-size:17px">Was du sicher kannst, bringt wenig, bis es wieder dran ist. Lange nicht geübt: <b>+20 %</b>. Gemischt mit anderen Paketen: <b>+20 %</b>.</div>')
 + rule('3', 'pause', 'Raten bringt nichts',
        '<div style="font-size:17px">Wenn du schneller tippst, als man lesen kann, gibt es <b>0 Punkte</b>. Lies die Frage, dann antworte. Dann zählt es auch für deine Haken.</div>')
 + '<div class="card" style="padding:14px 18px;display:flex;flex-direction:column;gap:10px"><div class="h" style="font-size:23px;font-weight:700">Sicher wird ein Paket mit drei Haken</div>'
 + '<div style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px">'
 + ''.join('<div class="hk" style="flex-direction:column;align-items:flex-start;gap:4px">%s<b style="font-size:18px">%s</b><span style="font-size:15px">%s</span><span class="chip" style="font-size:13px;background:#FFF1C7">%s</span></div>' % (ic(i, 26), n, t, b) for i, n, t, b in [
     ('eye', 'Kennen', 'Du erkennst es, zum Beispiel mit Antippen.', 'Haken: +20'),
     ('pencil', 'Können', 'Du kannst es selbst: messen, zeichnen, schreiben.', 'Haken: +30'),
     ('loop', 'Behalten', 'Du kannst es auch an einem anderen Tag, gemischt.', 'sicher: +50')])
 + '</div><div style="display:flex;gap:18px;align-items:center;justify-content:center">'
 + ''.join('<span style="display:flex;flex-direction:column;align-items:center;font-size:15px;font-weight:700">%s%s</span>' % (demo_tok(n, c, h), w) for n, c, h, w in [(4, '#239C8E', 0, 'neu'), (3, '#E0567F', 1, 'noch üben'), (5, '#D9862A', 2, 'noch üben'), (1, '#5B8DEF', 3, 'sicher')])
 + '</div></div>'
 + '<div class="card" style="padding:14px 18px;background:#FFFFFF"><div class="h" style="font-size:21px;font-weight:700">Extrapunkte</div>'
 + '<div style="font-size:17px">Neuer Haken: +20, +30 oder +50 · Wieder-dran-Paket aufgefrischt: +20 · Tagesziel geschafft: +15</div>'
 + '<div style="font-size:17px;margin-top:6px"><b>Punkte werden dir nie weggenommen.</b> Es gibt keine Leben und nichts, was verfällt.</div></div>'
 + '<a class="btn2" href="G-Punkte.dc.html" style="align-self:flex-start">' + ic('lightbulb', 22) + 'Punkte-Rechner ausprobieren</a>')

REGELN = ('<sc-if value="{{is.regeln}}" hint-placeholder-val="{{ false }}"><div class="scr">'
 + '<div style="flex:none;display:flex;align-items:center;gap:14px;padding:20px 32px 12px;background:#FFFBF2;border-bottom:3px solid #1D1B3A">'
 + '<button type="button" class="btn2" onClick="{{goBack}}" style="min-height:48px;padding:0 14px">' + ic('back', 22, 3) + 'Zurück</button>'
 + '<h1 class="h" style="font-size:32px">So bekommst du Punkte</h1></div>'
 + '<div class="scroll" style="padding:16px 32px 28px;display:flex;flex-direction:column;gap:14px">' + REGELN_BODY + '</div>'
 + '</div></sc-if>')

# ---------------- ICH ----------------
RANKS = [('staub', 'Sternenstaub', 0), ('meteor', 'Meteor', 100), ('komet', 'Komet', 250), ('planet', 'Planet', 500), ('pulsar', 'Pulsar', 850), ('supernova', 'Supernova', 1300), ('galaxis', 'Galaxis-Legende', 2000)]
ICH = ('<sc-if value="{{is.ich}}" hint-placeholder-val="{{ false }}"><div class="scr">'
 + '<div class="band" style="height:150px;padding:22px 32px 0">' + band_stars(768, 150, 30, 15)
 + '<div style="position:relative;display:flex;align-items:center;gap:16px"><span style="display:flex;width:70px;height:70px;border-radius:50%;background:#FFFBF2;border:3px solid #1D1B3A;align-items:center;justify-content:center;color:#1D1B3A;font-family:\'Baloo 2\';font-weight:800;font-size:32px">R</span>'
 + '<div style="flex:1"><h1 class="h" style="font-size:36px">Robin</h1><div style="color:#E3E4FF">{{rk.name}} · {{points}} Punkte · {{rk.toNext}}</div></div></div>' + HORIZON + '</div>'
 + '<div class="scroll" style="padding:8px 32px 112px;display:flex;flex-direction:column;gap:14px">'
 + '<div class="card" style="padding:12px 16px"><span class="cap muted">Deine Ränge in Mathe</span><div style="display:grid;grid-template-columns:repeat(7,minmax(0,1fr));gap:4px;margin-top:6px">'
 + ''.join('<div style="display:flex;flex-direction:column;align-items:center;gap:2px;padding:6px 2px;border-radius:14px;background:{{rb.%s}};text-align:center">%s<b style="font-size:12px;line-height:1.1">%s</b><span class="muted" style="font-size:11px">ab %d</span></div>' % (k, rank(k, 40), n, x) for k, n, x in RANKS)
 + '</div></div>'
 + '<button type="button" class="btn2" onClick="{{goRegeln}}" style="align-self:flex-start">' + ic('star', 22) + 'So bekommst du Punkte</button>'
 + '<div class="card" style="padding:14px 18px;display:flex;flex-direction:column;gap:12px;background:#FFFFFF">'
 + '<div style="display:flex;justify-content:space-between;align-items:center"><div class="h" style="font-size:24px">Für Eltern</div><span class="chip" style="font-size:13px">sonst mit Code geschützt</span></div>'
 + '<div><b style="font-size:17px">Wie frei darf Robin wählen?</b><div class="seg" style="grid-template-columns:repeat(3,minmax(0,1fr));margin-top:8px"><sc-for list="{{lenkOpts}}" as="o" hint-placeholder-count="3"><button type="button" class="{{o.cls}}" onClick="{{o.pick}}" aria-pressed="{{o.on}}">{{o.t}}</button></sc-for></div>'
 + '<div style="font-size:16px;margin-top:8px;padding:10px 12px;border-radius:12px;background:#F3F1FA">{{lenkText}}</div></div>'
 + '<div><b style="font-size:17px">Tagesziel</b><div class="seg" style="grid-template-columns:repeat(3,minmax(0,1fr));margin-top:8px"><sc-for list="{{zielOpts}}" as="o" hint-placeholder-count="3"><button type="button" class="{{o.cls}}" onClick="{{o.pick}}" aria-pressed="{{o.on}}">{{o.t}}</button></sc-for></div></div>'
 + '<div><b style="font-size:17px">Lernstand Mathe</b><div style="font-size:16px;margin-top:4px">{{elternStand}}</div><div class="muted" style="font-size:14px;margin-top:2px">Eltern sehen die Haken, nicht nur Punkte. Ein Haken heißt: Robin hat es wirklich selbst gekonnt.</div></div>'
 + '</div></div>' + tabs() + '</div></sc-if>')

# ---------------- GEMEINSAM ----------------
GEM = ('<sc-if value="{{is.gem}}" hint-placeholder-val="{{ false }}"><div class="scr">'
 + '<div class="band" style="height:150px;padding:22px 32px 0">' + band_stars(768, 150, 30, 19)
 + '<div style="position:relative"><span class="cap" style="color:#C9CCFF">Lerngruppe</span><h1 class="h" style="font-size:36px">Klasse 6b</h1></div>' + HORIZON + '</div>'
 + '<div class="scroll" style="padding:8px 32px 112px;display:flex;flex-direction:column;gap:14px">'
 + '<div class="card" style="padding:16px 18px;display:flex;flex-direction:column;gap:8px"><span class="cap muted">Gemeinsames Wochenziel</span><div class="h" style="font-size:26px">Zusammen 30 Haken</div>'
 + '<div style="display:flex;align-items:center;gap:10px"><span style="display:block;flex:1;height:18px;border-radius:9px;background:#E4E2EC;border:2px solid #1D1B3A;overflow:hidden"><span style="display:block;height:14px;width:{{gemPct}};background:#F2B517"></span></span><b>{{gemN}} von 30</b></div>'
 + '<div class="muted" style="font-size:15px">Jeder neue Haken zählt für alle. So hilft es auch, wenn jemand ein schweres Paket schafft.</div></div>'
 + '<div class="card" style="padding:12px 18px;background:#FFFFFF"><span class="cap muted">Haken diese Woche</span>'
 + ''.join('<div class="line" style="align-items:center"><span style="display:flex;width:40px;height:40px;border-radius:50%%;border:2px solid #1D1B3A;background:%s;align-items:center;justify-content:center;font-weight:700">%s</span><b style="flex:1;font-size:17px">%s</b><b class="h" style="font-size:20px">%s</b></div>' % r for r in [
     ('#FFE7A3', 'R', 'Robin (du)', '{{gemMe}}'), ('#D9E4FF', 'M', 'Mila', '6'), ('#DDF5E7', 'J', 'Jonas', '3'), ('#FFE1EA', 'E', 'Ela', '5')])
 + '</div>'
 + '<div class="card" style="padding:14px 18px;display:flex;align-items:center;gap:14px;box-shadow:0 3px 0 #1D1B3A">' + ic('bolt', 30) + '<div style="flex:1"><b style="font-size:17px">Duell und Arena</b><div class="muted" style="font-size:15px">wie heute: Tauziehen live, Geister-Duell. Im Entwurf nicht ausgearbeitet.</div></div></div>'
 + '</div>' + tabs() + '</div></sc-if>')

BODY = ('<div style="width:768px;height:1024px;position:relative;overflow:hidden;background:#EEF0FA;color:#1D1B3A;font-family:\'Atkinson Hyperlegible\',Verdana,sans-serif;font-size:17px;line-height:1.4">'
        + GROUND + HEUTE + FACH + FREI + UEB + WISSEN + ERG + REGELN + ICH + GEM + '</div>')

JS = open(sys.argv[1] + '/app.js').read().replace('__ICON__', json.dumps(ICON, ensure_ascii=False))

html = (head('G · Lernzentrale · Klick-Dummy').replace('%s', CSS, 1) + BODY + '\n</x-dc>\n'
        + '<script type="text/x-dc" data-dc-script data-props=\'{"$preview":{"width":768,"height":1024}}\'>\n' + JS + '\n</script>\n</body>\n</html>\n')
open(out + '/G-App.dc.html', 'w').write(html)
print('G-App', len(html))
