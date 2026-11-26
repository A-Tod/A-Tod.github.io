"""One-off: content page "תאורה מעל אי מטבח" (island-lamp.html).

Built from dining-lamp.html so head, header and footer stay identical.
Also: sitemap entry, and internal links from dining-lamp.html and
category-pendant-lamps.html. No CSS/JS changes.
"""
import io
import re

SLUG = 'island-lamp.html'
URL = 'https://studioatod.com/' + SLUG
TITLE = 'תאורה מעל אי מטבח — גובה, מרווח וכמה גופים | a-tod'
DESC = ('באיזה גובה תולים מנורות מעל אי מטבח, כמה גופים צריך ובאיזה מרווח. '
        'מדריך קצר, ואחריו מנורות תלייה מבטון בעבודת יד לאי המטבח.')

MAIN = '''<main id="main">
<div class="wrap">
<nav class="crumbs" aria-label="מיקום"><a href="index.html">בית</a><span>›</span>תאורה מעל אי מטבח</nav>
</div>

<div class="wrap">
<header class="pagehead">
<h1>תאורה מעל אי מטבח</h1>
<p>באיזה גובה תולים, כמה גופים צריך ובאיזה מרווח. מדריך קצר, ואחריו מנורות התלייה מבטון שמתאימות לאי.</p>
</header>

<div class="legal legal--intro">
<p>מעל אי מטבח עובדים, חותכים ואוכלים, ולכן התאורה שם צריכה להאיר את המשטח ולא רק לקשט. שלושה מספרים קובעים את רוב התוצאה: הגובה מעל המשטח, המרווח בין הגופים והמרחק מקצה האי.</p>
</div>
</div>

<div class="wrap">
<div class="legal">
<h2>גובה התלייה — 75 עד 90 ס"מ מהמשטח</h2>
<p>המרחק נמדד ממשטח האי ועד תחתית גוף התאורה, לא מהתקרה. 80 ס"מ היא נקודת פתיחה טובה בתקרה רגילה. בתקרה גבוהה מ-2.70 מ' אפשר לעלות לכיוון 90 ס"מ.</p>
<p>הגוף צריך להיות גבוה מספיק כדי לא לחסום מבט ממי שעומד בצד אחד של האי למי שעומד בצד השני, ונמוך מספיק כדי שהאור ייפול על המשטח ולא יתפזר בחדר.</p>
<p>בכל מנורות התלייה כאן אורך הכבל 150 ס"מ, והגובה הסופי נקבע בהתקנה לפי גובה התקרה.</p>

<h2>כמה גופים, ובאיזה מרווח</h2>
<p>אי עד 150 ס"מ — שני גופים. אי של 180 עד 240 ס"מ — שלושה. המרווח בין מרכז גוף למרכז הגוף הבא: 60 עד 75 ס"מ. מהגוף הקיצוני ועד קצה האי: 30 עד 45 ס"מ.</p>
<p>כלל בדיקה מהיר: השורה כולה, כולל המרווחים, תופסת בערך שני שליש מאורך האי. את הגופים תולים על ציר אחד, במרכז רוחב האי.</p>

<h2>קוטר — למה גופים קטנים עובדים בשורה</h2>
<p>מנורות התלייה של a-tod קטנות: Odd בקוטר 15 ס"מ, Set 23 ס"מ, Opeq ו-Ved 9 ס"מ. מעל אי הן עובדות בשורה ולא כגוף בודד. שלושה גופים קטנים במרווח שווה מאירים את כל אורך המשטח בצורה אחידה יותר מגוף אחד גדול באמצע.</p>
<p>Set ו-Odd מתאימים לאי רחב ולאי שמשמש גם לישיבה. Opeq ו-Ved מתאימים לאי צר, או לשורה של שלושה על אי ארוך.</p>

<h2>תקרה נמוכה או מעבר צפוף</h2>
<p>כשהתקרה נמוכה או שהאי נמצא במעבר ראשי במטבח, גוף תלוי עלול להפריע. במקרה כזה עדיף <a href="category-ceiling-lamps.html">גוף צמוד תקרה</a> מעל האי, שמאיר כלפי מטה בלי לרדת לגובה הראש.</p>

<h2>איזה אור ואיזו נורה</h2>
<p>מעל אי עבודה רוצים אור חם, 2700K עד 3000K, שנופל ישר על המשטח. גופי התלייה מעל האי משלימים את התאורה הכללית במטבח ולא מחליפים אותה.</p>
<p>Odd ו-Set עובדים עם נורת E27 LED. Opeq ו-Ved עם GU10 LED. הבטון מט ואינו מחזיר השתקפויות, ולכן הגוף לא מסנוור מי שעומד ליד האי.</p>
</div>
</div>

<div class="wrap">
<div class="legal legal--intro">
<h2>מנורות התלייה שמתאימות לאי מטבח</h2>
<p>כל גוף נוצק ביד בסטודיו מאותה תבנית של הדגם, ולכן שורה של שניים או שלושה גופים יוצאת אחידה בצורה ובמידות.</p>
</div>
<div class="grid-products">
<a class="card" href="product-odd.html">
<div class="card__media">
<img src="assets/img/177757_8f2b36f360ce4fa0abd96aa516981f3e.jpg" alt="Odd — מנורת תלייה מבטון מעל אי מטבח" loading="lazy"><img src="assets/img/177757_eb3300f976ef4192a6618224be7eab7e.jpg" alt="" loading="lazy">
</div>
<div class="card__name">Odd</div>
<div class="card__price">₪950</div>
</a>
<a class="card" href="product-set.html">
<div class="card__media">
<img src="assets/img/177757_1bf9f50b4e7c4bc8a70c651b64fba593.jpg" alt="Set — מנורת תלייה מבטון לאי מטבח רחב" loading="lazy"><img src="assets/img/177757_9ca70ab9b79446bc932ad2e77584bd90.jpg" alt="" loading="lazy">
</div>
<div class="card__name">Set</div>
<div class="card__price">₪1,350</div>
</a>
<a class="card" href="product-opeq.html">
<div class="card__media">
<img src="assets/img/177757_60d23ea1a2ef43bbaef6cd381697c685.jpg" alt="Opeq — מנורת תלייה קטנה מבטון לשורה מעל אי" loading="lazy"><img src="assets/img/177757_8c0b6359bdce4116929fee2a3bbb75c0.jpg" alt="" loading="lazy">
</div>
<div class="card__name">Opeq</div>
<div class="card__price">₪750</div>
</a>
<a class="card" href="product-ved.html">
<div class="card__media">
<img src="assets/img/177757_59c6c9a2e8c148779e94d47d0e948d7c.jpg" alt="Ved — מנורת תלייה קטנה מבטון לשורה מעל אי" loading="lazy"><img src="assets/img/177757_9a7590c9515b4a3b93a91ce2f57e8a82.jpg" alt="" loading="lazy">
</div>
<div class="card__name">Ved</div>
<div class="card__price">₪750</div>
</a>
</div>
</div>

<div class="wrap">
<div class="legal">
<h2>שאלות נפוצות</h2>
<p><strong>באיזה גובה תולים מנורות מעל אי מטבח?</strong><br>75 עד 90 ס"מ ממשטח האי ועד תחתית גוף התאורה. 80 ס"מ נקודת פתיחה טובה בתקרה רגילה.</p>
<p><strong>כמה מנורות צריך מעל אי מטבח?</strong><br>אי עד 150 ס"מ — שתיים. אי של 180 עד 240 ס"מ — שלוש.</p>
<p><strong>מה המרווח בין מנורות מעל אי?</strong><br>60 עד 75 ס"מ בין מרכז גוף למרכז הגוף הבא, ו-30 עד 45 ס"מ מהגוף הקיצוני ועד קצה האי.</p>
<p><strong>מה עושים כשהתקרה נמוכה?</strong><br>בוחרים גוף צמוד תקרה מעל האי במקום גוף תלוי, כדי שלא יפריע במעבר.</p>
<p><strong>איזו נורה מתאימה מעל אי מטבח?</strong><br>אור חם 2700K עד 3000K. Odd ו-Set עובדים עם E27 LED, Opeq ו-Ved עם GU10 LED.</p>
<p><a href="dining-lamp.html">מנורה לפינת אוכל</a> · <a href="category-pendant-lamps.html">כל מנורות התלייה</a> · <a href="shipping-returns.html">משלוחים והחזרות</a></p>
</div>
</div>

<script type="application/ld+json">
{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
{"@type":"Question","name":"באיזה גובה תולים מנורות מעל אי מטבח?","acceptedAnswer":{"@type":"Answer","text":"75 עד 90 ס\\"מ ממשטח האי ועד תחתית גוף התאורה. 80 ס\\"מ היא נקודת פתיחה טובה בתקרה רגילה."}},
{"@type":"Question","name":"כמה מנורות צריך מעל אי מטבח?","acceptedAnswer":{"@type":"Answer","text":"אי עד 150 ס\\"מ — שתיים. אי של 180 עד 240 ס\\"מ — שלוש."}},
{"@type":"Question","name":"מה המרווח בין מנורות מעל אי?","acceptedAnswer":{"@type":"Answer","text":"60 עד 75 ס\\"מ בין מרכז גוף למרכז הגוף הבא, ו-30 עד 45 ס\\"מ מהגוף הקיצוני ועד קצה האי."}},
{"@type":"Question","name":"מה עושים כשהתקרה נמוכה?","acceptedAnswer":{"@type":"Answer","text":"בוחרים גוף צמוד תקרה מעל האי במקום גוף תלוי, כדי שלא יפריע במעבר."}},
{"@type":"Question","name":"איזו נורה מתאימה מעל אי מטבח?","acceptedAnswer":{"@type":"Answer","text":"אור חם 2700K עד 3000K. Odd ו-Set עובדים עם E27 LED, Opeq ו-Ved עם GU10 LED."}}]}
</script>
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
{"@type":"ListItem","position":1,"name":"בית","item":"https://studioatod.com/"},
{"@type":"ListItem","position":2,"name":"תאורה מעל אי מטבח","item":"https://studioatod.com/island-lamp.html"}]}
</script>
</main>'''

