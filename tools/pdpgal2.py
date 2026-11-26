import sys

FILES = ['product-holo.html']

STYLE = '''<style>
.pdp__track{display:flex;flex-direction:column;gap:2px}
.pdp__galfoot{padding-top:12px;font-family:var(--f-he);font-weight:200;font-size:15px}
.pdp__3d{display:inline-block;text-decoration:underline;text-underline-offset:4px}
.pdp__dots{display:none}
@media (max-width:960px){
.pdp__track{flex-direction:row;align-items:center;gap:10px;padding-inline:14px;overflow-x:auto;scroll-behavior:smooth;scroll-snap-type:x mandatory;-webkit-overflow-scrolling:touch;scrollbar-width:none}
.pdp__track::-webkit-scrollbar{display:none}
.pdp__track>*{flex:0 0 86%;scroll-snap-align:center}
.pdp__galfoot{padding-inline:var(--gutter);padding-top:6px;text-align:center}
.pdp__dots{display:flex;gap:7px;justify-content:center;padding-bottom:14px}
.pdp__dot{width:7px;height:7px;border-radius:50%;background:currentColor;opacity:.2;border:0;padding:0;cursor:pointer;transition:opacity .25s var(--ease),transform .25s var(--ease)}
.pdp__dot[aria-current="true"]{opacity:.8;transform:scale(1.3)}
}
</style>'''

FOOT = ('<div class="pdp__galfoot">'
        '<div class="pdp__dots" role="tablist" aria-label="תמונות המוצר"></div>'
        '<a class="pdp__3d" href="#m3d">ראו איך הגוף נראה בחלל שלכם ‹</a>'
        '</div>')

SCRIPT = '''<script>
(function(){
  var tr=document.querySelector('.pdp__track'), dots=document.querySelector('.pdp__dots');
  if(!tr||!dots) return;
  var items=Array.prototype.slice.call(tr.children);
  if(items.length<2) return;
  items.forEach(function(el,i){
    var b=document.createElement('button');
    b.type='button'; b.className='pdp__dot'; b.setAttribute('aria-label','תמונה '+(i+1));
    b.addEventListener('click',function(){ el.scrollIntoView({behavior:'smooth',block:'nearest',inline:'center'}); });
    dots.appendChild(b);
  });
  var ds=Array.prototype.slice.call(dots.children), raf=0;
  function upd(){
    raf=0;
    var r=tr.getBoundingClientRect(), c=r.left+r.width/2, best=0, bd=1e9;
    items.forEach(function(el,i){
      var e=el.getBoundingClientRect(), d=Math.abs(e.left+e.width/2-c);
      if(d<bd){ bd=d; best=i; }
    });
    ds.forEach(function(d,i){ d.setAttribute('aria-current', i===best?'true':'false'); });
  }
  function q(){ if(!raf) raf=window.requestAnimationFrame(upd); }
  tr.addEventListener('scroll',q,{passive:true});
  window.addEventListener('resize',q);
  upd();
})();
</script>
'''

for f in FILES:
    s = open(f, encoding='utf-8').read()
    if 'pdp__track' not in s:
        print('GUARD FAIL no track in ' + f); sys.exit(1)
    if 'pdp__dots' in s:
        print('GUARD FAIL already applied ' + f); sys.exit(1)
    if s.count('<style>') != 1 or s.count('</style>') != 1:
        print('GUARD FAIL style count in ' + f); sys.exit(1)
    if s.count('<div class="pdp__galfoot">') != 1:
        print('GUARD FAIL galfoot count in ' + f); sys.exit(1)
    if s.count('</body>') != 1:
        print('GUARD FAIL body count in ' + f); sys.exit(1)

    a = s.index('<style>')
    b = s.index('</style>') + len('</style>')
    s = s[:a] + STYLE + s[b:]

    a = s.index('<div class="pdp__galfoot">')
    b = s.index('</div>', a) + len('</div>')
    s = s[:a] + FOOT + s[b:]

    s = s.replace('</body>', SCRIPT + '</body>', 1)

    open(f, 'w', encoding='utf-8').write(s)
    print('ok ' + f + ' ' + str(len(s)))
