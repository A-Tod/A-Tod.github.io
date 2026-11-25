import re, sys, io

TPL = 'shipping-returns.html'
OUT = 'dining-lamp.html'
URL = 'https://studioatod.com/dining-lamp.html'
TITLE = 'מנורה לפינת אוכל — מדריך בחירה ותלייה | a-tod'
DESC = 'באיזה גובה תולים מנורה מעל שולחן האוכל, איזה קוטר מתאים וכמה גופים צריך. מדריך קצר, ואחריו גופי תאורה מבטון בעבודת יד לפינת אוכל.'
TODAY = '2026-11-25'

s = open(TPL, encoding='utf-8').read()
i = s.index('<main')
k = s.index('</main>') + len('</main>')
head, tail = s[:i], s[k:]

def one(pat, repl, txt, label):
    out, n = re.subn(pat, repl, txt, count=0, flags=re.S)
    if n != 1:
        print('GUARD FAIL ' + label + ' n=' + str(n)); sys.exit(1)
    return out

head = one(r'<title>.*?</title>', '<title>' + TITLE + '</title>', head, 'title')
head = one(r'<meta name="description" content=".*?">', '<meta name="description" content="' + DESC + '">', head, 'desc')
head = one(r'<meta property="og:title" content=".*?">', '<meta property="og:title" content="' + TITLE + '">', head, 'ogtitle')
head = one(r'<meta property="og:description" content=".*?">', '<meta property="og:description" content="' + DESC + '">', head, 'ogdesc')
head = one(r'<link rel="canonical" href=".*?">', '<link rel="canonical" href="' + URL + '">', head, 'canonical')
head = one(r'<meta property="og:url" content=".*?">', '<meta property="og:url" content="' + URL + '">', head, 'ogurl')

