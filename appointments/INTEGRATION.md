# PSD Appointments System - Architecture & Security Integration

## Overview

A standalone appointment booking system for Performance Supply Depot, integrating with:
- **DepotChaos CRM** (read-only lead access)
- **Sentinel-Dusty Auth** (our existing security infrastructure)
- **Google Calendar** (for sync)
- **Android App** (primary client)

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIENT LAYER                              │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │  Android App │  │   Web UI     │  │   DepotChaos Web     │  │
│  │  (Primary)   │  │  (Fallback)  │  │   (embedded view)    │  │
│  └──────┬───────┘  └──────┬───────┘  └──────────┬───────────┘  │
└─────────┼─────────────────┼─────────────────────┼───────────────┘
          │                 │                     │
          └─────────────────┼─────────────────────┘
                            │ HTTPS/REST
┌───────────────────────────▼─────────────────────────────────────┐
│                    API GATEWAY (Nginx)                         │
│              Routes /appointments/* to Port 8083               │
└───────────────────────────┬─────────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────────┐
│           APPOINTMENT SERVICE (FastAPI, Port 8083)              │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │  Booking API │  │ Availability │  │   Sync Worker      │  │
│  │              │  │   Manager    │  │   (Google Cal)       │  │
│  └──────┬───────┘  └──────┬───────┘  └──────────┬───────────┘  │
│         │                │                     │                │
└─────────┼────────────────┼─────────────────────┼────────────────┘
          │                │                     │
┌─────────▼────────────────┼─────────────────────┼────────────────┐
│     appointments.db      │                     │                  │
│  ┌──────────────────┐    │                     │                  │
│  │ appointments     │    │                     │                  │
│  │ availability     │    │                     │                  │
│  │ sync_queue       │    │                     │                  │
│  │ mobile_sessions  │    │                     │                  │
│  └──────────────────┘    │                     │                  │
│                          │                     │                  │
│  ┌──────────────────┐    │                     │                  │
│  │ Google API       │◄───┘                     │                  │
│  │ (OAuth2)       │                          │                  │
│  └──────────────────┘                          │                  │
└───────────────────────────────────────────────┼────────────────────┘
                                                │
┌───────────────────────────────────────────────▼────────────────────┐
│                    AUTHENTICATION LAYER                           │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              Sentinel-Dusty Auth Service                 │   │
│  │                  (Port 3000)                             │   │
│  │                                                          │   │
│  │  • JWT Access Tokens (15 min expiry)                     │   │
│  │  • Refresh Tokens (7 days)                               │   │
│  │  • 2FA/MFA Support                                       │   │
│  │  • Device Fingerprinting                                 │   │
│  │  • Password Breach Checking                              │   │
│  │  • Rate Limiting                                         │   │
│  │  • CSRF Protection                                       │   │
│  │  • Audit Logging                                         │   │
│  └──────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────┘
          │
          │ Token Verification
          ▼
┌─────────────────────────────────────────────────────────────────┐
│                    DATA LAYER                                    │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────────┐  ┌──────────────────────────────────────┐ │
│  │  appointments.db │  │         DepotChaos (Port 8082)       │ │
│  │  (Read/Write)    │  │                                      │ │
│  └──────────────────┘  │  ┌──────────────────────────────┐   │ │
│                        │  │ unified.db (Read-Only)       │   │ │
│                        │  │  • leads                     │   │ │
│                        │  │  • vendors                   │   │ │
│                        │  └──────────────────────────────┘   │ │
│                        └──────────────────────────────────────┘ │
└───────────────────────────────────────────────────────────────────┘
```

## Security Integration

### Authentication Flow

```
1. Android App → Sentinel-Dusty Auth Service (Port 3000)
   POST /api/auth/login
   { email, password, deviceFingerprint }

2. Sentinel-Dusty validates:
   - Credentials (Argon2id)
   - 2FA/MFA code (if enabled)
   - Device fingerprint
   - Rate limits

3. Returns:
   { accessToken, refreshToken, expiresIn }

4. Android App stores tokens in EncryptedSharedPreferences

5. Subsequent API calls:
   Authorization: Bearer <accessToken>
   → Appointment Service (8083) verifies with Auth Service
   → Or validates JWT signature locally (if asymmetric keys)
```

### Security Features Inherited from Sentinel-Dusty

| Feature | Implementation | Status |
|---------|---------------|--------|
| **JWT Tokens** | RS256 asymmetric signing | ✅ Used |
| **Token Expiry** | 15 min access, 7 day refresh | ✅ Used |
| **2FA/TOTP** | speakeasy library | ✅ Supported |
| **Device Fingerprinting** | SHA-256 hash of device props | ✅ Used |
| **Password Breach Check** | HaveIBeenPwned API | ✅ Supported |
| **Rate Limiting** | Redis-backed (express-rate-limit) | ✅ Supported |
| **CSRF Protection** | Double-submit cookie pattern | ✅ Used |
| **Argon2id** | Password hashing | ✅ Used |
| **Audit Logging** | All auth events logged | ✅ Supported |

### Android App Security

```kotlin
// Token storage in Android
EncryptedSharedPreferences.create(
    "auth_prefs",
    MasterKey.Builder(context)
        .setKeyScheme(MasterKey.KeyScheme.AES256_GCM)
        .build(),
    context,
    EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
    EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM
)

// Biometric authentication option
BiometricPrompt.authenticate(
    BiometricPrompt.PromptInfo.Builder()
        .setTitle("Confirm appointment action")
        .setAllowedAuthenticators(BIOMETRIC_STRONG)
        .build()
)
```

## API Endpoints

### Authentication
All endpoints require Bearer token except `/health`.

```http
GET /health
Authorization: None
Response: { "status": "healthy", "version": "1.0.0" }

GET /api/v1/availability?date=2024-05-15&days=7
Authorization: Bearer <token>

POST /api/v1/bookings
Authorization: Bearer <token>
Body: {
    "customer_name": "John Doe",
    "customer_email": "john@example.com",
    "customer_phone": "555-1234",
    "service_type": "consultation",
    "scheduled_at": "2024-05-15T14:00:00Z",
    "duration_minutes": 60,
    "lead_id": 123  // Optional - link to DepotChaos lead
}

GET /api/v1/bookings?page=1&status=confirmed
Authorization: Bearer <token>

GET /api/v1/leads/search?q=abc
Authorization: Bearer <token>
// Returns leads from DepotChaos (read-only)
```

## Database Schema

See `database/schema.sql` for full schema.

Key tables:
- `appointments` - Core booking data
- `availability_slots` - Time slot management
- `sync_queue` - Async Google Calendar operations
- `mobile_sessions` - Android app session tracking

## Deployment

### 1. Start Appointment Service

```bash
cd /root/.openclaw/workspace/appointments/backend
python3 -m venv venv
source venv/bin/activate
pip install fastapi uvicorn httpx

# Initialize database
python3 -c "import appointments_service; appointments_service.init_database()"

# Start service
uvicorn appointments_service:app --host 0.0.0.0 --port 8083
```

### 2. Configure Nginx

```nginx
# /etc/nginx/sites-available/psdepot.com

location /appointments/ {
    proxy_pass http://localhost:8083/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
}
```

### 3. Android App Build

```bash
cd /root/.openclaw/workspace/appointments/android
./gradlew assembleRelease
```

### 4. Systemd Service

```ini
# /etc/systemd/system/psd-appointments.service
[Unit]
Description=PSD Appointment Service
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/.openclaw/workspace/appointments/backend
ExecStart=/root/.openclaw/workspace/appointments/backend/venv/bin/uvicorn appointments_service:app --host 0.0.0.0 --port 8083
Restart=always

[Install]
WantedBy=multi-user.target
```

## Environment Variables

```bash
# /root/.openclaw/workspace/appointments/.env

# Auth Service
AUTH_SERVICE_URL=http://localhost:3000
JWT_PUBLIC_KEY_PATH=/root/.openclaw/workspace/auth-system/keys/jwt-public.pem

# Google Calendar
GOOGLE_CLIENT_ID=your-client-id
GOOGLE_CLIENT_SECRET=your-client-secret
GOOGLE_REDIRECT_URI=https://psdepot.com/appointments/auth/callback

# Database
APPOINTMENTS_DB_PATH=/root/.openclaw/workspace/appointments/data/appointments.db
DEPOT_CHAOS_DB_PATH=/root/.openclaw/workspace/data/depot_chaos/unified.db

# Notifications
FCM_SERVER_KEY=your-firebase-key
```

## Monitoring

- Service health: `GET /health`
- Sync queue status: Check `sync_queue` table for pending items
- Auth failures: Monitor Sentinel-Dusty audit logs
- Database size: Track `appointments.db` growth

## Development Roadmap

### Phase 1 (MVP)
- [x] Backend service scaffold
- [x] Database schema
- [x] Android app structure
- [ ] Basic booking CRUD
- [ ] Availability slot management
- [ ] Sentinel-Dusty auth integration

### Phase 2
- [ ] Google Calendar sync
- [ ] Push notifications (FCM)
- [ ] Offline mode (Room caching)
- [ ] Biometric auth

### Phase 3
- [ ] Web UI
- [ ] DepotChaos dashboard widget
- [ ] Advanced reporting
- [ ] Multi-user support

## Security Checklist

- [ ] JWT tokens validated on every request
- [ ] HTTPS-only in production
- [ ] SQL injection prevention (parameterized queries)
- [ ] XSS protection (output encoding)
- [ ] Rate limiting on all endpoints
- [ ] Secure token storage (Android Keystore)
- [ ] Certificate pinning in Android app
- [ ] ProGuard/R8 obfuscation in release builds
