"""Auch bei Dunkelmodus im Gerät bleiben Startseite und alle Apps hell."""
import asyncio
from harness import *
def lum(c):
  import re
  r,g,b=[int(x) for x in re.findall(r'\d+',c)[:3]];return (r*299+g*587+b*114)/1000
async def main():
  async with async_playwright() as pw:
    br=await pw.chromium.launch()
    c=await br.new_context(viewport={'width':1024,'height':1000},color_scheme='dark'); await c.route('**/*',handle); await c.add_init_script(acct('Robin')); p=await c.new_page()
    await p.goto('http://app.test/'); await p.wait_for_timeout(800)
    bg=await p.evaluate("getComputedStyle(document.body).backgroundColor"); print('start',bg); assert lum(bg)>180,bg
    for h in ['W','Z','E','D']:
      await p.evaluate(f"location.hash='#{h}'"); await p.wait_for_timeout(2200)
      f=[fr for fr in p.frames if fr!=p.main_frame][-1]
      bg=await f.evaluate("getComputedStyle(document.body).backgroundColor");cs=await f.evaluate("getComputedStyle(document.documentElement).colorScheme")
      print(h,bg,cs); assert lum(bg)>150 and 'dark' not in cs,(h,bg,cs)
      await p.screenshot(path=OUTDIR+f'hell-{h}.png')
    await br.close()
asyncio.run(main())
