/* Gemeinsamer Kern jeder App: Testergebnisse speichern, Speicheränderungen an die Startseite melden (Geräte-Abgleich) */
window.lzRec=function(a,units,g,k){try{var L=JSON.parse(localStorage.getItem("lz-ergebnisse")||"[]"),d=new Date();L.push({a:a,u:(window.__NUTZER&&window.__NUTZER.cur)||"u1",units:[].concat(units),g:+g,k:k||"",d:d.getFullYear()+"-"+(d.getMonth()+1)+"-"+d.getDate(),ts:Date.now()});if(L.length>600)L=L.slice(-600);localStorage.setItem("lz-ergebnisse",JSON.stringify(L));}catch(e){}};
(function(){try{const P=Storage.prototype,s=P.setItem,r=P.removeItem;const d=k=>{try{if(parent&&parent!==window&&parent.lzDirty)parent.lzDirty(k);}catch(e){}};P.setItem=function(k,v){s.call(this,k,v);if(this===localStorage)d(k);};P.removeItem=function(k){r.call(this,k);if(this===localStorage)d(k);};}catch(e){}})();
/* Die frühere KI-Korrektur ist entfernt; die Schreibtests nutzen die Selbstkontrolle. */
window.lzAIMsg=function(){return "";};window.lzAIRetry=function(){return false;};
