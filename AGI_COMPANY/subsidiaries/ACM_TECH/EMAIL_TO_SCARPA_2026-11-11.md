# Email to Jon Scarpa — ACM API Credential Refresh / Authentication Access

**To:** Jon.Scarpa@acmtech.com
**CC:** michael.harrison@acmtech.com
**From:** antonio.hudnall@gmail.com
**Subject:** ACM API Integration (#71152) — Credential Refresh & Authentication Access

---

Hi Jon,

Following up on our API integration for Performance Supply Depot (Customer ID #71152).

Our SOAP client is rebuilt and ready to place ribbon orders, but we're still getting a **403 "Missing CN header"** on both:
- `https://api.acmtech.com/oauth/token`
- `https://api.acmtech.com/DataIntegration.asmx`

That error indicates the API now requires **client-certificate (x509) authentication**, or that our credentials have rotated since our last integration (May 2026). The credentials we hold appear to be stale.

Could you please help us resolve one of the following:

1. **Refresh/rotate our API credentials** (Client ID / Client Secret / Password), or
2. **Issue the x509 client certificate** (the "CN" header the API is requesting), or
3. **Whitelist our static IP** — `31.97.6.40`

**Account details:**
- Customer ID: 71152
- Company: Performance Supply Depot LLC
- Static IP: 31.97.6.40

We're ready to submit ribbon orders (ACM part #s `38619ERC30BR` and `51619RC700BR`) the moment authentication is sorted.

Thanks,
**Antonio Hudnall**
Performance Supply Depot LLC (#71152)
888-881-6834 · info@psdepot.com
