"""One-off: open each product page with the in-space photo Roie chose.

- Opeq and Opi get the two new photos he sent (converted to JPEG into
  assets/img/; the PNG uploads in tools/ are removed).
- For the others, the chosen existing photo moves to the first slide.
  The studio shot with the dimensions button becomes the second slide.
- og:image, JSON-LD and the product cards are not touched.
Choices are 1-based positions in the current gallery (1 = studio shot).
"""
import glob
import io
import os
import re

from PIL import Image

CHOICE = {'holo': 3, 'ilo': 2, 'loe': 1, 'odd': 2, 'opo': 2, 'qibo': 5,
          'redel': 3, 'set': 2, 'ule': 4, 'ved': 5}
NEW = {
    'opeq': ('tools/opeq/image.png', 'assets/img/opeq-bedroom.jpg', 'Opeq — מנורת תלייה מבטון ליד המיטה'),
    'opi': ('tools/opi/image.png', 'assets/img/opi-wall.jpg', 'Opi — מנורת קיר מבטון על קיר טיח'),
}

for slug, (src, dst, _) in NEW.items():
    Image.open(src).convert('RGB').save(dst, 'JPEG', quality=86, optimize=True, progressive=True)
    os.remove(src)
    print('IMAGE', dst, os.path.getsize(dst), 'bytes')

SHOT = re.compile(r'[ \t]*<img class="pdp__shot"[^>]*>\n?')


def first_slide(img):
    img = img.strip()
    img = img.replace(' loading="lazy"', '')
    return img


for path in sorted(glob.glob('product-*.html')):
    slug = path[len('product-'):-len('.html')]
    txt = io.open(path, encoding='utf-8').read()
    gal = txt.index('<div class="pdp__gal')
    stage = txt.index('<div class="pdp__stage">', gal)
    line_start = txt.rindex('\n', 0, stage) + 1
    indent = txt[line_start:stage]
    if slug in NEW:
        _, dst, alt = NEW[slug]
        if dst in txt:
            print('SKIP', path)
            continue
        img = f'<img class="pdp__shot" src="{dst}" alt="{alt}">'
    else:
        n = CHOICE.get(slug, 1)
        if n == 1:
            print('KEEP', path)
            continue
        shots = list(SHOT.finditer(txt, stage))
        m = shots[n - 2]
        img = first_slide(m.group(0))
        txt = txt[:m.start()] + txt[m.end():]
    txt = txt[:line_start] + indent + img + '\n' + txt[line_start:]
    io.open(path, 'w', encoding='utf-8').write(txt)
    print('UPDATED', path, '->', re.search(r'src="([^"]+)"', img).group(1))
