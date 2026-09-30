"""Detektiv-Büro: neue Aufgabentypen von den Lernzetteln (Wörter streichen Nr. 36, Satzgrenzen Nr. 39, Nebensatz nach vorne Nr. 40,
Weltraum-Konjunktionen Nr. 37), mehr Übungssätze, und Abwechslung: Eine zweite Runde bringt zuerst Aufgaben, die noch nicht dran waren."""
import asyncio
from harness import *
def fr(p):return [x for x in p.frames if x.url.split('?')[0].endswith('detektiv.html')][0]
async def round_(p,sel,mode):
  await p.goto('http://app.test/#D');await p.wait_for_timeout(1300);f=fr(p)
  await f.evaluate(f"lzSelect('{sel}','rep')");await f.click(f'[data-m="{mode}"]');await p.wait_for_timeout(250)
  # alle 10 Aufgaben einmal anzeigen (erste Antwort wählen / prüfen), damit sie als gesehen gelten
  qs=await f.evaluate("__detQs().map(q=>(q.t+'|'+(q.s||q.src)))")
  return f,qs
async def main():
  async with async_playwright() as pw:
    br=await pw.chromium.launch();c=await br.new_context(viewport={'width':412,'height':900});await c.route('**/*',handle);await c.add_init_script(acct('Robin'))
    p=await c.new_page();errs=[];p.on('pageerror',lambda e:errs.append(str(e)))
    await p.goto('http://app.test/#D');await p.wait_for_timeout(2500);f=fr(p)
    r=await f.evaluate("""(()=>{const I=window.__lzArena.I,bad=[];const cnt={};
      I.forEach(i=>{const k=(i.tag||i.t);cnt[k]=(cnt[k]||0)+1;
        if(i.t==='mc'&&(!i.o.includes(i.a)||new Set(i.o).size!==i.o.length))bad.push('mc '+i.s);
        if(i.t==='tap'&&!/\\*/.test(i.s))bad.push('tap '+i.s);
        if(i.t==='order'&&(!i.w||!i.head))bad.push('order '+i.src);
        if(i.t==='type'&&!(i.a&&i.a[0]))bad.push('type '+i.s);});
      return{n:I.length,z:I.filter(i=>i.z).length,cnt,bad,
        kurz:I.filter(i=>i.tag==='kurz').length,grenze:I.filter(i=>i.tag==='grenze').length,
        nr40:I.filter(i=>i.t==='order'&&/Nr\\. 40/.test(i.q)).length,nachdem:I.filter(i=>/^Ergänze im Plusquamperfekt: Nachdem/.test(i.s||'')).map(i=>i.s+' → '+i.a[0])};})()""")
    print({k:r[k] for k in ('n','z','kurz','grenze','nr40','bad')});print(r['cnt']);print('\n'.join(r['nachdem'][-3:]))
    assert not r['bad'] and r['z']>=120 and r['kurz']==6 and r['grenze']==7 and r['nr40']==5
    # Abwechslung: zweimal „Konjunktion wählen“ mit Paket 2+4 → die zweite Runde wiederholt nichts aus der ersten
    f,a=await round_(p,'p2,p4','konj')
    for k in range(10):
      await (await f.query_selector_all('.opt'))[0].click();await p.wait_for_timeout(80);await f.click('#nx');await p.wait_for_timeout(80)
    f,b=await round_(p,'p2,p4','konj')
    both=set(a)&set(b);print('Runde 1/2 gleich:',len(both));assert not both
    # Komma-Setzer enthält jetzt auch Satzgrenzen (Nr. 39); eine Satzgrenzen-Aufgabe richtig lösen
    found=False
    for k in range(6):
      f,qs=await round_(p,'p5','comma')
      tags=await f.evaluate("__detQs().map(q=>q.tag||q.t)")
      if 'grenze' in tags:
        i=tags.index('grenze')
        for j in range(i):
          if await f.query_selector('.opt'):await (await f.query_selector_all('.opt'))[0].click()
          else:await f.click('#chk')
          await p.wait_for_timeout(60);await f.click('#nx');await p.wait_for_timeout(60)
        a=await f.evaluate(f"__detQs()[{i}].a")
        await f.click(f'.opt[data-o="{a}"]');await p.wait_for_timeout(150)
        t=' '.join((await f.inner_text('#card')).split());print(t[:200]);assert 'Richtig' in t;found=True
        await p.screenshot(path=OUTDIR+'det-grenze.png');break
    assert found
    print('errors',errs);assert not errs;await br.close()
asyncio.run(main())
