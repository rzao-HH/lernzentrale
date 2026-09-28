/* ===================== ⚔️ Arena: Tauziehen, Power-ups, Geister-Duell, Fach-Glücksrad ===================== */
(function(){
const AK={W:["winkelakademie-v1",3],Z:["wasserzauberschule-v1",3],E:["unit6-progress",3],D:["detektivbuero-v1",1]};
const AN={W:["📐","Mathe"],Z:["🪄","NWT"],E:["🐚","Englisch"],D:["🕵️","Deutsch"]};
const WIN=6,DUR=120000;
const LSg=k=>{try{return localStorage.getItem(k);}catch(e){return null;}};
const LSj=(k,d)=>{try{const v=localStorage.getItem(k);return v?JSON.parse(v):d;}catch(e){return d;}};
const LSs=(k,v)=>{try{localStorage.setItem(k,JSON.stringify(v));}catch(e){}};
const esc=s=>String(s==null?"":s).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const shuf=a=>{a=a.slice();for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]];}return a;};
const pick=a=>a[Math.floor(Math.random()*a.length)];
let DEV=LSg("lz-dev");if(!DEV){DEV="d"+Math.random().toString(36).slice(2,10);try{localStorage.setItem("lz-dev",DEV);}catch(e){}}
function meP(){try{const u=NU.list.find(x=>x.id===NU.cur)||NU.list[0];return{uid:u.id,gid:u.gid||u.id,acc:!!u.acc,name:u.name,e:u.e};}catch(e){return{uid:"u1",gid:"u1",acc:false,name:"Ich",e:"🙂"};}}
const gidOf=u=>{const x=NU.list.find(v=>v.id===u);return x&&x.gid||u;};
function curAppK(){try{return curApp||"";}catch(e){return "";}}
function appState(k,uid){const [b,r]=AK[k];return LSj(uid==="u1"?b:b+("@"+uid).repeat(r),null);}

/* ---------- Arena-Punkte ---------- */
function ptsKey(uid){return "lz-arena-pts@"+uid;}
function ptsGet(uid){return Object.assign({p:0,w:0,l:0,d:0},LSj(ptsKey(uid),{}));}
function ptsAdd(uid,res,stake){const P=ptsGet(uid);if(res==="w"){P.p+=10+stake;P.w++;}else if(res==="l"){P.p=Math.max(0,P.p-stake);P.l++;}else P.d++;LSs(ptsKey(uid),P);return P;}
window.lzArenaPts=ptsGet;

/* ---------- Transport: über die Datenbank der Lerngruppe (lz_push / lz_pull) ----------
   Jedes Gerät schreibt in jede seiner Lerngruppen „on:<gerät>“ (online-Zeichen, alle 8 s)
   und Nachrichten reihum in „tx:<gerät>:0…15“. Alle Geräte fragen alle 1–3 s nach Neuem.
   lz_pull immer mit p_since 0 (wie Abgleich und Lerngruppen); Doppeltes wird hier aussortiert. */
let ONLINE=[],HANDLERS=[],SEQ=0,nextPoll=0;
const DIAG={err:"",at:0,rows:0,seen:0,fails:0};window.__arenaDiag=DIAG;
const SEEN_P={},SINCE={},PRIMED={};
const RPCa=(fn,b)=>window.__lzRpc(fn,b);
/* Zeitstempel unabhängig von falsch gehenden Geräteuhren: nie kleiner als alles, was wir schon gesehen haben */
let CLK=0;const clk=()=>{const m=Math.max(0,...Object.values(SINCE));CLK=Math.max(Date.now(),m+1,CLK+1);return CLK;};
function myPresence(){const m=meP();return{dev:DEV,uid:m.uid,gid:m.gid,acc:m.acc,name:m.name,e:m.e,app:curAppK(),ts:Date.now()};}
function spaces(){const L=[];(window.lzMyGroups?lzMyGroups():[]).forEach(g=>L.push({id:"grp:"+g.code,label:g.name,alias:g.alias||""}));return L;}
function netOK(){return !!window.__lzRpc&&/^https:/.test((window.__LZSB||{}).url||"");}
function mergePres(){const m={},now=Date.now();Object.values(SEEN_P).forEach(x=>{const p=x.p;if(!p||p.dev===DEV||p.off||now-x.at>25000)return;if(!m[p.dev]||m[p.dev].ts<p.ts)m[p.dev]=Object.assign({},p,{spl:x.spl});});setOnline(Object.values(m));}
function setOnline(list){const sig=JSON.stringify(list.map(p=>[p.dev,p.name,p.e,p.app]));ONLINE=list.filter(p=>p&&p.dev!==DEV);if(sig!==setOnline.sig){setOnline.sig=sig;drawCard();drawPick();}}
async function push(items){for(const sp of spaces()){const it=items.map(x=>x.k.startsWith("on:")&&sp.alias?{k:x.k,v:JSON.stringify(Object.assign(JSON.parse(x.v),{name:sp.alias})),ts:x.ts}:x);try{await RPCa("lz_push",{p_fam:sp.id,p_items:it});DIAG.err="";}catch(e){DIAG.err="Senden: "+(e&&e.message||e);DIAG.fails++;drawCard();}}}
function send(msg){msg.from_dev=DEV;msg.mid=msg.mid||Math.random().toString(36).slice(2);if(!netOK())return;
  push([{k:"tx:"+DEV+":"+(SEQ++%16),v:JSON.stringify(msg),ts:clk()}]);nextPoll=0;}
