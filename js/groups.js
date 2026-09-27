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
const DIR="lernzentrale:gruppen";/* Verzeichnis aller Lerngruppen: für alle sichtbar */
let DIRL=null;
async function dirPull(){try{const rows=(await RPC("lz_pull",{p_fam:DIR,p_since:0}))||[];DIRL=rows.map(r=>{let v=null;try{v=JSON.parse(r.v);}catch(e){}return v&&r.k.startsWith("grp:")?Object.assign(v,{code:r.k.slice(4)}):null;}).filter(Boolean);}catch(e){}return DIRL;}
async function dirAdd(code,name,by){try{await RPC("lz_push",{p_fam:DIR,p_items:[{k:"grp:"+code,v:JSON.stringify({name,by,created:Date.now()}),ts:Date.now()}]});}catch(e){}}
function me(){const u=NU.list.find(x=>x.id===NU.cur)||NU.list[0];return u;}
function ensureGid(){try{loadAll();}catch(e){}const u=me();if(!u.acc){alert("Bitte zuerst oben einen Benutzernamen festlegen.");window.lzAccOpen&&lzAccOpen("link",u.id);return null;}return u;}
function groupsOf(uid){const a=LSj("lz-groups@"+uid,[]);return Array.isArray(a)?a:[];}
function setGroups(uid,a){LSs("lz-groups@"+uid,a);}
window.lzGroupsOf=groupsOf;
window.lzMyGroups=()=>{try{return groupsOf(me().id);}catch(e){return[];}};
window.lzMe=()=>{const u=me();return{uid:u.id,gid:u.gid,name:u.name,e:u.e};};
function online(){return !!window.__lzRpc&&/^https:/.test((window.__LZSB||{}).url||"");}
function xpOf(uid){const o={};APPK.forEach(([k,b,r])=>{const v=J(uid==="u1"?b:b+("@"+uid).repeat(r),null);o[k]=v&&typeof v==="object"?Math.max(0,+v.xp||0):0;});return o;}
function memberRec(u,alias){const ar=J("lz-arena-pts@"+u.id,{})||{};return{gid:u.acc,acc:u.acc,name:alias||u.name,e:u.e,xp:xpOf(u.id),ar:Math.max(0,+ar.p||0),ts:Date.now()};}
/* Mitgliedsdaten hochladen (nur Name, Icon, Punkte) */
const SENT={};
async function pushMembers(){if(!online())return;for(const u of NU.list){if(!u.acc)continue;const gs=groupsOf(u.id);if(!gs.length)continue;
  for(const g of gs){const r=memberRec(u,g.alias),sig=JSON.stringify([r.name,r.e,r.xp,r.ar]);const key=g.code+"|"+u.gid;if(SENT[key]===sig)continue;try{await RPC("lz_push",{p_fam:space(g.code),p_items:[{k:"m:"+u.acc,v:JSON.stringify(r),ts:Date.now()}]});SENT[key]=sig;}catch(e){}}}}
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
async function create(){const u=ensureGid();if(!u)return;const name=(prompt("Wie soll die neue Lerngruppe heißen?\nz. B. Klasse 6b, Familie, Nachhilfe Mathe")||"").trim().slice(0,30);if(!name)return;
  if(!online()){alert("Lerngruppen brauchen eine Internetverbindung.");return;}
  if(DIRL&&DIRL.some(g=>String(g.name).toLowerCase()===name.toLowerCase())&&!confirm(`Eine Lerngruppe „${name}“ gibt es schon – unten unter „Weitere Lerngruppen“ kannst du ihr beitreten.\nTrotzdem eine neue mit demselben Namen anlegen?`))return;
  const code=newCode();
  try{await RPC("lz_push",{p_fam:space(code),p_items:[{k:"meta",v:JSON.stringify({name,by:u.name,created:Date.now()}),ts:Date.now()}]});}catch(e){alert("Das hat nicht geklappt. Bitte später noch einmal versuchen.");return;}
  await dirAdd(code,name,u.name);setGroups(u.id,[...groupsOf(u.id),{code,name,joined:Date.now()}]);await pushMembers();show({made:code});}
async function join(code){const u=ensureGid();if(!u)return false;code=normCode(code);if(!/^[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}$/.test(code)){alert("Der Code hat 12 Zeichen, z. B. KX7P-2M9Q-HT4R.");return false;}
  if(groupsOf(u.id).some(g=>g.code===code)){alert(u.name+" ist schon in dieser Lerngruppe.");return false;}
  const g=await pullGroup(code,true);if(!g||!g.meta){alert("Diese Lerngruppe gibt es nicht. Bitte den Code prüfen.");return false;}
  if(!confirm(`${u.e} ${u.name} tritt der Lerngruppe „${g.meta.name}“ bei?\n\nDie anderen sehen dann Name, Icon und Punkte und können ${u.name} zu Duellen herausfordern. Lernpläne und Noten bleiben privat.`))return false;
  let alias="";const taken=n=>g.members.some(m=>m.gid!==u.gid&&String(m.name).toLowerCase()===String(n).toLowerCase());
  if(taken(u.name)){for(;;){const a=prompt(`In „${g.meta.name}“ gibt es schon jemanden, der „${u.name}“ heißt.\nUnter welchem Namen möchtest du dort erscheinen? (z. B. mit Anfangsbuchstaben des Nachnamens)`,u.name+" "+u.name[0]+".");if(a===null)return false;const t=a.trim().slice(0,20);if(!t)continue;if(taken(t)){alert("Auch „"+t+"“ gibt es dort schon.");continue;}alias=t===u.name?"":t;break;}}
  
  setGroups(u.id,[...groupsOf(u.id),{code,name:g.meta.name,joined:Date.now(),alias}]);await pushMembers();show();return true;}
