"""Winkel-Akademie Paket 6: Aufgabe „Winkel beschriften“ – Buchstaben per Ziehen an Scheitel (S), Schenkel (a, b)
und in den Winkelbogen (griechischer Buchstabe). Richtig und falsch (a und b vertauscht)."""
import asyncio,math
from harness import *
async def drag(p,a,b,steps=10):
  await p.mouse.move(*a);await p.mouse.down()
  for i in range(1,steps+1):await p.mouse.move(a[0]+(b[0]-a[0])*i/steps,a[1]+(b[1]-a[1])*i/steps)
  await p.mouse.up()
async def main():
  async with async_playwright() as pw:
    br=await pw.chromium.launch();c=await br.new_context(viewport={'width':412,'height':900});await c.route('**/*',handle);await c.add_init_script(acct('Robin'))
    p=await c.new_page();errs=[];p.on('pageerror',lambda e:errs.append(str(e)))
    for right in (True,False):
      await p.goto('http://app.test/#W');await p.wait_for_timeout(1500);f=[x for x in p.frames if x.url.split('?')[0].endswith('winkel.html')][0]
      await f.evaluate("window.__wkForce='t6beschriften';lzSelect('p6','rep')");await f.click('[data-m="task"]');await p.wait_for_timeout(500)
      g=await f.evaluate('''(()=>{const s=document.querySelector('#stage svg'),M=s.getScreenCTM();
        const v=s.querySelector('.vertex'),r1=s.querySelector('.ray.r1'),r2=s.querySelector('.ray.r2');
        const P=(x,y)=>[M.a*x+M.c*y+M.e,M.b*x+M.d*y+M.f];const n=e=>['x1','y1','x2','y2'].map(a=>+e.getAttribute(a));
        const chips=[...s.querySelectorAll('.lbchip')].map(c=>{const b=c.getBoundingClientRect();return[c.textContent,b.x+b.width/2,b.y+b.height/2]});
        const a=n(r1),b=n(r2),S=[+v.getAttribute('cx'),+v.getAttribute('cy')];
        const ang=(q)=>Math.atan2(q[3]-q[1],q[2]-q[0]);const m=(ang(a)+ang(b))/2;
        return{S:P(S[0]-14,S[1]+16),a:P(a[0]+(a[2]-a[0])*.7,a[1]+(a[3]-a[1])*.7),b:P(b[0]+(b[2]-b[0])*.7,b[1]+(b[3]-b[1])*.7),
          w:P(S[0]+Math.cos(m)*60,S[1]+Math.sin(m)*60),chips};})()''')
      name=[c for c in g['chips'] if c[0] in 'αβγδεζηθικλμνξοπρστυφχψω'][0]
      tgt={'S':g['S'],'a':g['a'] if right else g['b'],'b':g['b'] if right else g['a']}
      ch={c[0]:(c[1],c[2]) for c in g['chips']}
      want=' '.join((await f.inner_text('#app')).split())
      nm=want.split('Winkelnamen ')[1][0]
      for k,v in tgt.items():await drag(p,ch[k],v)
      await drag(p,ch[nm],g['w']);await p.wait_for_timeout(100)
      await f.click('#done');await p.wait_for_timeout(400)
      fb=' '.join((await f.inner_text('#app')).split())
      await p.screenshot(path=OUTDIR+f'beschriften-{int(right)}.png');print(right,'|',fb[-220:])
      assert ('Nicht ganz' not in fb) if right else ('Nicht ganz' in fb),fb[-300:]
    print('errors',errs);assert not errs;await br.close()
asyncio.run(main())
