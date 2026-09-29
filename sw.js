/* Service Worker: Lernzentrale offline verfügbar machen.
   Eigene Dateien: erst Netz (damit Updates sofort ankommen), ohne Netz aus dem Speicher.
   Schriften und Bibliotheken von anderen Servern: aus dem Speicher, im Hintergrund aktualisieren. */
const VER="7.10.1",CACHE="lz-"+VER,EXT="lz-ext";
const FILES=['./','apps/detektiv.html','apps/kueste.html','apps/wasser.html','apps/winkel.html','css/lernplan.css','css/nutzer.css','css/start.css','index.html','js/app-core.js','js/arena-btn.js','js/arena.js','js/groups.js','js/home-btn.js','js/konto.js','js/lernzettel-btn.js','js/lernplan.js','js/news.js','js/nutzer-init.js','js/nutzer.js','js/router.js','js/start.js','js/sync.js','icon-180.png'];
self.addEventListener("install",e=>{e.waitUntil(caches.open(CACHE).then(c=>c.addAll(FILES.map(f=>new Request(f,{cache:"reload"})))).then(()=>self.skipWaiting()));});
self.addEventListener("activate",e=>{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k.startsWith("lz-")&&k!==CACHE&&k!==EXT).map(k=>caches.delete(k)))).then(()=>self.clients.claim()));});
function timeout(ms){return new Promise((_,rej)=>setTimeout(()=>rej(new Error("timeout")),ms));}
self.addEventListener("fetch",e=>{
  const r=e.request;if(r.method!=="GET")return;const u=new URL(r.url);
  if(u.origin===location.origin){
    e.respondWith((async()=>{
      try{const res=await Promise.race([fetch(r),timeout(5000)]);if(res&&res.ok){const c=await caches.open(CACHE);c.put(r,res.clone());}return res;}
      catch(err){const c=await caches.open(CACHE);const hit=await c.match(r,{ignoreSearch:true});if(hit)return hit;
        if(r.mode==="navigate"){const idx=await c.match("index.html");if(idx)return idx;}throw err;}})());
    return;}
  if(/fonts\.(googleapis|gstatic)\.com$|cdn\.jsdelivr\.net$/.test(u.hostname)){
    e.respondWith((async()=>{const c=await caches.open(EXT);const hit=await c.match(r);
      const net=fetch(r).then(res=>{if(res&&(res.ok||res.type==="opaque"))c.put(r,res.clone());return res;}).catch(()=>hit);
      return hit||net;})());}
});
