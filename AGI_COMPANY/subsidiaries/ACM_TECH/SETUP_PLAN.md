# ACM Technologies API Integration Plan

**Customer:** Performance Supply Depot (#71152)  
**Date:** 2026-05-02  
**Status:** Awaiting credential retrieval

---

## Phase 1: Credential Retrieval (NEXT STEP)

1. **Visit secure note URL:**
   ```
   https://secure-send.acmtech.com/note/5U567H575R4G6Z5g5e6T487Y6Q5C6O4i815O626J5i4k636B6W6n7J7B7t7E6q5Q#b4399ab938c0b925ba12558c0b856163746afb4cb1de0308775521c56af136ff
   ```

2. **Store credentials securely** in:
   - `acm_tech_config.json` (credentials section)
   - Or environment variables

3. **Contact Jon Scarpa** if link expired:
   - Email: Jon.Scarpa@acmtech.com
   - Phone: (951) 738-9898 Ext: 222

---

## Phase 2: API Authentication Test

1. **Test API connectivity**
   - Endpoint: `https://api.acmtech.com`
   - Auth method: TBD (likely API key or OAuth)

2. **Verify test mode access**
   - Account starts in test mode
   - Orders won't process until validated

3. **Document authentication flow**

---

## Phase 3: Product Catalog Sync

1. **Retrieve full product file**
   - Description
   - Pricing
   - Images
   - Availability

2. **Map ACM SKUs to PSDEPOT SKUs**
   - Align product codes
   - Update pricing strategy

3. **Store local product cache**

---

## Phase 4: Automation Setup

1. **Build order submission module**
   - Submit purchase orders via API
   - Check item availability before ordering
   - Track order status

2. **Invoice retrieval**
   - Automated invoice download
   - Accounting system integration

3. **Inventory sync**
   - Price updates
   - Stock level checks

---

## Phase 5: Testing & Validation

1. **Place test orders** (test mode)
2. **Validate with Jon Scarpa**
3. **Request account activation**
4. **Go live**

---

## Contacts

| Name | Role | Contact |
|------|------|---------|
| Jon Scarpa | IT Manager | Jon.Scarpa@acmtech.com, (951) 738-9898 x222 |
| Michael Harrison | Account Executive | michael.harrison@acmtech.com |

---

## Resources

- **Data Integration Site:** https://di.acmtech.com
- **API Docs:** https://api-help.acmtech.com
- **Company:** ACM Technologies Inc.
- **Address:** 2535 Research Drive, Corona, CA 92882
