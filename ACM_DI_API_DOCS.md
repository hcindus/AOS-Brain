# ACM DI (Data Integration) API Documentation

**Source:** https://api-help.acmtech.com/  
**Vendor:** ACM Technologies, Inc. (ACM)  
**Purpose:** Supply chain integration for 62245 ribbons/ink/toner  
**Date Extracted:** 2026-04-22

---

## 🎯 API OVERVIEW

ACM DI provides a **SOAP-based API** for:
- Product catalog access (ribbons, ink, toner)
- Inventory/pricing queries
- Order submission
- Shipping tracking
- Invoice retrieval

**Protocol:** SOAP XML (not REST/JSON)  
**Endpoint:** `https://api.acmtech.com`  
**Documentation:** `https://api-help.acmtech.com`

---

## 🔐 AUTHENTICATION

Three authentication methods supported:

### 1. DNS Validation
- Domain-based verification
- Requires DNS record configuration

### 2. Service Token
- API key/token-based authentication
- Most common for automated integrations
- **Recommended for supply chain automation**

### 3. Static IP
- IP address whitelisting
- Requires fixed IP from customer

---

## 🛒 ORDER SUBMISSION PROCESS

### 5-Step Transaction Flow

#### Step 1: Begin Transaction
- Initialize order session
- Returns transaction ID

#### Step 2: Order Header
- Submit order metadata
- Customer info, shipping address, PO number

#### Step 3: Order Detail
- Submit line items
- Product SKUs, quantities

#### Step 4: Check Availability
- Real-time inventory check
- Pricing confirmation
- Backorder status

#### Step 5: End Transaction
- Finalize order
- Receive order confirmation
- Get order ID

---

## 🚚 SHIPPING INFORMATION

### Step 6: Tracking Numbers
- Retrieve tracking numbers for orders
- Carrier information (UPS, FedEx, etc.)

### Step 7: Items Shipped
- Detailed shipment information
- Line items shipped
- Partial shipment handling

---

## 💰 INVOICE QUERIES

### Step 8: Invoice Summary
- List of invoices
- Date ranges, amounts, status

### Step 9: Invoice Detail
- Line-item invoice details
- Product SKUs, quantities, pricing
- Tax and shipping breakdowns

---

## 🛠️ UTILITIES

### Step A: City/State by Zip
- Input: ZIP code
- Output: City, State

### Step B: Zip by City/State
- Input: City, State
- Output: ZIP codes

### Step C: Get Product List ⭐ KEY
- **CRITICAL FOR SUPPLY CHAIN AUTOMATION**
- Returns complete product catalog
- Includes: SKU, description, pricing, availability
- **Use this to build live product status page**

---

## 📦 PRODUCT CATALOG (Expected)

Based on ACM's business (di.acmtech.com), the API provides:

| Category | Products |
|----------|----------|
| **Ribbons** | 62245 ribbons (your specific need) |
| **Ink** | Printer ink cartridges |
| **Toner** | Laser toner cartridges |
| **Supplies** | POS supplies, printer supplies |

**Note:** Exact SKUs and product list available via `Get Product List` utility.

---

## 🔄 INTEGRATION WORKFLOW

```
┌─────────────────────────────────────────────────────────────┐
│                    SUPPLY CHAIN AUTOMATION                   │
└─────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│ Product Sync │    │  Order Flow  │    │  Tracking    │
│  (5 min)     │    │  (Real-time) │    │  (Polling)   │
└──────────────┘    └──────────────┘    └──────────────┘
        │                   │                   │
        ▼                   ▼                   ▼
┌─────────────────────────────────────────────────────────────┐
│                    ACM DI SOAP API                           │
│         https://api.acmtech.com                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🛠️ TECHNICAL SPECIFICATIONS

### Request Format
```xml
<?xml version="1.0" encoding="UTF-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Header>
    <!-- Authentication -->
  </soap:Header>
  <soap:Body>
    <!-- API Request -->
  </soap:Body>
</soap:Envelope>
```

### Response Format
```xml
<?xml version="1.0" encoding="UTF-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <!-- API Response -->
  </soap:Body>
</soap:Envelope>
```

---

## 📋 NEXT STEPS FOR INTEGRATION

1. **Request API Access**
   - Email: askacm@acmtech.com
   - Subject: "API Access Request"
   - Mention: 62245 ribbons, supply chain automation

2. **Obtain Credentials**
   - Service Token (preferred)
   - Or Static IP setup

3. **Test Product List Query**
   - Use Step C: Get Product List
   - Verify ribbon SKUs available

4. **Implement Live Status Page**
   - Poll product list every 5 minutes
   - Display: SKU, description, price, stock

5. **Build Order Pass-Through**
   - Customer submits order on your platform
   - Forward to ACM via Steps 1-5
   - Return confirmation to customer

---

## 🔗 RELATED LINKS

| Resource | URL |
|----------|-----|
| **API Web Form** | https://api.acmtech.com |
| **API Documentation** | https://api-help.acmtech.com |
| **Partner Services** | https://di.acmtech.com |
| **Request Access** | mailto:askacm@acmtech.com |
| **FTP Docs** | https://ftp-help.acmtech.com |

---

**Extracted by:** Miles (AOS Agent)  
**Date:** 2026-04-22  
**Status:** Ready for prototype development
