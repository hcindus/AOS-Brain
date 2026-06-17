# Website Inventory & Backup Status
**Generated:** 2026-06-17
**Backup Location:** `/root/.openclaw/workspace/BACKUPS/websites/20260617/`

## Core AGI Company Sites

| Site | Source Location | Deployed To | Status |
|------|-----------------|-------------|--------|
| myl0nr0s.cloud | `AGI_COMPANY/subsidiaries/PERFORMANCE_SUPPLY_DEPOT/website/myl0nr0s/cloud/` | `/var/www/html/index.html` | ✅ BACKUP ✅ DEPLOY |
| performance-supply-depot.com | `AGI_COMPANY/subsidiaries/PERFORMANCE_SUPPLY_DEPOT/website/performance-supply-depot/` | `/var/www/psdepot.com/` | ✅ BACKUP |
| portal | `AGI_COMPANY/subsidiaries/PERFORMANCE_SUPPLY_DEPOT/website/portal/` | Not deployed | ✅ BACKUP |
| am-hud-supply | `AGI_COMPANY/subsidiaries/PERFORMANCE_SUPPLY_DEPOT/website/am-hud-supply/` | Not deployed | ⚠️ Needs backup |

## Product Sites

| Site | Source Location | Status |
|------|-----------------|--------|
| ReggieStarr POS | `aocros/projects/ReggieStarr/web/` | ✅ Active |
| Cream | `Cream/web/` | ✅ Active |
| Collections | `collections/` | ✅ Active |
| Appointments | `appointments/web/` | ✅ Active |

## Game Sites

| Site | Source Location | Deployed To | Status |
|------|-----------------|-------------|--------|
| N'og nog v3 | `nognog/v3/` | `/var/www/html/nog/` | ✅ Active |
| Space Battle | `spacebattle/` | `/var/www/html/spacebattle/` | ✅ Active |
| Space Agent | `aos-space-agent/` | `/var/www/html/aos-space-agent/` | ✅ Active |

## Legacy/Archive Sites

| Site | Location | Note |
|------|----------|------|
| AGI_COMPANY_WEBSITE_REBUILD | `AGI_COMPANY_WEBSITE_REBUILD/` | Previous rebuild attempt |
| TAPPYLEWIS_REBUILD | `TAPPYLEWIS_REBUILD/` | Tappylewis backup |
| tappylewis.cloud | `tappylewis.cloud/` | Music site |

## Critical Deployments Needed

1. **myl0nr0s.cloud** - Deployed but DNS routing issue (Hostinger "Coming Soon" page)
2. **portal** - Not deployed to web server
3. **am-hud-supply** - Not backed up yet

## Backup Verification
```
BACKUPS/websites/20260617/
├── myl0nr0s.cloud/
├── performance-supply-depot/
└── portal/
```

## Next Actions
- [ ] Fix DNS for myl0nr0s.cloud (Hostinger dashboard)
- [ ] Deploy portal site
- [ ] Backup am-hud-supply
- [ ] Verify all deployed sites match source
