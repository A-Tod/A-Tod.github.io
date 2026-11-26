import sys

FILES = ['product-holo.html']

STYLE = '''<style>
.pdp__track{display:flex;flex-direction:column;gap:2px}
.pdp__galfoot{padding-top:12px;font-family:var(--f-he);font-weight:200;font-size:15px}
.pdp__3d{display:inline-block;text-decoration:underline;text-underline-offset:4px}
.pdp__bar{display:none}
@media (max-width:960px){
.pdp__track{flex-direction:row;align-items:center;gap:0;overflow-x:auto;scroll-snap-type:x mandatory;-webkit-overflow-scrolling:touch;scrollbar-width:none}
.pdp__track::-webkit-scrollbar{display:none}
.pdp__track>*{flex:0 0 100%;scroll-snap-align:start}
.pdp__galfoot{padding-top:0;text-align:center}
.pdp__bar{display:block;position:relative;height:2px;background:rgba(46,37,31,.13)}
.pdp__barfill{position:absolute;top:0;bottom:0;inset-inline-start:0;width:0;background:var(--ink)}
.pdp__3d{margin-top:18px;padding-inline:var(--gutter)}
}
</style>'''

FOOT = ('<div class="pdp__galfoot">'
        '<div class="pdp__bar" aria-hidden="true"><span class="pdp__barfill"></span></div>'
        '<a class="pdp__3d" href="#m3d">ראו איך הגוף נראה בחלל שלכם ‹</a>'
        '</div>')

SCRIPT = '''<script>
(function(){
  var tr=document.querySelector('.pdp__track'), fill=document.querySelector('.pdp__barfill');
  if(!tr||!fill) return;
  var n=tr.children.length;
  if(n<2) return;
  var raf=0;
  function upd(){
    raf=0;
    var max=tr.scrollWidth-tr.clientWidth;
    var p=max>1?Math.min(1,Math.abs(tr.scrollLeft)/max):0;
    fill.style.width=(((1+p*(n-1))/n)*100).toFixed(2)+'%';
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
    if 'pdp__barfill' in s:
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
