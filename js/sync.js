/* ===== Konten-Abgleich (Supabase) =====
   Jede Person ist mit ihrem Benutzernamen angemeldet (Feld `acc` in nutzer-alle).
   Ihre Daten liegen auf dem Server unter „lernzentrale:<benutzername>“ mit geräteunabhängigen Schlüsseln:
     app:W|Z|E|D  lzp:W|Z|E|D  plan:W|Z|E|D  arena  groups  story  erg  profile  g:<geister-duell-id>
   Auf dem Gerät bleiben die bisherigen Speicherschlüssel (mit lokaler Personen-Nummer) erhalten.
   Später (E-Mail + Passwort): Konto einmal dem Benutzernamen zuordnen, Schlüssel bleiben gleich. */
(function(){
  const SB_URL='https://vhmxzlztbpjwfytnyhbv.supabase.co',SB_KEY='sb_publishable_x23BTTRX3UJBmXf0gGhyvQ_osygIIcE';
  window.__LZSB={url:SB_URL,key:SB_KEY};
  const P=Storage.prototype,oSet=P.setItem,oRem=P.removeItem;
  window.__lsSet=(k,v)=>oSet.call(localStorage,k,v);
  const LS=k=>{try{return localStorage.getItem(k);}catch(e){return null;}};
  const PJ=v=>{try{return JSON.parse(v);}catch(e){return null;}};
  let TS={};try{TS=JSON.parse(LS('lz-ts')||'{}')||{};}catch(e){}
  const saveTS=()=>{try{oSet.call(localStorage,'lz-ts',JSON.stringify(TS));}catch(e){}};
  const dirty=new Set();let timer=null,busy=false,err=false,last=0;
  const online=()=>/^https:\/\//.test(SB_URL);
  const appOpen=()=>{try{return !!curApp;}catch(e){return false;}};
  const APPK={W:["winkelakademie-v1",3],Z:["wasserzauberschule-v1",3],E:["unit6-progress",3],D:["detektivbuero-v1",1]};
  const PLK={W:"lernplan-winkel",Z:"lernplan-wasser",E:"lernplan-englisch",D:"lernplan-deutsch"};
  const norm=n=>String(n||'').trim().replace(/\s+/g,' ').toLowerCase();
  const space=acc=>'lernzentrale:'+acc;/* Server verlangt mind. 12 Zeichen */
  function persons(){const o=PJ(LS('nutzer-alle'));return o&&Array.isArray(o.list)?o.list:[];}
  function accOf(uid){const u=persons().find(x=>x.id===uid);return u&&u.acc||'';}
  function toCanon(k){
    for(const a in APPK){const [b,r]=APPK[a];if(k===b)return{uid:'u1',c:'app:'+a};
      if(k.startsWith(b+'@')){const m=k.slice(b.length).match(/^@(u\d+)/);if(m&&k===b+('@'+m[1]).repeat(r))return{uid:m[1],c:'app:'+a};}}
    let m;
    if((m=k.match(/^lzp-([WZED])@(u\d+)$/)))return{uid:m[2],c:'lzp:'+m[1]};
    for(const a in PLK){if(k.startsWith(PLK[a]+'@')){const uid=k.slice(PLK[a].length+1);if(/^u\d+$/.test(uid))return{uid,c:'plan:'+a};}}
    if((m=k.match(/^lz-arena-pts@(u\d+)$/)))return{uid:m[1],c:'arena'};
    if((m=k.match(/^lz-groups@(u\d+)$/)))return{uid:m[1],c:'groups'};
    if((m=k.match(/^lz-story@(u\d+)$/)))return{uid:m[1],c:'story'};
    return null;}
  function toLocal(uid,c){let m;
    if((m=c.match(/^app:([WZED])$/))){const [b,r]=APPK[m[1]];return uid==='u1'?b:b+('@'+uid).repeat(r);}
    if((m=c.match(/^lzp:([WZED])$/)))return 'lzp-'+m[1]+'@'+uid;
    if((m=c.match(/^plan:([WZED])$/)))return PLK[m[1]]+'@'+uid;
    return {arena:'lz-arena-pts@',groups:'lz-groups@',story:'lz-story@'}[c]?{arena:'lz-arena-pts@',groups:'lz-groups@',story:'lz-story@'}[c]+uid:null;}
  window.lzDirty=k=>{if(!k||k==='lz-ts'||!(toCanon(k)||k==='lz-ergebnisse'||k==='nutzer-alle'||k.startsWith('lz-arena-g-')))return;
    TS[k]=Date.now();saveTS();dirty.add(k);clearTimeout(timer);timer=setTimeout(flush,1500);};
  P.setItem=function(k,v){oSet.call(this,k,v);if(this===localStorage)window.lzDirty(k);};
  P.removeItem=function(k){oRem.call(this,k);if(this===localStorage)window.lzDirty(k);};
  async function rpc(fn,body){
    const r=await fetch(SB_URL.replace(/\/+$/,'')+'/rest/v1/rpc/'+fn,{method:'POST',headers:{'Content-Type':'application/json',apikey:SB_KEY},body:JSON.stringify(body)});
    if(!r.ok){let m='';try{m=(JSON.parse(await r.text())||{}).message||'';}catch(e){}throw new Error('HTTP '+r.status+(m?' – '+m.slice(0,80):''));}const t=await r.text();return t?JSON.parse(t):null;}
  window.__lzRpc=rpc;
  /* ---------- Hochladen ---------- */
  function ergOf(uid){return (PJ(LS('lz-ergebnisse'))||[]).filter(r=>r&&(r.u||'u1')===uid);}
  function items(ks){const by={},add=(acc,it)=>{if(!acc)return;(by[acc]=by[acc]||[]).push(it);};const L=persons();
    ks.forEach(k=>{const ts=TS[k]||Date.now();
      if(k==='nutzer-alle'){L.forEach(u=>{if(u.acc)add(u.acc,{k:'profile',v:JSON.stringify({name:u.name,e:u.e}),ts:u.t||ts});});return;}
      if(k==='lz-ergebnisse'){L.forEach(u=>{if(u.acc)add(u.acc,{k:'erg',v:JSON.stringify(ergOf(u.id)),ts});});return;}
      if(k.startsWith('lz-arena-g-')){const g=PJ(LS(k));if(!g)return;const v=JSON.stringify(g);[g.from,g.to].forEach(p=>{if(p&&p.acc&&p.gid)add(p.gid,{k:'g:'+g.id,v,ts});});return;}
      const cc=toCanon(k);if(!cc)return;const u=L.find(x=>x.id===cc.uid);if(!u||!u.acc)return;/* gelöschte/abgemeldete Personen: nichts am Server ändern */
      const v=LS(k);if(v===null)return;add(u.acc,{k:cc.c,v,ts});});
    return by;}
  async function flush(){
    if(!online())return;const ks=[...dirty];if(!ks.length)return;dirty.clear();
    const by=items(ks);let ok=true;
    for(const acc in by){try{await rpc('lz_push',{p_fam:space(acc),p_items:by[acc]});}catch(e){ok=false;}}
    if(!ok){ks.forEach(k=>dirty.add(k));err=true;}else{err=false;last=Date.now();}
    stat();}
  window.lzFlush=flush;
  /* ---------- Herunterladen ---------- */
  function xpOf(v){const o=PJ(v);return o&&typeof o==='object'?(+o.xp||0):0;}
  async function pullAcc(u){
    const rows=(await rpc('lz_pull',{p_fam:space(u.acc),p_since:0}))||[];
    const first=LS('lz-linked@'+u.id)!==u.acc;let changed=false;const seen=new Set();
    rows.forEach(x=>{if(!x||!x.k||x.v==null)return;const rt=+x.ts||0;seen.add(x.k);
      if(x.k==='profile'||x.k==='erg')return;
      if(x.k.startsWith('g:')){const k='lz-arena-g-'+x.k.slice(2),lv=LS(k),L=PJ(lv),R=PJ(x.v);if(!R)return;
        const take=!L||(!L.res&&R.res)||(R.res&&L.res&&!L.res.fromSeen&&R.res.fromSeen)||(rt>(TS[k]||0)&&!(L.res&&!R.res));
        if(take&&lv!==x.v){oSet.call(localStorage,k,x.v);TS[k]=rt;changed=true;}return;}
      const k=toLocal(u.id,x.k);if(!k)return;const lv=LS(k),lt=TS[k]||0;
      let takeRemote;
      if(first)takeRemote=x.k.startsWith('app:')?(lv===null||xpOf(x.v)>=xpOf(lv)):true;
      else takeRemote=rt>lt;
      if(takeRemote){if(lv!==x.v){oSet.call(localStorage,k,x.v);changed=true;}TS[k]=rt;dirty.delete(k);}
      else if(lv!==null&&lv!==x.v)dirty.add(k);});
    /* Testergebnisse zusammenführen */
    const er=rows.find(r=>r.k==='erg');const all=PJ(LS('lz-ergebnisse'))||[];const mine=all.filter(r=>r&&(r.u||'u1')===u.id);
    if(er){const R=(PJ(er.v)||[]).map(r=>Object.assign({},r,{u:u.id}));const key=r=>JSON.stringify([r.a,r.ts,r.g,r.k,r.units]);const have=new Set(mine.map(key));
      const add=R.filter(r=>!have.has(key(r)));if(add.length){let L=all.concat(add).sort((a,b)=>(a.ts||0)-(b.ts||0));if(L.length>600)L=L.slice(-600);oSet.call(localStorage,'lz-ergebnisse',JSON.stringify(L));changed=true;}
      if(mine.length>R.length)dirty.add('lz-ergebnisse');}
    else if(mine.length)dirty.add('lz-ergebnisse');
    /* was nur auf dem Gerät liegt, hochladen */
    for(let i=0;i<localStorage.length;i++){const k=localStorage.key(i);const cc=k&&toCanon(k);if(cc&&cc.uid===u.id&&!seen.has(cc.c)){if(!TS[k])TS[k]=Date.now();dirty.add(k);}}
    if(!seen.has('profile'))dirty.add('nutzer-alle');
    saveTS();if(first)oSet.call(localStorage,'lz-linked@'+u.id,u.acc);
    return changed;}
  async function pull(){
    if(!online()||busy||appOpen())return;const L=persons().filter(u=>u.acc);if(!L.length){stat();return;}
    busy=true;let changed=false;
    try{for(const u of L)changed=(await pullAcc(u))||changed;err=false;last=Date.now();}catch(e){err=true;}
    busy=false;if(!err&&dirty.size)await flush();stat();
    if(changed&&window.lzAfterSync)window.lzAfterSync();}
  window.lzPull=pull;
  /* ---------- Konto: prüfen / anlegen ---------- */
  window.lzAccount={norm,
    async lookup(name){const rows=(await rpc('lz_pull',{p_fam:space(norm(name)),p_since:0}))||[];const p=rows.find(r=>r.k==='profile');return p?(PJ(p.v)||{}):null;},
    async create(name,e){await rpc('lz_push',{p_fam:space(norm(name)),p_items:[{k:'profile',v:JSON.stringify({name:String(name).trim(),e,created:Date.now()}),ts:Date.now()}]});},
    pull,flush};
  /* ---------- Anzeige oben ---------- */
  const hh=d=>d.toLocaleTimeString('de-DE',{hour:'2-digit',minute:'2-digit'});
  function stat(){const top=document.getElementById('lzsync');if(!top)return;let u=null;try{u=NU.list.find(x=>x.id===NU.cur);}catch(e){}
    if(!u){top.innerHTML='';return;}
    if(!u.acc){top.innerHTML=`<div class="sync"><p><b>👤 ${esc2(u.e)} ${esc2(u.name)} ist noch nicht angemeldet</b><br>Mit einem Benutzernamen sind Punkte, Noten und Lernplan gesichert und auf jedem Gerät da.</p><button type="button" data-acclink="1">Benutzername festlegen</button></div>`;return;}
    top.innerHTML=`<button type="button" class="syncpill${err?' err':''}" data-accinfo="1">${err?'⚠️ Offline – wird nachgeholt':'☁️ Gesichert'+(last?' · '+hh(new Date(last)):'')}<span class="syncedit">👤 ${esc2(u.name)}</span></button>`;}
  const esc2=s=>String(s==null?'':s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
  window.lzCloudStat=stat;
  document.addEventListener('visibilitychange',()=>{if(document.hidden){if(dirty.size)flush();}else pull();});
  addEventListener('pagehide',()=>{if(dirty.size)flush();});
  setInterval(()=>{if(!document.hidden){if(dirty.size)flush();pull();}},30000);
  setTimeout(()=>{stat();pull();},0);
})();
