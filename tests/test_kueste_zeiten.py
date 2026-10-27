"""Küsten-Crew: Zeiten-Werkstatt (Zeit erkennen, Zeit-Detektiv, Satz umbauen, Sätze sortieren)."""
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
      await f.click('[data-ms="zeiten"]'); await p.wait_for_timeout(200)
      await p.screenshot(path=OUTDIR+f'zeiten-menu-{w}.png')
      # Zeit erkennen: alle richtig
      await f.click('[data-ze="erk"]')
      for _ in range(10):
        await f.evaluate("""()=>{const it=ZE.list[ZE.i];[...document.querySelectorAll('#zeO .option-btn')].find(b=>b.textContent.startsWith(ZE_T[it.t].n)).click();}""")
        if _==0: await p.screenshot(path=OUTDIR+f'zeiten-erk-{w}.png')
        await f.click('#zeN .btn-next')
      t=await f.inner_text('#scene'); assert '10 / 10' in t,t[:200]
      # Detektiv: alle richtig
      await f.evaluate("zeMenu()"); await f.click('[data-ze="det"]')
      for k in range(10):
        await f.evaluate("""()=>{const it=ZE.list[ZE.i],W=it.s.split(' '),sg=it.sig.split(' ').map(zeClean);W.forEach((x,i)=>{if(sg.includes(zeClean(x)))document.querySelector('.ze-w[data-i="'+i+'"]').click();});document.getElementById('zeC').click();}""")
        if k==0: await p.screenshot(path=OUTDIR+f'zeiten-det-{w}.png')
        await f.evaluate("""()=>{const it=ZE.list[ZE.i];[...document.querySelectorAll('#zeO .option-btn')].find(b=>b.textContent.startsWith(ZE_T[it.t].n)).click();}""")
        await f.click('#zeN .btn-next')
      t=await f.inner_text('#scene'); assert '10 / 10' in t,t[:200]
      # Satz umbauen: 9 richtig, einer falsch, Großschreibung/Punkt egal
      await f.evaluate("zeMenu()"); await f.click('[data-ze="um"]')
      for k in range(10):
        await f.evaluate("""(k)=>{const q=ZE.list[ZE.i],B=ZE_ROWS[q.r][ZE_K.indexOf(q.b)];const i=document.getElementById('zeI');i.value=k===0?'blabla':B[0].toUpperCase().replace(/\\./,'');document.getElementById('zeC').click();}""",k)
        if k==0: await p.screenshot(path=OUTDIR+f'zeiten-um-{w}.png')
        await f.click('#zeN .btn-next')
      t=await f.inner_text('#scene'); assert '9 / 10' in t,t[:200]
      # Sortieren: alle richtig
      await f.evaluate("zeMenu()"); await f.click('[data-ze="sort"]')
      await p.screenshot(path=OUTDIR+f'zeiten-sort-{w}.png')
      for _ in range(10):
        await f.evaluate("""()=>{const i=ZE.cards.findIndex(c=>!c.at);document.querySelector('[data-c="'+i+'"]').click();}""")
        await f.evaluate("""()=>{const i=ZE.cards.findIndex(c=>!c.at&&ZE.sel===ZE.cards.indexOf(c));const c=ZE.cards[ZE.sel];document.querySelector('[data-b="'+c.t+'"]').click();}""")
      await f.click('#zeC'); t=await f.inner_text('#scene'); assert '10 von 10 richtig' in t,t[:200]
      await p.screenshot(path=OUTDIR+f'zeiten-sort-done-{w}.png')
      print(w,'ok xp',await f.evaluate("progress.xp"),'errors',errs); assert not errs
    await br.close()
asyncio.run(main())