# ---- new page from the dining-lamp template
src = io.open('dining-lamp.html', encoding='utf-8').read()
a, b = src.index('<main'), src.index('</main>') + len('</main>')
page = src[:a] + MAIN + src[b:]
page = re.sub(r'<title>[^<]*</title>', f'<title>{TITLE}</title>', page, count=1)
page = re.sub(r'(<meta name="description" content=")[^"]*', r'\g<1>' + DESC, page, count=1)
page = re.sub(r'(<meta property="og:title" content=")[^"]*', r'\g<1>' + TITLE, page, count=1)
page = re.sub(r'(<meta property="og:description" content=")[^"]*', r'\g<1>' + DESC, page, count=1)
page = page.replace('https://studioatod.com/dining-lamp.html', URL)
assert 'dining-lamp.html"' in page  # only the in-body link back to the dining guide remains
io.open(SLUG, 'w', encoding='utf-8').write(page)
print('CREATED', SLUG)

# ---- sitemap
sm = io.open('sitemap.xml', encoding='utf-8').read()
if SLUG not in sm:
    m = re.search(r'[ \t]*<url>\s*<loc>https://studioatod\.com/dining-lamp\.html</loc>.*?</url>\n?', sm, re.S)
    assert m, 'dining-lamp entry not found in sitemap'
    entry = m.group(0).replace('dining-lamp.html', SLUG)
    entry = re.sub(r'<lastmod>[^<]*</lastmod>', '<lastmod>2026-11-26</lastmod>', entry)
    sm = sm[:m.end()] + entry + sm[m.end():]
    io.open('sitemap.xml', 'w', encoding='utf-8').write(sm)
    print('UPDATED sitemap.xml')

LINK = f'<a href="{SLUG}">תאורה מעל אי מטבח</a>'

# ---- link from the dining guide
d = io.open('dining-lamp.html', encoding='utf-8').read()
if SLUG not in d:
    old = '<a href="collection.html">כל הדגמים</a> · <a href="shipping-returns.html">משלוחים והחזרות</a>'
    assert old in d
    d = d.replace(old, f'{LINK} · {old}', 1)
    io.open('dining-lamp.html', 'w', encoding='utf-8').write(d)
    print('UPDATED dining-lamp.html')

# ---- link from the pendant category line
c = io.open('category-pendant-lamps.html', encoding='utf-8').read()
if SLUG not in c:
    m = re.search(r'(<p class="pagehead__guide">.*?)(</p>)', c, re.S)
    assert m, 'pagehead guide line not found'
    c = c[:m.start(2)] + f' · {LINK}' + c[m.start(2):]
    io.open('category-pendant-lamps.html', 'w', encoding='utf-8').write(c)
    print('UPDATED category-pendant-lamps.html')
