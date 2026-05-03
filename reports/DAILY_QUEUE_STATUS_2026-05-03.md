# Daily Queue Status Report
**Generated:** 2026-05-03 06:00 UTC
**Report ID:** queue-status-20260503-0600

---

## 📊 Executive Summary

| System | Status | Items | Trend |
|--------|--------|-------|-------|
| Email Queue | 🟡 Active | 1,236 pending | Steady |
| Scraper Queue | 🟢 Healthy | 37 items, 22 reports | Stable |
| Captain Local Queue | 🟢 Ready | 100 businesses | Ready for scraping |
| Dark Factory Tasks | 🟢 Active | 4 tasks | Processing |
| Expedition Reports | 🟢 Active | 20+ crew reports | Running |

---

## 📧 DataDepot Email Queue

**Location:** `/root/.openclaw/workspace/datadepot/queue/`

| File | Lines | Status |
|------|-------|--------|
| `pending_emails.json` | 1,236 | 🟡 Awaiting processing |
| `sent_emails.json` | 762 | ✅ Sent history |
| `followup_queue_20260429.json` | 1,701 | 🟡 Followups pending |

**Action Required:** Consider processing pending emails via `queue_followups.py`

---

## 🔍 Scraper Queue

**Location:** `/root/.openclaw/workspace/data/scraper/queue_status.json`

- **Items:** 37
- **Reports:** 22
- **Last Updated:** 2026-04-30T09:04:38+00:00

**Status:** Queue is processing normally

---

## 🏢 Captain Local Queue

**Location:** `/root/.openclaw/workspace/AGI_COMPANY/subsidiaries/PERFORMANCE_SUPPLY_DEPOT/products/enrichment/queues/captain_local_queue.json`

- **Queue ID:** captain_local_queue_001
- **Status:** ready_for_scraping
- **Count:** 100 businesses (sample)
- **Note:** Full 1,000 businesses ready when Captain initiates scrape

**Action Required:** Run `local_scraper.py` to enrich leads

---

## 🏭 Dark Factory Queue

**Location:** `/root/.openclaw/workspace/factory_queue/`

| Task | Status |
|------|--------|
| DF-REG-004-v2_Patricia2.md | Pending |
| DF-REG-004_Patricia_Task.md | Pending |
| DF-RS80-001-v2_Chelios2.md | Pending |
| DF-RS80-001_Forge_Task.md | Pending |

**Total:** 4 active tasks

---

## 🚀 Expedition Crew Reports

**Location:** `/root/.openclaw/workspace/expeditions/`

- **Active Reports:** 20+ timestamped crew reports
- **Last Activity:** Recent (crew reporting regularly)
- **Crew Status:** Vex (Pilot), Nyx (Engineer), Jax (Scientist), Luna (Combat), Aria (Medic)

**Note:** Crew automation running via `nognog-crew` service

---

## 📁 AGENT Factory Module Queues

**Location:** `/root/.openclaw/workspace/queue/`

Active queue documents:
- AGENT_FACTORY_MODULE_QUEUE.md
- AGENT_VERSE_QUEUE.md
- AGI_COMPANY_WEBSITE_BUILD.md
- CREAM_PROJECT_QUEUE.md
- MILK_MAN_GAME_QUEUE.md
- And 16 other project queues

**Daily Status Reports:** Available for 2026-04-05 through 2026-05-01

---

## 🔔 Recommendations

1. **Email Queue:** Process 1,236 pending emails (run `queue_followups.py`)
2. **Captain Local:** Initiate scraping for 100 business leads
3. **Dark Factory:** Review 4 pending tasks for assignment
4. **Scraper:** Continue monitoring - healthy status

---

*Report generated automatically by daily cron job*
*Next report: 2026-05-04 06:00 UTC*
