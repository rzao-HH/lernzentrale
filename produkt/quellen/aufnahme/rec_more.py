import asyncio,sys,math
sys.path.insert(0,'/tmp/claude-0/-home-user-lernzentrale/5e8e16f5-f205-563d-8368-15598a4bce8d/scratchpad')
from rec import *
async def center(loc):
    b=await loc.bounding_box(); return b['x']+b['width']/2,b['y']+b['height']/2
async def draw(pw):
    br,p=await setup(pw)
    await p.goto('http://app.test/#W'); await p.wait_for_timeout(2500); f=await frame(p)
    await f.evaluate("lzSelect('p1,p2','rep')"); await f.click('[data-m="draw"]'); await p.wait_for_timeout(600)
    txt=await f.inner_text('body'); import re
    m=re.search(r'Winkel von (\d+)',txt); deg=int(m.group(1)); print('draw',deg)
    info=await f.evaluate("(()=>{const s=document.getElementById('svg');const st=document.getElementById('stage');const v=s.querySelector('circle.vertex');const ls=[...s.querySelectorAll('line')].map(l=>['x1','y1','x2','y2'].map(k=>+l.getAttribute(k)));return {W:st.clientWidth,v:v?[+v.getAttribute('cx'),+v.getAttribute('cy')]:null,ls}})()")
    sb=await box(f,'#stage'); sc=sb['width']/info['W']; P=lambda x,y:(sb['x']+x*sc,sb['y']+y*sc)
    vx,vy=info['v'] if info['v'] else (info['ls'][0][0],info['ls'][0][1])
    await p.evaluate(DOT); r=Rec(p,f); r.x,r.y=400,600; await r.wait(700)
    R=150
    start=P(vx+R*math.cos(math.radians(20)),vy-R*math.sin(math.radians(20)))
    await r.move(*start,steps=10); await r.dot(*start,True); await p.mouse.move(*start); await p.mouse.down(); await r.snap(150)
    n=24
    for i in range(1,n+1):
        a=20+(deg-20)*i/n; x,y=P(vx+R*math.cos(math.radians(a)),vy-R*math.sin(math.radians(a)))
        await p.mouse.move(x,y); await r.dot(x,y,True); await r.snap(70)
    await p.mouse.up(); await r.dot(x,y,False); await r.wait(600)
    fb=f.get_by_role('button',name=re.compile('Fertig'))
    await r.tap(*(await center(fb.first)),after=2600)
    r.save('draw'); await br.close()
async def quiz(pw):
    br,p=await setup(pw)
    await p.goto('http://app.test/#E'); await p.wait_for_timeout(2500); f=await frame(p)
    await f.click('[data-kcall="v"]'); await f.click('[data-ms="quiz"]'); await p.wait_for_timeout(500)
    await p.evaluate(DOT); r=Rec(p,f); r.x,r.y=400,640; await r.wait(700)
    for q in range(2):
        word=(await f.inner_text('.quiz-word')).strip()
        de=await f.evaluate(f"(()=>{{const w=WORDS.find(x=>x.en==={word!r});return w?w.de:null}})()")
        btn=f.locator('.option-btn',has_text=de).first if de else f.locator('.option-btn').first
        await r.tap(*(await center(btn)),after=1600)
        nb=f.locator('.btn-next').first
        if q==0 and await nb.count(): await r.tap(*(await center(nb)),after=700)
    r.save('quiz'); await br.close()
async def eflip(pw):
    br,p=await setup(pw)
    await p.goto('http://app.test/#E'); await p.wait_for_timeout(2500); f=await frame(p)
    await f.click('[data-kcall="v"]'); await f.click('[data-ms="flash"]'); await p.wait_for_timeout(500)
    await p.evaluate(DOT); r=Rec(p,f); r.x,r.y=420,660; await r.wait(700)
    for q in range(2):
        await r.tap(*(await center(f.locator('#flipCard'))),after=1500)
        await r.tap(*(await center(f.get_by_role('button',name='Weiß ich!').first)),after=900)
    r.save('eflip'); await br.close()
async def dflip(pw):
    br,p=await setup(pw)
    await p.goto('http://app.test/#D'); await p.wait_for_timeout(2500); f=await frame(p)
    await f.evaluate("lzSelect('p1,p2,p3','rep')"); await f.click('[data-m="book"]'); await p.wait_for_timeout(500)
    await p.evaluate(DOT); r=Rec(p,f); r.x,r.y=420,660; await r.wait(700)
    for q in range(2):
        await r.tap(*(await center(f.get_by_text('Tippen zum Umdrehen').first)),after=1700)
        await r.tap(*(await center(f.get_by_role('button',name='Weiß ich!').first)),after=900)
    r.save('dflip'); await br.close()
async def kessel(pw):
    br,p=await setup(pw)
    await p.goto('http://app.test/#Z'); await p.wait_for_timeout(2500); f=await frame(p)
    if await f.query_selector('[data-h]'): await f.click('[data-h]'); await p.wait_for_timeout(400)
    await f.evaluate("lzSelect('p1,p2,p4','rep')"); await f.click('[data-m="lab"]'); await p.wait_for_timeout(600)
    b=f.get_by_text('+10',exact=True).first
    bb=await b.bounding_box(); sc=int(max(0,bb['y']-560)); print('kessel scroll',sc,bb)
    await p.evaluate(DOT); r=Rec(p,f); r.pin=sc; await r.snap(50); r.x,r.y=420,700; await r.wait(900)
    for i in range(9):
        await r.tap(*(await center(b)),after=450,steps=4 if i else 8)
    await r.wait(2600)
    r.save('kessel'); await br.close()
async def verhoer(pw):
    br,p=await setup(pw)
    await p.goto('http://app.test/#E'); await p.wait_for_timeout(2500); f=await frame(p)
    await f.click('[data-kcall="v"]'); await f.click('[data-ms="verhoer"]'); await p.wait_for_timeout(300)
    await p.evaluate(DOT); r=Rec(p,f); r.x,r.y=420,660; await r.wait(900)
    await r.tap(*(await center(f.locator('#vhGo'))),after=900)
    await r.tap(*(await center(f.locator('[data-s="0"]'))),after=900)
    for q in range(2):
        ok=await f.evaluate("(()=>{const s=VH.c.sus[0];const a=VH.asked[0]||[];const k=s.qa.findIndex((_,j)=>!a.includes(j));return s.qa[k].q[0]})()")
        await r.tap(*(await center(f.locator('.option-btn',has_text=ok).first)),after=2000)
        if q==0: await r.tap(*(await center(f.get_by_text('Nächste Frage').first)),after=900)
    r.save('verhoer'); await br.close()
async def main():
  async with async_playwright() as pw:
    for fn in [kessel]:
        try: await fn(pw)
        except Exception as e: print('FAIL',fn.__name__,str(e)[:300])
asyncio.run(main())
