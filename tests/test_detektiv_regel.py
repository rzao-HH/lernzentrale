"""Detektiv-Büro: Zu jeder Lernkarte gibt es eine Regel-Frage; sie kommt im Regel-Check, in der Blitz-Ermittlung und im Abschlusstest vor."""
import asyncio
from harness import *
async def main():
  async with async_playwright() as pw:
    br=await pw.chromium.launch();c=await br.new_context(viewport={'width':412,'height':900});await c.route('**/*',handle);await c.add_init_script(acct('Robin'))
    p=await c.new_page();errs=[];p.on('pageerror',lambda e:errs.append(str(e)))
    await p.goto('http://app.test/#D');await p.wait_for_timeout(2500)
    f=[x for x in p.frames if x.url.split('?')[0].endswith('detektiv.html')][0]
    r=await f.evaluate("""(()=>{const I=window.__lzArena.I,out={};I.filter(i=>i.tag==='regel').forEach(i=>out[i.p]=(out[i.p]||0)+1);
      const bad=I.filter(i=>i.tag==='regel'&&(i.o.length!==4||new Set(i.o).size!==4||!i.o.includes(i.a))).length;return{out,bad};})()""")
    print(r);assert r['out']=={'p1':6,'p2':6,'p3':6,'p4':8,'p5':5,'p6':9} and r['bad']==0
    # Abschlusstest mit allen Akten: genau 3 Regel-Fragen
    n=[]
    for k in range(4):
      await p.goto('http://app.test/#D');await p.wait_for_timeout(1500);f=[x for x in p.frames if x.url.split('?')[0].endswith('detektiv.html')][0]
      await f.evaluate("lzSelect('p1,p2,p3,p4,p5,p6','test')");await f.click('[data-m="test"]');await p.wait_for_timeout(200)
      n.append(await f.evaluate("__detQs().filter(q=>q.tag==='regel').length"))
    n=min(n) if all(x==3 for x in n) else n
    print('regel im Test',n);assert n==3
    await p.goto('http://app.test/#D');await p.wait_for_timeout(2000);f=[x for x in p.frames if x.url.split('?')[0].endswith('detektiv.html')][0]
    await f.evaluate("lzSelect('p4','rep')");await f.click('[data-m="regel"]');await p.wait_for_timeout(300)
    t=' '.join((await f.inner_text('#card')).split());print(t[:160]);assert 'Regel-Check' in t
    await (await f.query_selector_all('.opt'))[0].click();await p.wait_for_timeout(300);await p.screenshot(path=OUTDIR+'regel.png')
    print('errors',errs);assert not errs;await br.close()
asyncio.run(main())
