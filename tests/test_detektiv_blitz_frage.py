"""Detektiv-Büro Blitz: Bei Konjunktions-Aufgaben steht die Konjunktions-Frage, nicht „gebeugtes Verb“."""
import asyncio,time
from harness import *
async def main():
  async with async_playwright() as pw:
    br=await pw.chromium.launch()
    c=await br.new_context(viewport={'width':1024,'height':1000}); await c.route('**/*',handle); p=await c.new_page()
    errs=[];p.on('pageerror',lambda e:errs.append(str(e)))
    await p.goto('http://app.test/#D'); await p.wait_for_timeout(2500)
    f=[fr for fr in p.frames if fr!=p.main_frame][0]
    for pk in ['p1','p2','p3','p4','p5','p6']:
      el=await f.query_selector(f'.pack[data-p="{pk}"]')
      if el and 'on' not in (await el.get_attribute('class') or ''): await el.click()
    await f.click('[data-m="blitz"]'); await p.wait_for_timeout(300)
    seen={'K':0,'V':0,'other':0};t0=time.time();last=None
    while time.time()-t0<56 and not (seen['K'] and seen['V']):
      if await f.query_selector('.result'): break
      t=await f.inner_text('#card') if await f.query_selector('#card') else ''
      if t and t!=last and await f.query_selector('#card .words.tapm'):
        last=t;head=t.split('\n')[0]
        if 'Konjunktion' in head: seen['K']+=1; assert 'gebeugtes Verb' not in head,head; await p.screenshot(path=OUTDIR+'blitz-konj.png')
        elif 'gebeugtes Verb' in head: seen['V']+=1
        else: seen['other']+=1
      b=await f.query_selector_all('#card button:not([disabled])')
      if b: await b[0].click()
      await p.wait_for_timeout(120)
    print(seen,'errors',errs); assert seen['K']>=1 and not errs
    await br.close()
asyncio.run(main())