async function leave(code){const u=me(),g=groupsOf(u.id).find(x=>x.code===code);if(!g)return;
  if(!confirm(`${u.name} verlässt die Lerngruppe „${g.name}“?`))return;
  setGroups(u.id,groupsOf(u.id).filter(x=>x.code!==code));try{await RPC("lz_push",{p_fam:space(code),p_items:[{k:"m:"+u.acc,v:null,ts:Date.now()}]});}catch(e){}delete SENT[code+"|"+u.acc];show();}
/* Oberfläche */
const OV=document.createElement("div");OV.id="grpOv";document.body.appendChild(OV);
function show(o){o=o||{};const u=me(),gs=groupsOf(u.id);OV.classList.add("on");
  OV.innerHTML=`<div class="ar-box"><div class="ar-top"><b>👥 Lerngruppen</b><button type="button" class="ar-x" data-gx>✕</button></div>
   <p class="ar-p0">${esc(u.e)} <b>${esc(u.name)}</b> – in einer Lerngruppe sehen alle Name, Icon und Punkte und können sich zu Duellen herausfordern. Lernpläne und Noten bleiben privat.</p>
   ${o.made?(()=>{const g=gs.find(x=>x.code===o.made);return `<div class="gr-new"><div>✅ Lerngruppe <b>„${esc(g?g.name:"")}“</b> angelegt!</div><p class="ar-p0">Alle anderen sehen sie jetzt unter „Weitere Lerngruppen“ und können mit einem Tipp beitreten.</p></div>`;})():""}
   <div class="ar-h">Deine Lerngruppen</div>
   ${gs.length?gs.map(g=>`<div class="ar-g"><b>👥 ${esc(g.name)}</b>${g.alias?`<small class="gr-c">dort als „${esc(g.alias)}“</small>`:""}<span class="gr-btns"><button type="button" class="sec" data-gleave="${esc(g.code)}">Austreten</button></span></div>`).join(""):`<p class="ar-p0">Noch keine. Tritt unten einer bei oder leg eine neue an.</p>`}
   <div class="ar-h">Weitere Lerngruppen</div>
   ${(()=>{if(!DIRL)return `<p class="ar-p0">${online()?"Lädt …":"⚠️ Ohne Internetverbindung gehen Lerngruppen nicht."}</p>`;const mine=new Set(gs.map(g=>g.code));const L=DIRL.filter(g=>!mine.has(g.code)).sort((a,b)=>(b.created||0)-(a.created||0));
     return L.length?L.map(g=>`<div class="ar-g"><b>👥 ${esc(g.name)}</b><small class="gr-c">angelegt von ${esc(g.by||"?")}</small><span class="gr-btns"><button type="button" data-gjoin="${esc(g.code)}">Beitreten</button></span></div>`).join(""):`<p class="ar-p0">Keine weiteren – leg einfach eine neue an.</p>`;})()}
   <button type="button" class="ar-btn" data-gnew>➕ Neue Lerngruppe anlegen</button>
</div>`;
  if(!o.again&&online()){/* eigene ältere Gruppen ins Verzeichnis eintragen, dann Liste laden */
    dirPull().then(async L=>{if(!L)return;const have=new Set(L.map(g=>g.code));let add=false;for(const g of gs)if(!have.has(g.code)){await dirAdd(g.code,g.name,u.name);add=true;}if(add)await dirPull();if(OV.classList.contains("on"))show(Object.assign({},o,{again:true}));});}}
window.lzGroupsOpen=()=>show();
OV.addEventListener("click",async e=>{const t=e.target;
  if(t.closest("[data-gx]")||t===OV){OV.classList.remove("on");try{render();}catch(_){}return;}
  if(t.closest("[data-gnew]")){await create();return;}
  const l=t.closest("[data-gleave]");if(l){await leave(l.dataset.gleave);return;}
  const j=t.closest("[data-gjoin]");if(j){await join(j.dataset.gjoin);return;}});
/* ältere Einladungs-Links …/#join=CODE funktionieren weiter */
function checkHash(){const m=location.hash.match(/^#join=([A-Za-z0-9-]+)/);if(!m)return;try{history.replaceState(null,"",location.pathname+location.search);}catch(e){}
  setTimeout(()=>{show();join(m[1]);},600);}
checkHash();
setInterval(pushMembers,30000);setTimeout(pushMembers,4000);
})();
