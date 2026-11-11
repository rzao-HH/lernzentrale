import asyncio,sys
sys.path.insert(0,'/tmp/claude-0/-home-user-lernzentrale/5e8e16f5-f205-563d-8368-15598a4bce8d/scratchpad')
from rec import *
async def main():
  async with async_playwright() as pw:
    br,p=await setup(pw)
    await p.goto('http://app.test/#Z'); await p.wait_for_timeout(2500); f=await frame(p)
    if await f.query_selector('[data-h]'): await f.click('[data-h]'); await p.wait_for_timeout(400)
    await f.evaluate("lzSelect('p6','rep')"); await f.click('[data-m="kreislab"]'); await p.wait_for_timeout(500)
    await f.click('[data-st="kreis"]'); await p.wait_for_timeout(1200)
    await f.evaluate("(()=>{const a=document.getElementById('app');if(a)a.scrollTop=0;window.scrollTo(0,0)})()")
    b=await box(f,'#wkss'); sc=int(b['y']+22-660)
    st=await f.evaluate(f"(()=>{{const a=document.getElementById('app')||document.scrollingElement;a.scrollTop+={sc};return a.scrollTop}})()")
    await p.wait_for_timeout(300); b=await box(f,'#wkss'); print('slider',b,st)
    await p.evaluate(DOT); r=Rec(p,f); r.pin=st; r.x,r.y=420,640
    y=b['y']+b['height']/2; x0=b['x']+b['width']*0.5; x1=b['x']+b['width']*0.97
    await r.wait(800)
    await r.drag((x0,y),(x1,y),steps=18)
    await r.move(470,560,steps=6)
    await r.wait(4200)
    r.save('kreis')
    await br.close()
asyncio.run(main())
