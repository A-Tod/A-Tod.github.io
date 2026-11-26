"""One-off: apply the Holo mobile swipe gallery to every other product page.

Wraps the existing .pdp__gal children in .pdp__track, adds the progress bar
and 3D link footer, gives .m3d the #m3d anchor, and inlines the page-local
<style> and progress <script> exactly as on product-holo.html.
Images, names, prices and sizes are not touched.
"""
import glob
import io
import re

STYLE = """<style>
.pdp__track{display:flex;flex-direction:column;gap:2px}
.pdp__galfoot{padding-top:12px;font-family:var(--f-he);font-weight:200;font-size:15px}
.pdp__3d{display:inline-block;text-decoration:underline;text-underline-offset:4px}
.pdp__bar{display:none}
@media (max-width:960px){
.pdp__track{flex-direction:row;align-items:center;gap:0;overflow-x:auto;scroll-snap-type:x mandatory;-webkit-overflow-scrolling:touch;scrollbar-width:none}
.pdp__track::-webkit-scrollbar{display:none}
.pdp__track>*{flex:0 0 100%;scroll-snap-align:start;scroll-snap-stop:always;aspect-ratio:2/3;overflow:hidden}
.pdp__track>img.pdp__shot{width:100%;height:100%;object-fit:cover}
.pdp__stage img{width:100%;height:100%;object-fit:cover}
.pdp__galfoot{padding-top:0;text-align:center}
.pdp__bar{display:block;position:relative;height:2px;background:rgba(46,37,31,.13)}
.pdp__barfill{position:absolute;top:0;bottom:0;inset-inline-start:0;width:0;background:var(--ink)}
.pdp__3d{margin-top:18px;padding-inline:var(--gutter)}
}
</style>
"""

SCRIPT = """<script>
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
"""

LINK_3D = '<a class="pdp__3d" href="#m3d">ראו איך הגוף נראה בחלל שלכם ‹</a>'
GAL_OPEN = re.compile(r'<div class="pdp__gal(?:\s[^"]*)?">')
DIV_TOKEN = re.compile(r'<div\b|</div>')


def gal_span(txt):
    """Return (start_of_open_tag, end_of_open_tag, start_of_closing_div)."""
    m = GAL_OPEN.search(txt)
    if not m:
        return None
    depth = 0
    for tok in DIV_TOKEN.finditer(txt, m.start()):
        if tok.group(0) == '</div>':
            depth -= 1
            if depth == 0:
                return m.start(), m.end(), tok.start()
        else:
            depth += 1
    return None


changed = 0
for path in sorted(glob.glob('product-*.html')):
    if path == 'product-holo.html':
        continue
    txt = io.open(path, encoding='utf-8').read()
    if 'pdp__track' in txt:
        print('SKIP (already has track)', path)
        continue
    span = gal_span(txt)
    if not span:
        print('WARN no gallery found', path)
        continue
    s, o, e = span
    inner = txt[o:e]
    has3d = re.search(r'<div class="m3d"[ >]', txt) is not None
    foot = ('<div class="pdp__galfoot"><div class="pdp__bar" aria-hidden="true">'
            '<span class="pdp__barfill"></span></div>'
            + (LINK_3D if has3d else '') + '</div>\n')
    new_gal = txt[s:o] + '\n<div class="pdp__track">' + inner.rstrip() + '\n</div>\n' + foot
    new = txt[:s] + new_gal + txt[e:]
    if has3d and 'id="m3d"' not in new:
        new = new.replace('<div class="m3d">', '<div class="m3d" id="m3d">', 1)
    new = new.replace('</head>', STYLE + '</head>', 1)
    new = new.replace('</body>', SCRIPT + '</body>', 1)
    io.open(path, 'w', encoding='utf-8').write(new)
    shots = len(re.findall(r'<img\b', inner))
    print('UPDATED', path, 'images:', shots, '3d:', has3d)
    changed += 1

print('files changed:', changed)
