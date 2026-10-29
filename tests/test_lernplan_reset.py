"""Lernplan zurücksetzen: löscht Lernplan + Lernfortschritt nur im jeweiligen Fach; Punkte, Abzeichen (Rang) und andere Fächer bleiben."""
import asyncio,json,time
from harness import *
OLD=int(time.time()*1000)-86400000
SEED=acct('Robin')+"""if(!localStorage.getItem('seeded')){localStorage.setItem('seeded','1');
const P={n:5,done:['p1'],today:3,ok:[1,2]};
['winkel','wasser','englisch','deutsch'].forEach(x=>localStorage.setItem('lernplan-'+x+'@u1',JSON.stringify(P)));
['W','Z','E','D'].forEach(x=>localStorage.setItem('lzp-'+x+'@u1',JSON.stringify({count:2,doneDate:'',log:{1:{c:{learn:1},g:{},end:1},2:{c:{},g:{},end:2}}})));
localStorage.setItem('winkelakademie-v1',JSON.stringify({xp:640,sel:['p1'],stats:{p1:{h:[1,1,1],done:true}},grades:{'p1':1},high:{'p1':90},cl:{'1':'1.10.'},vl:{'p1|art':{n:3}},ab:{x:{s:1,a:0,w:0}},self:{a:{v:1}},note:{a:{t:'?'}},konOk:4}));
localStorage.setItem('wasserzauberschule-v1',JSON.stringify({xp:300,house:'h1',sel:['p1'],stats:{p1:{h:[1,1],done:true}},grades:{p1:2},wgrades:{p1:2},bk:{'p1:0':2},werk:{'a:1':1},mixm:{m1:1},high:{p1:50}}));
localStorage.setItem('unit6-progress',JSON.stringify({xp:210,_sel:['v1'],_mute:true,_st:{v1:[1,1]},'house':3,'river':2}));
localStorage.setItem('detektivbuero-v1',JSON.stringify({xp:120,sel:['p2'],stats:{p1:[1,1,1]},grades:{p1:1},bk:{'p1:0':2},seen:{a:1},seenN:1,high:{x:5}}));
localStorage.setItem('lz-ergebnisse',JSON.stringify([{a:'W',u:'u1',units:['p1'],g:1,k:'',d:'x',ts:%d},{a:'Z',u:'u1',units:['p1'],g:1,k:'',d:'x',ts:%d}]));
localStorage.setItem('lernzentrale-v1',JSON.stringify({mig2:1,W:{goal:'2026-12-01',last:0},Z:{goal:'2026-12-02',last:0}}));}
"""%(OLD,OLD)
J=lambda f,k:f.evaluate("k=>JSON.parse(localStorage.getItem(k)||'null')",k)
async def frame(p,k):
    await p.goto('http://app.test/#'+k); await p.wait_for_timeout(2500)
    return [x for x in p.frames if x!=p.main_frame and x.url.split('?')[0].endswith(APP[k])][0]
APP={'W':'winkel.html','Z':'wasser.html','E':'kueste.html','D':'detektiv.html'}
async def reset_via_ui(p,f,k,shot):
    await f.click('#lpBtn'); await p.wait_for_timeout(400)
    # Im Plan-Reiter (Standard bei vorhandenem Plan) steht der Knopf unten
    assert await f.query_selector('#lpRstGo'),'Knopf fehlt im Plan'
    await f.click('#lpRstGo'); await p.wait_for_timeout(300)
    txt=await f.inner_text('#lpRst'); assert 'Wirklich' in txt and 'Punkte' in txt,txt
    await p.screenshot(path=OUTDIR+shot+'-frage.png')
    # Abbrechen lässt alles stehen
    await f.click('#lpRstNo'); await p.wait_for_timeout(300)
    assert (await J(f,LPK[k]))['n']==5,'Abbrechen hat gelöscht'
    await f.click('#lpRstGo'); await p.wait_for_timeout(200)
    async with f.expect_navigation(): await f.click('#lpRstYes')
    await p.wait_for_timeout(1500)
    f=[x for x in p.frames if x!=p.main_frame and x.url.split('?')[0].endswith(APP[k])][0]
    assert await f.evaluate("document.getElementById('lp').classList.contains('open')"),'Lernplan nicht wieder geöffnet'
    assert 'Zurückgesetzt' in await f.inner_text('#lpBody')
    sel=await f.evaluate("document.querySelector('.lp-tab[aria-selected=\"true\"]').dataset.t"); assert sel=='set',sel
    await p.screenshot(path=OUTDIR+shot+'-danach.png')
    return f
