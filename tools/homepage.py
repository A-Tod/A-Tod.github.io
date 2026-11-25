import re, sys

F = 'index.html'
s = open(F, encoding='utf-8').read()

if 'home-picks' in s:
    print('GUARD FAIL already applied'); sys.exit(1)
for pat, label, want in [
    (r'<p class="hero__sub">.*?</p>', 'hero__sub', 1),
    (r'<section class="features', 'features', 1),
    (r'</head>', 'head', 1),
]:
    n = len(re.findall(pat, s, re.S))
    if n != want:
        print('GUARD FAIL ' + label + ' n=' + str(n)); sys.exit(1)

STYLE = '''<style>
.hero__cta{display:inline-block;margin-top:24px;background:#fff;color:var(--ink);font-family:var(--f-he);font-weight:400;font-size:16px;line-height:1;padding:14px 34px;border-radius:100px;text-decoration:none;transition:opacity .2s}
.hero__cta:hover{opacity:.86}
.home-picks{padding-block:clamp(48px,6vw,78px) 0}
.home-picks__h{font-family:var(--f-he);font-weight:200;font-size:clamp(24px,3vw,32px);line-height:1.4;text-align:center;margin-bottom:8px}
.home-picks__sub{font-family:var(--f-he);font-weight:200;font-size:17px;line-height:1.5;text-align:center;margin-bottom:30px;opacity:.72}
.home-picks__grid{padding-bottom:0;grid-template-columns:repeat(4,1fr)}
.home-picks__more{text-align:center;padding-block:30px clamp(40px,5vw,70px);font-family:var(--f-he);font-weight:200;font-size:17px}
@media (max-width:980px){.home-picks__grid{grid-template-columns:repeat(2,1fr)}}
@media (max-width:560px){
.home-picks__grid{display:flex;gap:14px;overflow-x:auto;scroll-snap-type:x mandatory;-webkit-overflow-scrolling:touch;padding-bottom:8px}
.home-picks__grid>.card{flex:0 0 76%;scroll-snap-align:start}
}
</style>
'''

CTA = '\n        <a class="hero__cta" href="collection.html">גלו את הקולקציה</a>'

def card(slug, name, price, img1, img2, alt):
    return ('      <a class="card" href="product-' + slug + '.html">\n'
            '        <div class="card__media">\n'
            '          <img src="assets/img/' + img1 + '" alt="' + alt + '" loading="lazy"><img src="assets/img/' + img2 + '" alt="" loading="lazy">\n'
            '        </div>\n'
            '        <div class="card__name">' + name + '</div>\n'
            '        <div class="card__price">' + price + '</div>\n'
            '      </a>\n')

CARDS = (card('holo', 'Holo', '₪800', '177757_146abf6909e443c8a0be70ec5702cd00.jpg', '177757_db7fbcf53a6046119dcebb33ac4b3669.jpg', 'Holo — מנורת שולחן מבטון בעבודת יד')
       + card('ved', 'Ved', '₪750', '177757_59c6c9a2e8c148779e94d47d0e948d7c.jpg', '177757_9a7590c9515b4a3b93a91ce2f57e8a82.jpg', 'Ved — מנורת תלייה מבטון בעבודת יד')
       + card('ule', 'Ule', '₪950', '177757_e38d0f5c39e3457a917a69b1317d8dcc.jpg', '177757_1e644e783ce74d7a8c009e4940337c44.jpg', 'Ule — מנורת תקרה מבטון בעבודת יד')
       + card('opo', 'Opo', '₪900', '177757_c7b6998ecbf8463daffc42bd8d1b8846.jpg', '177757_2858288634c14c08b91b98748febde4b.jpg', 'Opo — מנורת קיר מבטון בעבודת יד'))

SECTION = ('<section class="wrap home-picks">\n'
           '  <h2 class="home-picks__h">מהקולקציה</h2>\n'
           '  <p class="home-picks__sub">שולחן, תלייה, תקרה וקיר — כל גוף נוצק ביד בסטודיו.</p>\n'
           '  <div class="grid-products home-picks__grid">\n'
           + CARDS +
           '  </div>\n'
           '  <p class="home-picks__more"><a href="collection.html">לכל הדגמים</a></p>\n'
           '</section>\n\n')

s = s.replace('</head>', STYLE + '</head>', 1)

m = re.search(r'<p class="hero__sub">.*?</p>', s, re.S)
s = s[:m.end()] + CTA + s[m.end():]

i = s.index('<section class="features')
s = s[:i] + SECTION + s[i:]

open(F, 'w', encoding='utf-8').write(s)
print('index.html updated, bytes ' + str(len(s)))
