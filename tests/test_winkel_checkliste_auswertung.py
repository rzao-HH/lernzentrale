"""Winkel-Akademie, Checkliste: Auswertung pro Aufgabe (Versuche, Treffer, Zeit, Fehlerarten), klappbare Details,
Empfehlung mit Sprung in die Übung, Selbsteinschätzung, freie Frage des Kindes und Übersicht für Eltern."""
import asyncio,json
from harness import *
async def main():
  async with async_playwright() as pw:
    br=await pw.chromium.launch();c=await br.new_context(viewport={'width':412,'height':900});await c.route('**/*',handle);await c.add_init_script(acct('Robin'))
    p=await c.new_page();errs=[];p.on('pageerror',lambda e:errs.append(str(e)))
    await p.goto('http://app.test/#W');await p.wait_for_timeout(1500)
    f=[x for x in p.frames if x.url.split('?')[0].endswith('winkel.html')][0]
    # 1) Ohne Übung: Checkliste zeigt „noch zu wenig geübt“ und die Übersicht für Eltern sagt, dass Daten fehlen
    await f.evaluate("lzSelect('p1','rep')");await f.click('#clOpen');await p.wait_for_timeout(300)
    t=' '.join((await f.inner_text('#app')).split())
    assert 'Übersicht für Eltern' in t and 'noch zu wenig geübt' in t,t[:400]
    await f.click('.cl-par>summary');assert 'noch keine Übungsdaten' in ' '.join((await f.inner_text('.cl-par')).split())
    # 2) Gradzahl einordnen: 6 mal bewusst falsch (immer „gestreckt“ außer bei 180°), 2 mal richtig
    await f.click('.back');await f.evaluate("lzSelect('p1,p2','rep')")
    await f.click('[data-m="degree"]');await p.wait_for_timeout(300)
    wrongs=0
    for i in range(8):
      deg=int((await f.inner_text('#bignum')).replace('°',''))
      right=('null' if deg==0 else 'spitz' if deg<90 else 'recht' if deg==90 else 'stumpf' if deg<180 else 'gestreckt' if deg==180 else 'ueber' if deg<360 else 'voll')
      pick=right if i>=6 else ('gestreckt' if right!='gestreckt' else 'recht')
      wrongs+=0 if pick==right else 1
      await f.click(f'.tbtn[data-t="{pick}"]');await p.wait_for_timeout(500);await f.click('#weiter');await p.wait_for_timeout(200)
    vl=await f.evaluate("JSON.parse(localStorage.getItem('winkelakademie-v1')).vl")
    n=sum(s['n'] for s in vl.values());assert n==8,vl
    assert all(s['mn']>0 for s in vl.values()),vl   # Zeit wurde gemessen
    assert any(k.startswith('v|') for s in vl.values() for k in s['err']),vl  # Fehlerart „A als B eingeordnet“
    # 3) Checkliste: Aufgabe 6 (Gradzahl einordnen) ist klappbar und zeigt Tabelle, Fehler, Empfehlung
    await f.click('#back')
    await p.wait_for_timeout(200)
    await f.click('#clOpen');await p.wait_for_timeout(300)
    d=await f.query_selector('.cl-det[data-id="n6"]');assert d
    assert not await d.get_attribute('open'),'Details müssen zugeklappt starten'
    await f.click('.cl-det[data-id="n6"]>summary');await p.wait_for_timeout(150)
    txt=' '.join((await d.inner_text()).split())
    assert 'Häufige Fehler' in txt and 'eingeordnet' in txt and 'Treffer zuletzt' in txt,txt
    assert ('hier hakt es' in txt) or ('auf gutem Weg' in txt),txt
    assert await f.query_selector('.cl-det[data-id="n6"] .cl-vgo')
    # Übersicht für Eltern: Text + Tabelle
    assert await f.query_selector('.cl-par[open]'),'Übersicht bleibt nach dem Neuaufbau offen'
    pt=' '.join((await f.inner_text('.cl-par')).split())
    assert 'Bisher 8 Aufgaben beantwortet' in pt,pt
    # 4) Selbsteinschätzung + eigene Frage; danach bleiben die Details offen und alles ist gespeichert
    await f.click('.cl-det[data-id="n6"] .cl-sb[data-v="1"]');await p.wait_for_timeout(200)
    assert await f.query_selector('.cl-det[data-id="n6"][open]'),'Details klappen nach Klick auf ein Gefühl nicht zu'
    await f.fill('.cl-det[data-id="n6"] .cl-note','Ich verwechsle stumpf und überstumpf.');await p.wait_for_timeout(200)
    S=await f.evaluate("JSON.parse(localStorage.getItem('winkelakademie-v1'))")
    assert S['self']['n6']['v']==1 and 'verwechsle' in S['note']['n6']['t'],S
    await p.wait_for_timeout(100)
    pt=' '.join((await f.inner_text('.cl-par')).split());assert 'verwechsle stumpf' in pt,pt
    await p.screenshot(path=OUTDIR+'checkliste-auswertung.png',full_page=False)
    # 5) „Üben ▶“ in der Empfehlung startet sofort die Übung
    await f.click('.cl-det[data-id="n6"] .cl-vgo');await p.wait_for_timeout(400)
    assert await f.query_selector('#stage'),'Übung wurde nicht gestartet'
    print('errors',errs);assert not errs;await br.close()
asyncio.run(main())
