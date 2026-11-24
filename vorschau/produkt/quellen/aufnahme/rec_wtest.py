import asyncio,sys,math,re
sys.path.insert(0,'/tmp/claude-0/-home-user-lernzentrale/5e8e16f5-f205-563d-8368-15598a4bce8d/scratchpad')
from rec import *
async def center(loc):
    b=await loc.bounding_box(); return b['x']+b['width']/2,b['y']+b['height']/2
SEQ=['degree','degree','draw','degree','degree','degree','draw','degree','degree','degree','degree','degree']
WRONG=4
async def main():
  async with async_playwright() as pw:
    br,p=await setup(pw)
    await p.goto('http://app.test/#W'); await p.wait_for_timeout(2500); f=await frame(p)
    await f.evaluate("lzSelect('p1,p2,p3,p4','test')"); await p.wait_for_timeout(400)
    await p.evaluate(DOT); r=Rec(p,f); r.x,r.y=420,700
    await f.evaluate("window.__wkTestKind='degree'")
    tb=f.locator('[data-m="test"]')
    await tb.scroll_into_view_if_needed(); await r.wait(600)
    await r.tap(*(await center(tb)),after=500)
    for i,k in enumerate(SEQ):
        await r.wait(900)
        nxt=SEQ[i+1] if i+1<len(SEQ) else 'degree'
        q=await f.evaluate("""(()=>{const b=document.getElementById('bignum');const tx=document.body.innerText;const m=tx.match(/Winkel von (\\d+)/);
 if(document.querySelector('.tbtn')){const d=parseInt((b&&b.textContent)||'0');return {kind:'degree',deg:d};}
 return {kind:'draw',deg:m?+m[1]:0};})()""")
        tf=lambda d:'null' if d==0 else 'spitz' if d<90 else 'recht' if d==90 else 'stumpf' if d<180 else 'gestreckt' if d==180 else 'ueber' if d<360 else 'voll'
        q['t']=tf(q['deg']); print(i,q)
        await f.evaluate(f"window.__wkTestKind='{nxt}'")
        if q['kind'] in ('degree','visual'):
            t=q['t']
            if i==WRONG:
                ts=await f.evaluate("[...document.querySelectorAll('.tbtn')].map(b=>b.dataset.t)"); t=[x for x in ts if x!=q['t']][0]
            b=f.locator(f'.tbtn[data-t="{t}"]'); await b.scroll_into_view_if_needed()
            await r.tap(*(await center(b)),after=350,steps=6)
        elif q['kind']=='draw':
            deg=q['deg']
            info=await f.evaluate("(()=>{const s=document.getElementById('svg');const st=document.getElementById('stage');const v=s.querySelector('circle.vertex');const ls=[...s.querySelectorAll('line')].map(l=>['x1','y1','x2','y2'].map(k=>+l.getAttribute(k)));return {W:st.clientWidth,vb:s.getAttribute('viewBox'),v:v?[+v.getAttribute('cx'),+v.getAttribute('cy')]:null,ls}})()")
            sb=await box(f,'#stage'); sc=sb['width']/info['W']; P=lambda x,y:(sb['x']+x*sc,sb['y']+y*sc)
            vx,vy=info['v'] if info['v'] else (info['ls'][0][0],info['ls'][0][1])
            R=150
            start=P(vx+R*math.cos(math.radians(20)),vy-R*math.sin(math.radians(20)))
            await r.move(*start,steps=8); await r.dot(*start,True); await p.mouse.move(*start); await p.mouse.down(); await r.snap(120)
            n=16
            for j in range(1,n+1):
                a=20+(deg-20)*j/n; x,y=P(vx+R*math.cos(math.radians(a)),vy-R*math.sin(math.radians(a)))
                await p.mouse.move(x,y); await r.dot(x,y,True); await r.snap(60)
            await p.mouse.up(); await r.dot(x,y,False); await r.wait(300)
            fb=f.get_by_role('button',name=re.compile('Fertig'))
            await r.tap(*(await center(fb.first)),after=350,steps=6)
    await r.wait(800)
    print((await f.inner_text('body'))[:400])
    await f.evaluate("(()=>{const a=document.getElementById('app');if(a)a.scrollTop=0;document.scrollingElement.scrollTop=0})()")
    await r.wait(3200)
    r.save('wtest'); await br.close()
asyncio.run(main())