MAIN = '''<main id="main">
  <div class="wrap">
    <nav class="crumbs" aria-label="מיקום"><a href="index.html">בית</a><span>›</span>מנורה לפינת אוכל</nav>
  </div>

  <div class="wrap">
    <header class="pagehead">
      <h1>מנורה לפינת אוכל</h1>
      <p>באיזה גובה תולים, איזה קוטר מתאים וכמה גופים צריך. מדריך קצר, ואחריו הדגמים מבטון בעבודת יד שמתאימים לשולחן אוכל.</p>
    </header>

    <div class="legal legal--intro">
      <p>התאורה מעל שולחן האוכל היא היחידה בבית שיושבים מתחתיה שעה שלמה, בגובה העיניים, מול אנשים אחרים. לכן דווקא בה גובה התלייה והקוטר קובעים יותר מהעיצוב: גוף יפה שתלוי לא נכון יחסום מבט, יסנוור או ייראה קטן ואבוד מעל השולחן. שלושת המספרים שלמטה פותרים את רוב העבודה.</p>
    </div>
  </div>

  <div class="wrap">
    <div class="legal">
      <h2>גובה התלייה — 75 עד 90 ס"מ ממשטח השולחן</h2>
      <p>המרחק נמדד ממשטח השולחן ועד תחתית גוף התאורה, לא מהתקרה. 80 ס"מ היא נקודת פתיחה טובה כמעט בכל בית. בתקרה גבוהה מ-2.70 מ' אפשר לעלות ל-85 עד 90 ס"מ, ובפינת אוכל קומפקטית לרדת ל-75.</p>
      <p>הכלל שמאחורי המספר פשוט: הגוף צריך להיות גבוה מספיק כדי שלא יחסום מבט בין שני אנשים שיושבים משני צדי השולחן, ונמוך מספיק כדי שהנורה עצמה לא תיראה מהכיסא. אם מי שיושב רואה את הנורה — הגוף גבוה מדי.</p>
      <p>בכל הדגמים כאן אורך הכבל 150 ס"מ, והגובה הסופי נקבע בהתקנה לפי גובה התקרה.</p>

      <h2>כמה גופים, ובאיזה מרווח</h2>
      <p>שולחן עגול עד 90 ס"מ, או שולחן לשניים — גוף אחד במרכז. שולחן ל-4 עד 6 אנשים, בדרך כלל 140 עד 180 ס"מ — שני גופים. שולחן ארוך מ-200 ס"מ — שלושה.</p>
      <p>בשורה של כמה גופים: מרווח 60 עד 75 ס"מ בין גוף לגוף, ולפחות 30 ס"מ מהגוף הקרוב ביותר ועד קצה השולחן. את הגופים תולים על ציר אחד במקביל לשולחן; פיזור בלי ציר הוא מה שגורם לתאורה להיראות מקרית ולא מתוכננת.</p>

      <h2>קוטר — חצי עד שני שליש מרוחב השולחן</h2>
      <p>הכלל המקובל: רוחב התאורה הכולל הוא כחצי עד שני שליש מרוחב השולחן. בגוף בודד זה הקוטר שלו. בשורה מחשבים את סך הקטרים ועוד המרווחים ביניהם.</p>
      <p>הדגמים של a-tod קטנים בכוונה: Odd בקוטר 15 ס"מ, Set 23 ס"מ, Opeq ו-Ved 9 ס"מ. מכאן נובע איך משתמשים בהם — גוף בודד מתאים לשולחן עגול קטן, לשולחן לשניים או לאי מטבח צר, ומעל שולחן ל-6 אנשים גוף אחד ייראה אבוד. שם עובדת שורה של שניים עד שלושה, וזה גם נראה טוב יותר מגוף אחד גדול.</p>

      <h2>עגול או מלבני</h2>
      <p>שולחן עגול או ריבועי — גוף אחד במרכז, או שלושה צמודים יחסית. שולחן מלבני או שולחן בר — שורה לאורך. התאמת צורת התאורה לצורת השולחן היא ההחלטה שהעין מזהה מיד, עוד לפני הסגנון או החומר.</p>

      <h2>איזה אור ואיזו נורה</h2>
      <p>מעל שולחן אוכל רוצים אור חם, 2700K, שנופל על השולחן ולא מציף את כל החדר. דימר הוא התוספת שמשנה הכי הרבה: אותה פינה משמשת גם לארוחת בוקר וגם לשבת בערב.</p>
      <p>Odd ו-Set עובדים עם נורת E27 LED. Opeq ו-Ved עם GU10 LED. הבטון מט, בולע השתקפויות, והאור שיוצא ממנו רך ולא מסנוור מהכיסא.</p>
    </div>
  </div>

  <div class="wrap">
    <div class="legal legal--intro">
      <h2>הדגמים שמתאימים לפינת אוכל</h2>
      <p>כל גוף נוצק ביד בסטודיו, אחד בכל פעם. אין שני גופים זהים — הגוון, המרקם והמיקרו-בועות משתנים מיציקה ליציקה. מעל שולחן אוכל זה בדיוק העניין: זה האובייקט שמסתכלים עליו בכל ארוחה.</p>
    </div>
    <div class="grid-products">
      <a class="card" href="product-odd.html">
        <div class="card__media">
<img src="assets/img/177757_8f2b36f360ce4fa0abd96aa516981f3e.jpg" alt="Odd — מנורת תלייה מבטון לפינת אוכל" loading="lazy"><img src="assets/img/177757_eb3300f976ef4192a6618224be7eab7e.jpg" alt="" loading="lazy">
        </div>
        <div class="card__name">Odd</div>
        <div class="card__price">₪950</div>
      </a>
      <a class="card" href="product-set.html">
        <div class="card__media">
<img src="assets/img/177757_1bf9f50b4e7c4bc8a70c651b64fba593.jpg" alt="Set — מנורת תלייה מבטון לשולחן אוכל ולמזנון" loading="lazy"><img src="assets/img/177757_9ca70ab9b79446bc932ad2e77584bd90.jpg" alt="" loading="lazy">
        </div>
        <div class="card__name">Set</div>
        <div class="card__price">₪1,350</div>
      </a>
      <a class="card" href="product-opeq.html">
        <div class="card__media">
<img src="assets/img/177757_60d23ea1a2ef43bbaef6cd381697c685.jpg" alt="Opeq — מנורת תלייה קטנה מבטון לשורה מעל שולחן" loading="lazy"><img src="assets/img/177757_8c0b6359bdce4116929fee2a3bbb75c0.jpg" alt="" loading="lazy">
        </div>
        <div class="card__name">Opeq</div>
        <div class="card__price">₪750</div>
      </a>
      <a class="card" href="product-ved.html">
        <div class="card__media">
<img src="assets/img/177757_59c6c9a2e8c148779e94d47d0e948d7c.jpg" alt="Ved — מנורת תלייה קטנה מבטון לשורה מעל שולחן" loading="lazy"><img src="assets/img/177757_9a7590c9515b4a3b93a91ce2f57e8a82.jpg" alt="" loading="lazy">
        </div>
        <div class="card__name">Ved</div>
        <div class="card__price">₪750</div>
      </a>
    </div>
  </div>

  <div class="wrap">
    <div class="legal">
      <h2>שאלות נפוצות</h2>
      <p><strong>באיזה גובה תולים מנורה מעל שולחן אוכל?</strong><br>75 עד 90 ס"מ ממשטח השולחן ועד תחתית גוף התאורה. 80 ס"מ נקודת פתיחה טובה; בתקרה גבוהה מ-2.70 מ' אפשר 85 עד 90.</p>
      <p><strong>כמה גופי תאורה צריך מעל שולחן אוכל?</strong><br>שולחן עגול או שולחן לשניים — אחד. שולחן ל-4 עד 6 אנשים — שניים. שולחן ארוך מ-200 ס"מ — שלושה. מרווח 60 עד 75 ס"מ ביניהם, ולפחות 30 ס"מ מקצה השולחן.</p>
      <p><strong>איזה קוטר מנורה מתאים לשולחן אוכל?</strong><br>רוחב התאורה הכולל כחצי עד שני שליש מרוחב השולחן. בשורה של כמה גופים מחשבים את סך הקטרים והמרווחים.</p>
      <p><strong>אפשר לתלות מנורת בטון מעל שולחן אוכל?</strong><br>כן. הדגמים כאן שוקלים בין 0.5 ל-1.2 ק"ג, כמו גוף תאורה רגיל, ונתלים מנקודת חשמל סטנדרטית בתקרה.</p>
      <p><strong>איזו נורה מתאימה?</strong><br>Odd ו-Set — E27 LED. Opeq ו-Ved — GU10 LED. אור חם 2700K, ורצוי על דימר.</p>
      <p><a href="collection.html">כל הדגמים</a> · <a href="shipping-returns.html">משלוחים והחזרות</a></p>
    </div>
  </div>

  <script type="application/ld+json">
  {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
   {"@type":"Question","name":"באיזה גובה תולים מנורה מעל שולחן אוכל?","acceptedAnswer":{"@type":"Answer","text":"75 עד 90 ס\\"מ ממשטח השולחן ועד תחתית גוף התאורה. 80 ס\\"מ היא נקודת פתיחה טובה; בתקרה גבוהה מ-2.70 מ׳ אפשר 85 עד 90."}},
   {"@type":"Question","name":"כמה גופי תאורה צריך מעל שולחן אוכל?","acceptedAnswer":{"@type":"Answer","text":"שולחן עגול או שולחן לשניים — גוף אחד. שולחן ל-4 עד 6 אנשים — שניים. שולחן ארוך מ-200 ס\\"מ — שלושה. מרווח 60 עד 75 ס\\"מ ביניהם, ולפחות 30 ס\\"מ מקצה השולחן."}},
   {"@type":"Question","name":"איזה קוטר מנורה מתאים לשולחן אוכל?","acceptedAnswer":{"@type":"Answer","text":"רוחב התאורה הכולל הוא כחצי עד שני שליש מרוחב השולחן. בשורה של כמה גופים מחשבים את סך הקטרים והמרווחים ביניהם."}},
   {"@type":"Question","name":"אפשר לתלות מנורת בטון מעל שולחן אוכל?","acceptedAnswer":{"@type":"Answer","text":"כן. דגמי a-tod שוקלים בין 0.5 ל-1.2 ק\\"ג, כמו גוף תאורה רגיל, ונתלים מנקודת חשמל סטנדרטית בתקרה."}},
   {"@type":"Question","name":"איזו נורה מתאימה למנורה מעל שולחן האוכל?","acceptedAnswer":{"@type":"Answer","text":"Odd ו-Set עובדים עם E27 LED, Opeq ו-Ved עם GU10 LED. מומלץ אור חם 2700K על דימר."}}]}
  </script>
  <script type="application/ld+json">
  {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
   {"@type":"ListItem","position":1,"name":"בית","item":"https://studioatod.com/"},
   {"@type":"ListItem","position":2,"name":"מנורה לפינת אוכל","item":"https://studioatod.com/dining-lamp.html"}]}
  </script>
</main>'''

