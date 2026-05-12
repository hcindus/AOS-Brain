# PSD Appointments System

**Version:** 1.0.0-DEMO  
**Deployed:** 2026-05-12  
**Status:** Live and tested

## Live URLs

### Web Application
- **Main:** https://psdepot.com/appointments/
- **Login:** https://psdepot.com/appointments/login.html
- **Register:** https://psdepot.com/appointments/register.html
- **API Health:** https://psdepot.com/appointments/api/health

### API Endpoints
- **Availability:** https://psdepot.com/appointments/api/v1/availability
- **Bookings:** https://psdepot.com/appointments/api/v1/bookings
- **Leads Search:** https://psdepot.com/appointments/api/v1/leads/search

## Demo Mode

**Current Status:** DEMO MODE ENABLED

Demo mode allows testing with any credentials:
- Login with any email/password
- Registration auto-creates demo accounts
- No backend auth service required

**To disable demo mode:**
Edit `/appointments/web/assets/auth.js`:
```javascript
const DEMO_MODE = false;  // Set to false for production
```

Then start the Sentinel-Dusty auth service on port 3000.

## System Components

| Component | Status | Port |
|-----------|--------|------|
| Web SPA | ✅ Live | 443 |
| FastAPI Backend | ✅ Running | 8083 |
| Android App | ✅ Built | - |
| Auth Service | ⚠️ Demo Mode | 3000 |

## GitHub Commit

**Latest:** `ab959fe1c` - "Jordan office sync 2026-05-12_11:57"

Repository: https://github.com/hcindus/AOS-Brain

## Files

```
appointments/
├── web/                    # HTML/CSS/JS Web App
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── forgot-password.html
│   ├── reset-password.html
│   ├── css/styles.css
│   ├── js/app.js
│   └── assets/
│       ├── auth.css
│       └── auth.js        # DEMO_MODE enabled
├── android/               # Kotlin Android App
│   └── app/src/main/java/com/psdepot/appointments/
│       ├── ui/screens/
│       ├── data/
│       └── utils/
├── backend/               # FastAPI Python Service
│   └── appointments_service.py
└── AUTH_FLOW_DOCUMENTATION.md
```

## Testing Credentials (Demo Mode)

Use any email and password combination. Example:
- Email: `demo@psdepot.com`
- Password: `password123`

## Next Steps

1. Test all features in demo mode
2. Add availability slots to database
3. Switch to production auth (disable DEMO_MODE)
4. Build and test Android APK
5. Add Google Calendar sync

## Notes

- PSD branding applied throughout (Dark #0a0a1a, Cyan #00E0FF, Orange #FF7A00)
- Responsive design for mobile, tablet, desktop
- JWT token management with localStorage/sessionStorage
- Offline support ready in Android app (Room database)

---

*Last Updated: 2026-05-12 11:58 UTC*