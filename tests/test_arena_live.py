"""Arena: Live-Tauziehen zwischen zwei Geräten."""
import asyncio,json,random
from harness import *
async def main():
  async with async_playwright() as pw:
    br=await pw.chromium.launch()
    A,ea=await mk(br,'A',acct('Robin'))
    B,eb=await mk(br,'B',acct('Roya','🦉','u777777'))
    # Live-Duelle gibt es innerhalb einer Lerngruppe: A legt „Familie“ an, B tritt per Link bei
    A.on('dialog',lambda d: asyncio.ensure_future(d.accept('Familie')))
    B.on('dialog',lambda d: asyncio.ensure_future(d.accept()))
    await A.goto('http://app.test/'); await A.wait_for_timeout(2500)
    await A.evaluate("lzGroupsOpen()"); await A.click('[data-gnew]'); await A.wait_for_timeout(800)
    code=await A.inner_text('.gr-code'); await A.click('[data-gx]')
    await B.goto('http://app.test/#join='+code); await B.wait_for_timeout(3500); await B.click('[data-gx]')
    await B.goto('http://app.test/#W'); await A.wait_for_timeout(5000)
    print('A card:',(await A.inner_text('#arena'))[:120].replace('\n',' '))
    await A.evaluate("lzArenaOpen()"); await A.wait_for_timeout(300)
    await A.screenshot(path=OUTDIR+'ar-pick.png')
    await A.click('[data-live]'); 
    await B.wait_for_timeout(9000)
    await B.screenshot(path=OUTDIR+'ar-inv.png')
    await B.click('[data-acc]'); await A.wait_for_timeout(4500)
    await A.screenshot(path=OUTDIR+'ar-game.png')
    await asyncio.gather(play(A,30,True),play(B,6,False))
    await A.wait_for_timeout(800)
    await A.screenshot(path=OUTDIR+'ar-endA.png'); await B.screenshot(path=OUTDIR+'ar-endB.png')
    print('A end:',(await A.inner_text('#arenaOv'))[:150].replace('\n',' '))
    print('B end:',(await B.inner_text('#arenaOv'))[:150].replace('\n',' '))
    print('pts A',await A.evaluate("localStorage.getItem('lz-arena-pts@u1')"),'B',await B.evaluate("localStorage.getItem('lz-arena-pts@u777777')"))
    print('errors',ea,eb)
    await br.close()
asyncio.run(main())
