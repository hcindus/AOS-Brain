# PSD Appointments Authentication Flow Documentation

## Overview

This document describes the authentication system for PSD Appointments, integrating both Web and Mobile (Android) platforms with the existing Sentinel-Dusty Auth Service.

## Architecture

```
┌─────────────────────┐         ┌─────────────────────┐         ┌─────────────────────┐
│   Web Login (HTML)  │         │  Android Login (KT) │         │   Sentinel-Dusty    │
│   /appointments/web │──────────│      (Compose)      │──────────│   Auth Service      │
│                     │         │                     │         │      :3000          │
└─────────────────────┘         └─────────────────────┘         └─────────────────────┘
         │                                   │                            │
         ▼                                   ▼                            ▼
┌─────────────────────┐         ┌─────────────────────┐         ┌─────────────────────┐
│   auth.js (JWT)     │         │  AuthRepository     │         │   PostgreSQL DB     │
│   auth.css (PSD)    │         │  EncryptedSharedPref│         │   Argon2id Hashing  │
└─────────────────────┘         └─────────────────────┘         └─────────────────────┘
```

## Brand Colors

- **Primary Dark**: `#0a0a1a` - Background
- **Cyan Accent**: `#00E0FF` - Primary buttons, links, focus states
- **Orange Accent**: `#FF7A00` - Logo, highlights

---

## Web Authentication

### Files Created

1. **login.html** - Email/password login form
2. **register.html** - Multi-step account creation
3. **forgot-password.html** - Password reset request
4. **reset-password.html** - New password confirmation
5. **assets/auth.css** - PSD-branded styles
6. **assets/auth.js** - JWT handling and API integration

### Flow

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Login     │────▶│  Validate   │────▶│  Sentinel   │────▶│  Dashboard  │
│    Page     │     │   Input     │     │   Auth      │     │  (on success)│
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
                          │
                          ▼
                    ┌─────────────┐
                    │   MFA       │────▶ Enter Code ───▶ Success
                    │  Required   │
                    └─────────────┘
```

### Key Features

- **Remember Me**: Tokens stored in localStorage or sessionStorage
- **Form Validation**: Real-time email format and password strength checks
- **Password Breach Check**: Integration with HaveIBeenPwned API
- **CSRF Protection**: Token-based request validation
- **Device Fingerprinting**: For security tracking

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/auth/login` | POST | Authenticate user |
| `/api/auth/register` | POST | Create new account |
| `/api/auth/refresh` | POST | Refresh access token |
| `/api/auth/logout` | POST | Invalidate session |
| `/api/auth/password-reset/request` | POST | Request password reset |
| `/api/auth/password-reset/verify` | POST | Verify reset token |
| `/api/auth/password-reset/confirm` | POST | Confirm new password |
| `/api/auth/mfa/verify` | POST | Verify MFA code |

---

## Mobile (Android) Authentication

### Files Created

1. **LoginScreen.kt** - Main login with biometric support
2. **RegisterScreen.kt** - Multi-step registration
3. **ForgotPasswordScreen.kt** - Password reset flow
4. **LoginViewModel.kt** - Login state management
5. **RegisterViewModel.kt** - Registration state management
6. **ForgotPasswordViewModel.kt** - Password reset logic
7. **AuthRepository.kt** - Data layer for auth operations
8. **AuthApi.kt** - Retrofit API interface
9. **AuthModels.kt** - Data classes for API requests/responses
10. **SecurePreferences.kt** - EncryptedSharedPreferences wrapper
11. **Color.kt** - PSD brand colors

### Flow

```
┌─────────────────────┐
│   LoginScreen       │
│   ├─ Email/Password │
│   ├─ Remember Me    │
│   └─ Biometric Auth │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐     ┌─────────────────────┐
│  AuthRepository     │────▶│   Sentinel-Dusty  │
│  ├─ Encrypted Prefs │     │   Auth Service      │
│  └─ Token Refresh   │     │      :3000          │
└─────────┬───────────┘     └─────────────────────┘
          │
          ▼
┌─────────────────────┐
│   RegisterScreen    │
│   Step 1: Account   │
│   Step 2: Company   │
└─────────────────────┘
```

### Key Features

- **Biometric Authentication**: Fingerprint/Face ID support via Android BiometricPrompt
- **Encrypted Token Storage**: AndroidX Security library with AES-256
- **Remember Me**: Secure credential storage for biometric login
- **Session Management**: Automatic token refresh before expiry
- **Offline Awareness**: Graceful handling of network issues

