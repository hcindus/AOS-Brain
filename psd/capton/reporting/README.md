# Capton Systems Provider — Reporting Package

**Prepared by:** Miles | Performance Supply Depot LLC  
**Date:** 2026-08-03  
**Ref:** CSP Agreement Section 1.3 (Forecasts) & Section 1.2 (Installation Reporting)

---

## Template 1: Monthly Sales Forecast

**File:** `capton_monthly_forecast_template.csv`

**Purpose:** Satisfies Section 1.3 requirement for a monthly sales forecast in a format acceptable to Capton.

**Fields:**
| Field | Description |
|-------|-------------|
| Month/Year | Reporting month |
| Product SKU/Name | Which Capton product |
| Forecasted Units | Expected units to sell |
| Forecasted Revenue | Units × unit price |
| Expected Close Date | When we think this deal closes |
| Lead/Customer Name | Who it's for |
| Confidence (%) | 25/50/75/90% — how sure we are |
| Notes | Context |

**How to generate from CRM:**
1. Pull open leads tagged `capton` from PSD CRM
2. Sort by expected close date within the month
3. Apply confidence multipliers: Hot (75%) / Warm (50%) / Cold (25%)
4. Export as CSV in this format

---

## Template 2: Installation & Sales Report

**File:** `capton_install_sales_report_template.csv`

**Purpose:** Satisfies Section 1.2 — logs every install and sale completed that month.

**Fields:**
| Field | Description |
|-------|-------------|
| Install Date | Date system was placed |
| Customer Name | Business name |
| Business Type | Bar / Restaurant / Nightclub / Hotel / Other |
| Address/City/State | Location for territory verification |
| Contact Name/Email/Phone | Who we dealt with |
| Product SKU/Name | Which products installed |
| Units Installed | Quantity |
| Unit Price | Per-unit price we charged |
| Total Revenue | Units × price |
| Installation Notes | Any calibrations, training, issues |
| Follow-Up Date | Next check-in |

**How to generate:**
1. Pull closed-won opportunities tagged `capton` for the reporting month
2. Include installation date from fulfillment records
3. Export as CSV

---

## Automation Path (Future)

Once volumes justify it, this can be automated:
- CRM webhook → auto-populate templates
- Scheduled cron job → generate CSV on the 1st of each month
- Email to Capton rep directly from PSD system

**Estimated build effort:** ~4 hours for a Python script + cron job.

---

## Notes for Captain

- These are **draft templates** — we should send these to Capton for approval _before_ relying on them as our official format, since Section 1.3 says "format acceptable to Company."
- The forecast uses confidence percentages. If Capton wants a simpler number (just total units), we can collapse the confidence column.
- I recommend asking for **quarterly** instead of monthly reporting. If they push back, these templates work monthly too — just more paperwork.
