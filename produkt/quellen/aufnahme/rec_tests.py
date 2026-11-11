import asyncio,sys,re
sys.path.insert(0,'/tmp/claude-0/-home-user-lernzentrale/5e8e16f5-f205-563d-8368-15598a4bce8d/scratchpad')
from rec import *
SRC=open('/home/user/lernzentrale/apps/wasser.html').read()
MC={m.group(1):m.group(2) for m in re.finditer(r"q:'((?:[^'\\]|\\.)*)',a:\['((?:[^'\\]|\\.)*)'",SRC)}
TF={m.group(1):m.group(2)=='true' for m in re.finditer(r"s:'((?:[^'\\]|\\.)*)',t:(true|false)",SRC)}
async def center(loc):
    b=await loc.bounding_box(); return b['x']+b['width']/2,b['y']+b['height']/2
async def schnell(pw):
    br,p=await setup(pw)
    await p.goto('http://app.test/#Z'); await p.wait_for_timeout(2500); f=await frame(p)
    if await f.query_selector('[data-h]'): await f.click('[data-h]'); await p.wait_for_timeout(300)
    await f.evaluate("lzSelect('p1,p2,p3,p4','rep')"); await f.click('[data-m="test"]'); await p.wait_for_timeout(500)
    await p.evaluate(DOT); r=Rec(p,f); r.x,r.y=420,700; await r.wait(500)
    for i in range(16):
        q=(await f.evaluate("(document.querySelector('.q')||{}).textContent")) or ''
        q=q.replace('Abschlusstest: Die Auswertung kommt am Ende.','').strip()
        opts=f.locator('button.opt')
        n=await opts.count()
        if n==0: break
        texts=[(await opts.nth(k).inner_text()).strip() for k in range(n)]
        want=MC.get(q)
        if want is None:
            for s,t in TF.items():
                if s in q: want='Wahr' if t else 'Falsch'
        k=0
        if want:
            for j,tx in enumerate(texts):
                if tx.lower().startswith(want.lower()[:12]) or want.lower() in tx.lower(): k=j
        print(i,q[:50],'->',texts[k])
        await r.tap(*(await center(opts.nth(k))),after=380,steps=5)
    await r.wait(3200)
    r.save('schnelltest'); await br.close()
async def schreib(pw):
    br,p=await setup(pw)
    await p.goto('http://app.test/#Z'); await p.wait_for_timeout(2500); f=await frame(p)
    if await f.query_selector('[data-h]'): await f.click('[data-h]'); await p.wait_for_timeout(300)
    await f.evaluate("lzSelect('p1','rep')")
    for t in range(12):
        await f.click('[data-m="write"]'); await p.wait_for_timeout(400)
        await f.locator("button:text-is('3')").first.click(); await f.get_by_role('button',name='Test beginnen').click(); await p.wait_for_timeout(400)
        q=await f.inner_text('body')
        if 'im Eis angeordnet' in q: break
        await f.click('#back'); await p.wait_for_timeout(300)
        bk=f.get_by_role('button',name=re.compile('Abbrechen|Ja'))
        if await bk.count(): await bk.first.click(); await p.wait_for_timeout(300)
    print('try',t)
    await p.evaluate(DOT); r=Rec(p,f); r.pin=0; r.x,r.y=420,700; await r.wait(800)
    ta=f.locator('textarea'); await r.tap(*(await center(ta)),after=200)
    ans='Im Eis haben die Teilchen feste Plätze und sind regelmäßig angeordnet. Sie bewegen sich kaum.'
    for i in range(0,len(ans),3):
        await ta.fill(ans[:i+3]); await r.snap(60)
    await r.wait(500)
    for i in range(2):
        b=f.locator('button').filter(has_text=re.compile('Weiter')).last
        await r.tap(*(await center(b)),after=300,steps=5)
        await f.locator('textarea').fill(['Eis ist leichter als Wasser.','Die Teilchen bewegen sich schneller und weiter auseinander.'][i]); await r.snap(300)
    b=f.locator('button').filter(has_text='Abgeben').last
    await r.tap(*(await center(b)),after=900,steps=5)
    await r.wait(1600)
    # Selbstkontrolle Aufgabe 1: ja, ja, teils
    yes=f.locator("button",has_text='ja'); half=f.locator("button",has_text='teils'); no=f.locator("button",has_text='nein')
    b0=await yes.nth(0).bounding_box(); sc=int(max(0,b0['y']-520))
    for i in range(1,9): r.pin=int(sc*i/8); await r.snap(60)
    for loc in [yes.nth(0),yes.nth(1),half.nth(2)]:
        await r.tap(*(await center(loc)),after=500,steps=6)
    # restliche Aufgaben zügig
    rest=await yes.count()
    for j in range(3,rest):
        loc=[yes,yes,half][j%3].nth(j)
        bb=await loc.bounding_box(); want=int(r.pin+bb['y']-520)
        if want>r.pin:
            st=r.pin
            for i in range(1,5): r.pin=int(st+(want-st)*i/4); await r.snap(40)
        await r.tap(*(await center(loc)),after=120,steps=3)
    nb=f.get_by_role('button',name='Note berechnen')
    bb=await nb.bounding_box(); want=int(r.pin+bb['y']-560); st=r.pin
    for i in range(1,6): r.pin=int(st+(want-st)*i/5); await r.snap(50)
    await r.tap(*(await center(nb)),after=600,steps=5)
    r.pin=None; await r.wait(300)
    await f.evaluate("(()=>{const a=document.getElementById('app');if(a)a.scrollTop=0;document.scrollingElement.scrollTop=0})()")
    await r.wait(3000)
    r.save('schreibtest'); await br.close()
async def main():
  async with async_playwright() as pw:
    for fn in [schreib]:
        try: await fn(pw)
        except Exception as e: print('FAIL',fn.__name__,str(e)[:300])
asyncio.run(main())
