# System Restoration Plan - Temporal + All Systems
**Date:** 2026-06-12  
**Status:** IN PROGRESS

---

## ✅ CURRENT STATUS

### Services Already Online (✅ RUNNING)
- ✅ aos-brain-v4.service - Brain v4.5 operational
- ✅ aos-mission-control.service - Mission Control v2.1
- ✅ aos-bhsi-v4.service - BHSI v4
- ✅ aos-vision.service - Vision daemon
- ✅ continuous-scraper.service - Data scraper
- ✅ dark-factory-pipeline.service - Dark Factory
- ✅ forge-factory.service - Forge builds
- ✅ patricia-factory.service - Patricia tasks
- ✅ depotchaos.service - CRM web
- ✅ depotchaos-api.service - CRM API
- ✅ brain-health-monitor.service - Health monitoring
- ✅ psdepot-contact.service - Contact forms
- ✅ psdepot-payment.service - Payments

### Services Restored (🔄 JUST RESTARTED)
- 🔄 aos-ternary.service - Ternary system
- 🔄 certbot.service - SSL certificates

### Services Failed (❌ NEEDS ATTENTION)
- ❌ dailyaidecheck.service - AIDE security check

---

## 📋 RESTORATION CHECKLIST

### Phase 1: Core Brain Systems ✅
- [x] Brain v4.5
- [x] Mission Control
- [x] BHSI v4
- [x] Vision Systems
- [x] Health Monitor

### Phase 2: Data Collection ✅
- [x] Continuous Scraper
- [x] CA SOS Scraper V3 (cron scheduled)
- [x] Auto Enrichment Pipeline

### Phase 3: Factory & Pipeline ✅
- [x] Dark Factory Pipeline
- [x] Forge Factory
- [x] Patricia Factory

### Phase 4: CRM & Web ✅
- [x] DepotChaos CRM
- [x] DepotChaos API
- [x] PSDepot Contact
- [x] PSDepot Payment

### Phase 5: Temporal (⏳ PENDING)
- [ ] Temporal service installation
- [ ] Temporal server configuration
- [ ] Workflow migration
- [ ] Worker pool setup

---

## 🚨 CRITICAL: TEMPORAL STATUS

**Finding:** Temporal is NOT installed as a systemd service.

**Options:**
1. **Temporal is Docker-based** - Check `docker ps | grep temporal`
2. **Temporal not yet deployed** - Requires installation
3. **Temporal integrated elsewhere** - Check other services

**Next Action:** Verify Temporal deployment method

---

## 📝 VERIFICATION COMMANDS

```bash
# Check all services
systemctl list-units --type=service --state=active | grep -E "aos|brain|scraper|pipeline|factory|depot"

# Check Temporal specifically
docker ps | grep temporal
which temporal
systemctl status temporal

# Verify scrapers are generating leads
ls -la /root/.openclaw/workspace/AGI_COMPANY/data/leads_generated/
sqlite3 /root/.openclaw/workspace/data/depot_chaos/unified.db "SELECT COUNT(*) FROM leads WHERE created_at > datetime('now', '-24 hours');"
```

---

## 🎯 READY FOR TEMPORAL

Once Temporal is confirmed working:
1. Migrate cron jobs to Temporal workflows
2. Set up retry policies
3. Configure worker pools
4. Enable distributed tracing

---

**Status:** 12/14 services ONLINE (86%)
**Next:** Temporal verification