const SEEN=new Set();
function recv(msg){if(!msg||msg.from_dev===DEV)return;if(msg.to&&msg.to!==DEV)return;if(msg.mid){if(SEEN.has(msg.mid))return;SEEN.add(msg.mid);}HANDLERS.forEach(h=>{try{h(msg);}catch(e){}});}
window.__arenaIn=function(s){const m=typeof s==="string"?JSON.parse(s):s;if(m.type!=="presence")recv(m);};
let lastBeat=0,lastSig="";
function beat(force){const p=Object.assign(myPresence(),{ts:clk()}),sig=[p.uid,p.app,p.name,p.e].join("|");if(!force&&sig===lastSig&&Date.now()-lastBeat<8000)return;lastSig=sig;lastBeat=Date.now();push([{k:"on:"+DEV,v:JSON.stringify(p),ts:p.ts}]);}
let polling=false;
async function poll(){if(polling||!netOK())return;polling=true;const now=Date.now();
  try{let nrows=0;for(const sp of spaces()){
    const rows=(await RPCa("lz_pull",{p_fam:sp.id,p_since:0}))||[];const first=!PRIMED[sp.id];PRIMED[sp.id]=1;nrows+=rows.length;
    rows.forEach(r=>{const ts=+r.ts||0;if(ts>(SINCE[sp.id]||0))SINCE[sp.id]=ts;let v=null;try{v=JSON.parse(r.v);}catch(e){}if(!v)return;
      if(r.k.startsWith("on:")){const key=sp.id+"|"+r.k,o=SEEN_P[key];
        if(!o){SEEN_P[key]={ts,p:v,spl:sp.label,at:Math.abs(Date.now()-ts)<20000?Date.now():0};}
        else if(o.ts!==ts){o.ts=ts;o.p=v;o.at=Date.now();}}
      else if(r.k.startsWith("tx:")){if(first){if(v.mid)SEEN.add(v.mid);}else recv(v);}});}
    DIAG.err="";DIAG.at=Date.now();DIAG.rows=nrows;DIAG.seen=Object.values(SEEN_P).filter(x=>x.p&&x.p.dev!==DEV&&!x.p.off).length;
  }catch(e){DIAG.err="Abfrage: "+(e&&e.message||e);DIAG.fails++;DIAG.at=Date.now();}polling=false;mergePres();if(VIEW==="pick")drawDiag();}
function diagText(){if(!spaces().length)return"";const ago=DIAG.at?Math.round((Date.now()-DIAG.at)/1000)+" s":"–";
  return DIAG.err?`⚠️ Arena-Server: ${esc(DIAG.err)} (${DIAG.fails}×)`:`Verbindung ok · zuletzt geprüft vor ${ago} · ${DIAG.seen} andere${DIAG.seen===1?"s":""} Gerät${DIAG.seen===1?"":"e"} gesehen`;}
function drawDiag(){const d=OV.querySelector(".ar-diag");if(d)d.textContent=diagText().replace(/&amp;/g,"&");}
function busyNow(){return (GAME&&!GAME.over)||VIEW==="wait"||VIEW==="pick"||INV.classList.contains("on");}
setInterval(()=>{if(document.hidden||!spaces().length)return;beat(false);const now=Date.now();if(now>=nextPoll){nextPoll=now+(busyNow()?900:3000);poll();}},300);
addEventListener("pagehide",()=>{if(!netOK())return;const p=Object.assign(myPresence(),{off:true,ts:clk()});push([{k:"on:"+DEV,v:JSON.stringify(p),ts:p.ts}]);});
document.addEventListener("visibilitychange",()=>{if(!document.hidden){beat(true);nextPoll=0;}});

