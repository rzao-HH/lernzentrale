/* ===== Lernstand & Punkte nach verteilter Wiederholung (Spaced Repetition) =====
   Jedes Lernpaket hat eine Stufe 0–5. Punkte lenken dorthin, wo Lernen am meisten bringt:
   neu/wackelig = volle Punkte · sitzt (Intervall läuft noch) = wenig · wieder fällig = voll · lange überfällig = Bonus.
   Gespeichert im App-Stand der Person (Feld `ls`, Küsten-Crew `_ls`) → wandert mit dem normalen Abgleich (app:W|Z|E|D) mit.
   Pro Paket: { s: Stufe, t: Zeitpunkt der letzten wertenden Runde, d: Tag der heutigen Runden, r: Runden an diesem Tag }.
   Bereits gesammelte Punkte werden nie verändert – die Logik gilt nur für neue Punkte. */
window.LS_CONF={
  INTERVALL_TAGE:[0,1,2,4,8,16],   /* Wiederholungsintervall je Stufe 0–5 (Tage) */
  FAKTOR_KANN_SCHON:0.15,          /* Anteil der Punkte, solange ein Paket sitzt (Stufe 2+, Intervall läuft) */
  FAKTOR_TAGESDECKEL:0.15,         /* Anteil der Punkte ab der TAGESDECKEL_AB_RUNDE-ten Runde am selben Tag */
  MIN_PUNKTE:1,                    /* nie 0 Punkte */
  UEBERFAELLIG_AB:2,               /* ab doppeltem Intervall gilt ein Paket als deutlich überfällig … */
  BONUS_UEBERFAELLIG:0.2,          /* … und bringt +20 % */
  TAGESDECKEL_AB_RUNDE:3,          /* ab der 3. Runde desselben Pakets am selben Tag nur noch Minimalpunkte */
  RUNDE_MIN_ANTWORTEN:4,           /* so viele Antworten zu einem Paket braucht eine Runde, damit sie zählt */
  RUNDE_MAX_ANTWORTEN:25,          /* danach wird die Runde automatisch gewertet (z. B. sehr lange Zeitrunden) */
  STUFE_HOCH_AB:0.8,               /* ab 80 % richtig: Stufe +1 … */
  HOCH_NUR_WENN_FAELLIG:true,      /* … aber nur, wenn das Paket fällig war (sonst könnte man an einem Tag auf Stufe 5) */
  STUFE_RUNTER_UNTER:0.5,          /* unter 50 % richtig: Stufe −1 */
  /* Einmaliger Startwert aus dem bisherigen Fortschritt (gilt als ab dem Übernahmetag geübt) */
  START_STUFE_GUT:3,               /* Lernziel erreicht, ≥ 80 % Treffer oder Testnote 1–2 */
  START_STUFE_MITTEL:2,            /* ≥ 60 % Treffer oder Testnote 3 */
  START_MIN_ANTWORTEN:10           /* so viele Antworten braucht eine Trefferquote, damit sie zählt */
};
(function(){
const C=()=>window.LS_CONF,DAY=864e5;
const dkey=t=>{const d=new Date(t);return d.getFullYear()+"-"+(d.getMonth()+1)+"-"+d.getDate();};
const mid=t=>{const d=new Date(t);d.setHours(0,0,0,0);return d.getTime();};
const days=(a,b)=>Math.round((mid(b)-mid(a))/DAY);
const esc=s=>String(s==null?"":s).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const RANK={bonus:0,faellig:1,ueben:2,neu:3,sitzt:4,genug:5};

/* Zustand eines Pakets (rein rechnerisch, auch für die Startseite) */
function status(rec,now){
  now=now||Date.now();const K=C(),I=K.INTERVALL_TAGE;
  if(!rec||rec.t==null)return{kind:"neu",s:0,f:1,charge:0,left:0,el:0,played:false};
  const s=Math.max(0,Math.min(I.length-1,rec.s|0)),iv=I[s],el=days(rec.t,now);
  const today=rec.d===dkey(now)?(rec.r|0):0;
  const charge=s===0?0:Math.round(100*(s/(I.length-1))*Math.max(0,Math.min(1,1-el/Math.max(1,iv))));
  let kind,f;
  /* Ein sitzendes Paket bleibt „sitzt“ (wenig Punkte bis zur Fälligkeit), auch wenn es heute schon oft geübt wurde.
     Der Tagesdeckel („heute genug geübt“) betrifft nur Pakete, die noch gelernt werden oder fällig sind. */
  if(s>=2&&el<iv){kind="sitzt";f=K.FAKTOR_KANN_SCHON;}
  else if(today>=K.TAGESDECKEL_AB_RUNDE-1){kind="genug";f=K.FAKTOR_TAGESDECKEL;}
  else if(s<=1&&!(s>=1&&el>=K.UEBERFAELLIG_AB*iv)){kind="ueben";f=1;}
  else if(s>=2&&el<iv){kind="sitzt";f=K.FAKTOR_KANN_SCHON;}
  else if(s>=1&&el>=K.UEBERFAELLIG_AB*iv){kind="bonus";f=1+K.BONUS_UEBERFAELLIG;}
  else{kind="faellig";f=1;}
  const fresh=s===0?0:Math.max(0,Math.min(1,1-el/Math.max(1,iv)));
  return{kind,s,f,charge,fresh,left:Math.max(0,iv-el),el,today,played:true,due:s===0||el>=iv};
}
function points(base,factor){if(!(base>0))return base||0;return Math.max(C().MIN_PUNKTE,Math.round(base*factor));}

/* Eine gewertete Runde eines Pakets eintragen: ok von n richtig */
function applyRound(rec,ok,n,now){
  now=now||Date.now();const K=C(),I=K.INTERVALL_TAGE,st=status(rec,now),r=Object.assign({s:0,t:null,d:"",r:0},rec||{});
  const acc=n?ok/n:0,due=!st.played||st.due;let s=r.s|0,moved=false;
  if(acc>=K.STUFE_HOCH_AB&&(due||!K.HOCH_NUR_WENN_FAELLIG)){if(s<I.length-1){s++;}moved=true;}
  else if(acc<K.STUFE_RUNTER_UNTER){if(s>0)s--;moved=true;}
  /* Intervall startet neu, wenn die Stufe wechselt, das Paket fällig war oder noch wackelig ist –
     wer ein sitzendes Paket zwischendurch wiederholt, verschiebt den nächsten Fälligkeitstag nicht */
  if(moved||due||s<=1||r.t==null)r.t=now;
  r.s=s;const dk=dkey(now);if(r.d!==dk){r.d=dk;r.r=0;}r.r++;
  return r;
}

/* Was die Kachel sagt – eine Zeile, ohne Punktzahl (jede Übung bringt unterschiedlich viel: Karten 2, Quiz 5, Test nach Note …) */
const TXT={
  neu:()=>`💰 Volle Punkte – neu`,
  ueben:()=>`💰 Volle Punkte – noch üben`,
  faellig:()=>`💰 Volle Punkte – wieder fällig`,
  bonus:()=>`🎁 Bonus +${Math.round(C().BONUS_UEBERFAELLIG*100)} % – lange nicht geübt`,
  sitzt:s=>`🪙 Wenig Punkte – kannst du schon! Wieder voll ${s.left<=1?"morgen":"in "+s.left+" Tagen"}`,
  genug:()=>`🪙 Wenig Punkte – heute genug geübt. Morgen wieder voll`
};

/* ---------- Anbindung an eine App ----------
   LS.init({app:"W", units:[{id,icon,name}], base:10, get:()=>obj, save:()=>{}, pick:id=>{}, meter:{icon,name,full,empty}, cur:()=>[ids]}) */
const LS={conf:C,status,points,applyRound,dkey,RANK,TXT};
let A=null,buf={},pend={},hinted=false;
function store(){const o=A.get();if(!o)return{};return o;}
function rec(id){return store()[id];}
function st(id){return status(rec(id));}
/* Gewertete Runden werden erst eingetragen, wenn die nächste Runde beginnt oder die Übersicht gezeigt wird –
   so zählen die Punkte am Rundenende (Zeitrunde, Test) noch mit dem Lernstand, mit dem die Runde begonnen hat. */
function flush(){const ids=Object.keys(pend);if(!ids.length||!A)return;const o=store(),K=C();let ch=false;
  ids.forEach(id=>{const b=pend[id];if(b&&b.n>=K.RUNDE_MIN_ANTWORTEN){o[id]=applyRound(o[id],b.ok,b.n);ch=true;}});pend={};if(ch){try{A.save();}catch(e){}}}
function known(id){return A&&A.units.some(u=>u.id===id);}
function unit(id){return A.units.find(u=>u.id===id);}
LS.init=function(cfg){A=cfg;buf={};pend={};hinted=false;css();
  /* Paketnamen für die Startseite merken (nur auf diesem Gerät) */
  try{localStorage.setItem("ls-units-"+cfg.app,JSON.stringify(cfg.units.map(u=>({id:u.id,icon:u.icon,name:u.name}))));}catch(e){}
  seed();LS.checkPick();
  addEventListener("pagehide",()=>{LS.endRound();flush();});
  document.addEventListener("visibilitychange",()=>{if(document.hidden){LS.endRound();flush();}});
};
/* Einmalig: Stufe aus dem bisherigen Fortschritt übernehmen, damit Bekanntes nicht als „neu“ gilt.
   A.seed(id) → {n: Antworten, hit: Treffer, done: Lernziel erreicht, g: beste Testnote der App}; dazu Testnoten aus lz-ergebnisse.
   Pakete ohne bisherigen Fortschritt bleiben „neu“. Merker _start im Speicher, damit es nur einmal passiert. */
function startStage(x,g){const K=C(),q=x&&x.n>=K.START_MIN_ANTWORTEN?x.hit/x.n:-1;
  if((x&&x.done)||q>=0.8||(g&&g<=2))return K.START_STUFE_GUT;
  if(q>=0.6||g===3)return K.START_STUFE_MITTEL;
  if((x&&x.n>0)||g)return 1;return 0;}
function seed(){if(!A||!A.seed)return;const o=store();if(o._start)return;const now=Date.now();let R=[];
  try{const u=(window.__NUTZER&&window.__NUTZER.cur)||"u1";R=JSON.parse(localStorage.getItem("lz-ergebnisse")||"[]").filter(r=>r&&r.a===A.app&&(r.u||"u1")===u&&+r.g);}catch(e){}
  const norm=A.norm||(a=>a);
  A.units.forEach(un=>{const id=un.id;if(o[id])return;let x=null;try{x=A.seed(id);}catch(e){}
    const gs=R.filter(r=>norm(r.units||[]).includes(id)).map(r=>+r.g);if(x&&x.g)gs.push(+x.g);
    const s=startStage(x,gs.length?Math.min(...gs):0);if(s>0)o[id]={s,t:now,d:"",r:0};});
  o._start=now;try{A.save();}catch(e){}}
LS.startStage=startStage;
/* Sprung von der Startseite („Heute lohnt sich besonders“): Paket auswählen */
LS.checkPick=function(){if(!A)return;try{const k="ls-pick-"+A.app,p=sessionStorage.getItem(k);if(p){sessionStorage.removeItem(k);setTimeout(()=>{try{A.pick&&A.pick(p);}catch(e){}},50);}}catch(e){}};
LS.factor=function(ids){ids=[].concat(ids||[]).filter(known);if(!ids.length)return 1;return ids.reduce((a,id)=>a+st(id).f,0)/ids.length;};
/* Punkte für base in Bezug auf die Pakete ids (Durchschnitt bei mehreren, z. B. im Test) */
LS.pts=function(base,ids){if(!A)return base;ids=[].concat(ids||[]).filter(known);if(!ids.length||!(base>0))return base;
  const f=LS.factor(ids),p=points(base,f);if(f<1&&!hinted){hinted=true;setTimeout(()=>LS.hint(ids),300);}return p;};
/* Antwort zu einem Paket merken (für die Stufe am Rundenende) */
LS.answer=function(id,ok){if(!A||!known(id))return;flush();const b=buf[id]=buf[id]||{ok:0,n:0};b.n++;if(ok)b.ok++;
  if(b.n>=C().RUNDE_MAX_ANTWORTEN){pend[id]=b;delete buf[id];flush();}};
/* Rundenende: Pakete mit genug Antworten werden gewertet (siehe flush) */
LS.endRound=function(){if(!A)return;Object.assign(pend,buf);buf={};hinted=false;};
LS.flush=flush;
/* Bestes Paket zum Weiterlernen (für Hinweis und Startseite) */
LS.best=function(exclude){if(!A)return null;flush();exclude=[].concat(exclude||[]);
  const L=A.units.filter(u=>!exclude.includes(u.id)).map(u=>({u,st:st(u.id)})).filter(x=>x.st.f>=1);
  L.sort((a,b)=>RANK[a.st.kind]-RANK[b.st.kind]||(a.st.played===b.st.played?0:a.st.played?-1:1)||a.st.s-b.st.s);return L[0]||null;};

/* Anzeige auf der Paket-Kachel (innerhalb eines <button>, daher nur <span>) */
LS.tile=function(id){if(!A||!known(id))return"";flush();const s=st(id);
  return `<span class="ls-tile ls-${s.kind}"><span class="ls-txt">${esc(TXT[s.kind](s))}</span></span>`;};
/* Kurzer, freundlicher Hinweis, wenn es wenig Punkte gibt – mit Sprung zum lohnenderen Paket */
LS.hint=function(ids){if(!A)return;const s=st([].concat(ids)[0]),b=LS.best(ids);let el=document.getElementById("lsHint");
  if(!el){el=document.createElement("div");el.id="lsHint";el.setAttribute("role","status");document.body.appendChild(el);}
  const head=s.kind==="genug"?"Für heute hast du das schon richtig viel geübt! 💪":"Das kannst du schon super! 🌟";
  el.innerHTML=`<div><b>${head}</b> ${b?`Hier gibt's gerade ${b.st.kind==="bonus"?"Bonus-Punkte":"volle Punkte"}: <b>${esc(b.u.icon+" "+b.u.name)}</b>`:"Morgen gibt's hier wieder mehr Punkte."}</div>`+
    `<div class="ls-hb">${b&&A.pick?`<button type="button" data-lsgo="${esc(b.u.id)}">👉 Dorthin</button>`:""}<button type="button" data-lsx="1">Weiter üben</button></div>`;
  el.classList.add("on");clearTimeout(LS.hint.t);LS.hint.t=setTimeout(()=>el.classList.remove("on"),7000);
  el.onclick=e=>{const g=e.target.closest("[data-lsgo]");if(g){el.classList.remove("on");LS.endRound();try{A.pick(g.dataset.lsgo);}catch(_){}}else if(e.target.closest("[data-lsx]"))el.classList.remove("on");};};

/* ---------- Startseite: „Heute lohnt sich besonders“ ---------- */
LS.lohnt=function(list,base){/* list: [{app, units, store}] → [{app,u,st,p}] */
  const out=[];list.forEach(a=>a.units.forEach(u=>{const s=status((a.store||{})[u.id]);
    if(s.played&&(s.kind==="bonus"||s.kind==="faellig"||s.kind==="ueben"))out.push({app:a.app,u,st:s,p:points(a.base||base||10,s.f)});}));
  out.sort((a,b)=>RANK[a.st.kind]-RANK[b.st.kind]||a.st.s-b.st.s||b.st.el-a.st.el);return out;};

function css(){if(document.getElementById("lsCss"))return;const s=document.createElement("style");s.id="lsCss";s.textContent=`
.ls-tile{display:flex;flex-direction:column;gap:4px;margin-top:8px;padding:7px 9px;border-radius:12px;background:rgba(255,209,102,.16);border:1px solid rgba(214,158,20,.35);font-size:12.5px;line-height:1.25;text-align:left}
.ls-txt{font-weight:800;font-size:14px}
.ls-sitzt,.ls-genug{background:rgba(128,128,128,.10);border-color:rgba(128,128,128,.3)}
.ls-bonus{background:rgba(124,255,107,.18);border-color:rgba(40,160,60,.45)}
#lsHint{position:fixed;left:50%;top:calc(68px + env(safe-area-inset-top,0px));transform:translate(-50%,calc(-100% - 90px));z-index:9998;width:min(560px,calc(100vw - 24px));
  background:#fffaf0;color:#2b2b2b;border:2px solid #f0b43c;border-radius:16px;padding:12px 14px;box-shadow:0 10px 30px rgba(0,0,0,.25);font:600 15px/1.35 system-ui,sans-serif;transition:transform .35s ease}
#lsHint.on{transform:translate(-50%,0)}
#lsHint .ls-hb{display:flex;gap:8px;margin-top:8px;flex-wrap:wrap}
#lsHint button{min-height:40px;padding:0 14px;border-radius:10px;border:1px solid #d9a530;background:#fff;font:800 14px system-ui,sans-serif;color:#2b2b2b;cursor:pointer}
#lsHint button[data-lsgo]{background:#f0b43c;border-color:#f0b43c}`;document.head.appendChild(s);}
LS.css=css;
window.LS=LS;
})();
