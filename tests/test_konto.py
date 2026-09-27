"""Anmelden mit Benutzername: zwei Geräte, derselbe Name → dieselben Punkte; Lernplan pro Person."""
import asyncio,json
from harness import *
async def main():
  async with async_playwright() as pw:
    br=await pw.chromium.launch()
    A,pa,ea=await dev(br); await pa.goto('http://app.test/'); await pa.wait_for_timeout(1500)
    assert await pa.is_visible('#accOv.on'),'Anmelde-Dialog fehlt'
    await pa.screenshot(path=OUTDIR+'konto-dialog.png')
    await pa.fill('#accIn','Robin'); await pa.click('[data-acce="🦊"]'); await pa.click('[data-accgo]'); await pa.wait_for_timeout(1500)
    N=json.loads(await pa.evaluate("localStorage.getItem('nutzer-alle')")); u=N['list'][0]
    assert u['acc']=='robin' and u['name']=='Robin' and u['e']=='🦊',u
    assert ('acc:robin','profile') in DB
    await pa.evaluate("localStorage.setItem('winkelakademie-v1',JSON.stringify({xp:812}));localStorage.setItem(lpKey('W'),JSON.stringify({plan:'A'}))")
    await pa.wait_for_timeout(2500)
    assert json.loads(DB[('acc:robin','app:W')][0])['xp']==812, DB.keys()
    assert ('acc:robin','plan:W') in DB
    print('A:',await pa.inner_text('#lzsync'))
    # Gerät B: gleicher Name, andere Schreibweise
    B,pb,eb=await dev(br); await pb.emulate_media(color_scheme='dark'); await pb.goto('http://app.test/'); await pb.wait_for_timeout(1500)
    await pb.fill('#accIn','robin'); await pb.click('[data-accgo]'); await pb.wait_for_timeout(1000)
    t=await pb.inner_text('#accOv'); assert 'gibt es schon' in t,t
    await pb.screenshot(path=OUTDIR+'konto-confirm-dark.png')
    await pb.click('[data-accyes]'); await pb.wait_for_timeout(2500)
    N=json.loads(await pb.evaluate("localStorage.getItem('nutzer-alle')")); u=N['list'][0]
    assert u['name']=='Robin' and u['e']=='🦊',u
    wa=await pb.evaluate("localStorage.getItem('winkelakademie-v1')"); assert wa and json.loads(wa)['xp']==812,wa
    assert await pb.evaluate("localStorage.getItem(lpKey('W'))")=='{"plan":"A"}'
    # B sammelt Punkte → A bekommt sie
    await pb.evaluate("localStorage.setItem('winkelakademie-v1',JSON.stringify({xp:900}))"); await pb.wait_for_timeout(2500)
    await pa.evaluate("lzPull()"); await pa.wait_for_timeout(1000)
    assert json.loads(await pa.evaluate("localStorage.getItem('winkelakademie-v1')"))['xp']==900
    # zweite Person auf A: eigener Lernplan
    await pa.evaluate("lzAccOpen('new')"); await pa.fill('#accIn','Mia'); await pa.click('[data-accgo]'); await pa.wait_for_timeout(1500)
    N=json.loads(await pa.evaluate("localStorage.getItem('nutzer-alle')")); assert len(N['list'])==2 and N['list'][1]['acc']=='mia',N
    assert await pa.evaluate("localStorage.getItem(lpKey('W'))") is None,'Lernplan nicht pro Person'
    # Name schon auf diesem Gerät
    await pa.evaluate("lzAccOpen('new')"); await pa.fill('#accIn','ROBIN'); await pa.click('[data-accgo]'); await pa.wait_for_timeout(300)
    assert 'schon angemeldet' in await pa.inner_text('#accErr')
    print('errors',ea,eb)
    await br.close()
asyncio.run(main())