/* ---------- Fragen aus den Apps ---------- */
const DATA={};
function loadApp(k){
  if(DATA[k])return Promise.resolve(DATA[k]);
  return new Promise(res=>{
    try{sessionStorage.setItem("nutzer-ok-"+k,"1");}catch(e){}
    const f=document.createElement("iframe");f.style.cssText="position:absolute;width:1px;height:1px;left:-9999px;top:0;opacity:0;border:0";f.setAttribute("aria-hidden","true");f.tabIndex=-1;
    let done=false;const fin=v=>{if(done)return;done=true;DATA[k]=v;setTimeout(()=>{try{f.remove();}catch(e){}},50);res(v);};
    f.onload=()=>setTimeout(()=>{let v=null;try{const w=f.contentWindow;
      if(k==="E")v=JSON.parse(JSON.stringify(w.eval('({W:WORDS,P:PKG_SIZE,V:VERBS.filter(v=>v.inf!=="be"),Q:QUESTIONS,X:DETECT.filter(x=>x.o),R:REGIRR,sel:(typeof kcSel==="function"?kcSel():["v0"])})')));
      else if(k==="Z")v=JSON.parse(JSON.stringify({T:w.__lzArena.TF,sel:w.__lzArena.sel()}));
      else if(k==="D")v=JSON.parse(JSON.stringify({I:w.__lzArena.I.filter(i=>i.t==="mc"&&i.o.length<=5||i.t==="comma"||i.t==="tap"),sel:w.__lzArena.sel()}));
    }catch(e){v=null;}fin(v);},250);
    setTimeout(()=>fin(null),8000);
    f.src=APPURL[k]+"?v=7.3.0";document.body.appendChild(f);});
}
const DEG=[{n:"Nullwinkel",f:a=>a===0},{n:"spitzer Winkel",f:a=>a>0&&a<90},{n:"rechter Winkel",f:a=>a===90},{n:"stumpfer Winkel",f:a=>a>90&&a<180},{n:"gestreckter Winkel",f:a=>a===180},{n:"überstumpfer Winkel",f:a=>a>180&&a<360},{n:"Vollwinkel",f:a=>a===360}];
function qW(sel){
  const S=new Set(sel&&sel.length?sel:["p1","p2","p3","p4","p5","p6","p7","p8"]),G=[];
  const opt=(a,others)=>shuf([a,...shuf(others.filter(x=>x!==a)).slice(0,3)]);
  const kind=a=>DEG.find(d=>d.f(a)).n;
  if(S.has("p1")||S.has("p2")||S.has("p3")||S.has("p4"))G.push(()=>{let pool=[];if(S.has("p1"))pool.push(15+5*Math.floor(Math.random()*15),90);if(S.has("p2"))pool.push(95+5*Math.floor(Math.random()*16),180);if(S.has("p3"))pool.push(185+5*Math.floor(Math.random()*34));if(S.has("p4"))pool.push(0,360,89,91,179,181);const a=pick(pool);
    return{k:"W",q:"Welche Winkelart ist das?",s:a+"°",o:opt(kind(a),DEG.map(d=>d.n)),a:kind(a)};});
  if(S.has("p5"))G.push(()=>{const D=["Norden","Osten","Süden","Westen"],i=Math.floor(Math.random()*4),turn=pick([90,180,270]),r=Math.random()<.5,j=(i+(r?1:-1)*turn/90+8)%4;
    return{k:"W",q:"Kompass",s:`Du schaust nach ${D[i]} und drehst dich um ${turn}° nach ${r?"rechts":"links"}. Wohin schaust du?`,o:D.slice(),a:D[j]};});
  if(S.has("p5"))G.push(()=>{const c=pick([["eine Vierteldrehung","90°"],["eine halbe Drehung","180°"],["eine Dreivierteldrehung","270°"],["eine ganze Drehung","360°"]]);return{k:"W",q:"Kompass",s:`Wie viel Grad sind ${c[0]}?`,o:shuf(["90°","180°","270°","360°"]),a:c[1]};});
  if(S.has("p6"))G.push(()=>{const c=pick([["Wie heißt der Punkt, an dem sich die Schenkel treffen?","Scheitel",["Schenkel","Winkelbogen","Strahl"]],["Wie heißen die beiden Strahlen eines Winkels?","Schenkel",["Scheitel","Bögen","Seiten"]],["Welcher griechische Buchstabe heißt „Beta“?","β",["α","γ","δ"]],["Welcher griechische Buchstabe heißt „Gamma“?","γ",["α","β","ε"]],["Womit zeichnet man einen Winkel genau?","Geodreieck",["Zirkel","Lineal allein","Kompass"]]]);return{k:"W",q:"Winkel benennen",s:c[0],o:shuf([c[1],...c[2]]),a:c[1]};});
  if(S.has("p7"))G.push(()=>{const t=Math.random();if(t<.4){const a=10+5*Math.floor(Math.random()*33),r=180-a;return{k:"W",q:"Winkel berechnen",s:`Nebenwinkel von ${a}° = ?`,o:shuf([r+"°",(r+10)+"°",(360-a)+"°",(90-a>0?90-a:r-20)+"°"].filter((x,i,A)=>A.indexOf(x)===i)),a:r+"°"};}
    if(t<.75){const a=20+5*Math.floor(Math.random()*16),b=20+5*Math.floor(Math.random()*(Math.max(1,(150-a)/5))),c=180-a-b;return{k:"W",q:"Winkel berechnen",s:`Im Dreieck: ${a}° und ${b}°. Wie groß ist der dritte Winkel?`,o:shuf([c+"°",(c+10)+"°",(c-5)+"°",(360-a-b)+"°"].filter((x,i,A)=>A.indexOf(x)===i)),a:c+"°"};}
    const a=30+10*Math.floor(Math.random()*15);return{k:"W",q:"Winkel berechnen",s:`Innenwinkel ${a}°. Wie groß ist der überstumpfe Winkel?`,o:shuf([(360-a)+"°",(180-a)+"°",(360-a+10)+"°",(a+180)+"°"].filter((x,i,A)=>A.indexOf(x)===i)),a:(360-a)+"°"};});
  if(S.has("p8"))G.push(()=>{const c=pick([["Zwei Geraden schneiden sich im rechten Winkel. Sie sind …","senkrecht zueinander",["parallel zueinander","gleich lang","gestreckt"]],["Zwei Geraden haben überall denselben Abstand. Sie sind …","parallel zueinander",["senkrecht zueinander","gekreuzt","spitz"]],["Welches Zeichen bedeutet „senkrecht zu“?","⊥",["∥","∠","≈"]],["Welches Zeichen bedeutet „parallel zu“?","∥",["⊥","∠","="]]]);return{k:"W",q:"Senkrechte & Parallelen",s:c[0],o:shuf([c[1],...c[2]]),a:c[1]};});
  return G.length?()=>pick(G)():null;
}
function qZ(d){if(!d||!d.T)return null;let T=d.T.filter(x=>!d.sel||!d.sel.length||d.sel.includes(x.p));if(!T.length)T=d.T;
  return()=>{const x=pick(T);return{k:"Z",q:"Stimmt das?",s:x.s,o:["✔️ wahr","✖️ falsch"],a:x.t?"✔️ wahr":"✖️ falsch"};};}
function qE(d){if(!d||!d.W)return null;const G=[],vs=(d.sel||[]).filter(x=>x[0]==="v").map(x=>+x.slice(1)),gs=(d.sel||[]).filter(x=>x[0]==="g");
  const words=vs.length?vs.flatMap(i=>d.W.slice(i*d.P,(i+1)*d.P)):d.W;
  G.push(()=>{const w=pick(words);return{k:"E",q:"Was bedeutet das?",s:w.en,o:shuf([w.de,...shuf(d.W.filter(x=>x.de!==w.de)).slice(0,3).map(x=>x.de)]),a:w.de};});
  G.push(()=>{const w=pick(words);return{k:"E",q:"Wie heißt das auf Englisch?",s:w.de,o:shuf([w.en,...shuf(d.W.filter(x=>x.en!==w.en)).slice(0,3).map(x=>x.en)]),a:w.en};});
  if(!gs.length||gs.some(g=>g==="g0"||g==="g1"))G.push(()=>{const v=pick(d.V),wr=[v.inf+(v.inf.endsWith("e")?"d":"ed"),v.pp!==v.past?v.pp:v.inf+"s",v.inf].filter(x=>x!==v.past);return{k:"E",q:"Simple Past von …",s:`${v.inf} (${v.de})`,o:shuf([v.past,...[...new Set(wr)].slice(0,3)]),a:v.past};});
  if(!gs.length||gs.includes("g3"))G.push(()=>{const x=pick(d.Q);return{k:"E",q:"Welches Wort passt?",s:x.s,o:shuf(x.o),a:x.a};});
  if(!gs.length||gs.includes("g4"))G.push(()=>{const x=pick(d.X);return{k:"E",q:x.q||"Welches Wort passt?",s:x.s,o:shuf(x.o),a:x.a};});
  if(gs.includes("g6"))G.push(()=>{const x=pick(d.R);return{k:"E",q:x.q,s:x.s,o:shuf(x.o),a:x.a};});
  return()=>pick(G)();}
