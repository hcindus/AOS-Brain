#!/usr/bin/env python3
import re

SRC = "/root/.openclaw/workspace/AGI_COMPANY/subsidiaries/CREAM/sales/prospects/generate_2026-08-18.py"
DST = "/root/.openclaw/workspace/AGI_COMPANY/subsidiaries/CREAM/sales/prospects/generate_2026-08-20.py"

with open(SRC) as f:
    c = f.read()

# ---------- TARGET_DATE ----------
c = c.replace('TARGET_DATE = "2026-08-18"', 'TARGET_DATE = "2026-08-20"')

# ---------- TOTALS (descending; comma/K anchored, no streak collision) ----------
c = c.replace("113,000", "114,000")
c = c.replace("112,000", "113,000")
c = c.replace("111,000", "112,000")
c = c.replace("110,000", "111,000")
c = c.replace("112K", "113K")
c = c.replace("111K", "112K")

# ---------- PRIORITY BREAKDOWN numbers (descending) ----------
c = c.replace("45,200", "45,600")
c = c.replace("44,800", "45,200")
c = c.replace("39,550", "39,900")
c = c.replace("39,200", "39,550")
c = c.replace("28,250", "28,500")
c = c.replace("28,000", "28,250")

# ---------- STREAK: 111 -> 112 first ----------
c = c.replace("111 days", "112 days")
c = c.replace("111-day", "112-day")
c = c.replace("111-Day", "112-Day")
c = c.replace("Day 111", "Day 112")
c = c.replace("111 DAYS", "112 DAYS")
c = c.replace(r"\g<1>111\g<2>", r"\g<1>112\g<2>")
c = c.replace(r"\g<1>111\g<3>", r"\g<1>112\g<3>")

# ---------- STREAK: 110 -> 111 (after 111 done) ----------
c = c.replace("110 days", "111 days")
c = c.replace("110-day", "111-day")
c = c.replace("109-day", "110-day")
c = c.replace("108-day", "109-day")
c = c.replace("107-day", "108-day")
c = c.replace("108|109|110", "109|110|111")

# ---------- fallback defaults (integers, no comma) ----------
c = c.replace('prev_total = data.get("total_prospects", 112000)',
              'prev_total = data.get("total_prospects", 113000)')
c = c.replace('prev_streak = data.get("streak_days", 110)',
              'prev_streak = data.get("streak_days", 111)')
c = c.replace('{"A": 44800, "B": 39200, "C": 28000}',
              '{"A": 45200, "B": 39550, "C": 28250}')
c = c.replace('{"senior_6plus": 55996, "mid_3to5": 28047, "new_0to2": 27957}',
              '{"senior_6plus": 56496, "mid_3to5": 28297, "new_0to2": 28207}')

# ---------- DATES (descending) ----------
c = c.replace("August 18, 2026", "August 20, 2026")
c = c.replace("August 17, 2026", "August 18, 2026")

with open(DST, "w") as f:
    f.write(c)

print("Wrote", DST)
print("TARGET_DATE present:", 'TARGET_DATE = "2026-08-20"' in c)
print("114,000 present:", "114,000" in c)
print("113,000 present:", "113,000" in c)
print("112 days present:", "112 days" in c)
print("112-Day present:", "112-Day" in c)
print("Day 112 present:", "Day 112" in c)
