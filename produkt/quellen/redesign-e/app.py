import sys, json
sys.path.insert(0, sys.argv[1]); out = sys.argv[2]
from common import *

CSS = r"""
body{margin:0}
*{box-sizing:border-box}
button{font:inherit;color:inherit;cursor:pointer;border:0;background:none;padding:0;text-align:left}
button:focus-visible,input:focus-visible{outline:3px solid #FF8A00;outline-offset:2px}
.h{font-family:'Bricolage Grotesque','Trebuchet MS',sans-serif;font-weight:800;letter-spacing:-.01em;margin:0}
.scr{position:absolute;left:0;top:0;width:768px;height:1024px;display:flex;flex-direction:column}
.cap13{font-size:13px;font-weight:700;letter-spacing:.06em;text-transform:uppercase}
.btn{display:flex;align-items:center;justify-content:center;gap:10px;min-height:56px;padding:0 26px;border-radius:18px;font-weight:700;font-size:19px;background:#FFC83D;color:#15173A}
.btn:hover{background:#FFD469}.btn:active{transform:translateY(1px)}
.btn.sec{background:#FFFFFF;border:2px solid #15173A}
.btn.ghost{background:rgba(255,255,255,.12);color:#FFFFFF;border:2px solid #7C84D6}
.btn.off{background:#E4DFD2;color:#5A5C78;cursor:default}
.row{display:flex;align-items:center;gap:14px;width:100%;height:56px;padding:0 20px 0 24px;color:#FFFFFF}
.row:hover{background:rgba(255,255,255,.07)}
.row.cur{background:rgba(255,200,61,.17)}
.row.cur:hover{background:rgba(255,200,61,.24)}
.weave{position:relative;flex:none;width:224px;height:56px;display:block}
.ln{position:absolute;width:4px;border-radius:2px;display:block}
.cap{position:absolute;top:8px;height:40px;border-radius:20px;display:block}
.nd{position:absolute;top:13px;width:30px;height:30px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:15px}
.rtx{flex:1;min-width:0;display:flex;flex-direction:column;gap:1px}
.rt{font-weight:700;font-size:17px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.rs{font-size:14px;color:#C3C8F2}
.bdg{flex:none;padding:3px 10px;border-radius:999px;font-size:13px;font-weight:700;letter-spacing:.04em}
.ric{flex:none;width:40px;height:40px;border-radius:12px;display:flex;align-items:center;justify-content:center}
.tchip{display:flex;align-items:center;gap:6px;padding:6px 10px;border-radius:12px;font-size:14px;font-weight:700;background:#F1ECDF;color:#3D3F63;white-space:nowrap}
.tchip.cur{background:#15173A;color:#FFFFFF}
.tchip.done{background:#DFF5EA;color:#0B5C40}
.tab{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:2px;font-size:14px;font-weight:700;color:#5A5C78;height:100%}
.tab .ti{width:56px;height:32px;border-radius:16px;display:flex;align-items:center;justify-content:center}
.tab.on{color:#15173A}.tab.on .ti{background:#FFC83D}
.ans{display:flex;align-items:center;justify-content:space-between;gap:10px;min-height:76px;padding:0 22px;border-radius:20px;background:#FFFFFF;border:2px solid #CFC8B6;font-size:21px;font-weight:700}
.ans:hover{border-color:#15173A}
.ans.sel{border:3px solid #15173A;background:#FFF3CC}
.ans.ok{border:3px solid #0E7A54;background:#DFF5EA}
.ans.no{border:3px dashed #B4500A;background:#FFE9D6}
.ans.dim{color:#5A5C78;cursor:default}
.ans .mk{font-size:14px;font-weight:700}
.pk{display:flex;flex-direction:column;align-items:flex-start;gap:6px;min-height:104px;padding:12px;border-radius:18px;background:#FFFFFF;border:2px solid #CFC8B6}
.pk.on{border:3px solid #15173A;padding:11px;background:#FFF3CC}
.pk.lock{background:#F1ECDF;border-style:dashed;color:#5A5C78;cursor:default}
.dot{flex:none;width:30px;height:30px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:15px;color:#15173A}
.md{display:flex;align-items:center;gap:10px;min-height:64px;padding:8px 12px;border-radius:16px;background:#FFFFFF;border:2px solid #CFC8B6;font-weight:700;font-size:16px}
.md.on{border:3px solid #15173A;padding:7px 11px;background:#FFF3CC}
.md.lock{background:#F1ECDF;border-style:dashed;color:#5A5C78;cursor:default}
.md small{display:block;font-size:13px;font-weight:400;color:#5A5C78}
.card{background:#FFFFFF;border-radius:22px;padding:18px 20px}
.st{display:inline-flex;align-items:center;gap:6px;font-size:14px;font-weight:700}
.sheet{position:absolute;left:0;right:0;bottom:0;background:#FBF8F1;border-radius:30px 30px 0 0;padding:14px 28px 28px;color:#15173A;max-height:860px;overflow-y:auto}
.scrim{position:absolute;left:0;top:0;width:768px;height:1024px;background:rgba(10,11,40,.55);cursor:default}
@keyframes schnuppe{0%{transform:translate(0,0);opacity:0}4%{opacity:.7}12%{transform:translate(-300px,150px);opacity:0}100%{transform:translate(-300px,150px);opacity:0}}
.schnuppe{position:absolute;left:640px;top:20px;width:70px;height:2px;border-radius:2px;background:#FFFFFF;transform-origin:right center;rotate:-27deg;animation:schnuppe 16s linear infinite;opacity:0}
@keyframes wink{0%,100%{transform:rotate(0)}50%{transform:rotate(-4deg)}}
.kr{animation:wink 5s ease-in-out infinite;transform-origin:50% 90%}
@media (prefers-reduced-motion:reduce){.schnuppe,.kr{animation:none}}
"""

STARS = '<svg width="768" height="330" viewBox="0 0 768 330" aria-hidden="true" style="position:absolute;left:0;top:0;pointer-events:none">' + ''.join(
    '<circle cx="%d" cy="%d" r="%s" fill="#FFFFFF" opacity="%s"></circle>' % t for t in
    [(40,30,1.5,.7),(130,90,1,.5),(210,24,2,.6),(300,70,1,.5),(388,18,1.5,.8),(470,58,1,.5),(560,28,2,.5),(700,84,1.5,.6),(740,30,1,.7),(96,180,1,.4),(730,210,1.5,.4),(20,260,1.5,.5),(748,300,1,.5)]) + '</svg>'

def pathicon(hole, size=22, color='currentColor'):
    return '<svg width="%d" height="%d" viewBox="0 0 24 24" aria-hidden="true"><path d="{{%s}}" fill="none" stroke="%s" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path></svg>' % (size, size, hole, color)

TABBAR = '''<sc-if value="{{showTabs}}" hint-placeholder-val="{{ true }}">
<nav aria-label="Hauptbereiche" style="position:absolute;left:0;bottom:0;width:768px;height:80px;display:flex;background:#FBF8F1;border-top:1px solid #DAD3C2;padding:0 40px">
<sc-for list="{{tabs}}" as="t" hint-placeholder-count="4">
<button type="button" class="tab {{t.cls}}" onClick="{{t.go}}" aria-pressed="{{t.on}}"><span class="ti">''' + pathicon('t.icon', 24) + '''</span><span>{{t.label}}</span></button>
</sc-for>
</nav>
</sc-if>'''

