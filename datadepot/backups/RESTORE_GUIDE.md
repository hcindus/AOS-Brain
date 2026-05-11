# DepotChaos & PSD Dashboard - Restore Guide

## Quick Restore Commands

### 1. Restore Tier Categorization
```bash
sqlite3 /root/.openclaw/workspace/data/depot_chaos/unified.db < tier_system_backup_20260511.sql
```

### 2. Restore Database from Backup
```bash
# Stop services first
systemctl stop depotchaos-api psd-api

# Restore from backup (if available)
cp /path/to/unified.db.backup /root/.openclaw/workspace/data/depot_chaos/unified.db

# Restart services
systemctl start depotchaos-api psd-api
systemctl status depotchaos-api psd-api
```

### 3. Restore API Files
```bash
# From workspace backup
cp /root/.openclaw/workspace/datadepot/web/backups/psd_api_YYYYMMDD.py /root/.openclaw/workspace/datadepot/web/psd_api.py
cp /root/.openclaw/workspace/datadepot/web/backups/psd_performance_YYYYMMDD.html /var/www/psdepot.com/psd_performance.html

# Restart API
systemctl restart psd-api
```

---

## Configuration Reference

### Ports & Services
| Service | Port | PID File | Config |
|---------|------|----------|--------|
| DepotChaos API | 8082 | systemctl | `/etc/systemd/system/depotchaos-api.service` |
| PSD API | 8081 | systemctl | `/etc/systemd/system/psd-api.service` |
| Nginx | 80/443 | systemctl | `/etc/nginx/sites-enabled/psdepot.com` |

### Database Locations
| Database | Path | Purpose |
|----------|------|---------|
| Unified DB | `/root/.openclaw/workspace/data/depot_chaos/unified.db` | Customers, leads, sales |
| DepotChaos | `/root/.openclaw/workspace/DepotChaos/depot_chaos.db` | Vendors, Yelp cache |

### API Endpoints
```
DepotChaos CRM: http://localhost:8082/api/
  - /api/stats
  - /api/leads
  - /api/intelligence

PSD Dashboard: http://localhost:8081/api/
  - /api/dashboard/overview
  - /api/dashboard/monthly-revenue
  - /api/customers
```

---

## Tier System Mapping

| Tier ID | Display Name | Spend Range | Current Count |
|---------|--------------|-------------|---------------|
| `stone` | Stone | <$5K | 395 |
| `bronze` | PPCL | $5K-$10K | 105 |
| `silver` | Prime | $10K-$25K | 1 |
| `gold` | Spot On Target | $25K-$50K | 0 |
| `platinum` | Top 165 | $50K-$100K | 0 |
| `diamond` | Top 165 (VIP) | $100K+ | 0 |

---

## Troubleshooting

### Port Already in Use
```bash
# Find process using port 8082
lsof -i :8082
# or
ss -tlnp | grep 8082

# Kill zombie process
kill -9 <PID>
systemctl restart depotchaos-api
```

### API Not Responding
```bash
# Check logs
journalctl -u depotchaos-api -n 50 --no-pager
journalctl -u psd-api -n 50 --no-pager

# Test endpoints
curl http://localhost:8082/api/sts
curl http://localhost:8081/api/dashboard/overview
```

### Database Locked
```bash
# Check for .db-shm and .db-wal files
ls -la /root/.openclaw/workspace/data/depot_chaos/

# If present, checkpoint the database
sqlite3 /root/.openclaw/workspace/data/depot_chaos/unified.db "PRAGMA wal_checkpoint;"
```

---

## Backup History

| Date | File | Description |
|------|------|-------------|
| 2026-05-11 | `tier_system_backup_20260511.sql` | Tier categorization SQL |
| 2026-05-09 | `unified_backup_20260509_053801.db` | Database backup (pre-tier) |

---

*Last Updated: 2026-05-11 21:35 UTC*
