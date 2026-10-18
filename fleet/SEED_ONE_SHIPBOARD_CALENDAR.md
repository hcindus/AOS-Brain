# SEED ONE — Shipboard Calendar (International Fixed Calendar)

**In-universe adoption:** The AOCROS fleet runs on the 13-month International Fixed Calendar (Cotsworth) for all shipboard timekeeping.

**Rationale (in-universe):** A colony vessel spends decades — even generations — in transit. A Gregorian calendar's irregular months and shifting weekdays are an operational nuisance for watchkeeping, duty rosters, and agricultural cycles. The fixed calendar gives every crewmember an identical, predictable week grid. Hydroponics cycles, maintenance schedules, and crew rotations all map cleanly to 28-day months.

---

## Calendar Structure

- **13 months** × 28 days = 364 days
- **Year Day** — after December 28 (the 365th day, outside any month/week)
- **Leap Day** — after Sol 14 (mid-year, leap years only)

### The 13 Months
January · February · March · April · May · June · **Sol** · July · August · September · October · November · December

*"Sol" (after the sun) is the 13th month inserted between June and July — the ship's marker that the year is halfway through.*

---

## The Perpetual Grid

Every month is identical. Day 1 = Sunday, Day 28 = Saturday. No exceptions.

```
Sun Mon Tue Wed Thu Fri Sat
  1   2   3   4   5   6   7
  8   9  10  11  12 ★13★ 14
 15  16  17  18  19  20  21
 22  23  24  25  26  27  28
```

**★13★ = Friday the 13th — occurs in every month (13 per year).** Aboard SEED ONE this is not unlucky; it's simply "Maintenance Friday" — the 13th of every month is the scheduled deep-clean/maintenance rotation day.

---

## Crew Application

| Use | How the fixed calendar helps |
|-----|------------------------------|
| **Watch rotation** | 3-shift cycles map cleanly to the 4-week month (12 watches = 1 month) |
| **Hydroponics** | 28-day crop cycles align exactly with one month |
| **Rosters & leave** | Every crewmember's duty day is fixed to a weekday, forever |
| **Recycling** | Monthly harvest/recycle schedule = same days each month |
| **Nursery** | Age milestones (Sol-birthdays) are consistent |

---

## Year Day & Leap Day

- **Year Day** is a ship-wide "free day" — no month, no weekday, no duty roster. Used for the annual fleet-wide celebration (arrival anniversary).
- **Leap Day** (mid-year) is a "buffer day" for clock drift corrections and navigation recalibration.

---

## Relationship to the converter

- Python module: `scripts/ifc.py` (Gregorian ↔ IFC)
- Web tool: `tappylewis.cloud/ifc.html` (converter + perpetual grid)

*The SEED ONE logs all mission time in both Gregorian (for Earth comms) and IFC (for internal operations).*
