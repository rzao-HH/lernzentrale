"""Lernplan-Karte in Winkel-Akademie, Wasser-Zauberschule und Detektiv-Büro:
„Diese Pakete wählen“ (jetzt „📦 Pakete auswählen“) wählt nur die Pakete aus,
springt nicht mehr zu den Übungen, markiert stattdessen den passenden Modus
mit dickem Rahmen und zeigt am Knopf selbst, dass er schon geklickt wurde."""
import asyncio
from harness import *

APPS=[("W","lernplan-winkel"),("Z","lernplan-wasser"),("D","lernplan-deutsch")]

async def check(br,prefix,key):
    c=await br.new_context(viewport={'width':1024,'height':1000}); await c.route('**/*',handle)
    await c.add_init_script(acct('Robin')+f"localStorage.setItem('{key}@u1',JSON.stringify({{n:5,done:[],today:1,ok:[]}}));")
    p=await c.new_page(); errs=[]; p.on('pageerror',lambda e:errs.append(str(e)))
    await p.goto(f'http://app.test/#{prefix}'); await p.wait_for_timeout(3000)
    f=[x for x in p.frames if x!=p.main_frame][0]
    btns=await f.query_selector_all('.lzh-btn'); assert btns,f"{prefix}: keine Lernplan-Knöpfe gefunden"
    lab0=(await btns[0].inner_text()).strip(); assert lab0=='📦 Pakete auswählen',(prefix,lab0)
    y0=await p.evaluate("window.scrollY")
    await btns[0].click(); await p.wait_for_timeout(500)
    y1=await p.evaluate("window.scrollY")
    assert abs(y1-y0)<40,f"{prefix}: Seite ist trotzdem zu den Übungen gesprungen ({y0} -> {y1})"
    hl=await f.query_selector_all('.mode.hl'); assert len(hl)>0,f"{prefix}: kein markierter Modus nach Paket-Auswahl"
    labs=[(await b.inner_text()).strip() for b in await f.query_selector_all('.lzh-btn')]
    assert labs[0].startswith('✓'),f"{prefix}: Knopf zeigt nicht 'schon geklickt' ({labs})"
    assert sum(x.startswith('✓') for x in labs)==1,f"{prefix}: mehr als ein Knopf als geklickt markiert ({labs})"
    # Übung starten und zurück: Markierung bleibt
    await hl[0].click(); await p.wait_for_timeout(600)
    p.on('dialog',lambda d: asyncio.ensure_future(d.accept()))
    await f.locator('#back:visible, #lb:visible').first.click(); await p.wait_for_timeout(500)
    hl2=await f.query_selector_all('.mode.hl'); assert len(hl2)>0,f"{prefix}: Markierung nach der Übung verschwunden"
    # Pakete von Hand ändern: Markierung und Haken verschwinden
    await f.click('.pack:not(.on)'); await p.wait_for_timeout(300)
    assert not await f.query_selector_all('.mode.hl'),f"{prefix}: Markierung bleibt trotz geänderter Auswahl"
    assert not (await f.inner_text('.lzh-btn')).strip().startswith('✓'),f"{prefix}: Haken bleibt trotz geänderter Auswahl"
    print(prefix,'ok — hl:',len(hl),'labels:',labs)
    print(prefix,'errors',errs)
    await c.close()

async def main():
    async with async_playwright() as pw:
        br=await pw.chromium.launch()
        for prefix,key in APPS:
            await check(br,prefix,key)
        await br.close()
asyncio.run(main())
