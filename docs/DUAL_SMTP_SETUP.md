# Dual SMTP Setup - READY FOR SENDGRID API KEY

## Current Status: ✅ PREPARED

Your email system is ready for SendGrid integration. Just provide the API key.

---

## What Will Happen When You Run Setup:

| Email Type | Current (Hostinger) | After Setup (SendGrid) |
|------------|---------------------|------------------------|
| **CRITICAL** - Leads, Alerts, Sales | ✅ Rate limited (30s delay) | 🚀 Fast delivery |
| **CRITICAL** - Brain outages | ✅ Rate limited (30s delay) | 🚀 Fast delivery |
| **BULK** - Cron notifications | ✅ Rate limited (30s delay) | ✅ Rate limited (30s delay) |
| **BULK** - Daily reports | ✅ Rate limited (30s delay) | ✅ Rate limited (30s delay) |

---

## How to Complete Setup:

### Step 1: Get SendGrid API Key
1. Go to https://sendgrid.com
2. Create account (or log in)
3. Go to Settings → API Keys
4. Create API Key with "Mail Send" permissions
5. Copy the key (starts with "SG.")

### Step 2: Run Setup Script
```bash
/root/.openclaw/workspace/scripts/setup_dual_smtp.sh YOUR_SENDGRID_API_KEY_HERE
```

**Example:**
```bash
/root/.openclaw/workspace/scripts/setup_dual_smtp.sh SG.xxxxxxxxxx
```

### Step 3: Test
```bash
# Test critical email (should use SendGrid)
echo "Test lead alert" | mail -s "New Lead: Test Restaurant" miles@myl0nr0s.cloud

# Check routing
mailq
```

---

## Email Routing Logic:

```
FROM: miles@myl0nr0s.cloud  →  SendGrid (fast)
FROM: alerts@*              →  SendGrid (fast)
FROM: sales@*               →  SendGrid (fast)
FROM: leads@*               →  SendGrid (fast)
FROM: cron@*                →  Hostinger (bulk rate limited)
FROM: (others)              →  Hostinger (bulk rate limited)
```

---

## Monitoring:

After setup, check logs:
```bash
# SendGrid emails
tail -f /var/log/mail.log | grep sendgrid

# Hostinger emails
tail -f /var/log/mail.log | grep hostinger

# Queue status
mailq
```

---

## Status Now:

| Component | Status |
|-----------|--------|
| Hostinger queue | 🟡 Processing (30s delays) |
| Rate limiting | ✅ Active (30s, concurrency=2) |
| Dual SMTP config | ⏳ Ready for API key |
| Priority router | ✅ Script ready |

**Ready when you are!**
