#!/usr/bin/env python3
"""Patch generate_2026-08-29.py -> generate_2026-08-31.py (date/count/streak bumps)."""

PATH = "/root/.openclaw/workspace/AGI_COMPANY/subsidiaries/CREAM/sales/prospects/generate_2026-08-31.py"

with open(PATH, "r", encoding="utf-8") as f:
    s = f.read()

# Ordered (old, new) pairs. Order matters to avoid collisions.
repls = [
    # counts (comma format) — new then prev
    ("121,000", "123,000"),
    ("120,000", "122,000"),
    # priority totals in run report
    ("48,400", "49,200"),
    ("48,000", "48,800"),
    ("42,350", "43,050"),
    ("42,000", "42,700"),
    ("30,250", "30,750"),
    ("30,000", "30,500"),
    # old_values / stale marketing "119,000"
    ("119,000", "121,000"),
    # target date
    ("2026-08-29", "2026-08-31"),
    # streak (new=121, prev=120)
    ("119 days", "121 days"),
    ("119-day", "121-day"),
    ("119-Day", "121-Day"),
    ("119 DAYS", "121 DAYS"),
    ("Day 119", "Day 121"),
    ("119\\g", "121\\g"),
    ("118 days", "120 days"),
    ("118-day", "120-day"),
    ('"streak_days", 118', '"streak_days", 120'),
    ('"total_prospects", 120000', '"total_prospects", 122000'),
    ('{"A": 48000, "B": 42000, "C": 30000}', '{"A": 48800, "B": 42700, "C": 30500}'),
    ('{"senior_6plus": 59996, "mid_3to5": 30047, "new_0to2": 29957}',
     '{"senior_6plus": 61001, "mid_3to5": 30565, "new_0to2": 30434}'),
    # run report header date
    ("## August 29, 2026 Execution Summary", "## August 31, 2026 Execution Summary"),
    # marketing date-replacement lines (full lines)
    ('            content = content.replace("Updated: August 28, 2026", "Updated: August 29, 2026")',
     '            content = content.replace("Updated: August 30, 2026", "Updated: August 31, 2026")'),
    ('            content = content.replace("Updated: August 27, 2026", "Updated: August 29, 2026")',
     '            content = content.replace("Updated: August 29, 2026", "Updated: August 31, 2026")'),
    ('            content = content.replace("August 28, 2026", "August 29, 2026")',
     '            content = content.replace("August 30, 2026", "August 31, 2026")'),
    ('            content = content.replace("August 27, 2026", "August 29, 2026")',
     '            content = content.replace("August 29, 2026", "August 31, 2026")'),
]

for old, new in repls:
    if old not in s:
        print(f"WARN: not found -> {old!r}")
    s = s.replace(old, new)

with open(PATH, "w", encoding="utf-8") as f:
    f.write(s)

print("patched. leftover checks:")
for bad in ["119", "118", "120,000", "121,000", "August 28", "August 27", "2026-08-29"]:
    if bad in s:
        # show context
        import re
        for m in re.finditer(re.escape(bad), s):
            a = max(0, m.start()-40); b = m.end()+40
            print(f"  [{bad}] ...{s[a:b]}...")
print("done")
