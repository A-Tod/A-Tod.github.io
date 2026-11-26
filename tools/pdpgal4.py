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
.pdp__track>*{flex:0 0 100%;scroll-snap-align:start;aspect-ratio:2/3;overflow:hidden}
.pdp__track>img.pdp__shot{width:100%;height:100%;object-fit:cover}
.pdp__stage img{width:100%;height:100%;object-fit:cover}
.pdp__galfoot{padding-top:0;text-align:center}
.pdp__bar{display:block;position:relative;height:2px;background:rgba(46,37,31,.13)}
.pdp__barfill{position:absolute;top:0;bottom:0;inset-inline-start:0;width:0;background:var(--ink)}
.pdp__3d{margin-top:18px;padding-inline:var(--gutter)}
}
</style>'''

for f in FILES:
    s = open(f, encoding='utf-8').read()
    if 'pdp__barfill' not in s:
        print('GUARD FAIL bar version missing in ' + f); sys.exit(1)
    if 'aspect-ratio:2/3' in s:
        print('GUARD FAIL already applied ' + f); sys.exit(1)
    if s.count('<style>') != 1 or s.count('</style>') != 1:
        print('GUARD FAIL style count in ' + f); sys.exit(1)
    a = s.index('<style>')
    b = s.index('</style>') + len('</style>')
    s = s[:a] + STYLE + s[b:]
    open(f, 'w', encoding='utf-8').write(s)
    print('ok ' + f + ' ' + str(len(s)))
