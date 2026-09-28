"""📄-Knopf: Wasser, Detektiv und Küste verlinken ihre Lernzettel-Dateien (Englisch mit Auswahl), Winkel verlinkt mathe-winkel.html;
die Kopfleiste passt auch auf ein schmales Handy (390/360 px)."""
import asyncio, os
from harness import *
ROOT=os.environ.get('LZ_ROOT',os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
async def main():
  async with async_playwright() as pw:
    br=await pw.chromium.launch()
    for vw in (1024,390,360):
      c=await br.new_context(viewport={'width':vw,'height':900}); await c.route('**/*',handle); await c.add_init_script(acct('Robin'))
      p=await c.new_page(); errs=[]; p.on('pageerror',lambda e:errs.append(str(e)))
      for k,fn,files in [('Z','wasser.html',['nwt-wasser.html']),('D','detektiv.html',['deutsch-satzbau-zeitformen.html']),('E','kueste.html',['englisch-unit5-6.html','englisch-simple-past.html']),('W','winkel.html',['mathe-winkel.html'])]:
        await p.goto('http://app.test/#'+k); await p.wait_for_timeout(2500)
        f=[x for x in p.frames if x!=p.main_frame and x.url.split('?')[0].endswith(fn)][0]
        b=await f.query_selector('.zettel-btn')
        if not files: assert b is None,k; continue
        assert b,k
        if len(files)==1:
          h=await b.get_attribute('href'); assert h=='../lernzettel/'+files[0] and await b.get_attribute('target')=='_blank',h
        else:
          await b.click(); await p.wait_for_timeout(300)
          hs=[await a.get_attribute('href') for a in await f.query_selector_all('.zettel-menu a')]
          assert hs==['../lernzettel/'+x for x in files],hs
          await p.screenshot(path=OUTDIR+f'zettel-menu-{vw}.png')
          await f.click('body',position={'x':5,'y':600}); await p.wait_for_timeout(200)
          assert await f.query_selector('.zettel-menu') is None
        for x in files: assert os.path.exists(os.path.join(ROOT,'lernzettel',x)),x
        over=await f.evaluate("document.documentElement.scrollWidth-document.documentElement.clientWidth"); assert over<=1,(k,vw,over)
        r=await f.evaluate("Math.round(Math.max(...[...document.querySelectorAll('.home-btn,.icon-btn,.lp-btn,#soundBtn')].map(e=>e.getBoundingClientRect().right)))"); assert r<=vw,(k,vw,r)
        await p.screenshot(path=OUTDIR+f'zettel-{k}-{vw}.png')
      print(vw,'errors',errs); assert not errs
      await c.close()
    await br.close()
asyncio.run(main())
