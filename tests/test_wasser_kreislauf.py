"""Wasser-Zauberschule, Paket 6 „Der Wasserkreislauf“: Kachel, Lernkarten, Bild-Aufgaben, Kreislauf-Puzzle, Lückentext,
Wasserkreislauf-Labor (Landschaft + Mini-Wasserkreislauf im Glas) mit Forscher-Aufträgen, Abschluss- und Schreibtest."""
import asyncio,json
from harness import *
SEED=acct('Robin')+"if(!localStorage.getItem('s')){localStorage.setItem('s','1');localStorage.setItem('wasserzauberschule-v1',JSON.stringify({xp:0,house:'h1',sel:['p6'],sound:false,stats:{},high:{},grades:{}}));}"
J=lambda f,k:f.evaluate("k=>JSON.parse(localStorage.getItem(k)||'null')",k)
async def main():
  async with async_playwright() as pw:
    br=await pw.chromium.launch()
    c=await br.new_context(viewport={'width':1024,'height':900}); await c.route('**/*',handle); await c.add_init_script(SEED)
    p=await c.new_page(); errs=[]; p.on('pageerror',lambda e:errs.append(str(e)))
    await p.goto('http://app.test/#Z'); await p.wait_for_timeout(3000)
    f=[x for x in p.frames if x!=p.main_frame][0]
    card=await f.inner_text('.pack[data-p="p6"]'); print('Kachel:',card.replace('\n',' | ')[:200]); assert 'Der Wasserkreislauf' in card and 'Volle Punkte' in card
    modes=await f.evaluate("[...document.querySelectorAll('.mode:not([disabled])')].map(b=>b.dataset.m)"); print('Modi',modes)
    for m in ['book','kreislab','cycle','gaps','ana','quiz','tf','test','write','werk']: assert m in modes,m
    await p.screenshot(path=OUTDIR+'z6-home.png')
    # Lernkarten
    await f.click('[data-m="book"]'); await p.wait_for_timeout(400)
    n=await f.evaluate("__Z6.cards()"); txt=await f.inner_text('#card'); print('Karten',n); assert n>=20 and 'Kondensation' in txt or 'Wasserkreislauf' in txt
    # Zauberprüfung: Bild-Aufgaben vorhanden
    await f.evaluate("__Z6.home()"); await p.wait_for_timeout(200)
    it=await f.evaluate("__Z6.pics()"); print('Bild-Aufgaben',it); assert len(it)==3 and all(o==5 for a,o in it)
    await f.evaluate("__Z6.start('quiz')"); await p.wait_for_timeout(300)
    for k in range(10):
        b=await f.query_selector('#card .opt:not([disabled])')
        if not b: break
        await b.click(); await p.wait_for_timeout(150)
        w=await f.query_selector('#weiter')
        if w: await w.click(); await p.wait_for_timeout(150)
    await p.screenshot(path=OUTDIR+'z6-quiz.png')
    # Kreislauf-Puzzle fehlerfrei lösen
    await f.evaluate("__Z6.home()"); await p.wait_for_timeout(200); await f.click('[data-m="cycle"]'); await p.wait_for_timeout(300)
    seq=await f.evaluate("__Z6.seq()"); print('Puzzle',seq[0],'…')
    for s in seq: await f.click(f'.pbtns .opt[data-b="{s}"]'); await p.wait_for_timeout(80)
    fb=await f.inner_text('#fb'); print('Puzzle fertig:',fb[:60]); assert 'Fehlerfrei' in fb
    await p.screenshot(path=OUTDIR+'z6-puzzle.png')
    st=(await J(f,'wasserzauberschule-v1'))['stats']['p6']; assert st['h'][-1]==1,st
    # Lückentext für p6
    await f.evaluate("__Z6.home()"); await p.wait_for_timeout(200); await f.click('[data-m="gaps"]'); await p.wait_for_timeout(300)
    assert 'Die Reise des Wassers' in await f.inner_text('#pprog')
    # Labor: Landschaft
    await f.evaluate("__Z6.home()"); await p.wait_for_timeout(200); await f.click('[data-m="kreislab"]'); await p.wait_for_timeout(300)
    menu=await f.evaluate("[...document.querySelectorAll('.mxbig')].map(b=>b.dataset.st)"); print('Stationen',menu); assert menu==['kreis','miniglas']
    await f.click('.mxbig[data-st="kreis"]'); await p.wait_for_timeout(600)
    await p.screenshot(path=OUTDIR+'z6-kreis-start.png')
    async def task(k,setup,wait):
        await f.click(f'[data-tk="{k}"]'); await p.wait_for_timeout(150)
        for sel in setup: await f.click(sel); await p.wait_for_timeout(60)
        await p.wait_for_timeout(wait); await f.click('#tkchk'); await p.wait_for_timeout(200)
        msg=await f.inner_text('#tktask'); ok='Richtig' in msg; print(' Auftrag',k,'→',msg.split('\n')[1][:70] if '\n' in msg else msg[:70]); assert ok,(k,msg)
        await f.click('#tkdone'); await p.wait_for_timeout(100)
    await task('nosun',['#wknew','[data-s="0"]'],7000)
    await task('rain',['#wknew','[data-s="100"]','[data-c="0"]','[data-b="0"]','#wkwind'],6000)
    await p.screenshot(path=OUTDIR+'z6-kreis-regen.png')
    await task('flood',['#wknew','[data-b="1"]'],16000)
    await p.screenshot(path=OUTDIR+'z6-kreis-hochwasser.png')
    await task('snow',['#wknew','[data-b="0"]','[data-c="1"]'],10000)
    await p.screenshot(path=OUTDIR+'z6-kreis-schnee.png')
    bal=await f.inner_text('#wkbal'); print('Bilanz',bal.replace('\n',' ')); assert 'Gesamt: 1000' in bal
    # Mini-Wasserkreislauf
    await f.click('#wkback'); await p.wait_for_timeout(300)
    assert await f.evaluate("[...document.querySelectorAll('.mxbig')].map(b=>b.dataset.st)")==['kreis','miniglas'],'zurück ins Wasserkreislauf-Labor'
    await f.click('.mxbig[data-st="miniglas"]'); await p.wait_for_timeout(500)
    await task('fast',['[data-t="70"]','[data-f="1"]','[data-i="1"]','#wkgo'],11000)
    await p.screenshot(path=OUTDIR+'z6-miniglas.png')
    await task('open',['[data-f="0"]','[data-t="40"]','#wkgo'],7000)
    werk=(await J(f,'wasserzauberschule-v1'))['werk']; print('erledigt',werk); assert werk.get('kreis:rain') and werk.get('miniglas:fast')
    # Schreibtest hat p6-Fragen
    n=await f.evaluate("__Z6.wq()"); assert n>=6
    print('errors',errs); assert not errs,errs
    await br.close()
asyncio.run(main())
