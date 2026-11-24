"""Küsten-Crew: Vokabeln Unit 2 (Buch S. 247) als eigene Pakete hinter Unit 6 – Kacheln, Zuordnung, Quiz, Lernzettel."""
import asyncio
from harness import *
async def main():
  async with async_playwright() as pw:
    br=await pw.chromium.launch()
    c=await br.new_context(viewport={'width':1024,'height':1366}); await c.route('**/*',handle); await c.add_init_script(acct('Robin')); p=await c.new_page()
    errs=[];p.on('pageerror',lambda e:errs.append(str(e)))
    await p.goto('http://app.test/'); await p.wait_for_timeout(600)
    await p.evaluate("location.hash='#E'"); await p.wait_for_timeout(2500)
    f=[fr for fr in p.frames if fr!=p.main_frame][0]
    # Unit-6-Pakete unverändert, Unit 2 dahinter
    info=await f.evaluate("({n:PACKAGES.length,l9:pkgLabel(9),l10:pkgLabel(10),l11:pkgLabel(11),s:PACKAGES.slice(10).map(x=>x.length),all:WORDS.length})")
    print(info); assert info=={'n':12,'l9':'136–145','l10':'Unit 2: 1–16','l11':'Unit 2: 17–32','s':[16,16],'all':177},info
    # doppelte Wörter (fast, any) zählen im Unit-2-Paket für Unit 2
    u=await f.evaluate("[kcUW(PACKAGES[10].find(w=>w.en==='fast')),kcUW(PACKAGES[0].find(w=>w.en==='fast')),kcUW(PACKAGES[11].find(w=>w.en==='to clap'))]"); print(u); assert u==['v10','v0','v11'],u
    t=await f.inner_text('[data-pk="v10"]'); print('Kachel:',t.replace('\n',' | ')[:160]); assert 'Unit 2 · Vokabeln 1–16' in t and 'S. 247' in t
    await p.screenshot(path=OUTDIR+'e-unit2-home.png')
    # nur Unit 2 Paket wählen, Quiz: alle Fragen aus dem Paket
    await f.evaluate("progress._sel=['v10'];saveProgress()")
    await f.click('#kcBack') if await f.query_selector('#kcBack:visible') else None
    await f.evaluate("location.reload()"); await p.wait_for_timeout(2000)
    f=[fr for fr in p.frames if fr!=p.main_frame][0]
    await f.click('[data-ms="quiz"]'); await p.wait_for_timeout(400)
    ok=await f.evaluate("deck.every(w=>PACKAGES[10].includes(w))"); n=await f.evaluate("deck.length"); print('Quiz-Deck',n,ok); assert ok and n==16
    xp0=(await f.evaluate("progress.xp")) or 0
    await f.evaluate("""()=>{const w=deck[idx];const b=[...document.querySelectorAll('.option-btn')].find(x=>x.textContent.trim()===w.de.trim());b.click();}""")
    await p.wait_for_timeout(200); assert ((await f.evaluate("progress.xp")) or 0)>xp0
    await p.screenshot(path=OUTDIR+'e-unit2-quiz.png')
    # Lernstand kennt die neuen Pakete
    names=await f.evaluate("LS&&LS.units?LS.units.filter(u=>/Unit 2/.test(u.name)).map(u=>u.id):null"); print('LS',names)
    print('errors',errs); assert not errs,errs
    # Lernzettel: Unit 2 als erste Gruppe
    await p.goto('http://app.test/lernzettel/englisch-unit5-6.html'); await p.wait_for_timeout(800)
    g=await p.inner_text('.gtitle'); print('Lernzettel:',g); assert 'Unit 2' in g
    await p.click('.card'); await p.wait_for_timeout(500); assert 'S. 247' in await p.inner_text('#vTitle')
    # Lernplan: nur Unit 2; ein alter Unit-5/6-Plan wird beim ersten Öffnen zurückgesetzt
    c2=await br.new_context(viewport={'width':1024,'height':1366}); await c2.route('**/*',handle)
    await c2.add_init_script(acct('Robin')+"""if(!localStorage.getItem('s2')){localStorage.setItem('s2','1');localStorage.setItem('lernplan-englisch@u1',JSON.stringify({n:5,done:['v1'],today:3,ok:[1,2]}));localStorage.setItem('lzp-E@u1',JSON.stringify({count:2,doneDate:'',log:{1:{end:1},2:{end:2}}}));}""")
    p=await c2.new_page(); errs=[]; p.on('pageerror',lambda e:errs.append(str(e)))
    await p.goto('http://app.test/#E'); await p.wait_for_timeout(2500)
    f=[fr for fr in p.frames if fr!=p.main_frame][0]
    lp=await f.evaluate("JSON.parse(localStorage.getItem('lernplan-englisch@u1'))"); lz=await f.evaluate("JSON.parse(localStorage.getItem('lzp-E@u1'))")
    print('Plan nach Umstellung',lp,lz['count']); assert lp['n']==0 and lp['ver']=='u2' and lz['count']==0
    await f.evaluate("document.getElementById('lpBtn').click()"); await p.wait_for_timeout(500)
    body=await f.inner_text('#lpBody'); print('Einstellen:',body[:300].replace('\n',' | '))
    assert 'Unit 2: Vokabeln 1–16' in body and 'Unit 2: Vokabeln 17–32' in body and 'Vokabeln 1–15' not in body and 'Grammatik' not in body
    await f.click('#lpP'); await f.click('#lpGo'); await p.wait_for_timeout(500)
    plan=await f.inner_text('#lpBody'); print('Plan:',plan[:400].replace('\n',' | ')); assert 'Unit 2' in plan
    await p.screenshot(path=OUTDIR+'e-unit2-lernplan.png')
    lp=await f.evaluate("JSON.parse(localStorage.getItem('lernplan-englisch@u1'))"); print(lp); assert lp['n']==6 and lp['ver']=='u2'
    # erneutes Laden setzt den neuen Plan nicht wieder zurück
    await p.reload(); await p.wait_for_timeout(2500); f=[fr for fr in p.frames if fr!=p.main_frame][0]
    assert (await f.evaluate("JSON.parse(localStorage.getItem('lernplan-englisch@u1')).n"))==6
    print('errors',errs); assert not errs,errs
    await br.close()
asyncio.run(main())