function qD(d){if(!d||!d.I)return null;let I=d.I.filter(i=>!d.sel||!d.sel.length||d.sel.includes(i.p));if(!I.length)I=d.I;
  return()=>{const i=pick(I);
    if(i.t==="mc")return{k:"D",q:i.q||"Welche Antwort passt?",s:i.s,o:shuf(i.o),a:i.a};
    if(i.t==="tap"){const W=i.s.split(" ").map(w=>({w:w.replace(/\*/g,"").replace(/[.,!?;:“”]+$/,""),h:w.includes("*")}));const hit=pick(W.filter(x=>x.h)),oth=shuf(W.filter(x=>!x.h&&x.w.length>2)).slice(0,3).map(x=>x.w);
      return{k:"D",q:"Welches Wort ist ein gebeugtes Verb?",s:i.s.replace(/\*/g,""),o:shuf([hit.w,...[...new Set(oth)].filter(x=>x!==hit.w)]),a:hit.w};}
    const toks=i.s.split(" ").map(t=>{let c=0;if(/\(,\)$/.test(t)){c=2;t=t.replace(/\(,\)$/,"");}else if(/,$/.test(t)){c=1;t=t.slice(0,-1);}return{w:t,c};});
    const gaps=toks.map((x,j)=>j).filter(j=>j<toks.length-1&&toks[j].c!==2),yes=gaps.filter(j=>toks[j].c===1),no=gaps.filter(j=>toks[j].c===0);
    const g=(Math.random()<.5&&yes.length)||!no.length?pick(yes):pick(no);
    return{k:"D",q:"Gehört an die Stelle ▢ ein Komma?",s:toks.map((x,j)=>x.w+(j===g?" ▢":x.c===1?",":"")).join(" "),o:["✒️ Ja","➖ Nein"],a:toks[g].c===1?"✒️ Ja":"➖ Nein"};};}
async function makeQs(mode,n){
  const me=meP(),want=mode==="mix"?["W","Z","E","D"]:[mode],gens={};
  for(const k of want){try{if(k==="W"){const s=appState("W",me.uid);gens.W=qW(s&&s.sel);}else{const d=await loadApp(k);gens[k]=k==="Z"?qZ(d):k==="E"?qE(d):qD(d);}}catch(e){}}
  const ks=want.filter(k=>gens[k]);if(!ks.length)return[];
  const out=[];let last="";for(let i=0;i<n;i++){let k=pick(ks);if(ks.length>1&&k===last&&Math.random()<.6)k=pick(ks.filter(x=>x!==k));last=k;
    let q=null;for(let t=0;t<4&&!q;t++){try{q=gens[k]();}catch(e){q=null;}if(q&&(!q.o||q.o.length<2||!q.o.includes(q.a)))q=null;}if(q)out.push(q);}
  return out;}

/* ---------- Geister-Duelle (über die Lerngruppe synchronisiert) ---------- */
function ghostList(){const out=[];for(let i=0;i<localStorage.length;i++){const k=localStorage.key(i);if(k&&k.startsWith("lz-arena-g-")){const v=LSj(k,null);if(v)out.push(v);}}
  (window.lzMyGroups?lzMyGroups():[]).forEach(g=>{const c=window.lzGroupCache&&lzGroupCache(g.code);if(c)c.ghosts.forEach(x=>{if(!out.some(y=>y.id===x.id))out.push(x);});});
  return out.sort((a,b)=>b.ts-a.ts);}
function ghostSave(g){if(g.grp){window.lzGroupPut&&lzGroupPut(g.grp,"g:"+g.id,g);const c=lzGroupCache(g.grp);if(c){const i=c.ghosts.findIndex(x=>x.id===g.id);if(i>=0)c.ghosts[i]=g;else c.ghosts.push(g);}}else LSs("lz-arena-g-"+g.id,g);}
/* p.dev ist nur bei Online-Präsenz gesetzt (aus myPresence) – dort ist uid nur die geräteinterne Personen-Nummer
   (Standard "u1" auf jedem Gerät) und darf NIE zum Vergleich zwischen Geräten benutzt werden, sonst hält ein Gerät
   das jeweils andere für "sich selbst". Nur bei geräte-lokalen Geister-Duellen (kein dev, kein g.grp) ist uid gültig. */
function isMe(p,g){const m=meP();return !!p&&(p.gid===m.gid||(!p.dev&&!(g&&g.grp)&&p.uid===m.uid));}
function refreshGroups(){(window.lzMyGroups?lzMyGroups():[]).forEach(g=>{window.lzPullGroup&&lzPullGroup(g.code).then(()=>{drawCard();drawPick();});});}
setInterval(refreshGroups,30000);setTimeout(refreshGroups,2500);
function ghostClean(){const L=ghostList().filter(g=>!g.grp),old=Date.now()-14*864e5;L.forEach((g,i)=>{if(i>=30||g.ts<old){try{localStorage.removeItem("lz-arena-g-"+g.id);}catch(e){}}});}

/* ---------- Oberfläche ---------- */
const OV=document.createElement("div");OV.id="arenaOv";OV.setAttribute("role","dialog");OV.setAttribute("aria-label","Arena");document.body.appendChild(OV);
const INV=document.createElement("div");INV.id="arenaInv";document.body.appendChild(INV);
let VIEW=null,GAME=null,PENDING=null;
function close(){if(GAME&&!GAME.over&&!confirm("Duell wirklich abbrechen?"))return;if(GAME){GAME.over=true;clearInterval(GAME.iv);if(GAME.live)send({t:"quit",id:GAME.id,to:GAME.opp.dev});}GAME=null;VIEW=null;PENDING=null;OV.classList.remove("on");drawCard();try{render();}catch(e){}}
function openOv(){OV.classList.add("on");}
let PICK={mode:"mix",stake:10};
function offList(){const me=meP(),onG=new Set(),m={};
  NU.list.forEach(u=>{const g=u.gid||u.id;if(g!==me.gid&&!onG.has(g))m[g]={gid:g,uid:u.id,acc:!!u.acc,name:u.name,e:u.e,grp:"",gl:"dieses Gerät"};});
  (window.lzMyGroups?lzMyGroups():[]).forEach(G=>{const c=window.lzGroupCache&&lzGroupCache(G.code);if(c)c.members.forEach(x=>{if(x.gid!==me.gid&&!onG.has(x.gid)&&!m[x.gid])m[x.gid]={gid:x.gid,uid:"",acc:true,name:x.name,e:x.e,grp:G.code,gl:G.name};});});
  return Object.values(m);}
