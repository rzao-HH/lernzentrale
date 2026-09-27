"""Detektiv-Büro: Blitz-Ermittlung (dauert gut eine Minute)."""
import asyncio,json,random
from harness import *
async def main():
  async with async_playwright() as pw:
    br=await pw.chromium.launch()
    c=await br.new_context(viewport={'width':1024,'height':1000}); await c.route('**/*',handle); p=await c.new_page()
    errs=[];p.on('pageerror',lambda e:errs.append(str(e)))
    await p.goto('http://app.test/#D'); await p.wait_for_timeout(2500)
    f=[fr for fr in p.frames if fr!=p.main_frame][0]
    for pk in ['p2','p3','p4','p5','p6']: await f.click(f'.pack[data-p="{pk}"]')
    await f.click('[data-m="blitz"]'); await p.wait_for_timeout(300)
    shots=0;kinds=set()
    for k in range(200):
        await p.wait_for_timeout(250)
        if await f.query_selector('.result'): break
        q=await f.inner_text('#card')
        if 'Komma?' in q: kinds.add('comma')
        elif 'gebeugtes' in q: kinds.add('tap')
        else: kinds.add('mc')
        if shots<3 and kinds and ('Komma?' in q or 'gebeugtes' in q or 'Zeitform' in q):
            await p.screenshot(path=OUTDIR+f'db{shots}.png'); shots+=1
        btns=await f.query_selector_all('#card button:not([disabled])')
        if btns: await random.choice(btns).click()
    await p.wait_for_timeout(62000) if not await f.query_selector('.result') else None
    await p.screenshot(path=OUTDIR+'db-end.png')
    print(kinds, (await f.inner_text('.result'))[:150].replace('\n',' '))
    await f.click('[data-m]') if False else None
    print('errors',errs)
    await br.close()
asyncio.run(main())
