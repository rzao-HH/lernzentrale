/* ===== Familien-Sync (Supabase) ===== */
(function(){
  const SB_URL='https://vhmxzlztbpjwfytnyhbv.supabase.co',SB_KEY='sb_publishable_x23BTTRX3UJBmXf0gGhyvQ_osygIIcE';
  const TRACK=/^(nutzer-alle|lernzentrale-v1|lz-ergebnisse|lernplan-|lzp-|winkelakademie|wasserzauberschule|unit6-progress|detektivbuero|lz-story@|lz-arena-|lz-groups@)/;window.__LZSB={url:SB_URL,key:SB_KEY};
  const P=Storage.prototype,oSet=P.setItem,oRem=P.removeItem;
  window.__lsSet=(k,v)=>oSet.call(localStorage,k,v);
  const LS=k=>{try{return localStorage.getItem(k);}catch(e){return null;}};
  let TS={};try{TS=JSON.parse(LS('lz-ts')||'{}')||{};}catch(e){}
  const saveTS=()=>{try{oSet.call(localStorage,'lz-ts',JSON.stringify(TS));}catch(e){}};
  const dirty=new Set();let timer=null,busy=false,err=false,last=0;
  const fam=()=>LS('lz-fam')||'';
  const on=()=>/^https:\/\//.test(SB_URL)&&fam().length>=12;
  const synced=()=>LS('lz-synced')===fam();
  const appOpen=()=>{try{return !!curApp;}catch(e){return false;}};
  /* Familien-Code per Link: …/#fam=CODE */
  try{const m=location.hash.match(/^#fam=([^&]+)/);if(m){const c=decodeURIComponent(m[1]).trim();if(c.length>=12){oSet.call(localStorage,'lz-fam',c);oRem.call(localStorage,'lz-synced');}history.replaceState(null,'',location.pathname+location.search);}}catch(e){}
  window.lzDirty=k=>{if(!TRACK.test(k))return;TS[k]=Date.now();saveTS();dirty.add(k);if(on()&&synced()){clearTimeout(timer);timer=setTimeout(flush,1500);}};
  P.setItem=function(k,v){oSet.call(this,k,v);if(this===localStorage)window.lzDirty(k);};
  P.removeItem=function(k){oRem.call(this,k);if(this===localStorage)window.lzDirty(k);};
  async function rpc(fn,body){
    const r=await fetch(SB_URL.replace(/\/+$/,'')+'/rest/v1/rpc/'+fn,{method:'POST',headers:{'Content-Type':'application/json',apikey:SB_KEY},body:JSON.stringify(body)});
    if(!r.ok)throw new Error('HTTP '+r.status);const t=await r.text();return t?JSON.parse(t):null;}
  window.__lzRpc=rpc;
  async function flush(){
    if(!on()||!synced())return;const ks=[...dirty];if(!ks.length)return;dirty.clear();
    const items=ks.map(k=>({k,v:LS(k),ts:TS[k]||Date.now()}));
    try{await rpc('lz_push',{p_fam:fam(),p_items:items});err=false;last=Date.now();}
    catch(e){ks.forEach(k=>dirty.add(k));err=true;}
    setStat();}
  window.lzFlush=flush;
  function mergeNU(A,B){
    A=A&&A.list?A:{list:[]};B=B&&B.list?B:{list:[]};
    const del=[...new Set([...(A.del||[]),...(B.del||[])])];
    const m=new Map();
    B.list.forEach(u=>{if(u&&u.id)m.set(u.id,u);});
    A.list.forEach(u=>{if(!u||!u.id)return;const x=m.get(u.id);if(!x||(u.t||0)>(x.t||0))m.set(u.id,u);if(x){const ga=u.gid,gb=x.gid,g=ga&&gb?(ga<gb?ga:gb):(ga||gb);const w=m.get(u.id);if(g&&w.gid!==g)m.set(u.id,Object.assign({},w,{gid:g}));}});
    const order=[...A.list.map(u=>u&&u.id),...B.list.map(u=>u&&u.id)].filter((id,i,a)=>id&&a.indexOf(id)===i);
    const list=order.map(id=>m.get(id)).filter(u=>u&&!del.includes(u.id));
    const n=Math.max(A.n||1,B.n||1);
    let cur=A.cur&&list.some(u=>u.id===A.cur)?A.cur:(list[0]&&list[0].id)||'u1';
    const out={list,cur,n};if(del.length)out.del=del;return out;}
  function mergeErg(A,B){
    const seen=new Set(),out=[];
    [...(Array.isArray(B)?B:[]),...(Array.isArray(A)?A:[])].forEach(r=>{if(!r)return;const key=JSON.stringify([r.a,r.u,r.ts,r.g,r.k,r.units]);if(!seen.has(key)){seen.add(key);out.push(r);}});
    out.sort((x,y)=>(x.ts||0)-(y.ts||0));return out.length>600?out.slice(-600):out;}
  const P0=o=>{try{return JSON.parse(o);}catch(e){return null;}};
  async function pull(){
    if(!on()||busy||appOpen())return;busy=true;let changed=false;
    try{
      const rows=(await rpc('lz_pull',{p_fam:fam(),p_since:0}))||[];
      const first=!synced(),R={};rows.forEach(x=>{if(x&&x.k)R[x.k]=x;});
      rows.forEach(x=>{
        const k=x.k;if(!k||!TRACK.test(k))return;
        const local=LS(k),lt=TS[k]||0,rt=+x.ts||0;
        if(k==='nutzer-alle'||k==='lz-ergebnisse'){
          if(x.v===null)return;const B=P0(x.v);if(!B)return;const A=P0(local);
          const M=k==='nutzer-alle'?mergeNU(A,B):mergeErg(A,B);const mv=JSON.stringify(M);
          if(mv!==local){oSet.call(localStorage,k,mv);changed=true;}
          const same=k==='nutzer-alle'?JSON.stringify(Object.assign({},M,{cur:0}))===JSON.stringify(Object.assign({},mergeNU(B,B),{cur:0})):mv===JSON.stringify(mergeErg(B,[]));
          if(same){TS[k]=rt;dirty.delete(k);}else{TS[k]=Math.max(Date.now(),rt+1);dirty.add(k);}
          return;}
        if(first||rt>lt){
          if(x.v===null){if(local!==null){oRem.call(localStorage,k);changed=true;}}
          else if(local!==x.v){oSet.call(localStorage,k,x.v);changed=true;}
          TS[k]=rt;dirty.delete(k);
        }else if(lt>rt&&local!==x.v)dirty.add(k);
      });
      for(let i=0;i<localStorage.length;i++){const k=localStorage.key(i);if(k&&TRACK.test(k)&&!R[k]){if(!TS[k])TS[k]=Date.now();dirty.add(k);}}
      saveTS();if(first)oSet.call(localStorage,'lz-synced',fam());
      err=false;last=Date.now();
    }catch(e){err=true;}
    busy=false;
    if(!err&&dirty.size)await flush();
    setStat();
    if(changed&&window.lzAfterSync)window.lzAfterSync();
  }
  window.lzPull=pull;
  const hh=d=>d.toLocaleTimeString('de-DE',{hour:'2-digit',minute:'2-digit'});
  function setStat(){
    const el=document.getElementById('lzcloud'),top=document.getElementById('lzsync');
    if(!/^https:\/\//.test(SB_URL)){if(el)el.textContent='📱 Fortschritt wird auf diesem Gerät gespeichert.';if(top)top.innerHTML='';return;}
    if(!on()){
      if(el)el.innerHTML='📱 Nur auf diesem Gerät gespeichert · <a href="#" data-fam="1">Geräte verbinden</a>';
      if(top&&!top.querySelector('.sync'))top.innerHTML='<div class="sync"><p><b>📱 Eigene Geräte verbinden</b><br>Mit einem Geräte-Code (mind. 12 Zeichen) ist der ganze Lernstand – Personen, Punkte, Noten, Lernpläne – auf iPad und Handy gleich. Nur für die eigenen Geräte, nicht weitergeben.</p><input id="lzfamin" type="text" autocomplete="off" autocapitalize="off" spellcheck="false" placeholder="Geräte-Code"><button type="button" data-famgo="1">Verbinden</button><div class="nuerr" id="lzfamerr"></div></div>';
      return;}
    const t=err?'⚠️ Gerade keine Verbindung – wird nachgeholt':'📱 Geräte verbunden'+(last?' ('+hh(new Date(last))+')':'');
    if(el)el.innerHTML=t+' · <a href="#" data-fam="1">Geräte-Code ändern</a>';
    if(top)top.innerHTML='<button type="button" class="syncpill'+(err?' err':'')+'" data-fam="1" title="Geräte-Code ändern">'+(err?'⚠️ Offline – wird nachgeholt':'📱 Geräte verbunden'+(last?' · '+hh(new Date(last)):''))+'<span class="syncedit">✏️ Geräte-Code ändern</span></button>';}
  function famSet(v){oSet.call(localStorage,'lz-fam',v);oRem.call(localStorage,'lz-synced');const top=document.getElementById('lzsync');if(top)top.innerHTML='';setStat();pull();}
  document.addEventListener('click',e=>{const b=e.target.closest&&e.target.closest('[data-famgo]');if(!b)return;e.preventDefault();
    const i=document.getElementById('lzfamin'),er=document.getElementById('lzfamerr'),v=(i&&i.value||'').trim();
    if(v.length<12){if(er)er.textContent='Der Code muss mindestens 12 Zeichen lang sein.';return;}famSet(v);});
  document.addEventListener('keydown',e=>{if(e.key==='Enter'&&e.target&&e.target.id==='lzfamin'){e.preventDefault();const b=document.querySelector('[data-famgo]');if(b)b.click();}});
  window.lzCloudStat=setStat;
  document.addEventListener('click',e=>{const a=e.target.closest&&e.target.closest('[data-fam]');if(!a)return;e.preventDefault();
    const c=prompt('Geräte-Code eingeben (mindestens 12 Zeichen).\nNur für die eigenen Geräte – nicht an andere weitergeben.\nAuf allen Geräten derselbe Code:',fam());
    if(c===null)return;const v=c.trim();
    if(!v){oRem.call(localStorage,'lz-fam');oRem.call(localStorage,'lz-synced');const top=document.getElementById('lzsync');if(top)top.innerHTML='';setStat();return;}
    if(v.length<12){alert('Der Code muss mindestens 12 Zeichen lang sein.');return;}
    famSet(v);});
  document.addEventListener('visibilitychange',()=>{if(document.hidden){if(dirty.size)flush();}else pull();});
  addEventListener('pagehide',()=>{if(dirty.size)flush();});
  setInterval(()=>{if(!document.hidden){if(dirty.size&&synced())flush();pull();}},30000);
  setTimeout(()=>{setStat();pull();},0);
})();
