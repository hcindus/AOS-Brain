#!/usr/bin/env python3
"""Transform generate_2026-08-26.py -> generate_2026-08-28.py"""
import re

src = "/root/.openclaw/workspace/AGI_COMPANY/subsidiaries/CREAM/sales/prospects/generate_2026-08-26.py"
dst = "/root/.openclaw/workspace/AGI_COMPANY/subsidiaries/CREAM/sales/prospects/generate_2026-08-28.py"

s = open(src, encoding='utf-8').read()

# ---- Dates (token approach, oldest-first) ----
s = s.replace("August 26, 2026", "@D26@")
s = s.replace("August 25, 2026", "@D25@")
s = s.replace("August 24, 2026", "@D24@")
s = s.replace("@D24@", "August 26, 2026")
s = s.replace("@D25@", "August 27, 2026")
s = s.replace("@D26@", "August 28, 2026")

# ISO target date
s = s.replace("2026-08-26", "2026-08-28")

# ---- Comma counts (high -> low) ----
s = s.replace("119,000", "120,000")
s = s.replace("118,000", "119,000")
s = s.replace("117,000", "118,000")

# ---- No-comma count default ----
s = s.replace("117000", "118000")

# ---- K-abbrev exact phrase ----
s = s.replace("117K \u2192 118K", "118K \u2192 119K")

# ---- Priority totals (high -> low) ----
s = s.replace("47,600", "48,000").replace("47,200", "47,600")
s = s.replace("41,650", "42,000").replace("41,300", "41,650")
s = s.replace("29,750", "30,000").replace("29,500", "29,750")

# ---- Streak suffixed (high -> low) ----
s = s.replace("117 DAYS", "118 DAYS")
s = s.replace("117 days", "118 days")
s = s.replace("117-day", "118-day")
s = s.replace("117-Day", "118-Day")
s = s.replace("Day 117", "Day 118")
s = s.replace("116 days", "117 days")
s = s.replace("116-day", "117-day")
s = s.replace("115-day", "116-day")
s = s.replace("114-day", "115-day")
s = s.replace("113-day", "114-day")

# ---- regex internals ----
s = s.replace("(113|114|115)", "(114|115|116)")
s = s.replace("r'\\g<1>117\\g<2>'", "r'\\g<1>118\\g<2>'")
s = s.replace("r'\\g<1>117\\g<3>'", "r'\\g<1>118\\g<3>'")

# ---- prev_streak default ----
s = s.replace('"streak_days", 115', '"streak_days", 116')

open(dst, 'w', encoding='utf-8').write(s)
print("Wrote", dst)
print("Remaining '117':", s.count("117"), "| '119,000':", s.count("119,000"), "| '120,000':", s.count("120,000"))
print("Remaining 'Aug 26':", s.count("August 26, 2026"), "| 'Aug 28':", s.count("August 28, 2026"))
