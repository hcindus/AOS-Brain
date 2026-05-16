# ACM Technologies - Performance Supply Depot Account

**Customer ID:** 71152  
**Company:** Performance Supply Depot LLC  
**Status:** API Code Corrected - Ready for Testing

---

## 📊 ACCOUNT STATUS

| Item | Status | Notes |
|------|--------|-------|
| API Access | ✅ Granted | Test mode (orders don't process) |
| Credentials | ✅ Retrieved | Stored in `acm_api.env` |
| SOAP Client | ✅ Fixed | Rebuilt per Jon Scarpa's spec (2026-05-15) |
| Connection Test | ⏳ Pending | Next step: validate connectivity |
| Order Submission | ⏳ Pending | After connection confirmed |
| Production Activation | ⏳ Pending | Requires validation with Jon |

---

## 🔐 CREDENTIALS

**Location:** `/root/.openclaw/workspace/aocros/secrets/acm_api.env`

| Field | Value |
|-------|-------|
| UserID | 71152 |
| Password | See secure env file |
| Customer ID | 71152 |

---

## 🔧 TECHNICAL FIX

**Problem:** Original automation sent REST/JSON → API rejected all calls  
**Solution:** Rebuilt with proper SOAP/XML structure

**Changes Made:**
1. ✅ SOAP 1.1 envelopes with correct namespace
2. ✅ UserID/Password in SOAP body (each step)
3. ✅ 5-step transaction flow implemented
4. ✅ XML parsing for responses

**Files:**
- `acm_soap_client.py` - New corrected client
- `ACM_SOAP_API_CORRECTED.md` - Fixed documentation

---

## 🧪 NEXT STEPS

### Immediate
1. **Test API Connection**
   ```bash
   cd /root/.openclaw/workspace/aocros/supply_depot/acm_di_integration
   python3 acm_soap_client.py
   ```

2. **Verify Endpoint**
   - Current: `https://api.acmtech.com/DataIntegration.asmx`
   - May need adjustment based on ACM docs

3. **Test Order Flow**
   - Use test mode (no real orders)
   - Validate SOAP structure

### Validation
4. **Contact Jon Scarpa**
   - Email: Jon.Scarpa@acmtech.com
   - Confirm test order format
   - Request production activation

---

## 📞 CONTACTS

| Name | Role | Contact |
|------|------|---------|
| Jon Scarpa | IT Manager | Jon.Scarpa@acmtech.com, (951) 738-9898 x222 |
| Michael Harrison | Account Executive | michael.harrison@acmtech.com |

---

## 📋 API STEPS

```
Step 1: Begin Transaction → Get Transaction_ID
Step 2: Order Header → Submit customer/shipping
Step 3: Order Detail → Submit line items
Step 4: (Check Availability - optional)
Step 5: End Transaction → Finalize order
```

---

## 🗂️ FILES

| File | Purpose |
|------|---------|
| `acm_soap_client.py` | Corrected SOAP client |
| `acm_di_client.py` | Old/incorrect REST client (deprecated) |
| `acm_api.env` | Credentials (secure) |
| `ACM_SOAP_API_CORRECTED.md` | Documentation |

---

**Last Updated:** 2026-05-16  
**Fixed By:** Miles (AOS Agent)