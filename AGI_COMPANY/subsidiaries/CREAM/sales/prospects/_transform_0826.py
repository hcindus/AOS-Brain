#!/usr/bin/env python3
"""Transform generate_2026-08-25.py -> generate_2026-08-26.py"""
import io

SRC = "generate_2026-08-25.py"
DST = "generate_2026-08-26.py"

with open(SRC, "r", encoding="utf-8") as f:
    c = f.read()

# Ordered (old, new) replacements. Order matters to avoid cascades.
repls = [
    # Phase 1 — ISO date
    ("2026-08-25", "2026-08-26"),
    # Phase 2 — human dates
    ("August 24, 2026", "August 25, 2026"),
    ("August 23, 2026", "August 25, 2026"),
    ("August 25, 2026", "August 26, 2026"),
    # Phase 3 — counts (descending thousands)
    ("118,000", "119,000"),
    ("117,000", "118,000"),
    ("116,000", "117,000"),
    # Phase 4 — streak numbers (descending)
    ("116-day", "117-day"),
    ("116-Day", "117-Day"),
    ("116 days", "117 days"),
    ("116 DAYS", "117 DAYS"),
    ("Day 116", "Day 117"),
    ("116K \u2192 117K", "117K \u2192 118K"),
    ("115-day", "116-day"),
    ("114-day", "115-day"),
    ("113-day", "114-day"),
    ("112-day", "113-day"),
    ("115 days", "116 days"),
    # Phase 5 — numeric defaults
    ("116000", "117000"),
    ('"streak_days", 114', '"streak_days", 115'),
    ('{"A": 46400, "B": 40600, "C": 29000}', '{"A": 46800, "B": 40950, "C": 29250}'),
    ('{"senior_6plus": 57996, "mid_3to5": 29047, "new_0to2": 28957}',
     '{"senior_6plus": 58496, "mid_3to5": 29297, "new_0to2": 29207}'),
    # Phase 6 — regex literals
    (r'\g<1>116\g<2>', r'\g<1>117\g<2>'),
    ("(112|113|114)", "(113|114|115)"),
    (r'\g<1>116\g<3>', r'\g<1>117\g<3>'),
]

for old, new in repls:
    c = c.replace(old, new)

with open(DST, "w", encoding="utf-8") as f:
    f.write(c)

print("Wrote", DST)