open(OUT, 'w', encoding='utf-8').write(head + MAIN + tail)
print('wrote ' + OUT + ' ' + str(len(head + MAIN + tail)))

# sitemap: clone the collection.html entry
sm = open('sitemap.xml', encoding='utf-8').read()
m = re.search(r'<url>(?:(?!</url>).)*collection\.html(?:(?!</url>).)*</url>', sm, re.S)
if not m:
    print('GUARD FAIL sitemap entry not found'); sys.exit(1)
if 'dining-lamp.html' in sm:
    print('GUARD FAIL already in sitemap'); sys.exit(1)
block = m.group(0)
nb = block.replace('collection.html', 'dining-lamp.html')
nb = re.sub(r'<lastmod>.*?</lastmod>', '<lastmod>' + TODAY + '</lastmod>', nb, flags=re.S)
sm = sm[:m.end()] + '\n' + nb + sm[m.end():]
open('sitemap.xml', 'w', encoding='utf-8').write(sm)
print('sitemap ok')

# internal link from the collection page
c = open('collection.html', encoding='utf-8').read()
if c.count('<header class="pagehead">') != 1:
    print('GUARD FAIL collection pagehead'); sys.exit(1)
if 'dining-lamp.html' in c:
    print('GUARD FAIL collection already linked'); sys.exit(1)
link = '      <p>מחפשים תאורה לשולחן האוכל? <a href="dining-lamp.html">מדריך בחירת מנורה לפינת אוכל</a> — גובה תלייה, קוטר וכמה גופים.</p>\n'
j = c.index('<header class="pagehead">')
e = c.index('</header>', j)
c = c[:e] + link + c[e:]
open('collection.html', 'w', encoding='utf-8').write(c)
print('collection ok')
