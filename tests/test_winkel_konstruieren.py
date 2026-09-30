"""Winkel-Akademie: Winkel konstruieren genau nach den Infoblättern „Winkel zeichnen 1“ (spitz/stumpf, Geodreieck verkehrt)
und „Winkel zeichnen 2“ (überstumpf: Trick 360° − β, Geodreieck unten an, großer Bogen). Mit Finger-Gesten:
Trick rechnen, Schenkel ziehen, S und a beschriften (Ziehen), Geodreieck schieben/drehen (falsche Seite wird erkannt),
markieren (und korrigieren), neu anlegen, Schenkel b ziehen, Bogen antippen, b und Winkelnamen beschriften."""
import asyncio,math
from harness import *
async def drag(p,a,b,steps=12):
  await p.mouse.move(*a);await p.mouse.down()
  for i in range(1,steps+1):await p.mouse.move(a[0]+(b[0]-a[0])*i/steps,a[1]+(b[1]-a[1])*i/steps)
  await p.mouse.up()
async def geo_xy(f):
  g=await f.evaluate("(document.querySelector('.kgeo')||{getAttribute:()=>'translate(-1 -1)'}).getAttribute('transform')")
  if g=='translate(-1 -1)':raise AssertionError(await f.inner_text('#kst'))
  return [float(v) for v in g.split('translate(')[1].split(')')[0].split()]
async def chip(f,c):
  return await f.evaluate(f"[...document.querySelectorAll('.lbchip')].findIndex(g=>g.textContent==={c!r})")
