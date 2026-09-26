"""Alle vier Apps öffnen ohne Fehler."""
import asyncio,json,random
from harness import *
async def main():
  async with async_playwright() as pw:
    br=await pw.chromium.launch()
    c,p,errs=await dev(br)
    await p.goto('http://app.test/'); await p.wait_for_timeout(800)
    for k in 'WZED':
        await p.evaluate(f"location.hash='#{k}'"); await p.wait_for_timeout(2500)
        fr=[f for f in p.frames if f!=p.main_frame]
        print(k,'frames',len(fr))
        await p.evaluate("lzHome()"); await p.wait_for_timeout(800)
    print('errors',errs); await br.close()
asyncio.run(main())