WEG = '''<sc-if value="{{isWeg}}" hint-placeholder-val="{{ true }}">
<div class="scr" style="background:#171A45;color:#FFFFFF;padding-bottom:80px">
''' + STARS + '''<div class="schnuppe" aria-hidden="true"></div>
<div style="position:relative;display:flex;align-items:center;justify-content:space-between;height:68px;padding:0 24px;flex:none">
<div style="display:flex;flex-direction:column">
<span class="cap13" style="color:#C3C8F2">Mathe · Weltraum</span>
<h1 class="h" style="font-size:26px;line-height:1.1">Winkel-Akademie</h1>
</div>
<button type="button" onClick="{{goIch}}" aria-label="Rang und Punkte ansehen" style="display:flex;align-items:center;gap:10px;min-height:48px;padding:4px 16px 4px 8px;border-radius:24px;background:#262B6B;border:1px solid #4A52A8">
''' + rank('meteor', 36, '#FFFFFF') + '''
<span style="display:flex;flex-direction:column;line-height:1.15"><span style="font-weight:700;font-size:16px">Meteor</span><span style="font-size:14px;color:#C3C8F2">{{points}} Punkte</span></span>
</button>
</div>
<div style="position:relative;display:flex;align-items:flex-end;gap:6px;padding:0 24px 0 14px;flex:none">
<div class="kr" style="flex:none;margin-bottom:-4px">''' + krabbi(118, 'helm', label='Krabbi mit Raumhelm') + '''</div>
<div style="position:relative;flex:1;background:#FBF8F1;color:#15173A;border-radius:24px;padding:16px 20px 18px;display:flex;flex-direction:column;gap:12px">
<div style="position:absolute;left:-8px;bottom:44px;width:18px;height:18px;background:#FBF8F1;transform:rotate(45deg);border-radius:3px"></div>
<span class="cap13" style="color:#5A5C78">{{heuteLabel}}</span>
<p style="margin:0;font-size:18px;line-height:1.4">{{heuteText}}</p>
<div style="display:flex;gap:8px;flex-wrap:wrap">
<sc-for list="{{today}}" as="t" hint-placeholder-count="3">
<span class="tchip {{t.cls}}">''' + pathicon('t.icon', 18) + '''<span>{{t.label}}</span></span>
</sc-for>
</div>
<button type="button" class="btn" onClick="{{startCur}}" style="align-self:stretch">Weiterfliegen: {{curShort}} ''' + icon('pfeil', 22) + '''</button>
</div>
</div>
<div style="position:relative;display:flex;align-items:center;gap:14px;padding:18px 24px 6px;flex:none">
<div style="display:flex;width:224px;flex:none">
<sc-for list="{{heads}}" as="p" hint-placeholder-count="4">
<button type="button" onClick="{{p.open}}" aria-label="{{p.aria}}" style="width:56px;height:48px;display:flex;align-items:center;justify-content:center"><span class="dot" style="width:36px;height:36px;font-size:17px;background:{{p.bg}};border:{{p.bd}};color:{{p.ink}}">{{p.n}}</span></button>
</sc-for>
</div>
<div style="flex:1;min-width:0">
<h2 class="h" style="font-size:20px">Flugkarte · Abschnitt 1: Winkelarten</h2>
<p style="margin:0;font-size:14px;color:#C3C8F2">Jede Leuchtspur ist ein Paket. Wo Spuren zusammenlaufen, wird gemischt.</p>
</div>
</div>
<div style="position:relative;flex:1;min-height:0;overflow-y:auto">
<button type="button" class="row" onClick="{{toggleDone}}" aria-expanded="{{showDone}}" style="height:44px">
<span class="weave" style="height:44px">
<sc-for list="{{togLines}}" as="l" hint-placeholder-count="2"><span class="ln" style="left:{{l.x}}px;top:0;height:44px;background:{{l.bg}}"></span></sc-for>
</span>
<span style="font-size:15px;font-weight:700;color:#C3C8F2;text-decoration:underline;text-underline-offset:3px">{{togLabel}}</span>
</button>
<sc-for list="{{rows}}" as="r" hint-placeholder-count="9">
<button type="button" class="row {{r.cls}}" onClick="{{r.open}}" aria-label="{{r.aria}}">
<span class="weave">
<sc-for list="{{r.lines}}" as="l" hint-placeholder-count="3"><span class="ln" style="left:{{l.x}}px;top:{{l.top}}px;height:{{l.h}}px;background:{{l.bg}};opacity:{{l.op}}"></span></sc-for>
<span class="cap" style="left:{{r.capX}}px;width:{{r.capW}}px;background:{{r.capBg}};border:{{r.capBd}}"></span>
<sc-for list="{{r.nodes}}" as="n" hint-placeholder-count="2"><span class="nd" style="left:{{n.x}}px;background:{{n.bg}};border:{{n.bd}};color:{{n.ink}}">{{n.n}}</span></sc-for>
</span>
<span class="rtx"><span class="rt" style="color:{{r.tcol}}">{{r.title}}</span><span class="rs">{{r.sub}}</span></span>
<sc-if value="{{r.hasBadge}}" hint-placeholder-val="{{ false }}"><span class="bdg" style="background:{{r.badgeBg}};color:#15173A">{{r.badge}}</span></sc-if>
<span class="ric" style="background:{{r.icBg}};color:{{r.icCol}}">''' + pathicon('r.icon', 22) + '''</span>
</button>
</sc-for>
<div style="display:flex;align-items:center;gap:14px;margin:10px 24px 16px;padding:14px 18px;border-radius:18px;border:2px dashed #5C64B8;color:#FFFFFF">
<span style="flex:none;color:#FFC83D">''' + icon('fernrohr', 30) + '''</span>
<div><div style="font-weight:700;font-size:16px">Im Fernrohr: Abschnitt 2 · Kompass und Kurs</div><div style="font-size:14px;color:#C3C8F2">Mit Schatzsuche nach Himmelsrichtungen. Geht auf nach dem Kurztest.</div></div>
</div>
</div>
</div>
</sc-if>'''