function drawPick(){if(VIEW!=="pick")return;const me=meP(),on=ONLINE.filter(p=>!isMe(p));
  const off=offList();const fam=spaces().length;
  OV.innerHTML=`<div class="ar-box"><div class="ar-top"><b>⚔️ Arena</b><button type="button" class="ar-x" data-ax>✕</button></div>
   <div class="ar-me">${esc(me.e)} <b>${esc(me.name)}</b> · ${ptsGet(me.uid).p} Arena-Punkte</div>
   <div class="ar-h">🎰 Welche Fächer?</div><div class="ar-seg">${[["mix","🎰 Glücksrad (alle)"],["W","📐 Mathe"],["Z","🪄 NWT"],["E","🐚 Englisch"],["D","🕵️ Deutsch"]].map(([k,l])=>`<button type="button" data-am="${k}" class="${PICK.mode===k?"on":""}">${l}</button>`).join("")}</div>
   <div class="ar-h">💰 Einsatz (Arena-Punkte)</div><div class="ar-seg">${[0,10,25,50].map(s=>`<button type="button" data-as="${s}" class="${PICK.stake===s?"on":""}">${s||"ohne"}</button>`).join("")}</div>
   <div class="ar-h">🟢 Live-Duell – gerade online, ihr spielt gleichzeitig</div>
   ${fam?(on.length?`<div class="ar-list">${on.map(p=>`<button type="button" class="ar-p" data-live="${esc(p.dev)}"><span>${esc(p.e)}</span><b>${esc(p.name)}</b><small>${p.spl?"👥 "+esc(p.spl)+" · ":""}${p.app&&AN[p.app]?"in "+AN[p.app][0]+" "+AN[p.app][1]:"auf der Startseite"}</small><em>🪢 live</em></button>`).join("")}</div>`:`<p class="ar-p0">Gerade ist niemand online.</p>`):`<p class="ar-p0">Für Live-Duelle: gemeinsam einer Lerngruppe beitreten, z. B. „Familie“.</p>`}
   ${fam?`<p class="ar-p0 ar-diag">${diagText()}</p>`:""}
   ${off.length?`<div class="ar-h">👻 Geister-Duell – alle aus deinen Lerngruppen</div><p class="ar-p0">Du spielst jetzt, die andere Person später gegen deine Aufzeichnung.</p><div class="ar-list">${off.map(u=>`<button type="button" class="ar-p" data-ghost="${esc(u.gid)}"><span>${esc(u.e)}</span><b>${esc(u.name)}</b><small>${u.grp?"👥 "+esc(u.gl):"📱 "+esc(u.gl)}</small><em>👻</em></button>`).join("")}</div>`:""}
   ${myGhostBoxes()}</div>`;}
function myGhostBoxes(){const L=ghostList();
  const inc=L.filter(g=>isMe(g.to,g)&&!g.res),res=L.filter(g=>isMe(g.from,g)&&g.res&&!g.res.fromSeen);
  return (inc.length?`<div class="ar-h">📨 Herausforderungen an dich</div>${inc.map(g=>`<div class="ar-g">👻 <b>${esc(g.from.e)} ${esc(g.from.name)}</b> fordert dich heraus${g.grpName?" (👥 "+esc(g.grpName)+")":""} · ${g.mode==="mix"?"🎰 Glücksrad":AN[g.mode][0]+" "+AN[g.mode][1]} · Einsatz ${g.stake}<button type="button" data-gplay="${g.id}">▶ Annehmen</button></div>`).join("")}`:"")
   +(res.length?`<div class="ar-h">📬 Ergebnisse</div>${res.map(g=>`<div class="ar-g">👻 gegen <b>${esc(g.to.e)} ${esc(g.to.name)}</b>: ${g.res.win==="from"?"🏆 Du hast gewonnen!":g.res.win==="to"?"Leider verloren.":"Unentschieden."} <button type="button" data-gseen="${g.id}">OK</button></div>`).join("")}`:"");}
window.lzArenaOpen=function(){if(GAME&&!GAME.over){openOv();return;}VIEW="pick";openOv();drawPick();};
function toast(t){const d=document.createElement("div");d.className="ar-toast";d.textContent=t;document.body.appendChild(d);setTimeout(()=>d.remove(),3200);}

/* Start: live */
async function challengeLive(dev){
  const p=ONLINE.find(x=>x.dev===dev);if(!p)return;VIEW="wait";
  OV.innerHTML=`<div class="ar-box c"><div class="ar-big">🎰</div><p>Fragen werden gemischt …</p></div>`;
  const qs=await makeQs(PICK.mode,40);if(!qs.length){OV.innerHTML=`<div class="ar-box c"><p>Keine Fragen gefunden. Wähle in den Apps Pakete aus.</p><button type="button" class="ar-btn" data-ax>Schließen</button></div>`;return;}
  const id="L"+Date.now().toString(36)+Math.random().toString(36).slice(2,6),me=meP();
  PENDING={id,opp:Object.assign({},p,{grp:p.sp&&p.sp.startsWith("grp:")?p.sp.slice(4):""}),qs,mode:PICK.mode,stake:PICK.stake};
  send({t:"inv",id,to:dev,from:{dev:DEV,uid:me.uid,name:me.name,e:me.e},qs,mode:PICK.mode,stake:PICK.stake});
  OV.innerHTML=`<div class="ar-box c"><div class="ar-big">⏳</div><p>Warte auf <b>${esc(p.e)} ${esc(p.name)}</b> …</p><p class="ar-p0" id="arCd">noch 25 s</p><button type="button" class="ar-btn sec" data-ax>Abbrechen</button></div>`;
  let n=25;PENDING.iv=setInterval(()=>{n--;const el=document.getElementById("arCd");if(el)el.textContent="noch "+n+" s";if(n<=0){clearInterval(PENDING.iv);noAnswer("hat nicht geantwortet");}},1000);}
function noAnswer(why){if(!PENDING)return;const P=PENDING;
  OV.innerHTML=`<div class="ar-box c"><div class="ar-big">🙈</div><p><b>${esc(P.opp.e)} ${esc(P.opp.name)}</b> ${why}.</p><p class="ar-p0">Du kannst jetzt als Geister-Duell spielen. Die andere Person tritt später gegen deine Aufzeichnung an.</p><button type="button" class="ar-btn" data-g2="1">👻 Als Geister-Duell spielen</button><button type="button" class="ar-btn sec" data-ax>Schließen</button></div>`;}
