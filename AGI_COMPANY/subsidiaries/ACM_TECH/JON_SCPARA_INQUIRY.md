# Email to Jon Scarpa - ACM API Connection Issue

**To:** Jon.Scarpa@acmtech.com  
**CC:** michael.harrison@acmtech.com  
**From:** antonio.hudnall@gmail.com  
**Re:** ACM API Integration - Connection Diagnostic Results

---

Hi Jon,

Thanks for the detailed SOAP documentation. I've rebuilt our automation client with the correct XML structure per your email.

However, I'm getting **403 Forbidden** when attempting to connect to the API endpoints. Here's what I found:

## Diagnostic Results

**Error:** `403 Forbidden - Missing CN header`

**Endpoints tested:**
- `https://api.acmtech.com/DataIntegration.asmx` - 403
- `https://api.acmtech.com/Order.asmx` - 403
- `https://api.acmtech.com/` - 403

**Working:**
- `https://di.acmtech.com/` - 200 ✓ (Portal loads)
- `https://www.acmtech.com/` - 200 ✓

**Our IP:** `31.97.6.40`

## Questions

1. **Client Certificate:** Does the API require a client certificate (x509) for authentication? The "Missing CN header" error suggests this.

2. **Static IP Whitelisting:** Should I provide our IP for whitelisting? Our outbound IP is `31.97.6.40`.

3. **Endpoint Confirmation:** Is `api.acmtech.com/DataIntegration.asmx` the correct SOAP endpoint, or should we be using a different URL?

4. **Test Mode:** Is account #71152 activated for API test mode?

## What I've Built

- ✅ SOAP 1.1 client with proper namespace (`http://microsoft.com/webservices/`)
- ✅ 5-step transaction flow (Begin → Header → Detail → Check → End)
- ✅ Price validation included per line item
- ✅ Additional methods: Product list, availability, tracking, invoices

Just need to resolve this connection issue to begin testing.

Let me know the best path forward.

Thanks,  
Antonio Hudnall  
Performance Supply Depot (#71152)  
miles@myl0nr0s.cloud | (555) 019-2834

---

## Technical Notes (for reference)

**SOAP Test Request:**
```xml
POST https://api.acmtech.com/DataIntegration.asmx
Content-Type: text/xml; charset=utf-8
SOAPAction: http://microsoft.com/webservices/Step1_BeginTransaction

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <Step1_BeginTransaction xmlns="http://microsoft.com/webservices/">
      <UserID>71152</UserID>
      <Password>[REDACTED]</Password>
    </Step1_BeginTransaction>
  </soap:Body>
</soap:Envelope>
```

**Response:** `403 Forbidden - Missing CN header`