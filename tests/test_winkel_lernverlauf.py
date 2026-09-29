"""Winkel-Akademie, Checkliste: Lernverlauf (Tendenz, Verlaufskurve), „lange nicht geübt“, Aufgaben-Mission je Aufgabenart
mit gezieltem Üben, und Abbrüche (erfasst beim Verlassen einer Übung, angezeigt in Details und Elternübersicht)."""
import asyncio
from harness import *
SEED="""(()=>{if(localStorage.getItem('winkelakademie-v1'))return;
const D=n=>{const d=new Date(Date.now()-n*864e5);return d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0');};
const now=Date.now(),vl={};
vl['p5|task']={n:20,ok:12,ms:0,mn:0,h:[1,1,0,1,1,0,1,1,1,0],err:{'t|Kurs bestimmen':4},t:now,d:{[D(20)]:[10,4],[D(0)]:[10,8]},
  sub:{t5kurs:{l:'Kurs bestimmen',n:6,ok:1,h:[0,0,1,0,0,0]},t5dreh:{l:'Drehung am Kompass',n:10,ok:9,h:[1,1,1,1,1,1,1,1,1,0]}}};
vl['p1|measure']={n:20,ok:19,ms:0,mn:0,h:[1,1,1,1,1,1,1,1,1,1],err:{},t:now-10*864e5,d:{[D(10)]:[20,19]}};
localStorage.setItem('winkelakademie-v1',JSON.stringify({xp:500,sel:['p1'],diff:'leicht',sound:false,stats:{},high:{},grades:{},cl:{},vl,ab:{konstr:{s:4,a:3,w:2}}}));})();"""
async def main():
  async with async_playwright() as pw:
    br=await pw.chromium.launch();c=await br.new_context(viewport={'width':412,'height':900});await c.route('**/*',handle)
    await c.add_init_script(acct('Robin'));await c.add_init_script(SEED)
    p=await c.new_page();errs=[];p.on('pageerror',lambda e:errs.append(str(e)))
    await p.goto('http://app.test/#W');await p.wait_for_timeout(1500)
    f=[x for x in p.frames if x.url.split('?')[0].endswith('winkel.html')][0]
    await f.click('#clOpen');await p.wait_for_timeout(300)
    J=lambda t:' '.join(t.split())
    # Kompass (Paket 5): Tendenz, Verlaufskurve, Aufgabenarten-Tabelle, gezielte Empfehlung
    await f.click('.cl-det[data-id="k0"]>summary');k0=J(await f.inner_text('.cl-det[data-id="k0"]'))
    assert 'besser geworden' in k0 and 'früher 40 %' in k0,k0
    assert 'Kurs bestimmen' in k0 and 'Drehung am Kompass' in k0 and 'Gezielt' in k0,k0
    assert await f.query_selector('.cl-det[data-id="k0"] svg.cl-spark rect'),'Verlaufskurve fehlt'
    # Messen: sitzt, aber seit 10 Tagen nicht geübt -> Auffrischen
    await f.click('.cl-det[data-id="k2"]>summary');k2=J(await f.inner_text('.cl-det[data-id="k2"]'))
    assert 'lange nicht geübt' in k2 and 'vor 10 Tagen' in k2 and 'Auffrischen' in k2,k2
    # Konstruieren: oft abgebrochen
    await f.click('.cl-det[data-id="k3"]>summary');k3=J(await f.inner_text('.cl-det[data-id="k3"]'))
    assert '3 von 4 Mal' in k3,k3
    # Elternübersicht: Rhythmus, Tendenz, lange nicht geübt, Abbrüche
    await f.click('.cl-par>summary');pt=J(await f.inner_text('.cl-par'))
    for w in ['Übungsrhythmus','besser geworden','lange nicht geübt','Oft vorzeitig beendet']:assert w in pt,(w,pt)
    await p.screenshot(path=OUTDIR+'checkliste-lernverlauf.png')
    # Gezielt üben: startet die Aufgaben-Mission nur mit „Kurs bestimmen“
    await f.click('.cl-det[data-id="k0"] .cl-vgo[data-vf="t5kurs"]');await p.wait_for_timeout(400)
    assert 'gezielt' in await f.inner_text('.gtitle')
    asks=set()
    for i in range(3):
      asks.add(J(await f.inner_text('.ask')))
      await f.evaluate("(()=>{const b=document.querySelector('.tbtn');if(b)b.click();else{const n=document.querySelector('.numpad [data-n=\"1\"]');n.click();document.querySelector('.numpad [data-n=\"ok\"]').click();}})()")
      await p.wait_for_timeout(300);w=await f.query_selector('#weiter')
      if w:await w.click();await p.wait_for_timeout(200)
    S=await f.evaluate("JSON.parse(localStorage.getItem('winkelakademie-v1'))")
    assert S['vl']['p5|task']['sub']['t5kurs']['n']>=8,S['vl']['p5|task']['sub']
    # Abbruch: nach Antworten zurück -> gezählt
    await f.click('#back');await p.wait_for_timeout(200)
    S=await f.evaluate("JSON.parse(localStorage.getItem('winkelakademie-v1'))")
    assert S['ab']['task']['a']==1 and S['ab']['task']['s']==1,S['ab']
    print('errors',errs);assert not errs;await br.close()
asyncio.run(main())