### Dependencies

```groovy
// In build.gradle (app level)
dependencies {
    implementation "androidx.security:security-crypto:1.1.0-alpha06"
    implementation "androidx.biometric:biometric:1.2.0-alpha05"
    implementation "androidx.lifecycle:lifecycle-viewmodel-compose:2.7.0"
    implementation "com.google.dagger:hilt-android:2.50"
    kapt "com.google.dagger:hilt-compiler:2.50"
    implementation "com.squareup.retrofit2:retrofit:2.9.0"
    implementation "com.squareup.retrofit2:converter-gson:2.9.0"
}
```

---

## Security Features

### Password Requirements

- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one number
- At least one special character
- Checked against HaveIBeenPwned breach database

### Token Management

| Token Type | Storage | Expiry | Usage |
|------------|---------|--------|-------|
| Access Token | EncryptedSharedPreferences (Android) / localStorage (Web) | 15 min | API requests |
| Refresh Token | EncryptedSharedPreferences (Android) / httpOnly cookie (Web) | 7 days | Token refresh |
| CSRF Token | Memory only | Session | Form submission |

### Session Security

- Automatic token refresh before expiry (5 min buffer)
- Device fingerprint tracking
- Failed attempt lockout (5 attempts = 15 min lock)
- Session timeout after 30 min inactivity

---

## Error Handling

### Common Error Codes

| Code | Meaning | User Message |
|------|---------|--------------|
| 400 | Bad Request | "Please check your input and try again" |
| 401 | Unauthorized | "Invalid email or password" |
| 403 | Forbidden | "Account locked. Please try again later." |
| 409 | Conflict | "Email already registered" |
| 429 | Rate Limited | "Too many attempts. Please wait." |
| 500 | Server Error | "Something went wrong. Please try again." |

---

## Integration Checklist

### Web Setup

- [ ] Copy `/appointments/web/` files to your web server
- [ ] Update `API_BASE` in `auth.js` if needed
- [ ] Configure CORS on Sentinel-Dusty for web domain
- [ ] Test all flows end-to-end

### Android Setup

- [ ] Add dependencies to `build.gradle`
- [ ] Apply Hilt plugin and annotation
- [ ] Implement `NetworkModule` for Retrofit/DI
- [ ] Add `INTERNET` and `USE_BIOMETRIC` permissions
- [ ] Test on physical device with biometric

---

## File Structure

```
/root/.openclaw/workspace/appointments/
├── web/
│   ├── login.html
│   ├── register.html
│   ├── forgot-password.html
│   ├── reset-password.html
│   └── assets/
│       ├── auth.css
│       └── auth.js
└── android/
    └── app/src/main/java/com/psdepot/appointments/
        ├── data/
        │   ├── remote/
        │   │   ├── api/
        │   │   │   └── AuthApi.kt
        │   │   └── model/
        │   │       └── AuthModels.kt
        │   └── repository/
        │       └── AuthRepository.kt
        ├── ui/
        │   ├── screens/
        │   │   ├── LoginScreen.kt
        │   │   ├── RegisterScreen.kt
        │   │   └── ForgotPasswordScreen.kt
        │   ├── viewmodel/
        │   │   ├── LoginViewModel.kt
        │   │   ├── RegisterViewModel.kt
        │   │   └── ForgotPasswordViewModel.kt
        │   └── theme/
        │       └── Color.kt
        └── utils/
            └── SecurePreferences.kt
```

---

## Testing

### Web Manual Tests

1. ✓ Login with valid credentials
2. ✓ Login with invalid credentials
3. ✓ Registration with company details
4. ✓ Password reset flow
5. ✓ Remember me functionality
6. ✓ Session timeout
7. ✓ Token refresh

### Android Manual Tests

1. ✓ Login with valid credentials
2. ✓ Biometric authentication
3. ✓ Registration multi-step form
4. ✓ Password reset
5. ✓ Offline error handling
6. ✓ Token persistence across app restarts
7. ✓ Background/foreground session handling

---

## Support

For issues or questions:
- Sentinel-Dusty Auth: `localhost:3000`
- Web files: `/appointments/web/`
- Android source: `/appointments/android/`
- Auth Service README: `/root/.openclaw/workspace/auth-system/SENTINEL-DUSTY-README.md`