const APPS=[
 {k:"W",name:"Winkel-Akademie",sub:"Mathe: Winkel, Karte & Kompass",icon:"📐"},
 {k:"Z",name:"Wasser-Zauberschule",sub:"NWT: Wasser",icon:"🪄"},
 {k:"E",name:"Küsten-Crew",sub:"Englisch Unit 5/6",icon:"🐚"},
 {k:"D",name:"Detektiv-Büro",sub:"Deutsch: Satzbau & Zeitformen",icon:"🕵️",url:"#D"}
];
const CONF={"W": {"units": [{"id": "p1", "icon": "🛰️", "name": "Spitz & Recht"}, {"id": "p2", "icon": "🚀", "name": "Stumpf & Gestreckt"}, {"id": "p3", "icon": "🪐", "name": "Überstumpf"}, {"id": "p4", "icon": "🌌", "name": "Null, Voll & Grenzfälle"}, {"id": "p5", "icon": "🧭", "name": "Kompass & Kurs"}, {"id": "p6", "icon": "🏷️", "name": "Winkel benennen"}, {"id": "p7", "icon": "🧮", "name": "Winkel berechnen"}, {"id": "p8", "icon": "📏", "name": "Senkrechte & Parallelen"}], "final": "Abschlusstest mit Note, dabei alle Pakete auswählen.", "testName": "Abschlusstest", "est": {"learn": 20, "rep": 5, "test": 10, "final": 20}}, "Z": {"units": [{"id": "p1", "icon": "🧊", "name": "Die drei Zustände"}, {"id": "p2", "icon": "🔄", "name": "Verwandlungen"}, {"id": "p3", "icon": "🧪", "name": "Eis schwimmt"}, {"id": "p4", "icon": "🏞️", "name": "Das Geheimnis des Sees"}, {"id": "p5", "icon": "🔬", "name": "Forschen wie Profis"}], "final": "Abschlusstest mit Note, dabei alle Pakete auswählen.", "testName": "Abschlusstest", "est": {"learn": 20, "rep": 5, "test": 10, "final": 20, "write": 15}, "write": true}, "E": {"units": [{"id": "v0", "icon": "📚", "name": "Vokabeln 1–15", "group": "Vokabeln"}, {"id": "v1", "icon": "📚", "name": "Vokabeln 16–30", "group": "Vokabeln"}, {"id": "v2", "icon": "📚", "name": "Vokabeln 31–45", "group": "Vokabeln"}, {"id": "v3", "icon": "📚", "name": "Vokabeln 46–60", "group": "Vokabeln"}, {"id": "v4", "icon": "📚", "name": "Vokabeln 61–75", "group": "Vokabeln"}, {"id": "v5", "icon": "📚", "name": "Vokabeln 76–90", "group": "Vokabeln"}, {"id": "v6", "icon": "📚", "name": "Vokabeln 91–105", "group": "Vokabeln"}, {"id": "v7", "icon": "📚", "name": "Vokabeln 106–120", "group": "Vokabeln"}, {"id": "v8", "icon": "📚", "name": "Vokabeln 121–135", "group": "Vokabeln"}, {"id": "v9", "icon": "📚", "name": "Vokabeln 136–145", "group": "Vokabeln"}, {"id": "g0", "icon": "⚡", "name": "Verben 1–40", "group": "Grammatik (simple past)"}, {"id": "g1", "icon": "⚡", "name": "Verben 41–77", "group": "Grammatik (simple past)", "sub": "Grammatik → Verben, Pakete 41–50 bis 71–77"}, {"id": "g2", "icon": "🧩", "name": "Lücken", "group": "Grammatik (simple past)"}, {"id": "g3", "icon": "❓", "name": "Fragen", "group": "Grammatik (simple past)"}, {"id": "g4", "group": "Grammatik (simple past)", "icon": "🕵️", "name": "Simple-Past-Detektiv", "sub": "-ed, didn't + Infinitiv, Did …?, Signalwörter", "learn": "Grammatik → 🕵️ Detektiv, alle Pakete. Dazu das Merkblatt „Simple Past“.", "rep": "Grammatik → Detektiv oder Grammatik-Test mit „Detektiv“."}, {"id": "g5", "group": "Schreibwerkstatt", "icon": "✍️", "name": "Schreibwerkstatt", "sub": "My Superhero's Craziest Day", "learn": "Grammatik → ✍️ Schreibwerkstatt: Geschichte schreiben und prüfen lassen.", "rep": "Schreibwerkstatt noch einmal mit einer neuen Geschichte."}, {"id": "g6", "group": "Grammatik (simple past)", "icon": "✅", "name": "Regelmäßige Verben", "sub": "-ed, -d, -ied, Verdopplung; regelmäßig oder unregelmäßig?", "learn": "Grammatik → 🔀 Regelmäßig oder unregelmäßig? (erst die Erklärung lesen), dann ✅ Verben (regelmäßig).", "rep": "✅ Verben (regelmäßig) oder 🔀 Regelmäßig oder unregelmäßig?"}], "final": "Vokabel-Test mit allen Paketen, dann der Grammatik-Test mit allen Themen und eine Geschichte in der Schreibwerkstatt.", "testName": "Test", "tests": {"Vokabeln": "Vokabel-Test", "Grammatik (simple past)": "Grammatik-Test", "Schreibwerkstatt": "Schreibwerkstatt"}, "est": {"learn": 15, "rep": 5, "test": 10, "final": 25, "write": 20}}, "D": {"key": "lernplan-deutsch", "prefix": "D", "btnTarget": "#soundBtn", "btnInsert": "before", "btnClass": "icon-btn", "multi": "Dafür mehrere Akten gleichzeitig auswählen.", "final": "Abschlusstest mit Note, dabei alle Akten auswählen.", "units": [{"id": "p1", "icon": "🔍", "name": "Hauptsatz & Nebensatz", "learn": "Erst „Akte lesen“, dann Verb-Jäger.", "rep": "Verb-Jäger oder Satzreihe oder Satzgefüge?"}, {"id": "p2", "icon": "🔗", "name": "Satzreihe", "learn": "Erst „Akte lesen“, dann Komma-Setzer und Konjunktion wählen.", "rep": "Komma-Setzer oder Satz-Baumeister."}, {"id": "p3", "icon": "🧩", "name": "Satzgefüge", "learn": "Erst „Akte lesen“, dann Satz-Baumeister und Komma-Setzer.", "rep": "Satz-Baumeister oder Verb-Jäger."}, {"id": "p4", "icon": "🗝️", "name": "Konjunktionen", "learn": "Erst „Akte lesen“, dann Konjunktion wählen.", "rep": "Konjunktion wählen oder Satz-Baumeister."}, {"id": "p5", "icon": "✒️", "name": "Komma-Profi", "learn": "Erst „Akte lesen“, dann Komma-Setzer und Satzreihe oder Satzgefüge?", "rep": "Komma-Setzer."}, {"id": "p6", "icon": "⏳", "name": "Zeitformen", "learn": "Erst „Akte lesen“, dann Zeitmaschine.", "rep": "Zeitmaschine."}], "testName": "Abschlusstest", "write": true, "est": {"learn": 15, "rep": 5, "test": 10, "final": 20, "write": 15}}};
const KEY="lernzentrale-v1";
let S={};
try{S=JSON.parse(localStorage.getItem(KEY)||"{}")||{};}catch(e){S={};}
const EMOG=[["Zauberwelt", ["🧙", "🧙‍♀️", "🧙‍♂️", "🪄", "⚡", "🦉", "🧹", "🔮", "📜", "🏰", "🗝️", "🧪", "🕯️", "🐉", "🐍", "🦁", "🦡", "🦅", "🦌", "🐈‍⬛", "🧝", "🧚", "🦄", "🐺"]], ["Weltraum", ["🚀", "🛸", "🛰️", "🌌", "🪐", "🌟", "⭐", "☄️", "🌠", "🌑", "🔭", "🧑‍🚀", "🤖", "👽", "👾", "🦾", "⚔️", "🗡️", "🛡️", "🥷"]], ["Personen", ["🧒", "👧", "👦", "🧑", "👩", "👨", "👵", "👴", "🧔", "👱", "🧑‍🎓", "🦸", "🦹"]], ["Haarfarben", ["👩‍🦰", "👱‍♀️", "👩‍🦱", "👩‍🦳", "👨‍🦰", "👱‍♂️", "👨‍🦱", "👨‍🦳", "🧑‍🦰", "🧑‍🦱", "🧑‍🦳", "👩‍🦲", "👨‍🦲"]], ["Tiere", ["🐭", "🐁", "🦊", "🐼", "🐸", "🐯", "🐙", "🐧", "🐢", "🐬", "🦖", "🐶", "🐱", "🐰"]]],EMO=EMOG.flatMap(g=>g[1]);
const LPK={W:"lernplan-winkel",Z:"lernplan-wasser",E:"lernplan-englisch",D:"lernplan-deutsch"},DK={W:"winkelakademie-v1",Z:"wasserzauberschule-v1",E:"unit6-progress",D:"detektivbuero-v1"};
const J=(k,d)=>{try{const v=localStorage.getItem(k);return v?JSON.parse(v):d;}catch(e){return d;}};
const JW=(k,v)=>{try{localStorage.setItem(k,JSON.stringify(v));}catch(e){}};
let NU=null,LPC={},PC={};
function nuMerge(N){const F=J("nutzer-alle",null);if(F&&F.list){const del=[...new Set([...(N.del||[]),...(F.del||[])])];F.list.forEach(u=>{if(!N.list.some(x=>x.id===u.id))N.list.push(u);});N.del=del;N.list=N.list.filter(u=>!del.includes(u.id));N.n=Math.max(N.n||1,F.n||1);if(N.cur===window.__nuLoadCur&&F.cur&&N.list.some(u=>u.id===F.cur))N.cur=F.cur;}if(!N.list.length)N.list=[{id:"u1",name:"Ich",e:"🙂"}];if(!N.list.some(u=>u.id===N.cur))N.cur=N.list[0].id;window.__nuLoadCur=N.cur;return N;}
function nuRecover(N){const ids=new Set();try{for(let i=0;i<localStorage.length;i++){const k=localStorage.key(i)||"";if(/^(lzp-|winkelakademie|wasserzauberschule|unit6-progress|detektivbuero)/.test(k)){const m=k.match(/@(u\d+)/);if(m)ids.add(m[1]);}}J("lz-ergebnisse",[]).forEach(r=>{if(r&&r.u)ids.add(r.u);});}catch(e){}
  let ch=false,mx=N.n||1;ids.forEach(id=>{mx=Math.max(mx,+id.slice(1)||0);if(id!=="u1"&&!N.list.some(u=>u.id===id)&&!(N.del||[]).includes(id)){N.list.push({id,name:"Person "+id.slice(1),e:"❓"});ch=true;}});
  N.list.forEach(u=>{mx=Math.max(mx,+u.id.slice(1)||0);});(N.del||[]).forEach(d=>{mx=Math.max(mx,+d.slice(1)||0);});if(mx!==N.n){N.n=mx;ch=true;}return ch;}
