# Email to Jon Scarpa - ACM API Connection Issue (Updated)

**To:** Jon.Scarpa@acmtech.com  
**CC:** michael.harrison@acmtech.com  
**From:** antonio.hudnall@gmail.com  
**Re:** ACM API Integration - Client Certificate / Auth Method Required

---

Hi Jon,

Following up on the API integration for Performance Supply Depot (#71152).

## Diagnostic Results

**Error:** `403 Forbidden - Missing CN header`

**Findings:**
- All API endpoints return 403 with "Missing CN header" response
- OAuth token endpoint also returns 403
- `di.acmtech.com` portal loads fine (200)
- SOAP requests fail regardless of authentication method tried

**Our IP:** `31.97.6.40`

## Root Cause Analysis

The "Missing CN header" error indicates **client certificate authentication (x509)** is required. The CN (Common Name) field in a client certificate is expected but not being provided.

## Authentication Methods per Our Profile

Looking at our security gateway options:

| Method | Status | Issue |
|--------|--------|-------|
| A. DNS Verification | Not configured | Needs domain setup |
| B. Service Tokens | Client ID/Secret provided | Still returns 403 |
| C. Static IP | None configured | May need IP whitelisting |

## Questions

1. **Client Certificate:** Do you need to issue us an x509 client certificate for the CN header?

2. **Static IP Whitelisting:** Should we proceed with Method C? Our IP is `31.97.6.40`

3. **DNS Method:** Should we provide a domain for Method A authentication?

4. **Service Token + DNS:** Does Method B (Service Tokens) require Method A (DNS) to be configured first?

## Request

Please advise which authentication method we should use:
- **Option 1:** Provide client certificate for x509 authentication
- **Option 2:** Whitelist IP `31.97.6.40` (Static IP method)
- **Option 3:** Configure DNS verification (provide domain)

Once authentication is resolved, we have the SOAP client ready with:
- ✅ OAuth2 support (if that's the path)
- ✅ SOAP 1.1 with proper namespace
- ✅ 5-step transaction flow
- ✅ Price validation per line item
- ✅ Product list, tracking, invoices

Thanks,  
Antonio Hudnall  
Performance Supply Depot (#71152)  
miles@myl0nr0s.cloud

---

## Technical Notes

**Tested endpoints:**
```
https://api.acmtech.com/DataIntegration.asmx
https://api.acmtech.com/oauth/token
https://api.acmtech.com/auth/token
```

**All return:** `403 Missing CN header`

**SOAP sample tried:**
```xml
POST /DataIntegration.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: http://microsoft.com/webservices/Step1_BeginTransaction
Authorization: Bearer {token}

<soap:Envelope>
  <soap:Body>
    <Step1_BeginTransaction xmlns="http://microsoft.com/webservices/">
      <UserID>71152</UserID>
      <Password>***</Password>
    </Step1_BeginTransaction>
  </soap:Body>
</soap:Envelope>
```

**Response:** `403 Missing CN header`