import asyncio,sys,math
sys.path.insert(0,'/tmp/claude-0/-home-user-lernzentrale/5e8e16f5-f205-563d-8368-15598a4bce8d/scratchpad')
from rec import *
INFO="""(()=>{const s=document.getElementById('svg');const st=document.getElementById('stage');
const r1=s.querySelector('line.r1'),r2=s.querySelector('line.r2'),v=s.querySelector('circle.vertex');
const n=e=>['x1','y1','x2','y2'].map(k=>+e.getAttribute(k));
return {W:st.clientWidth,H:st.clientHeight,v:[+v.getAttribute('cx'),+v.getAttribute('cy')],r1:n(r1),r2:n(r2)}})()"""
async def main():
  async with async_playwright() as pw:
    br,p=await setup(pw)
    await p.goto('http://app.test/#W'); await p.wait_for_timeout(2500); f=await frame(p)
    await f.evaluate("lzSelect('p1,p2','rep')")
    await f.click('[data-d="profi"]'); await p.wait_for_timeout(300)
    for tries in range(15):
        await f.click('[data-m="measure"]'); await p.wait_for_timeout(500)
        if not await f.query_selector('#geoTog') or not await f.query_selector('line.r1'):
            await f.click('#back'); await p.wait_for_timeout(300); continue
        info=await f.evaluate(INFO); r1=info['r1']
        rot=math.degrees(math.atan2(-(r1[3]-r1[1]),r1[2]-r1[0]))
        r2=info['r2']; a2=math.degrees(math.atan2(-(r2[3]-r2[1]),r2[2]-r2[0]))
        deg=round((a2-rot)%360)
        print('try',tries,round(rot),deg)
        t0=((rot+90)%180)-90
        if 18<t0<70 and 30<deg<150: break
        await f.click('#back'); await p.wait_for_timeout(300)
    print('rot',rot,'deg',deg,'try',tries)
    await p.evaluate(DOT); r=Rec(p,f); r.x,r.y=300,560
    await r.wait(700)
    tog=await box(f,'#geoTog'); await r.tap(tog['x']+tog['width']/2,tog['y']+tog['height']/2,after=600)
    sb=await box(f,'#stage'); W,H=info['W'],info['H']; sc=sb['width']/W
    P=lambda x,y:(sb['x']+x*sc,sb['y']+y*sc)
    geo=await f.evaluate("document.querySelector('.geo').getAttribute('transform')")
    gx,gy=[float(v) for v in geo.split('translate(')[1].split(')')[0].split()]
    vx,vy=info['v']; Hh=min(W,H)*.55; hy=-Hh-34
    # 1) Geodreieck an den Scheitel schieben
    a=P(gx,gy-28); b=P(vx,vy-28)
    await r.drag(a,b,steps=18,ms=70); await r.wait(500)
    # 2) am Griff drehen
    t=((rot+90)%180)-90
    hp=lambda tt:P(vx+hy*math.sin(math.radians(tt)),vy+hy*math.cos(math.radians(tt)))
    await r.move(*hp(0),steps=10); await r.dot(*hp(0),True); await p.mouse.move(*hp(0)); await p.mouse.down(); await r.snap(150)
    n=22
    for i in range(1,n+1):
        tt=t*i/n; x,y=hp(tt); await p.mouse.move(x,y); await r.dot(x,y,True); await r.snap(80)
    await p.mouse.up(); await r.dot(*hp(t),False); await r.wait(500)
    # 3) Ablesen am zweiten Schenkel
    R=Hh*.68*0.88; ar=math.radians(rot+deg)
    await r.move(*P(vx+R*math.cos(ar),vy-R*math.sin(ar)),steps=12); await r.wait(1400)
    # 4) zum Ziffernfeld scrollen, eintippen und OK
    okb=await f.locator("button:text-is('OK')").first.bounding_box()
    pb=await box(f,'#panel'); need=max(0,int(okb['y']+okb['height']+70-(pb['y']+pb['height'])))
    for i in range(1,9):
        r.pin=int(need*i/8); await r.snap(70)
    print('need',need,await f.evaluate("document.scrollingElement.scrollTop"), await p.evaluate("(()=>{const fr=document.querySelector('iframe');let o=[];document.querySelectorAll('*').forEach(e=>{if(e.scrollHeight>e.clientHeight+5&&e.contains(fr))o.push(e.tagName+'#'+e.id+' '+e.scrollTop)});return o.join(',')})()"))
    await r.wait(300)
    for ch in str(deg):
        bt=f.locator(f"button:text-is('{ch}')").first; bb=await bt.bounding_box()
        await r.tap(bb['x']+bb['width']/2,bb['y']+bb['height']/2,after=260,steps=6)
    bb=await f.locator("button:text-is('OK')").first.bounding_box()
    await r.tap(bb['x']+bb['width']/2,bb['y']+bb['height']/2,after=2800,steps=6)
    r.save('geo')
    await br.close()
asyncio.run(main())
