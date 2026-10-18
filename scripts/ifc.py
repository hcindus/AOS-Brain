#!/usr/bin/env python3
"""
International Fixed Calendar (Cotsworth / 13-month) — pure Python implementation.

13 months × 28 days = 364 days, + 1 Year Day, + 1 Leap Day (leap years).
Every date falls on the same weekday forever. Month 7 = "Sol".

Reference: Moses B. Cotsworth's International Fixed Calendar (Kodak used it 1928–1989).
"""
from datetime import date

MONTHS = ["January", "February", "March", "April", "May", "June",
          "Sol", "July", "August", "September", "October", "November", "December"]

WEEKDAYS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

# In the IFC, every month is 28 days and every month starts on the same weekday.
# Day 1 of every month = Sunday, so Day 13 = Friday, Day 28 = Saturday.


def is_leap_year(year: int) -> bool:
    """Gregorian leap-year rule (the IFC keeps the same year numbering)."""
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)


def gregorian_day_of_year(year: int, month: int, day: int) -> int:
    """1-indexed Gregorian day-of-year."""
    return (date(year, month, day) - date(year, 1, 1)).days + 1


def gregorian_to_ifc(year: int, month: int, day: int):
    """
    Convert a Gregorian date to IFC.
    Returns a dict: {year, month (name or None), day (int or None), special (None | 'Year Day' | 'Leap Day')}
    """
    doy = gregorian_day_of_year(year, month, day)
    leap = is_leap_year(year)

    # Leap Day is inserted after June 28 (IFC). In a leap year:
    #   days 1–168  → Jan 1 .. Jun 28
    #   day 169     → Leap Day (outside months)
    #   days 170–366 → Sol 1 .. Dec 28 .. Year Day
    # Non-leap:
    #   days 1–364  → Jan 1 .. Dec 28
    #   day 365     → Year Day

    # Handle Year Day (last day of the Gregorian year)
    if (leap and doy == 366) or (not leap and doy == 365):
        return {"year": year, "month": None, "day": None, "special": "Year Day"}

    # Handle Leap Day
    if leap and doy == 169:
        return {"year": year, "month": None, "day": None, "special": "Leap Day"}

    # Adjust for leap year: days after the Leap Day shift down by 1
    adjusted = doy
    if leap and doy > 169:
        adjusted = doy - 1

    # Map to month/day (1-indexed within the 13×28 grid)
    month_idx = (adjusted - 1) // 28
    day_in_month = (adjusted - 1) % 28 + 1

    return {
        "year": year,
        "month": MONTHS[month_idx],
        "day": day_in_month,
        "special": None,
    }


def ifc_to_gregorian(year: int, month_name: str, day: int):
    """Convert an IFC date (month name + day) to a Gregorian date. Returns (year, month, day)."""
    month_idx = MONTHS.index(month_name)
    ifc_doy = month_idx * 28 + day  # 1..364 within the month grid

    leap = is_leap_year(year)
    # In a leap year, days after June 28 shift up by 1 (Leap Day occupies day 169)
    greg_doy = ifc_doy
    if leap and ifc_doy > 168:
        greg_doy = ifc_doy + 1

    d = date(year, 1, 1) + __import__("datetime").timedelta(days=greg_doy - 1)
    return d.year, d.month, d.day


def weekday(ifc_month: str, ifc_day: int) -> str:
    """Perpetual weekday — Day 1 of every month is Sunday, so weekday = (day-1) % 7."""
    if ifc_month is None:
        return None  # Year Day / Leap Day have no weekday
    return WEEKDAYS[(ifc_day - 1) % 7]


def today_ifc():
    """Today's date in the International Fixed Calendar."""
    t = date.today()
    return gregorian_to_ifc(t.year, t.month, t.day)


def format_ifc(ifc: dict) -> str:
    """Human-readable IFC date string."""
    if ifc["special"] == "Year Day":
        return f"Year Day, {ifc['year']}"
    if ifc["special"] == "Leap Day":
        return f"Leap Day, {ifc['year']}"
    wd = weekday(ifc["month"], ifc["day"])
    return f"{wd}, {ifc['month']} {ifc['day']}, {ifc['year']}"


if __name__ == "__main__":
    # Self-test
    print("=== International Fixed Calendar self-test ===")
    print(f"Today (Gregorian {date.today()}):")
    t = today_ifc()
    print(f"  IFC: {format_ifc(t)}")

    # Known check: 2026-01-01 (a Thursday) should be IFC January 1 (Thursday? no — Sunday)
    # IFC Jan 1 is always Sunday, so Gregorian Jan 1 maps to a fixed weekday only if aligned.
    print(f"\nGregorian 2026-06-28 → IFC: {format_ifc(gregorian_to_ifc(2026, 6, 28))}")
    print(f"Gregorian 2026-06-29 → IFC: {format_ifc(gregorian_to_ifc(2026, 6, 29))}")
    print(f"Gregorian 2026-12-31 → IFC: {format_ifc(gregorian_to_ifc(2026, 12, 31))}")

    # Leap year check (2028 is a leap year)
    print(f"\nGregorian 2028-06-29 → IFC: {format_ifc(gregorian_to_ifc(2028, 6, 29))}")  # should be Leap Day
    print(f"Gregorian 2028-07-01 → IFC: {format_ifc(gregorian_to_ifc(2028, 7, 1))}")

    # Round-trip
    print(f"\nRound-trip check: IFC Sol 1 2026 → Gregorian {ifc_to_gregorian(2026, 'Sol', 1)}")
    print(f"Friday the 13th in every month: {weekday('January', 13)} (should be Friday)")
