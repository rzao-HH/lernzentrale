"""Küsten-Crew: 10er-Verbpakete + Mission Verben-Karten; alte Auswahl g0/g1 wird umgerechnet."""
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
      await f.evaluate("kcSetSel(['g0']);kcShowHome()")
      assert await f.evaluate("JSON.stringify(kcSel())")=='["i0","i1","i2","i3"]'
      assert await f.evaluate("kcHas('g0')") and not await f.evaluate("kcHas('g1')")
      assert await f.evaluate("ilVerbs().length")==40
      await f.evaluate("kcSetSel(['i7']);kcShowHome()")
      assert await f.evaluate("ilVerbs().length")==7
      names=await f.evaluate("[...document.querySelectorAll('[data-pk^=i]')].map(b=>b.querySelector('b').textContent)")
      print(names); assert len(names)==8 and '71–77' in names[7] and '1–10' in names[0]
      await f.evaluate("kcSetSel(['i0']);kcShowHome()")
      assert await f.evaluate("ilVerbs().map(v=>v.inf).sort().join()")=='cut,draw,drink,forget,freeze,let,put,say,send,sing'
      await f.evaluate("kcSetSel(['i0','i1']);kcShowHome()")
      await p.screenshot(path=OUTDIR+f'karten-home-{w}.png')
      await f.click('[data-ms="irrcards"]'); await p.wait_for_timeout(200)
      await f.click('#icGo'); await p.wait_for_timeout(200)
      n=await f.evaluate("IC.q.length"); assert n==16,n
      await f.click('#flipCard'); await p.screenshot(path=OUTDIR+f'karten-card-{w}.png')
      # erste Karte "nochmal", dann alle gewusst
      v0=await f.evaluate("IC.q[0].v.inf")
      await f.click('#icAg'); assert await f.evaluate("IC.q.length")==16
      for _ in range(16): await f.click('#icKn')
      t=await f.inner_text('#scene'); assert 'gleich gewusst' in t,t[:200]
      assert '7 von 8' in t, t[:100]
      await p.screenshot(path=OUTDIR+f'karten-end-{w}.png')
      assert await f.evaluate("progress.irr['%s'].b"%v0)==0
      # Verbformen nutzt nur gewählte Pakete
      await f.evaluate("kcSetSel(['i1']);kcShowHome()")
      assert await f.evaluate("kcPool('verbs').every(v=>VK.indexOf(v)>=10&&VK.indexOf(v)<20)")
      print(w,'ok errors',errs); assert not errs
    await br.close()
asyncio.run(main())
