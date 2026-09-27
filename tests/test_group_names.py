"""Lerngruppen: gleicher Name → eigener Anzeigename."""
import asyncio,json,random
from harness import *
async def main():
  async with async_playwright() as pw:
    br=await pw.chromium.launch()
    A,ea=await mk(br,'A',acct('Robin'))
    A.on('dialog',lambda d: asyncio.ensure_future(d.accept('Familie')))
    await A.goto('http://app.test/'); await A.wait_for_timeout(3000)
    await A.evaluate("lzGroupsOpen()"); await A.click('[data-gnew]'); await A.wait_for_timeout(800)
    code=await A.evaluate("lzMyGroups()[0].code"); await A.click('[data-gx]')
    C,ec=await mk(br,'C',acct('Robin K'))
    C.on('dialog',lambda d: asyncio.ensure_future(d.accept('Robin K.') if d.type=='prompt' else d.accept()))
    await C.goto('http://app.test/'); await C.wait_for_timeout(2500)
    await C.evaluate("lzGroupsOpen()"); await C.wait_for_timeout(1500)
    t=await C.inner_text('#grpOv'); assert 'weitere lerngruppen' in t.lower() and 'Familie' in t and 'angelegt von Robin' in t,t
    await C.screenshot(path=OUTDIR+'gr-list.png')
    await C.click('[data-gjoin="'+code+'"]'); await C.wait_for_timeout(2500)
    assert code in await C.evaluate("localStorage.getItem('lz-groups@u1')")
    print('C groups',await C.evaluate("localStorage.getItem('lz-groups@u1')"))
    await C.click('[data-gx]')
    await C.evaluate("RK_TAB=lzMyGroups()[0].code;lzPullGroup(RK_TAB,true).then(()=>document.getElementById('rank').innerHTML=rankHTML())"); await C.wait_for_timeout(1500)
    print('C rank:',(await C.inner_text('#rank'))[:160].replace('\n',' '))
    await C.click('#nwBtn'); await C.wait_for_timeout(300); await C.screenshot(path=OUTDIR+'news.png')
    print('errors',ea,ec)
    await br.close()
asyncio.run(main())
