import asyncio,sys
sys.path.insert(0,'/tmp/claude-0/-home-user-lernzentrale/5e8e16f5-f205-563d-8368-15598a4bce8d/scratchpad')
from rec import *
async def center(loc):
    b=await loc.bounding_box(); return b['x']+b['width']/2,b['y']+b['height']/2
SC="""(y)=>{const g=document.getElementById('lpGo');let e=g.parentElement;while(e&&!(e.scrollHeight>e.clientHeight+5&&getComputedStyle(e).overflowY!='visible'))e=e.parentElement;(e||document.scrollingElement).scrollTop=y;return (e||document.scrollingElement).scrollTop;}"""
async def scrollto(r,f,y0,y1,n=10):
    for i in range(1,n+1):
        await f.evaluate(SC,int(y0+(y1-y0)*i/n)); await r.snap(60)
async def main():
  async with async_playwright() as pw:
    br,p=await setup(pw,w=640,h=853,dsf=1.3)
    await p.goto('http://app.test/#W'); await p.wait_for_timeout(2500); f=await frame(p)
    await p.evaluate(DOT); r=Rec(p,f); r.x,r.y=420,700; await r.wait(700)
    print(await f.locator('#lpBtn').bounding_box()); await r.tap(*(await center(f.locator('#lpBtn'))),after=700); await p.screenshot(path='wl1.png'); print(await f.locator('#lpP').count())
    for k in range(2): await r.tap(*(await center(f.locator('#lpP'))),after=250,steps=5)
    await r.tap(*(await center(f.locator('label[for="lpc_p1"], #lpc_p1').first)),after=400,steps=6)
    await r.wait(300)
    g=f.locator('#lpGo'); bb=await g.bounding_box(); want=int(bb['y']-480)
    await scrollto(r,f,0,want,12)
    await r.tap(*(await center(g)),after=900)
    for y in [0]:
        await f.evaluate("(()=>{document.querySelectorAll('*').forEach(e=>{if(e.scrollHeight>e.clientHeight+5&&getComputedStyle(e).overflowY!='visible')e.scrollTop=0;})})()")
    await r.wait(1500)
    # Plan langsam durchscrollen
    h=await f.evaluate("(()=>{let m=0;document.querySelectorAll('*').forEach(e=>{if(e.scrollHeight>e.clientHeight+5&&getComputedStyle(e).overflowY!='visible'&&e.offsetParent)m=Math.max(m,e.scrollHeight-e.clientHeight);});return m;})()")
    print('h',h)
    tgt=min(h,700)
    for i in range(1,21):
        await f.evaluate(f"(()=>{{document.querySelectorAll('*').forEach(e=>{{if(e.scrollHeight>e.clientHeight+5&&getComputedStyle(e).overflowY!='visible'&&e.offsetParent)e.scrollTop={int(tgt*i/20)};}})}})()"); await r.snap(90)
    await r.wait(1500)
    r.save('wplan'); await br.close()
asyncio.run(main())