function lzAdopt(){/* verwaiste Punkte unter alten Speicher-Schlüsseln übernehmen */
  const APPS2=[["winkelakademie-v1",3],["wasserzauberschule-v1",3],["unit6-progress",3],["detektivbuero-v1",1]];let n=0;
  try{const keys=[];for(let i=0;i<localStorage.length;i++)keys.push(localStorage.key(i));
    APPS2.forEach(([base,rep])=>{keys.forEach(k=>{if(!k.startsWith(base+"@"))return;const parts=k.slice(base.length).split("@").filter(Boolean);if(!parts.length||parts.some(p=>p!==parts[0]))return;
      if(parts.length===rep)return;const cur=base+("@"+parts[0]).repeat(rep);let o=null,c=null;try{o=JSON.parse(localStorage.getItem(k));c=JSON.parse(localStorage.getItem(cur));}catch(e){}
      if(!o||typeof o!=="object")return;const ox=+(o.xp||0),cx=c&&typeof c==="object"?+(c.xp||0):-1;
      if(cx<ox||(c===null&&ox>=0)){localStorage.setItem(cur,JSON.stringify(o));n++;}});});}catch(e){}return n;}
function lzDiag(){try{const v=(document.querySelector(".ver")||{}).textContent||"";let B=J("lz-born",null);if(!B){B={d:Date.now(),v,h:location.hostname};JW("lz-born",B);}
  let L=J("lz-versions",[]);if(L[L.length-1]!==v){L.push(v);if(L.length>40)L=L.slice(-40);JW("lz-versions",L);}
  const el=document.getElementById("lzdiag");if(el)el.textContent="🔎 Speicher-Info: angelegt am "+new Date(B.d).toLocaleString("de-DE",{day:"2-digit",month:"2-digit",year:"numeric",hour:"2-digit",minute:"2-digit"})+" mit "+B.v+" · seitdem "+L.length+" Version(en) · Adresse: "+location.hostname;}catch(e){}}
