#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
סורק את הקבצים שהדפדפן מוריד, ומחפש מפתחות וסודות שדלפו לצד הלקוח.

למה זה קיים
-----------
כל קובץ שהאתר מגיש — HTML, JS, CSS, JSON — נפתח אצל כל מבקר בלחיצת F12.
מפתח API אמיתי שנכנס לשם הוא מפתח ציבורי, גם אם הוא "מוסתר" באמצע הקוד.
באתר הזה הסליקה רצה דרך Make, ולכן פרטי גרו לא אמורים להופיע באתר בכלל.
הסקריפט הזה הוא רשת ביטחון: הוא נכשל בקול אם משהו כזה יידחף בטעות.

מה נסרק
-------
קובצי HTML בשורש, וכל מה שמתחת ל-assets/ מסוג js/css/json/txt/xml,
וגם products.txt, stock.json, sitemap.xml ו-robots.txt.
tools/ ו-.github/ אינם מוגשים לדפדפן ולכן אינם נסרקים.

ערכים ציבוריים מוכרים
---------------------
חלק מהמזהים אמורים להיות גלויים — מזהה Google Analytics, מפתח publishable
של ספק סליקה, מפתח Google Maps לדפדפן. הם ברשימת ההיתר למטה.

הדפסה בטוחה
-----------
ממצא מודפס ממוסך (ארבעה תווים ראשונים בלבד). הלוג של Actions גלוי,
ואין טעם להדליף שם את מה שבדיוק מצאנו.

הרצה: python3 tools/scan_secrets.py   (מתיקיית השורש של המאגר)
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SCAN_DIRS = ["assets"]
SCAN_EXT = {".html", ".js", ".css", ".json", ".txt", ".xml"}
SKIP_DIRS = {".git", ".github", "tools", "node_modules"}
# תיקיות נכסים שאינן טקסט
SKIP_PATH_PARTS = {os.path.join("assets", "img"), os.path.join("assets", "3d"),
                   os.path.join("assets", "fonts")}

# ערכים שמותר להם להופיע בצד הלקוח
ALLOW = [
    re.compile(r"G-[A-Z0-9]{8,}"),                 # מזהה Google Analytics — ציבורי בהגדרה
    re.compile(r"hook\.(eu|us)\d*\.make\.com"),    # כתובת הוובהוק של Make
    re.compile(r"pk_(live|test)_"),                # מפתח publishable — ציבורי בהגדרה
    re.compile(r"fonts\.(googleapis|gstatic)\.com"),
    re.compile(r"unpkg\.com|cdnjs\.cloudflare\.com|cdn\.jsdelivr\.net"),
]

# תבניות של סודות אמיתיים
RULES = [
    ("מפתח סודי של Stripe",      re.compile(r"\b(sk|rk)_(live|test)_[A-Za-z0-9]{16,}")),
    ("מפתח Google API",          re.compile(r"\bAIza[0-9A-Za-z\-_]{35}\b")),
    ("מפתח AWS",                 re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("טוקן GitHub",              re.compile(r"\b(gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{20,})")),
    ("טוקן Slack",               re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}")),
    ("מפתח SendGrid",            re.compile(r"\bSG\.[A-Za-z0-9_\-]{16,}\.[A-Za-z0-9_\-]{16,}")),
    ("מפתח פרטי",                re.compile(r"-----BEGIN (?:RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----")),
    ("טוקן JWT",                 re.compile(r"\beyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}")),
    ("כותרת Authorization",      re.compile(r"[Aa]uthorization['\"]?\s*[:=]\s*['\"]\s*(?:Bearer|Basic)\s+\S{12,}")),
    ("פרטי גרו / משולם",         re.compile(r"\b(pageCode|userId|apiKey)\s*[:=]\s*['\"][A-Za-z0-9_\-]{8,}['\"]")),
    ("השמה של סוד",              re.compile(r"\b(api[_-]?key|apikey|secret|client[_-]?secret|password|passwd|access[_-]?token|private[_-]?key)\s*[:=]\s*['\"][^'\"]{12,}['\"]", re.I)),
]


def wanted(path):
    rel = os.path.relpath(path, ROOT)
    parts = rel.split(os.sep)
    if parts[0] in SKIP_DIRS:
        return False
    for skip in SKIP_PATH_PARTS:
        if rel.startswith(skip + os.sep):
            return False
    if os.path.splitext(rel)[1].lower() not in SCAN_EXT:
        return False
    # קובצי שורש: רק אלה שמוגשים באמת
    if len(parts) == 1:
        return rel.endswith(".html") or rel in {"products.txt", "stock.json",
                                                "sitemap.xml", "robots.txt"}
    return parts[0] in SCAN_DIRS


def files():
    for base, dirs, names in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for n in names:
            p = os.path.join(base, n)
            if wanted(p):
                yield p


def allowed(hit):
    return any(a.search(hit) for a in ALLOW)


def mask(hit):
    hit = hit.strip()
    return hit[:4] + "…" + ("%d תווים" % len(hit))


def main():
    findings = []
    scanned = 0
    for path in sorted(files()):
        scanned += 1
        try:
            with open(path, encoding="utf-8", errors="replace") as f:
                lines = f.read().split("\n")
        except OSError as e:
            print("לא ניתן לקרוא %s: %s" % (path, e))
            continue
        for i, line in enumerate(lines, 1):
            if "scan-ok" in line:          # סימון ידני לשורה שנבדקה ואושרה
                continue
            for name, rx in RULES:
                for m in rx.finditer(line):
                    hit = m.group(0)
                    if allowed(hit):
                        continue
                    findings.append((os.path.relpath(path, ROOT), i, name, mask(hit)))

    print("נסרקו %d קבצים שהאתר מגיש לדפדפן." % scanned)

    if not findings:
        print("לא נמצאו מפתחות או סודות בצד הלקוח.")
        return 0

    print("")
    print("נמצאו %d ממצאים. כל אחד מהם גלוי לכל מי שפותח F12 באתר:" % len(findings))
    for rel, line, name, masked in findings:
        print("  %s שורה %d — %s: %s" % (rel, line, name, masked))
    print("")
    print("מה לעשות: להוציא את הערך מהקוד שהדפדפן מוריד, להעביר אותו לשרת")
    print("או ל-Make, ולבטל את המפתח הקיים אצל הספק — הוא כבר נחשף.")
    print("אם זה ערך שאמור להיות ציבורי, אפשר להוסיף לשורה הערה שמכילה scan-ok.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
