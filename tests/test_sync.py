"""Geräte-Abgleich: zwei Geräte, Personen und Punkte wandern mit."""
import asyncio,json,random
from harness import *
async def main():
  async with async_playwright() as pw:
    br=await pw.chromium.launch()
    A,pa,ea=await dev(br); await pa.goto('http://app.test/'); await pa.wait_for_timeout(800)
    print('A stat0:',await pa.inner_text('#lzsync'))
    # A: rename u1 via storage + progress
    await pa.evaluate("""()=>{const N=JSON.parse(localStorage.getItem('nutzer-alle'));N.list[0].name='Rob';N.list[0].e='🦊';N.list[0].t=Date.now();localStorage.setItem('nutzer-alle',JSON.stringify(N));localStorage.setItem('winkelakademie-v1',JSON.stringify({xp:812}));}""")
    await pa.evaluate("localStorage.setItem('lz-fam','familie-test-1234')"); await pa.reload(); await pa.wait_for_timeout(2500)
    print('A stat:',await pa.inner_text('#lzsync')); print('DB keys:',sorted(k for f,k in DB))
    B,pb,eb=await dev(br)
    await pb.goto('http://app.test/#fam=familie-test-1234'); await pb.wait_for_timeout(2500)
    nb=await pb.evaluate("localStorage.getItem('nutzer-alle')"); print('B nutzer:',nb)
    print('B wa:',await pb.evaluate("localStorage.getItem('winkelakademie-v1')"))
    print('B shows Rob:', await pb.inner_text('body'))
    # B adds person and changes xp
    await pb.evaluate("""()=>{const N=JSON.parse(localStorage.getItem('nutzer-alle'));N.list.push({id:'u55555',name:'Roya',e:'🦉',t:Date.now()});localStorage.setItem('nutzer-alle',JSON.stringify(N));localStorage.setItem('winkelakademie-v1',JSON.stringify({xp:900}));}""")
    await pb.wait_for_timeout(2500)
    await pa.evaluate("lzPull()"); await pa.wait_for_timeout(1000)
    print('A nutzer:',await pa.evaluate("localStorage.getItem('nutzer-alle')"))
    print('A wa:',await pa.evaluate("localStorage.getItem('winkelakademie-v1')"))
    await pa.reload(); await pa.wait_for_timeout(1500)
    print('A after reload wa:',await pa.evaluate("localStorage.getItem('winkelakademie-v1')"),'cur',json.loads(await pa.evaluate("localStorage.getItem('nutzer-alle')"))['cur'])
    print('errors',ea,eb)
    await br.close()
asyncio.run(main())
