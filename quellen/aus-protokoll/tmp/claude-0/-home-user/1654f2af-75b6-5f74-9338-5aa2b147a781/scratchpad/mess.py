import sys
from playwright.sync_api import sync_playwright
CHROME="/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
want = set(int(x) for x in sys.argv[1:]) if len(sys.argv)>1 else None
js = r"""() => { const PX=96/25.4, out=[];
 document.querySelectorAll('.sheet').forEach(sh=>{ const p=+sh.dataset.page;
  sh.querySelectorAll('.panel,.col,.toc__col,.capbox,.chapbox').forEach(b=>{
   const r=b.getBoundingClientRect(); let lo=r.top, hi=r.top;
   b.querySelectorAll('*').forEach(c=>{ const q=c.getBoundingClientRect();
     if(q.height>0&&q.width>0){ if(q.bottom>hi)hi=q.bottom; if(q.top<lo)lo=q.top; } });
   out.push({p, cls:b.className.split(' ')[0], h:r.height/PX,
             used:(hi-r.top)/PX, over:(hi-r.bottom)/PX, top:(lo-r.top)/PX}); }); });
 return out; }"""
with sync_playwright() as pw:
    b=pw.chromium.launch(executable_path=CHROME)
    pg=b.new_page(viewport={"width":1800,"height":1300})
    pg.goto("file:///home/user/wick/src/broschuere.html?mode=print", wait_until="networkidle")
    pg.wait_for_timeout(700); rows=pg.evaluate(js); b.close()
for r in rows:
    if want and r['p'] not in want: continue
    flag = '  ÜBER' if r['over']>0.5 else ('  leer' if r['h']-r['used']>14 else '')
    print(f"S.{r['p']:02d} {r['cls']:10s} Höhe {r['h']:6.1f}  genutzt {r['used']:6.1f}"
          f"  Rest {r['h']-r['used']:6.1f}{flag}")