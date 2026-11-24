import sys, json
sys.path.insert(0, sys.argv[1]); outdir = sys.argv[2]
import common
from common import krabbi, icon, ICON, week
FONTF = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fredoka:wght@500;600;700&family=Figtree:wght@400;600;700&display=swap">'

CSS = r"""
body{margin:0}
*{box-sizing:border-box}
button{font:inherit;color:inherit;cursor:pointer;border:0;background:none;padding:0;text-align:left}
button:focus-visible,input:focus-visible{outline:3px solid #1F6FEB;outline-offset:2px}
.h{font-family:'Fredoka','Trebuchet MS',sans-serif;font-weight:600;margin:0;line-height:1.15}
.scr{position:absolute;left:0;top:0;width:768px;height:1024px;display:flex;flex-direction:column}
.cap{font-size:13px;font-weight:700;letter-spacing:.05em;text-transform:uppercase}
.btn{display:flex;align-items:center;justify-content:center;gap:8px;min-height:56px;padding:0 24px;border-radius:28px;font-family:'Fredoka','Trebuchet MS',sans-serif;font-weight:600;font-size:20px}
.btn:active{transform:translateY(1px)}
.nav{display:flex;align-items:center;gap:8px;min-height:44px;padding:0 14px;border-radius:22px;background:rgba(255,255,255,.18);font-weight:700;font-size:15px}
.nav:hover{background:rgba(255,255,255,.3)}
.qp{min-height:44px;padding:0 14px;border-radius:22px;background:#FFFFFF;font-weight:700;font-size:15px;white-space:nowrap}
.qp:hover{filter:brightness(.96)}
.gh{display:flex;align-items:center;gap:10px;width:100%;min-height:44px;padding:0 6px;border-radius:12px;font-size:15px}
.gh:hover{background:rgba(0,0,0,.05)}
.tok{flex:none;width:112px;display:flex;flex-direction:column;align-items:center;gap:3px;padding:8px 2px 6px;border-radius:16px;text-align:center}
.tok:hover{background:rgba(0,0,0,.05)}
.tc{position:relative;width:48px;height:48px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-family:'Fredoka',sans-serif;font-weight:600;font-size:17px}
.tn{font-size:13px;font-weight:700;line-height:1.2;max-width:108px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.ts{font-size:12px;line-height:1.2}
.tile{position:relative;display:flex;align-items:center;gap:8px;width:calc(100% - 12px);min-height:60px;margin:6px 6px 0;padding:6px 8px;border-radius:14px;background:#FFFFFF;border:2px solid #FFFFFF;font-size:15px;line-height:1.2}
.tile b{display:block}
.tile small{display:block;font-size:13px;margin-top:1px}
.tile.lock{background:transparent;border:2px dashed currentColor;cursor:default}
.peg{width:24px;height:24px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;border:2px solid #FFFFFF}
.ans{display:flex;align-items:center;justify-content:space-between;gap:10px;min-height:76px;padding:0 22px;border-radius:24px;background:#FFFFFF;border:3px solid #FFFFFF;font-size:22px;font-weight:700}
.ans:hover{border-color:#B9BFCC}
.ans.sel{border-color:currentColor}
.ans.ok{border-color:#0E7A54;background:#DFF5EA}
.ans.no{border:3px dashed #B4500A;background:#FFE9D6}
.ans.dim{opacity:.75;cursor:default}
.ans .mk{font-size:14px}
.card{background:#FFFFFF;border-radius:24px;padding:16px 20px}
.sheet{position:absolute;left:0;right:0;bottom:0;background:#FFFFFF;border-radius:32px 32px 0 0;padding:22px 28px 28px;max-height:880px;overflow-y:auto}
.scrim{position:absolute;left:0;top:0;width:768px;height:1024px;background:rgba(20,22,40,.5);cursor:default}
@keyframes wipp{0%,100%{transform:rotate(0)}50%{transform:rotate(-5deg)}}
.kr{animation:wipp 5s ease-in-out infinite;transform-origin:50% 90%}
@media (prefers-reduced-motion:reduce){.kr{animation:none}}
"""
def pi(hole, size=22):
    return '<svg width="%d" height="%d" viewBox="0 0 24 24" aria-hidden="true" style="flex:none"><path d="{{%s}}" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path></svg>' % (size, size, hole)
def kboth(w, cls=''):
    return ('<span class="%s" style="display:block;flex:none"><sc-if value="{{isE}}" hint-placeholder-val="{{ true }}">%s</sc-if><sc-if value="{{isM}}" hint-placeholder-val="{{ false }}">%s</sc-if></span>'
            % (cls, krabbi(w, 'suedwester', label='Krabbi mit Südwester'), krabbi(w, 'helm', label='Krabbi mit Raumhelm')))
EDGE = '<svg width="768" height="24" viewBox="0 0 768 24" aria-hidden="true" style="position:absolute;left:0;bottom:-1px;display:block"><path d="{{T.edge}}" fill="{{T.ground}}"></path></svg>'
def band(inner, pad='16px 24px 34px'):
    return '<div style="position:relative;flex:none;background:{{T.band}};color:#FFFFFF;padding:%s">%s%s</div>' % (pad, inner, EDGE)
TOK = '''<button type="button" class="tok" onClick="{{p.toggle}}" aria-pressed="{{p.on}}" aria-label="{{p.aria}}" style="transform:{{p.tf}}"><span class="tc" style="background:{{p.fill}};border:{{p.bd}};box-shadow:{{p.ring}}">{{p.label}}</span><span class="tn">{{p.name}}</span><span class="ts" style="color:{{T.mute}}">{{p.word}}</span></button>'''