HANDLERS.push(m=>{
  if(m.t==="inv"){if(GAME&&!GAME.over){send({t:"dec",id:m.id,to:m.from.dev,busy:1});return;}
    INV.innerHTML=`<div class="ar-inv"><div class="ar-big">⚔️</div><p><b>${esc(m.from.e)} ${esc(m.from.name)}</b> fordert dich zum Tauziehen heraus!</p><p class="ar-p0">${m.mode==="mix"?"🎰 Glücksrad – alle Fächer":AN[m.mode][0]+" "+AN[m.mode][1]} · Einsatz: ${m.stake||"ohne"}</p><div class="ar-row"><button type="button" class="ar-btn" data-acc="1">✅ Annehmen</button><button type="button" class="ar-btn sec" data-dec="1">Später</button></div></div>`;
    INV.classList.add("on");INV._m=m;clearTimeout(INV._t);INV._t=setTimeout(()=>{INV.classList.remove("on");},25000);
    try{navigator.vibrate&&navigator.vibrate(200);}catch(e){}}
  else if(m.t==="acc"&&PENDING&&m.id===PENDING.id){clearInterval(PENDING.iv);const P=PENDING;PENDING=null;startGame({id:P.id,live:true,opp:P.opp,qs:P.qs,mode:P.mode,stake:P.stake,host:true});}
  else if(m.t==="dec"&&PENDING&&m.id===PENDING.id){clearInterval(PENDING.iv);noAnswer(m.busy?"ist gerade in einem anderen Duell":"möchte gerade nicht");}
  else if(GAME&&m.id===GAME.id){
    if(m.t==="tot"){GAME.oppTot=m.v;GAME.oppOk=m.c||0;GAME.oppStreak=m.s||0;drawRope();checkEnd();}
    else if(m.t==="frz"){GAME.frozenUntil=Date.now()+3000;drawQ(true);}
    else if(m.t==="end"){finish(m.b,m.a,true);}
    else if(m.t==="quit"&&!GAME.over){finish(GAME.myTot,GAME.oppTot,true,"hat aufgegeben");}}
});
INV.addEventListener("click",e=>{const m=INV._m;if(!m)return;
  if(e.target.closest("[data-acc]")){INV.classList.remove("on");send({t:"acc",id:m.id,to:m.from.dev});openOv();startGame({id:m.id,live:true,opp:m.from,qs:m.qs,mode:m.mode,stake:m.stake});}
  else if(e.target.closest("[data-dec]")){INV.classList.remove("on");send({t:"dec",id:m.id,to:m.from.dev});}});

/* ---------- Spiel ---------- */
function startGame(o){
  const me=meP();GAME=Object.assign({me,myTot:0,oppTot:0,ok:0,oppOk:0,streak:0,pu:null,dbl:0,shield:false,frozenUntil:0,qi:0,tl:[[0,0]],fz:[],over:false,lock:false},o);VIEW="game";openOv();
  let n=3;OV.innerHTML=`<div class="ar-box c"><div class="ar-vs"><span>${esc(me.e)}<b>${esc(me.name)}</b></span><i>VS</i><span>${esc(GAME.opp.e)}<b>${esc(GAME.opp.name)}</b></span></div>${GAME.ghost?`<p class="ar-p0">👻 Du spielst gegen die Aufzeichnung von ${esc(GAME.opp.name)}.</p>`:GAME.recording?`<p class="ar-p0">👻 Deine Runde wird für ${esc(GAME.opp.name)} aufgezeichnet.</p>`:""}<div class="ar-big" id="arN">3</div><p class="ar-p0">Zieh das Seil ${WIN} Felder zu dir! Falsche Antworten lassen es zurückrutschen.</p></div>`;
  const iv=setInterval(()=>{n--;const el=document.getElementById("arN");if(n>0){if(el)el.textContent=n;return;}clearInterval(iv);GAME.start=Date.now();GAME.ghostClock=0;GAME.lastT=GAME.start;
    GAME.iv=setInterval(tick,100);drawGame();},1000);}
function ghostTot(){const g=GAME.ghost;let v=0;for(const [t,x] of g.tl){if(t<=GAME.ghostClock)v=x;else break;}return v;}
function tick(){if(!GAME||GAME.over)return;const now=Date.now(),dt=now-GAME.lastT;GAME.lastT=now;
  if(GAME.ghost){if(now>=GAME.ghostFrozenUntil)GAME.ghostClock+=dt;const v=ghostTot();if(v!==GAME.oppTot){GAME.oppTot=v;drawRope();}
    const t=now-GAME.start;
    GAME.ghost.fz.forEach((f,i)=>{if(!GAME.fzUsed)GAME.fzUsed={};if(!GAME.fzUsed[i]&&t>=f){GAME.fzUsed[i]=1;GAME.frozenUntil=now+3000;drawQ(true);}});}
  const left=Math.max(0,DUR-(now-GAME.start)),tt=document.getElementById("arT");if(tt)tt.textContent=Math.ceil(left/1000)+" s";
  const fr=document.getElementById("arFrz");if(fr)fr.classList.toggle("on",now<GAME.frozenUntil);
  if(GAME.frozenUntil&&now>=GAME.frozenUntil&&GAME.wasFrozen){GAME.wasFrozen=false;if(!GAME.lock){const el=document.getElementById("arQ");if(el)el.querySelectorAll("[data-o]").forEach(b=>b.disabled=false);}}
  checkEnd();if(left<=0&&!GAME.over)finish(GAME.myTot,GAME.oppTot);}
function checkEnd(){if(!GAME||GAME.over)return;const d=GAME.myTot-GAME.oppTot;if(Math.abs(d)>=WIN){if(GAME.live)send({t:"end",id:GAME.id,to:GAME.opp.dev,a:GAME.myTot,b:GAME.oppTot});finish(GAME.myTot,GAME.oppTot);}}
function drawGame(){
  OV.innerHTML=`<div class="ar-box game"><div class="ar-top"><span class="ar-tm">⏱️ <b id="arT">120 s</b></span><span class="ar-mode">${GAME.mode==="mix"?"🎰 Glücksrad":AN[GAME.mode][0]+" "+AN[GAME.mode][1]}</span><button type="button" class="ar-x" data-ax>✕</button></div>
   <div class="ar-rope"><div class="ar-side me">${esc(GAME.me.e)}<b>${esc(GAME.me.name)}</b></div><div class="ar-track" id="arTrack">${Array.from({length:WIN*2+1},(_,i)=>`<i class="${i===WIN?"mid":""}"></i>`).join("")}<span class="ar-knot" id="arKnot">🪢</span></div><div class="ar-side opp">${esc(GAME.opp.e)}<b>${esc(GAME.opp.name)}</b>${GAME.ghost?"<small>👻</small>":""}</div></div>
   <div class="ar-pu" id="arPu"></div><div class="ar-q" id="arQ"></div><div class="ar-frz" id="arFrz">❄️ Eingefroren!</div></div>`;
  drawRope();drawPu();drawQ();}
