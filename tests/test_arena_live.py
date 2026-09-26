"""Arena: Live-Tauziehen zwischen zwei Geräten."""
import asyncio,json,random
from harness import *
async def main():
  async with async_playwright() as pw:
    br=await pw.chromium.launch()
    A,ea=await mk(br,'A',"localStorage.setItem('lz-fam','familie-test-1234');")
    B,eb=await mk(br,'B',"if(!localStorage.getItem('nutzer-alle'))localStorage.setItem('nutzer-alle',JSON.stringify({list:[{id:'u1',name:'Robin',e:'🧒'},{id:'u777777',name:'Roya',e:'🦉',t:1}],cur:'u777777',n:777777}));localStorage.setItem('lz-fam','familie-test-1234');")
    await A.goto('http://app.test/'); await B.goto('http://app.test/#W')
    await A.wait_for_timeout(5000)
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