MAIN = '''<sc-if value="{{isMain}}" hint-placeholder-val="{{ true }}">
<div class="scr">
''' + band('''<div style="display:flex;align-items:center;justify-content:space-between;gap:12px">
<div><span class="cap" style="color:{{T.bandMute}}">{{T.kicker}}</span><h1 class="h" style="font-size:30px">{{T.welt}}</h1></div>
<div style="display:flex;gap:8px"><button type="button" class="nav" onClick="{{goGem}}">''' + icon('gem', 20) + '''Gemeinsam</button><button type="button" class="nav" onClick="{{goIch}}">''' + icon('ich', 20) + '''{{T.rang}} · {{points}} P</button></div>
</div>
<div style="display:flex;align-items:center;gap:12px;margin-top:10px">''' + kboth(76, 'kr') + '''
<div style="flex:1"><span class="cap" style="color:{{T.bandMute}}">{{heuteCap}}</span><p style="margin:2px 0 0;font-size:17px;line-height:1.35">{{heuteText}}</p></div>
<button type="button" class="btn" onClick="{{openSo}}" style="flex:none;background:#FFFFFF;color:{{T.ink}};font-size:17px;min-height:52px;padding:0 18px">''' + icon('fernrohr', 22) + '''Standort bestimmen</button>
</div>''') + '''
<div style="flex:1;min-height:0;overflow-y:auto;padding:4px 20px 14px">
<div style="display:flex;align-items:center;justify-content:space-between;gap:12px">
<h2 class="h" style="font-size:22px">1 · Was möchtest du lernen?</h2>
<div style="display:flex;align-items:center;gap:8px"><label for="suche" style="font-size:14px;font-weight:700">Suche</label><input id="suche" type="search" value="{{q}}" onChange="{{onSearch}}" placeholder="Paket suchen" style="width:190px;height:44px;border-radius:22px;border:2px solid {{T.mute}};padding:0 14px;font:inherit;font-size:15px;background:#FFFFFF;color:{{T.ink}}"></div>
</div>
<div style="display:flex;gap:8px;margin-top:8px;flex-wrap:wrap">
<sc-for list="{{quick}}" as="k" hint-placeholder-count="5"><button type="button" class="qp" onClick="{{k.go}}" style="background:{{k.bg}}">{{k.t}}</button></sc-for>
</div>
<sc-if value="{{hasQ}}" hint-placeholder-val="{{ false }}">
<div style="margin-top:8px"><span style="font-size:15px;font-weight:700">{{foundText}}</span><div style="display:flex;flex-wrap:wrap">
<sc-for list="{{found}}" as="p" hint-placeholder-count="3">''' + TOK + '''</sc-for></div></div>
</sc-if>
<sc-if value="{{noQ}}" hint-placeholder-val="{{ true }}">
<div style="margin-top:6px;display:flex;flex-direction:column;gap:2px">
<sc-for list="{{groups}}" as="g" hint-placeholder-count="5">
<div>
<button type="button" class="gh" onClick="{{g.toggle}}" aria-expanded="{{g.open}}">
<span style="display:flex;transform:{{g.rot}}">''' + icon('pfeil', 18) + '''</span>
<b style="font-size:16px">{{g.name}}</b>
<span style="display:flex;gap:3px" aria-hidden="true"><sc-for list="{{g.strip}}" as="x" hint-placeholder-count="6"><span style="width:12px;height:12px;border-radius:50%;background:{{x.bg}};border:{{x.bd}}"></span></sc-for></span>
<span style="flex:1;color:{{T.mute}}">{{g.info}}</span>
<sc-if value="{{g.hasSel}}" hint-placeholder-val="{{ false }}"><span style="padding:2px 10px;border-radius:999px;font-size:13px;font-weight:700;background:{{T.ink}};color:#FFFFFF">{{g.selText}}</span></sc-if>
</button>
<sc-if value="{{g.open}}" hint-placeholder-val="{{ true }}">
<div style="display:flex;overflow-x:auto;padding-bottom:2px"><sc-for list="{{g.pks}}" as="p" hint-placeholder-count="6">''' + TOK + '''</sc-for></div>
</sc-if>
</div>
</sc-for>
</div>
</sc-if>
<div style="display:flex;align-items:center;justify-content:space-between;gap:12px;margin-top:12px">
<h2 class="h" style="font-size:22px">2 · Wie möchtest du üben?</h2>
<button type="button" class="qp" onClick="{{openTreppe}}">So geht die Treppe</button>
</div>
<p style="margin:2px 0 0;font-size:15px;color:{{T.mute}}">Deine Pakete stehen auf der Stufe, die sie erreicht haben. Zwei gute Runden, und ein Paket steigt eine Stufe höher.</p>
<div style="display:grid;grid-template-columns:repeat(4, minmax(0, 1fr));gap:8px;margin-top:8px;align-items:end">
<sc-for list="{{steps}}" as="st" hint-placeholder-count="4">
<div style="background:{{st.bg}};border-radius:18px;padding-bottom:8px;min-height:{{st.minH}}px">
<div style="background:{{T.band}};color:#FFFFFF;border-radius:18px 18px 6px 6px;padding:6px 10px 8px;min-height:62px">
<div style="display:flex;align-items:baseline;justify-content:space-between"><span class="h" style="font-size:17px">{{st.name}}</span><span style="font-size:13px;font-weight:700;color:{{T.bandMute}}">Stufe {{st.k}}</span></div>
<div style="display:flex;gap:3px;margin-top:4px;min-height:24px;align-items:center"><sc-for list="{{st.pegs}}" as="g" hint-placeholder-count="1"><span class="peg" style="background:{{g.col}};color:{{T.ink}}">{{g.label}}</span></sc-for><span style="font-size:12px;color:{{T.bandMute}}">{{st.pegText}}</span></div>
</div>
<sc-for list="{{st.mods}}" as="m" hint-placeholder-count="2">
<button type="button" class="tile {{m.cls}}" onClick="{{m.pick}}" aria-pressed="{{m.on}}" style="border-color:{{m.bd}};background:{{m.bg}};color:{{m.ink}}">''' + pi('m.icon') + '''<span><b>{{m.t}}</b><small>{{m.sub}}</small></span><sc-if value="{{m.tip}}" hint-placeholder-val="{{ false }}"><span style="position:absolute;right:6px;top:-9px;padding:1px 8px;border-radius:999px;font-size:12px;font-weight:700;background:{{T.accent}};color:{{T.ink}}">Krabbis Tipp</span></sc-if></button>
</sc-for>
</div>
</sc-for>
</div>
<sc-for list="{{tests}}" as="m" hint-placeholder-count="1">
<button type="button" class="tile {{m.cls}}" onClick="{{m.pick}}" aria-pressed="{{m.on}}" style="width:100%;margin:8px 0 0;border-color:{{m.bd}};background:{{m.bg}};color:{{m.ink}}">''' + pi('m.icon') + '''<span><b>{{m.t}}</b><small>{{m.sub}}</small></span></button>
</sc-for>
</div>
<div style="flex:none;background:{{T.ink}};color:#FFFFFF;border-radius:28px 28px 0 0;padding:14px 20px 16px;display:flex;align-items:center;gap:16px">
<div style="flex:1;min-width:0">
<div class="h" style="font-size:20px">{{barTitle}}</div>
<div style="display:flex;gap:3px;height:24px;margin-top:6px;border-radius:12px;overflow:hidden;background:rgba(255,255,255,.14)">
<sc-for list="{{mix}}" as="x" hint-placeholder-count="3"><span style="flex-grow:{{x.w}};flex-basis:0;background:{{x.col}};color:{{T.ink}};font-size:13px;font-weight:700;display:flex;align-items:center;justify-content:center">{{x.label}}</span></sc-for>
</div>
<p role="status" style="margin:6px 0 0;font-size:14px;line-height:1.3;color:{{barNoteCol}}">{{barNote}}</p>
</div>
<button type="button" class="btn" onClick="{{start}}" aria-disabled="{{notReady}}" style="flex:none;background:{{startBg}};color:{{T.ink}}">Runde starten ''' + icon('pfeil', 22) + '''</button>
</div>
</div>
</sc-if>'''

SO = '''<sc-if value="{{isSo}}" hint-placeholder-val="{{ false }}">
<div class="scr">
''' + band('''<span class="cap" style="color:{{T.bandMute}}">{{T.kicker}}</span><h1 class="h" style="font-size:34px">Standort bestimmen</h1>''', '22px 28px 40px') + '''
<div style="flex:1;padding:8px 28px 28px;display:flex;flex-direction:column;gap:16px">
<div style="display:flex;align-items:center;gap:16px">''' + kboth(120, 'kr') + '''<p style="margin:0;font-size:20px;line-height:1.4">Ich stelle dir ein paar Fragen quer durch alle Pakete, die du schon angefangen hast. Danach weiß ich, wo es sich für dich am meisten lohnt.</p></div>
<div class="card" style="display:flex;flex-direction:column;gap:12px;font-size:18px">
<div style="display:flex;gap:12px;align-items:center"><span style="flex:none;display:flex;color:{{T.band}}">''' + icon('zeit', 28) + '''</span><span><b>Kurz:</b> {{soLen}}</span></div>
<div style="display:flex;gap:12px;align-items:center"><span style="flex:none;display:flex;color:{{T.band}}">''' + icon('muenze', 28) + '''</span><span><b>Ohne Druck:</b> keine Note, keine Punkte, nichts geht verloren.</span></div>
<div style="display:flex;gap:12px;align-items:center"><span style="flex:none;display:flex;color:{{T.band}}">''' + icon('fernrohr', 28) + '''</span><span><b>Danach:</b> Ich schlage dir einen Fokus vor: die Pakete, die noch Übung brauchen. Du entscheidest, ob du ihn nimmst.</span></div>
</div>
<div style="flex:1"></div>
<div style="display:flex;gap:12px"><button type="button" class="btn" onClick="{{goMain}}" style="flex:1;background:#FFFFFF;color:{{T.ink}}">Zurück</button><button type="button" class="btn" onClick="{{startSo}}" style="flex:1.6;background:{{T.accent}};color:{{T.ink}}">Los geht es ''' + icon('pfeil', 22) + '''</button></div>
</div>
</div>
</sc-if>
<sc-if value="{{isSoRes}}" hint-placeholder-val="{{ false }}">
<div class="scr">
''' + band('''<span class="cap" style="color:{{T.bandMute}}">Standort · {{soScore}}</span><h1 class="h" style="font-size:34px">Hier stehst du</h1>''', '22px 28px 40px') + '''
<div style="flex:1;min-height:0;overflow-y:auto;padding:4px 28px 24px;display:flex;flex-direction:column;gap:14px">
<div class="card"><span class="cap" style="color:{{T.mute}}">Deine Pakete auf einen Blick</span>
<div style="display:flex;flex-direction:column;gap:8px;margin-top:8px">
<sc-for list="{{soGroups}}" as="g" hint-placeholder-count="4"><div style="display:flex;align-items:center;gap:12px;font-size:16px"><b style="width:220px;flex:none">{{g.name}}</b><span style="display:flex;gap:4px" aria-hidden="true"><sc-for list="{{g.strip}}" as="x" hint-placeholder-count="6"><span style="width:16px;height:16px;border-radius:50%;background:{{x.bg}};border:{{x.bd}}"></span></sc-for></span><span style="color:{{T.mute}}">{{g.info}}</span></div></sc-for>
</div>
<p style="margin:10px 0 0;font-size:14px;color:{{T.mute}}">Voller Kreis: sicher · halber Kreis: noch üben · leerer Kreis: neu</p></div>
<div class="card" style="background:{{T.tint}}"><div style="display:flex;align-items:center;gap:14px">''' + kboth(84) + '''<div><span class="cap" style="color:{{T.mute}}">Krabbis Fokus für dich</span><p style="margin:2px 0 0;font-size:18px;line-height:1.35">{{soText}}</p></div></div>
<div style="display:flex;flex-direction:column;gap:8px;margin-top:12px">
<sc-for list="{{fokus}}" as="p" hint-placeholder-count="3"><div style="display:flex;align-items:center;gap:12px;font-size:17px;background:#FFFFFF;border-radius:16px;padding:8px 12px"><span class="tc" style="width:40px;height:40px;font-size:15px;background:{{p.fill}};border:{{p.bd}}">{{p.label}}</span><span style="flex:1"><b>{{p.name}}</b> · {{p.word}}</span><span style="color:{{T.mute}};font-size:15px">{{p.why}}</span></div></sc-for>
</div></div>
<div style="flex:1"></div>
<div style="display:flex;gap:12px"><button type="button" class="btn" onClick="{{goMain}}" style="flex:1;background:#FFFFFF;color:{{T.ink}}">Selbst wählen</button><button type="button" class="btn" onClick="{{takeFokus}}" style="flex:1.6;background:{{T.accent}};color:{{T.ink}}">Fokus übernehmen ''' + icon('pfeil', 22) + '''</button></div>
</div>
</div>
</sc-if>'''

