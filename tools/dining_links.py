"""One-off: internal links to dining-lamp.html so Google can discover it.

- category-pendant-lamps.html: one line under the H1, with a page-local style
- the four pendant product pages: a link under the spec column, using the
  existing .detail__link style
Nothing else changes.
"""
import io

HREF = 'dining-lamp.html'
TEXT = 'המדריך: מנורה לפינת אוכל'
PRODUCTS = ['product-set.html', 'product-odd.html', 'product-ved.html', 'product-opeq.html']

CAT = 'category-pendant-lamps.html'
CAT_CSS = ('<style>\n.pagehead__guide{font-family:var(--f-he);font-weight:200;font-size:16px;'
           'line-height:1.5;margin-top:6px}\n.pagehead__guide a{text-decoration:underline;'
           'text-underline-offset:4px}\n</style>\n')
CAT_LINE = f'\n<p class="pagehead__guide">בוחרים תלייה מעל שולחן אוכל? <a href="{HREF}">{TEXT}</a></p>'

txt = io.open(CAT, encoding='utf-8').read()
if HREF in txt:
    print('SKIP', CAT)
else:
    h1 = txt.index('</h1>', txt.index('class="pagehead"')) + len('</h1>')
    txt = txt[:h1] + CAT_LINE + txt[h1:]
    txt = txt.replace('</head>', CAT_CSS + '</head>', 1)
    io.open(CAT, 'w', encoding='utf-8').write(txt)
    print('UPDATED', CAT)

for path in PRODUCTS:
    txt = io.open(path, encoding='utf-8').read()
    if HREF in txt:
        print('SKIP', path)
        continue
    spec = txt.index('<h2>מפרט</h2>')
    end = txt.index('\n</div>', spec)
    txt = txt[:end] + f'\n<a class="detail__link" href="{HREF}">{TEXT}</a>' + txt[end:]
    io.open(path, 'w', encoding='utf-8').write(txt)
    print('UPDATED', path)
