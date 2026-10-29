/* Personen-Auswahl in den Apps */
(function(){
const A=window.__APPK, K="nutzer-alle", P=window.__NUTZER, DATA=window.__DATAKEY;
const EMG=[["Zauberwelt", ["🧙", "🧙‍♀️", "🧙‍♂️", "🪄", "⚡", "🦉", "🧹", "🔮", "📜", "🏰", "🗝️", "🧪", "🕯️", "🐉", "🐍", "🦁", "🦡", "🦅", "🦌", "🐈‍⬛", "🧝", "🧚", "🦄", "🐺"]], ["Weltraum", ["🚀", "🛸", "🛰️", "🌌", "🪐", "🌟", "⭐", "☄️", "🌠", "🌑", "🔭", "🧑‍🚀", "🤖", "👽", "👾", "🦾", "⚔️", "🗡️", "🛡️", "🥷"]], ["Personen", ["🧒", "👧", "👦", "🧑", "👩", "👨", "👵", "👴", "🧔", "👱", "🧑‍🎓", "🦸", "🦹"]], ["Haarfarben", ["👩‍🦰", "👱‍♀️", "👩‍🦱", "👩‍🦳", "👨‍🦰", "👱‍♂️", "👨‍🦱", "👨‍🦳", "🧑‍🦰", "🧑‍🦱", "🧑‍🦳", "👩‍🦲", "👨‍🦲"]], ["Tiere", ["🐭", "🐁", "🦊", "🐼", "🐸", "🐯", "🐙", "🐧", "🐢", "🐬", "🦖", "🐶", "🐱", "🐰"]]],EM=EMG.flatMap(g=>g[1]);
const $=s=>document.querySelector(s);
const esc=s=>String(s).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const save=()=>{try{const F=JSON.parse(localStorage.getItem(K)||"null");if(F&&F.list){const del=[...new Set([...(P.del||[]),...(F.del||[])])];F.list.forEach(u=>{if(!P.list.some(x=>x.id===u.id))P.list.push(u);});P.del=del;P.list=P.list.filter(u=>!del.includes(u.id));P.n=Math.max(P.n||1,F.n||1);}localStorage.setItem(K,JSON.stringify(P));}catch(e){}};
const cur=()=>P.list.find(u=>u.id===P.cur);
const keyOf=id=>DATA+(id==="u1"?"":"@"+id);
let mode="pick", draft={name:"",e:"🧒"}, editId=null;

function btn(){const b=document.getElementById("nuBtn");if(!b)return;const u=cur();
  b.innerHTML=`<span aria-hidden="true">${u.e}</span>${P.list.length>1?`<span class="nu-n">${esc(u.name)}</span>`:""}`;
  b.setAttribute("aria-label","Nutzer: "+u.name+". Wechseln");}
function open(m){try{const F=JSON.parse(localStorage.getItem(K)||"null");if(F&&F.list){P.list=F.list;P.n=F.n;P.del=F.del;}}catch(e){}mode=m||"pick";$("#nu").classList.add("open");draw();}
function close(){$("#nu").classList.remove("open");try{sessionStorage.setItem("nutzer-ok-"+A,"1");}catch(e){}}
function sw(id){try{sessionStorage.setItem("nutzer-ok-"+A,"1");}catch(e){}
  if(id===P.cur){close();return;} P.cur=id;save();location.reload();}
function draw(){
  const box=$("#nuBox");
  if(mode==="form"){
    box.innerHTML=`<div class="nu-f"><h2>${editId?"Person bearbeiten":"Neue Person"}</h2><p>Jede Person hat ihre eigenen Punkte und ihren eigenen Fortschritt. Der Lernplan gilt für alle.</p>
      <input type="text" id="nuName" maxlength="16" placeholder="Name" value="${esc(draft.name)}" aria-label="Name">
      <div class="nu-em">${EMG.map(([t,l])=>`<div class="nu-et">${t}</div><div class="nu-eg">${l.map(e=>`<button data-em="${e}" aria-pressed="${e===draft.e}">${e}</button>`).join("")}</div>`).join("")}</div>
      <div class="nu-err" id="nuErr"></div>
      <div class="nu-row"><button class="nu-b" id="nuBack">Abbrechen</button><button class="nu-b p" id="nuSave">${editId?"Speichern":"Anlegen und wechseln"}</button></div></div>`;
    box.querySelectorAll("[data-em]").forEach(b=>b.onclick=()=>{draft.e=b.dataset.em;draft.name=$("#nuName").value;const em=box.querySelector(".nu-em"),y=em?em.scrollTop:0;draw();const e2=box.querySelector(".nu-em");if(e2)e2.scrollTop=y;});
    $("#nuBack").onclick=()=>{editId=null;mode="pick";draw();};
    $("#nuSave").onclick=()=>{const n=$("#nuName").value.trim();
      if(!n){$("#nuErr").textContent="Bitte einen Namen eingeben.";return;}
      if(P.list.some(u=>u.id!==editId&&u.name.toLowerCase()===n.toLowerCase())){$("#nuErr").textContent="Diesen Namen gibt es schon.";return;}
      if(editId){const u=P.list.find(x=>x.id===editId);if(!u.acc)u.name=n;u.e=draft.e;u.t=Date.now();editId=null;save();btn();mode="pick";draw();return;}
      let id="u"+(100000+Math.floor(Math.random()*899900000));while(P.list.some(u=>u.id===id)||(P.del||[]).includes(id))id="u"+(100000+Math.floor(Math.random()*899900000));P.list.push({id,name:n,e:draft.e,t:Date.now()});save();sw(id);};
    setTimeout(()=>{const i=$("#nuName");if(i)i.focus();},50);
    return;
  }
  box.innerHTML=`<h2>Wer lernt gerade?</h2><p>Antippen zum Wechseln. Punkte und Fortschritt gehören zur gewählten Person.</p>
    <div class="nu-list">${P.list.map(u=>`<button class="nu-u ${u.id===P.cur?"cur":""}" data-u="${u.id}"><span class="e">${u.e}</span><span class="n">${esc(u.name)}</span>${u.id===P.cur?`<span class="c">gerade aktiv</span>`:""}</button>`).join("")}
      <button class="nu-u nu-add" id="nuAdd"><span class="e">＋</span><span class="n">Neue Person</span></button></div>
    ${mode==="manage"?`<div class="nu-mg">${P.list.map(u=>`<div class="it"><span>${u.e} ${esc(u.name)}</span><button data-ed="${u.id}">✎ Bearbeiten</button>${u.id!==P.cur?`<button data-del="${u.id}">Löschen</button>`:""}</div>`).join("")}</div>`:""}
    <div class="nu-row"><button class="nu-b" id="nuMg">${mode==="manage"?"Fertig":"Personen verwalten"}</button><button class="nu-b p" id="nuX">Weiter als ${esc(cur().name)}</button></div>`;
  box.querySelectorAll("[data-u]").forEach(b=>b.onclick=()=>sw(b.dataset.u));
  $("#nuAdd").onclick=()=>{draft={name:"",e:EM[P.list.length%EM.length]};editId=null;mode="form";draw();};
  $("#nuMg").onclick=()=>{mode=mode==="manage"?"pick":"manage";draw();};
  $("#nuX").onclick=close;
  box.querySelectorAll("[data-ed]").forEach(b=>b.onclick=()=>{const u=P.list.find(x=>x.id===b.dataset.ed);draft={name:u.name,e:u.e};editId=u.id;mode="form";draw();});
  box.querySelectorAll("[data-del]").forEach(b=>b.onclick=()=>{const u=P.list.find(x=>x.id===b.dataset.del);
    if(!confirm(u.name+" löschen? Punkte und Fortschritt dieser Person gehen verloren."))return;
    try{localStorage.removeItem(keyOf(u.id));}catch(e){}try{parent.lzPurge&&parent.lzPurge(u.id);}catch(e){}
    P.del=[...(P.del||[]),u.id];P.list=P.list.filter(x=>x.id!==u.id);save();draw();btn();});
}
const tgt=document.querySelector(window.__NU_TARGET);
if(tgt){const b=document.createElement("button");b.id="nuBtn";b.className=window.__NU_CLASS+" nu-btn";b.onclick=()=>open("pick");tgt.before(b);}
btn();
document.addEventListener("keydown",e=>{if(e.key==="Escape"&&$("#nu").classList.contains("open"))close();});
let ok=false;try{ok=sessionStorage.getItem("nutzer-ok-"+A)==="1";}catch(e){}
if(P.list.length>1&&!ok)open("pick");
})();
