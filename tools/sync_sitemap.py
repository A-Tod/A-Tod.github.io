#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
מייצר את sitemap.xml מהעמודים שקיימים בפועל במאגר.

למה זה קיים
-----------
מפת האתר הייתה קובץ שנכתב ביד. עמוד חדש לא נכנס אליה, עמוד שנמחק נשאר בה,
ולא היה בה <lastmod> — ולכן לגוגל לא הייתה שום אינדיקציה מתי עמוד השתנה,
והיא סרקה מחדש לפי קצב משלה.

מה הסקריפט עושה
---------------
  • עובר על קובצי ה-HTML בשורש המאגר
  • מדלג על עמוד עם <meta name="robots" content="noindex"> ועל 404.html
  • מוסיף <lastmod> מתאריך הקומיט האחרון שנגע בקובץ (git log)
  • שומר על סדר הכתובות שכבר קיים ב-sitemap.xml, ומוסיף עמודים חדשים בסוף

מה הוא לא עושה
--------------
לא ממציא כתובות ולא משנה כתובות קיימות. עמוד שכבר במפה נשאר באותו מקום
ובאותה כתובת בדיוק; רק ה-lastmod שלו מתרענן.

הרצה: python3 tools/sync_sitemap.py   (מתיקיית השורש של המאגר)
       --check  מוודא בלבד ומחזיר קוד יציאה 1 אם יש פער, בלי לכתוב.
"""

import os
import re
import subprocess
import sys
import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITEMAP = os.path.join(ROOT, "sitemap.xml")
BASE = "https://studioatod.com/"

# עמודים שלא נכנסים למפה גם אם אין בהם noindex
EXCLUDE = {"404.html"}

NOINDEX = re.compile(
    r"<meta[^>]+name=[\"']robots[\"'][^>]+content=[\"'][^\"']*noindex", re.I)
LOC = re.compile(r"<loc>\s*([^<\s]+)\s*</loc>", re.I)


def indexable_files():
    """שמות קובצי ה-HTML בשורש שאמורים להיכנס למפה."""
    out = []
    for name in sorted(os.listdir(ROOT)):
        if not name.endswith(".html") or name in EXCLUDE:
            continue
        with open(os.path.join(ROOT, name), encoding="utf-8") as f:
            head = f.read(4000)
        if NOINDEX.search(head):
            continue
        out.append(name)
    return out


def url_of(name):
    return BASE if name == "index.html" else BASE + name


def name_of(url):
    tail = url[len(BASE):] if url.startswith(BASE) else url
    return "index.html" if tail in ("", "/") else tail.lstrip("/")


def lastmod(name):
    """תאריך הקומיט האחרון שנגע בקובץ. אם אין היסטוריה — תאריך השינוי בדיסק."""
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%cI", "--", name],
            cwd=ROOT, capture_output=True, text=True, timeout=30)
        stamp = out.stdout.strip()
        if stamp:
            return stamp[:10]
    except Exception:
        pass
    ts = os.path.getmtime(os.path.join(ROOT, name))
    return datetime.date.fromtimestamp(ts).isoformat()


def existing_order():
    """סדר הכתובות במפה הקיימת, כדי לא לטרוף אותו."""
    if not os.path.exists(SITEMAP):
        return []
    with open(SITEMAP, encoding="utf-8") as f:
        return [name_of(u) for u in LOC.findall(f.read())]


def build():
    files = indexable_files()
    have = set(files)

    ordered = [n for n in existing_order() if n in have]
    seen = set(ordered)
    added = [n for n in files if n not in seen]
    ordered += added

    dropped = [n for n in existing_order() if n not in have]

    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for n in ordered:
        lines.append('  <url><loc>%s</loc><lastmod>%s</lastmod></url>'
                     % (url_of(n), lastmod(n)))
    lines.append('</urlset>')
    return "\n".join(lines) + "\n", added, dropped


def main():
    check_only = "--check" in sys.argv
    new, added, dropped = build()

    for n in added:
        print("נוסף למפה: " + n)
    for n in dropped:
        print("הוסר מהמפה (הקובץ אינו קיים או מסומן noindex): " + n)

    old = ""
    if os.path.exists(SITEMAP):
        with open(SITEMAP, encoding="utf-8") as f:
            old = f.read()

    if old == new:
        print("sitemap.xml מעודכן. %d כתובות." % new.count("<loc>"))
        return 0

    print("sitemap.xml אינו תואם למצב המאגר (%d כתובות לאחר העדכון)."
          % new.count("<loc>"))
    if check_only:
        return 1

    with open(SITEMAP, "w", encoding="utf-8", newline="\n") as f:
        f.write(new)
    print("sitemap.xml נכתב מחדש.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
