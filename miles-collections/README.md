# Miles Collections Module
## Production-Ready Collections System

**Version:** 1.0.0  
**Built by:** Miles  
**Status:** Operational

---

## Quick Start

```bash
cd /root/.openclaw/workspace/miles-collections

# Add a test account
node miles-collections.js add "Acme Corp" "billing@acme.com" "555-1234" 5000 45

# List all accounts
node miles-collections.js list

# View metrics
node miles-collections.js metrics

# Export to CSV
node miles-collections.js export > accounts.csv
```

---

## Features

| Feature | Description |
|---------|-------------|
| **Persistent Storage** | JSON files in `/data` directory |
| **Priority Scoring** | Auto-calculate critical/high/medium/low |
| **4 Workflows** | Early, Mid, Late stage, Payment plan |
| **Payment Tracking** | Record payments, track balance |
| **Communication Log** | Track all contact attempts |
| **Payment Plans** | Automated installment plans |
| **CSV Export** | Easy reporting and analysis |
| **Event Emitter** | Hook into account lifecycle |

---

## API

### Initialize
```javascript
const MilesCollections = require('./miles-collections');
const collections = new MilesCollections({ tier: 'professional' });
await collections.init();
```

### Add Account
```javascript
const account = await collections.addAccount({
  debtorName: 'Customer Name',
  debtorEmail: 'customer@email.com',
  debtorPhone: '555-1234',
  balance: 5000.00,
  daysDelinquent: 45,
  invoiceRefs: ['INV-001']
});
```

### Process Payment
```javascript
const payment = await collections.processPayment(accountId, 500.00, 'credit_card');
```

### Get Metrics
```javascript
const metrics = collections.getMetrics();
// Returns: totalAccounts, recoveryRate, totalRecovered, byPriority, etc.
```

---

## Data Structure

```json
{
  "id": "acc_1234567890",
  "debtor": {
    "name": "Customer Name",
    "email": "customer@email.com",
    "phone": "555-1234",
    "address": "123 Main St"
  },
  "originalBalance": 5000.00,
  "currentBalance": 4500.00,
  "daysDelinquent": 45,
  "status": "active",
  "priority": "high",
  "workflow": "mid_stage",
  "payments": [],
  "communications": [],
  "createdAt": "2026-06-12T01:00:00.000Z"
}
```

---

## Workflows

### Early Stage (0-30 days)
- Day 0: Friendly email reminder
- Day 3: Follow-up email
- Day 7: SMS reminder
- Day 14: Phone call

### Mid Stage (31-60 days)
- Day 31: Urgent notice
- Day 35: Phone call
- Day 45: Demand letter
- Day 60: Final notice

### Late Stage (60+ days)
- Day 61: Legal notice
- Day 75: Collection agency
- Day 90: Litigation prep

---

## Priority Calculation

```
Score = (Balance × 0.6) + (Days × 10)

Critical: Score ≥ 5000
High:     Score ≥ 2000
Medium:   Score ≥ 500
Low:      Score < 500
```

---

## Events

```javascript
collections.on('account:added', (account) => {
  console.log('New account:', account.id);
});

collections.on('payment:received', ({ accountId, payment }) => {
  console.log('Payment:', payment.amount);
});

collections.on('account:paid', (account) => {
  console.log('Account paid:', account.id);
});
```

---

## File Locations

| Path | Purpose |
|------|---------|
| `miles-collections.js` | Main service |
| `data/*.json` | Account storage |
| `templates/` | Outreach templates |

---

## Next Steps

- [ ] Email template integration
- [ ] SMS via Twilio
- [ ] Voice calls via Twilio
- [ ] Automated workflow execution
- [ ] Web dashboard
- [ ] API server

---

*Built with ❤️ by Miles for Performance Supply Depot*