function loadAll(){lzAdopt();
  NU=J("nutzer-alle",null);
  if(!NU||!NU.list||!NU.list.length){NU={list:[{id:"u1",name:"Ich",e:"🙂"}],cur:"u1",n:1};
    if(S.people){NU={list:S.people.map(u=>({id:u.id,name:u.name,e:u.icon})),cur:S.cur||"u1",n:S.people.length+1};}
    JW("nutzer-alle",NU);}
  if(!NU.list.some(u=>u.id===NU.cur))NU.cur=NU.list[0].id;
  if(nuRecover(NU))JW("nutzer-alle",NU);window.__nuLoadCur=NU.cur;
  Object.keys(LPK).forEach(k=>{const old=localStorage.getItem(LPK[k]);if(old===null)return;NU.list.forEach(u=>{if(localStorage.getItem(LPK[k]+"@"+u.id)===null&&!localStorage.getItem("lz-linked@"+u.id))localStorage.setItem(LPK[k]+"@"+u.id,old);});});
  if(NU.list.some(u=>!u.gid)){NU.list.forEach(u=>{if(!u.gid){u.gid="p"+Math.random().toString(36).slice(2,10)+Date.now().toString(36).slice(-4);u.t=Date.now();}});JW("nutzer-alle",NU);}
  LPC={};PC={};
  if(!S.mig2){["W","Z","E"].forEach(k=>{const o=S[k]||{};
      if(o.code&&!J(LPK[k],null)){const r=parse(k,o.code);if(!r.err)JW(LPK[k],{n:r.n,done:r.done,today:1,ok:[]});}
      if(!S.p&&o.count&&!J("lzp-"+k+"@u1",null))JW("lzp-"+k+"@u1",{count:o.count,doneDate:o.doneDate||"",log:{}});
      Object.keys(S.p||{}).forEach(u=>{const x=S.p[u][k];if(x&&!J("lzp-"+k+"@"+u,null))JW("lzp-"+k+"@"+u,x);});
      S[k]={goal:o.goal||"",last:o.last||0};});
    delete S.people;delete S.cur;delete S.p;S.mig2=1;JW(KEY,S);}
}
const lpKey=k=>LPK[k]+"@"+(NU&&NU.cur||"u1");window.lpKey=lpKey;
const save=()=>{JW(KEY,S);JW("nutzer-alle",nuMerge(NU));Object.keys(LPC).forEach(K=>JW(K,LPC[K]));Object.keys(PC).forEach(x=>JW(x,PC[x]));};
function people(){if(!NU)loadAll();return NU.list.map(u=>({id:u.id,name:u.name,icon:u.e}));}
const me=()=>people().find(u=>u.id===NU.cur);
const lp=k=>{const K=lpKey(k);return LPC[K]=LPC[K]||J(K,{n:0,done:[],today:1,ok:[]});};/* Cache pro Person */
const pst=(k,uid)=>{people();const x="lzp-"+k+"@"+(uid||NU.cur);if(PC[x])return PC[x];const o=J(x,{count:0,doneDate:"",log:{}});o.log=o.log||{};let ch=false;
  for(let t=1;t<=(o.count||0);t++){const l=o.log[t]=o.log[t]||{c:{},g:{}};if(!l.end){l.end=1;ch=true;}}
  Object.keys(o.log).forEach(t=>{if(+t>(o.count||0)&&o.log[t].end){delete o.log[t].end;ch=true;}});
  if(ch)JW(x,o);return PC[x]=o;};
const sh=k=>(S[k]=S[k]||{goal:"",last:0});
function codeOf(k){const a=lp(k),U=CONF[k].units;if(!a.n)return"";const m=U.reduce((m,u,i)=>(a.done||[]).includes(u.id)?m+Math.pow(2,i):m,0);return k+a.n+"-"+m.toString(36).toUpperCase();}
function st(k){const o={};
  Object.defineProperty(o,"code",{get:()=>codeOf(k),set:()=>{},enumerable:true});
  Object.defineProperty(o,"n",{get:()=>lp(k).n||0,set:v=>{lp(k).n=v;lp(k).ok=[];lp(k).today=1;},enumerable:true});
  Object.defineProperty(o,"done",{get:()=>lp(k).done||[],set:v=>{lp(k).done=v;},enumerable:true});
  ["goal","last"].forEach(f=>Object.defineProperty(o,f,{get:()=>sh(k)[f],set:v=>{sh(k)[f]=v;},enumerable:true}));
  ["count","doneDate","log"].forEach(f=>Object.defineProperty(o,f,{get:()=>pst(k)[f],set:v=>{pst(k)[f]=v;},enumerable:true}));
  return o;}
function lzPurge(id){try{const re=new RegExp("@"+id+"(?!\\d)"),ks=[];for(let i=0;i<localStorage.length;i++){const k=localStorage.key(i)||"";if(re.test(k))ks.push(k);}ks.forEach(k=>localStorage.removeItem(k));}catch(e){}
  JW("lz-ergebnisse",J("lz-ergebnisse",[]).filter(r=>r.u!==id));}
window.lzPurge=lzPurge;
const dlog=(k,t)=>{const L=pst(k).log;const o=L[t]=L[t]||{c:{},g:{}};o.a=o.a||{};return o;};
const esc=s=>String(s).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const dstr=d=>d.getFullYear()+"-"+(d.getMonth()+1)+"-"+d.getDate();
const today=()=>dstr(new Date());

