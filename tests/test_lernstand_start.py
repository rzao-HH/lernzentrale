"""Punkte nach Lernstand: Beim ersten Öffnen übernimmt jedes Paket einmalig eine Stufe aus dem bisherigen Fortschritt
(Lernziel/Trefferquote/Testnote) – Bekanntes gilt sofort als „kannst du schon“, Ungeübtes bleibt „neu“. Nach „Lernplan zurücksetzen“ keine erneute Übernahme."""
import asyncio,json
from harness import *
SEED=acct('Robin')+"""if(!localStorage.getItem('seeded')){localStorage.setItem('seeded','1');const N=Date.now();
localStorage.setItem('winkelakademie-v1',JSON.stringify({xp:900,sel:['p1'],sound:false,stats:{p1:{h:Array(20).fill(1),done:true},p2:{h:[1,1,1,1,1,1,1,1,1,1,1,1,0,0],done:false},p3:{h:[1,0,0],done:false}},grades:{'p4+p5':2}}));
localStorage.setItem('detektivbuero-v1',JSON.stringify({xp:300,sel:['p1'],sound:false,stats:{p3:[1,1,1,1,1,1,1,1,0,0,0,0]},bk:{},grades:{}}));
localStorage.setItem('lz-ergebnisse',JSON.stringify([{a:'D',u:'u1',units:['p4'],g:2,k:'',d:'x',ts:N-5e8},{a:'E',u:'u1',units:['g0'],g:3,k:'',d:'x',ts:N-5e8}]));
const P0={};const VI=['cut','draw','drink','forget','freeze','let','put','say','send','sing'],pr={xp:200,_sel:['v0'],_mute:true,_st:{g2:Array(18).fill(1)},irr:{},_ls:{_start:N-1e8}};VI.forEach((v,i)=>{pr[v]=i<9?2:0;});
localStorage.setItem('unit6-progress',JSON.stringify(pr));}"""
J=lambda f,k:f.evaluate("k=>JSON.parse(localStorage.getItem(k)||'null')",k)
def fr(p,name): return [x for x in p.frames if x!=p.main_frame and x.url.split('?')[0].endswith(name)][-1]
async def main():
  async with async_playwright() as pw:
    br=await pw.chromium.launch()
    c=await br.new_context(viewport={'width':1024,'height':900}); await c.route('**/*',handle); await c.add_init_script(SEED)
    p=await c.new_page(); errs=[]; p.on('pageerror',lambda e:errs.append(str(e)))
    await p.goto('http://app.test/#W'); await p.wait_for_timeout(2500); f=fr(p,'winkel.html')
    w=(await J(f,'winkelakademie-v1'))['ls']; print('W',{k:(v['s'] if isinstance(v,dict) else 'start') for k,v in w.items()})
    assert w['p1']['s']==3 and w['p2']['s']==3 and w['p3']['s']==1 and w['p4']['s']==3 and w['p5']['s']==3 and 'p6' not in w and w['_start']
    t1=await f.inner_text('.pack[data-p="p1"] .ls-tile'); t6=await f.inner_text('.pack[data-p="p6"] .ls-tile'); print(t1.replace('\n',' '),'|',t6.replace('\n',' '))
    assert 'kannst du schon' in t1 and 'Wenig Punkte' in t1 and 'neu' in t6
    assert (await J(f,'winkelakademie-v1'))['xp']==900,'Punkte unverändert'
    await p.screenshot(path=OUTDIR+'ls-start-winkel.png')
    # zweites Öffnen: nichts wird erneut übernommen
    await f.evaluate("(()=>{const o=JSON.parse(localStorage.getItem('winkelakademie-v1'));delete o.ls.p1;localStorage.setItem('winkelakademie-v1',JSON.stringify(o));})()")
    await f.evaluate("location.reload()"); await p.wait_for_timeout(2500); f=fr(p,'winkel.html')
    assert 'p1' not in (await J(f,'winkelakademie-v1'))['ls'],'nur einmal übernehmen'
    await p.evaluate("lzHome()"); await p.wait_for_timeout(400); await p.evaluate("location.hash='#D'"); await p.wait_for_timeout(2500); f=fr(p,'detektiv.html')
    d=(await J(f,'detektivbuero-v1'))['ls']; print('D',d); assert d['p3']['s']==2 and d['p4']['s']==3 and 'p1' not in d
    await p.evaluate("lzHome()"); await p.wait_for_timeout(400); await p.evaluate("location.hash='#E'"); await p.wait_for_timeout(3000); f=fr(p,'kueste.html')
    e=(await J(f,'unit6-progress'))['_ls']; print('E',{k:(v['s'] if isinstance(v,dict) else 'start') for k,v in e.items()})
    assert e['g2']['s']==2 or e['g2']['s']==3; assert e['i0']['s']==3,'mit Karten geübte Verben 1–10 → kannst du schon'
    assert e['i1']['s']==2 and e['i3']['s']==2 and 'i4' not in e and 'v0' not in e
    # „Karten“ mit Verben zählen jetzt für den Fortschrittsbalken des Verben-Pakets
    await f.evaluate("kcSetSel(['i5']);kcStart('flash')"); await p.wait_for_timeout(400)
    for k in range(10):
        b=await f.query_selector('#btnKnow')
        if not b: break
        await b.click(); await p.wait_for_timeout(80)
    await f.evaluate("kcShowHome()"); await p.wait_for_timeout(300)
    st=(await J(f,'unit6-progress')).get('_st',{}).get('i5',[]); print('i5 Treffer',st); assert len(st)>=8 and all(st)
    # Lernplan zurücksetzen (Detektiv) → keine erneute Übernahme aus alten Testnoten
    await p.evaluate("lzHome()"); await p.wait_for_timeout(400); await p.evaluate("location.hash='#D'"); await p.wait_for_timeout(2500); f=fr(p,'detektiv.html')
    await f.evaluate("lzResetProgress()"); await f.evaluate("location.reload()"); await p.wait_for_timeout(2500); f=fr(p,'detektiv.html')
    d=(await J(f,'detektivbuero-v1'))['ls']; print('D nach Reset',d); assert set(d)<={'_start','_sv'},d
    print('errors',errs); assert not errs,errs
    await br.close()
asyncio.run(main())
