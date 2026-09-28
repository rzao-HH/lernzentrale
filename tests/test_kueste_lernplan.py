"""Küsten-Crew: Lernplan-Karte auf der Übersicht wie in den anderen Apps, „Diese Pakete wählen“ wählt die Pakete aus."""
import asyncio,json
from harness import *
async def main():
  async with async_playwright() as pw:
    br=await pw.chromium.launch()
    c=await br.new_context(viewport={'width':1024,'height':1000}); await c.route('**/*',handle)
    await c.add_init_script(acct('Robin')+"localStorage.setItem('lernplan-englisch@u1',JSON.stringify({n:5,done:[],today:1,ok:[]}));")
    p=await c.new_page(); errs=[]; p.on('pageerror',lambda e:errs.append(str(e)))
    await p.goto('http://app.test/#E'); await p.wait_for_timeout(3000)
    f=[x for x in p.frames if x!=p.main_frame][0]
    t=await f.inner_text('#kcLz'); print('card:',t[:120].replace('\n',' ')); assert 'Laut Lernplan heute' in t
    btns=await f.query_selector_all('#kcLz .lzh-btn'); labs=[(await b.inner_text()).strip() for b in btns]; assert labs and all(x=='📦 Pakete auswählen' for x in labs),labs
    await btns[0].click(); await p.wait_for_timeout(800)
    sel=await f.evaluate("kcSel()"); print('sel',sel); assert len(sel)>1
    hl=await f.query_selector_all('#kcHome .kc-ms.hl'); print('hl count',len(hl)); assert len(hl)>0,'kein markierter Modus nach Paket-Auswahl'
    lab2=await f.inner_text('#kcLz .lzh-btn'); print('label after click',lab2); assert '✓' in lab2,'Knopf zeigt nicht, dass er schon geklickt wurde'
    await p.screenshot(path=OUTDIR+'kc-lernplan.png')
    print('errors',errs); await br.close()
asyncio.run(main())
