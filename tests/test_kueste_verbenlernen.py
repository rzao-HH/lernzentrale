"""Küsten-Crew: Unregelmäßige Verben lernen (Ansehen → Mit Hilfe → Ohne Hilfe, Wiederholung falscher Verben)."""
import asyncio
from harness import *
async def main():
  async with async_playwright() as pw:
    br=await pw.chromium.launch()
    for w in (1024,390):
      c=await br.new_context(viewport={'width':w,'height':1000}); await c.route('**/*',handle); await c.add_init_script(acct('Robin')); p=await c.new_page()
      errs=[];p.on('pageerror',lambda e:errs.append(str(e)))
      await p.goto('http://app.test/'); await p.wait_for_timeout(500)
      await p.evaluate("location.hash='#E'"); await p.wait_for_timeout(2200)
      f=[fr for fr in p.frames if fr!=p.main_frame][-1]
      await f.evaluate("kcSetSel(['g0','g1']);kcShowHome()")
      await f.click('[data-ms="irrlern"]'); await p.wait_for_timeout(200)
      await p.screenshot(path=OUTDIR+f'irr-intro-{w}.png')
      await f.click('#ilGo'); await p.wait_for_timeout(200)
      pk1=await f.evaluate("IL.pk.map(v=>v.inf)"); print('Paket1',pk1); assert len(pk1)==5
      await p.screenshot(path=OUTDIR+f'irr-look-{w}.png')
      await f.click('#ilNext')
      for k in range(10):
        await f.evaluate("""()=>{const it=IL.items[IL.i],c=it.k==='past'?it.v.past:it.v.pp;[...document.querySelectorAll('#ilO .option-btn')].find(b=>b.textContent===c).click();}""")
        if k==0: await p.screenshot(path=OUTDIR+f'irr-help-{w}.png')
        await f.click('#ilN .btn-next')
      await p.screenshot(path=OUTDIR+f'irr-type-{w}.png')
      # ohne Hilfe: 4 richtig, 1 falsch
      await f.evaluate("""()=>{document.querySelectorAll('.il-in').forEach(i=>{const v=IL.pk[+i.dataset.v];i.value=(IL.pk.indexOf(v)===0)?'xxx':(i.dataset.k==='past'?v.past:v.pp);});}""")
      await f.click('#ilC'); await p.wait_for_timeout(200)
      t=await f.inner_text('#scene'); assert '4 von 5' in t,t[:150]
      await p.screenshot(path=OUTDIR+f'irr-result-{w}.png')
      rec=await f.evaluate("JSON.stringify(progress.irr)"); print(rec)
      bad=pk1[0]
      await f.click('#ilAgain'); pk2=await f.evaluate("IL.pk.map(v=>v.inf)"); print('Paket2',pk2)
      assert bad in pk2, 'falsches Verb kommt zuerst wieder'
      assert len(set(pk2)-set(pk1))>=3, 'neue Verben dabei'
      print(w,'ok errors',errs); assert not errs
    await br.close()
asyncio.run(main())
