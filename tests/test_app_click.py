"""Öffnen-Knopf auf der Startseite: App erscheint sofort (vorher blieb sie leer bis zum Neuladen). NWT: ein Forscherlabor, Test-Namen eindeutig."""
import asyncio,os
from harness import *
async def main():
  async with async_playwright() as pw:
    br=await pw.chromium.launch()
    c=await br.new_context(viewport={'width':1024,'height':800},service_workers='allow'); await c.route('**/*',handle)
    await c.add_init_script(acct('Robin'))
    p=await c.new_page(); errs=[]; p.on('pageerror',lambda e:errs.append(str(e)))
    await p.goto('http://app.test/'); await p.wait_for_timeout(2500)
    for k in ['W','Z','E','D']:
        await p.click(f'[data-open="{k}"]'); await p.wait_for_timeout(2500)
        f=await (await p.query_selector('#appv iframe.on')).content_frame()
        n=await f.evaluate("document.body.innerText.length"); print(k,f.url[-30:],n); assert n>500,(k,f.url)
        await p.evaluate("history.back()"); await p.wait_for_timeout(800)
    await p.click('[data-open="Z"]'); await p.wait_for_timeout(1500)
    f=await (await p.query_selector('#appv iframe.on')).content_frame()
    for pk in ['p2','p3','p4']:
        el=await f.query_selector(f'[data-p="{pk}"]')
        if el: await el.click()
    names=await f.evaluate("[...document.querySelectorAll('.mode')].map(b=>b.innerText.split('\\n').map(x=>x.trim()).filter(Boolean)[1])"); print(names)
    assert names.count('Forscherlabor')==1 and 'Experimentier-Werkstatt' not in names and 'Zauberprüfung' in names and names.count('Abschlusstest')==1,names
    await f.click('[data-m="werk"]'); await p.wait_for_timeout(500)
    st=await f.evaluate("[...document.querySelectorAll('.mxbig b')].map(b=>b.innerText)"); print(st); assert len(st)==6,st
    await f.click('#wkpred'); await p.wait_for_timeout(800); assert await f.query_selector('#card'),'Versuchsreihe'
    await p.screenshot(path=OUTDIR+'z-labor.png')
    print('errors',errs); await br.close()
asyncio.run(main())
