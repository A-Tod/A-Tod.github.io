"""One-off: studio page in four stages + Roie's portrait on the about page.

- tools/about/image.png -> assets/img/roie-danziger.jpg (input removed)
- about.html: portrait replaces the cropped sketch photo; the "חומר גלם רגשי" line is removed
- studio.html: process rewritten as planning, mold, casting, finishing
"""
import io
import os

from PIL import Image

SRC, DST = 'tools/about/image.png', 'assets/img/roie-danziger.jpg'
im = Image.open(SRC).convert('RGB')
if im.width > 1600:
    im = im.resize((1600, round(im.height * 1600 / im.width)), Image.LANCZOS)
im.save(DST, 'JPEG', quality=85, optimize=True, progressive=True)
os.remove(SRC)
print('IMAGE', DST, im.size, os.path.getsize(DST))

SKETCH = 'assets/img/177757_c9548c9ad1e74337a041ae1b4f42d0f5.jpg'

# ---- about.html
p = 'about.html'
t = io.open(p, encoding='utf-8').read()
old_img = f'<img src="{SKETCH}" alt="הדרך לכאן" loading="lazy">'
assert old_img in t
t = t.replace(old_img, f'<img src="{DST}" alt="רועי דנציגר, מייסד הסטודיו" loading="lazy">', 1)
start = t.index('<section class="story wrap">\n<div class="legal">')
end = t.index('</section>', start) + len('</section>\n')
assert 'רגשי' in t[start:end]
t = t[:start] + t[end:]
io.open(p, 'w', encoding='utf-8').write(t)
print('UPDATED', p)

# ---- studio.html
STAGES = f'''<section class="story story--intro wrap">
<div class="legal legal--intro">
<p class="story__text">כל גוף תאורה עובר ארבעה שלבים בסטודיו: תכנון, תבנית, יציקה וגימור. כל שלב נעשה באותו דיוק, כדי שכל גוף ייצא נקי ועקבי עם הדגם.</p>
</div>
</section>
<div class="wrap"><hr class="rule"></div>
<section class="story story--flip wrap">
<div class="story__grid">
<div class="story__media">
<img src="{SKETCH}" alt="שרטוט ידני של דגמים בסטודיו" loading="lazy">
</div>
<div class="story__body">
<h2 class="story__title">התכנון</h2>
<p class="story__text">כל דגם מתחיל בשרטוט ידני ועובר למודל תלת־ממדי. במודל נקבעים הצורה, עובי הדופן, מיקום המפזר והמעבר לחשמל.</p>
<p class="story__text">רק דגם שהפרופורציות שלו מדויקות ממשיך לתבנית.</p>
</div>
</div>
</section>
<section class="story wrap">
<div class="story__grid">
<div class="story__media">
<img src="assets/img/177757_9ae39368535d4d3189022fb30d4ff05af000.jpg" alt="תבנית מודפסת לפני יציקה" loading="lazy">
</div>
<div class="story__body">
<h2 class="story__title">התבנית</h2>
<p class="story__text">התבנית מודפסת בסטודיו בהדפסת תלת־ממד, בשכבות דקות של חומר גמיש, ומשויפת ביד עד שפני השטח חלקים.</p>
<p class="story__text">מאותה תבנית נוצקים כל הגופים של הדגם, ולכן כולם יוצאים באותה צורה ובאותן מידות.</p>
</div>
</div>
</section>
<section class="story story--flip wrap">
<div class="story__grid">
<div class="story__media">
<img src="assets/img/177757_798c49d1ca6f40949f8fc5f31d3483d1f002.jpg" alt="ערבוב הבטון" loading="lazy">
</div>
<div class="story__body">
<h2 class="story__title">היציקה</h2>
<p class="story__text">צמנט, אגרגט ומים נמדדים בכמויות מדויקות ומעורבבים למרקם אחיד. התערובת נמזגת סביב ליבה שמשאירה חלל למעבר החשמל, והתבנית מרודדת כדי לשחרר בועות אוויר.</p>
<p class="story__text">אחרי שעות של התקשות הגוף מחולץ ונבדק לאיתור סדקים. רק גוף שעובר את הבדיקה ממשיך לגימור.</p>
</div>
</div>
</section>
<section class="story wrap">
<div class="story__grid">
<div class="story__media">
<img src="assets/img/177757_df61dc6e5be74edbbd6f584230dcd574f000.jpg" alt="גימור הגוף ביד" loading="lazy">
</div>
<div class="story__body">
<h2 class="story__title">הגימור</h2>
<p class="story__text">המפזר משויף ביד במים, בלי חומרי מילוי או צבע יסוד, כדי שהאור יעבור דרכו באופן אחיד.</p>
<p class="story__text">בסוף הגוף מורכב עם הכבל ובית הנורה.</p>
</div>
</div>
</section>
'''

p = 'studio.html'
t = io.open(p, encoding='utf-8').read()
a = t.index('<section class="story story--intro wrap">')
b = t.index('<div class="wrap" style="text-align:center;padding-bottom:90px">')
t = t[:a] + STAGES + t[b:]
DESC = 'ארבעה שלבים בסטודיו: תכנון, תבנית מודפסת, יציקת בטון וגימור ביד.'
t = t.replace('<meta name="description" content="תהליך היצירה">', f'<meta name="description" content="{DESC}">', 1)
t = t.replace('<meta property="og:description" content="תהליך היצירה">', f'<meta property="og:description" content="{DESC}">', 1)
io.open(p, 'w', encoding='utf-8').write(t)
print('UPDATED', p)
