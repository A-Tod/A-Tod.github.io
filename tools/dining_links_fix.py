"""One-off fix: move the dining-lamp guide link into the spec column.

The first run put it at the end of the page on the four pendant pages.
This removes it there and inserts it before the closing </div> of the
"מפרט" column (found by structure, so indentation doesn't matter).
"""
import io

HREF = 'dining-lamp.html'
TEXT = 'המדריך: מנורה לפינת אוכל'
LINK = f'<a class="detail__link" href="{HREF}">{TEXT}</a>'
PRODUCTS = ['product-set.html', 'product-odd.html', 'product-ved.html', 'product-opeq.html']

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