LPK={'W':'lernplan-winkel@u1','Z':'lernplan-wasser@u1','E':'lernplan-englisch@u1','D':'lernplan-deutsch@u1'}
async def main():
  async with async_playwright() as pw:
    br=await pw.chromium.launch()
    c=await br.new_context(viewport={'width':1024,'height':900}); await c.route('**/*',handle)
    await c.add_init_script(SEED)
    p=await c.new_page(); errs=[]; p.on('pageerror',lambda e:errs.append(str(e)))
    # --- Winkel-Akademie über die Oberfläche
    f=await frame(p,'W'); f=await reset_via_ui(p,f,'W','reset-winkel')
    w=await J(f,'winkelakademie-v1'); print('W',w)
    assert w['xp']==640 and w['high']=={'p1':90} and w['sel']==['p1'],'Punkte/Rekorde/Auswahl verloren'
    assert w['stats']=={} and w['grades']=={} and w['cl']=={} and w['vl']=={} and w['self']=={} and w['note']=={} and w['konOk']==0
    assert (await J(f,'lernplan-winkel@u1'))['n']==0
    z=await J(f,'lzp-W@u1'); assert z['count']==0 and z['log']['0']['end']>OLD,z
    for k in ['Z','E','D']: assert (await J(f,LPK[k]))['n']==5,'anderes Fach betroffen: '+k
    assert (await J(f,'lzp-Z@u1'))['count']==2
    assert len(await J(f,'lz-ergebnisse'))==2,'Testergebnisse gelöscht'
    # Lernplan-Leiste in der App zählt alte Testnote nicht mehr: neuen Plan anlegen
    await f.click('#lpGo'); await p.wait_for_timeout(400)
    T=await f.evaluate("lzToday()"); assert T['t']==1 and all(not x['best'] for x in T['tests']),T['tests']
    # Startseite: Zieldatum des Fachs weg, anderes bleibt; Rangliste-Punkte bleiben
    await p.evaluate("lzHome()"); await p.wait_for_timeout(800)
    st=await J(p,'lernzentrale-v1'); assert st['W']['goal']=='' and st['Z']['goal']=='2026-12-02',st
    # --- die anderen drei Fächer über die Oberfläche
    for k in ['Z','E','D']:
        f=await frame(p,k); f=await reset_via_ui(p,f,k,'reset-'+k)
    z=await J(f,'wasserzauberschule-v1'); print('Z',z)
    assert z['xp']==300 and z['house']=='h1' and z['high']=={'p1':50}
    assert z['stats']=={} and z['grades']=={} and z['wgrades']=={} and z['bk']=={} and z['werk']=={} and z['mixm']=={} and z['rst']>OLD
    e=await J(f,'unit6-progress'); print('E',e); assert {k:v for k,v in e.items() if k!='_ls'}=={'xp':210,'_sel':['v1'],'_mute':True} and list(e.get('_ls',{}))==['_start'],e
    d=await J(f,'detektivbuero-v1'); print('D',d)
    assert d['xp']==120 and d['seen']=={'a':1} and d['high']=={'x':5} and d['stats']=={} and d['grades']=={} and d['bk']=={}
    # Wasser: Paket-Noten aus alten Testergebnissen nicht mehr angezeigt
    await p.evaluate("lzHome()"); await p.wait_for_timeout(600)
    await p.evaluate("location.hash='#Z'"); await p.wait_for_timeout(2500)
    f=[x for x in p.frames if x!=p.main_frame and x.url.split('?')[0].endswith('wasser.html')][-1]
    print('pkgs',len(await f.query_selector_all('.pkgs')),errs)
    assert not await f.query_selector('.pkg.ok'),'alte Noten noch sichtbar'
    print('errors',errs); assert not errs
    await br.close()
asyncio.run(main())
