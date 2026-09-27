"""Speicheränderungen innerhalb einer App werden abgeglichen."""
import asyncio,json,random
from harness import *
async def main():
  async with async_playwright() as pw:
    br=await pw.chromium.launch()
    A,pa,ea=await dev(br); await A.add_init_script(acct('Robin')); await pa.goto('http://app.test/'); await pa.wait_for_timeout(1500)
    await pa.goto('http://app.test/#W'); await pa.reload(); await pa.wait_for_timeout(2500)
    f=[fr for fr in pa.frames if fr!=pa.main_frame][0]
    await f.evaluate("localStorage.setItem('winkelakademie-v1',JSON.stringify({xp:1234}))")
    await pa.wait_for_timeout(2500)
    v=DB.get(('acc:robin','app:W'));print('DB wa:',v);assert v and json.loads(v[0])['xp']==1234
    print('errors',ea); await br.close()
asyncio.run(main())
