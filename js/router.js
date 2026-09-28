const APPURL={W:"apps/winkel.html",Z:"apps/wasser.html",E:"apps/kueste.html",D:"apps/detektiv.html"};
const FR={};let lzPushed=false,curApp="";
function sig(k){return localStorage.getItem("nutzer-alle")+"|"+(NU&&NU.cur)+"|"+localStorage.getItem(lpKey(k))+"|"+localStorage.getItem("lzp-"+k+"@"+(NU&&NU.cur));}
function openPlan(f){const go=()=>{try{const d=f.contentDocument;d.getElementById("lpBtn").click();const t=d.querySelector('.lp-tab[data-t="set"]');if(t)t.click();}catch(e){}};if(f.dataset.ready)setTimeout(go,50);else f.addEventListener("load",()=>setTimeout(go,150),{once:true});}
function showApp(k,plan){
  if(!APPURL[k])return;
  loadAll();["W","Z","E","D"].forEach(x=>{try{sessionStorage.setItem("nutzer-ok-"+x,"1");}catch(e){}});
  let f=FR[k];
  if(!f){f=FR[k]=document.createElement("iframe");f.title=APPS.find(a=>a.k===k).name;document.getElementById("appv").appendChild(f);}
  if(f.dataset.sig!==sig(k)){f.dataset.sig=sig(k);/* sonst lädt ein zweiter Aufruf (Klick + Adresswechsel) die gerade startende App als leere Seite neu */f.dataset.ready="";f.addEventListener("load",()=>{f.dataset.ready="1";},{once:true});if(!f.getAttribute("src"))f.src=APPURL[k]+"?v=7.6.0";else{try{f.contentWindow.location.reload();}catch(e){f.src=APPURL[k]+"?v=7.6.0&r="+Date.now();}}}
  if(plan)openPlan(f);
  Object.values(FR).forEach(x=>x.classList.toggle("on",x===f));
  document.getElementById("appv").classList.add("on");document.documentElement.style.overflow="hidden";curApp=k;
  if(location.hash!=="#"+k){try{history.pushState(null,"","#"+k);lzPushed=true;}catch(e){}}
  setTimeout(()=>{try{f.focus();}catch(e){}},50);
}
function hideApp(){
  if(!curApp)return;const f=FR[curApp];loadAll();if(f)f.dataset.sig=sig(curApp);
  curApp="";document.getElementById("appv").classList.remove("on");document.documentElement.style.overflow="";render();
}
window.lzHome=function(){if(lzPushed&&location.hash){lzPushed=false;history.back();setTimeout(()=>{if(curApp)hideApp();},400);}else{hideApp();try{history.replaceState(null,"",location.pathname+location.search);}catch(e){}}};
function route(){const k=location.hash.slice(1);if(APPURL[k]){if(curApp!==k)showApp(k);}else hideApp();}
addEventListener("hashchange",route);setTimeout(lzDiag,0);window.FR=FR;window.lzAfterSync=()=>{Object.keys(FR).forEach(k=>{try{FR[k].remove();}catch(e){}delete FR[k];});if(curApp){location.reload();return;}loadAll();render();};document.addEventListener("visibilitychange",()=>{if(!document.hidden&&!curApp){loadAll();render();}});addEventListener("popstate",route);
route();
