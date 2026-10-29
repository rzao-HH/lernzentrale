/* ===================== 👤 Anmelden mit Benutzername =====================
   Der Benutzername ist überall eindeutig (Groß-/Kleinschreibung egal) und bestimmt, wem die Daten gehören.
   Noch ohne Passwort – später wird ein E-Mail-Konto einmal dem Benutzernamen zugeordnet. */
(function(){
const esc=s=>String(s==null?"":s).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const OV=document.createElement("div");OV.id="accOv";document.body.appendChild(OV);
let ST=null;/* {mode:'link'|'new', uid, name, e, step, profile, err} */
const DEF=n=>!n||n==="Ich";
function person(uid){return NU.list.find(x=>x.id===uid);}
function open(mode,uid){const u=uid&&person(uid);ST={mode,uid:u?u.id:null,name:u&&!DEF(u.name)?u.name:"",e:u?u.e:"🙂",step:"name",err:""};draw();OV.classList.add("on");}
function close(){OV.classList.remove("on");ST=null;try{render();}catch(e){}}
function draw(){if(!ST)return;
  if(ST.step==="confirm"){const p=ST.profile||{};
    OV.innerHTML=`<div class="ar-box c"><div class="ar-big">${esc(p.e||"👤")}</div><h3>„${esc(p.name||ST.name)}“ gibt es schon.</h3><p>Bist du das? Dann werden deine Punkte, Noten und dein Lernplan auf dieses Gerät geladen.</p>
      <div class="ar-row"><button type="button" class="ar-btn" data-accyes>✅ Ja, das bin ich</button><button type="button" class="ar-btn sec" data-accback>Nein, anderer Name</button></div></div>`;return;}
  if(ST.step==="busy"){OV.innerHTML=`<div class="ar-box c"><div class="ar-big">⏳</div><p>Einen Moment …</p></div>`;return;}
  OV.innerHTML=`<div class="ar-box"><div class="ar-top"><b>👤 ${ST.mode==="new"?"Neue Person anmelden":"Wie heißt du in der Lernzentrale?"}</b>${ST.mode==="new"?`<button type="button" class="ar-x" data-accx>✕</button>`:""}</div>
   <p class="ar-p0">Mit deinem Benutzernamen sind Punkte, Noten und Lernplan gesichert. Auf einem anderen Gerät gibst du einfach denselben Namen ein, und alles ist da.</p>
   <div class="gr-join"><input id="accIn" maxlength="20" placeholder="Benutzername, z. B. Robin" autocomplete="off" autocapitalize="words" spellcheck="false" value="${esc(ST.name)}" style="text-transform:none;font-family:inherit"></div>
   <div class="nuerr" id="accErr">${esc(ST.err)}</div>
   <div class="ar-h">Dein Symbol</div><div class="acc-emo">${(typeof EMOG!=="undefined"?EMOG:[]).map(([t,l])=>`<div class="emot">${esc(t)}</div><div class="acc-es">${l.map(x=>`<button type="button" data-acce="${x}" class="${x===ST.e?"on":""}">${x}</button>`).join("")}</div>`).join("")}</div>
   <button type="button" class="ar-btn" data-accgo>Weiter</button>
   ${ST.mode==="link"?`<button type="button" class="ar-btn sec" data-acclater>Später</button>`:""}</div>`;
  const i=document.getElementById("accIn");if(i)setTimeout(()=>i.focus(),50);}
async function go(){const i=document.getElementById("accIn");ST.name=(i?i.value:ST.name).trim().replace(/\s+/g," ");
  const acc=lzAccount.norm(ST.name);
  if(!acc){ST.err="Bitte einen Namen eingeben.";draw();return;}
  if(!/^[\p{L}\p{N} ._-]+$/u.test(ST.name)){ST.err="Bitte nur Buchstaben, Zahlen, Leerzeichen, Punkt, Minus oder Unterstrich.";draw();return;}
  if(NU.list.some(u=>u.acc===acc&&u.id!==ST.uid)){ST.err="„"+ST.name+"“ ist auf diesem Gerät schon angemeldet – oben einfach zu dieser Person wechseln.";draw();return;}
  if(!navigator.onLine){ST.err="Für die Anmeldung braucht es einmal Internet.";draw();return;}
  ST.step="busy";draw();
  try{const p=await lzAccount.lookup(ST.name);
    if(p){ST.profile=p;ST.step="confirm";draw();return;}
    await lzAccount.create(ST.name,ST.e);link({name:ST.name,e:ST.e});
  }catch(e){ST.step="name";ST.err="Keine Verbindung zum Server. Bitte gleich noch einmal versuchen.";draw();}}
function link(p){const acc=lzAccount.norm(p.name);let u;
  if(ST.mode==="new"){let id;do{id="u"+(100000+Math.floor(Math.random()*899900000));}while(NU.list.some(x=>x.id===id)||(NU.del||[]).includes(id));
    u={id,name:p.name,e:p.e||ST.e,t:Date.now()};NU.list.push(u);NU.cur=id;}
  else u=person(ST.uid);
  if(!u){close();return;}
  u.acc=acc;u.gid=acc;u.name=p.name||ST.name;u.e=p.e||ST.e;u.t=Date.now();
  save();close();lzAccount.pull();}
OV.addEventListener("click",e=>{const t=e.target;if(!ST)return;
  const em=t.closest("[data-acce]");if(em){const i=document.getElementById("accIn");ST.name=i?i.value:ST.name;ST.e=em.dataset.acce;const g=OV.querySelector(".acc-emo"),y=g?g.scrollTop:0;draw();const g2=OV.querySelector(".acc-emo");if(g2)g2.scrollTop=y;return;}
  if(t.closest("[data-accgo]")){go();return;}
  if(t.closest("[data-accyes]")){link(ST.profile);return;}
  if(t.closest("[data-accback]")){ST.step="name";ST.err="Dann wähle bitte einen anderen Namen, z. B. mit Anfangsbuchstaben des Nachnamens.";draw();return;}
  if(t.closest("[data-acclater]")){try{sessionStorage.setItem("lz-acc-later@"+ST.uid,"1");}catch(_){}close();return;}
  if(t.closest("[data-accx]")){close();return;}});
OV.addEventListener("keydown",e=>{if(e.key==="Enter"&&e.target.id==="accIn"){e.preventDefault();go();}});
/* Info zur Anmeldung (Klick auf „☁️ Gesichert · 👤 Name“) */
function info(){const u=person(NU.cur);if(!u)return;ST={mode:"info"};OV.classList.add("on");
  OV.innerHTML=`<div class="ar-box"><div class="ar-top"><b>👤 ${esc(u.e)} ${esc(u.name)}</b><button type="button" class="ar-x" data-accx>✕</button></div>
   <p>Angemeldet mit dem Benutzernamen <b>${esc(u.name)}</b>. Punkte, Noten, Lernplan, Lerngruppen und Arena-Punkte sind unter diesem Namen gesichert.</p>
   <p class="ar-p0">Auf einem anderen Gerät: oben „Neue Person“ bzw. beim ersten Start einfach denselben Namen eingeben.</p>
   <p class="ar-p0">Den Namen kann man nicht ändern. Das Symbol änderst du über die Personen-Auswahl.</p>
   <button type="button" class="ar-btn sec" data-acclogout>Auf diesem Gerät abmelden</button></div>`;}
OV.addEventListener("click",e=>{if(!e.target.closest("[data-acclogout]"))return;const u=person(NU.cur);if(!u)return;
  if(!confirm(`${u.name} auf diesem Gerät abmelden?\n\nDie Punkte bleiben unter dem Benutzernamen gespeichert und sind nach erneutem Anmelden wieder da.`))return;
  lzFlush&&lzFlush();NU.del=[...(NU.del||[]),u.id];NU.list=NU.list.filter(x=>x!==u);
  if(!NU.list.length){NU.list=[{id:"u"+(100000+Math.floor(Math.random()*899900000)),name:"Ich",e:"🙂"}];}
  NU.cur=NU.list[0].id;save();try{localStorage.removeItem("lz-linked@"+u.id);}catch(_){}lzPurge(u.id);OV.classList.remove("on");ST=null;render();});
document.addEventListener("click",e=>{const t=e.target.closest&&e.target;if(!t)return;
  if(t.closest("[data-acclink]")){open("link",NU.cur);return;}
  if(t.closest("[data-accinfo]")){info();return;}});
window.lzAccOpen=open;
/* Automatisch fragen, wenn die ausgewählte Person noch keinen Benutzernamen hat */
function auto(){try{if(OV.classList.contains("on"))return;const u=person(NU.cur);if(!u||u.acc)return;let later=null;try{later=sessionStorage.getItem("lz-acc-later@"+u.id);}catch(_){}
  if(later)return;if(typeof curApp!=="undefined"&&curApp)return;open("link",u.id);}catch(e){}}
window.lzAccAuto=auto;
setTimeout(auto,900);
})();