function drawRope(){const k=document.getElementById("arKnot");if(!k)return;const d=Math.max(-WIN,Math.min(WIN,GAME.myTot-GAME.oppTot));k.style.left=(50-d*(50/WIN)*.92)+"%";k.classList.toggle("win",d>0);k.classList.toggle("lose",d<0);}
function drawPu(){const el=document.getElementById("arPu");if(!el)return;const P={frz:["❄️","Einfrieren"],dbl:["✖️2","Doppelzug"],shd:["🛡️","Schild"]};
  el.innerHTML=(GAME.pu?`<button type="button" class="ar-pub" data-pu="1">${P[GAME.pu][0]} ${P[GAME.pu][1]} einsetzen</button>`:`<span class="ar-st">🔥 Serie: ${GAME.streak}${GAME.streak%3||!GAME.streak?` · Power-up in ${3-GAME.streak%3}`:""}</span>`)
   +(GAME.dbl?`<span class="ar-st on">✖️2 aktiv (${GAME.dbl})</span>`:"")+(GAME.shield?`<span class="ar-st on">🛡️ aktiv</span>`:"");}
function drawQ(frozenOnly){const el=document.getElementById("arQ");if(!el||!GAME)return;const now=Date.now(),fz=now<GAME.frozenUntil;
  if(fz){GAME.wasFrozen=true;el.querySelectorAll("button").forEach(b=>b.disabled=true);if(frozenOnly)return;}
  if(frozenOnly&&!fz)return;
  const q=GAME.qs[GAME.qi%GAME.qs.length];GAME.lock=false;
  const show=()=>{el.innerHTML=`<div class="ar-badge">${AN[q.k][0]} ${AN[q.k][1]}</div><div class="ar-ql">${esc(q.q)}</div><div class="ar-qs">${esc(q.s)}</div><div class="ar-opts">${q.o.map((o,i)=>`<button type="button" data-o="${i}">${esc(o)}</button>`).join("")}</div>`;
    if(Date.now()<GAME.frozenUntil)el.querySelectorAll("button").forEach(b=>b.disabled=true);};
  if(GAME.mode==="mix"&&!GAME.noSpin){let c=0;const ks=["W","Z","E","D"];el.innerHTML=`<div class="ar-wheel" id="arWh">🎰</div>`;const iv=setInterval(()=>{const w=document.getElementById("arWh");if(!w){clearInterval(iv);return;}w.textContent=AN[ks[c++%4]][0];if(c>5){clearInterval(iv);show();}},70);}
  else show();}
function answer(i){if(!GAME||GAME.over||GAME.lock||Date.now()<GAME.frozenUntil)return;GAME.lock=true;
  const q=GAME.qs[GAME.qi%GAME.qs.length],ok=q.o[i]===q.a,el=document.getElementById("arQ");
  el.querySelectorAll("button").forEach(b=>{b.disabled=true;if(q.o[+b.dataset.o]===q.a)b.classList.add("ok");});if(!ok)el.querySelector(`[data-o="${i}"]`).classList.add("bad");
  if(ok){GAME.ok++;const add=GAME.dbl>0?2:1;if(GAME.dbl>0)GAME.dbl--;GAME.myTot+=add;GAME.streak++;if(GAME.streak%3===0&&!GAME.pu)GAME.pu=pick(["frz","dbl","shd"]);}
  else{if(GAME.shield)GAME.shield=false;else GAME.myTot-=1;GAME.streak=0;}
  GAME.tl.push([Date.now()-GAME.start,GAME.myTot]);
  if(GAME.live)send({t:"tot",id:GAME.id,to:GAME.opp.dev,v:GAME.myTot,s:GAME.streak,c:GAME.ok});
  drawRope();drawPu();checkEnd();
  if(!GAME.over)setTimeout(()=>{if(!GAME||GAME.over)return;GAME.qi++;drawQ();},ok?450:1200);}
function usePu(){if(!GAME||!GAME.pu)return;const p=GAME.pu;GAME.pu=null;
  if(p==="dbl")GAME.dbl=2;else if(p==="shd")GAME.shield=true;
  else{if(GAME.live)send({t:"frz",id:GAME.id,to:GAME.opp.dev});if(GAME.recording)GAME.fz.push(Date.now()-GAME.start);if(GAME.ghost)GAME.ghostFrozenUntil=Date.now()+3000;toast("❄️ "+GAME.opp.name+" ist 3 Sekunden eingefroren!");}
  drawPu();}
function finish(a,b,remote,why){if(!GAME||GAME.over)return;GAME.over=true;clearInterval(GAME.iv);
  const d=a-b,res=d>0?"w":d<0?"l":"d",me=GAME.me,stake=GAME.stake||0;
  let txt="";
  if(GAME.recording){const grp=GAME.opp.grp||"",gg=grp&&lzMyGroups().find(x=>x.code===grp)||{},gn=gg.name;if(gg.alias)me.name=gg.alias;const g={id:GAME.id,ts:Date.now(),grp,grpName:gn||"",from:{uid:me.uid,gid:me.gid,acc:!!me.acc,name:me.name,e:me.e},to:{uid:GAME.opp.uid,gid:GAME.opp.gid,acc:!!GAME.opp.acc,name:GAME.opp.name,e:GAME.opp.e},mode:GAME.mode,stake,qs:GAME.qs,rec:{tl:GAME.tl,fz:GAME.fz,fin:GAME.myTot,ok:GAME.ok},res:null};ghostSave(g);ghostClean();
    txt=`<div class="ar-big">👻</div><h3>Aufgezeichnet!</h3><p>Du hast <b>${GAME.ok}</b> Fragen richtig beantwortet. ${esc(GAME.opp.name)} bekommt deine Herausforderung und spielt später gegen deinen Geist.</p>`;}
  else{const P=ptsAdd(me.uid,res,stake);
    if(GAME.ghostRec){const g=GAME.ghostRec;g.res={win:res==="w"?"to":res==="l"?"from":"draw",a:g.rec.fin,b:a,okA:g.rec.ok||0,okB:GAME.ok,ts:Date.now(),fromSeen:false};ghostSave(g);}
    txt=`<div class="ar-big">${res==="w"?"🏆":res==="l"?"💪":"🤝"}</div><h3>${res==="w"?"Gewonnen!":res==="l"?"Verloren – beim nächsten Mal!":"Unentschieden!"}</h3>${why?`<p>${esc(GAME.opp.name)} ${why}.</p>`:""}<p>${d>0?"Das Seil ist bei dir! ":d<0?"Das Seil ist bei "+esc(GAME.opp.name)+". ":""}Richtige Antworten: <b>${esc(me.name)} ${GAME.ok}</b> · <b>${esc(GAME.opp.name)} ${GAME.ghost?(GAME.ghostRec.rec.ok||"–"):GAME.oppOk}</b></p><p class="ar-p0">${res==="w"?"+"+(10+stake):res==="l"?"−"+stake:"±0"} Arena-Punkte · jetzt ${P.p}</p>`;
    if(res==="w")try{confettiA();}catch(e){}}
  OV.innerHTML=`<div class="ar-box c">${txt}<div class="ar-row"><button type="button" class="ar-btn" data-again="1">⚔️ Neues Duell</button><button type="button" class="ar-btn sec" data-ax>Schließen</button></div></div>`;
  GAME.done=true;try{render();}catch(e){}}