SHEET = '''<sc-if value="{{hasSheet}}" hint-placeholder-val="{{ false }}">
<div style="position:absolute;left:0;top:0;width:768px;height:1024px;z-index:5">
<button type="button" class="scrim" onClick="{{closeSheet}}" aria-label="Schließen"></button>
<sc-if value="{{isStSheet}}" hint-placeholder-val="{{ false }}">
<div class="sheet" role="dialog" aria-label="{{sh.title}}">
<div style="width:56px;height:5px;border-radius:3px;background:#CFC8B6;margin:0 auto 16px"></div>
<div style="display:flex;align-items:center;gap:14px">
<span class="ric" style="width:52px;height:52px;border-radius:16px;background:#15173A;color:#FFC83D">''' + pathicon('sh.icon', 28) + '''</span>
<div style="flex:1"><span class="cap13" style="color:#5A5C78">{{sh.kicker}}</span><h2 class="h" style="font-size:28px;line-height:1.1">{{sh.title}}</h2></div>
<button type="button" onClick="{{closeSheet}}" aria-label="Schließen" style="width:48px;height:48px;border-radius:24px;background:#F1ECDF;display:flex;align-items:center;justify-content:center">''' + icon('x', 22) + '''</button>
</div>
<p style="margin:16px 0 0;font-size:18px">{{sh.was}}</p>
<div style="margin-top:18px">
<span class="cap13" style="color:#5A5C78">Die Mischung · 10 Aufgaben</span>
<div style="display:flex;gap:3px;height:18px;margin-top:8px;border-radius:9px;overflow:hidden">
<sc-for list="{{sh.mix}}" as="m" hint-placeholder-count="3"><span style="flex-grow:{{m.c}};flex-basis:0;background:{{m.col}}"></span></sc-for>
</div>
<div style="display:flex;flex-direction:column;gap:6px;margin-top:10px">
<sc-for list="{{sh.mix}}" as="m" hint-placeholder-count="3">
<div style="display:flex;align-items:center;gap:10px;font-size:16px"><span class="dot" style="width:26px;height:26px;font-size:14px;background:{{m.col}}">{{m.n}}</span><span style="font-weight:700">{{m.c}} × {{m.name}}</span><span style="color:#5A5C78">{{m.tag}}</span></div>
</sc-for>
</div>
</div>
<div style="display:grid;grid-template-columns:repeat(2, minmax(0, 1fr));gap:12px;margin-top:18px">
<div class="card"><span class="cap13" style="color:#5A5C78">Warum jetzt?</span><p style="margin:6px 0 0;font-size:16px">{{sh.why}}</p></div>
<div style="display:flex;flex-direction:column;gap:12px">
<div class="card" style="display:flex;gap:12px;align-items:flex-start"><span style="flex:none;color:#8A5A00">''' + icon('muenze', 28) + '''</span><div><div style="font-weight:700;font-size:17px">{{sh.coin}}</div><div style="font-size:15px;color:#3D3F63">{{sh.coinWhy}}</div></div></div>
<div class="card"><span class="cap13" style="color:#5A5C78">Danach kommt</span><p style="margin:6px 0 0;font-size:16px;font-weight:700">{{sh.next}}</p></div>
</div>
</div>
<sc-if value="{{sh.locked}}" hint-placeholder-val="{{ false }}">
<div style="display:flex;gap:12px;align-items:center;margin-top:18px;padding:14px 18px;border-radius:18px;background:#F1ECDF;font-size:16px"><span style="flex:none">''' + icon('schloss', 26) + '''</span><span>{{sh.lockText}}</span></div>
</sc-if>
<sc-if value="{{sh.canStart}}" hint-placeholder-val="{{ true }}">
<button type="button" class="btn" onClick="{{sh.start}}" style="width:100%;margin-top:18px">{{sh.startLabel}}</button>
</sc-if>
</div>
</sc-if>
<sc-if value="{{isPkSheet}}" hint-placeholder-val="{{ false }}">
<div class="sheet" role="dialog" aria-label="{{ps.name}}">
<div style="width:56px;height:5px;border-radius:3px;background:#CFC8B6;margin:0 auto 16px"></div>
<div style="display:flex;align-items:center;gap:14px">
<span class="dot" style="width:52px;height:52px;font-size:24px;background:{{ps.col}}">{{ps.n}}</span>
<div style="flex:1"><span class="cap13" style="color:#5A5C78">Paket {{ps.n}} · {{ps.st}}</span><h2 class="h" style="font-size:28px;line-height:1.1">{{ps.name}}</h2></div>
<button type="button" onClick="{{closeSheet}}" aria-label="Schließen" style="width:48px;height:48px;border-radius:24px;background:#F1ECDF;display:flex;align-items:center;justify-content:center">''' + icon('x', 22) + '''</button>
</div>
<p style="margin:16px 0 0;font-size:18px">{{ps.ziel}}</p>
<div class="card" style="margin-top:16px"><span class="cap13" style="color:#5A5C78">Dein Stand</span><p style="margin:6px 0 0;font-size:16px">{{ps.info}}</p></div>
<sc-if value="{{ps.reached}}" hint-placeholder-val="{{ true }}">
<button type="button" class="btn sec" onClick="{{goFrei}}" style="width:100%;margin-top:16px">Frei üben mit diesem Paket</button>
</sc-if>
</div>
</sc-if>
<sc-if value="{{isCodeSheet}}" hint-placeholder-val="{{ false }}">
<div class="sheet" role="dialog" aria-label="Eltern-Bereich">
<div style="width:56px;height:5px;border-radius:3px;background:#CFC8B6;margin:0 auto 16px"></div>
<h2 class="h" style="font-size:28px">Eltern-Bereich</h2>
<p style="margin:10px 0 0;font-size:18px">Hier stehen Lernverlauf, Übungsrhythmus, Noten, Lernplan bis zur Arbeit und Einstellungen. Der Bereich öffnet sich mit dem Eltern-Code.</p>
<label for="ecode" style="display:block;margin-top:18px;font-weight:700;font-size:16px">Eltern-Code (4 Ziffern)</label>
<div style="display:flex;gap:12px;margin-top:8px">
<input id="ecode" type="password" inputmode="numeric" maxlength="4" autocomplete="off" style="flex:1;height:56px;border-radius:16px;border:2px solid #15173A;padding:0 18px;font:inherit;font-size:24px;letter-spacing:.4em;background:#FFFFFF;color:#15173A">
<button type="button" class="btn" onClick="{{closeSheet}}">Öffnen</button>
</div>
<button type="button" onClick="{{closeSheet}}" style="margin-top:14px;min-height:44px;font-size:16px;font-weight:700;text-decoration:underline;text-underline-offset:3px">Zurück</button>
</div>
</sc-if>
</div>
</sc-if>'''

EX = '''<sc-if value="{{isEx}}" hint-placeholder-val="{{ false }}">
<div class="scr" style="background:#FBF8F1;padding:20px 32px 28px;gap:18px">
<div style="display:flex;align-items:center;gap:16px;flex:none">
<button type="button" onClick="{{quitEx}}" aria-label="Übung beenden" style="width:48px;height:48px;border-radius:24px;background:#F1ECDF;display:flex;align-items:center;justify-content:center;flex:none">''' + icon('x', 22) + '''</button>
<div role="img" aria-label="{{exProgress}}" style="flex:1;display:flex;gap:6px">
<sc-for list="{{segs}}" as="g" hint-placeholder-count="4"><span style="flex:1;height:12px;border-radius:6px;background:{{g.bg}}"></span></sc-for>
</div>
<span style="flex:none;display:flex;align-items:center;gap:6px;font-weight:700;font-size:17px;padding:8px 14px;border-radius:999px;background:#15173A;color:#FFFFFF"><span style="color:#FFC83D;display:flex">''' + icon('muenze', 20) + '''</span>{{exPts}} Punkte</span>
</div>
<div style="display:flex;align-items:center;justify-content:space-between;gap:12px;flex:none">
<div style="display:flex;align-items:center;gap:10px;font-size:16px"><span class="dot" style="background:{{q.col}}">{{q.pn}}</span><span><strong>Paket {{q.pn}} · {{q.pname}}</strong> · {{q.ptag}}</span></div>
<span style="font-size:15px;color:#5A5C78">{{exTitle}} · {{exProgress}}</span>
</div>
<h1 class="h" style="font-size:32px;flex:none">Welche Winkelart ist das?</h1>
<div style="flex:none;height:300px;background:#FFFFFF;border-radius:26px;border:1px solid #DAD3C2;display:flex;align-items:center;justify-content:center">
<svg width="440" height="280" viewBox="0 0 400 260" role="img" aria-label="Ein Winkel mit zwei Schenkeln und einem Bogen">
<path d="{{q.arc}}" fill="none" stroke="#F47B20" stroke-width="6" stroke-linecap="round"></path>
<path d="{{q.rays}}" fill="none" stroke="#15173A" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"></path>
<circle cx="200" cy="140" r="7" fill="#15173A"></circle>
</svg>
</div>
<div style="display:grid;grid-template-columns:repeat(2, minmax(0, 1fr));gap:12px;flex:none">
<sc-for list="{{opts}}" as="o" hint-placeholder-count="4">
<button type="button" class="ans {{o.cls}}" onClick="{{o.pick}}" aria-pressed="{{o.on}}"><span>{{o.t}}</span><sc-if value="{{o.hasMark}}" hint-placeholder-val="{{ false }}"><span class="mk" style="color:{{o.markCol}}">{{o.mark}}</span></sc-if></button>
</sc-for>
</div>
<div style="flex:1"></div>
<sc-if value="{{notChecked}}" hint-placeholder-val="{{ true }}">
<div style="display:flex;align-items:center;gap:16px;flex:none">
<p style="flex:1;margin:0;font-size:16px;color:#5A5C78">Erst antippen, dann prüfen. Du kannst deine Wahl vorher noch ändern.</p>
<button type="button" class="btn {{checkCls}}" onClick="{{check}}" style="min-width:220px">Prüfen</button>
</div>
</sc-if>
<sc-if value="{{checked}}" hint-placeholder-val="{{ false }}">
<div role="status" style="display:flex;align-items:center;gap:14px;padding:14px 18px 14px 10px;border-radius:24px;background:{{fbBg}};flex:none">
<div style="flex:none">''' + krabbi(76, 'helm') + '''</div>
<div style="flex:1"><div class="h" style="font-size:22px">{{fbHead}}</div><p style="margin:2px 0 0;font-size:17px">{{fbText}}</p></div>
<button type="button" class="btn" onClick="{{next}}" style="flex:none;background:#15173A;color:#FFFFFF">{{nextLabel}}</button>
</div>
</sc-if>
</div>
</sc-if>'''

