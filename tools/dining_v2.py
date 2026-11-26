"""One-off: internal links to dining-lamp.html (rebuilt on current main).

- category-pendant-lamps.html: one line under the H1, page-local style
- Set, Odd, Ved, Opeq: link at the end of the spec column (.detail__link)
"""
import io

HREF = 'dining-lamp.html'
TEXT = 'המדריך: מנורה לפינת אוכל'
LINK = f'<a class="detail__link" href="{HREF}">{TEXT}</a>'
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
    txt = txt.replace('\n' + LINK, '', 1) if ('\n' + LINK) in txt else txt.replace(LINK, '', 1)
    assert LINK not in txt, path
    spec = txt.index('<h2>מפרט</h2>')
    ship = txt.index('<h2>משלוח ואספקה</h2>', spec)
    col_open = txt.rindex('<div', spec, ship)      # opening of the shipping column
    close = txt.rindex('</div>', spec, col_open)    # closing of the spec column
    line_start = txt.rindex('\n', 0, close) + 1
    if txt[line_start:close].strip() == '':
        prev_start = txt.rindex('\n', 0, line_start - 1) + 1
        prev = txt[prev_start:line_start - 1]
        indent = prev[:len(prev) - len(prev.lstrip())]
        txt = txt[:line_start - 1] + '\n' + indent + LINK + txt[line_start - 1:]
    else:
        txt = txt[:close] + LINK + txt[close:]
    io.open(path, 'w', encoding='utf-8').write(txt)
    a, b = txt.index(LINK), txt.index('<h2>משלוח ואספקה</h2>')
    print('FIXED', path, 'inside spec column:', spec < a < b)
