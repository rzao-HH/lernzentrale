/* Lernplan-Modul, gemeinsam für alle Apps (Konfiguration: window.LP_CONF in der App) */
(function(){
const C=window.LP_CONF, U=C.units;
/* Lernplan gilt pro Person: Schlüssel <plan>@<person>; alter gemeinsamer Plan wird einmalig übernommen */
const PK=C.key+"@"+((window.__NUTZER&&window.__NUTZER.cur)||"u1");try{if(localStorage.getItem(PK)===null){const o=localStorage.getItem(C.key);if(o!==null)localStorage.setItem(PK,o);}}catch(e){}
const $=s=>document.querySelector(s);
let S={n:0,done:[],today:1,ok:[]};
try{const r=localStorage.getItem(PK);if(r)S=Object.assign(S,JSON.parse(r));}catch(e){}
const save=()=>{try{localStorage.setItem(PK,JSON.stringify(S));}catch(e){}};
let draft=null, tab=null;
const LZU=(window.__NUTZER&&window.__NUTZER.cur)||"u1",LZK="lzp-"+C.prefix+"@";
function lzGet(u){try{return JSON.parse(localStorage.getItem(LZK+u)||"null")||{count:0,doneDate:"",log:{}};}catch(e){return{count:0,doneDate:"",log:{}};}}
function lzSet(u,o){try{localStorage.setItem(LZK+u,JSON.stringify(o));}catch(e){}}
function lzDay(){const d=new Date();return d.getFullYear()+"-"+(d.getMonth()+1)+"-"+d.getDate();}
function lzSync(){try{const r=localStorage.getItem(PK);if(r){const o=JSON.parse(r);S.n=o.n||0;S.done=o.done||[];}}catch(e){}
  const p=lzGet(LZU);S.ok=[];for(let i=1;i<=Math.min(p.count,S.n);i++)S.ok.push(i);S.today=Math.max(1,Math.min(p.count+1,S.n||1));}
lzSync();


function build(n,doneIds){
  const done=new Set(doneIds);
  const days=Array.from({length:n},(_,i)=>({d:i+1,learn:[],rep:[],fresh:[],final:false}));
  const open=U.filter(u=>!done.has(u.id)), k=open.length;
  if(n===1){days[0].learn=open.slice();days[0].final=true;return days;}
  days[n-1].final=true;
  const last=n-1, Lend=n>=4?n-2:n-1;
  const load=j=>3*days[j].learn.length+days[j].rep.length+days[j].fresh.length;
  const L=open.map((u,i)=>{const d=1+Math.floor(i*Lend/k);days[d-1].learn.push(u);return d;});
  open.forEach((u,i)=>{const r1=L[i]+1;if(r1<=last)days[r1-1].rep.push(u);});
  open.forEach((u,i)=>{
    const from=L[i]+2; if(from>last)return;
    let b=-1; for(let j=from-1;j<last;j++){const pref=j+1>=L[i]+3?0:0.5; if(b<0||load(j)+pref<load(b)+(b+1>=L[i]+3?0:0.5))b=j;}
    days[b].rep.push(u);
  });
  U.filter(u=>done.has(u.id)).forEach(u=>{let b=0;for(let j=1;j<last;j++)if(load(j)<load(b))b=j;days[b].fresh.push(u);});
  return days;
}
function mask(ids){return U.reduce((m,u,i)=>ids.includes(u.id)?m+Math.pow(2,i):m,0);}
function code(){return C.prefix+S.n+"-"+mask(S.done).toString(36).toUpperCase();}
function parse(t){
  const m=String(t).toUpperCase().replace(/\s/g,"").match(/^([A-Z])(\d{1,2})-([0-9A-Z]+)$/);
  if(!m)return{err:"Der Code hat nicht das richtige Format, zum Beispiel "+C.prefix+"6-3."};
  if(m[1]!==C.prefix)return{err:"Dieser Code gehört zu einer anderen App. Codes dieser App beginnen mit "+C.prefix+"."};
  const n=+m[2], mk=parseInt(m[3],36);
  if(n<1||n>30||isNaN(mk)||mk>=Math.pow(2,U.length))return{err:"Diesen Code kennt die App nicht. Bitte noch einmal prüfen."};
  return{n,done:U.filter((u,i)=>Math.floor(mk/Math.pow(2,i))%2===1).map(u=>u.id)};
}
const esc=s=>String(s).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const nm=u=>esc(u.icon+" "+u.name);

function renderBtn(){
  const b=document.getElementById("lpBtn"); if(!b)return;
  b.innerHTML="🗓️"+(S.n?`<span class="lp-t">${S.today}/${S.n}</span>`:"");
}
function open(t){lzSync();renderBtn();$("#lp").classList.add("open");document.body.style.overflow="hidden";show(t||(S.n?"plan":"set"));}
function close(){$("#lp").classList.remove("open");document.body.style.overflow="";setTimeout(()=>{const x=document.querySelector(".lzh:not(.lzh-ev)");if(x&&document.querySelector(".packs"))x.remove();if(window.lzRehome)lzRehome();if(window.lzBar)lzBar();},0);}
function show(t){tab=t;document.querySelectorAll(".lp-tab").forEach(b=>b.setAttribute("aria-selected",b.dataset.t===t));
  ({plan:rPlan,pk:rPk,set:rSet})[t]();$(".lp-body").scrollTop=0;}

function rSet(){
  if(!draft)draft={n:S.n||5,done:S.done.slice()};
  const groups=[...new Set(U.map(u=>u.group||""))];
  $("#lpBody").innerHTML=`
  <div class="lp-card"><h3>Wie viele Lerntage bleiben?</h3>
    <div class="lp-muted">Nur die Tage zählen, an denen wirklich gelernt wird. Freie Tage und Wochenenden also schon abziehen.</div>
    <div class="lp-step"><button id="lpM" aria-label="Weniger Tage">−</button><output id="lpN">${draft.n}</output><button id="lpP" aria-label="Mehr Tage">+</button><span class="lp-muted">Lerntage</span></div>
  </div>
  <div class="lp-card"><h3>Was sitzt schon?</h3>
    <div class="lp-muted">Haken setzen bei Paketen, die schon gut klappen. Sie werden nur noch einmal kurz aufgefrischt.</div>
    ${groups.map(g=>(g?`<div class="lp-muted" style="margin-top:10px;font-weight:800">${esc(g)}</div>`:"")+
      U.filter(u=>(u.group||"")===g).map(u=>`<div class="lp-pk"><input type="checkbox" id="lpc_${u.id}" data-id="${u.id}" ${draft.done.includes(u.id)?"checked":""}><label for="lpc_${u.id}">${nm(u)}${u.sub?`<small>${esc(u.sub)}</small>`:""}</label></div>`).join("")).join("")}
  </div>
  <button class="lp-go" id="lpGo">${S.n?"Plan neu erstellen":"Plan erstellen"}</button>
  <div class="lp-card" style="margin-top:16px"><h3>Plan auf anderem Gerät</h3>
    <div class="lp-muted">Der Code enthält Lerntage und Häkchen. Auf dem anderen Gerät eintippen, dann entsteht genau derselbe Plan.</div>
    ${S.n?`<div class="lp-code" style="margin-top:8px"><span class="lp-muted">Code dieses Plans:</span><b>${code()}</b></div>`:""}
    <div class="lp-code" style="margin-top:10px"><input id="lpIn" placeholder="${C.prefix}6-3" autocomplete="off" autocapitalize="characters" spellcheck="false" aria-label="Plan-Code"><button class="lp-sm" id="lpUse">Code übernehmen</button></div>
    <div class="lp-msg" id="lpMsg"></div>
  </div>`;
  const setN=v=>{draft.n=Math.max(1,Math.min(30,v));$("#lpN").textContent=draft.n;};
  $("#lpM").onclick=()=>setN(draft.n-1); $("#lpP").onclick=()=>setN(draft.n+1);
  document.querySelectorAll(".lp-pk input").forEach(c=>c.onchange=()=>{const id=c.dataset.id;draft.done=draft.done.filter(x=>x!==id);if(c.checked)draft.done.push(id);});
  $("#lpGo").onclick=()=>{apply(draft.n,draft.done);};
  $("#lpUse").onclick=()=>{const r=parse($("#lpIn").value);if(r.err){$("#lpMsg").textContent=r.err;$("#lpMsg").style.color="#b3342b";return;}apply(r.n,r.done);};
}
function apply(n,done){
  const changed=n!==S.n||mask(done)!==mask(S.done);
  S.n=n;S.done=U.filter(u=>done.includes(u.id)).map(u=>u.id);
  if(changed){S.ok=[];S.today=1;let L=[];try{L=(JSON.parse(localStorage.getItem("nutzer-alle")||"null")||{list:[{id:"u1"}]}).list;}catch(e){}lzSet((window.__NUTZER&&window.__NUTZER.cur)||"u1",{count:0,doneDate:"",log:{}});}
  S.today=Math.min(S.today,n);draft=null;save();renderBtn();show("plan");
}
function item(i,u,txt,hint){return `<li><span class="i">${i}</span><span><b>${txt}</b> ${nm(u)}${hint?`<small>${esc(hint)}</small>`:""}</span></li>`;}

function mkTests(C,U,days){
  const E=C.est||{learn:15,rep:5,test:10,final:20},seen={},learned=[],n=days.length,mid=n>=5?Math.floor(n/2):0;
  const LA=new Set();days.forEach(d=>d.learn.forEach(u=>LA.add(u.id)));
  const nm_=g=>(C.tests&&C.tests[g])||C.testName||"Test";
  const grp=(arr,goal,kind,T)=>{const by={};arr.forEach(u=>(by[u.group||""]=by[u.group||""]||[]).push(u));Object.keys(by).forEach(g=>T.push({name:nm_(g),units:U.filter(u=>by[g].includes(u)),goal,kind}));};
  return days.map(d=>{const T=[];
    d.learn.forEach(u=>{seen[u.id]=1;learned.push(u);});
    d.rep.forEach(u=>{seen[u.id]=(seen[u.id]||1)+1;});
    if(!d.final){
      grp(d.learn,3,"Neu",T);
      grp(d.rep.filter(u=>seen[u.id]===2),2,"Wiederholung",T);
      grp(d.rep.filter(u=>seen[u.id]>=3).concat(d.fresh),1,"Wiederholung",T);
      if(d.d===mid){const all=U.filter(u=>learned.includes(u)||!LA.has(u.id));if(all.length>=2)grp(all,2,"Zwischenprobe",T);}
    }
    if(C.write){const wd=mid||(n>=3?n-1:0),allL=U.filter(u=>learned.includes(u)||!LA.has(u.id));
      if(!d.final&&d.d===wd&&allL.length)T.push({name:"Schreibtest",units:allL,goal:3,kind:"Schreibtest"});
      if(d.final)T.push({name:"Schreibtest",units:U.slice(),goal:2,kind:"Schreibtest"});}
    const m=E.learn*d.learn.length+E.rep*(d.rep.length+d.fresh.length)+E.test*T.length+T.filter(t=>t.kind==="Schreibtest").length*((E.write||15)-E.test)+(d.final?E.final:0);
    return{tests:T,min:Math.max(10,Math.round(m/5)*5)};});
}
function extras(days){return mkTests(C,U,days);}
function testLi(t){return `<li><span class="i">🏆</span><span><b>${t.kind==="Neu"?"Test neue Pakete":t.kind==="Zwischenprobe"?"Zwischenprobe":"Test Wiederholung"} (${esc(t.name)}):</b> ${t.units.map(nm).join(", ")}<small>Ziel: Note ${t.goal} oder besser. Nicht geschafft? Fehler anschauen und den Test am nächsten Lerntag wiederholen.</small></span></li>`;}
function rPlan(){
  if(!S.n){$("#lpBody").innerHTML=`<div class="lp-empty"><p class="lp-muted">Noch kein Plan. Unter „Einstellen“ Lerntage wählen oder einen Code eingeben.</p><button class="lp-go" id="lpToSet">Plan einstellen</button></div>`;$("#lpToSet").onclick=()=>show("set");return;}
  const days=build(S.n,S.done), X=extras(days);
  $("#lpBody").innerHTML=`
  <div class="lp-card lp-today"><label for="lpDay"><b>Heute ist</b></label>
    <select id="lpDay">${days.map(d=>`<option value="${d.d}" ${d.d===S.today?"selected":""}>Tag ${d.d}</option>`).join("")}</select>
    <span class="lp-muted">Plan-Code ${code()}</span></div>
  ${days.map(d=>{
    const grp=(arr,ic,txt)=>{const gs=[...new Set(arr.map(u=>u.group||""))];return gs.map(g=>{const us=arr.filter(u=>(u.group||"")===g);
      return `<li><span class="i">${ic}</span><span><b>${txt}</b> ${us.map(nm).join(", ")}<small>${esc(us[0].rep)}${us.length>1?" "+C.multi:""}</small></span></li>`;}).join("");};
    const li=[...d.learn.map(u=>item("📘",u,"Lernen:",u.learn))];
    if(d.rep.length)li.push(grp(U.filter(u=>d.rep.includes(u)),"🔁","Wiederholen:"));
    if(d.fresh.length)li.push(grp(U.filter(u=>d.fresh.includes(u)),"✨","Auffrischen:"));
    X[d.d-1].tests.forEach(t=>li.push(testLi(t)));
    if(d.final)li.push(`<li><span class="i">🎓</span><span><b>Generalprobe:</b> ${esc(C.final)}<small>Ziel: Note 1 oder 2. ${S.n>1?"Kein neuer Stoff. Fehler notieren und die Pakete dazu noch einmal kurz anschauen.":"Alles an einem Tag: erst lernen, dann testen."}</small></span></li>`);
    if(!li.length)li.push(`<li><span class="i">☕</span><span class="lp-muted">Heute ist nichts eingeplant.</span></li>`);
    const ok=S.ok.includes(d.d), now=d.d===S.today;
    return `<div class="lp-card lp-day ${now?"now":""} ${ok?"ok":""}"><h3>Tag ${d.d}${now?`<span class="lp-now">heute</span>`:""}<span class="lp-min">⏱️ ca. ${X[d.d-1].min} Min.</span></h3><ul>${li.join("")}</ul>
      <label class="lp-chk"><input type="checkbox" data-d="${d.d}" ${ok?"checked":""}> erledigt</label></div>`;}).join("")}`;
  $("#lpDay").onchange=e=>{{const p=lzGet(LZU);p.count=+e.target.value-1;p.doneDate="";p.log=p.log||{};for(let i=1;i<=p.count;i++){p.log[i]=p.log[i]||{c:{},g:{}};p.log[i].end=p.log[i].end||Date.now();}Object.keys(p.log).forEach(i=>{if(+i>p.count)delete p.log[i].end;});lzSet(LZU,p);lzSync();}save();renderBtn();rPlan();};
  document.querySelectorAll(".lp-chk input").forEach(c=>c.onchange=()=>{const d=+c.dataset.d,p=lzGet(LZU);if(c.checked){p.count=Math.max(p.count,d);p.doneDate=lzDay();p.log=p.log||{};for(let i=1;i<=d;i++){p.log[i]=p.log[i]||{c:{},g:{}};p.log[i].end=p.log[i].end||Date.now();}}else{p.count=Math.min(p.count,d-1);p.doneDate="";p.log=p.log||{};Object.keys(p.log).forEach(i=>{if(+i>=d)delete p.log[i].end;});}lzSet(LZU,p);lzSync();save();renderBtn();rPlan();});
  const nowEl=document.querySelector(".lp-day.now"); if(nowEl&&S.today>1)setTimeout(()=>nowEl.scrollIntoView({block:"start"}),30);
}
function rPk(){
  if(!S.n){rPlan();return;}
  const days=build(S.n,S.done), info={};
  U.forEach(u=>info[u.id]={l:[],r:[],f:[]});
  days.forEach(d=>{d.learn.forEach(u=>info[u.id].l.push(d.d));d.rep.forEach(u=>info[u.id].r.push(d.d));d.fresh.forEach(u=>info[u.id].f.push(d.d));});
  const groups=[...new Set(U.map(u=>u.group||""))];
  $("#lpBody").innerHTML=groups.map(g=>`<div class="lp-card">${g?`<h3>${esc(g)}</h3>`:""}${U.filter(u=>(u.group||"")===g).map(u=>{const x=info[u.id];
    const tags=[...x.l.map(d=>`<span class="lp-tag l">📘 Lernen Tag ${d}</span>`),
      ...(x.r.length?[`<span class="lp-tag">🔁 Wiederholen Tag ${x.r.join(" + ")}</span>`]:[]),
      ...(x.f.length?[`<span class="lp-tag">✅ sitzt · ✨ Auffrischen Tag ${x.f.join(" + ")}</span>`]:[]),
      `<span class="lp-tag">🎓 Generalprobe Tag ${S.n}</span>`];
    return `<div class="lp-pk" style="display:block"><div><b>${nm(u)}</b>${u.sub?`<small>${esc(u.sub)}</small>`:""}</div><div>${tags.join("")}</div></div>`;}).join("")}</div>`).join("");
}
document.querySelectorAll(".lp-tab").forEach(b=>b.onclick=()=>show(b.dataset.t));
$("#lpX").onclick=close;
document.addEventListener("keydown",e=>{if(e.key==="Escape"&&$("#lp").classList.contains("open"))close();});
const tgt=document.querySelector(C.btnTarget);
if(tgt){const b=document.createElement("button");b.id="lpBtn";b.className=C.btnClass+" lp-btn";b.setAttribute("aria-label","Lernplan öffnen");b.onclick=()=>open();
  if(C.btnInsert==="after")tgt.after(b);else tgt.before(b);}
renderBtn();

window.lzToday=function(){
  lzSync(); if(!S.n)return null;
  const p=lzGet(LZU),t=Math.max(1,Math.min((p.count||0)+1,S.n)),days=build(S.n,S.done),X=extras(days),d=days[t-1],lo=(p.log&&p.log[t-1]&&p.log[t-1].end)||0;
  let R=[];try{R=JSON.parse(localStorage.getItem("lz-ergebnisse")||"[]").filter(r=>r.a===C.prefix&&r.u===LZU&&r.ts>lo);}catch(e){}
  const has=(r,us)=>r.units.length===us.length&&us.every(u=>r.units.includes(u.id));
  const tests=X[t-1].tests.map(tt=>{const rs=R.filter(r=>has(r,tt.units)&&(r.k==="write")===(tt.kind==="Schreibtest")),best=rs.length?Math.min(...rs.map(r=>r.g)):0;
    return{name:tt.name,kind:tt.kind,units:tt.units,goal:tt.goal,best,state:!best?"":best<=tt.goal?"ok":"no"};});
  if(d.final){[...new Set(U.map(u=>u.group||""))].forEach(g=>{const us=U.filter(u=>(u.group||"")===g),rs=R.filter(r=>r.k!=="write"&&has(r,us)),best=rs.length?Math.min(...rs.map(r=>r.g)):0;
    tests.push({name:(C.tests&&C.tests[g])||C.testName||"Test",kind:"Generalprobe",units:us,goal:2,best,state:!best?"":best<=2?"ok":"no",final:true});});}
  return{t,n:S.n,learn:d.learn,rep:d.rep,fresh:d.fresh,final:!!d.final,tests};
};
const lzUL=us=>us.map(u=>u.icon+" "+u.name).join(", ");
function lzBtn(kind,us,label,mt){
  const ids=us.map(u=>u.id).join(",");
  return`<button type="button" class="lzh-btn" data-lzsel="${ids}" data-lzm="${mt||(kind==="learn"&&C.prefix==="E"?"learn":"test")}">${label||"Diese Pakete wählen"}</button>`;
}
window.lzRows=function(filter){
  const T=window.lzToday(); if(!T)return[];
  const rows=[];
  const fl=us=>us.filter(u=>!filter||filter(u));
  const grp=(arr,tag,txt)=>{const us=fl(arr);if(!us.length)return;const tip=us.map(u=>u[txt]).filter(Boolean)[0]||"";
    rows.push(`<div class="lzh-row"><div><b>${tag}: ${lzUL(us)}</b>${tip?`<small>${tip}</small>`:""}</div>${lzBtn("learn",us)}</div>`);};
  grp(T.learn,"📘 Lernen","learn");grp(T.rep,"🔁 Wiederholen","rep");grp(T.fresh,"✨ Auffrischen","rep");
  T.tests.forEach(x=>{if(filter&&!x.units.every(filter))return;
    const lab=x.final?"🎓 Generalprobe ("+x.name+"): alle Pakete":x.kind==="Schreibtest"?"✍️ Schreibtest: "+lzUL(x.units):"🏆 "+(x.kind==="Neu"?"Test neue Pakete":x.kind==="Zwischenprobe"?"Zwischenprobe":"Test Wiederholung")+" ("+x.name+"): "+lzUL(x.units);
    const st=x.state==="ok"?`<span class="lzh-ok">✓ Note ${x.best} geschafft</span>`:x.state==="no"?`<span class="lzh-no">✗ Note ${x.best}, nochmal</span>`:"";
    rows.push(`<div class="lzh-row${x.state==="ok"?" done":""}"><div><b>${lab}</b><small>Ziel: Note ${x.final?"1 oder 2":x.goal+" oder besser"}${x.kind==="Schreibtest"?" · im Modus ✍️ Schreibtest":""}</small>${st}</div>${lzBtn("test",x.units,null,x.kind==="Schreibtest"?"write":"test")}</div>`);});
  return rows;
};
window.lzHint=function(filter,title){
  const T=window.lzToday(); if(!T)return"";
  const rows=window.lzRows(filter); if(!rows.length)return"";
  return`<div class="lzh"><div class="lzh-t">${title||"🗓️ Laut Lernplan heute (Tag "+T.t+" von "+T.n+")"}</div>${rows.join("")}</div>`;
};
window.lzEval=function(units,grade,kind){
  const T=window.lzToday(); if(!T)return"";
  const ids=[].concat(units),tt=T.tests.find(x=>(x.kind==="Schreibtest")===(kind==="write")&&x.units.length===ids.length&&x.units.every(u=>ids.includes(u.id)));
  let h;
  if(!tt)h=`<div class="lzh-t">🗓️ Dieser Test steht so nicht im Lernplan für heute.</div>`;
  else if(grade<=tt.goal)h=`<div class="lzh-t">🗓️ Lernplan: Ziel war Note ${tt.goal}${tt.final?" oder 2":""} → <span class="lzh-ok" style="display:inline">geschafft ✓</span></div>`;
  else h=`<div class="lzh-t">🗓️ Lernplan: Ziel war Note ${tt.goal} → <span class="lzh-no" style="display:inline">noch nicht geschafft.</span> Fehler anschauen und am nächsten Lerntag nochmal testen.</div>`;
  const nxt=T.tests.filter(x=>x!==tt&&x.state!=="ok");
  const btns=nxt.slice(0,1).map(x=>lzBtn("test",x.units,"➡️ Nächster Test: "+(x.final?"Generalprobe":x.kind==="Neu"?"neue Pakete":x.kind)+" · "+x.units.map(u=>u.name).join(", "),x.kind==="Schreibtest"?"write":"test"));
  btns.push(`<button type="button" class="lzh-btn lzh-home" data-lzhome>🏠 Zur Startseite</button>`);
  return`<div class="lzh lzh-ev">${h}<div class="lzh-acts">${btns.join("")}</div></div>`;
};
window.LP={build,parse,open};if(window.lzRehome)lzRehome();if(window.lzBar)lzBar();
})();