EX = '''<sc-if value="{{isEx}}" hint-placeholder-val="{{ false }}">
<div class="scr" style="padding:20px 32px 28px;gap:16px">
<div style="display:flex;align-items:center;gap:16px;flex:none">
<button type="button" onClick="{{goMain}}" aria-label="Runde beenden" style="width:48px;height:48px;border-radius:24px;background:#FFFFFF;display:flex;align-items:center;justify-content:center;flex:none">''' + icon('x', 22) + '''</button>
<div role="img" aria-label="{{exProgress}}" style="flex:1;display:flex;gap:6px"><sc-for list="{{segs}}" as="g" hint-placeholder-count="4"><span style="flex:1;height:14px;border-radius:7px;background:{{g.bg}}"></span></sc-for></div>
<span style="flex:none;font-weight:700;font-size:17px;padding:8px 14px;border-radius:999px;background:{{T.ink}};color:#FFFFFF">{{exBadge}}</span>
</div>
<div style="display:flex;align-items:center;justify-content:space-between;gap:12px;flex:none;font-size:16px">
<div style="display:flex;align-items:center;gap:10px"><span class="peg" style="width:32px;height:32px;font-size:13px;background:{{src.col}};color:{{T.ink}};border-color:{{T.ink}}">{{src.label}}</span><span>aus <b>{{src.name}}</b> · {{src.word}}</span></div>
<span style="color:{{T.mute}}">{{exTitle}} · {{exProgress}}</span>
</div>
<h1 class="h" style="font-size:32px;flex:none">{{T.prompt}}</h1>
<div style="flex:none;height:280px;background:#FFFFFF;border-radius:32px;display:flex;align-items:center;justify-content:center">
<sc-if value="{{isE}}" hint-placeholder-val="{{ true }}"><div style="text-align:center"><span class="cap" style="color:{{T.mute}}">Englisch</span><div class="h" style="font-size:72px;color:{{T.band}}">{{qv.w}}</div></div></sc-if>
<sc-if value="{{isM}}" hint-placeholder-val="{{ false }}"><svg width="420" height="260" viewBox="0 0 400 260" role="img" aria-label="Ein Winkel mit zwei Schenkeln und einem Bogen"><path d="{{qv.arc}}" fill="none" stroke="#FF7AB6" stroke-width="7" stroke-linecap="round"></path><path d="{{qv.rays}}" fill="none" stroke="#1B1740" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"></path><circle cx="200" cy="140" r="8" fill="#1B1740"></circle></svg></sc-if>
</div>
<div style="display:grid;grid-template-columns:repeat(2, minmax(0, 1fr));gap:12px;flex:none">
<sc-for list="{{opts}}" as="o" hint-placeholder-count="4"><button type="button" class="ans {{o.cls}}" onClick="{{o.pick}}" aria-pressed="{{o.on}}"><span>{{o.t}}</span><sc-if value="{{o.hasMark}}" hint-placeholder-val="{{ false }}"><span class="mk" style="color:{{o.markCol}}">{{o.mark}}</span></sc-if></button></sc-for>
</div>
<div style="flex:1"></div>
<sc-if value="{{notChecked}}" hint-placeholder-val="{{ true }}">
<div style="display:flex;align-items:center;gap:16px;flex:none"><p style="flex:1;margin:0;font-size:16px;color:{{T.mute}}">Erst antippen, dann prüfen. Vorher kannst du deine Wahl noch ändern.</p><button type="button" class="btn" onClick="{{check}}" aria-disabled="{{noPick}}" style="min-width:220px;background:{{checkBg}};color:{{T.ink}}">Prüfen</button></div>
</sc-if>
<sc-if value="{{checked}}" hint-placeholder-val="{{ false }}">
<div role="status" style="display:flex;align-items:center;gap:14px;padding:14px 18px 14px 12px;border-radius:28px;background:{{fbBg}};flex:none">''' + kboth(72) + '''<div style="flex:1"><div class="h" style="font-size:22px">{{fbHead}}</div><p style="margin:2px 0 0;font-size:17px">{{fbText}}</p></div><button type="button" class="btn" onClick="{{next}}" style="flex:none;background:{{T.ink}};color:#FFFFFF">{{nextLabel}}</button></div>
</sc-if>
</div>
</sc-if>'''

RES = '''<sc-if value="{{isRes}}" hint-placeholder-val="{{ false }}">
<div class="scr">
''' + band('''<div style="display:flex;align-items:center;gap:16px">''' + kboth(110, 'kr') + '''<div><span class="cap" style="color:{{T.bandMute}}">{{exTitle}}</span><h1 class="h" style="font-size:38px">{{resHead}}</h1><p style="margin:4px 0 0;font-size:18px">{{resText}}</p></div></div>''', '20px 28px 40px') + '''
<div style="flex:1;min-height:0;overflow-y:auto;padding:4px 28px 24px;display:flex;flex-direction:column;gap:14px">
<sc-if value="{{hasUnlock}}" hint-placeholder-val="{{ false }}">
<div class="card" style="background:{{T.accent}};display:flex;align-items:center;gap:14px"><span style="flex:none;display:flex">''' + icon('stern', 36) + '''</span><div><div class="h" style="font-size:22px">Neue Stufe frei</div><p style="margin:2px 0 0;font-size:17px">{{unlockText}}</p></div></div>
</sc-if>
<div class="card"><span class="cap" style="color:{{T.mute}}">So lief es je Paket</span>
<div style="display:flex;flex-direction:column;gap:10px;margin-top:10px">
<sc-for list="{{resPk}}" as="p" hint-placeholder-count="3"><div style="display:flex;align-items:center;gap:12px;font-size:16px"><span class="peg" style="width:32px;height:32px;font-size:13px;background:{{p.col}};color:{{T.ink}};border-color:{{T.ink}}">{{p.label}}</span><b style="width:150px;flex:none">{{p.name}}</b><span style="width:110px;flex:none">{{p.score}}</span><span style="color:{{T.mute}}">{{p.txt}}</span></div></sc-for>
</div></div>
<div style="display:grid;grid-template-columns:repeat(2, minmax(0, 1fr));gap:14px">
<div class="card"><span class="cap" style="color:{{T.mute}}">Punkte</span><div class="h" style="font-size:36px">+{{resPts}}</div><p style="margin:2px 0 0;font-size:15px;color:{{T.mute}}">{{resPtsNote}}</p></div>
<div class="card"><span class="cap" style="color:{{T.mute}}">Heute</span><div class="h" style="font-size:36px">{{resRound}}</div><p style="margin:2px 0 0;font-size:15px;color:{{T.mute}}">Heute leuchtet dein Stern im Sternbild der Woche. Freie Tage löschen nichts.</p></div>
</div>
<div style="flex:1"></div>
<div style="display:flex;gap:12px"><button type="button" class="btn" onClick="{{goMain}}" style="flex:1;background:#FFFFFF;color:{{T.ink}}">Zur Auswahl</button><button type="button" class="btn" onClick="{{again}}" style="flex:1.6;background:{{T.accent}};color:{{T.ink}}">{{againLabel}} ''' + icon('pfeil', 22) + '''</button></div>
</div>
</div>
</sc-if>'''

