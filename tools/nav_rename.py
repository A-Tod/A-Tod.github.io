"""One-off: rename the "חנות" menu item to "גופי תאורה" on every page.

Changes only: the nav dropdown label, breadcrumb links to collection.html,
and breadcrumb names in JSON-LD. Prints any other "חנות" left for review.
"""
import glob
import io
import re

OLD, NEW = 'חנות', 'גופי תאורה'
NAV = re.compile(r'(<button class="nav__link nav__toggle"[^>]*>\s*)' + OLD + r'(\s*<svg)')
CRUMB = re.compile(r'(<a href="collection\.html">)' + OLD + r'(</a>)')
LD = re.compile(r'("name":\s*")' + OLD + r'(")')

total = 0
for path in sorted(glob.glob('*.html')):
    txt = io.open(path, encoding='utf-8').read()
    new, a = NAV.subn(r'\g<1>' + NEW + r'\g<2>', txt)
    new, b = CRUMB.subn(r'\g<1>' + NEW + r'\g<2>', new)
    new, c = LD.subn(r'\g<1>' + NEW + r'\g<2>', new)
    if new != txt:
        io.open(path, 'w', encoding='utf-8').write(new)
        total += 1
    left = new.count(OLD)
    print(f'{path}: nav={a} crumb={b} ld={c} remaining={left}')
    if left:
        for m in re.finditer(OLD, new):
            print('   ...', new[max(0, m.start() - 60):m.end() + 40].replace('\n', ' '))
print('files changed:', total)
