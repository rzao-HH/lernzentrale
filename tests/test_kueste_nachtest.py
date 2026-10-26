"""Küsten-Crew: Nachschreibtest Simple Past (7 Varianten, Note, PDF-Links)."""
import asyncio,os
from harness import *
async def main():
  async with async_playwright() as pw:
    br=await pw.chromium.launch()
    c=await br.new_context(viewport={'width':1024,'height':1366}); await c.route('**/*',handle); await c.add_init_script(acct('Robin')); p=await c.new_page()
    errs=[];p.on('pageerror',lambda e:errs.append(str(e)))
    await p.goto('http://app.test/'); await p.wait_for_timeout(600)
    await p.evaluate("location.hash='#E'"); await p.wait_for_timeout(2500)
    f=[fr for fr in p.frames if fr!=p.main_frame][0]
    await f.click('[data-ms="nach"]'); await p.wait_for_timeout(300)
    assert await f.evaluate("document.querySelectorAll('#nxVs [data-v]').length")==8
    links=await f.evaluate("[...document.querySelectorAll('#scene a')].map(a=>a.getAttribute('href'))")
    print('links',links)
    root=os.path.join(os.path.dirname(__file__),'..','nachtest')
    for l in links: assert os.path.exists(os.path.join(root,os.path.basename(l))),l
    await p.screenshot(path=OUTDIR+'nach-intro.png')
    for v in range(8):
      await f.click(f'#nxVs [data-v="{v}"]'); await p.wait_for_timeout(150)
      await f.click('#nxGo')
      # alle richtig, Teil 3 absichtlich 2 falsch
      for s in range(3):
        await f.evaluate("""(s)=>{document.querySelectorAll('.nx-in').forEach((el,i)=>{let sol=NX.sec[NX.s].items[i].sol;if(NX.s===2&&i<2)sol='wrong';el.value=sol;el.dispatchEvent(new Event('input'));});}""",s)
        await f.click('#nxS' if s==2 else '#nxW')
      await p.wait_for_timeout(200)
      t=(await f.inner_text('#scene'))
      assert 'Note 1' in t and '28 von 30' in t,(v,t[:200])
      await f.click('#kcAgainB'); await p.wait_for_timeout(100)
    await f.evaluate("nxStart(0)")
    await f.click('#nxGo'); 
    await f.evaluate("document.querySelectorAll('.nx-in').forEach((el,i)=>{el.value=NX.sec[0].items[i].sol.toUpperCase();el.dispatchEvent(new Event('input'));})")
    await f.click('#nxW'); await f.click('#nxW'); p.once('dialog',lambda d:asyncio.ensure_future(d.accept())); await f.click('#nxS'); await p.wait_for_timeout(200)
    print((await f.inner_text('#scene'))[:120].replace('\n',' | '))
    await p.screenshot(path=OUTDIR+'nach-result.png')
    print('errors',errs); assert not errs
    await br.close()
asyncio.run(main())
