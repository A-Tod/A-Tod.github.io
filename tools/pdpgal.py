import sys

FILES = ['product-holo.html']

STYLE = '''<style>
.pdp__track{display:flex;flex-direction:column;gap:2px}
.pdp__galfoot{display:flex;align-items:center;justify-content:space-between;gap:14px;flex-wrap:wrap;padding-top:12px;font-family:var(--f-he);font-weight:200;font-size:15px}
.pdp__swipe{display:none;opacity:.6}
.pdp__3d{text-decoration:underline;text-underline-offset:4px}
@media (max-width:960px){
.pdp__track{flex-direction:row;overflow-x:auto;scroll-snap-type:x mandatory;-webkit-overflow-scrolling:touch;gap:0}
.pdp__track>*{flex:0 0 100%;scroll-snap-align:start}
.pdp__swipe{display:inline}
.pdp__galfoot{padding-inline:var(--gutter);padding-top:10px}
}
</style>
'''

FOOT = ('    <div class="pdp__galfoot">'
        '<span class="pdp__swipe">החליקו לתמונות נוספות</span>'
        '<a class="pdp__3d" href="#m3d">ראו איך הגוף נראה בחלל שלכם ‹</a>'
        '</div>\n  ')


def close_index(s, open_end):
    depth = 1
    i = open_end
    while depth > 0:
        a = s.find('<div', i)
        b = s.find('</div>', i)
        if b < 0:
            return -1
        if a >= 0 and a < b:
            depth += 1
            i = a + 4
        else:
            depth -= 1
            i = b + 6
            if depth == 0:
                return b
    return -1


for f in FILES:
    s = open(f, encoding='utf-8').read()
    if 'pdp__track' in s:
        print('GUARD FAIL already applied ' + f); sys.exit(1)
    for tag, label in [('<div class="pdp__gal">', 'gal'), ('<div class="m3d">', 'm3d'), ('</head>', 'head')]:
        if s.count(tag) != 1:
            print('GUARD FAIL ' + label + ' in ' + f + ' n=' + str(s.count(tag))); sys.exit(1)

    s = s.replace('</head>', STYLE + '</head>', 1)
    s = s.replace('<div class="m3d">', '<div class="m3d" id="m3d">', 1)

    open_tag = '<div class="pdp__gal">'
    start = s.index(open_tag)
    inner_start = start + len(open_tag)
    close = close_index(s, inner_start)
    if close < 0:
        print('GUARD FAIL unbalanced gal in ' + f); sys.exit(1)
    inner = s[inner_start:close]
    s = s[:inner_start] + '\n    <div class="pdp__track">' + inner + '</div>\n' + FOOT + s[close:]
    open(f, 'w', encoding='utf-8').write(s)
    print('ok ' + f + ' ' + str(len(s)))
