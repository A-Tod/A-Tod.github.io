#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
מסנכרן את products.txt (הפיד ל-Google Merchant Center) מנתוני האתר עצמו.

למה זה קיים
-----------
הפיד היה קובץ סטטי: שינוי מחיר בדף מוצר או שינוי זמינות ב-stock.json
לא עדכן אותו, ולכן נוצר פער בין מה שגוגל מציג לבין מה שהאתר מציג.
פער כזה גורם ל-Merchant Center לפסול מוצרים
("Mismatched value: price" / "availability").

מה הסקריפט מעדכן, ומה הוא לא נוגע בו
------------------------------------
מתעדכן אוטומטית (השדות שמשתנים בפועל):
  price          <- data-price של כפתור ההזמנה בדף המוצר
  availability   <- stock.json  (in -> in_stock, out -> out_of_stock)
  image_link     <- data-img של כפתור ההזמנה, כתובת מוחלטת

נשאר בדיוק כפי שהוא (תוכן שנכתב ביד):
  id, title, description, link, condition, brand, mpn

כך הפורמט והכתובות הקיימות נשמרים, ושום טקסט שיווקי לא נדרס.

הרצה: python3 tools/sync_feed.py   (מתיקיית השורש של המאגר)
       --check  מוודא בלבד ומחזיר קוד יציאה 1 אם יש פער, בלי לכתוב.
"""

import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FEED = os.path.join(ROOT, "products.txt")
STOCK = os.path.join(ROOT, "stock.json")
BASE = "https://studioatod.com/"

AVAIL = {"in": "in_stock", "out": "out_of_stock"}
DEFAULT_AVAIL = "in_stock"          # מוצר שלא מופיע ב-stock.json נחשב במלאי

CTA = re.compile(r"<button[^>]*\bclass=\"[^\"]*pdp__cta[^\"]*\"[^>]*>", re.I)
ATTR = lambda name: re.compile(r"data-%s=\"([^\"]*)\"" % name, re.I)


def read_stock():
    with open(STOCK, encoding="utf-8") as f:
        raw = json.load(f)
    # מפתחות שמתחילים ב-_ הם הערות הסבר בתוך הקובץ, לא מוצרים
    return {k: v for k, v in raw.items() if not k.startswith("_")}


def page_data(slug):
    """מחזיר {'price':..., 'image':...} מדף המוצר, או None אם אין דף."""
    path = os.path.join(ROOT, "product-%s.html" % slug)
    if not os.path.exists(path):
        return None
    html = open(path, encoding="utf-8").read()
    m = CTA.search(html)
    if not m:
        return None
    tag = m.group(0)
    price = ATTR("price").search(tag)
    image = ATTR("img").search(tag)
    if not price:
        return None
    return {
        "price": price.group(1).strip(),
        "image": image.group(1).strip() if image else None,
    }


def money(value):
    """'1350' -> '1350.00 ILS' — בדיוק הפורמט שהפיד משתמש בו היום."""
    return "%.2f ILS" % float(str(value).replace(",", "").strip())


def absolute(url):
    if not url:
        return None
    return url if url.startswith("http") else BASE + url.lstrip("/")


def main():
    check_only = "--check" in sys.argv

    with open(FEED, encoding="utf-8") as f:
        lines = f.read().rstrip("\n").split("\n")

    header = lines[0].split("\t")
    col = {name: i for i, name in enumerate(header)}
    for needed in ("link", "price", "availability", "image_link"):
        if needed not in col:
            sys.exit("products.txt: חסרה עמודה %s" % needed)

    stock = read_stock()
    seen, changes, warnings = set(), [], []
    out = [lines[0]]

    for line in lines[1:]:
        if not line.strip():
            continue
        row = line.split("\t")
        if len(row) != len(header):
            sys.exit("products.txt: שורה עם %d עמודות במקום %d" % (len(row), len(header)))

        link = row[col["link"]]
        m = re.search(r"product-([a-z0-9]+)\.html", link, re.I)
        if not m:
            warnings.append("לא זוהה slug בכתובת %s — השורה נשארה כפי שהיא" % link)
            out.append(line)
            continue
        slug = m.group(1).lower()
        seen.add(slug)

        data = page_data(slug)
        if not data:
            warnings.append("לא נמצא דף מוצר או כפתור הזמנה עבור %s — השורה נשארה כפי שהיא" % slug)
            out.append(line)
            continue

        for field, new in (
            ("price", money(data["price"])),
            ("availability", AVAIL.get(str(stock.get(slug, "in")).lower(), DEFAULT_AVAIL)),
            ("image_link", absolute(data["image"]) or row[col["image_link"]]),
        ):
            old = row[col[field]]
            if old != new:
                changes.append("%s · %s: %s -> %s" % (slug, field, old, new))
                row[col[field]] = new

        out.append("\t".join(row))

    for slug in sorted(set(stock) - seen):
        warnings.append("%s מופיע ב-stock.json אך לא בפיד — יש להוסיף שורה ידנית עם כותרת ותיאור" % slug)

    for w in warnings:
        print("אזהרה: " + w)

    if not changes:
        print("products.txt מעודכן. אין פערים במחיר, בזמינות או בתמונה.")
        return 0

    print("נמצאו %d פערים:" % len(changes))
    for c in changes:
        print("  " + c)

    if check_only:
        return 1

    with open(FEED, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(out) + "\n")
    print("products.txt נכתב מחדש.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
