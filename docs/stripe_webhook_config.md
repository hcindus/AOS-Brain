# Stripe Webhook Configuration
## Performance Supply Depot LLC
**Generated:** 2026-06-05 20:32 UTC

---

## 🎯 Event Destination Configuration

### Scope Selection
**Recommended: "Your account"**

Since Performance Supply Depot operates as a single merchant (not a platform with connected accounts), you should select:

**☑️ Your account**
- Events from resources in your account
- Includes: charges, payments, customers, invoices, subscriptions

**Why not "Connected accounts"?**
- That option is for platforms like Stripe Connect that manage other businesses' Stripe accounts
- You don't have connected accounts (v1 or v2)

---

## 🔗 Webhook Endpoint URL

**Your webhook endpoint:**
```
https://psdepot.com/webhook
```

**Alternative (if using separate server):**
```
https://api.psdepot.com:8085/webhook
```

---

## 📡 Events to Listen For

### Essential Events (Recommended)

| Event | Description | Action |
|-------|-------------|--------|
| `payment_intent.succeeded` | Payment completed | Send receipt, update order status |
| `payment_intent.payment_failed` | Payment failed | Log failure, notify admin |
| `charge.succeeded` | Charge succeeded | Backup confirmation |
| `charge.failed` | Charge failed | Backup failure handling |
| `invoice.payment_succeeded` | Invoice paid | Subscription handling |
| `invoice.payment_failed` | Invoice failed | Dunning management |
| `customer.created` | New customer | CRM update |
| `customer.updated` | Customer updated | Sync customer data |

### Optional Events

| Event | Description | Use Case |
|-------|-------------|----------|
| `checkout.session.completed` | Checkout finished | Post-purchase actions |
| `refund.created` | Refund processed | Inventory adjustment |
| `dispute.created` | Chargeback received | Alert admin |

---

## 🔐 Webhook Signing Secret

**Purpose:** Verifies webhooks came from Stripe (security)

**After creating the endpoint:**
1. Stripe Dashboard → Developers → Webhooks
2. Click your endpoint
3. Reveal "Signing secret"
4. Save to: `/root/.openclaw/workspace/aocros/secrets/stripe.env`

```bash
STRIPE_WEBHOOK_SECRET=whsec_...
```

---

## 📋 Setup Steps

### Step 1: Create Webhook Endpoint in Stripe Dashboard
1. Go to: https://dashboard.stripe.com/webhooks
2. Click "+ Add endpoint"
3. Enter URL: `https://psdepot.com/webhook`
4. Select "Your account" for scope
5. Select events to listen for (see table above)
6. Click "Add endpoint"

### Step 2: Get Signing Secret
1. Click the newly created endpoint
2. Click "Reveal" next to "Signing secret"
3. Copy the secret (starts with `whsec_`)

### Step 3: Store Secret Securely
```bash
# Add to existing stripe.env file
echo "STRIPE_WEBHOOK_SECRET=whsec_your_secret_here" >> /root/.openclaw/workspace/aocros/secrets/stripe.env
```

### Step 4: Start Webhook Server
```bash
export STRIPE_WEBHOOK_SECRET=whsec_your_secret_here
python3 /root/.openclaw/workspace/aocros/webhook_server.py
```

Or use systemd service (recommended for production).

### Step 5: Test Webhook
1. In Stripe Dashboard, click "Send test event"
2. Select "payment_intent.succeeded"
3. Check webhook server logs for successful receipt

---

## 🔧 Technical Details

### Webhook Handler Code
**Location:** `/root/.openclaw/workspace/aocros/webhook_server.py`

**Features:**
- ✅ Signature verification
- ✅ Event type routing
- ✅ Payment success/failure handling
- ✅ Logging to stdout
- ✅ JSON response

**Port:** 8085 (configurable)

### Nginx Configuration
Add to `/etc/nginx/sites-available/psdepot.com`:

```nginx
# Stripe Webhook
location /webhook {
    proxy_pass http://127.0.0.1:8085;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    # Important: Don't buffer webhook responses
    proxy_buffering off;
}
```

Then reload nginx:
```bash
systemctl reload nginx
```

---

## 📊 Webhook Event Flow

```
Customer pays on psdepot.com
        ↓
Stripe processes payment
        ↓
Stripe sends webhook to psdepot.com/webhook
        ↓
Webhook server receives event
        ↓
Handler processes event type:
   - payment_intent.succeeded → Send email receipt
   - payment_intent.failed → Log and notify
   - etc.
        ↓
Order status updated in database
        ↓
Confirmation sent to customer
```

---

## 🚨 Security Considerations

### Webhook Verification
Always verify webhook signatures in production:
```python
event = stripe.Webhook.construct_event(
    payload, sig_header, STRIPE_WEBHOOK_SECRET
)
```

### IP Allowlisting (Optional)
Stripe sends webhooks from these IPs:
- 3.130.192.104
- 3.18.174.96
- 3.130.192.105

Can configure firewall if desired.

### Response Time
Return 200 OK within 30 seconds or Stripe will retry.

---

## 📞 Support

**Stripe Webhook Docs:** https://stripe.com/docs/webhooks
**Test Events:** Stripe Dashboard → Developers → Webhooks → "Send test event"
**Logs:** Stripe Dashboard → Developers → Logs

---

## ✅ Checklist

- [ ] Create webhook endpoint in Stripe Dashboard
- [ ] Select "Your account" scope
- [ ] Select relevant events to listen for
- [ ] Copy signing secret
- [ ] Store secret in secrets file
- [ ] Start webhook server
- [ ] Test webhook with Stripe test event
- [ ] Verify webhook server receives events
- [ ] Implement business logic (receipt emails, etc.)
- [ ] Monitor webhook logs

---

*Generated by Miles for Performance Supply Depot LLC*
