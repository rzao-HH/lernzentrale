"""Kurze Bewegtbilder der App mit sichtbarem Fingerpunkt aufnehmen (Einzelbilder -> animiertes WebP)."""
import asyncio,sys,io,os
sys.path.insert(0,'/home/user/lernzentrale/tests')
from harness import *
from PIL import Image
A='/tmp/claude-0/-home-user-lernzentrale/5e8e16f5-f205-563d-8368-15598a4bce8d/scratchpad/anim/'
DOT="""(()=>{if(document.getElementById('fdot'))return;const d=document.createElement('div');d.id='fdot';
d.style.cssText='position:fixed;left:-100px;top:-100px;width:34px;height:34px;margin:-17px 0 0 -17px;border-radius:50%;background:rgba(255,122,92,.45);border:3px solid #ff7a5c;box-shadow:0 0 0 6px rgba(255,122,92,.18);z-index:2147483647;pointer-events:none;transition:transform .12s';
document.body.appendChild(d);window.__dot=(x,y,p)=>{d.style.left=x+'px';d.style.top=y+'px';d.style.transform=p?'scale(.75)':'scale(1)';d.style.background=p?'rgba(255,122,92,.75)':'rgba(255,122,92,.45)';};})()"""
class Rec:
    def __init__(s,p,f=None): s.p=p; s.f=f; s.frames=[]; s.x=280; s.y=600; s.pin=None
    async def snap(s,ms=110):
        if getattr(s,'ppin',None) is not None: await s.p.evaluate(f"(()=>{{window.scrollTo(0,{s.ppin});const fr=document.querySelector('iframe');document.querySelectorAll('*').forEach(e=>{{if(e.scrollHeight>e.clientHeight+5&&getComputedStyle(e).overflowY!='visible'&&e.contains(fr))e.scrollTop={s.ppin};}});}})()")
        if s.pin is not None and s.f: await s.f.evaluate(f"(()=>{{const a=document.getElementById('app');if(a)a.scrollTop={s.pin};const pn=document.getElementById('panel');if(pn)pn.scrollTop={s.pin};document.scrollingElement.scrollTop={s.pin};}})()")
        b=await s.p.screenshot(); s.frames.append((Image.open(io.BytesIO(b)).convert('RGB'),ms))
    async def dot(s,x,y,press=False):
        s.x,s.y=x,y; await s.p.evaluate(f"window.__dot&&__dot({x},{y},{str(press).lower()})")
    async def move(s,x,y,steps=8,ms=60):
        x0,y0=s.x,s.y
        for i in range(1,steps+1):
            await s.dot(x0+(x-x0)*i/steps,y0+(y-y0)*i/steps); await s.snap(ms)
    async def tap(s,x,y,after=900,steps=8):
        await s.move(x,y,steps); await s.dot(x,y,True); await s.snap(140)
        await s.p.mouse.click(x,y); await s.dot(x,y,False); await s.wait(after)
    async def drag(s,a,b,steps=16,ms=70):
        await s.move(*a); await s.dot(*a,True); await s.p.mouse.move(*a); await s.p.mouse.down(); await s.snap(120)
        for i in range(1,steps+1):
            x=a[0]+(b[0]-a[0])*i/steps; y=a[1]+(b[1]-a[1])*i/steps
            await s.p.mouse.move(x,y); await s.dot(x,y,True); await s.snap(ms)
        await s.p.mouse.up(); await s.dot(*b,False); await s.snap(120)
    async def wait(s,ms,step=160):
        t=0
        while t<ms: await s.p.wait_for_timeout(step); await s.snap(step); t+=step
    def save(s,name,w=600):
        ims=[];du=[]
        for im,ms in s.frames:
            ims.append(im.resize((w,int(im.height*w/im.width)),Image.LANCZOS)); du.append(ms)
        du[-1]=max(du[-1],1500)
        ims[0].save(A+name+'.webp',save_all=True,append_images=ims[1:],duration=du,loop=0,quality=72,method=4)
        print(name,len(ims),'Bilder',os.path.getsize(A+name+'.webp')//1024,'KB')
async def setup(pw,w=560,h=746,dsf=1.5):
    br=await pw.chromium.launch(executable_path='/opt/pw-browsers/chromium-1243/chrome-linux64/chrome')
    c=await br.new_context(viewport={'width':w,'height':h},device_scale_factor=dsf); await c.route('**/*',handle); p=await c.new_page()
    await c.add_init_script("try{localStorage.setItem('lz-news-seen','9.9.9')}catch(e){}")
    await p.goto('http://app.test/'); await p.wait_for_timeout(1500)
    b=p.get_by_role('button',name='Später')
    if await b.count(): await b.first.click()
    return br,p
async def frame(p): return [f for f in p.frames if f!=p.main_frame and f.url.startswith('http://app.test/apps')][-1]
async def box(f,sel):
    el=await f.query_selector(sel); return await el.bounding_box()