RES = '''<sc-if value="{{isRes}}" hint-placeholder-val="{{ false }}">
<div class="scr" style="background:#171A45;color:#FFFFFF;padding:28px 32px;gap:16px">
''' + STARS + '''
<div style="position:relative;display:flex;align-items:center;gap:18px;flex:none">
<div class="kr" style="flex:none">''' + krabbi(130, 'helm', label='Krabbi') + '''</div>
<div><span class="cap13" style="color:#C3C8F2">{{exTitle}}</span><h1 class="h" style="font-size:40px;line-height:1.05">{{resHead}}</h1><p style="margin:8px 0 0;font-size:18px;color:#E6E8FB">{{resText}}</p></div>
</div>
<div style="position:relative;display:grid;grid-template-columns:repeat(2, minmax(0, 1fr));gap:14px;flex:none">
<div class="card" style="color:#15173A"><span class="cap13" style="color:#5A5C78">Punkte</span><div class="h" style="font-size:38px">+{{resPts}}</div><p style="margin:4px 0 0;font-size:15px;color:#3D3F63">{{resPtsNote}}</p></div>
<div class="card" style="color:#15173A"><span class="cap13" style="color:#5A5C78">Rang</span>
<div style="display:flex;align-items:center;gap:10px;margin-top:4px">''' + rank('meteor', 40) + '''<div style="flex:1"><div style="font-weight:700;font-size:18px">Meteor · {{points}} Punkte</div><div style="height:12px;border-radius:6px;background:#E4DFD2;margin-top:6px;overflow:hidden"><div style="height:12px;border-radius:6px;background:#F47B20;width:{{rankPct}}%"></div></div></div>''' + rank('komet', 32) + '''</div>
<p style="margin:6px 0 0;font-size:15px;color:#3D3F63">Noch {{toNext}} Punkte bis Komet.</p></div>
</div>
<div class="card" style="position:relative;color:#15173A;flex:none">
<span class="cap13" style="color:#5A5C78">So lief es je Paket</span>
<div style="display:flex;flex-direction:column;gap:10px;margin-top:10px">
<sc-for list="{{resPk}}" as="p" hint-placeholder-count="3">
<div style="display:flex;align-items:center;gap:12px;font-size:17px"><span class="dot" style="background:{{p.col}}">{{p.n}}</span><span style="flex:1;font-weight:700">{{p.name}}</span><span>{{p.score}}</span><span class="st" style="min-width:150px;justify-content:flex-end">{{p.st}}</span></div>
</sc-for>
</div>
</div>
<div class="card" style="position:relative;color:#15173A;flex:none;display:flex;align-items:center;gap:18px">
''' + week(True) + '''
<div><div style="font-weight:700;font-size:17px">Sternbild der Woche</div><p style="margin:2px 0 0;font-size:15px;color:#3D3F63">Heute leuchtet ein neuer Stern. Freie Tage löschen nichts.</p></div>
</div>
<div style="flex:1"></div>
<div style="position:relative;display:flex;gap:14px;flex:none">
<button type="button" class="btn ghost" onClick="{{replay}}" style="flex:1">Noch einmal üben</button>
<button type="button" class="btn" onClick="{{backToWeg}}" style="flex:1.4">Zurück zur Flugkarte ''' + icon('pfeil', 22) + '''</button>
</div>
</div>
</sc-if>'''

FREI = '''<sc-if value="{{isFrei}}" hint-placeholder-val="{{ false }}">
<div class="scr" style="background:#FBF8F1;padding:24px 28px 96px;gap:14px;overflow-y:auto">
<div style="flex:none"><h1 class="h" style="font-size:34px">Frei üben</h1><p style="margin:4px 0 0;font-size:17px;color:#3D3F63">Deine eigene Mischung aus allem, was du auf der Flugkarte schon erreicht hast. Neues gibt es nur dort.</p></div>
<div style="flex:none"><h2 class="h" style="font-size:20px;margin-bottom:8px">1 · Was? <span style="font-family:'Atkinson Hyperlegible',Verdana,sans-serif;font-weight:400;font-size:15px;color:#5A5C78;letter-spacing:0">Ein Paket oder mehrere</span></h2>
<div style="display:grid;grid-template-columns:repeat(4, minmax(0, 1fr));gap:10px">
<sc-for list="{{fPk}}" as="p" hint-placeholder-count="8">
<button type="button" class="pk {{p.cls}}" onClick="{{p.toggle}}" aria-pressed="{{p.on}}" aria-disabled="{{p.locked}}"><span style="display:flex;align-items:center;gap:8px"><span class="dot" style="background:{{p.col}}">{{p.n}}</span><sc-if value="{{p.locked}}" hint-placeholder-val="{{ false }}">''' + icon('schloss', 18) + '''</sc-if></span><span style="font-weight:700;font-size:16px;line-height:1.2">{{p.name}}</span><span style="font-size:14px">{{p.st}}</span></button>
</sc-for>
</div></div>
<div style="flex:none"><h2 class="h" style="font-size:20px;margin-bottom:8px">2 · Wie? <span style="font-family:'Atkinson Hyperlegible',Verdana,sans-serif;font-weight:400;font-size:15px;color:#5A5C78;letter-spacing:0">Eine Lernform</span></h2>
<div style="display:grid;grid-template-columns:repeat(3, minmax(0, 1fr));gap:10px">
<sc-for list="{{fMod}}" as="m" hint-placeholder-count="9">
<button type="button" class="md {{m.cls}}" onClick="{{m.pick}}" aria-pressed="{{m.on}}" aria-disabled="{{m.locked}}"><span style="flex:none;display:flex">''' + pathicon('m.icon', 24) + '''</span><span>{{m.t}}<small>{{m.note}}</small></span></button>
</sc-for>
</div></div>
<div style="flex:none;background:#171A45;color:#FFFFFF;border-radius:24px;padding:18px 20px;display:flex;flex-direction:column;gap:12px">
<div style="display:flex;align-items:center;justify-content:space-between;gap:12px"><div><span class="cap13" style="color:#C3C8F2">Deine Mischung</span><div class="h" style="font-size:22px">{{fTitle}}</div></div>
<button type="button" class="btn {{fStartCls}}" onClick="{{fStart}}">Mischung starten</button></div>
<div style="display:flex;gap:3px;height:14px;border-radius:7px;overflow:hidden;background:#262B6B">
<sc-for list="{{fMix}}" as="m" hint-placeholder-count="2"><span style="flex:1;background:{{m.col}}"></span></sc-for>
</div>
<div style="display:flex;flex-direction:column;gap:4px">
<sc-for list="{{fMix}}" as="m" hint-placeholder-count="2">
<div style="display:flex;align-items:center;gap:10px;font-size:15px"><span class="dot" style="width:24px;height:24px;font-size:13px;background:{{m.col}}">{{m.n}}</span><span><strong>{{m.coin}}</strong> · {{m.why}}</span></div>
</sc-for>
<sc-if value="{{fEmpty}}" hint-placeholder-val="{{ false }}"><p style="margin:0;font-size:15px;color:#C3C8F2">Wähle oben mindestens ein Paket.</p></sc-if>
</div>
</div>
</div>
</sc-if>'''

def gcard(ic, title, text, btn):
    return ('<div class="card" style="display:flex;align-items:center;gap:16px"><span class="ric" style="width:56px;height:56px;border-radius:18px;background:#15173A;color:#FFC83D">' + icon(ic, 30) + '</span><div style="flex:1"><div class="h" style="font-size:20px">' + title + '</div><p style="margin:2px 0 0;font-size:16px;color:#3D3F63">' + text + '</p></div><button type="button" class="btn sec" style="flex:none;font-size:17px;padding:0 18px">' + btn + '</button></div>')

