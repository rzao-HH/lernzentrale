"""Lernzettel-Bezug: Pakete nennen ihren Lernzettel, Deutsch-Karten haben eine Zusatz-Erklärung,
Satz-Baumeister akzeptiert vertauschte Teile bei „und/noch“."""
import asyncio
from harness import *
async def main():
  async with async_playwright() as pw:
    br=await pw.chromium.launch()
    c=await br.new_context(viewport={'width':1024,'height':1000}); await c.route('**/*',handle); await c.add_init_script(acct('Robin'))
    p=await c.new_page(); errs=[]; p.on('pageerror',lambda e:errs.append(str(e)))
    for k,sel in [('D','.pack .psrc'),('Z','.pack .psrc'),('W','.pack .psrc'),('E','#kcHome .kc-fx')]:
        await p.goto('http://app.test/#'+k); await p.wait_for_timeout(2500)
        f=[x for x in p.frames if x!=p.main_frame and x.url.split('?')[0].endswith({'D':'detektiv.html','Z':'wasser.html','W':'winkel.html','E':'kueste.html'}[k])][0]
        t=' | '.join([await e.inner_text() for e in await f.query_selector_all(sel) if '📄' in await e.inner_text()]); print(k,t[:160]); assert '📄' in t,k
    await p.goto('http://app.test/#D'); await p.wait_for_timeout(2500)
    f=[x for x in p.frames if x.url.split('?')[0].endswith('detektiv.html')][0]
    # Zusatz-Erklärung auf der Karten-Rückseite, Karte wächst mit
    if not await f.query_selector('.pack.on[data-p="p1"]'): await f.click('.pack[data-p="p1"]')
    await f.click('[data-m="book"]'); await p.wait_for_timeout(400)
    await f.click('#bkc'); await p.wait_for_timeout(600)
    ex=await f.inner_text('.fcb .fex'); print('ex:',ex[:90]); assert len(ex)>20
    over=await f.evaluate("(()=>{const b=document.querySelector('.fcb');return b.scrollHeight-b.clientHeight})()"); assert over<=2,over
    await p.screenshot(path=OUTDIR+'d-card-ex.png')
    # vertauschte Reihenfolge
    v=await f.evaluate("orderVariants(['es gibt kein Wasser und keine Luft'])"); assert 'es gibt keine Luft und kein Wasser' in v,v
    print('errors',errs); assert not errs
    await br.close()
asyncio.run(main())
