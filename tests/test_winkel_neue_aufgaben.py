"""Winkel-Akademie: neue Aufgaben nach Abgleich mit den Lernzetteln – Punkt einzeichnen, Weg mit Kurs, links/rechts herum,
Winkel an Parallelen, Winkel in Figuren messen, Parallele im Abstand, Rechteck ergänzen. Richtig und falsch lösen, keine Fehler."""
import asyncio
from harness import *
CASES=[('p5','t5punkt','tap'),('p5','t5weg','tap'),('p5','t5gleich','mc'),('p7','t7parallel','num'),('p7','t7figur','num'),('p8','t8abstand','tap'),('p8','t8rechteck','tap')]
async def main():
  async with async_playwright() as pw:
    br=await pw.chromium.launch();c=await br.new_context(viewport={'width':412,'height':900});await c.route('**/*',handle);await c.add_init_script(acct('Robin'))
    p=await c.new_page();errs=[];p.on('pageerror',lambda e:errs.append(str(e)))
    await p.goto('http://app.test/#W');await p.wait_for_timeout(2500)
    f=[x for x in p.frames if x.url.split('?')[0].endswith('winkel.html')][0]
    for pk,fn,kind in CASES:
      for right in (True,False):
        await f.evaluate(f"window.__wkForce='{fn}';lzSelect('{pk}','rep')");await f.click('[data-m="task"]');await p.wait_for_timeout(500)
        q=' '.join((await f.inner_text('#app')).split())
        if kind=='mc':
          btn=await f.query_selector_all('.tbtn');await btn[0].click()
        elif kind=='num':
          for ch in ('9','9'):await f.click(f'button:text-is("{ch}")')
          await f.click('button:text-is("OK")')
        else:
          svg=await f.query_selector('#stage svg');bb=await svg.bounding_box()
          await p.mouse.click(bb['x']+bb['width']*(0.5 if right else 0.2),bb['y']+bb['height']*(0.5 if right else 0.8))
          await p.wait_for_timeout(200);await f.click('#done')
        await p.wait_for_timeout(500);fb=' '.join((await f.inner_text('#app')).split())
        assert ('Leider' in fb) or ('richtig' in fb.lower()) or ('Genau' in fb) or ('Fast' in fb) or any(x in fb for x in ['Treffer','Stark','Volltreffer','Perfekt','Mission erfüllt']),(fn,fb[-300:])
        await p.screenshot(path=OUTDIR+f'neu-{fn}-{int(right)}.png')
        print(fn,right,'|',q[q.find('/ 10')+4:][:110])
        await f.click('#lb, .back, [aria-label="Zurück zur Übersicht"]') if await f.query_selector('#lb') else None
        await p.goto('http://app.test/#W');await p.wait_for_timeout(1500);f=[x for x in p.frames if x.url.split('?')[0].endswith('winkel.html')][0]
    # Logik: Parallelen-Winkel sind immer t oder 180-t, und Nebenwinkel ergänzen sich zu 180
    bad=await f.evaluate('''(()=>{let bad=[];for(let i=0;i<300;i++){const q=__wkTasks.t7parallel();if(q.opts)continue;const m=q.ask.match(/Winkel (\\d) = (\\d+)°/);const g=+m[2];if(!(q.ans===g||q.ans===180-g))bad.push(q.ask);}
      for(let i=0;i<200;i++){const q=__wkTasks.t8rechteck();const w=q.want;if(w[0]<0||w[0]>8||w[1]<0||w[1]>6)bad.push('rect '+w);}
      for(let i=0;i<200;i++){const q=__wkTasks.t5weg();const w=q.want;if(!w||w[0]<0||w[0]>8||w[1]<0||w[1]>6)bad.push('weg '+w);}return bad;})()''')
    print('logik',bad[:3]);assert not bad
    print('errors',errs);assert not errs
    await br.close()
asyncio.run(main())