GEM = '''<sc-if value="{{isGem}}" hint-placeholder-val="{{ false }}">
<div class="scr" style="background:#FBF8F1;padding:24px 28px 96px;gap:14px;overflow-y:auto">
<div style="flex:none"><h1 class="h" style="font-size:34px">Gemeinsam</h1><p style="margin:4px 0 0;font-size:17px;color:#3D3F63">Spielen mit Familie, Klasse und Freunden. Die Fragen kommen nur aus Paketen, die alle Mitspielenden schon erreicht haben.</p></div>
''' + gcard('seil', 'Tauziehen', 'Live gegeneinander. Jede richtige Antwort zieht das Seil zu dir.', 'Herausfordern') + gcard('geist', 'Geister-Duell', 'Gegen die Aufzeichnung von jemandem, der gerade keine Zeit hat.', 'Geist wählen') + gcard('rad', 'Fach-Glücksrad', 'Fragen aus allen Fächern gemischt, oder aus einem Fach.', 'Drehen') + '''
<h2 class="h" style="font-size:20px;margin-top:6px;flex:none">Deine Lerngruppen</h2>
<div style="display:grid;grid-template-columns:repeat(2, minmax(0, 1fr));gap:12px;flex:none">
<div class="card"><div style="font-weight:700;font-size:18px">Familie</div><p style="margin:2px 0 10px;font-size:15px;color:#3D3F63">3 dabei · du bist diese Woche auf Platz 2</p><button type="button" class="btn sec" style="min-height:48px;font-size:16px;width:100%">Rangliste ansehen</button></div>
<div class="card"><div style="font-weight:700;font-size:18px">Klasse 6b</div><p style="margin:2px 0 10px;font-size:15px;color:#3D3F63">11 dabei · du bist diese Woche auf Platz 5</p><button type="button" class="btn sec" style="min-height:48px;font-size:16px;width:100%">Rangliste ansehen</button></div>
</div>
<button type="button" class="btn sec" style="flex:none;border-style:dashed">Gruppe gründen oder mit Code beitreten</button>
</div>
</sc-if>'''

RANKS = [('staub','Sternenstaub','0'),('meteor','Meteor','200'),('komet','Komet','500'),('planet','Planet','1 000'),('pulsar','Pulsar','2 000'),('supernova','Supernova','4 000'),('galaxis','Galaxis-Legende','8 000')]
def ladder():
    s = '<div style="display:grid;grid-template-columns:repeat(7, minmax(0, 1fr));gap:6px;margin-top:12px">'
    for i, (k, n, p) in enumerate(RANKS):
        cur = i == 1; done = i < 1
        box = 'background:#FFC83D;' if cur else ('background:#262B6B;' if done else 'background:transparent;border:2px dashed #5C64B8;')
        s += ('<div style="display:flex;flex-direction:column;align-items:center;gap:4px;text-align:center"><div style="width:60px;height:60px;border-radius:20px;display:flex;align-items:center;justify-content:center;%s">%s</div><div style="font-size:14px;font-weight:700;line-height:1.15;color:%s">%s</div><div style="font-size:13px;color:#C3C8F2">ab %s</div></div>'
              % (box, rank(k, 42, '#15173A' if cur else '#FFFFFF'), '#FFC83D' if cur else '#FFFFFF', n, p))
    return s + '</div>'

def coinrow(t, d, bg):
    return '<div style="display:flex;align-items:center;gap:12px"><span style="flex:none;min-width:128px;text-align:center;padding:6px 10px;border-radius:999px;font-size:14px;font-weight:700;background:%s;color:#15173A">%s</span><span style="font-size:15px">%s</span></div>' % (bg, t, d)

ICH = '''<sc-if value="{{isIch}}" hint-placeholder-val="{{ false }}">
<div class="scr" style="background:#FBF8F1;padding-bottom:80px;overflow-y:auto">
<div style="position:relative;background:#171A45;color:#FFFFFF;padding:22px 28px 22px;flex:none">
<div style="display:flex;align-items:center;justify-content:space-between;gap:12px">
<div><span class="cap13" style="color:#C3C8F2">Ich · Mathe · Weltraum</span><h1 class="h" style="font-size:32px;line-height:1.1">Mika, Rang Meteor</h1></div>
<div style="text-align:right"><div class="h" style="font-size:32px;color:#FFC83D">{{points}}</div><div style="font-size:15px;color:#C3C8F2">Punkte · noch {{toNext}} bis Komet</div></div>
</div>
''' + ladder() + '''
</div>
<div style="padding:16px 28px 20px;display:flex;flex-direction:column;gap:14px">
<div class="card"><span class="cap13" style="color:#5A5C78">Wofür es Punkte gibt</span>
<div style="display:flex;flex-direction:column;gap:8px;margin-top:10px">
''' + coinrow('volle Punkte', 'Neues und alles, was du noch übst.', '#FFC83D') + coinrow('+20 % Bonus', 'Was du lange nicht geübt hast und wieder dran ist.', '#FFA366') + coinrow('wenige Punkte', 'Was schon sicher ist und noch nicht wieder dran ist.', '#E4DFD2') + coinrow('keine Punkte', 'Falsche Antworten und sehr schnelles Tippen ohne Lesen.', '#FFFFFF;border:2px dashed #5A5C78') + '''
</div></div>
<div class="card"><span class="cap13" style="color:#5A5C78">Meine Pakete</span>
<div style="display:grid;grid-template-columns:repeat(4, minmax(0, 1fr));gap:10px;margin-top:10px">
<sc-for list="{{allPk}}" as="p" hint-placeholder-count="8">
<div style="display:flex;align-items:center;gap:8px"><span class="dot" style="background:{{p.bg}};border:{{p.bd}}">{{p.n}}</span><span style="font-size:14px;line-height:1.2"><strong>{{p.name}}</strong><br>{{p.st}}</span></div>
</sc-for>
</div></div>
<div class="card" style="display:flex;align-items:center;gap:18px">
<sc-if value="{{todayLit}}" hint-placeholder-val="{{ false }}">''' + week(True) + '''</sc-if>
<sc-if value="{{todayDark}}" hint-placeholder-val="{{ true }}">''' + week(False) + '''</sc-if>
<div><div style="font-weight:700;font-size:17px">Sternbild der Woche</div><p style="margin:2px 0 0;font-size:15px;color:#3D3F63">{{weekText}}</p></div>
</div>
<div style="display:flex;gap:12px">
<button type="button" class="btn sec" style="flex:1;font-size:17px">Person wechseln</button>
<button type="button" class="btn sec" onClick="{{openCode}}" style="flex:1;font-size:17px">''' + icon('schloss', 20) + ''' Eltern-Bereich</button>
</div>
</div>
</div>
</sc-if>'''

BODY = ('<div style="width:768px;height:1024px;position:relative;overflow:hidden;font-family:' + BODYFONT + ';font-size:17px;line-height:1.4;background:#FBF8F1;color:#15173A">\n'
        + WEG + '\n' + FREI + '\n' + GEM + '\n' + ICH + '\n' + EX + '\n' + RES + '\n' + TABBAR + '\n' + SHEET + '\n</div>')

