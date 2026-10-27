"""Arena (Geister-Duell, Deutsch): Frage passt zur Antwort – Konjunktionen werden nicht als „gebeugtes Verb“ abgefragt."""
import asyncio
from harness import *
async def main():
  async with async_playwright() as pw:
    br=await pw.chromium.launch()
    A,ea=await mk(br,'A',acct('Robin'))
    await A.goto('http://app.test/'); await A.wait_for_timeout(2500)
    await A.evaluate("""()=>{const N=JSON.parse(localStorage.getItem('nutzer-alle'));N.list.push({id:'u777777',name:'Roya',e:'🦉',acc:'roya',gid:'roya',t:Date.now()});localStorage.setItem('nutzer-alle',JSON.stringify(N));}""")
    await A.reload(); await A.wait_for_timeout(2500)
    await A.evaluate("location.hash='#D'"); await A.wait_for_timeout(2500)
    fr=[x for x in A.frames if x!=A.main_frame][-1]
    for pk in ['p3','p4']:
      el=await fr.query_selector(f'.pack[data-p="{pk}"]')
      if el and 'on' not in (await el.get_attribute('class') or ''): await el.click()
    await A.evaluate("lzHome()"); await A.wait_for_timeout(800)
    await A.evaluate("lzArenaOpen()"); await A.wait_for_timeout(300)
    await A.click('[data-am="D"]'); await A.click('[data-ghost]')
    await A.wait_for_timeout(4000)
    qs=await A.evaluate("(()=>{const G=__arenaGame();return G?G.qs.map(q=>({q:q.q,a:q.a,s:q.s})):[]})()")
    print(len(qs),'Fragen'); assert qs
    CONJ={'obwohl','sodass','weil','dass','damit','nachdem','bevor','wenn','als','da','während','seit','wie','wo','und','aber','oder','denn','doch','ob','bis','dass','indem','falls','sobald','obwohl'}
    nv=nk=0
    for q in qs:
      if 'gebeugtes Verb' in q['q']: nv+=1; assert q['a'].lower() not in CONJ,q
      if 'die Konjunktion, die die Teilsätze' in q['q']: nk+=1
    print('Verb-Fragen',nv,'Konjunktions-Fragen',nk,'errors',ea); assert not ea and nv and nk
    await br.close()
asyncio.run(main())
