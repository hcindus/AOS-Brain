# Phone Login System - Installation Guide
## AGI Company Business Login

---

## Overview

This system allows businesses to log in using their **phone number**:
1. Enter business phone → System looks up business in database
2. Verify phone with SMS code
3. Confirm shipping/billing address
4. Provide email for receipts
5. Proceed to order/checkout

---

## Prerequisites

- Python 3.8+
- pip3
- Business database (YP.com scraped data)
- SQLite3

---

## Installation

### Step 1: Clone Repository
```bash
git clone https://github.com/hcindus/aos-brain.git
cd aos-brain/aos_brain_py
```

### Step 2: Install Dependencies
```bash
pip3 install fastapi uvicorn pydantic
```

### Step 3: Setup Database
```bash
# The database will be created automatically on first run
# Data location: /root/.openclaw/workspace/data/phone_auth.db
```

### Step 4: Run the Server
```bash
python3 phone_login_web.py
```

Server starts on: **http://localhost:8080**

---

## Configuration

### Business Database

The system looks up businesses in:
- `/data/north_america_businesses/north_america_master.json`
- `/data/yp_businesses/business_database.json`

**To populate:**
```bash
# Scrape YP.com data
node north_america_scraper.js
```

### Environment Variables (Optional)

```bash
# For SMS (Twilio)
export TWILIO_ACCOUNT_SID=your_sid
export TWILIO_AUTH_TOKEN=your_token
export TWILIO_PHONE_NUMBER=+1234567890
```

---

## Usage

### Web Interface

1. Open browser: `http://YOUR_VPS_IP:8080`
2. Enter business phone number
3. System finds matching business
4. Verify with SMS code
5. Confirm address
6. Enter email
7. Select product and order

### API Endpoints

```bash
# Step 1: Lookup business
curl -X POST http://localhost:8080/api/lookup \
  -H "Content-Type: application/json" \
  -d '{"phone": "(555) 123-4567"}'

# Step 2: Verify code
curl -X POST http://localhost:8080/api/verify-phone \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "code": "123456"}'

# Step 3: Verify address
curl -X POST http://localhost:8080/api/verify-address \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "address_correct": true}'

# Step 4: Collect email
curl -X POST http://localhost:8080/api/collect-email \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "email": "owner@business.com"}'

# Step 5: Create order
curl -X POST http://localhost:8080/api/create-order \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "product": "Greet", "price": "$249"}'
```

---

## Database Schema

### users table
- id, phone, business_name, address, city, state, zip_code
- country, address_verified, email, email_verified
- verification_code, code_expires, created_at

### orders table
- id, user_id, product, price, status
- shipping_address, billing_address, created_at

---

## Security Notes

- Phone numbers normalized to 10 digits
- Verification codes expire in 10 minutes
- Address must be verified before ordering
- SQLite database secured with file permissions

---

## Troubleshooting

### "Business not found"
- Run scraper first: `node north_america_scraper.js`
- Check database exists in `/data/`

### "Port already in use"
```bash
# Change port in phone_login_web.py
uvicorn.run(app, host="0.0.0.0", port=8081)  # Different port
```

### Database locked
```bash
# Check for other processes
lsof /root/.openclaw/workspace/data/phone_auth.db
```

---

## Files

| File | Purpose |
|------|---------|
| `enhanced_phone_login.py` | Core login system logic |
| `phone_login_web.py` | FastAPI web server + HTML |
| `north_america_scraper.js` | Business database scraper |
| `GITHUB_INSTALL.md` | This file |

---

## Support

- Email: miles@myl0nr0s.cloud
- GitHub: https://github.com/hcindus/aos-brain

---

**Last Updated:** 2026-03-28
**Version:** 1.0
