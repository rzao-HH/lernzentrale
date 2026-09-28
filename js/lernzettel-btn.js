/* 📄-Knopf in der Kopfleiste: öffnet die Lernzettel der App (Dateien in lernzettel/, Liste in window.__LZ_ZETTEL).
   Eine Datei → direkt öffnen, mehrere → kleine Auswahl. Öffnet in neuem Tab, weil die App im iframe läuft. */
(function(){
var L=window.__LZ_ZETTEL;if(!L||!L.length)return;
var h=document.querySelector(".arena-btn")||document.querySelector(".home-btn");if(!h)return;
var base=(document.querySelector(".home-btn").className||"").replace(/\s*home-btn\b/,"");
var url=function(f){return"../lernzettel/"+f;};
var b=document.createElement("a");b.className=base+" home-btn zettel-btn";b.textContent="📄";b.title="Lernzettel";b.setAttribute("aria-label","Lernzettel öffnen");b.rel="noopener";
var m=null;
function close(){if(m){m.remove();m=null;}}
if(L.length===1){b.href=url(L[0].f);b.target="_blank";}
else{b.href="#";b.onclick=function(e){e.preventDefault();if(m){close();return;}
  m=document.createElement("div");m.className="zettel-menu";m.setAttribute("role","menu");
  var r=b.getBoundingClientRect();m.style.top=(r.bottom+6)+"px";m.style.right=Math.max(8,innerWidth-r.right)+"px";
  m.innerHTML='<b>📄 Lernzettel</b>'+L.map(function(x){return'<a role="menuitem" target="_blank" rel="noopener" href="'+url(x.f)+'">'+x.t+(x.d?'<small>'+x.d+'</small>':'')+'</a>';}).join("");
  m.addEventListener("click",function(ev){if(ev.target.closest("a"))setTimeout(close,0);});
  document.body.appendChild(m);};
  document.addEventListener("click",function(e){if(m&&!m.contains(e.target)&&e.target!==b)close();});
  document.addEventListener("keydown",function(e){if(e.key==="Escape")close();});
  addEventListener("resize",close);}
h.after(b);
var s=document.createElement("style");
s.textContent=".zettel-menu{position:fixed;z-index:9999;min-width:220px;max-width:calc(100vw - 16px);background:#fff;color:#1a1a2e;border:1px solid rgba(0,0,0,.15);border-radius:14px;box-shadow:0 10px 30px rgba(0,0,0,.25);padding:8px;font:600 15px/1.3 system-ui,sans-serif}.zettel-menu>b{display:block;padding:6px 10px 8px;font-size:13px;opacity:.7}.zettel-menu a{display:block;padding:10px;border-radius:10px;color:inherit;text-decoration:none}.zettel-menu a:hover,.zettel-menu a:focus{background:rgba(0,0,0,.07)}.zettel-menu small{display:block;font-weight:500;font-size:12.5px;opacity:.7;margin-top:2px}";
document.head.appendChild(s);
})();
