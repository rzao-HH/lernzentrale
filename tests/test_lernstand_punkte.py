"""Punkte nach Lernstand (js/lernstand.js): sitzende Pakete bringen wenig, überfällige Bonus, neue volle Punkte;
Runden heben die Stufe; Tagesdeckel; Kachel-Anzeige in allen Apps; „Heute lohnt sich besonders“ auf der Startseite."""
import asyncio,json
from harness import *
D=86400000
SEED=acct('Robin')+"""if(!localStorage.getItem('seeded')){localStorage.setItem('seeded','1');const N=Date.now(),D=864e5,dk=t=>{const d=new Date(t);return d.getFullYear()+'-'+(d.getMonth()+1)+'-'+d.getDate();};
localStorage.setItem('detektivbuero-v1',JSON.stringify({sel:['p1'],xp:1000,stats:{},bk:{},grades:{},sound:false,
  ls:{p1:{s:3,t:N-D,d:'',r:0},p2:{s:2,t:N-5*D,d:'',r:0},p4:{s:1,t:N,d:dk(N),r:2}}}));
localStorage.setItem('unit6-progress',JSON.stringify({xp:500,_sel:['v0'],_mute:true,_ls:{v0:{s:4,t:N-D,d:'',r:0}}}));
localStorage.setItem('winkelakademie-v1',JSON.stringify({xp:640,sel:['p1'],sound:false,ls:{p2:{s:2,t:N-3*D,d:'',r:0}}}));}"""
J=lambda f,k:f.evaluate("k=>JSON.parse(localStorage.getItem(k)||'null')",k)
def fr(p,name): return [x for x in p.frames if x!=p.main_frame and x.url.split('?')[0].endswith(name)][-1]
async def main():
  async with async_playwright() as pw:
    br=await pw.chromium.launch()
    c=await br.new_context(viewport={'width':1024,'height':900}); await c.route('**/*',handle)
    await c.add_init_script(SEED)
    p=await c.new_page(); errs=[]; p.on('pageerror',lambda e:errs.append(str(e)))
    # ---------- Startseite: „Heute lohnt sich besonders“
    await p.goto('http://app.test/'); await p.wait_for_timeout(2500)
    t=await p.inner_text('#lohnt'); print('lohnt:',t.replace('\n',' | ')); assert 'Heute lohnt sich besonders' in t
    assert 'Bonus' in t and 'Satzreihe' in t,'überfälliges Detektiv-Paket fehlt'
    assert 'Hauptsatz' not in t,'sitzendes Paket darf nicht als lohnend erscheinen'
    assert 'Stumpf' in t and 'wieder fällig' in t,'fälliges Winkel-Paket fehlt'
    await p.screenshot(path=OUTDIR+'ls-start.png')
    # Klick → Detektiv-Büro öffnet mit dieser Akte
    await p.click('[data-lohnt="D|p2"]'); await p.wait_for_timeout(2500)
    f=fr(p,'detektiv.html'); sel=await f.evaluate("JSON.parse(localStorage.getItem('detektivbuero-v1')).sel"); print('sel nach Sprung',sel); assert sel==['p2'],sel
    # ---------- Detektiv: Kacheln
    tiles=await f.evaluate("[...document.querySelectorAll('.pack')].map(b=>b.querySelector('.ls-tile')?b.querySelector('.ls-tile').innerText.replace(/\\n/g,' '):'-')"); print('tiles',tiles)
    assert 'kannst du schon' in tiles[0] and 'Wenig Punkte' in tiles[0] and 'Wieder voll in 3 Tagen' in tiles[0],tiles[0]
    assert 'Bonus' in tiles[1] and '+20 %' in tiles[1] and 'lange nicht geübt' in tiles[1],tiles[1]
    assert 'neu' in tiles[2] and 'Volle Punkte' in tiles[2],tiles[2]
    assert 'genug' in tiles[3] and 'Morgen wieder voll' in tiles[3],tiles[3]
    # sitzendes Paket, heute schon 2× geübt: bleibt „kannst du schon“, kein „morgen wieder voll“
    s2=await f.evaluate("(()=>{const n=Date.now(),s=LS.status({s:3,t:n,d:LS.dkey(n),r:2},n);return [s.kind,LS.TXT[s.kind](s)]})()"); print('sitzt 2x',s2); assert s2[0]=='sitzt' and 'morgen' not in s2[1].lower(),s2
    await p.screenshot(path=OUTDIR+'ls-detektiv-kacheln.png')
    # ---------- Detektiv: echte Übung mit sitzender Akte p1 → 1 Punkt pro richtige Antwort, Hinweis erscheint
    await f.click('.pack[data-p="p1"]'); await f.click('.pack[data-p="p2"]'); await p.wait_for_timeout(200)  # nur p1
    assert (await J(f,'detektivbuero-v1'))['sel']==['p1']
    x0=(await J(f,'detektivbuero-v1'))['xp']
    m=await f.evaluate("(()=>{const b=document.querySelector('.mode[data-m=regel]:not([disabled])')||[...document.querySelectorAll('.mode:not([disabled])')].find(b=>!/book|blitz|test|write/.test(b.dataset.m));b.click();return b.dataset.m})()"); print('Modus',m)
    ok=0;n=0
    for k in range(12):
        await p.wait_for_timeout(250)
        if await f.query_selector('.result,.rcard'): break
        if not await f.query_selector('#nx'):
            btns=await f.query_selector_all('#card .opt:not([disabled]), #card .w:not([disabled]), #card button.word:not([disabled])')
            if not btns: btns=await f.query_selector_all('#card button:not([disabled])')
            await btns[0].click(); await p.wait_for_timeout(250)
            if await f.query_selector('#card .chk:not([disabled]), #card #chk'):
                try: await f.click('#card #chk')
                except Exception: pass
                await p.wait_for_timeout(200)
        if await f.query_selector('#nx'):
            n+=1; ok+=1 if await f.query_selector('.fbox.ok') else 0
            if ok==1 and n<=12 and not await f.query_selector('#lsHint.on'): await p.wait_for_timeout(500)
            await f.click('#nx')
    x1=(await J(f,'detektivbuero-v1'))['xp']; print('Antworten',n,'richtig',ok,'Punkte',x1-x0)
    assert n>=4 and x1-x0==ok,'sitzende Akte muss 1 Punkt pro richtige Antwort geben'
    if ok: assert await f.query_selector('#lsHint'),'Hinweis fehlt'; ht=await f.inner_text('#lsHint'); print('Hinweis:',ht.replace('\n',' ')); assert 'Bonus-Punkte' in ht or 'volle Punkte' in ht or 'Morgen' in ht
    await p.screenshot(path=OUTDIR+'ls-hinweis.png')
    # Runde gewertet (≥4 Antworten): Runde heute +1, Stufe nicht höher (nicht fällig)
    await f.evaluate("LS.endRound();LS.flush()"); ls=(await J(f,'detektivbuero-v1'))['ls']; print('p1',ls['p1'])
    assert ls['p1']['r']==1 and ls['p1']['s']<=3
    # ---------- Stufen: neue Akte p3 → gute Runde → Stufe 1; zweite gute Runde am selben Tag → keine Stufe mehr; dritte Runde → Tagesdeckel
    r=await f.evaluate("""(()=>{const o=[];for(let k=0;k<3;k++){for(let i=0;i<5;i++)LS.answer('p3',true);LS.endRound();LS.flush();const s=LS.status(JSON.parse(localStorage.getItem('detektivbuero-v1')).ls.p3);o.push([s.s,s.kind,LS.pts(5,['p3'])]);}return o;})()""")
    print('p3 Runden',r); assert r[0][0]==1 and r[0][1]=='ueben' and r[0][2]==5
    assert r[1][0]==1 and r[1][1]=='genug' and r[1][2]==1,'ab der 3. Runde am Tag nur Minimalpunkte'
    r2=await f.evaluate("(()=>{for(let i=0;i<5;i++)LS.answer('p5',false);LS.endRound();LS.flush();return JSON.parse(localStorage.getItem('detektivbuero-v1')).ls.p5})()"); print('p5 schlecht',r2); assert r2['s']==0
    av=await f.evaluate("[LS.pts(5,['p6']),LS.pts(100,['p1','p6']),LS.factor(['p1']),LS.factor(['p6'])]"); print('Durchschnitt',av)
    assert av[0]==5 and av[1] in (57,58),'Test: Durchschnitt aus sitzt (0,15) und neu (1)'
    # ---------- Küsten-Crew
    await p.evaluate("lzHome()"); await p.wait_for_timeout(500); await p.evaluate("location.hash='#E'"); await p.wait_for_timeout(3000)
    f=fr(p,'kueste.html')
    u=await f.evaluate("[kcUW(PACKAGES[3][0]),kcUW(VK[12]),kcUW(kcVerbCards()[0]||VK[0]),kcUW(GAPS[0])]"); print('Zuordnung',u); assert u[0]=='v3' and u[1]=='i1' and u[3]=='g2'
    cafe=await f.evaluate("KC_MP.cafe()"); print('Café →',cafe); assert cafe and all(x.startswith('v') for x in cafe)
    x0=(await J(f,'unit6-progress'))['xp']; g=await f.evaluate("kcXP(5,['v0'])"); x1=(await J(f,'unit6-progress'))['xp']; print('v0 sitzt:',g,x1-x0); assert g==1 and x1-x0==1
    assert await f.evaluate("kcXP(5,['v1'])")==5
    kt=await f.inner_text('.kc-pk[data-pk="v0"] .ls-tile'); print('Küste Kachel',kt.replace('\n',' ')); assert 'kannst du schon' in kt and 'Wieder voll in' in kt
    await p.screenshot(path=OUTDIR+'ls-kueste.png')
    # ---------- Winkel + Wasser: Kacheln mit Motto
    await p.evaluate("lzHome()"); await p.wait_for_timeout(500); await p.evaluate("location.hash='#W'"); await p.wait_for_timeout(3000)
    f=fr(p,'winkel.html'); wt=await f.inner_text('.pack[data-p="p2"] .ls-tile'); print('Winkel p2',wt.replace('\n',' ')); assert 'wieder fällig' in wt and 'Volle Punkte' in wt
    await p.screenshot(path=OUTDIR+'ls-winkel.png')
    await p.evaluate("lzHome()"); await p.wait_for_timeout(500); await p.evaluate("location.hash='#Z'"); await p.wait_for_timeout(3000)
    f=fr(p,'wasser.html'); zt=await f.inner_text('.pack[data-p="p1"] .ls-tile'); print('Wasser p1',zt.replace('\n',' ')); assert 'Volle Punkte – neu' in zt
    # bestehende Punkte unverändert
    assert (await J(f,'winkelakademie-v1'))['xp']==640
    print('errors',errs); assert not errs,errs
    await br.close()
asyncio.run(main())
