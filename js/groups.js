/* ===================== 👥 Lerngruppen ===================== */
(function(){
const RPC=(fn,b)=>window.__lzRpc(fn,b);
const esc=s=>String(s==null?"":s).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const LSj=(k,d)=>{try{const v=localStorage.getItem(k);return v?JSON.parse(v):d;}catch(e){return d;}};
const LSs=(k,v)=>{try{localStorage.setItem(k,JSON.stringify(v));}catch(e){}};
const APPK=[["W","winkelakademie-v1",3],["Z","wasserzauberschule-v1",3],["E","unit6-progress",3],["D","detektivbuero-v1",1]];
const ALPH="ABCDEFGHJKLMNPQRSTUVWXYZ23456789";
const newCode=()=>{let c="";const r=crypto.getRandomValues(new Uint32Array(12));for(let i=0;i<12;i++)c+=ALPH[r[i]%ALPH.length];return c.slice(0,4)+"-"+c.slice(4,8)+"-"+c.slice(8);};
const normCode=c=>String(c||"").toUpperCase().replace(/[^A-Z0-9]/g,"").replace(/^(.{4})(.{4})(.{4})$/,"$1-$2-$3");
const space=code=>"grp:"+normCode(code);
function me(){const u=NU.list.find(x=>x.id===NU.cur)||NU.list[0];return u;}
function ensureGid(){try{loadAll();}catch(e){}const u=me();if(!u.gid){u.gid="p"+Math.random().toString(36).slice(2,10)+Date.now().toString(36).slice(-4);u.t=Date.now();try{save();}catch(e){}}return u;}
function groupsOf(uid){const a=LSj("lz-groups@"+uid,[]);return Array.isArray(a)?a:[];}
function setGroups(uid,a){LSs("lz-groups@"+uid,a);}
window.lzGroupsOf=groupsOf;
window.lzMyGroups=()=>{try{return groupsOf(me().id);}catch(e){return[];}};
window.lzMe=()=>{const u=me();return{uid:u.id,gid:u.gid,name:u.name,e:u.e};};
function online(){return !!window.__lzRpc&&/^https:/.test((window.__LZSB||{}).url||"");}
function xpOf(uid){const o={};APPK.forEach(([k,b,r])=>{const v=J(uid==="u1"?b:b+("@"+uid).repeat(r),null);o[k]=v&&typeof v==="object"?Math.max(0,+v.xp||0):0;});return o;}
function memberRec(u,alias){const ar=J("lz-arena-pts@"+u.id,{})||{};return{gid:u.gid,name:alias||u.name,e:u.e,xp:xpOf(u.id),ar:Math.max(0,+ar.p||0),ts:Date.now()};}
/* Mitgliedsdaten hochladen (nur Name, Icon, Punkte) */
const SENT={};
async function pushMembers(){if(!online())return;for(const u of NU.list){if(!u.gid)continue;const gs=groupsOf(u.id);if(!gs.length)continue;
  for(const g of gs){const r=memberRec(u,g.alias),sig=JSON.stringify([r.name,r.e,r.xp,r.ar]);const key=g.code+"|"+u.gid;if(SENT[key]===sig)continue;try{await RPC("lz_push",{p_fam:space(g.code),p_items:[{k:"m:"+u.gid,v:JSON.stringify(r),ts:Date.now()}]});SENT[key]=sig;}catch(e){}}}}
window.lzPushMembers=pushMembers;
/* Gruppendaten holen (Cache) */
const CACHE={};
async function pullGroup(code,force){const c=normCode(code),x=CACHE[c];if(x&&!force&&Date.now()-x.at<20000)return x;
  try{const rows=(await RPC("lz_pull",{p_fam:space(c),p_since:0}))||[];const o={at:Date.now(),meta:null,members:[],ghosts:[]};
    rows.forEach(r=>{if(r.v==null)return;let v=null;try{v=JSON.parse(r.v);}catch(e){}if(!v)return;
      if(r.k==="meta")o.meta=v;else if(r.k.startsWith("m:"))o.members.push(v);else if(r.k.startsWith("g:"))o.ghosts.push(Object.assign(v,{grp:c}));});
    CACHE[c]=o;return o;}catch(e){return x||null;}}
window.lzPullGroup=pullGroup;
window.lzGroupCache=c=>CACHE[normCode(c)];
window.lzGroupPut=async(code,k,v)=>{await RPC("lz_push",{p_fam:space(code),p_items:[{k,v:v==null?null:JSON.stringify(v),ts:Date.now()}]});const x=CACHE[normCode(code)];if(x)x.at=0;};
/* Anlegen / Beitreten / Austreten */
async function create(){const u=ensureGid();const name=(prompt("Wie soll die neue Lerngruppe heißen?\nz. B. Klasse 6b, Familie, Nachhilfe Mathe")||"").trim().slice(0,30);if(!name)return;
  if(!online()){alert("Lerngruppen brauchen eine Internetverbindung.");return;}
  if(groupsOf(u.id).some(g=>g.name.toLowerCase()===name.toLowerCase())&&!confirm(`${u.name} ist schon in einer Lerngruppe „${name}“.\nTrotzdem eine weitere mit demselben Namen anlegen? (Zur Unterscheidung steht der Code daneben.)`))return;
  const code=newCode();
  try{await RPC("lz_push",{p_fam:space(code),p_items:[{k:"meta",v:JSON.stringify({name,by:u.name,created:Date.now()}),ts:Date.now()}]});}catch(e){alert("Das hat nicht geklappt. Bitte später noch einmal versuchen.");return;}
  setGroups(u.id,[...groupsOf(u.id),{code,name,joined:Date.now()}]);await pushMembers();show({share:code});}
async function join(code){const u=ensureGid();code=normCode(code);if(!/^[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}$/.test(code)){alert("Der Code hat 12 Zeichen, z. B. KX7P-2M9Q-HT4R.");return false;}
  if(groupsOf(u.id).some(g=>g.code===code)){alert(u.name+" ist schon in dieser Lerngruppe.");return false;}
  const g=await pullGroup(code,true);if(!g||!g.meta){alert("Diese Lerngruppe gibt es nicht. Bitte den Code prüfen.");return false;}
  if(!confirm(`${u.e} ${u.name} tritt der Lerngruppe „${g.meta.name}“ bei?\n\nDie anderen sehen dann Name, Icon und Punkte und können ${u.name} zu Duellen herausfordern. Lernpläne und Noten bleiben privat.`))return false;
  let alias="";const taken=n=>g.members.some(m=>m.gid!==u.gid&&String(m.name).toLowerCase()===String(n).toLowerCase());
  if(taken(u.name)){for(;;){const a=prompt(`In „${g.meta.name}“ gibt es schon jemanden, der „${u.name}“ heißt.\nUnter welchem Namen möchtest du dort erscheinen? (z. B. mit Anfangsbuchstaben des Nachnamens)`,u.name+" "+u.name[0]+".");if(a===null)return false;const t=a.trim().slice(0,20);if(!t)continue;if(taken(t)){alert("Auch „"+t+"“ gibt es dort schon.");continue;}alias=t===u.name?"":t;break;}}
  const same=groupsOf(u.id).some(x=>x.name.toLowerCase()===String(g.meta.name).toLowerCase());if(same)alert(`Hinweis: ${u.name} ist schon in einer anderen Lerngruppe namens „${g.meta.name}“. Zur Unterscheidung steht der Code daneben.`);
  setGroups(u.id,[...groupsOf(u.id),{code,name:g.meta.name,joined:Date.now(),alias}]);await pushMembers();show();return true;}
async function leave(code){const u=me(),g=groupsOf(u.id).find(x=>x.code===code);if(!g)return;
  if(!confirm(`${u.name} verlässt die Lerngruppe „${g.name}“?`))return;
  setGroups(u.id,groupsOf(u.id).filter(x=>x.code!==code));try{await RPC("lz_push",{p_fam:space(code),p_items:[{k:"m:"+u.gid,v:null,ts:Date.now()}]});}catch(e){}delete SENT[code+"|"+u.gid];show();}
function link(code){return location.origin+location.pathname+"#join="+code;}
async function share(code,name){const url=link(code),text=`Tritt meiner Lerngruppe „${name}“ in der Lernzentrale bei: ${url}\nCode: ${code}`;
  try{if(navigator.share){await navigator.share({title:"Lerngruppe "+name,text});return;}}catch(e){if(e&&e.name==="AbortError")return;}
  try{await navigator.clipboard.writeText(text);alert("Link und Code sind kopiert. Du kannst sie jetzt z. B. per Nachricht verschicken.");}catch(e){prompt("Diesen Text kopieren und verschicken:",text);}}
/* Oberfläche */
const OV=document.createElement("div");OV.id="grpOv";document.body.appendChild(OV);
function show(o){o=o||{};const u=me(),gs=groupsOf(u.id);OV.classList.add("on");
  OV.innerHTML=`<div class="ar-box"><div class="ar-top"><b>👥 Lerngruppen</b><button type="button" class="ar-x" data-gx>✕</button></div>
   <p class="ar-p0">${esc(u.e)} <b>${esc(u.name)}</b> – in einer Lerngruppe sehen alle Name, Icon und Punkte und können sich zu Duellen herausfordern. Lernpläne und Noten bleiben privat.</p>
   ${o.share?(()=>{const g=gs.find(x=>x.code===o.share);return `<div class="gr-new"><div>✅ Lerngruppe <b>„${esc(g?g.name:"")}“</b> angelegt!</div><div class="gr-code">${esc(o.share)}</div><p class="ar-p0">Schick den Code oder Link an alle, die mitmachen sollen. Wer ihn eingibt, ist automatisch dabei.</p><button type="button" class="ar-btn" data-gshare="${esc(o.share)}">📤 Link teilen</button></div>`;})():""}
   <div class="ar-h">Deine Lerngruppen</div>
   ${gs.length?gs.map(g=>`<div class="ar-g"><b>👥 ${esc(g.name)}</b><small class="gr-c">${esc(g.code)}${g.alias?" · dort als „"+esc(g.alias)+"“":""}</small><span class="gr-btns"><button type="button" data-gshare="${esc(g.code)}">📤 Teilen</button><button type="button" class="sec" data-gleave="${esc(g.code)}">Austreten</button></span></div>`).join(""):`<p class="ar-p0">Noch keine. Leg eine an oder tritt mit einem Code bei.</p>`}
   <div class="ar-h">Beitreten</div><div class="gr-join"><input id="grIn" placeholder="Code, z. B. KX7P-2M9Q-HT4R" autocapitalize="characters" autocomplete="off" spellcheck="false"><button type="button" data-gjoin>Beitreten</button></div>
   <button type="button" class="ar-btn" data-gnew>➕ Neue Lerngruppe anlegen</button>
   ${online()?"":`<p class="ar-p0">⚠️ Ohne Internetverbindung gehen Lerngruppen nicht.</p>`}</div>`;}
window.lzGroupsOpen=()=>show();
OV.addEventListener("click",async e=>{const t=e.target;
  if(t.closest("[data-gx]")||t===OV){OV.classList.remove("on");try{render();}catch(_){}return;}
  if(t.closest("[data-gnew]")){await create();return;}
  const s=t.closest("[data-gshare]");if(s){const g=groupsOf(me().id).find(x=>x.code===s.dataset.gshare);share(s.dataset.gshare,g?g.name:"");return;}
  const l=t.closest("[data-gleave]");if(l){await leave(l.dataset.gleave);return;}
  if(t.closest("[data-gjoin]")){const v=document.getElementById("grIn").value;await join(v);return;}});
OV.addEventListener("keydown",e=>{if(e.key==="Enter"&&e.target.id==="grIn"){e.preventDefault();join(e.target.value);}});
/* Einladungs-Link …/#join=CODE */
function checkHash(){const m=location.hash.match(/^#join=([A-Za-z0-9-]+)/);if(!m)return;try{history.replaceState(null,"",location.pathname+location.search);}catch(e){}
  setTimeout(()=>{show();join(m[1]);},600);}
checkHash();
setInterval(pushMembers,30000);setTimeout(pushMembers,4000);
})();
