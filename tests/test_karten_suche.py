"""Lernkarten „Alle ansehen“: Suche in Detektiv-Büro und Wasser-Zauberschule (über alle Pakete, Treffer markiert)."""
import asyncio
from harness import *
async def main():
  async with async_playwright() as pw:
    br=await pw.chromium.launch();c=await br.new_context(viewport={'width':412,'height':900});await c.route('**/*',handle);await c.add_init_script(acct('Robin'))
    p=await c.new_page();errs=[];p.on('pageerror',lambda e:errs.append(str(e)))
    for k,fn,start,word,other in [('D','detektiv.html',"book(['p6'],'all')",'finit','xyzqq'),('Z','wasser.html',"book(['p5'],'all')",'siedetemperatur','xyzqq')]:
      await p.goto('http://app.test/#'+k);await p.wait_for_timeout(2500)
      f=[x for x in p.frames if x.url.split('?')[0].endswith(fn)][0]
      await f.click('[data-m="book"]');await p.wait_for_timeout(300);await f.click('[data-v="all"]');await p.wait_for_timeout(300)
      await f.fill('#bks',word);await p.wait_for_timeout(300)
      t=await f.inner_text('#bkl');n=len(await f.query_selector_all('#bkl mark'));print(k,t.split('\n')[0],'| marks',n)
      assert 'gefunden' in t and n>0,t[:200]
      assert await f.evaluate("document.activeElement.id")=='bks'
      await p.screenshot(path=OUTDIR+f'suche-{k}.png')
      await f.fill('#bks',other);await p.wait_for_timeout(200);assert 'Keine Karte' in await f.inner_text('#bkl')
      await f.fill('#bks','');await p.wait_for_timeout(200);assert 'gefunden' not in await f.inner_text('#bkl')
    print('errors',errs);assert not errs;await br.close()
asyncio.run(main())
