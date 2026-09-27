"""Küsten-Crew: Startseite, Pakete und alle Missionen."""
import asyncio,json,random
from harness import *
async def main():
  async with async_playwright() as pw:
    br=await pw.chromium.launch()
    for w,h in [(1024,1366),(390,844)]:
      c=await br.new_context(viewport={'width':w,'height':h}); await c.route('**/*',handle); await c.add_init_script(acct('Robin')); p=await c.new_page()
      errs=[];p.on('pageerror',lambda e:errs.append(str(e)))
      await p.goto('http://app.test/'); await p.wait_for_timeout(600)
      await p.evaluate("location.hash='#E'"); await p.wait_for_timeout(2500)
      f=[fr for fr in p.frames if fr!=p.main_frame][0]
      await p.screenshot(path=OUTDIR+f'e-home-{w}.png',full_page=False)
      if w==1024:
        await f.click('[data-kcall="g"]'); await f.click('[data-pk="v1"]'); await p.wait_for_timeout(300)
        print('sel',await f.evaluate("JSON.stringify(progress._sel)"))
        for ms in ['flash','quiz','quiz-rev','verbs','regverbs','regirr','gaps','questions','detect','rule','duel','falcon','race','gduel','test','gtest','story']:
          await f.click(f'[data-ms="{ms}"]'); await p.wait_for_timeout(400)
          home=await f.evaluate("document.body.classList.contains('kc-home')")
          txt=(await f.inner_text('#scene'))[:70].replace('\n',' | ')
          print(ms,'home' if home else 'mission','::',txt)
          if ms=='quiz':
            # answer correct
            await f.evaluate("""()=>{const w=deck[idx];const b=[...document.querySelectorAll('.option-btn')].find(x=>x.textContent.trim()===w.de.trim());if(b)b.click();}""")
            print('  xp after quiz',await f.evaluate("progress.xp"))
          if ms=='gaps':
            await f.evaluate("""()=>{const it=gDeck[gIdx];document.getElementById('gIn1').value=it.a;document.getElementById('gCheck').click();}""")
            print('  xp after gap',await f.evaluate("progress.xp"),await f.evaluate("JSON.stringify(progress._st)"))
          await f.click('#kcBack'); await p.wait_for_timeout(200)
        await p.evaluate("lzHome()"); await p.wait_for_timeout(800)
        print(await p.inner_text('#rank'))
      print(w,'errors',errs)
    await br.close()
asyncio.run(main())