def crow(t, d, bg):
    return '<div style="display:flex;align-items:center;gap:12px"><span style="flex:none;min-width:124px;text-align:center;padding:5px 10px;border-radius:999px;font-size:14px;font-weight:700;background:%s">%s</span><span style="font-size:15px">%s</span></div>' % (bg, t, d)
def gcard(ic, title, text, btn):
    return ('<div class="card" style="display:flex;align-items:center;gap:16px"><span style="flex:none;width:56px;height:56px;border-radius:28px;background:{{T.band}};color:#FFFFFF;display:flex;align-items:center;justify-content:center">' + icon(ic, 30) + '</span><div style="flex:1"><div class="h" style="font-size:20px">' + title + '</div><p style="margin:2px 0 0;font-size:16px;color:{{T.mute}}">' + text + '</p></div><button type="button" class="btn" style="flex:none;font-size:17px;min-height:48px;padding:0 18px;background:{{T.tint}}">' + btn + '</button></div>')
BACK = '<button type="button" class="nav" onClick="{{goMain}}" style="margin-bottom:8px"><span style="display:flex;transform:rotate(180deg)">' + icon('pfeil', 20) + '</span>Zurück zum Lernen</button>'
SIDE = '''<sc-if value="{{isIch}}" hint-placeholder-val="{{ false }}">
<div class="scr">
''' + band(BACK + '''<div style="display:flex;align-items:flex-end;justify-content:space-between"><div><span class="cap" style="color:{{T.bandMute}}">Ich · {{T.kicker}}</span><h1 class="h" style="font-size:34px">Mika, Rang {{T.rang}}</h1></div><div style="text-align:right"><div class="h" style="font-size:34px">{{points}}</div><div style="font-size:15px;color:{{T.bandMute}}">Punkte · {{T.rangNext}}</div></div></div>''', '16px 28px 40px') + '''
<div style="flex:1;min-height:0;overflow-y:auto;padding:4px 28px 24px;display:flex;flex-direction:column;gap:14px">
<div class="card" style="display:flex;align-items:center;gap:18px"><sc-if value="{{todayLit}}" hint-placeholder-val="{{ false }}">''' + week(True) + '''</sc-if><sc-if value="{{todayDark}}" hint-placeholder-val="{{ true }}">''' + week(False) + '''</sc-if><div><div class="h" style="font-size:19px">Sternbild der Woche</div><p style="margin:2px 0 0;font-size:15px;color:{{T.mute}}">Jeder Lerntag lässt einen Stern leuchten. Freie Tage löschen nichts.</p></div></div>
<div class="card"><span class="cap" style="color:{{T.mute}}">Wofür es Punkte gibt</span><div style="display:flex;flex-direction:column;gap:8px;margin-top:10px">
''' + crow('volle Punkte', 'Neues und alles, was du noch übst.', '{{T.accent}}') + crow('+20 % Bonus', 'Sicheres, das wieder dran ist.', '#FFC53D') + crow('wenige Punkte', 'Sicheres, das noch nicht wieder dran ist.', '#E6E8EE') + crow('keine Punkte', 'Falsche Antworten und sehr schnelles Tippen ohne Lesen.', '#FFFFFF;border:2px dashed {{T.mute}}') + '''
</div><p style="margin:10px 0 0;font-size:15px;color:{{T.mute}}">Punkte bringen dich im Rang nach oben. Neue Stufen auf der Treppe gibt es nur für gute Runden, nicht für Punkte.</p></div>
<div style="display:flex;gap:12px"><button type="button" class="btn" style="flex:1;font-size:18px;background:#FFFFFF">Person wechseln</button><button type="button" class="btn" onClick="{{openCode}}" style="flex:1;font-size:18px;background:#FFFFFF">''' + icon('schloss', 20) + '''Eltern-Bereich</button></div>
</div>
</div>
</sc-if>
<sc-if value="{{isGem}}" hint-placeholder-val="{{ false }}">
<div class="scr">
''' + band(BACK + '''<h1 class="h" style="font-size:34px">Gemeinsam</h1><p style="margin:2px 0 0;font-size:17px">Die Fragen kommen nur aus Paketen, die alle Mitspielenden schon auf Stufe 2 oder höher haben.</p>''', '16px 28px 40px') + '''
<div style="flex:1;padding:4px 28px 24px;display:flex;flex-direction:column;gap:14px">
''' + gcard('seil', 'Tauziehen', 'Live gegeneinander. Jede richtige Antwort zieht das Seil zu dir.', 'Herausfordern') + gcard('geist', 'Geister-Duell', 'Gegen die Aufzeichnung von jemandem, der gerade keine Zeit hat.', 'Geist wählen') + gcard('rad', 'Fach-Glücksrad', 'Fragen aus allen Fächern gemischt.', 'Drehen') + '''
<div style="display:grid;grid-template-columns:repeat(2, minmax(0, 1fr));gap:14px"><div class="card"><div class="h" style="font-size:19px">Familie</div><p style="margin:2px 0 0;font-size:15px;color:{{T.mute}}">3 dabei · du bist diese Woche auf Platz 2</p></div><div class="card"><div class="h" style="font-size:19px">Klasse 6b</div><p style="margin:2px 0 0;font-size:15px;color:{{T.mute}}">11 dabei · du bist diese Woche auf Platz 5</p></div></div>
</div>
</div>
</sc-if>'''

