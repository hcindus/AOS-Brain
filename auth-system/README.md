# Secure Authentication System v1.0

Production-ready authentication with NIST/OWASP compliance.

## Features

- ✅ **Argon2id** password hashing (memory-hard, GPU-resistant)
- ✅ **JWT** session management with refresh tokens
- ✅ **TOTP MFA** (Google Authenticator, Authy compatible)
- ✅ **Rate limiting** (Redis-backed, distributed)
- ✅ **Breach detection** (Have I Been Pwned integration)
- ✅ **Secure password reset** (time-limited signed tokens)
- ✅ **CSRF protection** (double-submit cookie pattern)
- ✅ **Device fingerprinting** (risk-based auth)
- ✅ **Audit logging** (all auth events)

## Quick Start

```bash
npm install
npm run setup
npm run dev
```

## Architecture

```
auth-system/
├── backend/           # Express.js API
│   ├── middleware/    # Auth, rate limiting, validation
│   ├── models/        # User, Session, AuditLog
│   ├── routes/        # Auth endpoints
│   └── utils/         # Crypto, tokens, breach check
├── frontend/          # Vanilla JS components
│   ├── components/    # Login, Register, MFA forms
│   └── assets/        # CSS, icons
└── database/          # Schema + migrations
```

## Security Checklist

- [ ] HTTPS only (HSTS enabled)
- [ ] Secure cookie flags (httpOnly, secure, sameSite)
- [ ] Rate limiting per IP + username
- [ ] Password breach checking on registration
- [ ] MFA required for admin accounts
- [ ] Session timeout after 15min idle
- [ ] Audit logs to secure storage

## Deployment

See `DEPLOY.md` for production setup.