function build(U,n,doneIds){
  const done=new Set(doneIds);
  const days=Array.from({length:n},(_,i)=>({d:i+1,learn:[],rep:[],fresh:[],final:false}));
  const open=U.filter(u=>!done.has(u.id)), k=open.length;
  if(n===1){days[0].learn=open.slice();days[0].final=true;return days;}
  days[n-1].final=true;
  const last=n-1, Lend=n>=4?n-2:n-1;
  const load=j=>3*days[j].learn.length+days[j].rep.length+days[j].fresh.length;
  const L=open.map((u,i)=>{const d=1+Math.floor(i*Lend/k);days[d-1].learn.push(u);return d;});
  open.forEach((u,i)=>{const r1=L[i]+1;if(r1<=last)days[r1-1].rep.push(u);});
  open.forEach((u,i)=>{
    const from=L[i]+2; if(from>last)return;
    let b=-1; for(let j=from-1;j<last;j++){const pref=j+1>=L[i]+3?0:0.5; if(b<0||load(j)+pref<load(b)+(b+1>=L[i]+3?0:0.5))b=j;}
    days[b].rep.push(u);
  });
  U.filter(u=>done.has(u.id)).forEach(u=>{let b=0;for(let j=1;j<last;j++)if(load(j)<load(b))b=j;days[b].fresh.push(u);});
  return days;
}
function parse(k,t){
  const U=CONF[k].units;
  const m=String(t).toUpperCase().replace(/\s/g,"").match(/^([A-Z])(\d{1,2})-([0-9A-Z]+)$/);
  if(!m)return{err:"Der Code hat nicht das richtige Format, zum Beispiel "+k+"6-3."};
  if(m[1]!==k)return{err:"Dieser Code gehört zu einer anderen App. Codes für diese App beginnen mit "+k+"."};
  const n=+m[2], mk=parseInt(m[3],36);
  if(n<1||n>30||isNaN(mk)||mk>=Math.pow(2,U.length))return{err:"Diesen Code gibt es nicht. Bitte in der App unter 🗓️ Lernplan nachsehen."};
  return{n,code:m[0],done:U.filter((u,i)=>Math.floor(mk/Math.pow(2,i))%2===1).map(u=>u.id)};
}
function ago(ts){
  if(!ts)return"noch nie von hier aus";
  const d=new Date(ts), now=new Date(), mins=Math.round((now-d)/60000);
  const t=d.toLocaleTimeString("de-DE",{hour:"2-digit",minute:"2-digit"});
  if(dstr(d)===dstr(now))return mins<2?"gerade eben":"heute, "+t+" Uhr";
  const y=new Date(now);y.setDate(y.getDate()-1);
  if(dstr(d)===dstr(y))return"gestern, "+t+" Uhr";
  const days=Math.round((new Date(dstr(now).replace(/-/g,"/"))-new Date(dstr(d).replace(/-/g,"/")))/86400000);
  return"vor "+days+" Tagen";
}
function names(us){return us.map(u=>esc(u.icon+" "+u.name)).join(", ");}
function mkTests(C,U,days){
  const E=C.est||{learn:15,rep:5,test:10,final:20},seen={},learned=[],n=days.length,mid=n>=5?Math.floor(n/2):0;
  const LA=new Set();days.forEach(d=>d.learn.forEach(u=>LA.add(u.id)));
  const nm_=g=>(C.tests&&C.tests[g])||C.testName||"Test";
  const grp=(arr,goal,kind,T)=>{const by={};arr.forEach(u=>(by[u.group||""]=by[u.group||""]||[]).push(u));Object.keys(by).forEach(g=>T.push({name:nm_(g),units:U.filter(u=>by[g].includes(u)),goal,kind}));};
  return days.map(d=>{const T=[];
    d.learn.forEach(u=>{seen[u.id]=1;learned.push(u);});
    d.rep.forEach(u=>{seen[u.id]=(seen[u.id]||1)+1;});
    if(!d.final){
      grp(d.learn,3,"Neu",T);
      grp(d.rep.filter(u=>seen[u.id]===2),2,"Wiederholung",T);
      grp(d.rep.filter(u=>seen[u.id]>=3).concat(d.fresh),1,"Wiederholung",T);
      if(d.d===mid){const all=U.filter(u=>learned.includes(u)||!LA.has(u.id));if(all.length>=2)grp(all,2,"Zwischenprobe",T);}
    }
    if(C.write){const wd=mid||(n>=3?n-1:0),allL=U.filter(u=>learned.includes(u)||!LA.has(u.id));
      if(!d.final&&d.d===wd&&allL.length)T.push({name:"Schreibtest",units:allL,goal:3,kind:"Schreibtest"});
      if(d.final)T.push({name:"Schreibtest",units:U.slice(),goal:2,kind:"Schreibtest"});}
    const m=E.learn*d.learn.length+E.rep*(d.rep.length+d.fresh.length)+E.test*T.length+T.filter(t=>t.kind==="Schreibtest").length*((E.write||15)-E.test)+(d.final?E.final:0);
    return{tests:T,min:Math.max(10,Math.round(m/5)*5)};});
}
function ext(k,days){return mkTests(CONF[k],CONF[k].units,days);}
const tkey=t=>t.name+":"+t.units.map(u=>u.id).join(",");
function full(k){
  const s=st(k),days=build(CONF[k].units,s.n,s.done),X=ext(k,days),E=CONF[k].est||{test:10},L=s.log||{};let carry=[];
  X.forEach((x,i)=>{const t=i+1,keys=new Set(x.tests.map(tkey));
    const add=carry.filter(c=>!keys.has(tkey(c))).map(c=>Object.assign({},c,{again:true}));
    if(add.length){x.tests=add.concat(x.tests);x.min+=Math.round(E.test*add.length/5)*5;}
    const g=(L[t]&&L[t].g)||{};carry=x.tests.filter(tt=>g[tkey(tt)]&&+g[tkey(tt)]>tt.goal);});
  return{days,X};
}
function gradeSel(k,t,key,val,goal){
  const o=["<option value=\"\">Note?</option>"].concat([1,2,3,4,5,6].map(n=>`<option value="${n}"${+val===n?" selected":""}>Note ${n}</option>`)).join("");
  const rs=RES[k+"|"+t+"|"+key]||[],fmtT=ts=>new Date(ts).toLocaleTimeString("de-DE",{hour:"2-digit",minute:"2-digit"});
  if(rs.length){const list=rs.map(r=>`<span class="rg${r.g<=goal?" ok":""}" title="${fmtT(r.ts)} Uhr">${r.g}</span>`).join("");
    const g=Math.min(...rs.map(r=>r.g));
    return `<span class="gr"><span class="res au">📲 Tests in der App:</span>${list}${g<=goal?`<span class="res ok">✓ Ziel erreicht</span>`:`<span class="res no">✗ nächster Lerntag: nochmal</span>`}</span>`;}
  const au="";

  const r=au+(val?(+val<=goal?`<span class="res ok">✓ Ziel erreicht</span>`:`<span class="res no">✗ nächster Lerntag: nochmal</span>`):"");
  return `<span class="gr"><select data-grade="${k}|${t}|${esc(key)}" aria-label="Erreichte Note">${o}</select>${r}</span>`;
}
function items(k,d,x,t){
  const ed=!!t, lg=ed?dlog(k,t):null;
  const L=(ic,key,html,goal)=>{
    if(!ed)return `<li><span>${ic}</span><span>${html}</span></li>`;
    const on=!!lg.c[key]||(goal&&lg.g[key]);
    return `<li class="ck${on?" on":""}"><label><input type="checkbox" data-chk="${k}|${t}|${esc(key)}"${on?" checked":""}><span>${ic}</span></label><span>${html}${goal?gradeSel(k,t,key,lg.g[key],goal):""}</span></li>`;};
  const li=[];
  if(d.learn.length)li.push(L("📘","learn",`<b>Lernen:</b> ${names(d.learn)}`));
  if(d.rep.length)li.push(L("🔁","rep",`<b>Wiederholen:</b> ${names(d.rep)}`));
  if(d.fresh.length)li.push(L("✨","fresh",`<b>Auffrischen:</b> ${names(d.fresh)}`));
  if(x)x.tests.forEach(tt=>li.push(L("🏆",tkey(tt),`<b>${tt.again?"Nochmal: ":""}${tt.kind==="Schreibtest"?"✍️ Schreibtest":(tt.kind==="Neu"?"Test neue Pakete":tt.kind==="Zwischenprobe"?"Zwischenprobe":"Test Wiederholung")+" ("+esc(tt.name)+")"}:</b> ${names(tt.units)} <em class="goalc">Ziel: Note ${tt.goal} oder besser</em>`,ed?tt.goal:0)));
  if(d.final)li.push(L("🎓","final",`<b>Generalprobe:</b> ${esc(CONF[k].final)} <em class="goalc">Ziel: Note 1 oder 2</em>`,ed?2:0));
  if(!li.length)li.push(`<li><span>☕</span><span>Nichts eingeplant.</span></li>`);
  return li.join("");
}
/* Tagesnummer, die "heute" in dieser App gilt (1-basiert); nächster offener Tag */
function curDay(s){return s.doneDate===today()?s.count:s.count+1;}
function nextDay(s){return s.count+1+(s.doneDate===today()?0:1);}
const UI=()=>(S.ui=S.ui||{});
function whenLabel(off){return off<=0?"Heute":off===1?"Nächster Lerntag":off+". Lerntag ab jetzt";}
function daysUntil(iso){const [y,m,d]=iso.split("-").map(Number);const a=new Date();a.setHours(0,0,0,0);return Math.round((new Date(y,m-1,d)-a)/86400000);}
function goalBox(k,s,doneToday){
  const g=s.goal||"", left=s.n-s.count;
  let chip="";
  if(g){const dd=daysUntil(g), avail=dd+(doneToday?0:1), p=avail-left;
    if(dd<0)chip=`<span class="chip r">Zieldatum ist vorbei</span>`;
    else if(p>0)chip=`<span class="chip g">🟢 ${p} ${p===1?"Tag":"Tage"} Puffer</span>`;
    else if(p===0)chip=`<span class="chip o">🟠 Kein Puffer: ab jetzt jeden Tag lernen</span>`;
    else chip=`<span class="chip r">🔴 ${-p} ${p===-1?"Lerntag":"Lerntage"} zu viel: Tage zusammenlegen oder kürzeren Plan wählen</span>`;}
  return `<div class="goal"><label>🎯 Alles gelernt bis <input type="date" data-goal="${k}" value="${g}" min="${new Date().toISOString().slice(0,10)}"></label>${chip}</div>`;
}
function maxRows(){
  return Math.max(0,...APPS.map(a=>{const s=st(a.k);return s.n&&s.count<s.n?s.n-nextDay(s)+1:0;}));
}
function rest(k,s){
  const M=maxRows(); if(!M)return"";
  const {days,X}=full(k), from=nextDay(s), out=[];
  for(let off=1;off<=M;off++){const t=from+off-1;
    out.push(t<=s.n?`<div class="dy" data-off="${off}"><h3>${whenLabel(off)} <small>· Tag ${t} · ⏱️ ca. ${X[t-1].min} Min.</small></h3><ul>${items(k,days[t-1],X[t-1])}</ul></div>`
      :`<div class="dy none" data-off="${off}"><h3>${whenLabel(off)}</h3><ul><li><span>–</span><span>${t===s.n+1?"Plan zu Ende":""}</span></li></ul></div>`);}
  const n=Math.max(0,s.n-from+1);
  return `<details class="rest"${UI().rest?" open":""}><summary>Restlicher Plan · noch ${n} ${n===1?"Tag":"Tage"}</summary><div class="days">${out.join("")}</div></details>`;
}
function results(k,t){
  const L=pst(k).log||{},lo=(L[t-1]&&L[t-1].end)||0,hi=(L[t]&&L[t].end)||Infinity;
  return J("lz-ergebnisse",[]).filter(r=>r.a===k&&r.u===NU.cur&&r.ts>lo&&r.ts<=hi);
}
const RES={};
function autoGrades(k,t){
  const R=results(k,t),{days,X}=full(k),lg=dlog(k,t);let ch=false;
  const has=(r,us)=>r.units.length===us.length&&us.every(u=>r.units.includes(u.id)),sup=(r,us)=>us.every(u=>r.units.includes(u.id)),TT=X[t-1].tests;
  const setG=(key,rs)=>{RES[k+"|"+t+"|"+key]=rs;if(!rs.length){if(lg.a[key]){delete lg.a[key];delete lg.g[key];delete lg.c[key];ch=true;}return;}const g=Math.min(...rs.map(r=>r.g));
    if((!lg.g[key]||lg.a[key])&&lg.g[key]!==g){lg.g[key]=g;lg.c[key]=1;lg.a[key]=1;ch=true;}};
  const wk=(r,tt)=>(r.k==="write")===(tt.kind==="Schreibtest");
  TT.forEach(tt=>{let rs=R.filter(r=>has(r,tt.units)&&wk(r,tt));
    if(!rs.length)rs=R.filter(r=>wk(r,tt)&&sup(r,tt.units)&&TT.filter(o=>o!==tt&&o.name===tt.name&&sup(r,o.units)).length===0);
    setG(tkey(tt),rs);});
  if(days[t-1].final){const U=CONF[k].units,gs=[...new Set(U.map(u=>u.group||""))];let rs=[],ok=true;
    for(const g of gs){const m=R.filter(r=>r.k!=="write"&&has(r,U.filter(u=>(u.group||"")===g)));if(!m.length){ok=false;break;}rs.push(m.reduce((a,b)=>a.g<=b.g?a:b));}
    setG("final",ok?[{g:Math.max(...rs.map(r=>r.g)),ts:Math.max(...rs.map(r=>r.ts))}]:[]);}
  if(ch)save();
}
function todo(k,s){
  autoGrades(k,Math.max(1,Math.min(curDay(s),s.n)));
  const {days,X}=full(k), t=Math.max(1,Math.min(curDay(s),s.n)), i=t-1;
  return `<ul class="todo"><li class="min"><span>⏱️</span><span>Tag ${t}: ca. ${X[i].min} Min. · abhaken und Noten eintragen</span></li>${items(k,days[i],X[i],t)}</ul>`;
}
function past(k,s){
  const last=curDay(s)-1; if(last<1)return"";
  const {days,X}=full(k), out=[];
  for(let t=last;t>=1;t--){autoGrades(k,t);out.push(`<div class="dy"><h3>Tag ${t}</h3><ul class="todo">${items(k,days[t-1],X[t-1],t)}</ul></div>`);}
  return `<details class="past"${UI()["p"+k]?" open":""} data-past="${k}"><summary>Bisherige Lerntage · ${last}</summary><div class="days">${out.join("")}</div></details>`;
}
function testBar(k){
  const s=st(k);if(!s.n)return"";const {days,X}=full(k),L=pst(k).log||{};let tot=0,ok=0;
  X.forEach((x,i)=>{const lg=L[i+1]||{g:{}};x.tests.forEach(tt=>{tot++;const g=lg.g&&lg.g[tkey(tt)];if(g&&g<=tt.goal)ok++;});
    if(days[i].final){tot++;const g=lg.g&&lg.g.final;if(g&&g<=2)ok++;}});
  return `<div class="tb"><div class="meta">Tests bestanden: <b>${ok}</b> von ${tot}</div><div class="bar tbar" aria-hidden="true"><i style="width:${tot?Math.round(100*ok/tot):0}%"></i></div></div>`;
}
function grades(k){
  {const s=st(k);for(let t=1;t<=Math.max(1,Math.min(curDay(s),s.n));t++)autoGrades(k,t);}
  const L=pst(k).log||{},out=[];
  Object.keys(L).map(Number).sort((a,b)=>a-b).forEach(t=>Object.values(L[t].g||{}).forEach(g=>{if(g)out.push(g);}));
  return out.length?`<div class="meta">Noten: <b>${out.join(" · ")}</b></div>`:"";
}
function card(a,W){
  const s=st(a.k), doneToday=s.doneDate===today(), fin=s.n&&s.count>=s.n&&!doneToday;
  let plan;
  if(!s.n){
    plan=`<div class="hint">Noch kein Lernplan. Lege fest, wie viele Lerntage es gibt und was schon sitzt.</div><div class="row"><button class="done" data-plan="${a.k}">🗓️ Lernplan einstellen</button></div>`;
  }else if(fin){
    plan=`<div class="party">🎉 Plan geschafft! Alle ${s.n} Lerntage erledigt.</div>${grades(a.k)}${past(a.k,s)}<div class="row"><button class="lnk" data-plan="${a.k}">Neuen Lernplan einstellen</button></div>`;
  }else{
    const day=doneToday?s.count:s.count+1, left=s.n-s.count;
    plan=`<div class="dayline"><b>${doneToday?"Tag "+day+" geschafft ✓":"Heute: Tag "+day+" von "+s.n}</b><span class="meta">noch <b>${left}</b> ${left===1?"Lerntag":"Lerntage"}</span></div>
      <div class="bar" aria-hidden="true"><i style="width:${Math.round(100*s.count/s.n)}%"></i></div>
      ${goalBox(a.k,s,doneToday)}
      ${grades(a.k)}${testBar(a.k)}
      ${past(a.k,s)}
      ${todo(a.k,s)}
      ${doneToday&&left?`<div class="hint">Nächster Lerntag: Tag ${day+1}.</div>`:""}
      ${W?"":rest(a.k,s)}
      <div class="row"><button class="done ${doneToday?"is":""}" data-done="${a.k}">${doneToday?"✓ Heute erledigt (rückgängig)":"Heute erledigt"}</button>
      <button class="lnk" data-plan="${a.k}">Lernplan ändern</button></div>`;
  }
  const head=`<div class="top"><div class="ico" aria-hidden="true">${a.icon}</div><div class="nm"><h2>${esc(a.name)}</h2><small>${esc(a.sub)}</small></div>
      <a class="open" href="#${a.k}" data-open="${a.k}">Öffnen</a></div>`, body=`<div class="body"><div class="meta">Zuletzt geöffnet: <b>${ago(s.last)}</b></div>${plan}</div>`;
  return W?{head,body}:`<article class="app" style="--c:var(--${a.k})">${head}${body}</article>`;
}
const WIDE=matchMedia("(min-width:1000px)");
function board(){
  const M=maxRows(), open=!!UI().rest&&M>0, P=APPS.map(a=>card(a,true));
  const R=3+(open?2*M:0), h=[];
  APPS.forEach((a,i)=>{const c=i+1,st_=`--c:var(--${a.k});grid-column:${c}`;
    h.push(`<div class="colbg" style="grid-column:${c};grid-row:1/${R+1}"></div>`,
      `<div style="${st_};grid-row:1;display:flex">${P[i].head}</div>`,`<div style="${st_};grid-row:2;display:flex">${P[i].body}</div>`);});
  if(M)h.push(`<button class="tog" style="grid-row:3" data-rest aria-expanded="${open}">${open?"Restlichen Plan zuklappen":"Restlichen Plan aufklappen"} <span aria-hidden="true">${open?"▴":"▾"}</span></button>`);
  if(open){
    const cols=APPS.map(a=>{const s=st(a.k);return s.n&&s.count<s.n?Object.assign(full(a.k),{s,from:nextDay(s)}):null;});
    for(let off=1;off<=M;off++){const r=2+2*off;
      h.push(`<div class="lbl" style="grid-row:${r}"><span>${whenLabel(off)}</span></div>`);
      APPS.forEach((a,i)=>{const c=cols[i],t=c?c.from+off-1:0,last=off===M?" last":"";
        let inner;
        if(!c)inner="";
        else if(t<=c.s.n)inner=`<div class="tg">Tag ${t} <span>· ⏱️ ca. ${c.X[t-1].min} Min.</span></div><ul>${items(a.k,c.days[t-1],c.X[t-1])}</ul>`;
        else inner=t===c.s.n+1?`<div class="tg none">Plan zu Ende</div>`:"";
        h.push(`<div class="cell${last}" style="--c:var(--${a.k});grid-column:${i+1};grid-row:${r+1}">${inner}</div>`);});
    }
  }
  return `<div class="board" style="grid-template-rows:repeat(${R},auto)">${h.join("")}</div>`;
}
let whoOpen=false,whoMode="",newEmo="👩",wDraft={name:"",e:"👩"},editId=null;
function renderWho(){
  const u=me(),P=people();
  document.getElementById("hi").textContent=u.acc||u.name!=="Ich"?"Hallo "+u.name+"!":"Hallo!";
  let h=`<button class="whob" data-who aria-expanded="${whoOpen}"><span>${u.icon}</span> ${esc(u.name)} <span aria-hidden="true">▾</span></button>`;
  if(whoOpen){
    h+=`<div class="whop">`;
    if(whoMode==="add"||whoMode==="form"){
      h+=`<div class="wt">${whoMode==="form"?"Person bearbeiten":"Neue Person"}</div><div class="addp"><input id="nuName" placeholder="Name" maxlength="20" autocomplete="off" value="${esc(wDraft.name)}"><div class="emog">${EMOG.map(([t,l])=>`<div class="emot">${t}</div><div class="emos">${l.map(e=>`<button data-emo="${e}" class="${e===wDraft.e?"on":""}" aria-label="Symbol ${e}">${e}</button>`).join("")}</div>`).join("")}</div><div class="nuerr" id="nuErr"></div><div class="row2"><button class="lnk" data-wmode="">Abbrechen</button><button class="go" data-addp>${whoMode==="form"?"Speichern":"Person anlegen"}</button></div></div>`;
    }else{
      h+=`<div class="wt">${whoMode==="edit"?"Wen möchtest du bearbeiten?":"Wer lernt gerade?"}</div><div class="tiles">${P.map(p=>`<div class="tile${p.id===u.id?" cur":""}"><button ${whoMode==="edit"?`data-editp="${p.id}"`:`data-pick="${p.id}"`}><span class="em">${p.icon}</span>${esc(p.name)}${whoMode==="edit"?'<small>✎</small>':''}</button>${whoMode==="del"&&p.id!==u.id?`<button class="x" data-delp="${p.id}" aria-label="${esc(p.name)} löschen">✕</button>`:""}</div>`).join("")}</div>`;
      h+=whoMode?`<div class="row"><button class="lnk" data-wmode="">Fertig</button></div>`:`<div class="row"><button class="lnk" data-wmode="add">＋ Neue Person</button><button class="lnk" data-wmode="edit">✎ Bearbeiten</button>${P.length>1?`<button class="lnk" data-wmode="del">Person löschen</button>`:""}</div>`;
    }
    h+=`</div>`;}
  document.getElementById("who").innerHTML=h;
}
const RKA=[["W","winkelakademie-v1",3,"📐"],["Z","wasserzauberschule-v1",3,"🪄"],["E","unit6-progress",3,"🐚"],["D","detektivbuero-v1",1,"🕵️"]];
window.RK_TAB=window.RK_TAB||"";window.RK_USER_SET=window.RK_USER_SET||false;
function rankHTML(){
  const f=n=>(+n||0).toLocaleString("de-DE"),gs=window.lzMyGroups?lzMyGroups():[];if(RK_TAB&&!gs.some(g=>g.code===RK_TAB))RK_TAB="";
  if(!RK_TAB&&!RK_USER_SET&&gs.length)RK_TAB=gs[0].code;
  const tabs=gs.length?`<div class="rk-tabs"><button type="button" class="${RK_TAB?"":"on"}" data-rk="">📱 Dieses Gerät</button>${gs.map(g=>`<button type="button" class="${RK_TAB===g.code?"on":""}" data-rk="${esc(g.code)}">👥 ${esc(g.name)}</button>`).join("")}</div>`:"";
  let rows,myId,note="";
  if(!RK_TAB){const L=people().filter(u=>u&&u.id);myId=NU.cur;
    rows=L.map(u=>{const v=RKA.map(([k,b,r])=>{const o=J(u.id==="u1"?b:b+("@"+u.id).repeat(r),null);return o&&typeof o==="object"?Math.max(0,+o.xp||0):0;});const ar=J("lz-arena-pts@"+u.id,{})||{};return{id:u.id,e:u.icon,name:u.name,v,ar:Math.max(0,+ar.p||0)};});
    if(L.length<2)note=" Leg weitere Personen an oder tritt einer Lerngruppe bei, um gegeneinander anzutreten.";}
  else{const c=window.lzGroupCache&&lzGroupCache(RK_TAB);
    if(!c||Date.now()-c.at>20000)window.lzPullGroup&&lzPullGroup(RK_TAB,true).then(()=>{const el=document.getElementById("rank");if(el&&RK_TAB)el.innerHTML=rankHTML();});
    if(!c)return `<section class="rank" aria-label="Rangliste"><h2>🏆 Rangliste</h2>${tabs}<p>⏳ Lerngruppe wird geladen …</p></section>`;
    myId=(NU.list.find(u=>u.id===NU.cur)||{}).gid;
    rows=c.members.map(m=>({id:m.gid,e:m.e,name:m.name,v:RKA.map(a=>Math.max(0,+(m.xp||{})[a[0]]||0)),ar:Math.max(0,+m.ar||0)}));
    if(rows.length<2)note=" Teile den Code der Lerngruppe, damit andere mitmachen.";}
  rows.forEach(r=>r.t=r.v.reduce((a,b)=>a+b,0));
  rows.sort((a,b)=>b.t-a.t||String(a.name).localeCompare(String(b.name)));
  const mx=RKA.map((_,i)=>Math.max(0,...rows.map(r=>r.v[i]))),mxA=Math.max(0,...rows.map(r=>r.ar));
  const med=["🥇","🥈","🥉"];let pl=0;
  const tr=rows.map((r,i)=>{if(i===0||r.t<rows[i-1].t)pl=i;const m=r.t>0?(med[pl]||(pl+1)+"."):"";
    return `<tr class="${r.id===myId?"me":""}"><td class="m">${m}</td><td class="n">${esc(r.e)} ${esc(r.name)}</td>${r.v.map((x,j)=>`<td class="${x&&x===mx[j]&&rows.length>1?"best":""}">${f(x)}</td>`).join("")}<td class="t">${f(r.t)}</td><td class="${r.ar&&r.ar===mxA&&rows.length>1?"best":""}">${f(r.ar)}</td></tr>`;}).join("");
  return `<section class="rank" aria-label="Rangliste"><h2>🏆 Rangliste</h2>${tabs}<table><thead><tr><th class="m"></th><th class="n">Name</th>${RKA.map(a=>`<th title="${esc(APPS.find(x=>x.k===a[0]).name)}">${a[3]}</th>`).join("")}<th>Gesamt</th><th title="Arena-Punkte">⚔️</th></tr></thead><tbody>${tr}</tbody></table><p>Punkte aus 📐 Winkel-Akademie, 🪄 Wasser-Zauberschule, 🐚 Küsten-Crew und 🕵️ Detektiv-Büro. Grün = Bestwert in der App. ⚔️ = Arena-Punkte aus Duellen (zählen nicht zur Gesamtsumme).${note}</p></section>`;
}
document.addEventListener("click",e=>{const b=e.target.closest&&e.target.closest("[data-rk]");if(!b)return;RK_TAB=b.dataset.rk;RK_USER_SET=true;const el=document.getElementById("rank");if(el)el.innerHTML=rankHTML();});
function render(){
  try{setTimeout(()=>{window.lzCloudStat&&lzCloudStat();window.lzAccAuto&&lzAccAuto();},0);}catch(e){}
  loadAll();document.body.classList.toggle("compact",!!UI().compact);const cb=document.getElementById("cmp");cb.textContent=UI().compact?"Alles zeigen":"Nur heute";cb.setAttribute("aria-pressed",!!UI().compact);
  renderWho();
  const d=new Date();
  document.getElementById("date").textContent=d.toLocaleDateString("de-DE",{weekday:"long",day:"numeric",month:"long"});
  const g=document.getElementById("grid");
  if(WIDE.matches){g.className="";g.innerHTML=board();}else{g.className="grid";g.innerHTML=APPS.map(a=>card(a,false)).join("");}
  try{document.getElementById("rank").innerHTML=rankHTML();}catch(e){}
  try{window.lzArenaCard&&lzArenaCard();}catch(e){}
  const act=APPS.filter(a=>{const s=st(a.k);return s.n&&s.count<s.n;});
  const open=act.filter(a=>st(a.k).doneDate!==today());
  const maxLeft=Math.max(0,...APPS.map(a=>{const s=st(a.k);return s.n?s.n-s.count:0;}));
  let t;
  if(!act.length&&!APPS.some(a=>st(a.k).n))t="Stell bei jeder App den Lernplan ein, dann steht hier, was heute dran ist.";
  else if(!act.length)t="<b>Alle Pläne geschafft.</b> Stark!";
  else if(!open.length)t=`<b>Für heute alles erledigt.</b> Noch höchstens ${maxLeft} ${maxLeft===1?"Lerntag":"Lerntage"}.`;
  else t=`<b>Heute dran:</b> ${open.map(a=>esc(a.name)).join(", ")}. Noch höchstens ${maxLeft} ${maxLeft===1?"Lerntag":"Lerntage"}.`;
  document.getElementById("sum").innerHTML=t;
}
document.addEventListener("click",e=>{
  if(e.target.closest("[data-rest]")){UI().rest=!UI().rest;save();render();return;}
  if(e.target.closest("#cmp")){UI().compact=!UI().compact;save();render();return;}
  const wb=e.target.closest("[data-who]"); if(wb){whoOpen=!whoOpen;whoMode="";renderWho();return;}
  const pu=e.target.closest("[data-pick]"); if(pu){NU.cur=pu.dataset.pick;RK_TAB="";RK_USER_SET=false;whoOpen=false;save();render();return;}
  const wm=e.target.closest("[data-wmode]"); if(wm){if(wm.dataset.wmode==="add"){whoOpen=false;whoMode="";renderWho();window.lzAccOpen&&lzAccOpen("new");return;}whoMode=wm.dataset.wmode;editId=null;if(whoMode==="add")wDraft={name:"",e:EMO[NU.list.length%EMO.length]};renderWho();return;}
  const ep=e.target.closest("[data-editp]"); if(ep){const x=NU.list.find(y=>y.id===ep.dataset.editp);if(x){editId=x.id;wDraft={name:x.name,e:x.e};whoMode="form";renderWho();}return;}
  const em=e.target.closest("[data-emo]"); if(em){const i0=document.getElementById("nuName"),g0=document.querySelector(".emog"),y=g0?g0.scrollTop:0;wDraft.name=i0?i0.value:wDraft.name;wDraft.e=em.dataset.emo;renderWho();const g1=document.querySelector(".emog");if(g1)g1.scrollTop=y;return;}
  if(e.target.closest("[data-addp]")){const inp=document.getElementById("nuName"),n=(inp.value||"").trim(),er=document.getElementById("nuErr");
    if(!n){er.textContent="Bitte einen Namen eingeben.";inp.focus();return;}
    if(NU.list.some(x=>x.id!==editId&&x.name.toLowerCase()===n.toLowerCase())){er.textContent="Diesen Namen gibt es schon.";return;}
    if(whoMode==="form"&&editId){const x=NU.list.find(y=>y.id===editId);if(x){if(!x.acc)x.name=n.slice(0,20);x.e=wDraft.e;x.t=Date.now();}editId=null;whoMode="";save();render();return;}
    NU.n=Math.max(NU.n||0,...NU.list.map(u=>+u.id.slice(1)||0),...(NU.del||[]).map(d=>+d.slice(1)||0))+1;let id="u"+(100000+Math.floor(Math.random()*899900000));while(NU.list.some(u=>u.id===id)||(NU.del||[]).includes(id))id="u"+(100000+Math.floor(Math.random()*899900000));NU.list.push({id,name:n.slice(0,20),e:wDraft.e,t:Date.now()});NU.cur=id;whoOpen=false;whoMode="";save();render();return;}
  const dp=e.target.closest("[data-delp]"); if(dp){const u=NU.list.find(x=>x.id===dp.dataset.delp);
    if(u&&confirm(u.acc?u.name+" auf diesem Gerät abmelden? Die Punkte bleiben unter dem Benutzernamen gespeichert.":u.name+" löschen? Fortschritt, Punkte und Noten dieser Person gehen in allen Apps verloren.")){try{localStorage.removeItem("lz-linked@"+u.id);}catch(_){}NU.del=[...(NU.del||[]),u.id];NU.list=NU.list.filter(x=>x!==u);save();lzPurge(u.id);renderWho();}return;}
  const o=e.target.closest("[data-open]"); if(o){st(o.dataset.open).last=Date.now();save();lzPushed=true;setTimeout(()=>showApp(o.dataset.open),0);return;}
  const pl=e.target.closest("[data-plan]"); if(pl){const k=pl.dataset.plan;st(k).last=Date.now();save();showApp(k,true);return;}
  const dn=e.target.closest("[data-done]"); if(dn){const s=st(dn.dataset.done);
    if(s.doneDate===today()){s.count=Math.max(0,s.count-1);s.doneDate="";delete dlog(dn.dataset.done,s.count+1).end;}else{s.count=Math.min(s.n,s.count+1);s.doneDate=today();dlog(dn.dataset.done,s.count).end=Date.now();}
    save();render();return;}
});
document.addEventListener("change",e=>{const g=e.target.closest("[data-goal]");if(g){st(g.dataset.goal).goal=g.value;save();render();return;}
  const c=e.target.closest("[data-chk]");if(c){const [k,t,key]=c.dataset.chk.split("|");const l=dlog(k,+t);if(c.checked)l.c[key]=1;else{delete l.c[key];delete l.g[key];}save();render();return;}
  const s=e.target.closest("[data-grade]");if(s){const [k,t,key]=s.dataset.grade.split("|");const l=dlog(k,+t);delete l.a[key];if(s.value){l.g[key]=+s.value;l.c[key]=1;}else delete l.g[key];save();render();return;}});