JS = r"""
class Component extends DCLogic {
  constructor(p){ super(p); this.state = { tab: 'weg', scr: 'main', sheet: null, showDone: false, cur: 'r9', extra: false, points: 380, doneToday: 0,
    playing: null, free: false, qi: 0, sel: -1, checked: false, res: [], pts: 0, tShown: 0, last: null, fSel: [true, false, true], fMod: 'erkennen' }; }
  renderVals() {
    const s = this.state, I = __ICONS__;
    const INK = '#15173A', STAGE = '#171A45';
    const PK = [
      { n: 1, name: 'Spitz & recht', col: '#FFC83D', st: 'sicher · wieder dran', ziel: 'Ich kann spitze und rechte Winkel erkennen und messen.', info: 'Sicher. Zuletzt vor 9 Tagen geübt, deshalb ist das Paket wieder dran. Einmal üben bringt 20 % Bonus und lässt den Stern wieder hell leuchten.', coin: '+20 % Bonus', why: 'lange nicht geübt' },
      { n: 2, name: 'Stumpf & gestreckt', col: '#5FE3C0', st: 'sicher', ziel: 'Ich kann stumpfe und gestreckte Winkel erkennen und zeichnen.', info: 'Sicher. Wieder dran in 3 Tagen. Bis dahin bringt freies Üben nur wenige Punkte.', coin: 'wenige Punkte', why: 'sicher, noch nicht wieder dran' },
      { n: 3, name: 'Überstumpf', col: '#FF93B8', st: 'noch üben', ziel: 'Ich kann überstumpfe Winkel erkennen und zeichnen.', info: 'Noch üben. Zweimal allein geübt, es klappt einigermaßen. Jetzt wird es mit Paket 1 und 2 gemischt.', coin: 'volle Punkte', why: 'noch nicht sicher' },
      { n: 4, name: 'Grenzfälle', col: '#9FB6FF', st: 'neu', ziel: 'Ich kann Nullwinkel und Vollwinkel unterscheiden.', info: 'Neu. Das Paket startet auf der Flugkarte, sobald Überstumpf gemischt einigermaßen klappt. Vorher lässt es sich nicht wählen.' },
      { n: 5, name: 'Kompass', col: '#FFA366', st: 'neu' }, { n: 6, name: 'Benennen', col: '#C9A2FF', st: 'neu' },
      { n: 7, name: 'Berechnen', col: '#8BE08B', st: 'neu' }, { n: 8, name: 'Senkrecht & parallel', col: '#7FD8F2', st: 'neu' }
    ];
    const MOD = {
      wissen: { t: 'Wissen lesen', was: 'Du liest das Wichtigste in Ruhe, mit Bildern. Am Ende kommen zwei kurze Fragen.' },
      erkennen: { t: 'Erkennen', was: 'Du siehst einen Winkel und tippst die richtige Winkelart an.' },
      messen: { t: 'Messen', was: 'Du legst das Geodreieck an und liest die Gradzahl ab.' },
      zeichnen: { t: 'Zeichnen', was: 'Du zeichnest einen Winkel mit einer vorgegebenen Größe, Schritt für Schritt wie im Heft.' },
      zeit: { t: 'Zeitrunde', was: '60 Sekunden: so viele Winkel richtig erkennen wie möglich. Dein Rekord wird gespeichert.' },
      schaetzen: { t: 'Schätzen', was: 'Ohne Geodreieck und ohne Auswahl: Wie groß ist der Winkel ungefähr?' },
      duell: { t: 'Duell', was: 'Tauziehen gegen Krabbi oder jemanden aus deiner Lerngruppe. Jede richtige Antwort zieht das Seil zu dir.' },
      test: { t: 'Kurztest', was: '10 Aufgaben ohne Hilfen. Am Ende bekommst du eine Note. Die beste Note zählt.' },
      sortieren: { t: 'Sortieren', was: 'Du ziehst Winkel-Bilder in die richtige Gruppe. Gleicher Stoff, anderer Blick.' }
    };
    const ST = [
      { id: 'r1', m: 'wissen', pk: [0], why: 'Am Anfang steht das Wissen: kurz lesen, was ein spitzer und ein rechter Winkel ist.' },
      { id: 'r2', m: 'erkennen', pk: [0], why: 'Erst erkennen, mit Auswahl. So siehst du schnell, ob das Gelesene angekommen ist.' },
      { id: 'r3', m: 'messen', pk: [0], why: 'Jetzt selbst machen: Mit dem Geodreieck merkst du dir die Winkel besser als nur durch Antippen.' },
      { id: 'r4', m: 'wissen', pk: [1], why: 'Paket 1 klappte gut genug. Deshalb kommt ein neues Paket dazu, zuerst allein.' },
      { id: 'r5', m: 'zeichnen', pk: [1], why: 'Selbst zeichnen statt antippen: ein anderer Blick auf dasselbe Paket.' },
      { id: 'r6', m: 'zeit', pk: [0, 1], why: 'Die erste Mischung: Paket 1 und 2 durcheinander, gegen die Uhr. So kommen die Aufgaben auch in der Arbeit.' },
      { id: 'r7', m: 'wissen', pk: [2], why: 'Paket 2 klappte gut genug. Neues Paket, zuerst allein: der überstumpfe Winkel.' },
      { id: 'r8', m: 'zeichnen', pk: [2], why: 'Überstumpfe Winkel selbst zeichnen, noch ohne die anderen Pakete.' },
      { id: 'r9', m: 'erkennen', pk: [0, 1, 2], why: 'Überstumpf hast du zweimal allein geübt, und es klappt einigermaßen. Jetzt kommt es zu Paket 1 und 2 dazu. Gemischt merkst du, ob du die Winkelarten auseinanderhalten kannst.', kr: 'Überstumpf kennst du jetzt allein. Heute mischen wir es mit Paket 1 und 2, so wie die Aufgaben in der Arbeit kommen.' },
      { id: 'rx', m: 'sortieren', pk: [0, 1, 2], extra: true, why: 'Die Misch-Runde war noch knapp. Statt dasselbe zu wiederholen, sortierst du Winkel-Bilder in Gruppen. Danach geht es normal weiter.', kr: 'Das üben wir noch einmal anders: Wir sortieren Bilder. Gleiche Winkel, anderer Blick.' },
      { id: 'r10', m: 'messen', pk: [0], bonus: true, why: 'Paket 1 hast du vor 9 Tagen zuletzt geübt. Bevor es verblasst, einmal messen. Dafür gibt es 20 % Bonus.', kr: 'Paket 1 hast du länger nicht geübt. Einmal nachleuchten lassen bringt 20 % Bonus.' },
      { id: 'r11', m: 'schaetzen', pk: [0, 1, 2], neu: true, why: 'Schätzen ist neu: ohne Geodreieck und ohne Auswahl. Das geht auf, wenn du die drei Pakete gemischt erkennst.', kr: 'Jetzt wird es spannend: Schätzen ohne Geodreieck. Das ist neu.' },
      { id: 'r12', m: 'wissen', pk: [3], why: 'Neues Paket, zuerst allein: Nullwinkel und Vollwinkel.' },
      { id: 'r13', m: 'erkennen', pk: [3], why: 'Erkennen mit Auswahl, nur das neue Paket.' },
      { id: 'r14', m: 'duell', pk: [0, 1, 2, 3], neu: true, why: 'Tauziehen mit allen vier Paketen. Das Duell geht auf, wenn Paket 4 einigermaßen klappt.' },
      { id: 'r15', m: 'test', pk: [0, 1, 2, 3], note: true, why: 'Der Abschluss des Abschnitts: 10 Aufgaben ohne Hilfen, mit Note.' }
    ].filter((x) => !x.extra || s.extra);
    const curIdx = Math.max(0, ST.findIndex((x) => x.id === s.cur));
    const ORDER = ['r1','r2','r3','r4','r5','r6','r7','r8','r9','rx','r10','r11','r12','r13','r14','r15'], LSTART = ['r1','r4','r7','r12'];
    const cx = (i) => 28 + i * 56;
    const titleOf = (x) => MOD[x.m].t + (x.extra ? ' · Extra-Station' : x.bonus ? ' · Paket 1 nachleuchten' : x.pk.length > 1 ? ' · gemischt' : ' · Paket ' + (x.pk[0] + 1));
    const mixOf = (x) => {
      const c = x.pk.length === 1 ? [10] : x.pk.length === 2 ? [4, 6] : x.pk.length === 3 ? [3, 2, 5] : [2, 2, 2, 4];
      return x.pk.map((p, k) => ({ n: PK[p].n, name: PK[p].name, col: PK[p].col, c: c[k], tag: x.pk.length > 1 && k === x.pk.length - 1 ? 'neu dabei' : (x.pk.length > 1 ? 'kennst du schon' : '') }));
    };
    const start = (id, free) => () => this.setState({ scr: 'ex', sheet: null, playing: id, free: !!free, qi: 0, sel: -1, checked: false, res: [], pts: 0, tShown: Date.now() });
    const build = (x, i) => {
      const status = i < curIdx ? 'done' : i === curIdx ? 'cur' : 'lock';
      const lo = x.pk[0], hi = x.pk[x.pk.length - 1];
      const lines = [];
      for (let l = 0; l < 4; l++) {
        if (ORDER.indexOf(x.id) < ORDER.indexOf(LSTART[l])) continue;
        const isStart = x.id === LSTART[l];
        lines.push({ x: cx(l) - 2, top: isStart ? 28 : 0, h: isStart ? 28 : 56, bg: PK[l].col, op: status === 'lock' ? 0.35 : 1 });
      }
      const nodes = x.pk.map((p) => ({ n: PK[p].n, x: cx(p) - 15,
        bg: status === 'lock' ? STAGE : PK[p].col, bd: status === 'lock' ? '2px solid ' + PK[p].col : '2px solid ' + PK[p].col, ink: status === 'lock' ? PK[p].col : INK }));
      const away = i - curIdx;
      const sub = status === 'done' ? 'geschafft' : status === 'cur' ? 'jetzt dran · ' + (x.bonus ? '+20 % Bonus' : 'volle Punkte') : away === 1 ? 'als Nächstes' : 'geht auf nach ' + away + ' Stationen';
      const badge = status === 'done' ? '' : x.bonus ? '+20 %' : x.neu ? 'NEU' : x.note ? 'Note' : x.extra ? 'Extra' : '';
      return { id: x.id, cls: status, title: titleOf(x), sub, tcol: status === 'lock' ? '#DADDF7' : '#FFFFFF',
        lines, nodes, capX: cx(lo) - 21, capW: (hi - lo) * 56 + 42,
        capBg: status === 'cur' ? '#FFFFFF' : status === 'done' ? 'rgba(255,255,255,.16)' : 'transparent',
        capBd: status === 'lock' ? '2px dashed #5C64B8' : '2px solid transparent',
        hasBadge: badge !== '', badge, badgeBg: x.bonus ? '#FFA366' : x.neu ? '#FFC83D' : '#FFFFFF',
        icon: status === 'done' ? I.check : I[x.m === 'zeit' ? 'zeit' : x.m], icBg: status === 'cur' ? '#FFC83D' : status === 'done' ? '#262B6B' : 'transparent', icCol: status === 'cur' ? INK : status === 'done' ? '#8BE0B6' : '#C3C8F2',
        aria: titleOf(x) + ', ' + sub, open: () => this.setState({ sheet: { t: 'st', id: x.id } }), status, away };
    };
    const all = ST.map(build);
    const rows = s.showDone ? all : all.slice(6);
    const cur = ST[curIdx], curRow = all[curIdx];
    const tIdx = ST.findIndex((x) => x.id === 'r9');
    const today = ST.slice(tIdx, tIdx + 3).map((x, k) => { const r = all[tIdx + k]; return { label: MOD[x.m].t, icon: r.status === 'done' ? I.check : I[x.m], cls: r.status === 'done' ? 'done' : r.status === 'cur' ? 'cur' : '' }; });
    const todayLeft = today.filter((t) => t.cls !== 'done').length;
    const sheet = s.sheet || {};
    let sh = { mix: [] }, ps = {};
    if (sheet.t === 'st') {
      const i = ST.findIndex((x) => x.id === sheet.id), x = ST[i], r = all[i], nx = ST[i + 1];
      sh = { title: titleOf(x), icon: I[x.m], kicker: r.status === 'done' ? 'Geschafft' : r.status === 'cur' ? 'Jetzt dran' : 'Kommt noch', was: MOD[x.m].was, why: x.why, mix: mixOf(x),
        coin: r.status === 'done' ? 'wenige Punkte' : x.bonus ? '+20 % Bonus' : 'volle Punkte',
        coinWhy: r.status === 'done' ? 'Schon geschafft und noch nicht wieder dran.' : x.bonus ? 'Lange nicht geübt.' : 'Hier lernst du Neues oder übst, was noch nicht sicher ist.',
        next: nx ? titleOf(nx) : 'Abschnitt 2 · Kompass und Kurs', locked: r.status === 'lock',
        lockText: (r.away === 1 ? 'Noch zu. Geht auf, sobald die Station davor geschafft ist.' : 'Noch zu. Geht auf nach ' + r.away + ' Stationen.') + ' Überspringen geht nicht, aber du siehst schon, was kommt.',
        canStart: r.status !== 'lock', startLabel: r.status === 'cur' ? 'Starten' : 'Noch einmal üben (wenige Punkte)', start: start(x.id) };
    }
    if (sheet.t === 'pk') { const p = PK[sheet.i]; ps = { n: p.n, name: p.name, col: p.col, st: p.st, ziel: p.ziel, info: p.info, reached: sheet.i < 3 }; }
    // Übung
    const QS = [
      { p: 2, a: 230, opts: ['stumpfer Winkel', 'überstumpfer Winkel', 'spitzer Winkel', 'gestreckter Winkel'], ok: 1, ex: 'Der Bogen geht über die gerade Linie hinaus. Das sind mehr als 180°, also überstumpf.' },
      { p: 0, a: 90, opts: ['spitzer Winkel', 'stumpfer Winkel', 'rechter Winkel', 'gestreckter Winkel'], ok: 2, ex: 'Die Schenkel stehen wie eine Zimmerecke zueinander: genau 90°, ein rechter Winkel.' },
      { p: 2, a: 300, opts: ['überstumpfer Winkel', 'stumpfer Winkel', 'rechter Winkel', 'spitzer Winkel'], ok: 0, ex: 'Der Bogen läuft fast ganz herum. Mehr als 180° und weniger als 360°: überstumpf.' },
      { p: 1, a: 130, opts: ['spitzer Winkel', 'gestreckter Winkel', 'überstumpfer Winkel', 'stumpfer Winkel'], ok: 3, ex: 'Größer als ein rechter Winkel, aber noch keine gerade Linie: zwischen 90° und 180°, also stumpf.' }
    ];
    const qd = QS[Math.min(s.qi, QS.length - 1)], rad = qd.a * Math.PI / 180, f = (v) => v.toFixed(1);
    const q = { pn: PK[qd.p].n, pname: PK[qd.p].name, col: PK[qd.p].col, ptag: qd.p === 2 ? 'neu dabei' : 'kennst du schon',
      rays: 'M320 140L200 140L' + f(200 + 120 * Math.cos(rad)) + ' ' + f(140 - 120 * Math.sin(rad)),
      arc: 'M244 140A44 44 0 ' + (qd.a > 180 ? 1 : 0) + ' 0 ' + f(200 + 44 * Math.cos(rad)) + ' ' + f(140 - 44 * Math.sin(rad)) };
    const lastR = s.res[s.qi] || {};
    const opts = qd.opts.map((t, i) => {
      const isOk = i === qd.ok, isSel = i === s.sel;
      return { t, on: isSel, cls: s.checked ? (isOk ? 'ok' : isSel ? 'no' : 'dim') : (isSel ? 'sel' : ''),
        hasMark: s.checked && (isOk || isSel), mark: isOk ? 'richtig' : 'deine Antwort', markCol: isOk ? '#0B5C40' : '#8A3C06',
        pick: () => { if (!this.state.checked) this.setState({ sel: i }); } };
    });
    const check = () => { const st = this.state; if (st.sel < 0 || st.checked) return;
      const ok = st.sel === qd.ok, fast = Date.now() - st.tShown < 1500, gain = ok && !fast ? 10 : 0;
      this.setState({ checked: true, res: st.res.concat([{ ok, fast, p: qd.p }]), pts: st.pts + gain }); };
    const next = () => { const st = this.state;
      if (st.qi < QS.length - 1) { this.setState({ qi: st.qi + 1, sel: -1, checked: false, tShown: Date.now() }); return; }
      const correct = st.res.filter((r) => r.ok).length, pass = correct >= 3, onPath = !st.free && st.playing === st.cur;
      const upd = { scr: 'res', points: st.points + st.pts, doneToday: st.doneToday + 1, last: { correct, pass, pts: st.pts, fastN: st.res.filter((r) => r.fast && r.ok).length, res: st.res, onPath, wasR9: st.playing === 'r9', extraNow: false } };
      if (onPath) {
        if (st.cur === 'r9' && !pass && !st.extra) { upd.extra = true; upd.cur = 'rx'; upd.last.extraNow = true; }
        else if (pass || st.cur === 'rx') { const ids = ST.map((x) => x.id), k = ids.indexOf(st.cur); upd.cur = ids[Math.min(k + 1, ids.length - 1)]; }
      }
      this.setState(upd); };
    const playing = ST.find((x) => x.id === s.playing);
    const exTitle = s.free ? 'Frei üben · ' + MOD[s.fMod].t : playing ? titleOf(playing) : '';
    const L = s.last || { correct: 0, pass: true, pts: 0, fastN: 0, res: [] };
    const resPk = [2, 0, 1].map((p) => { const rs = L.res.filter((r) => r.p === p); const okN = rs.filter((r) => r.ok).length;
      return { n: PK[p].n, name: PK[p].name, col: PK[p].col, score: okN + ' von ' + rs.length + ' richtig', st: p === 2 ? (okN === rs.length ? 'noch üben · fast sicher' : 'noch üben') : 'sicher' }; });
    const toNext = Math.max(0, 500 - s.points);
    // Frei üben
    const fCount = s.fSel.filter(Boolean).length;
    const fPk = PK.map((p, i) => { const locked = i > 2, on = !locked && s.fSel[i];
      return { n: p.n, name: p.name, col: locked ? '#DAD3C2' : p.col, st: locked ? 'kommt auf der Flugkarte' : p.st, locked, on, cls: locked ? 'lock' : on ? 'on' : '',
        toggle: () => { if (locked) return; const a = this.state.fSel.slice(); a[i] = !a[i]; this.setState({ fSel: a }); } }; });
    const FM = [['wissen', ''], ['erkennen', ''], ['messen', ''], ['zeichnen', ''], ['zeit', 'ab 2 Paketen'], ['schaetzen', 'geht auf nach 2 Stationen'], ['duell', 'geht auf nach 5 Stationen'], ['test', 'geht auf nach 6 Stationen']];
    const fMod = FM.map(([k, note], i) => { const locked = i > 4, unfit = k === 'zeit' && fCount < 2, on = !locked && !unfit && s.fMod === k;
      return { t: MOD[k].t, icon: locked ? I.schloss : I[k], note: locked ? note : unfit ? 'geht erst ' + note : (k === 'zeit' ? 'mit deiner Mischung' : ''), locked: locked || unfit, on, cls: locked || unfit ? 'lock' : on ? 'on' : '',
        pick: () => { if (locked || unfit) return; this.setState({ fMod: k }); } }; });
    const fModOk = !(s.fMod === 'zeit' && fCount < 2);
    const fMix = PK.slice(0, 3).filter((p, i) => s.fSel[i]).map((p) => ({ n: p.n, col: p.col, coin: p.coin, why: p.name + ': ' + p.why }));
    const fReady = fCount > 0 && fModOk;
    const TABS = [['weg', 'Flugkarte', I.weg], ['frei', 'Frei üben', I.frei], ['gem', 'Gemeinsam', I.gem], ['ich', 'Ich', I.ich]];
    const main = s.scr === 'main';
    const goTab = (k) => () => this.setState({ tab: k, scr: 'main', sheet: null });
    return {
      isWeg: main && s.tab === 'weg', isFrei: main && s.tab === 'frei', isGem: main && s.tab === 'gem', isIch: main && s.tab === 'ich',
      isEx: s.scr === 'ex', isRes: s.scr === 'res', showTabs: main,
      tabs: TABS.map(([k, label, icon]) => ({ label, icon, on: s.tab === k, cls: s.tab === k ? 'on' : '', go: goTab(k) })),
      points: s.points, toNext, rankPct: Math.round((s.points - 200) / 3),
      heuteLabel: todayLeft === 0 ? 'Heute · geschafft' : 'Heute · noch ' + todayLeft + (todayLeft === 1 ? ' Station' : ' Stationen') + ' · etwa ' + todayLeft * 4 + ' Minuten',
      heuteText: todayLeft === 0 ? 'Für heute bist du fertig. Du kannst aufhören oder noch weiterfliegen, ganz wie du magst.' : (cur.kr || 'Weiter geht es mit ' + titleOf(cur) + '.'),
      today, curShort: MOD[cur.m].t, startCur: start(cur.id),
      heads: PK.slice(0, 4).map((p, i) => ({ n: p.n, bg: i < 3 ? p.col : STAGE, bd: '2px solid ' + p.col, ink: i < 3 ? INK : p.col, aria: 'Paket ' + p.n + ', ' + p.name + ', ' + p.st, open: () => this.setState({ sheet: { t: 'pk', i } }) })),
      showDone: s.showDone, toggleDone: () => this.setState({ showDone: !s.showDone }),
      togLabel: s.showDone ? 'Geschaffte Stationen einklappen' : '6 Stationen geschafft · anzeigen',
      togLines: s.showDone ? [] : [{ x: cx(0) - 2, bg: PK[0].col }, { x: cx(1) - 2, bg: PK[1].col }],
      rows, hasSheet: !!s.sheet, isStSheet: sheet.t === 'st', isPkSheet: sheet.t === 'pk', isCodeSheet: sheet.t === 'code', sh, ps,
      closeSheet: () => this.setState({ sheet: null }), goIch: goTab('ich'), goFrei: goTab('frei'), openCode: () => this.setState({ sheet: { t: 'code' } }),
      q, opts, check, next, checked: s.checked, notChecked: !s.checked, checkCls: s.sel < 0 ? 'off' : '',
      segs: QS.map((_, i) => ({ bg: i < s.res.length ? (s.res[i].ok ? '#0E7A54' : '#E08A3C') : i === s.qi ? '#15173A' : '#DAD3C2' })),
      exProgress: 'Aufgabe ' + (s.qi + 1) + ' von ' + QS.length, exPts: s.pts, exTitle,
      fbBg: lastR.ok ? (lastR.fast ? '#FFF3CC' : '#DFF5EA') : '#FFE9D6',
      fbHead: lastR.ok ? (lastR.fast ? 'Richtig, aber sehr schnell' : 'Richtig · +10 Punkte') : 'Noch nicht ganz',
      fbText: lastR.ok && lastR.fast ? 'Dafür gibt es diesmal keine Punkte. Lies die Frage in Ruhe, dann zählt es wieder.' : qd.ex,
      nextLabel: s.qi < QS.length - 1 ? 'Weiter' : 'Zum Ergebnis',
      quitEx: () => this.setState({ scr: 'main', sheet: null }),
      resHead: L.correct + ' von 4 richtig', resPts: L.pts,
      resText: !L.onPath ? 'Gut geübt. Auf der Flugkarte geht es an derselben Stelle weiter.' : L.extraNow ? 'Das war noch knapp, und das ist in Ordnung. Ich habe dir eine Extra-Station eingebaut: gleiche Winkel, aber als Bilder zum Sortieren.' : L.pass ? (L.wasR9 ? 'Gelandet. Überstumpf klappt auch gemischt. Als Nächstes lassen wir Paket 1 nachleuchten.' : 'Gelandet. Die nächste Station ist offen.') : 'Das üben wir noch einmal. Die Station bleibt für dich offen.',
      resPtsNote: L.fastN > 0 ? 'Bei ' + L.fastN + (L.fastN === 1 ? ' Aufgabe' : ' Aufgaben') + ' warst du sehr schnell. Dafür gab es keine Punkte.' : '10 Punkte für jede richtige Antwort.',
      resPk, backToWeg: goTab('weg'), replay: start(s.playing, s.free),
      fPk, fMod, fMix, fEmpty: fCount === 0, fTitle: fCount === 0 ? 'Noch nichts gewählt' : MOD[s.fMod].t + ' mit ' + fCount + (fCount === 1 ? ' Paket' : ' Paketen'),
      fStartCls: fReady ? '' : 'off', fStart: () => { if (fReady) start(s.cur, true)(); },
      allPk: PK.map((p, i) => ({ n: p.n, name: p.name, st: p.st, bg: i < 3 ? p.col : '#FFFFFF', bd: i < 3 ? '2px solid ' + p.col : '2px dashed #5A5C78' })),
      todayLit: s.doneToday > 0, todayDark: s.doneToday === 0,
      weekText: s.doneToday > 0 ? '4 Sterne leuchten, auch der von heute. Freie Tage löschen nichts.' : '3 Sterne leuchten. Der Stern für heute wartet auf deine erste Station. Freie Tage löschen nichts.'
    };
  }
}
""".replace('__ICONS__', json.dumps(ICON))

open(out, 'w').write(page('E · Flugkarte · Klick-Dummy', CSS, BODY, JS))
