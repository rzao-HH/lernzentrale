"""Arena: Geister-Duell im selben Haushalt."""
import asyncio,json,random
from harness import *
async def main():
  async with async_playwright() as pw:
    br=await pw.chromium.launch()
    A,ea=await mk(br,'A',acct('Robin'))
    await A.goto('http://app.test/'); await A.wait_for_timeout(2500)
    await A.evaluate("""()=>{const N=JSON.parse(localStorage.getItem('nutzer-alle'));N.list.push({id:'u777777',name:'Roya',e:'🦉',acc:'roya',gid:'roya',t:Date.now()});localStorage.setItem('nutzer-alle',JSON.stringify(N));}""")
    await A.reload(); await A.wait_for_timeout(2500)
    await A.evaluate("lzArenaOpen()"); await A.wait_for_timeout(300)
    await A.click('[data-am="E"]'); await A.click('[data-ghost]')
    await A.wait_for_timeout(5000)
    await play(A,12,True); await play(A,3,False)
    # wait for time out? force: play until end or 125s
    for k in range(40):
        g=await A.evaluate("(()=>{const G=__arenaGame();return G&&!G.over})()")
        if not g: break
        await play(A,5,True)
    print('A rec end:',(await A.inner_text('#arenaOv'))[:160].replace('\n',' '))
    await A.wait_for_timeout(2500)
    # device B: Roya mit ihrem Benutzernamen angemeldet
    B,eb=await mk(br,'B',acct('Roya','🦉','u777777'))
    await B.goto('http://app.test/'); await B.wait_for_timeout(4000)
    print('B card:',(await B.inner_text('#arena'))[:160].replace('\n',' '))
    await B.evaluate("lzArenaOpen()"); await B.wait_for_timeout(300)
    await B.screenshot(path=OUTDIR+'gh-pick.png')
    await B.click('[data-gplay]'); await B.wait_for_timeout(4500)
    await B.screenshot(path=OUTDIR+'gh-game.png')
    for k in range(40):
        g=await B.evaluate("(()=>{const G=__arenaGame();return G&&!G.over})()")
        if not g: break
        await play(B,3,True)
    print('B end:',(await B.inner_text('#arenaOv'))[:200].replace('\n',' '))
    await B.wait_for_timeout(3000)
    await A.reload(); await A.wait_for_timeout(4000)
    print('A card after:',(await A.inner_text('#arena'))[:160].replace('\n',' '))
    await A.evaluate("lzArenaOpen()"); await A.wait_for_timeout(300)
    await A.click('[data-gseen]'); await A.wait_for_timeout(300)
    print('pts A',await A.evaluate("localStorage.getItem('lz-arena-pts@u1')"),'B',await B.evaluate("localStorage.getItem('lz-arena-pts@u777777')"))
    print('errors',ea,eb)
    await br.close()
asyncio.run(main())
