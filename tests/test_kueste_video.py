"""Küsten-Crew: Mission „Erklärvideo“ (unter Lernen) öffnet videos/zeitreise-krabbi.html in neuem Tab; die Seite startet, zeigt 9 Szenen und läuft ohne Fehler weiter."""
import asyncio, os
from harness import *
ROOT=os.environ.get('LZ_ROOT',os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
async def main():
  async with async_playwright() as pw:
    br=await pw.chromium.launch()
    for vw in (1024,390):
      c=await br.new_context(viewport={'width':vw,'height':900}); await c.route('**/*',handle); await c.add_init_script(acct('Robin'))
      p=await c.new_page(); errs=[]; p.on('pageerror',lambda e:errs.append(str(e)))
      await p.goto('http://app.test/#E'); await p.wait_for_timeout(2500)
      f=[x for x in p.frames if x!=p.main_frame and x.url.split('?')[0].endswith('kueste.html')][0]
      b=await f.query_selector('[data-ms="video"]'); assert b,'Mission fehlt'
      assert 'Lernen' in await f.evaluate("e=>{let n=e.parentElement.previousElementSibling;return n?n.textContent:''}",b)
      async with c.expect_page() as pi:
        await b.click()
      v=await pi.value; verrs=[]; v.on('pageerror',lambda e:verrs.append(str(e)) if 'localStorage' not in str(e) else None)  # about:blank des Popups: Test-Seed kann dort nicht schreiben
      await v.wait_for_load_state(); await v.wait_for_timeout(1500)
      assert v.url.endswith('/videos/zeitreise-krabbi.html'),v.url
      assert await v.locator('.scene').count()==9
      assert await v.locator('.scene.active').count()==1
      assert (await v.inner_text('#say')).startswith('Hi, ich bin Krabbi')
      await v.click('#next'); await v.wait_for_timeout(700)
      assert 'Szene 2 von 9' in await v.inner_text('#where')
      await v.click('#play'); await v.wait_for_timeout(300)   # Pause
      assert (await v.inner_text('#playlabel'))=='Weiter'
      for i in range(7): await v.click('#next')
      await v.wait_for_timeout(900)
      assert 'Szene 9 von 9' in await v.inner_text('#where')
      over=await v.evaluate("document.documentElement.scrollWidth-document.documentElement.clientWidth"); assert over<=1,(vw,over)
      await v.screenshot(path=OUTDIR+f'video-{vw}.png')
      print(vw,'errors',errs+verrs); assert not errs and not verrs
      await c.close()
    await br.close()
asyncio.run(main())