document.addEventListener("toggle",e=>{const d=e.target;if(d.dataset&&d.dataset.past){UI()["p"+d.dataset.past]=d.open;save();return;}
  if(!d.classList||!d.classList.contains("rest"))return;
  if(UI().rest===d.open)return;
  UI().rest=d.open;save();document.querySelectorAll("details.rest").forEach(x=>{if(x.open!==d.open)x.open=d.open;});},true);
WIDE.addEventListener("change",render);
document.addEventListener("visibilitychange",()=>{if(!document.hidden)render();});
render();

/* Offline-Modus: alle Dateien dauerhaft im Browser speichern */
if("serviceWorker" in navigator){addEventListener("load",()=>{navigator.serviceWorker.register("sw.js").catch(()=>{});});}
/* Neue Version erkennen: Tablets bleiben oft stundenlang offen und zeigen sonst noch die alte App.
   Alle 5 Minuten und beim Zurückkehren sw.js am Server nachsehen; ist VER neuer, Leiste zum Aktualisieren zeigen. */
(function(){
  const cur=((document.querySelector('script[src*="start.js"]')||{}).src||"").split("v=")[1]||"";if(!cur)return;
  let last=0,shown=false;
  async function check(){if(shown||Date.now()-last<60000)return;last=Date.now();
    try{const t=await(await fetch("sw.js?check="+Date.now(),{cache:"no-store"})).text(),m=t.match(/VER="([\d.]+)"/);
      if(m&&m[1]!==cur){shown=true;const b=document.createElement("button");b.id="lzUpd";b.type="button";
        b.innerHTML="🆕 Neue Version "+m[1]+" ist da – <u>jetzt aktualisieren</u>";
        b.style.cssText="position:fixed;left:50%;transform:translateX(-50%);bottom:calc(12px + env(safe-area-inset-bottom,0px));z-index:10000;max-width:calc(100vw - 24px);border:0;border-radius:14px;padding:12px 18px;background:#1b7f3b;color:#fff;font:800 16px/1.3 Nunito,system-ui,sans-serif;box-shadow:0 8px 24px rgba(0,0,0,.3);cursor:pointer";
        b.onclick=()=>location.reload();document.body.appendChild(b);}}catch(e){}}
  setInterval(check,300000);setTimeout(check,15000);
  document.addEventListener("visibilitychange",()=>{if(!document.hidden)check();});
  window.__lzUpdCheck=()=>{last=0;return check();};
})();
