import asyncio,json,os,sys
from playwright.async_api import async_playwright
D=os.path.dirname(os.path.abspath(__file__)); OUT=D+'/frames/'; os.makedirs(OUT,exist_ok=True)
FPS=25; only=sys.argv[1] if len(sys.argv)>1 else None
async def main():
  async with async_playwright() as pw:
    br=await pw.chromium.launch(executable_path='/opt/pw-browsers/chromium-1243/chrome-linux64/chrome')
    p=await br.new_page(viewport={'width':1280,'height':720},device_scale_factor=1.5)
    await p.add_init_script('window.ANIMS='+open(D+'/anims.json').read())
    await p.goto('file://'+D+'/video.html'); await p.wait_for_timeout(1500)
    await p.evaluate("Promise.all(Object.values(ANIMS).flatMap(a=>a.f).concat(['t_arena.jpg','t_plan.jpg']).map(s=>new Promise(r=>{const i=new Image();i.onload=i.onerror=r;i.src=s;})))")
    total=await p.evaluate('TOTAL'); n=int(total/1000*FPS); print('total',total,'frames',n,flush=True)
    rng=range(n) if not only else [int(x) for x in only.split(',')]
    for i in rng:
        await p.evaluate(f"render({i*1000/FPS})")
        await p.evaluate("Promise.all([...document.images].filter(i=>i.offsetParent).map(i=>i.complete?1:i.decode().catch(()=>1)))")
        await p.screenshot(path=OUT+f'f_{i:05d}.jpg',quality=90,type='jpeg')
        if i%250==0: print(i,flush=True)
    await br.close()
asyncio.run(main())
