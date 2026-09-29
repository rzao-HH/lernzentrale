"""Winkel-Akademie: Winkel konstruieren – alle sechs Schritte mit Finger-Gesten (Schenkel ziehen, Geodreieck schieben/drehen,
markieren, neu anlegen, Schenkel b ziehen, Bogen antippen); richtig und mit Bogen auf der falschen Seite; kommt im Abschlusstest vor."""
import asyncio,math
from harness import *
async def drag(p,a,b,steps=12):
  await p.mouse.move(*a);await p.mouse.down()
  for i in range(1,steps+1):await p.mouse.move(a[0]+(b[0]-a[0])*i/steps,a[1]+(b[1]-a[1])*i/steps)
  await p.mouse.up()
async def run(p,f,deg_force,wrong_side=False):
  await f.evaluate(f"lzSelect('p1,p2,p3','rep')");await f.click('[data-m="konstr"]');await p.wait_for_timeout(400)
  svg=await f.query_selector('#svg');bb=await svg.bounding_box();ox,oy=bb['x'],bb['y']
  info=await f.evaluate("(()=>{const s=document.getElementById('svg').viewBox.baseVal;return[s.width,s.height]})()");W,H=info;sc=bb['width']/W
  deg=int(''.join(ch for ch in (await f.inner_text('.tgt')).split('=')[1] if ch.isdigit()))
  S=(W*.25,H*.6);A=(W*.8,H*.6)
  P=lambda x,y:(ox+x*sc,oy+y*sc)
  await drag(p,P(*S),P(*A));await p.wait_for_timeout(200)
  # Geodreieck: am Körper greifen (knapp über der Kante) und auf S schieben
  geo=await f.evaluate("(()=>{const g=document.querySelector('.kgeo').getAttribute('transform');return g})()")
  gx,gy=[float(v) for v in geo.split('translate(')[1].split(')')[0].split()]
  await drag(p,P(gx,gy-15),P(S[0],S[1]-15));await p.wait_for_timeout(200)
  assert await f.query_selector('#kok'),'Geodreieck rastet nicht ein'
  await f.click('#kok')
  d=deg if deg<180 else 360-deg
  mx,my=S[0]+math.cos(math.radians(d))*W*.2,S[1]-math.sin(math.radians(d))*W*.2
  await p.mouse.click(*P(mx,my));await p.wait_for_timeout(150);await f.click('#kok')
  # Geodreieck neu anlegen: drehen am Griff, dann schieben
  geo=await f.evaluate("document.querySelector('.kgeo').getAttribute('transform')");gx,gy=[float(v) for v in geo.split('translate(')[1].split(')')[0].split()]
  hh=await f.evaluate("(()=>{const h=document.querySelector('.kh');const r=h.getBoundingClientRect();return[r.x+r.width/2,r.y+r.height/2]})()")
  tgt=(ox+(gx+math.cos(math.radians(d+90))*200)*sc,oy+(gy-math.sin(math.radians(d+90))*200)*sc)
  await drag(p,hh,tgt,20);await p.wait_for_timeout(100)
  geo=await f.evaluate("document.querySelector('.kgeo').getAttribute('transform')");gx,gy=[float(v) for v in geo.split('translate(')[1].split(')')[0].split()]
  # Körperpunkt ein Stück über der Kante, dann so verschieben, dass die Kante durch S geht
  ux,uy=math.cos(math.radians(d)),-math.sin(math.radians(d));nx,ny=-uy,ux
  off=(S[0]-gx)*(-uy)+(S[1]-gy)*ux  # Abstand senkrecht
  grab=(gx+nx*(-12)+0,gy+ny*(-12))
  await drag(p,P(*grab),P(grab[0]+(-uy)*off,grab[1]+ux*off));await p.wait_for_timeout(150)
  assert await f.query_selector('#kok'),('Kante nicht durch S',await f.inner_text('#kst'))
  await f.click('#kok')
  bx,by=S[0]+ux*W*.3,S[1]+uy*W*.3
  await drag(p,P(*S),P(bx,by));await p.wait_for_timeout(150)
  mid=d/2 if ((deg<180)!=wrong_side) else d/2+180
  await p.mouse.click(*P(S[0]+math.cos(math.radians(mid))*40,S[1]-math.sin(math.radians(mid))*40));await p.wait_for_timeout(300)
  return deg,' '.join((await f.inner_text('#fb')).split())
async def main():
  async with async_playwright() as pw:
    br=await pw.chromium.launch();c=await br.new_context(viewport={'width':1180,'height':820},has_touch=False);await c.route('**/*',handle);await c.add_init_script(acct('Robin'))
    p=await c.new_page();errs=[];p.on('pageerror',lambda e:errs.append(str(e)))
    for ws in (False,True,False,False):
      await p.goto('http://app.test/#W');await p.wait_for_timeout(2000);f=[x for x in p.frames if x.url.split('?')[0].endswith('winkel.html')][0]
      deg,fb=await run(p,f,None,ws);print(deg,ws,'|',fb[:150])
      await p.screenshot(path=OUTDIR+f'konstr-{int(ws)}.png')
      assert (('konstruiert' in fb) if not ws else ('falschen Seite' in fb)),fb
    print('errors',errs);assert not errs;await br.close()
asyncio.run(main())
