"""Detektiv-Büro: Lernkarten zeigen eine Frage; im Verb-Jäger ist die Auswahl sichtbar."""
import asyncio,json
from harness import *
async def main():
  async with async_playwright() as pw:
    br=await pw.chromium.launch()
    for scheme in ['light','dark']:
      c=await br.new_context(viewport={'width':1024,'height':800},color_scheme=scheme); await c.route('**/*',handle)
      await c.add_init_script(acct('Robin'))
      p=await c.new_page(); errs=[]; p.on('pageerror',lambda e:errs.append(str(e)))
      await p.goto('http://app.test/#D'); await p.wait_for_timeout(3000)
      f=[x for x in p.frames if x!=p.main_frame][0]
      await f.click('[data-m="book"]'); await p.wait_for_timeout(500)
      front=(await f.inner_text('.fcf')).split('\n'); q=[x for x in front if x.strip() and 'Tippen' not in x][-1]; print(scheme,'front:',q); assert q.strip().endswith('?') or 'Beispiel' in q,q
      await p.screenshot(path=OUTDIR+f'd-karte-{scheme}.png')
      await f.click('#bkc'); await p.wait_for_timeout(900); src=await f.inner_text('.fcb .fsrc'); print(scheme,'quelle:',src); assert src.startswith('📄')
      await p.screenshot(path=OUTDIR+f'd-karte-rueck-{scheme}.png')
      import re; src=open(ROOT+'/apps/detektiv.html',encoding='utf8').read(); blk=src[src.find('const CARDS='):src.find('\n};',src.find('const CARDS='))]
      fronts=re.findall(r"\[\['([^']*)'|\],\s*\['([^']*)'",blk); fronts=[a or b for a,b in fronts]; bad=[x for x in fronts if not (x.endswith('?') or x.endswith('Beispiel.'))]; print('fronts',len(fronts)); assert len(fronts)>=35 and not bad,bad
      await f.click('#back'); await p.wait_for_timeout(500)
      await f.click('[data-m="verb"]'); await p.wait_for_timeout(500)
      w=await f.query_selector_all('.words .w'); await w[1].click(); await p.wait_for_timeout(200)
      bg=await w[1].evaluate("e=>getComputedStyle(e).backgroundColor"); bg0=await w[0].evaluate("e=>getComputedStyle(e).backgroundColor"); print(scheme,'sel',bg,'unsel',bg0); assert bg!=bg0
      await p.screenshot(path=OUTDIR+f'd-verb-{scheme}.png')
      print('errors',errs); await c.close()
    await br.close()
asyncio.run(main())
