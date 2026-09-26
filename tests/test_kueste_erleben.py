"""Küsten-Crew: Café, Verhör, Schatzkarte, Hör-Kapitän, Schreibtest komplett durchspielen."""
import asyncio,json,random
from harness import *
CLICK_CORRECT="""(sol)=>{const b=[...document.querySelectorAll('.option-btn:not([disabled])')].find(x=>x.textContent===sol);if(b){b.click();return true;}return false;}"""
async def main():
  async with async_playwright() as pw:
    br=await pw.chromium.launch()
    c=await br.new_context(viewport={'width':1024,'height':1366}); await c.route('**/*',handle); p=await c.new_page()
    errs=[];p.on('pageerror',lambda e:errs.append(str(e)))
    await p.goto('http://app.test/#E'); await p.wait_for_timeout(2500)
    f=[fr for fr in p.frames if fr!=p.main_frame][0]
    f.on=None
    await f.click('[data-kcall="g"]'); await f.click('[data-kcall="v"]')
    await p.screenshot(path=OUTDIR+'e10-home.png',full_page=True)
    # CAFE
    await f.click('[data-ms="cafe"]'); await p.wait_for_timeout(300)
    await p.screenshot(path=OUTDIR+'e10-cafe1.png')
    for step in range(40):
        html=await f.inner_text('#scene')
        if 'Feierabend' in html: break
        if await f.query_selector('#cfPayB'):
            tot=await f.evaluate("CF.orders[CF.c].a.p+(CF.orders[CF.c].b?CF.orders[CF.c].b.p:0)")
            n=0
            while n<tot:
                await f.click('[data-c="10"]'); n+=10
            if step==3: await p.screenshot(path=OUTDIR+'e10-cafe-pay.png')
            await f.click('#cfPayB')
        else:
            opts=await f.evaluate("[...document.querySelectorAll('.option-btn')].map(b=>b.textContent)")
            await f.evaluate("()=>{document.querySelectorAll('.option-btn')[0].click();}")
        await p.wait_for_timeout(50)
        nb=await f.query_selector('.btn-next')
        if nb: await nb.click()
        await p.wait_for_timeout(50)
    print('cafe end:',(await f.inner_text('#scene'))[:120].replace('\n',' '))
    await f.click('#kcHomeB')
    # VERHOER
    await f.click('[data-ms="verhoer"]'); await f.click('#vhGo')
    await p.wait_for_timeout(100); await p.screenshot(path=OUTDIR+'e10-vh-room.png')
    for s in range(3):
      for q in range(3):
        await f.click(f'[data-s="{s}"]') if q==0 else None
        await f.evaluate("()=>{const qs=VH.c.sus;}")
        await f.evaluate("""()=>{const b=[...document.querySelectorAll('.option-btn')];b[0].click();}""")
        if s==0 and q==1: await p.screenshot(path=OUTDIR+'e10-vh-q.png')
        await f.click('.btn-next')
    await p.screenshot(path=OUTDIR+'e10-vh-notes.png',full_page=True)
    await f.click('#vhSolve')
    for q in range(3):
        await f.evaluate("()=>{document.querySelectorAll('.option-btn')[0].click();}"); await f.click('.btn-next')
    await f.click('[data-t="1"]')
    print('vh end:',(await f.inner_text('#scene'))[:200].replace('\n',' '))
    await f.click('#kcHomeB')
    # MAP
    await f.click('[data-ms="map"]'); await p.wait_for_timeout(100); await p.screenshot(path=OUTDIR+'e10-map.png')
    for k in range(40):
        t=await f.inner_text('#scene')
        if 'Schatz gefunden' in t: break
        if await f.query_selector('[data-pl]:not([disabled])'):
            tid=await f.evaluate("MP.route[MP.i].id"); await f.click(f'[data-pl="{tid}"]')
        elif await f.query_selector('#mpI'):
            await f.fill('#mpI','xx'); await f.click('#mpC'); await f.click('.btn-next')
        else:
            await f.evaluate("()=>{document.querySelectorAll('.option-btn')[0].click();}"); await f.click('.btn-next')
    print('map end:',(await f.inner_text('#scene'))[:100].replace('\n',' '))
    await f.click('#kcHomeB')
    # HEAR
    await f.click('[data-ms="hear"]'); await p.wait_for_timeout(300); await p.screenshot(path=OUTDIR+'e10-hear.png')
    for k in range(10):
        if await f.query_selector('#hkI'): await f.fill('#hkI','abc'); await f.click('#hkC')
        else: await f.evaluate("()=>{document.querySelectorAll('.option-btn')[0].click();}")
        await f.click('.btn-next')
    print('hear end:',(await f.inner_text('#scene'))[:80].replace('\n',' '))
    await f.click('#kcHomeB')
    # WRITE
    await f.click('[data-ms="write"]'); await f.click('[data-n="3"]'); await f.click('#wtGo')
    await f.fill('#wtA','Yesterday I went to the beach.'); await f.click('#wtW')
    await p.screenshot(path=OUTDIR+'e10-write.png')
    await f.click('#wtW'); await f.evaluate("window.confirm=()=>true"); await f.click('#wtS')
    await f.evaluate("()=>{document.querySelectorAll('[data-v]').forEach(b=>{if(b.dataset.v==='0.5')b.click();});}")
    await f.evaluate("()=>{document.querySelectorAll('[data-v]').forEach(b=>{if(b.dataset.v==='0.5')b.click();});}")
    await p.screenshot(path=OUTDIR+'e10-self.png',full_page=True)
    await f.click('#wtCalc')
    print('write end:',(await f.inner_text('#scene'))[:120].replace('\n',' '))
    print('xp',await f.evaluate("progress.xp"),'erg',await f.evaluate("localStorage.getItem('lz-ergebnisse')"))
    print('errors',errs)
    await br.close()
asyncio.run(main())
