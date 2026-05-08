# Security Audit Report - Auth System
**Date:** 2026-05-08
**Auditor:** Miles (AGI Company Security Team)
**Scope:** Complete authentication system

---

## 🚨 CRITICAL VULNERABILITIES

### 1. JWT Algorithm Confusion / None Algorithm Attack
**Location:** `backend/utils/tokens.js` - `verifyAccessToken()`
**Severity:** CRITICAL

**Issue:** The JWT verification does not explicitly specify allowed algorithms:
```javascript
function verifyAccessToken(token) {
    try {
        return jwt.verify(token, process.env.JWT_ACCESS_SECRET); // No algorithm specified!
    } catch (err) {
        return null;
    }
}
```

**Attack:** Attacker can forge tokens using `alg: 'none'` or RS256→HS256 confusion.

**Fix:** Add explicit algorithm restriction:
```javascript
return jwt.verify(token, process.env.JWT_ACCESS_SECRET, { algorithms: ['HS256'] });
```

---

### 2. Weak JWT Secrets in Development
**Location:** `scripts/setup.js`
**Severity:** CRITICAL

**Issue:** Setup script generates hex strings which may be predictable or weak:
```javascript
JWT_ACCESS_SECRET: your-access-secret-min-32-chars-long // Static placeholder!
```

**Attack:** Weak secrets allow brute force of JWT tokens.

**Fix:** Generate cryptographically secure random strings:
```javascript
const crypto = require('crypto');
const secret = crypto.randomBytes(64).toString('base64'); // 512 bits
```

---

### 3. SQL Injection via Raw SQL in Database Queries
**Location:** `backend/utils/tokens.js`, `database/models/User.js`
**Severity:** CRITICAL

**Issue:** SQLite uses parameterized queries but some concatenation exists. However, the main issue is that `db.get()` and `db.run()` are used throughout without proper input validation before the database layer.

**Status:** Reviewed - actually uses parameterized queries correctly. Lower severity.

---

### 4. Timing Attack on Password Comparison
**Location:** `backend/utils/crypto.js`
**Severity:** HIGH

**Issue:** Argon2 verification may have timing differences that leak password correctness:
```javascript
async function verifyPassword(password, hash) {
    try {
        return await argon2.verify(hash, password); // Timing attack possible
    } catch (err) {
        return false;
    }
}
```

**Attack:** Attacker can measure response times to determine if email exists.

**Fix:** Add constant-time comparison or random delay.

---

### 5. Missing Rate Limiting on Token Refresh
**Location:** `backend/routes/auth.js` - `/refresh` endpoint
**Severity:** HIGH

**Issue:** The refresh token endpoint has no rate limiting, allowing infinite token refresh attacks.

---

### 6. CORS Misconfiguration
**Location:** `backend/server.js`
**Severity:** HIGH

**Issue:** CORS allows credentials from any origin:
```javascript
origin: process.env.FRONTEND_URL || 'http://localhost:8080'
```

If `FRONTEND_URL` is not set in production, it defaults to localhost which is wrong.

**Fix:** Be explicit about origins, reject requests without proper origin.

---

### 7. Missing Security Headers
**Location:** `backend/server.js`
**Severity:** MEDIUM

**Issues:**
- No `X-Frame-Options` header
- No `X-Content-Type-Options` header
- No `Referrer-Policy` header
- No `Permissions-Policy` header

---

### 8. Information Disclosure via Error Messages
**Location:** Multiple
**Severity:** MEDIUM

**Issue:** Detailed error messages expose system internals:
```javascript
console.error('Registration error:', err);
res.status(500).json({ error: 'Registration failed' }); // Generic is good
```

Actually this one is fine, but need to check all endpoints.

---

### 9. Insecure Session ID Generation
**Location:** `backend/utils/crypto.js`
**Severity:** MEDIUM

**Issue:** Uses `crypto.randomBytes` which is good, but session IDs should be longer:
```javascript
function generateSecureToken(length = 32) {
    return crypto.randomBytes(length).toString('hex'); // 64 hex chars = 256 bits, good
}
```

Actually this is acceptable (256 bits).

---

### 10. Missing Input Validation on MFA Secret
**Location:** `backend/routes/auth.js` - MFA setup
**Severity:** MEDIUM

**Issue:** The MFA secret is stored in plaintext in the database and returned to the client:
```javascript
res.json({
    secret: secret.base32, // Exposed!
    ...
});
```

**Fix:** Don't return the secret - only return the QR code.

---

### 11. Race Condition on Token Refresh
**Location:** `backend/routes/auth.js` - `/refresh` endpoint
**Severity:** HIGH

**Issue:** Token refresh is not atomic - old token is revoked after verification, allowing replay attacks if parallel requests are made.

**Fix:** Implement token family detection or use Redis for atomic operations.

---

### 12. CSRF Token Not Rotated After Login
**Location:** `backend/middleware/auth.js`
**Severity:** MEDIUM

**Issue:** CSRF token is generated once and lasts 24 hours. Should rotate after login/logout.

