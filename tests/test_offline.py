"""Offline-Modus: Service Worker speichert alles, Seite und Apps öffnen ohne Netz."""
import asyncio,os,subprocess,sys,time
from playwright.async_api import async_playwright
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
srv=subprocess.Popen([sys.executable,"-m","http.server","8765"],cwd=ROOT,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(1)
async def main():
  async with async_playwright() as pw:
    br=await pw.chromium.launch()
    c=await br.new_context(service_workers='allow',viewport={'width':1024,'height':900}); p=await c.new_page()
    errs=[];p.on('pageerror',lambda e:errs.append(str(e)))
    await p.goto('http://localhost:8765/'); await p.wait_for_timeout(1500)
    ok=await p.evaluate("navigator.serviceWorker.ready.then(r=>!!r.active)"); print('sw active',ok)
    await p.wait_for_timeout(2500)
    print('cached',await p.evaluate("caches.keys().then(k=>caches.open(k.find(x=>x.startsWith('lz-')&&x!=='lz-ext'))).then(c=>c.keys()).then(k=>k.length)"))
    await c.set_offline(True)
    await p.reload(); await p.wait_for_timeout(1500)
    print('offline title:',await p.title(),'| hi:',await p.inner_text('#hi'))
    await p.evaluate("location.hash='#Z'"); await p.wait_for_timeout(2500)
    f=[fr for fr in p.frames if fr!=p.main_frame][0]
    print('Z offline:',(await f.inner_text('body'))[:80].replace('\n',' '))
    await p.screenshot(path=os.path.join(os.path.dirname(os.path.abspath(__file__)),'out','off-Z.png'))
    p2=await c.new_page(); await p2.goto('http://localhost:8765/apps/kueste.html'); await p2.wait_for_timeout(1500)
    print('E direct offline:',(await p2.inner_text('body'))[:60].replace('\n',' '))
    print('errors',errs)
    await br.close()
try:
    asyncio.run(main())
finally:
    srv.terminate()
