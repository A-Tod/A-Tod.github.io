import glob, re, sys

MARK = 'polish-2026-11-26'
NEWV = 55

CSS = '''

/* ''' + MARK + ''' — ליטוש ממשק */
a,button,summary,label,input,select,[role="button"]{touch-action:manipulation}
h1,h2,h3,.hero__title,.pagehead h1,.home-picks__h{text-wrap:balance}
.legal p,.pagehead p,.story__body p,.pdp__blurb{text-wrap:pretty}
.card__price,.pdp__price,.drow span,.pdp__meta,.sum__row span{font-variant-numeric:tabular-nums}
@media (max-width:760px){
  .footer__list a,.footer__list button,.more,.home-picks__more a{display:inline-flex;align-items:center;min-height:40px}
}
'''

p = 'assets/css/style.css'
css = open(p, encoding='utf-8').read()
if MARK in css:
    print('GUARD FAIL css already patched'); sys.exit(1)
if 'text-wrap' in css or 'touch-action' in css:
    print('GUARD FAIL unexpected existing rules'); sys.exit(1)
open(p, 'w', encoding='utf-8').write(css + CSS)
print('css appended, bytes ' + str(len(css + CSS)))

files = sorted(glob.glob('*.html'))
olds, n = set(), 0
for f in files:
    s = open(f, encoding='utf-8').read()
    m = re.findall(r'style\.css\?v(\d+)', s)
    if not m:
        continue
    olds.update(int(x) for x in m)
    s = re.sub(r'style\.css\?v\d+', 'style.css?v' + str(NEWV), s)
    open(f, 'w', encoding='utf-8').write(s)
    n += 1

print('bumped ' + str(n) + ' of ' + str(len(files)) + ' html files, old versions ' + str(sorted(olds)))
if n < 20:
    print('GUARD FAIL too few files bumped'); sys.exit(1)
if any(v >= NEWV for v in olds):
    print('GUARD FAIL old version not lower than new'); sys.exit(1)
