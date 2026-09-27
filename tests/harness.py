"""Test-Umgebung: liefert die Lernzentrale aus dem Repository aus, simuliert Supabase (lz_pull/lz_push) und die Live-Verbindung der Arena."""
import json,asyncio,os,mimetypes
from playwright.async_api import async_playwright
from playwright.async_api._generated import Browser as _B
_nc=_B.new_context
async def _new_context(self,**kw):
    kw.setdefault('service_workers',os.environ.get('LZ_SW','block'));return await _nc(self,**kw)
_B.new_context=_new_context
ROOT=os.environ.get('LZ_ROOT',os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB={}
OUTDIR=os.path.join(os.path.dirname(os.path.abspath(__file__)),'out')+'/'
os.makedirs(OUTDIR,exist_ok=True)
async def handle(route,req):
    url=req.url
    if url.startswith('https://sb.test/'):
        b=json.loads(req.post_data or '{}')
        if len(b.get('p_fam',''))<12: return await route.fulfill(status=400,body='{"message":"p_fam zu kurz"}')  # wie die echte Datenbank
        if url.endswith('lz_pull'):
            if not (0<=b.get('p_since',0)<=2147483647): return await route.fulfill(status=400,body='{"message":"p_since out of range"}')  # wie ein int4-Parameter
            rows=[{'k':k,'v':v,'ts':ts} for (f,k),(v,ts) in DB.items() if f==b['p_fam'] and ts>b['p_since']]
            return await route.fulfill(status=200,content_type='application/json',body=json.dumps(rows))
        if url.endswith('lz_push'):
            for it in b['p_items']:
                key=(b['p_fam'],it['k']);old=DB.get(key)
                if not old or old[1]<it['ts']: DB[key]=(it['v'],it['ts'])
            return await route.fulfill(status=204,body='')
    if url.startswith('http://app.test/'):
        path=url[len('http://app.test/'):].split('#')[0].split('?')[0] or 'index.html'
        fp=os.path.join(ROOT,path)
        if not os.path.isfile(fp): return await route.fulfill(status=404,body='')
        data=open(fp,'rb').read()
        if path=='js/sync.js': data=data.replace(b'https://vhmxzlztbpjwfytnyhbv.supabase.co',b'https://sb.test')
        ct=mimetypes.guess_type(fp)[0] or 'application/octet-stream'
        if fp.endswith('.js'): ct='text/javascript'
        return await route.fulfill(status=200,content_type=ct+('; charset=utf-8' if ct.startswith('text') else ''),body=data)
    await route.fulfill(status=200,body='')
async def dev(br):
    c=await br.new_context(); await c.route('**/*',handle); p=await c.new_page()
    errs=[]; p.on('pageerror',lambda e:errs.append(str(e))); return c,p,errs
PAGES={}
PRES={}
async def relay(name,msg):
    m=json.loads(msg); other=[n for n in PAGES if n!=name]
    if m.get('type')=='presence-me':
        PRES[name]=m['p']
        for o in other:
            try: await PAGES[o].evaluate("s=>window.__arenaIn&&__arenaIn(s)",json.dumps({'type':'presence','list':[PRES[n] for n in PRES if n!=o]}))
            except Exception: pass  # Seite lädt gerade neu
        return
    for o in other:
        try: await PAGES[o].evaluate("s=>window.__arenaIn&&__arenaIn(s)",msg)
        except Exception: pass
async def mk(br,name,seed):
    c=await br.new_context(viewport={'width':1024,'height':900}); await c.route('**/*',handle)
    await c.add_init_script("window.__arenaMock=true;"+seed)
    p=await c.new_page(); errs=[]; p.on('pageerror',lambda e:errs.append(str(e)))
    await p.expose_binding('__arenaOut',lambda src,msg: asyncio.ensure_future(relay(name,msg)))
    PAGES[name]=p; return p,errs
async def play(p,n,correct=True):
    for k in range(n):
        g=await p.evaluate("(()=>{const G=__arenaGame();if(!G||G.over)return null;const q=G.qs[G.qi%G.qs.length];return {a:q.a,o:q.o,lock:G.lock,fz:Date.now()<G.frozenUntil}})()")
        if not g: return
        if g['lock'] or g['fz'] or not await p.query_selector('#arQ [data-o]:not([disabled])'): await p.wait_for_timeout(150); continue
        idx=g['o'].index(g['a']) if correct else (g['o'].index(g['a'])+1)%len(g['o'])
        await p.click(f'#arQ [data-o="{idx}"]'); await p.wait_for_timeout(600)
def acct(name,e='🧒',uid='u1',more=''):
    """Seed für ein Gerät, auf dem `name` schon mit Benutzernamen angemeldet ist (optional weitere Personen als JS-Objekte in `more`)."""
    a=name.strip().lower()
    return ("if(!localStorage.getItem('nutzer-alle')){localStorage.setItem('nutzer-alle',JSON.stringify({list:[{id:'%s',name:'%s',e:'%s',acc:'%s',gid:'%s',t:1}%s],cur:'%s',n:1}));localStorage.setItem('lz-linked@%s','%s');}"
            %(uid,name,e,a,a,(','+more) if more else '',uid,uid,a))