---

### 13. Missing Account Enumeration Protection
**Location:** `backend/routes/auth.js` - Login
**Severity:** MEDIUM

**Issue:** Different error timing for "user not found" vs "wrong password" could allow enumeration.

**Current:**
```javascript
if (!user) {
    return res.status(401).json({ error: 'Invalid credentials' });
}
```

This is actually correct - generic error message. ✓

---

### 14. No Max Password Length
**Location:** Registration
**Severity:** LOW

**Issue:** No maximum password length could allow DoS via very long passwords (hashing is CPU intensive).

**Fix:** Enforce max password length (e.g., 128 characters).

---

### 15. Device Fingerprint Too Weak
**Location:** `backend/utils/crypto.js`
**Severity:** MEDIUM

**Issue:** Device fingerprint is hash of easily spoofed values:
```javascript
const data = [
    req.headers['user-agent'] || '',
    req.headers['accept-language'] || '',
    req.headers['accept-encoding'] || '',
    req.ip
].join('|');
```

**Fix:** Add more entropy or don't rely on it for security decisions.

---

## 🔧 IMMEDIATE FIXES NEEDED

### Patch 1: Fix JWT Verification
```javascript
// backend/utils/tokens.js
function verifyAccessToken(token) {
    try {
        return jwt.verify(token, process.env.JWT_ACCESS_SECRET, {
            algorithms: ['HS256'],  // Explicitly allow only HS256
            complete: false
        });
    } catch (err) {
        return null;
    }
}
```

### Patch 2: Add Rate Limiting to Token Refresh
```javascript
// backend/routes/auth.js
const { refreshLimiter } = require('../middleware/rateLimit');

router.post('/refresh', refreshLimiter, authenticateRefreshToken, async (req, res) => {
    // ... existing code
});
```

### Patch 3: Secure Setup Script
```javascript
// scripts/setup.js - generate strong secrets
const crypto = require('crypto');

function generateSecret() {
    return crypto.randomBytes(64).toString('base64');
}

JWT_ACCESS_SECRET=${generateSecret()}
JWT_REFRESH_SECRET=${generateSecret()}
BCRYPT_PEPPER=${generateSecret()}
```

### Patch 4: Add Security Headers Middleware
```javascript
// backend/middleware/security.js
function securityHeaders(req, res, next) {
    res.setHeader('X-Frame-Options', 'DENY');
    res.setHeader('X-Content-Type-Options', 'nosniff');
    res.setHeader('Referrer-Policy', 'strict-origin-when-cross-origin');
    res.setHeader('Permissions-Policy', 'geolocation=(), microphone=(), camera=()');
    next();
}
```

### Patch 5: Fix Race Condition in Token Refresh
```javascript
// Use Redis or database transaction for atomicity
async function refreshTokenAtomic(oldToken, newTokenData) {
    return db.transaction(async (trx) => {
        // Verify old token still valid
        const session = await trx.get('SELECT * FROM sessions WHERE refresh_token = ? AND revoked_at IS NULL', [oldToken]);
        if (!session) throw new Error('Token already used');
        
        // Revoke old token
        await trx.run('UPDATE sessions SET revoked_at = CURRENT_TIMESTAMP WHERE id = ?', [session.id]);
        
        // Create new token
        await trx.run('INSERT INTO sessions (...) VALUES (...)', [...]);
    });
}
```

### Patch 6: Don't Expose MFA Secret
```javascript
// backend/routes/auth.js
res.json({
    // secret: secret.base32,  // REMOVE THIS LINE
    qrCode: qrCodeUrl,
    manualEntryKey: secret.base32.slice(0, 4) + '****' // Show partial only
});
```

### Patch 7: Add Max Password Length
```javascript
// backend/routes/auth.js
body('password')
    .isLength({ min: 8, max: 128 })  // Add max length
    .withMessage('Password must be between 8 and 128 characters')
```

---

## 📋 RECOMMENDED HARDENING

1. **Implement HSTS** with preload
2. **Add request signing** for sensitive operations
3. **Implement account lockout** notifications via email
4. **Add CAPTCHA** after 3 failed attempts
5. **Implement device confirmation** emails for new devices
6. **Add WebAuthn/FIDO2** for passwordless authentication
7. **Implement signed audit logs**
8. **Add database encryption at rest**
9. **Implement backup MFA codes**
10. **Add session timeout warnings**

---

## ✅ VERIFICATION CHECKLIST

- [ ] JWT algorithm explicitly set to HS256 only
- [ ] All rate limiters tested and working
- [ ] Security headers present on all responses
- [ ] MFA secret not exposed in API responses
- [ ] Password length limited (8-128 chars)
- [ ] CORS origin validation strict
- [ ] Error messages don't leak internals
- [ ] CSRF tokens rotate on auth events
- [ ] Database connections use SSL
- [ ] Secrets are 256+ bits and random

---

**Next Steps:** Implement patches in priority order (Critical → High → Medium → Low)