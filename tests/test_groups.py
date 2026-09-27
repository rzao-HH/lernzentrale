"""Lerngruppen: anlegen, per Link beitreten, Rangliste, Geister-Duell über die Gruppe."""
import asyncio,json,random
from harness import *
async def main():
  async with async_playwright() as pw:
    br=await pw.chromium.launch()
    A,ea=await mk(br,'A',acct('Robin'))
    A.on('dialog',lambda d: asyncio.ensure_future(d.accept('Klasse 6b')))
    await A.goto('http://app.test/'); await A.wait_for_timeout(3000)
    await A.evaluate("lzGroupsOpen()"); await A.click('[data-gnew]'); await A.wait_for_timeout(800)
    code=await A.evaluate("lzMyGroups()[0].code"); print('code',code)
    await A.screenshot(path=OUTDIR+'gr-created.png')
    await A.click('[data-gx]')
    C,ec=await mk(br,'C',acct('Mia','🐱')+"localStorage.setItem('winkelakademie-v1',JSON.stringify({xp:333}));")
    C.on('dialog',lambda d: asyncio.ensure_future(d.accept()))
    await C.goto('http://app.test/#join='+code); await C.wait_for_timeout(3500)
    print('C groups',await C.evaluate("localStorage.getItem('lz-groups@u1')"))
    await C.click('[data-gx]'); await C.reload(); await C.wait_for_timeout(2500)
    tabs=await C.evaluate("[...document.querySelectorAll('.rk-tabs button')].map(b=>b.innerText)"); print('tabs',tabs); assert any('Klasse 6b' in x for x in tabs),'Lerngruppen-Reiter fehlt nach Neuladen'
    ontab=await C.evaluate("document.querySelector('.rk-tabs button.on')?.innerText||''"); print('default tab',ontab)
    assert 'Klasse 6b' in ontab,'Lerngruppe sollte standardmäßig aktiv sein, nicht \"Dieses Gerät\": '+ontab
    await C.evaluate('lzGroupsOpen()'); await C.wait_for_timeout(500)
    await C.click('[data-gx]'); await C.wait_for_timeout(500)
    await A.evaluate("RK_TAB=lzMyGroups()[0].code;lzPullGroup(RK_TAB,true).then(()=>document.getElementById('rank').innerHTML=rankHTML())"); await A.wait_for_timeout(1500)
    print('A rank group:',(await A.inner_text('#rank'))[:200].replace('\n',' '))
    await A.screenshot(path=OUTDIR+'gr-rank.png',full_page=True)
    await A.goto('http://app.test/leer.html'); await C.wait_for_timeout(4000)  # Robin geht offline (leere Seite, gleicher Ursprung)
    # C ghost-challenges Robin via group
    await C.evaluate("__arenaIn({type:'presence',list:[]})"); await C.evaluate("lzArenaOpen()"); await C.wait_for_timeout(2500)
    await C.evaluate("lzArenaOpen()"); await C.wait_for_timeout(300)
    await C.screenshot(path=OUTDIR+'gr-pick.png')
    await C.click('[data-am="W"]'); await C.click('[data-ghost]'); await C.wait_for_timeout(4500)
    for k in range(40):
        g=await C.evaluate("(()=>{const G=__arenaGame();return G&&!G.over})()")
        if not g: break
        await play(C,4,True)
    print('C rec:',(await C.inner_text('#arenaOv'))[:120].replace('\n',' '))
    await C.click('[data-ax]')
    await A.goto('http://app.test/'); await A.wait_for_timeout(5000)
    print('A card:',(await A.inner_text('#arena'))[:160].replace('\n',' '))
    await A.evaluate("lzArenaOpen()"); await A.wait_for_timeout(300)
    await A.click('[data-gplay]'); await A.wait_for_timeout(4500)
    for k in range(40):
        g=await A.evaluate("(()=>{const G=__arenaGame();return G&&!G.over})()")
        if not g: break
        await play(A,2,True)
    print('A end:',(await A.inner_text('#arenaOv'))[:160].replace('\n',' '))
    await C.reload(); await C.wait_for_timeout(5000)
    print('C card:',(await C.inner_text('#arena'))[:160].replace('\n',' '))
    print('errors',ea,ec)
    await br.close()
asyncio.run(main())
