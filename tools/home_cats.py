"""One-off: add category shortcuts to the homepage, right after "מהקולקציה".

Four tiles link to the existing category pages, using the lit photos that
already appear on hover in the featured cards. CSS goes into the page-local
<style> block, so no cache-bust is needed. Nothing else on the page changes.
"""
import io

PATH = 'index.html'

CSS = """.home-cats{padding-block:0 clamp(16px,3vw,32px)}
.home-cats__h{font-family:var(--f-he);font-weight:200;font-size:clamp(24px,3vw,32px);line-height:1.4;text-align:center;margin-bottom:30px}
.home-cats__grid{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}
.home-cat{position:relative;display:block;aspect-ratio:4/5;overflow:hidden;text-decoration:none}
.home-cat img{width:100%;height:100%;object-fit:cover;transition:transform .6s ease}
.home-cat:hover img{transform:scale(1.03)}
.home-cat::after{content:"";position:absolute;inset:0;background:linear-gradient(to top,rgba(0,0,0,.42),rgba(0,0,0,0) 45%);pointer-events:none}
.home-cat__label{position:absolute;z-index:1;inset-inline-start:16px;bottom:14px;color:#fff;font-family:var(--f-he);font-weight:300;font-size:clamp(17px,1.6vw,20px);line-height:1.2}
@media (max-width:760px){.home-cats__grid{grid-template-columns:repeat(2,1fr);gap:10px}.home-cat__label{inset-inline-start:12px;bottom:10px}}
"""

HTML = """
<section class="wrap home-cats" aria-labelledby="home-cats-h">
<h2 class="home-cats__h" id="home-cats-h">לפי סוג</h2>
<div class="home-cats__grid">
<a class="home-cat" href="category-table-lamps.html"><img src="assets/img/177757_db7fbcf53a6046119dcebb33ac4b3669.jpg" alt="" loading="lazy"><span class="home-cat__label">מנורות שולחן</span></a>
<a class="home-cat" href="category-pendant-lamps.html"><img src="assets/img/177757_9a7590c9515b4a3b93a91ce2f57e8a82.jpg" alt="" loading="lazy"><span class="home-cat__label">מנורות תליה</span></a>
<a class="home-cat" href="category-wall-lamps.html"><img src="assets/img/177757_2858288634c14c08b91b98748febde4b.jpg" alt="" loading="lazy"><span class="home-cat__label">מנורות קיר</span></a>
<a class="home-cat" href="category-ceiling-lamps.html"><img src="assets/img/177757_1e644e783ce74d7a8c009e4940337c44.jpg" alt="" loading="lazy"><span class="home-cat__label">צמודי תקרה</span></a>
</div>
</section>
"""

txt = io.open(PATH, encoding='utf-8').read()
if 'home-cats' in txt:
    print('SKIP already present')
else:
    picks = txt.index('<section class="wrap home-picks">')
    end = txt.index('</section>', picks) + len('</section>')
    style_end = txt.index('</style>')
    assert style_end < picks, 'page-local style block not found in head'
    new = txt[:style_end] + CSS + txt[style_end:end] + '\n' + HTML.rstrip('\n') + txt[end:]
    io.open(PATH, 'w', encoding='utf-8').write(new)
    print('UPDATED', PATH)