function confettiA(){const c=document.createElement("div");c.className="ar-conf";for(let i=0;i<30;i++){const d=document.createElement("i");d.style.left=Math.random()*100+"%";d.style.background=`hsl(${Math.random()*360},80%,60%)`;d.style.animationDelay=Math.random()*.5+"s";c.appendChild(d);}document.body.appendChild(c);setTimeout(()=>c.remove(),2500);}

async function ghostRecord(gid){const u=offList().find(x=>x.gid===gid)||(PENDING&&PENDING.opp.gid===gid?Object.assign({grp:PENDING.opp.grp||""},PENDING.opp):null);if(!u)return;
  OV.innerHTML=`<div class="ar-box c"><div class="ar-big">🎰</div><p>Fragen werden gemischt …</p></div>`;
  const qs=PENDING&&PENDING.opp.gid===gid?PENDING.qs:await makeQs(PICK.mode,40);PENDING=null;
  if(!qs.length){OV.innerHTML=`<div class="ar-box c"><p>Keine Fragen gefunden.</p><button type="button" class="ar-btn" data-ax>Schließen</button></div>`;return;}
  startGame({id:"G"+Date.now().toString(36)+Math.random().toString(36).slice(2,6),recording:true,opp:{uid:u.uid,gid:u.gid,acc:!!u.acc,name:u.name,e:u.e,dev:"",grp:u.grp||""},qs,mode:PICK.mode,stake:PICK.stake});}
function ghostPlay(id){const g=ghostList().find(x=>x.id===id);if(!g||g.res)return;
  startGame({id:g.id,ghost:{tl:g.rec.tl,fz:g.rec.fz||[]},ghostRec:g,ghostFrozenUntil:0,opp:Object.assign({dev:""},g.from),qs:g.qs,mode:g.mode,stake:g.stake});}
function ghostSeen(id){const g=ghostList().find(x=>x.id===id);if(!g||!g.res||g.res.fromSeen)return;
  const res=g.res.win==="from"?"w":g.res.win==="to"?"l":"d";ptsAdd(g.from.uid,res,g.stake||0);g.res.fromSeen=true;ghostSave(g);
  toast(res==="w"?"🏆 +"+(10+(g.stake||0))+" Arena-Punkte":res==="l"?"−"+(g.stake||0)+" Arena-Punkte":"Unentschieden");drawPick();drawCard();}

OV.addEventListener("click",e=>{const t=e.target;
  if(t.closest("[data-ax]")){close();return;}
  const m=t.closest("[data-am]");if(m){PICK.mode=m.dataset.am;drawPick();return;}
  const s=t.closest("[data-as]");if(s){PICK.stake=+s.dataset.as;drawPick();return;}
  const l=t.closest("[data-live]");if(l){challengeLive(l.dataset.live);return;}
  const g=t.closest("[data-ghost]");if(g){ghostRecord(g.dataset.ghost);return;}
  if(t.closest("[data-g2]")){ghostRecord(PENDING.opp.gid||PENDING.opp.uid);return;}
  const gp=t.closest("[data-gplay]");if(gp){ghostPlay(gp.dataset.gplay);return;}
  const gs=t.closest("[data-gseen]");if(gs){ghostSeen(gs.dataset.gseen);return;}
  if(t.closest("[data-again]")){GAME=null;VIEW="pick";drawPick();return;}
  if(t.closest("[data-pu]")){usePu();return;}
  const o=t.closest("[data-o]");if(o&&GAME){answer(+o.dataset.o);return;}});

/* ---------- Karte auf der Startseite ---------- */
function drawCard(){const el=document.getElementById("arena");if(!el)return;const on=ONLINE.filter(p=>!isMe(p)),L=ghostList();
  const inc=L.filter(g=>isMe(g.to,g)&&!g.res).length,res=L.filter(g=>isMe(g.from,g)&&g.res&&!g.res.fromSeen).length;const gs=window.lzMyGroups?lzMyGroups():[];
  el.innerHTML=`<section class="ar-card"><div><b>⚔️ Arena</b><small>${gs.length?`👥 ${gs.map(g=>esc(g.name)).join(", ")} · `:""}${spaces().length?(on.length?`🟢 online: ${on.map(p=>esc(p.e)+" "+esc(p.name)).join(", ")}`:"Gerade ist niemand sonst online."):"Tauziehen gegen andere – live oder als Geister-Duell."}${inc?` · 📨 ${inc} Herausforderung${inc>1?"en":""}`:""}${res?` · 📬 ${res} Ergebnis${res>1?"se":""}`:""}${DIAG.err?` · ⚠️ Arena-Server: ${esc(DIAG.err)}`:""}</small></div><span class="ar-cb"><button type="button" class="ar-go sec" onclick="lzGroupsOpen()">👥 Lerngruppen</button><button type="button" class="ar-go" onclick="lzArenaOpen()">⚔️ Herausfordern</button></span></section>`;}
window.lzArenaCard=drawCard;
if(window.__arenaMock)window.__arenaGame=()=>GAME;
setInterval(drawCard,10000);setTimeout(drawCard,300);
})();
