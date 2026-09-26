/* Aktuelle Person für die App bestimmen (vor dem App-Code) */
(function(){
  var K="nutzer-alle", P=null;
  try{P=JSON.parse(localStorage.getItem(K)||"null");}catch(e){}
  if(!P||!P.list||!P.list.length)P={list:[{id:"u1",name:"Robin",e:"🧒"}],cur:"u1",n:1};
  if(!P.list.some(function(u){return u.id===P.cur;}))P.cur=P.list[0].id;
  window.__NUTZER=P; window.__UK=P.cur==="u1"?"":"@"+P.cur;
})();
