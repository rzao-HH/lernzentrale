"""Neue Version: Liegt auf dem Server eine neuere sw.js, erscheint die Leiste „Neue Version … jetzt aktualisieren“."""
import asyncio
from harness import *
async def main():
  async with async_playwright() as pw:
    br=await pw.chromium.launch();c=await br.new_context(viewport={'width':412,'height':900});await c.route('**/*',handle);await c.add_init_script(acct('Robin'))
    p=await c.new_page();errs=[];p.on('pageerror',lambda e:errs.append(str(e)))
    await p.goto('http://app.test/');await p.wait_for_timeout(1500)
    await p.evaluate("__lzUpdCheck()");await p.wait_for_timeout(500);assert await p.query_selector('#lzUpd') is None,'Leiste ohne neue Version'
    async def newer(route,req): await route.fulfill(status=200,content_type='text/javascript',body='const VER="99.0.0";')
    await p.route('**/sw.js?check=*',newer)
    await p.evaluate("__lzUpdCheck()");await p.wait_for_timeout(500)
    t=await p.inner_text('#lzUpd');print(t);assert '99.0.0' in t
    print('errors',errs);assert not errs;await br.close()
asyncio.run(main())
