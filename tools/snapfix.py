import re, sys

KEY = 'f03a303db3bb465ab018533ce6018c9a'

# 1. product-holo.html: remove the square gallery image, add snap-stop
f = 'product-holo.html'
s = open(f, encoding='utf-8').read()

imgs = re.findall(r'<img[^>]*' + KEY + r'[^>]*>', s)
if len(imgs) != 1:
    print('GUARD FAIL img count=' + str(len(imgs))); sys.exit(1)
s = s.replace(imgs[0], '', 1)

old = '.pdp__track>*{flex:0 0 100%;scroll-snap-align:start;aspect-ratio:2/3;overflow:hidden}'
new = '.pdp__track>*{flex:0 0 100%;scroll-snap-align:start;scroll-snap-stop:always;aspect-ratio:2/3;overflow:hidden}'
if s.count(old) != 1:
    print('GUARD FAIL pdp track rule'); sys.exit(1)
s = s.replace(old, new, 1)
open(f, 'w', encoding='utf-8').write(s)
print('ok ' + f)

# 2. index.html: one swipe = one card
f = 'index.html'
s = open(f, encoding='utf-8').read()
old = '.home-picks__grid>.card{flex:0 0 76%;scroll-snap-align:start}'
new = '.home-picks__grid>.card{flex:0 0 76%;scroll-snap-align:start;scroll-snap-stop:always}'
if s.count(old) != 1:
    print('GUARD FAIL home card rule'); sys.exit(1)
s = s.replace(old, new, 1)
open(f, 'w', encoding='utf-8').write(s)
print('ok ' + f)
