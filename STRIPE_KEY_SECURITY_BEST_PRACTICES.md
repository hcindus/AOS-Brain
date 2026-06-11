# Stripe API Key Security Best Practices

## 🔐 Performance Supply Depot LLC — Security Documentation

---

## 1. Key Types Overview

### Publishable Key (`pk_live_...` / `pk_test_...`)
- ✅ **Safe for frontend/public code**
- Used to tokenize cards in browser
- Cannot charge cards directly
- Starts with: `pk_live_` (production) or `pk_test_` (test)

### Secret Key (`sk_live_...` / `sk_test_...`)
- ⚠️ **SERVER-SIDE ONLY** — Never expose to frontend
- Creates PaymentIntents, charges cards, refunds
- Full account access
- Starts with: `sk_live_` (production) or `sk_test_` (test)

### Restricted Key (`rk_live_...` / `rk_test_...`)
- ✅ **Best practice for production**
- Limited permissions (e.g., only PaymentIntents)
- Cannot access other account features
- **Recommended for psdepot.com**

---

## 2. Security Best Practices

### ✅ DO:

| Practice | Implementation |
|----------|----------------|
| **Use Environment Variables** | `export STRIPE_SECRET_KEY=sk_live_...` |
| **Set File Permissions** | `chmod 600 .env` (owner read/write only) |
| **Use Restricted Keys** | Create limited-scope keys in Dashboard |
| **Rotate Regularly** | Generate new keys every 90 days |
| **Audit Access** | Check Stripe Dashboard → Developers → Logs |
| **IP Restrictions** | Limit key to production server IPs |

### ❌ DON'T:

| Risk | Why |
|------|-----|
| Never commit to git | Keys in GitHub are publicly searchable |
| Never log to console | `console.log(process.env.STRIPE_SECRET_KEY)` exposes key |
| Never include in frontend | `sk_` keys in browser = instant compromise |
| Never email keys | Email is not encrypted |
| Never share with team | Use Stripe Connect instead |

---

## 3. Current PSDepot Setup Assessment

### Current Configuration:
```
File: /etc/systemd/system/psdepot-payment.service
Permission: root:root (system file)
Storage: Environment variable
```

### ✅ What's Good:
- Key is NOT in code repository
- Key is in systemd environment (process-only access)
- Frontend has only publishable key (`pk_live_`)

### ⚠️ What Should Improve:
- **Replace with Restricted Key** (recommended)
- **Add IP restrictions** in Stripe Dashboard
- **Enable webhook signature verification** (done ✓)
- **Set up key rotation schedule**

---

## 4. Recommended Key Setup

### Step 1: Create Restricted Key (In Stripe Dashboard)

1. Go to: https://dashboard.stripe.com/apikeys
2. Click **"+ Create restricted key"**
3. Name it: `psdepot-payment-server`
4. Set permissions:
   - ✅ Standard read
   - ✅ Standard write
   - ✅ PaymentIntents: Write
   - ✅ PaymentIntents: Read
   - ✅ Customers: Read/Write
   - ❌ No access to other resources
5. **Copy the `rk_live_...` key**

### Step 2: Restrict by IP

In Stripe Dashboard:
1. Go to Developers → API keys
2. Click gear icon next to your key
3. Add IP restrictions:
   - `31.97.6.40` (psdepot.com server)
   - `127.0.0.1` (localhost for testing)

### Step 3: Update Server

```bash
# Edit the service
sudo systemctl edit psdepot-payment --full

# Change to restricted key:
Environment="STRIPE_SECRET_KEY=rk_live_YOUR_RESTRICTED_KEY_HERE"

# Reload and restart
sudo systemctl daemon-reload
sudo systemctl restart psdepot-payment

# Verify
systemctl status psdepot-payment
```

### Step 4: Secure the Secret Key (If Using Full Key)

```bash
# Create secure env file
sudo nano /etc/psdepot/stripe.env
# Contents:
STRIPE_SECRET_KEY=sk_live_...

# Set permissions
sudo chmod 600 /etc/psdepot/stripe.env
sudo chown root:root /etc/psdepot/stripe.env

# Update service to load from file
# In /etc/systemd/system/psdepot-payment.service:
EnvironmentFile=/etc/psdepot/stripe.env
```

---

## 5. Key Rotation Procedure

### Every 90 Days:

1. **Generate new key** in Stripe Dashboard
2. **Update server** with new key
3. **Test payment** with `4242 4242 4242 4242`
4. **Verify** webhook still works
5. **Delete old key** after 24 hours (grace period)

### Emergency Rotation (If Key Leaked):

1. **Immediately revoke** old key in Stripe Dashboard
2. Generate new key
3. Update server
4. Restart service
5. Test transactions

---

## 6. Testing Keys vs Live Keys

| Environment | Publishable Key | Secret Key | Usage |
|-------------|-----------------|------------|-------|
| **Test** | `pk_test_...` | `sk_test_...` | Development, CI/CD |
| **Live** | `pk_live_...` | `sk_live_...` | Production only |

### Test Card Numbers:
- ✅ Success: `4242 4242 4242 4242`
- ❌ Decline: `4000 0000 0000 0002`
- ⚠️ Requires 3D Secure: `4000 0025 0000 3155`

---

## 7. Compliance & Audit

### PCI Compliance:
- ✅ Using Stripe Elements = Stripe handles PCI compliance
- ✅ Never store raw card numbers
- ✅ Store only Stripe tokens (`pm_...`, `pi_...`)

### Security Checklist:
- [ ] Keys not in git repository
- [ ] File permissions set to 600
- [ ] Using restricted keys for production
- [ ] IP restrictions enabled
- [ ] Webhook signature verification enabled
- [ ] Key rotation scheduled (90 days)
- [ ] Audit logs reviewed monthly

---

## 8. Current Action Required

### Immediate Fix:

The current `psdepot-payment.service` has an **incorrect secret key** (copied from publishable key).

**Option A: Use Full Secret Key (Quick Fix)**
1. Get `sk_live_...` from Stripe Dashboard
2. Update systemd service
3. Restart service

**Option B: Use Restricted Key (Recommended)**
1. Create restricted key in Dashboard (only PaymentIntents permission)
2. Copy `rk_live_...` key
3. Update systemd service
4. Add IP restriction to VPS IP

**Option C: Secure File Storage (Best Practice)**
1. Create `/etc/psdepot/stripe.env` with `chmod 600`
2. Move key to file
3. Update service to use `EnvironmentFile`

---

## 9. Documentation

### Where Keys Should NOT Be:
- ❌ GitHub repository
- ❌ Frontend JavaScript
- ❌ Docker images
- ❌ Server logs
- ❌ Email/chat messages

### Where Keys SHOULD Be:
- ✅ Environment variables (systemd)
- ✅ Secure vault (HashiCorp, AWS Secrets Manager)
- ✅ Encrypted files (chmod 600)
- ✅ Stripe Dashboard (for reference)

---

**Document Owner:** Miles / Performance Supply Depot
**Last Updated:** 2026-05-25
**Classification:** Internal Security Document

---

*"Your keys are your money. Guard them like your vault."* 🔐