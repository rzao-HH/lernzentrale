import asyncio,io,os
from playwright.async_api import async_playwright
from PIL import Image
D=os.path.dirname(os.path.abspath(__file__))
async def main():
  async with async_playwright() as pw:
    br=await pw.chromium.launch(executable_path='/opt/pw-browsers/chromium-1243/chrome-linux64/chrome')
    p=await br.new_page(viewport={'width':600,'height':800},device_scale_factor=1)
    await p.goto('file://'+D+'/duell.html'); await p.wait_for_timeout(1200)
    total=await p.evaluate('TOTAL'); ims=[];step=80
    for t in range(0,total,step):
        await p.evaluate(f'render({t})'); b=await p.screenshot(); ims.append(Image.open(io.BytesIO(b)).convert('RGB'))
    du=[step]*len(ims); du[-1]=1500
    ims[0].save(D+'/../anim/duell.webp',save_all=True,append_images=ims[1:],duration=du,loop=0,quality=74,method=4)
    for t in [2000,7500,9300,11000,15200,17600]:
        pass
    print(len(ims),os.path.getsize(D+'/../anim/duell.webp')//1024,'KB')
    import json
    pts=[2500,4200,6200,9200,12500,15500,19000,22500,25000,total-500]
    sel=[ims[min(len(ims)-1,int(t/step))] for t in pts]
    print('total',total)
    s=Image.new('RGB',(5*240,2*320))
    for k,im in enumerate(sel): s.paste(im.resize((240,320)),((k%5)*240,(k//5)*320))
    s.save(D+'/../duell_strip.png')
    await br.close()
asyncio.run(main())
