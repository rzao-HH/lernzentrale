/* Gemeinsamer Kern jeder App: Testergebnisse speichern, Speicheränderungen an die Startseite melden (Geräte-Abgleich) */
window.lzRec=function(a,units,g,k){try{var L=JSON.parse(localStorage.getItem("lz-ergebnisse")||"[]"),d=new Date();L.push({a:a,u:(window.__NUTZER&&window.__NUTZER.cur)||"u1",units:[].concat(units),g:+g,k:k||"",d:d.getFullYear()+"-"+(d.getMonth()+1)+"-"+d.getDate(),ts:Date.now()});if(L.length>600)L=L.slice(-600);localStorage.setItem("lz-ergebnisse",JSON.stringify(L));}catch(e){}};
(function(){try{const P=Storage.prototype,s=P.setItem,r=P.removeItem;const d=k=>{try{if(parent&&parent!==window&&parent.lzDirty)parent.lzDirty(k);}catch(e){}};P.setItem=function(k,v){s.call(this,k,v);if(this===localStorage)d(k);};P.removeItem=function(k){r.call(this,k);if(this===localStorage)d(k);};}catch(e){}})();
/* Die frühere KI-Korrektur ist entfernt; die Schreibtests nutzen die Selbstkontrolle. */
window.lzAIMsg=function(){return "";};window.lzAIRetry=function(){return false;};

/* Suche in „Alle ansehen“ (Lernkarten): alle Suchwörter müssen vorkommen; Groß/klein, Umlaute und ß egal */
window.lzFind=(function(){
  const norm=s=>String(s||"").toLowerCase().replace(/ß/g,"ss").normalize("NFD").replace(/[\u0300-\u036f]/g,"");
  const words=q=>norm(q).split(/\s+/).filter(Boolean);
  const hit=(q,texts)=>{const w=words(q),t=norm(texts.join(" "));return w.every(x=>t.includes(x));};
  /* html: bereits maskierter Text; markiert die Suchwörter mit <mark> */
  const mark=(html,q)=>{const w=String(q||"").split(/\s+/).filter(Boolean).map(x=>x.replace(/[.*+?^${}()|[\]\\]/g,"\\$&"));if(!w.length)return html;
    const re=new RegExp("("+w.join("|")+")","gi");return html.split(/(<[^>]*>)/).map(p=>p.startsWith("<")?p:p.replace(re,"<mark>$1</mark>")).join("");};
  return{norm,hit,mark};})();

/* Versionsnummer klein unten links in jeder App (aus dem ?v= dieses Skripts) */
(function(){try{const v=((document.currentScript||{}).src||"").split("v=")[1];if(!v)return;
  const add=()=>{if(document.getElementById("lzVer"))return;const d=document.createElement("div");d.id="lzVer";d.textContent="Version "+v;
    d.style.cssText="position:fixed;left:8px;bottom:calc(4px + env(safe-area-inset-bottom,0px));z-index:5;font:700 11px/1 system-ui,sans-serif;opacity:.45;pointer-events:none;color:inherit";document.body.appendChild(d);};
  if(document.body)add();else document.addEventListener("DOMContentLoaded",add);}catch(e){}})();