SHEET = '''<sc-if value="{{hasSheet}}" hint-placeholder-val="{{ false }}">
<div style="position:absolute;left:0;top:0;width:768px;height:1024px;z-index:5">
<button type="button" class="scrim" onClick="{{closeSheet}}" aria-label="Schließen"></button>
<sc-if value="{{isTreppe}}" hint-placeholder-val="{{ false }}">
<div class="sheet" role="dialog" aria-label="So geht die Treppe">
<div style="display:flex;align-items:center;gap:14px">''' + kboth(84) + '''<div style="flex:1"><h2 class="h" style="font-size:28px">So geht die Treppe</h2><p style="margin:2px 0 0;font-size:18px">Jedes Paket steigt vier Stufen hoch. Auf jeder Stufe warten andere Lernformen.</p></div></div>
<div style="display:grid;grid-template-columns:repeat(4, minmax(0, 1fr));gap:8px;margin-top:16px;align-items:end">
<sc-for list="{{legend}}" as="l" hint-placeholder-count="4"><div style="background:{{l.bg}};border-radius:16px;padding:10px 12px;min-height:{{l.h}}px"><div class="h" style="font-size:18px">{{l.k}} · {{l.name}}</div><p style="margin:4px 0 0;font-size:15px;line-height:1.3">{{l.text}}</p></div></sc-for>
</div>
<div style="display:flex;flex-direction:column;gap:8px;margin-top:16px;font-size:17px">
<p style="margin:0"><b>Eine gute Runde:</b> mindestens 7 von 10 richtig, in Ruhe beantwortet.</p>
<p style="margin:0"><b>Zwei gute Runden</b> auf einer Stufe, und das Paket steigt eine Stufe höher. Dort gehen neue Lernformen auf.</p>
<p style="margin:0"><b>Klappt eine Runde nicht,</b> passiert nichts Schlimmes. Das Paket bleibt, wo es ist, und du probierst eine andere Lernform derselben Stufe.</p>
<p style="margin:0"><b>Der Kurztest</b> geht immer, zum Beispiel vor einer Arbeit.</p>
</div>
<button type="button" class="btn" onClick="{{closeSheet}}" style="width:100%;margin-top:18px;background:{{T.accent}};color:{{T.ink}}">Verstanden</button>
</div>
</sc-if>
<sc-if value="{{isCode}}" hint-placeholder-val="{{ false }}">
<div class="sheet" role="dialog" aria-label="Eltern-Bereich">
<h2 class="h" style="font-size:28px">Eltern-Bereich</h2>
<p style="margin:8px 0 0;font-size:18px">Lernverlauf, Noten, Lernplan bis zur Arbeit und Einstellungen. Der Bereich öffnet sich mit dem Eltern-Code.</p>
<label for="ecode" style="display:block;margin-top:16px;font-weight:700;font-size:16px">Eltern-Code (4 Ziffern)</label>
<div style="display:flex;gap:12px;margin-top:8px"><input id="ecode" type="password" inputmode="numeric" maxlength="4" autocomplete="off" style="flex:1;height:56px;border-radius:28px;border:2px solid {{T.ink}};padding:0 22px;font:inherit;font-size:24px;letter-spacing:.4em;background:#FFFFFF;color:{{T.ink}}"><button type="button" class="btn" onClick="{{closeSheet}}" style="background:{{T.accent}};color:{{T.ink}}">Öffnen</button></div>
</div>
</sc-if>
</div>
</sc-if>'''

BODY = ("<div style=\"width:768px;height:1024px;position:relative;overflow:hidden;font-family:'Figtree','Verdana',sans-serif;font-size:17px;line-height:1.4;background:{{T.ground}};color:{{T.ink}}\">\n"
        + MAIN + '\n' + SO + '\n' + EX + '\n' + RES + '\n' + SIDE + '\n' + SHEET + '\n</div>')

