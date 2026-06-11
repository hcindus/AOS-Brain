# STRIPE SECRET KEY RETRIEVAL

## ⚠️ REQUIRED ACTION: Get Live Secret Key

The payment server needs the **Secret Key** (not the Publishable Key) to process live payments.

---

## Step-by-Step Instructions

### 1. Log into Stripe Dashboard
- Go to: https://dashboard.stripe.com/apikeys
- Make sure you're in **LIVE MODE** (toggle top-right)

### 2. Find the Secret Key
- Look for **"Secret key"** section
- Click **"Reveal"** button
- Copy the key that starts with: `sk_live_...`

### 3. Provide the Key

**Option A: Paste it here (encrypted)**
Just paste the key and I'll secure it immediately.

**Option B: Set it directly yourself**
```bash
# Edit the service file
sudo systemctl edit psdepot-payment --full

# Find this line:
Environment="STRIPE_SECRET_KEY=sk_live_..."

# Replace with your actual key, then save and exit

# Restart the service
sudo systemctl daemon-reload
sudo systemctl restart psdepot-payment

# Verify it's working
curl -s https://myl0nr0s.cloud/api/config | grep stripe_mode
```

---

## Current Status

| Key Type | Value | Status |
|----------|-------|--------|
| Publishable Key | `pk_live_51TQu42...` | ✅ Correct (frontend) |
| Secret Key | `sk_live_51TQu42...` (WRONG - copied from pub key) | ❌ **NEEDS FIX** |

---

## Why Payments Are Failing

The backend is trying to use the **Publishable Key** as a **Secret Key**.
- Publishable keys (pk_live_...) = Frontend only, creates cards
- Secret keys (sk_live_...) = Backend only, creates PaymentIntents

Without the real secret key, the server cannot create PaymentIntents = payments fail.

---

## After Fix

Test with:
```bash
curl -s https://myl0nr0s.cloud/api/config | grep stripe_mode
# Should return: "stripe_mode": "live"
```

Then try a test payment on psdepot.com with card `4242 4242 4242 4242`

---

*Generated: 2026-05-25*