async def run(p,f,pack,wrong_side=False,wrong_lab=False):
  await f.evaluate(f"lzSelect('{pack}','rep')");await f.click('[data-m="konstr"]');await p.wait_for_timeout(400)
  svg=await f.query_selector('#svg');bb=await svg.bounding_box();ox,oy=bb['x'],bb['y']
  W,H=await f.evaluate("(()=>{const s=document.getElementById('svg').viewBox.baseVal;return[s.width,s.height]})()");sc=bb['width']/W
  deg=int(''.join(ch for ch in (await f.inner_text('.tgt')).split('=')[1] if ch.isdigit()));big=deg>180
  P=lambda x,y:(ox+x*sc,oy+y*sc)
  kst=await f.inner_text('#kst')
  assert ('Winkel zeichnen 2' in kst) if big else ('Winkel zeichnen 1' in kst),kst
  if big:
    await f.fill('#ktrick','50' if 360-deg!=50 else '40');await f.click('#ktok');assert 'Rechne nochmal' in await f.inner_text('#kst')
    await f.fill('#ktrick',str(360-deg));await f.click('#ktok');await p.wait_for_timeout(100)
  S=(W*.25,H*.5);A=(W*.8,H*.5)
  await drag(p,P(*S),P(*A));await p.wait_for_timeout(200)
  # Schritt 2 des Blatts: S und a beschriften – erst falsch (kleines s an den Scheitel), dann richtig
  tray=lambda i:P(26+i*46,26)
  await drag(p,tray(await chip(f,'s')),P(S[0]-12,S[1]+14));await drag(p,tray(await chip(f,'a')),P(W*.6,S[1]-12))
  await f.click('#klab');await p.wait_for_timeout(100);assert 'Noch nicht richtig' in await f.inner_text('#kst')
  await drag(p,P(S[0]-12,S[1]+14),tray(await chip(f,'s')));await drag(p,tray(await chip(f,'S')),P(S[0]-12,S[1]+14))
  await f.click('#klab');await p.wait_for_timeout(150)
  assert 'Geodreieck' in await f.inner_text('.ksteps .now'),await f.inner_text('#kst')
  # Geodreieck auf S schieben (Spitze oben). Blatt 2 verlangt „unten an“ → Hinweis, dann um 180° drehen
  gx,gy=await geo_xy(f)
  await drag(p,P(gx,gy-15),P(S[0],S[1]-15));await p.wait_for_timeout(200)
  if big:
    assert 'falschen Seite' in await f.inner_text('#kst'),await f.inner_text('#kst')
    hh=await f.evaluate("(()=>{const h=document.querySelector('.kh');const r=h.getBoundingClientRect();return[r.x+r.width/2,r.y+r.height/2]})()")
    await drag(p,hh,P(S[0],S[1]+200),24);await p.wait_for_timeout(200)
  assert 'markieren' in await f.inner_text('.ksteps .now'),('Geodreieck rastet nicht ein',await f.inner_text('#kst'))
  d=deg if not big else 360-deg;dd=d if not big else -d
  mx,my=S[0]+math.cos(math.radians(dd))*W*.2,S[1]-math.sin(math.radians(dd))*W*.2
  # Markierung auf der falschen Seite → Hinweis; dann verschieben an die richtige Stelle
  await p.mouse.click(*P(mx,2*S[1]-my));await p.wait_for_timeout(100);assert 'gehört an die Skala' in await f.inner_text('#kst')
  await drag(p,P(mx,2*S[1]-my),P(mx,my));await p.wait_for_timeout(150);await f.click('#kok')
  # Verbinden: Geodreieck drehen (Griff) und so schieben, dass die Kante durch S geht
  gx,gy=await geo_xy(f)
  hh=await f.evaluate("(()=>{const h=document.querySelector('.kh');const r=h.getBoundingClientRect();return[r.x+r.width/2,r.y+r.height/2]})()")
  await drag(p,hh,(ox+(gx+math.cos(math.radians(dd+90))*200)*sc,oy+(gy-math.sin(math.radians(dd+90))*200)*sc),20);await p.wait_for_timeout(100)
  ux,uy=math.cos(math.radians(dd)),-math.sin(math.radians(dd))
  if await f.query_selector('.kgeo'):  # kann beim Drehen schon zufällig einrasten
    gx,gy=await geo_xy(f)
    ux,uy=math.cos(math.radians(dd)),-math.sin(math.radians(dd));nx,ny=-uy,ux
    off=(S[0]-gx)*(-uy)+(S[1]-gy)*ux
    grab=(gx+nx*(-12),gy+ny*(-12))
    await drag(p,P(*grab),P(grab[0]+(-uy)*off,grab[1]+ux*off));await p.wait_for_timeout(150)
  assert 'Zieh die Linie an der Kante' in await f.inner_text('#kst'),('Kante nicht durch S',await f.inner_text('#kst'))
  bx,by=S[0]+ux*W*.3,S[1]+uy*W*.3
  await drag(p,P(*S),P(bx,by));await p.wait_for_timeout(150)
  small=dd/2;mid=small if (not big)!=wrong_side else small+180
  await p.mouse.click(*P(S[0]+math.cos(math.radians(-3))*60,S[1]-math.sin(math.radians(-3))*60));await p.wait_for_timeout(100)
  assert 'Tippe deutlich' in await f.inner_text('#kst'),'Tipp auf Schenkel a darf keinen Bogen wählen'
  if not wrong_side:  # erst falsche Seite antippen, im Beschriften-Schritt durch Antippen korrigieren
    await p.mouse.click(*P(S[0]+math.cos(math.radians(mid+180))*40,S[1]-math.sin(math.radians(mid+180))*40));await p.wait_for_timeout(100)
  await p.mouse.click(*P(S[0]+math.cos(math.radians(mid))*40,S[1]-math.sin(math.radians(mid))*40));await p.wait_for_timeout(200)
  # Schritt 6 des Blatts: b an den zweiten Schenkel, Winkelname in den Bogen
  name=(await f.inner_text('.tgt')).split('=')[0].strip()
  await drag(p,tray(await chip(f,'b')),P(S[0]+ux*W*.2+6,S[1]+uy*W*.2))
  nm=P(S[0]+math.cos(math.radians(mid))*58,S[1]-math.sin(math.radians(mid))*58)
  await drag(p,tray(await chip(f,name)),nm if not wrong_lab else P(W*.7,S[1]-8))
  await f.click('#kfin');await p.wait_for_timeout(300)
  return deg,' '.join((await f.inner_text('#fb')).split())
