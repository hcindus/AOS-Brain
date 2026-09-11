# DataDepot Cleanup Plan — ca_abc_licenses_raw.csv Reconciliation

**Date:** 2026-09-11
**Blocker:** Master CSV corrupted (flagged since ~Aug 21) — appends suspended.

---

## Root Cause (confirmed)

`ca_abc_licenses_raw.csv` (87,464 lines) has **four incompatible schemas concatenated** in one file:

| Columns | Rows | Schema | Origin |
|---------|------|--------|--------|
| 13 | 1,251 | `license_number,business_name,dba,address,city,county,state,zip,license_type,status,issue_date,expiration,capacity` | **Old synthetic scraper** (fabricated "Little Kitchen", "Grill" names, fake zips) |
| 14 | 7 | 13-col + 1 stray field | Data anomaly |
| 30 | 86,191 | Real ABC DailyExport (license#, APP/PEND, P40/P41 types, name, addr, city, county, ZIP+4, etc.) | **Patricia's live abc.ca.gov scrape** (the real data) |
| 31 | 15 | 30-col + 1 stray field | Data anomaly |

**The problem:** when the live scrape started, the real 30-column ABC data was appended onto the old 13-column synthetic CSV. They share a `license_number` + `business_name` concept but different field order/count — so the file is now unparseable as a single schema.

---

## Cleanup Plan (one-time, safe, reversible)

### Phase 1 — Backup & Snapshot (no data loss)
1. `cp ca_abc_licenses_raw.csv ca_abc_licenses_raw.corrupt_backup_20260911.csv`
2. Record row counts + md5 for audit trail.

### Phase 2 — Split by schema (read-only)
3. Partition the file by column count into 4 temp files:
   - `_c13.csv` (1,251 rows) — old synthetic
   - `_c14.csv` (7 rows) — anomaly
   - `_c30.csv` (86,191 rows) — **real ABC data (keep)**
   - `_c31.csv` (15 rows) — anomaly
4. For the 14/31 anomalies, inspect: they're likely 13/30-col rows with a trailing stray comma or an embedded comma in a quoted field — fixable by re-parsing with a proper CSV reader.

### Phase 3 — Rebuild (the real schema wins)
5. Establish the **canonical 30-column ABC schema** as the master (from `_c30.csv` header).
6. Migrate any genuinely-unique 13-col rows into the 30-col schema *only if they map to real licenses* (cross-check `license_number` exists in the 30-col set; if not, flag for manual review).
7. **Discard** the known-fabricated synthetic rows (the "Little Kitchen"/"Grill"/fake-zip records) — archive to `_synthetic_archive.csv`, not delete.
8. Write one clean `ca_abc_licenses_raw.csv` with the single 30-col schema.

### Phase 4 — Guardrails (prevent recurrence)
9. Add a **schema validator** to the daily collection job: before any append, assert the incoming row's column count matches the master header. Reject + log on mismatch (never blind-append).
10. Add a **line-count/header sanity check** that fires a halt if the file ever mixes schemas again.

### Phase 5 — Re-enable appends
11. After rebuild + validator, resume daily appends (live scrape → clean CSV).

---

## Secondary blockers (same sprint)

| Blocker | Action | Owner |
|---------|--------|-------|
| Google Places API key (enrichment blocked) | Provision key → wire into `icbrowser` / enrichment path | Captain (paste key) |
| POS detection model stale (since 2026-05-18) | Either retrain (needs labeled data) or deprioritize — POS detection is not blocking lead generation | Patricia/Jordan |

---

## Effort estimate

- Phase 1–3 (rebuild): ~30–45 min, safe/scripted, reversible.
- Phase 4 (validator): ~15 min, small script.
- **Total:** under an hour, fully reversible, no data loss.

**Note:** I will NOT execute this autonomously during a cron run — it's a one-time destructive-looking op that needs a Captain go-ahead. This plan is the "ready when you are" spec.
