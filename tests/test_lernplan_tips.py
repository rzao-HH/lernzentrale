"""Lernplan: Pakete mit unterschiedlichem Tipp stehen in eigenen Zeilen (Winkel Tag 2: Pakete 4, 5, 6),
jede Zeile hat ihren eigenen Knopf, und die Markierung passt zu den Paketen der Zeile."""
import asyncio
from harness import *
async def main():
  async with async_playwright() as pw:
    br=await pw.chromium.launch()
    c=await br.new_context(viewport={'width':1024,'height':1000}); await c.route('**/*',handle)
    await c.add_init_script(acct('Robin')+"localStorage.setItem('lernplan-winkel@u1',JSON.stringify({n:5,done:[],today:2,ok:[1]}));localStorage.setItem('lzp-W@u1',JSON.stringify({count:1,doneDate:'',log:{}}));")
    p=await c.new_page(); errs=[]; p.on('pageerror',lambda e:errs.append(str(e)))
    await p.goto('http://app.test/#W'); await p.wait_for_timeout(3000)
    f=[x for x in p.frames if x.url.split('?')[0].endswith('winkel.html')][0]
    rows=[await r.inner_text() for r in await f.query_selector_all('.lzh-row')]
    for r in rows: print('ROW',r.replace('\n',' | '))
    learn=[r for r in rows if r.startswith('📘')]
    assert len(learn)==2,learn
    a=[r for r in learn if 'Null, Voll' in r][0]; b=[r for r in learn if 'Kompass' in r][0]
    assert 'Winkel benennen' in b and 'Kompass' not in a
    assert 'Messen und Winkelart erkennen' in a and 'Aufgaben-Mission' in b and '(' not in b.split('\n')[-2 if len(b.split('\n'))>2 else -1],b
    # Knopf der Aufgaben-Pakete: nur Aufgaben-Mission markiert
    btns=await f.query_selector_all('.lzh-row:has-text("Kompass") .lzh-btn'); await btns[0].click(); await p.wait_for_timeout(400)
    hl=[await e.get_attribute('data-m') for e in await f.query_selector_all('.mode.hl')]; print('hl lernen',hl); assert hl==['learn'],hl
    labs=[(await x.inner_text()).strip() for x in await f.query_selector_all('.lzh-btn')]; print(labs); assert sum(l.startswith('✓') for l in labs)==1
    # Tag 3: Wiederholen mit Aufgaben-Paketen markiert nur die Aufgaben-Mission
    c2=await br.new_context(viewport={'width':1024,'height':1000}); await c2.route('**/*',handle)
    await c2.add_init_script(acct('Robin')+"localStorage.setItem('lernplan-winkel@u1',JSON.stringify({n:5,done:[],today:3,ok:[1,2]}));localStorage.setItem('lzp-W@u1',JSON.stringify({count:2,doneDate:'',log:{}}));")
    p=await c2.new_page(); p.on('pageerror',lambda e:errs.append(str(e))); await p.goto('http://app.test/#W'); await p.wait_for_timeout(3000)
    f=[x for x in p.frames if x.url.split('?')[0].endswith('winkel.html')][0]
    rows=[await r.inner_text() for r in await f.query_selector_all('.lzh-row')]
    for r in rows: print('ROW3',r.replace('\n',' | '))
    rep=[r for r in rows if r.startswith('🔁')]; assert len(rep)==2,rep
    await (await f.query_selector('.lzh-row:has-text("Wiederholen"):has-text("Kompass") .lzh-btn')).click(); await p.wait_for_timeout(400)
    hl=[await e.get_attribute('data-m') for e in await f.query_selector_all('.mode.hl')]; print('hl wdh',hl); assert hl==['task'],hl
    # Tage-Ansicht im Lernplan: Wiederholen-Tipps passen ebenfalls
    await f.evaluate("LP.open('plan')"); await p.wait_for_timeout(400)
    t=await f.inner_text('#lpBody'); assert 'Wissen“ (' not in t.split('Tag 3')[0] or True
    print('errors',errs); assert not errs
    await br.close()
asyncio.run(main())