JS = r"""
class Component extends DCLogic {
  constructor(p){ super(p); const E = '__FACH__' === 'e';
    this.state = { scr: 'main', open: E ? { A: true, B: true } : { A: true, B: true }, sel: E ? ['7', '8', '4'] : ['3', '1', '2'], mod: null, hint: '', q: '', ov: {}, doneToday: 0, points: E ? 140 : 380,
      sheet: null, mode: 'norm', playMod: null, playInc: [], qi: 0, pick: -1, checked: false, res: [], pts: 0, tShown: 0, last: null, lastMod: null, fokus: false }; }
  renderVals() {
    const s = this.state, E = '__FACH__' === 'e', I = __ICONS__;
    const T = E ? { kicker: 'Englisch · Küste', welt: 'Küsten-Crew', ground: '#FFF4DE', band: '#0E7C86', bandMute: '#D3F1F1', accent: '#FF7F6B', ink: '#1D2A3A', mute: '#566273', tint: '#FFE3DC', rang: 'Schiffsjunge', rangNext: 'Ränge bis Admiral',
        edge: 'M0 12Q48 0 96 12T192 12T288 12T384 12T480 12T576 12T672 12T768 12V24H0Z', prompt: 'Was heißt das auf Deutsch?', hues: { A: '#8ED8D0', B: '#FFC97A', C: '#FFB0A5', D: '#B9C8FF', E: '#C5E59A' }, rgb: '14,124,134' }
      : { kicker: 'Mathe · Weltraum', welt: 'Winkel-Akademie', ground: '#F0EFFF', band: '#3B2FBF', bandMute: '#DCD8FF', accent: '#FFC53D', ink: '#1B1740', mute: '#5A5680', tint: '#FFF0C2', rang: 'Meteor', rangNext: 'noch ' + Math.max(0, 500 - s.points) + ' bis Komet',
        edge: 'M0 24Q384 -6 768 24Z', prompt: 'Welche Winkelart ist das?', hues: { A: '#FFC97A', B: '#FFA9D0' }, rgb: '59,47,191' };
    const G = E ? [['A', 'Unit 1 · Vokabeln'], ['B', 'Unit 2 · Vokabeln'], ['C', 'Unit 3 · Vokabeln'], ['D', 'Unregelmäßige Verben'], ['E', 'Grammatik · Simple Past']]
      : [['A', 'Winkelarten und Messen'], ['B', 'Kompass, Benennen, Rechnen']];
    const RAW = E ? [
      ['1', 'Familie', 'A', 'sicher', 4, 0], ['2', 'Zuhause', 'A', 'sicher', 4, 0], ['3', 'Schule', 'A', 'sicher', 4, 0, 1], ['4', 'Im Café', 'A', 'sicher', 4, 0, 1], ['5', 'Essen und Trinken', 'A', 'sicher', 3, 1], ['6', 'Einkaufen', 'A', 'sicher', 4, 0],
      ['7', 'Am Hafen', 'B', 'noch üben', 2, 1], ['8', 'Am Strand', 'B', 'noch üben', 2, 1], ['9', 'Wetter', 'B', 'noch üben', 1, 0], ['10', 'Auf dem Schiff', 'B', 'neu', 1, 0], ['11', 'Tiere am Meer', 'B', 'neu', 1, 0], ['12', 'Unterwegs', 'B', 'neu', 1, 0],
      ['13', 'Hobbys', 'C', 'neu', 1, 0], ['14', 'Sport', 'C', 'neu', 1, 0], ['15', 'Kleidung', 'C', 'neu', 1, 0], ['16', 'In der Stadt', 'C', 'neu', 1, 0], ['17', 'Ferien', 'C', 'neu', 1, 0], ['18', 'Gefühle', 'C', 'neu', 1, 0],
      ['V1', 'Verben 1–10', 'D', 'sicher', 3, 0], ['V2', 'Verben 11–20', 'D', 'noch üben', 2, 0], ['V3', 'Verben 21–30', 'D', 'neu', 1, 0], ['V4', 'Verben 31–40', 'D', 'neu', 1, 0],
      ['G1', 'Aussagesätze', 'E', 'noch üben', 2, 0], ['G2', 'Fragen, Verneinung', 'E', 'neu', 1, 0]
    ] : [
      ['1', 'Spitz & recht', 'A', 'sicher', 4, 0, 1], ['2', 'Stumpf & gestreckt', 'A', 'sicher', 3, 1], ['3', 'Überstumpf', 'A', 'noch üben', 2, 1], ['4', 'Grenzfälle', 'A', 'neu', 1, 0],
      ['5', 'Kompass', 'B', 'neu', 1, 0], ['6', 'Benennen', 'B', 'neu', 1, 0], ['7', 'Berechnen', 'B', 'neu', 1, 0], ['8', 'Senkrecht & parallel', 'B', 'neu', 1, 0]
    ];
    const PK = RAW.map((r) => { const o = s.ov[r[0]] || {}; const lvl = o.lvl || r[4];
      return { id: r[0], name: r[1], grp: r[2], st: r[3] === 'neu' && o.lvl ? 'noch üben' : r[3], lvl, good: o.good != null ? o.good : r[5], due: !!r[6] }; });
    const byId = {}; PK.forEach((p) => { byId[p.id] = p; });
    const STG = ['Kennenlernen', 'Mit Auswahl', 'Selbst machen', 'Ohne Hilfen'];
    const A4 = ['1', '2', '3', '4'], B4 = ['5', '6', '7', '8'];
    const MODS = E ? [
      { id: 'karten', t: 'Lernkarten', stage: 1, icon: I.karten }, { id: 'hoeren', t: 'Hör-Kapitän', stage: 1, icon: I.erkennen },
      { id: 'quiz', t: 'Quiz', stage: 2, icon: I.sortieren }, { id: 'raetsel', t: 'Buchstabenrätsel', stage: 2, icon: I.frei },
      { id: 'schreiben', t: 'Schreiben', stage: 3, icon: I.zeichnen }, { id: 'luecken', t: 'Lückensätze', stage: 3, icon: I.wissen },
      { id: 'zeit', t: 'Zeitrunde', stage: 4, icon: I.zeit }, { id: 'duell', t: 'Duell', stage: 4, icon: I.duell },
      { id: 'test', t: 'Kurztest mit Note', stage: 5, icon: I.test }
    ] : [
      { id: 'wissen', t: 'Wissen lesen', stage: 1, icon: I.wissen }, { id: 'karten', t: 'Lernkarten', stage: 1, icon: I.karten },
      { id: 'erkennen', t: 'Erkennen', stage: 2, icon: I.erkennen },
      { id: 'zeichnen', t: 'Zeichnen', stage: 3, icon: I.zeichnen, only: A4 }, { id: 'messen', t: 'Messen', stage: 3, icon: I.messen, only: A4 }, { id: 'mission', t: 'Aufgaben-Mission', stage: 3, icon: I.fernrohr, only: B4 },
      { id: 'schaetzen', t: 'Schätzen', stage: 4, icon: I.schaetzen, only: A4 }, { id: 'zeit', t: 'Zeitrunde', stage: 4, icon: I.zeit, only: A4 }, { id: 'duell', t: 'Duell', stage: 4, icon: I.duell },
      { id: 'test', t: 'Kurztest mit Note', stage: 5, icon: I.test }
    ];
    const PAL = ['#FFC53D', '#7FDCC8', '#FFA0C0', '#A9BEFF', '#FFB07A', '#C9E38F'];
    const selP = s.sel.map((id) => byId[id]), selN = selP.length;
    const colOf = (id) => PAL[Math.max(0, s.sel.indexOf(id)) % 6];
    const fits = (p, m) => (!m.only || m.only.indexOf(p.id) >= 0) && (m.stage === 5 || p.lvl >= m.stage);
    const runden = (n) => n === 1 ? '1 gute Runde' : n + ' gute Runden';
    const cond = (p, m) => (m.only && m.only.indexOf(p.id) < 0) ? 'passt nicht zu Paket ' + p.id
      : p.lvl === m.stage - 1 ? 'Paket ' + p.id + ': noch ' + runden(2 - p.good) + ' auf Stufe ' + p.lvl
      : 'Paket ' + p.id + ': erst Stufe ' + (m.stage - 1) + ' schaffen';
    const wordOf = (p) => p.st + (p.due ? ', wieder dran' : '');
    const coinOf = (p) => p.st === 'sicher' ? (p.due ? '+20 %' : 'wenige Punkte') : 'volle Punkte';
    const minL = selN ? Math.min.apply(null, selP.map((p) => p.lvl)) : 0;
    let cands = MODS.filter((m) => m.stage === minL && selP.some((p) => fits(p, m)));
    if (!cands.length) cands = MODS.filter((m) => selP.some((p) => fits(p, m)));
    const tip = cands.filter((m) => m.id !== s.lastMod && selP.every((p) => fits(p, m)))[0] || cands.filter((m) => m.id !== s.lastMod)[0] || cands[0] || null;
    const cur = (s.mod && MODS.filter((m) => m.id === s.mod)[0]) || tip;
    const inc = cur ? selP.filter((p) => fits(p, cur)) : [], exc = cur ? selP.filter((p) => !fits(p, cur)) : [];
    const ready = selN > 0 && inc.length > 0;
    const setSel = (ids, extra) => this.setState(Object.assign({ sel: ids, mod: null, hint: '', q: '' }, extra || {}));
    const toggle = (id) => () => { const st = this.state; const i = st.sel.indexOf(id);
      if (i >= 0) { setSel(st.sel.filter((x) => x !== id), { q: st.q }); return; }
      if (st.sel.length >= 6) { this.setState({ hint: 'Mehr als 6 Pakete passen nicht in eine Runde. Nimm eins heraus, dann geht es.' }); return; }
      setSel(st.sel.concat([id]), { q: st.q }); };
    const tokOf = (p) => { const hue = T.hues[p.grp], on = s.sel.indexOf(p.id) >= 0;
      return { label: p.id, name: p.name, word: wordOf(p), on, tf: on ? 'translateY(-3px)' : 'none',
        fill: p.st === 'sicher' ? hue : p.st === 'noch üben' ? 'linear-gradient(0deg, ' + hue + ' 50%, #FFFFFF 50%)' : '#FFFFFF',
        bd: p.st === 'neu' ? '2px dashed ' + T.mute : '2px solid ' + T.ink, ring: on ? '0 0 0 4px ' + T.accent + ', 0 0 0 6px ' + T.ink : 'none',
        aria: 'Paket ' + p.id + ', ' + p.name + ', ' + wordOf(p) + (on ? ', gewählt' : ''), toggle: toggle(p.id) }; };
    const stripOf = (list) => list.map((p) => ({ bg: p.st === 'sicher' ? T.ink : p.st === 'noch üben' ? 'linear-gradient(0deg, ' + T.ink + ' 50%, #FFFFFF 50%)' : '#FFFFFF', bd: p.st === 'neu' ? '1.5px dashed ' + T.mute : '1.5px solid ' + T.ink }));
    const infoOf = (list) => { const c = (w) => list.filter((p) => p.st === w).length; return [[c('sicher'), 'sicher'], [c('noch üben'), 'noch üben'], [c('neu'), 'neu']].filter((x) => x[0]).map((x) => x[0] + ' ' + x[1]).join(' · '); };
    const groups = G.map(([id, name]) => { const list = PK.filter((p) => p.grp === id), nSel = list.filter((p) => s.sel.indexOf(p.id) >= 0).length, open = !!s.open[id];
      return { name, open, rot: open ? 'rotate(90deg)' : 'none', strip: stripOf(list), info: infoOf(list), hasSel: nSel > 0, selText: nSel + ' gewählt', pks: list.map(tokOf),
        toggle: () => { const o = Object.assign({}, this.state.open); o[id] = !o[id]; this.setState({ open: o }); } }; });
    const ql = s.q.trim().toLowerCase(), found = ql ? PK.filter((p) => (p.name + ' ' + p.id).toLowerCase().indexOf(ql) >= 0).slice(0, 12) : [];
    const VOR = E ? ['7', '8', '4'] : ['3', '1', '2'];
    const firstNew = PK.filter((p) => p.st === 'neu')[0];
    const same = (a) => a.length === s.sel.length && a.every((x) => s.sel.indexOf(x) >= 0);
    const QP = [['Krabbis Vorschlag', VOR], ['Was dran ist', PK.filter((p) => p.due).slice(0, 6).map((p) => p.id)], ['Noch üben', PK.filter((p) => p.st === 'noch üben').slice(0, 6).map((p) => p.id)], ['Nächstes neues Paket', firstNew ? [firstNew.id] : []], ['Leeren', []]];
    const quick = QP.map(([t, ids]) => ({ t, bg: ids.length && same(ids) ? T.accent : '#FFFFFF', go: () => { const o = Object.assign({}, this.state.open); ids.forEach((id) => { o[byId[id].grp] = true; }); setSel(ids, { open: o }); } }));
    const modView = (m) => { const mi = selP.filter((p) => fits(p, m)), locked = mi.length === 0, on = !!cur && cur.id === m.id && !locked;
      const sub = !selN ? 'erst Pakete wählen' : locked ? cond(selP.filter((p) => !fits(p, m))[0], m) : m.stage === 5 ? 'geht immer, mit jeder Auswahl' : mi.length === selN ? (selN === 1 ? 'mit deinem Paket' : selN === 2 ? 'mit beiden Paketen' : 'mit allen ' + selN + ' Paketen') : 'mit ' + mi.length + ' von ' + selN + ' Paketen';
      return { t: m.t, icon: locked ? I.schloss : m.icon, sub, on, cls: locked ? 'lock' : '', tip: !locked && !!tip && tip.id === m.id,
        bd: locked ? T.mute : on ? T.ink : '#FFFFFF', bg: locked ? 'transparent' : on ? T.tint : '#FFFFFF', ink: locked ? T.mute : T.ink,
        pick: () => { if (!selN) { this.setState({ hint: 'Wähle oben zuerst ein Paket oder mehrere.' }); return; }
          if (locked) { this.setState({ hint: m.t + ' geht mit dieser Auswahl noch nicht. ' + selP.filter((p) => !fits(p, m)).map((p) => cond(p, m)).join('; ') + '.' }); return; }
          this.setState({ mod: m.id, hint: '' }); } }; };
    const steps = [1, 2, 3, 4].map((k) => { const pegs = selP.filter((p) => p.lvl === k);
      return { k, name: STG[k - 1], bg: 'rgba(' + T.rgb + ',' + (0.1 + k * 0.05) + ')', minH: 150 + k * 34, pegs: pegs.map((p) => ({ label: p.id, col: colOf(p.id) })), pegText: pegs.length ? '' : '', mods: MODS.filter((m) => m.stage === k).map(modView) }; });
    const w = (p) => p.st === 'sicher' ? (p.due ? 2 : 1) : 3;
    const coins = {}; inc.forEach((p) => { const c = coinOf(p); (coins[c] = coins[c] || []).push(p.id); });
    const coinText = Object.keys(coins).map((c) => c + ': Paket ' + coins[c].join(', ')).join(' · ');
    const excText = exc.length ? ' Noch nicht dabei: Paket ' + exc.map((p) => p.id).join(', ') + '.' : '';
    // Fragen
    const QE = [{ w: 'harbour', opts: ['Hafen', 'Strand', 'Hügel', 'Brücke'], ok: 0, ex: '„harbour“ heißt auf Deutsch „Hafen“.' }, { w: 'lighthouse', opts: ['Laterne', 'Leuchtturm', 'Hochhaus', 'Fackel'], ok: 1, ex: '„lighthouse“ heißt „Leuchtturm“: light ist das Licht, house das Haus.' },
      { w: 'seagull', opts: ['Seehund', 'Segel', 'Möwe', 'Muschel'], ok: 2, ex: '„seagull“ heißt „Möwe“. Der Seehund heißt „seal“.' }, { w: 'to order', opts: ['bezahlen', 'bringen', 'probieren', 'bestellen'], ok: 3, ex: '„to order“ heißt „bestellen“. Bezahlen heißt „to pay“.' }];
    const QM = [{ a: 230, opts: ['stumpfer Winkel', 'überstumpfer Winkel', 'spitzer Winkel', 'gestreckter Winkel'], ok: 1, ex: 'Der Bogen geht über die gerade Linie hinaus. Mehr als 180°, also überstumpf.' }, { a: 90, opts: ['spitzer Winkel', 'stumpfer Winkel', 'rechter Winkel', 'gestreckter Winkel'], ok: 2, ex: 'Die Schenkel stehen wie eine Zimmerecke zueinander: genau 90°, ein rechter Winkel.' },
      { a: 300, opts: ['überstumpfer Winkel', 'stumpfer Winkel', 'rechter Winkel', 'spitzer Winkel'], ok: 0, ex: 'Der Bogen läuft fast ganz herum. Mehr als 180° und weniger als 360°: überstumpf.' }, { a: 130, opts: ['spitzer Winkel', 'gestreckter Winkel', 'überstumpfer Winkel', 'stumpfer Winkel'], ok: 3, ex: 'Größer als ein rechter Winkel, aber noch keine gerade Linie: stumpf.' }];
    const QS = E ? QE : QM, qd = QS[Math.min(s.qi, 3)];
    const SOSRC = E ? ['7', '4', '8', 'V2'] : ['3', '1', '3', '2'];
    const srcIds = s.mode === 'standort' ? SOSRC : (s.playInc.length ? s.playInc : ['1']);
    const srcP = byId[srcIds[s.qi % srcIds.length]];
    const src = { label: srcP.id, name: srcP.name, word: srcP.st, col: s.mode === 'standort' ? T.hues[srcP.grp] : colOf(srcP.id) };
    const f = (v) => v.toFixed(1), rad = (qd.a || 0) * Math.PI / 180;
    const qv = { w: qd.w || '', rays: 'M320 140L200 140L' + f(200 + 120 * Math.cos(rad)) + ' ' + f(140 - 120 * Math.sin(rad)), arc: 'M244 140A44 44 0 ' + (qd.a > 180 ? 1 : 0) + ' 0 ' + f(200 + 44 * Math.cos(rad)) + ' ' + f(140 - 44 * Math.sin(rad)) };
    const lastR = s.res[s.qi] || {};
    const opts = qd.opts.map((t, i) => { const isOk = i === qd.ok, isSel = i === s.pick;
      return { t, on: isSel, cls: s.checked ? (isOk ? 'ok' : isSel ? 'no' : 'dim') : (isSel ? 'sel' : ''), hasMark: s.checked && (isOk || isSel), mark: isOk ? 'richtig' : 'deine Antwort', markCol: isOk ? '#0B5C40' : '#8A3C06',
        pick: () => { if (!this.state.checked) this.setState({ pick: i }); } }; });
    const begin = (mode, modId, incIds) => this.setState({ scr: 'ex', mode, playMod: modId, playInc: incIds, qi: 0, pick: -1, checked: false, res: [], pts: 0, tShown: Date.now(), hint: '' });
    const check = () => { const st = this.state; if (st.pick < 0 || st.checked) return;
      const ok = st.pick === qd.ok, fast = Date.now() - st.tShown < 1500, gain = st.mode === 'norm' && ok && !fast ? 10 : 0;
      this.setState({ checked: true, res: st.res.concat([{ ok, fast, id: srcP.id }]), pts: st.pts + gain }); };
    const next = () => { const st = this.state;
      if (st.qi < 3) { this.setState({ qi: st.qi + 1, pick: -1, checked: false, tShown: Date.now() }); return; }
      const correct = st.res.filter((r) => r.ok).length;
      if (st.mode === 'standort') { this.setState({ scr: 'sores', last: { correct } }); return; }
      const m = MODS.filter((x) => x.id === st.playMod)[0], good = correct >= 3 && st.res.filter((r) => r.fast).length < 2;
      const ov = Object.assign({}, st.ov), up = [];
      const lines = st.playInc.map((id) => { const p = byId[id], rs = st.res.filter((r) => r.id === id); let txt = '';
        if (m.stage === 5) txt = 'Test zählt nicht für die Treppe';
        else if (p.lvl > m.stage || p.lvl >= 4 && m.stage === 4) txt = 'steht schon auf Stufe ' + p.lvl;
        else if (!good) txt = 'bleibt auf Stufe ' + p.lvl + ', nichts verloren';
        else if (p.good + 1 >= 2) { ov[id] = { lvl: p.lvl + 1, good: 0 }; up.push(id); txt = 'steigt auf Stufe ' + (p.lvl + 1) + ' · ' + STG[p.lvl]; }
        else { ov[id] = { lvl: p.lvl, good: p.good + 1 }; txt = 'gute Runde 1 von 2 für Stufe ' + (p.lvl + 1); }
        return { label: id, name: p.name, col: PAL[Math.max(0, st.sel.indexOf(id)) % 6], score: rs.filter((r) => r.ok).length + ' von ' + rs.length + ' richtig', txt }; });
      const newStage = up.length ? byId[up[0]].lvl + 1 : 0;
      this.setState({ scr: 'res', ov, points: st.points + st.pts, doneToday: st.doneToday + 1, lastMod: st.playMod, mod: null,
        last: { correct, good, pts: st.pts, fastN: st.res.filter((r) => r.fast && r.ok).length, lines, up, newStage, modT: m.t,
          newMods: MODS.filter((x) => x.stage === newStage).map((x) => x.t).join(', ') } }); };
    const L = Object.assign({ correct: 0, good: false, pts: 0, fastN: 0, lines: [], up: [], newStage: 0, modT: '', newMods: '' }, s.last || {});
    const playM = MODS.filter((x) => x.id === s.playMod)[0];
    const FOK = E ? [['8', '1 von 2 richtig'], ['9', 'bisher kaum geübt'], ['V2', 'lange nicht geübt']] : [['3', '1 von 2 richtig'], ['2', 'unsicher bei „gestreckt“']];
    const started = PK.filter((p) => p.st !== 'neu');
    const left = Math.max(0, 3 - s.doneToday);
    const names = (ids) => ids.map((id) => '„' + byId[id].name + '“');
    return {
      T, isE: E, isM: !E, points: s.points, q: s.q,
      isMain: s.scr === 'main', isSo: s.scr === 'so', isSoRes: s.scr === 'sores', isEx: s.scr === 'ex', isRes: s.scr === 'res', isIch: s.scr === 'ich', isGem: s.scr === 'gem',
      goMain: () => this.setState({ scr: 'main', sheet: null }), goIch: () => this.setState({ scr: 'ich' }), goGem: () => this.setState({ scr: 'gem' }), openSo: () => this.setState({ scr: 'so' }),
      heuteCap: left ? 'Heute · Runde ' + (s.doneToday + 1) + ' von 3' : 'Heute · geschafft',
      heuteText: !left ? 'Drei Runden sind geschafft. Für heute reicht es, wenn du magst.' : s.fokus ? 'Dein Fokus ist gewählt. Unten siehst du, welche Lernform ich dir dafür empfehle.' : s.doneToday ? 'Gut gemacht. Nimm für die nächste Runde ruhig eine andere Lernform, das hilft beim Merken.' : 'Mein Vorschlag ist schon gewählt: ' + names(VOR.slice(0, 2)).join(' und ') + ' festigen, dazu ' + names(VOR.slice(2))[0] + ' auffrischen.',
      onSearch: (e) => this.setState({ q: e.target.value }), hasQ: !!ql, noQ: !ql, found: found.map(tokOf), foundText: found.length ? found.length + (found.length === 1 ? ' Paket gefunden' : ' Pakete gefunden') : 'Kein Paket gefunden. Probiere ein anderes Wort.',
      quick, groups, steps, tests: MODS.filter((m) => m.stage === 5).map(modView),
      openTreppe: () => this.setState({ sheet: 'treppe' }), openCode: () => this.setState({ sheet: 'code' }), closeSheet: () => this.setState({ sheet: null }),
      hasSheet: !!s.sheet, isTreppe: s.sheet === 'treppe', isCode: s.sheet === 'code',
      legend: [['Du lernst das Paket kennen: Karten lesen und anhören.'], ['Du erkennst die richtige Antwort unter mehreren.'], ['Du schreibst, zeichnest oder misst selbst.'], ['Ohne Hilfen, gegen die Uhr und im Duell.']].map((x, i) => ({ k: i + 1, name: STG[i], text: x[0], bg: 'rgba(' + T.rgb + ',' + (0.1 + (i + 1) * 0.05) + ')', h: 110 + i * 26 })),
      barTitle: !selN ? 'Noch kein Paket gewählt' : !cur ? 'Wähle eine Lernform' : cur.t + ' · 10 Aufgaben aus ' + (inc.length === 1 ? '1 Paket' : inc.length + ' Paketen'),
      mix: inc.map((p) => ({ label: p.id, col: colOf(p.id), w: w(p) })),
      barNote: s.hint || (!selN ? 'Tippe oben Pakete an oder nimm Krabbis Vorschlag.' : ready ? coinText + '.' + excText : 'Diese Lernform passt noch nicht zur Auswahl.'),
      barNoteCol: s.hint ? '#FFD08A' : '#D5D9E2', start: () => { if (ready) begin('norm', cur.id, inc.map((p) => p.id)); else this.setState({ hint: 'Erst ein Paket und eine passende Lernform wählen, dann geht es los.' }); },
      notReady: !ready, startBg: ready ? T.accent : '#8C93A3',
      soLen: 'etwa 12 Fragen aus ' + started.length + ' Paketen, 5 Minuten. Im Dummy sind es 4.', startSo: () => begin('standort', null, []),
      soScore: (L.correct || 0) + ' von 4 richtig', soGroups: G.map(([id, name]) => { const list = PK.filter((p) => p.grp === id); return { name, strip: stripOf(list), info: infoOf(list) }; }),
      soText: E ? 'Die meisten Pakete aus Unit 1 sind sicher. Am meisten lohnt es sich jetzt bei diesen drei.' : 'Paket 1 ist sicher. Am meisten lohnt es sich jetzt bei diesen beiden.',
      fokus: FOK.map(([id, why]) => { const t = tokOf(byId[id]); return { label: id, name: byId[id].name, word: byId[id].st, why, fill: t.fill, bd: t.bd }; }),
      takeFokus: () => { const o = {}; FOK.forEach(([id]) => { o[byId[id].grp] = true; }); this.setState({ scr: 'main', sel: FOK.map((x) => x[0]), mod: null, hint: '', fokus: true, open: o, q: '' }); },
      src, qv, opts, check, next, checked: s.checked, notChecked: !s.checked, noPick: s.pick < 0, checkBg: s.pick < 0 ? '#C9CDD6' : T.accent,
      segs: [0, 1, 2, 3].map((i) => ({ bg: i < s.res.length ? (s.res[i].ok ? '#0E7A54' : '#E08A3C') : i === s.qi ? T.ink : '#D9DCE3' })),
      exProgress: 'Aufgabe ' + (s.qi + 1) + ' von 4', exBadge: s.mode === 'standort' ? 'ohne Punkte' : s.pts + ' Punkte', exTitle: s.mode === 'standort' ? 'Standort' : playM ? playM.t : '',
      fbBg: lastR.ok ? (lastR.fast ? '#FFF0C2' : '#DFF5EA') : '#FFE9D6',
      fbHead: lastR.ok ? (lastR.fast ? 'Richtig, aber sehr schnell' : s.mode === 'standort' ? 'Richtig' : 'Richtig · +10 Punkte') : 'Noch nicht ganz',
      fbText: lastR.ok && lastR.fast ? (s.mode === 'standort' ? 'Lies die Frage in Ruhe, dann weiß ich besser, wo du stehst.' : 'Dafür gibt es diesmal keine Punkte. Lies die Frage in Ruhe, dann zählt es wieder.') : qd.ex,
      nextLabel: s.qi < 3 ? 'Weiter' : s.mode === 'standort' ? 'Zum Standort' : 'Zum Ergebnis',
      resHead: L.correct + ' von 4 richtig', resPts: L.pts,
      resText: L.good ? (L.up.length ? 'Eine gute Runde. Damit geht es eine Stufe höher.' : 'Eine gute Runde. Sie zählt für die Treppe.') : 'Das war noch knapp, und das ist in Ordnung. Probiere als Nächstes eine andere Lernform derselben Stufe.',
      hasUnlock: L.up.length > 0, unlockText: (L.up.length === 1 ? 'Paket ' + L.up[0] + ' steht' : 'Die Pakete ' + L.up.join(' und ') + ' stehen') + ' jetzt auf Stufe ' + L.newStage + ' „' + (STG[L.newStage - 1] || '') + '“. Neu dabei: ' + L.newMods + '.',
      resPk: L.lines, resPtsNote: L.fastN > 0 ? 'Bei ' + L.fastN + (L.fastN === 1 ? ' Aufgabe' : ' Aufgaben') + ' warst du sehr schnell. Dafür gab es keine Punkte.' : '10 Punkte für jede richtige Antwort.',
      resRound: 'Runde ' + Math.min(3, s.doneToday) + ' von 3', again: () => this.setState({ scr: 'main', sheet: null }), againLabel: 'Nächste Runde wählen',
      todayLit: s.doneToday > 0, todayDark: s.doneToday === 0
    };
  }
}
""".replace('__ICONS__', json.dumps(ICON))

common.FONT = FONTF
for fach, name, title in [('e', 'F-Englisch.dc.html', 'F · Englisch · Pakete wählen'), ('m', 'F-Mathe.dc.html', 'F · Mathe · Pakete wählen')]:
    open(outdir + '/' + name, 'w').write(common.page(title, CSS, BODY, JS.replace('__FACH__', fach)))
