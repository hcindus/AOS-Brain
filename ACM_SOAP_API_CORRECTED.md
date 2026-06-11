# ACM Technologies SOAP API - CORRECTED Documentation

**Source:** Jon Scarpa email (2026-05-15)  
**Fixed Date:** 2026-05-16  
**Previous Issue:** REST/JSON calls were failing - API is SOAP-based, not REST

---

## 🔴 CRITICAL FIX

**What was wrong:**
- Previous automation sent REST/JSON requests
- ACM API expects SOAP/XML requests
- Protocol mismatch caused all calls to fail

**What's fixed:**
- Proper SOAP 1.1 XML envelopes
- Correct namespace: `http://microsoft.com/webservices/`
- UserID/Password embedded in each SOAP body (not headers)
- Proper 5-step transaction flow

---

## 📋 AUTHENTICATION

Each SOAP request includes:
```xml
<UserID>YourUserID</UserID>
<Password>YourPassword</Password>
```

**Credentials for Performance Supply Depot:**
- UserID: `71152`
- Password: See secure note / `acm_api.env`

---

## 🔄 ORDER SUBMISSION FLOW

### Step 1: Begin Transaction
**Action:** `Step1_BeginTransaction`

```xml
<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <Step1_BeginTransaction xmlns="http://microsoft.com/webservices/">
      <UserID>71152</UserID>
      <Password>YourPassword</Password>
    </Step1_BeginTransaction>
  </soap:Body>
</soap:Envelope>
```

**Returns:** Transaction_ID (UUID format)

---

### Step 2: Order Header
**Action:** `Step2_OrderHeaderFulfillment`

```xml
<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <Step2_OrderHeaderFulfillment xmlns="http://microsoft.com/webservices/">
      <UserID>71152</UserID>
      <Password>YourPassword</Password>
      <Transaction_ID>ABCD1234-EFGH-5678-IJKL-9012MNOP3456</Transaction_ID>
      <OrderDate>2024/03/15</OrderDate>
      <PO>PO12345</PO>
      <ItemCnt>5</ItemCnt>
      <MailingName>David Johnson</MailingName>
      <Address1>1234 Gale Ave</Address1>
      <City>Eureka</City>
      <State>CA</State>
      <Zip>90165</Zip>
      <Country>US</Country>
    </Step2_OrderHeaderFulfillment>
  </soap:Body>
</soap:Envelope>
```

**Fields:**
| Field | Format | Notes |
|-------|--------|-------|
| Transaction_ID | UUID | From Step 1 |
| OrderDate | YYYY/MM/DD | 2024/03/15 |
| PO | String | Purchase order number |
| ItemCnt | Integer | Total line items |
| MailingName | String | Ship to name |
| Address1 | String | Street address |
| City | String | City name |
| State | String | 2-letter code (CA) |
| Zip | String | ZIP code |
| Country | String | US (default) |

---

### Step 3: Order Detail Line
**Action:** `Step3_OrderDetailFulfillment`

Called once per line item:

```xml
<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <Step3_OrderDetailFulfillment xmlns="http://microsoft.com/webservices/">
      <UserID>71152</UserID>
      <Password>YourPassword</Password>
      <Transaction_ID>ABCD1234-EFGH-5678-IJKL-9012MNOP3456</Transaction_ID>
      <ACM_ItemNo>652334560T</ACM_ItemNo>
      <Qty>5</Qty>
      <Price>23.99</Price>
    </Step3_OrderDetailFulfillment>
  </soap:Body>
</soap:Envelope>
```

**Fields:**
| Field | Format | Notes |
|-------|--------|-------|
| ACM_ItemNo | String | ACM SKU |
| Qty | Integer | Quantity ordered |
| Price | Decimal | Unit price |

---

### Step 5: End Transaction
**Action:** `Step5_EndTransaction`

```xml
<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <Step5_EndTransaction xmlns="http://microsoft.com/webservices/">
      <UserID>71152</UserID>
      <Password>YourPassword</Password>
      <Transaction_ID>ABCD1234-EFGH-5678-IJKL-9012MNOP3456</Transaction_ID>
    </Step5_EndTransaction>
  </soap:Body>
</soap:Envelope>
```

**Returns:** Order confirmation/order ID

---

## 💰 PRICE VALIDATION (Key Point from Jon)

ACM validates the purchase price we submit:
- Price is included in each line item (Step 3)
- ACM validates on their end
- Ensures customers see transparent pricing
- Prevents invoice discrepancies

```python
OrderItem(sku="652334560T", quantity=5, price=23.99)
# Price submitted → ACM validates → Customer sees final price
```

---

## 🛠️ API REFERENCE

### Order Submission
| Step | Method | Description |
|------|--------|-------------|
| 1 | Step1_BeginTransaction | Initialize order session |
| 2 | Step2_OrderHeaderFulfillment | Submit customer/shipping info |
| 3 | Step3_OrderDetailFulfillment | Submit line items with **price** |
| 4 | Step4_CheckAvailability | Verify real-time inventory (Page 13) |
| 5 | Step5_EndTransaction | Finalize order |

### Additional Capabilities (Pages 16, 19-20, 24)
| Method | Description | Page |
|--------|-------------|------|
| GetProductList | Daily pricing, inventory, images | Page 24 |
| Step4_CheckAvailability | Real-time availability | Page 13 |
| GetTracking | Shipment tracking | Page 16 |
| GetInvoiceSummary | Invoice list by date | Page 19 |
| GetInvoiceDetail | Detailed line items | Page 20 |

---

## 📦 IMPLEMENTATION

**Python client:** `acm_soap_client.py`

```python
from acm_soap_client import ACMSOAPClient, OrderHeader, OrderItem, ShippingAddress

# Initialize
client = ACMSOAPClient(user_id="71152", password="your_password")

# Create order header
ship_to = ShippingAddress(
    name="David Johnson",
    address1="1234 Gale Ave",
    city="Eureka",
    state="CA",
    zip_code="90165"
)

header = OrderHeader(
    po_number="PO12345",
    order_date="2024/03/15",
    item_count=1,
    ship_to=ship_to
)

# Create line items
items = [
    OrderItem(sku="652334560T", quantity=5, price=23.99)
]

# Submit order
result = client.submit_full_order(header, items)

if result['success']:
    print(f"Order submitted: {result['order_id']}")
else:
    print(f"Error: {result['error']}")
```

---

## 🔗 ENDPOINT

**Base URL:** `https://api.acmtech.com/DataIntegration.asmx`

*Note: Actual endpoint may vary - verify with Jon Scarpa if connection fails*

---

## 👥 CONTACTS

| Name | Role | Contact |
|------|------|---------|
| Jon Scarpa | IT Manager | Jon.Scarpa@acmtech.com, (951) 738-9898 x222 |
| Michael Harrison | Account Executive | michael.harrison@acmtech.com |

---

## 📚 REFERENCES

- API Docs: https://api-help.acmtech.com
- Original Email: Jon Scarpa (2026-05-15) RE: ACM Tracking — PO 051426007

---

**Fixed by:** Miles (AOS Agent)  
**Date:** 2026-05-16