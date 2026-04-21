# Factory Order: DF-REG-004-v2
**Agent:** Patricia2  
**Priority:** HIGH  
**Status:** ASSIGNED  
**Created:** 2026-04-21 07:47 UTC
**Supervisor:** Miles

---

## Mission: ReggieStarr Phase 4 — Scheduled Tasks Automation

### Background
ReggieStarr RS-79 POS completed Phases 1-3 on Abacus AI. Phase 4 was blocked due to credit exhaustion. Your mission: complete the scheduled tasks infrastructure.

### Deliverables
1. **Daily Z-Report** — Auto-generate at midnight, save to disk, email to admin
2. **Loyalty Point Expiration** — Purge points >12 months old, monthly run  
3. **Low-Stock Alerts** — Check inventory, email/notify when below threshold
4. **Transaction Archive** — Move orders >90 days to archive table
5. **Database Backup** — pg_dump daily, compress, store locally + optional S3

### Architecture
```
scheduler/
├── index.ts                 # Main entry point
├── jobs/
│   ├── zReport.ts           # Midnight Z-report generation
│   ├── loyaltyExpire.ts      # Point expiration logic
│   ├── lowStockAlert.ts      # Inventory threshold monitoring
│   ├── archiveOrders.ts       # Transaction archival
│   └── backup.ts            # DB backup runner
├── notifications/
│   ├── email.ts              # Nodemailer integration
│   └── webhook.ts            # Optional Slack/Discord alerts
└── config/
    └── scheduler.yaml        # Cron schedule definitions
```

### Tech Requirements
- PostgreSQL + pg_cron extension
- Prisma ORM (existing codebase)
- Node.js + node-cron (fallback if pg_cron unavailable)
- Location: `/root/.openclaw/workspace/aocros/projects/ReggieStarr/`

### Check-in Protocol
- Daily progress reports to Miles
- Blockers: escalate immediately
- Completion: notify Miles for factory queue update

---
**Authority:** Captain (root)  
**Supervisor:** Miles  
**Execution:** Patricia2
