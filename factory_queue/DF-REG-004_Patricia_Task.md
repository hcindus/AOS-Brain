# Factory Order: DF-REG-004
**Agent:** Patricia  
**Priority:** HIGH  
**Status:** ASSIGNED  
**Created:** 2026-04-21 07:47 UTC

---

## Mission: ReggieStarr Phase 4 — Scheduled Tasks

### Background
ReggieStarr RS-79 POS completed Phases 1-3 on Abacus AI. Phase 4 blocked due to credits. Remaining work: database automation.

### Deliverables
1. **Daily Z-Report** — Auto-generate at midnight, save to disk, email to admin
2. **Loyalty Expiration** — Purge points >12 months old, monthly run
3. **Low-Stock Alerts** — Check inventory, email when below threshold
4. **Transaction Archive** — Move orders >90 days to archive table
5. **Database Backup** — pg_dump daily, compress, store locally + S3

### Tech Stack
- PostgreSQL + pg_cron (or Node.js node-cron fallback)
- Prisma ORM (existing)
- Nodemailer or SendGrid for alerts
- Location: `/root/.openclaw/workspace/aocros/projects/ReggieStarr/`

### Files to Create
```
ReggieStarr/
├── prisma/
│   └── migrations/
│       └── 004_add_scheduler/migration.sql
├── src/
│   └── scheduler/
│       ├── index.ts          # Main scheduler entry
│       ├── zReport.ts        # Z-report generation
│       ├── loyaltyExpire.ts  # Point expiration
│       ├── lowStockAlert.ts  # Inventory alerts
│       ├── archiveOrders.ts  # Transaction archival
│       └── backup.ts         # DB backup runner
├── .env.scheduler            # Scheduler env vars
└── docs/
    └── SCHEDULED_TASKS.md    # Documentation
```

### Check-in
Daily updates to Captain via sessions.

---
**Assigned by:** Miles  
**Approved by:** Captain