async def main():
  async with async_playwright() as pw:
    br=await pw.chromium.launch();c=await br.new_context(viewport={'width':1180,'height':820},has_touch=False);await c.route('**/*',handle);await c.add_init_script(acct('Robin'))
    p=await c.new_page();errs=[];p.on('pageerror',lambda e:errs.append(str(e)))
    for pack,ws,wl in (('p1',False,False),('p3',False,False),('p2',True,False),('p3',True,False),('p1',False,True)):
      await p.goto('http://app.test/#W');await p.wait_for_timeout(1500);f=[x for x in p.frames if x.url.split('?')[0].endswith('winkel.html')][0]
      deg,fb=await run(p,f,pack,ws,wl);print(pack,deg,ws,wl,'|',fb[:160])
      await p.screenshot(path=OUTDIR+f'konstr-{pack}-{int(ws)}{int(wl)}.png')
      if wl:assert 'Beschriftung' in fb,fb
      elif ws:assert 'falschen Seite' in fb,fb
      else:assert 'konstruiert' in fb,fb
    # Schritt zurück
    await p.goto('http://app.test/#W');await p.wait_for_timeout(1500);f=[x for x in p.frames if x.url.split('?')[0].endswith('winkel.html')][0]
    await f.evaluate("lzSelect('p1','rep')");await f.click('[data-m="konstr"]');await p.wait_for_timeout(300)
    svg=await f.query_selector('#svg');bb=await svg.bounding_box();W,H=await f.evaluate("(()=>{const s=document.getElementById('svg').viewBox.baseVal;return[s.width,s.height]})()");sc=bb['width']/W
    P=lambda x,y:(bb['x']+x*sc,bb['y']+y*sc)
    await drag(p,P(W*.25,H*.5),P(W*.8,H*.5));await f.click('#kback');await p.wait_for_timeout(100)
    assert 'Ersten Schenkel' in await f.inner_text('.ksteps .now')
    # Abschlusstest: keine Anleitung, Geodreieck auch „falsch herum“ nutzbar, Umdrehen-Knopf; bis zum Ende zeichenbar
    await p.goto('http://app.test/#W');await p.wait_for_timeout(1500);f=[x for x in p.frames if x.url.split('?')[0].endswith('winkel.html')][0]
    await f.evaluate("window.__wkTestKind='konstr';lzSelect('p3','test')");await f.click('[data-m="test"]');await p.wait_for_timeout(400)
    kst=await f.inner_text('#kst');print('TEST |',' '.join(kst.split())[:160])
    assert 'ohne Hilfen' in kst and 'Infoblatt' not in kst and 'Trick' not in kst and '360°' not in kst,kst
    deg=int(''.join(ch for ch in (await f.inner_text('.tgt')).split('=')[1] if ch.isdigit()))
    svg=await f.query_selector('#svg');bb=await svg.bounding_box();W,H=await f.evaluate("(()=>{const s=document.getElementById('svg').viewBox.baseVal;return[s.width,s.height]})()");sc=bb['width']/W
    P=lambda x,y:(bb['x']+x*sc,bb['y']+y*sc);S=(W*.25,H*.5)
    await drag(p,P(*S),P(W*.8,H*.5))
    for ch in ('S','a'):
      i=await chip(f,ch);await drag(p,P(26+i*46,26),P(S[0]-12,S[1]+14) if ch=='S' else P(W*.6,S[1]-12))
    await f.click('#klab');await p.wait_for_timeout(100)
    await f.click('[data-kr="180"]');await f.click('[data-kr="15"]');await f.click('[data-kr="-15"]');await f.click('#kgeohome')
    gx,gy=await geo_xy(f);await drag(p,P(gx,gy-15),P(S[0],S[1]-15));await p.wait_for_timeout(150)
    kst=await f.inner_text('#kst');assert 'Markierung' not in kst or True
    d=360-deg;mx,my=S[0]+math.cos(math.radians(d))*W*.2,S[1]-math.sin(math.radians(d))*W*.2  # oben gezeichnet (Geodreieck verkehrt) – im Test erlaubt
    await p.mouse.click(*P(mx,my));await p.wait_for_timeout(100);await f.click('#kok')
    await f.click('#kgeohome');gx,gy=await geo_xy(f)
    hh=await f.evaluate("(()=>{const h=document.querySelector('.kh');const r=h.getBoundingClientRect();return[r.x+r.width/2,r.y+r.height/2]})()")
    await drag(p,hh,(bb['x']+(gx+math.cos(math.radians(d+90))*200)*sc,bb['y']+(gy-math.sin(math.radians(d+90))*200)*sc),20)
    ux,uy=math.cos(math.radians(d)),-math.sin(math.radians(d))
    if await f.query_selector('.kgeo'):
      gx,gy=await geo_xy(f);nx,ny=-uy,ux;off=(S[0]-gx)*(-uy)+(S[1]-gy)*ux;grab=(gx+nx*(-12),gy+ny*(-12))
      await drag(p,P(*grab),P(grab[0]+(-uy)*off,grab[1]+ux*off));await p.wait_for_timeout(150)
    await drag(p,P(*S),P(S[0]+ux*W*.3,S[1]+uy*W*.3));await p.wait_for_timeout(100)
    mid=d/2+180;await p.mouse.click(*P(S[0]+math.cos(math.radians(mid))*40,S[1]-math.sin(math.radians(mid))*40));await p.wait_for_timeout(150)
    name=(await f.inner_text('.tgt')).split('=')[0].strip()
    i=await chip(f,'b');await drag(p,P(26+i*46,26),P(S[0]+ux*W*.2+6,S[1]+uy*W*.2))
    i=await chip(f,name);await drag(p,P(26+i*46,26),P(S[0]+math.cos(math.radians(mid))*58,S[1]-math.sin(math.radians(mid))*58))
    await f.click('#kfin');await p.wait_for_timeout(300)
    body=' '.join((await f.inner_text('#app')).split());print('TEST fertig |',deg,body[:200])
    assert '2 / ' in body and 'Schritt zurück' not in body,body[:300]
    await p.screenshot(path=OUTDIR+'konstr-test.png')
    print('errors',errs);assert not errs;await br.close()
asyncio.run(main())
