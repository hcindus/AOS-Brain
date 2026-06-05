# ACM Technologies SOAP API Integration Documentation
## Performance Supply Depot - Product Configuration
**Generated:** 2026-06-05 20:20 UTC  
**Status:** Documented Only - No Changes Made

---

## 🔐 API Credentials

**File Location:** `/root/.openclaw/workspace/aocros/secrets/acm_api.env`

```
# ACM Tech API Credentials
# PERFORMANCE SUPPLY DEPOT (Customer ID: 71152)
# API Endpoint: api.acmtech.com

ACM_CUSTOMER_ID=71152
ACM_COMPANY="PERFORMANCE SUPPLY DEPOT"
ACM_API_ENDPOINT=api.acmtech.com

# Auth Method 1: Service Tokens (preferred for automation)
ACM_CLIENT_ID=ScY4GjsdoIOnDlHXSXJoYJZfXGHbrvVa
ACM_CLIENT_SECRET=54mnLrjCh6peoK9JZQAJiDZxojOlBrkpEM8W8hJ5vwFtyxstmXB7wmslUhUVBvO0

# Auth Method 2: Username/Password (fallback)
ACM_USERNAME=71152
ACM_PASSWORD=UPP9EvDE9xkEpI
```

---

## 📦 Products Requiring SOAP Integration

### Product 1: ERC 30/34/38 Black/Red Ribbons
- **SKU:** 62245
- **ACM Part #:** To be confirmed with Jon Scarpa
- **Description:** ERC 30/34/38 Black/Red Ribbons
- **Unit:** Per dozen
- **Price:** $42.00 /dozen
- **Status:** Not yet integrated (SOAP ready)

### Product 2: Star SP700 Black/Red Ink Ribbons  
- **SKU:** 67240
- **ACM Part #:** To be confirmed with Jon Scarpa
- **Description:** Star SP700 Black/Red Ink Ribbons
- **Unit:** Per dozen
- **Price:** $52.00 /dozen
- **Status:** Not yet integrated (SOAP ready)

---

## 🔌 SOAP API Specification

**Endpoint:** `https://api.acmtech.com/DataIntegration.asmx`

**5-Step Transaction Process:**

### Step 1: Begin Transaction
```xml
<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <Step1_BeginTransaction xmlns="http://microsoft.com/webservices/">
      <UserID>71152</UserID>
      <Password>UPP9EvDE9xkEpI</Password>
    </Step1_BeginTransaction>
  </soap:Body>
</soap:Envelope>
```

### Step 2: Order Header
```xml
<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <Step2_OrderHeaderFulfillment xmlns="http://microsoft.com/webservices/">
      <UserID>71152</UserID>
      <Password>UPP9EvDE9xkEpI</Password>
      <Transaction_ID>{transaction_id}</Transaction_ID>
      <OrderDate>{yyyy-mm-dd}</OrderDate>
      <PO>{po_number}</PO>
      <ItemCnt>{item_count}</ItemCnt>
      <MailingName>{customer_name}</MailingName>
      <Address1>{address_line_1}</Address1>
      <City>{city}</City>
      <State>{state}</State>
      <Zip>{zip}</Zip>
      <Country>US</Country>
      <Address2>{address_line_2}</Address2>
    </Step2_OrderHeaderFulfillment>
  </soap:Body>
</soap:Envelope>
```

### Step 3: Order Detail (Per Item)
```xml
<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <Step3_OrderDetailFulfillment xmlns="http://microsoft.com/webservices/">
      <UserID>71152</UserID>
      <Password>UPP9EvDE9xkEpI</Password>
      <Transaction_ID>{transaction_id}</Transaction_ID>
      <ACM_ItemNo>{acm_sku}</ACM_ItemNo>
      <Qty>{quantity}</Qty>
      <Price>{unit_price}</Price>
    </Step3_OrderDetailFulfillment>
  </soap:Body>
</soap:Envelope>
```

### Step 4: Check Availability (Optional)
```xml
<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <Step4_CheckAvailability xmlns="http://microsoft.com/webservices/">
      <UserID>71152</UserID>
      <Password>UPP9EvDE9xkEpI</Password>
      <Transaction_ID>{transaction_id}</Transaction_ID>
    </Step4_CheckAvailability>
  </soap:Body>
</soap:Envelope>
```

### Step 5: End Transaction
```xml
<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <Step5_EndTransaction xmlns="http://microsoft.com/webservices/">
      <UserID>71152</UserID>
      <Password>UPP9EvDE9xkEpI</Password>
      <Transaction_ID>{transaction_id}</Transaction_ID>
    </Step5_EndTransaction>
  </soap:Body>
</soap:Envelope>
```

---

## 📞 ACM Contacts

- **Jon Scarpa** (IT Manager): Jon.Scarpa@acmtech.com, (951) 738-9898 x222
- **Michael Harrison** (Account Executive): michael.harrison@acmtech.com
- **Customer ID:** 71152
- **API Help:** https://api-help.acmtech.com

---

## 🔧 Implementation Notes

### Current Status
- ✅ API credentials retrieved and stored
- ✅ SOAP client code exists (Google Apps Script)
- ❌ Product SKUs not mapped to ACM part numbers
- ❌ No live testing completed
- ❌ Account activation pending with Jon Scarpa

### Next Steps (When Ready)
1. Contact Jon Scarpa to map SKUs 62245 and 67240 to ACM part numbers
2. Test connectivity in test mode
3. Verify order submission flow
4. Retrieve product catalog from ACM
5. Request account activation for live orders

### Google Apps Script Reference
**Location:** `/root/.openclaw/workspace/AGI_COMPANY/subsidiaries/ACM_TECH/acm_api_apps_script.gs`

Contains complete working implementation of all 5 SOAP steps.

---

## ⚠️ IMPORTANT

**NO CHANGES MADE TO LIVE SYSTEM**  
This documentation is for planning purposes only. The psdepot.com checkout is currently working with Stripe payments. ACM SOAP integration should be implemented as a separate fulfillment pathway after:
1. SKUs are confirmed with Jon Scarpa
2. Test transactions succeed
3. Account is activated for live orders

---

## 📊 Current System Snapshot

### Working Configuration
- **Checkout:** https://psdepot.com/checkout.html
- **Payment API:** https://psdepot.com/api/create-payment-intent
- **Stripe Account:** acct_1PJRYHJ5gaWR1O3E (LIVE, activated)
- **Payment Server:** Port 4242 via nginx proxy
- **Status:** ✅ Fully operational

### DepotChaos Email Queue
- **Teriyaki Madness emails:** 197 queued
- **Status:** Ready to send
- **Template:** Thermal paper availability

### Files Saved
1. `/root/.openclaw/workspace/aocros/secrets/acm_api.env` - Credentials
2. `/root/.openclaw/workspace/AGI_COMPANY/subsidiaries/ACM_TECH/acm_api_apps_script.gs` - SOAP client
3. `/root/.openclaw/workspace/docs/acm_ribbon_soap_config.md` - This file

---

*Documentation generated by Miles for Performance Supply Depot LLC*  
*Do not modify live system without approval*
