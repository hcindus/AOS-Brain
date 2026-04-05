# TASK: CREAM Mobile Apps — Assigned to Software Team
**Created:** 2026-03-16 16:57 UTC  
**Assigned to:** Spindle (CTO), Pipeline (Backend), TapTap (Mobile), BugCatcher (QA)  
**Priority:** HIGH  
**Source:** Captain's request  
**Review by:** Captain upon completion

---

## Overview
Build CREAM (Capitalize Real Estate Asset Management) for mobile — **both Android and iOS**. This is a comprehensive real estate CRM, planning, and transaction management platform. Existing web/DroidScript version exists; this is native mobile build.

---

## Decision: React Native (Recommended)

**Approach:** React Native (single codebase → Android + iOS)

**Why:**
- 60-70% code reuse between platforms
- Faster development (2x vs native)
- One team, one codebase
- Good performance for this use case
- Easy maintenance

**Alternative:** Native (Kotlin + Swift) if React Native proves limiting

---

## Team Assignment

| Role | Assignee | Responsibility |
|------|----------|----------------|
| **Project Lead** | Spindle (CTO) | Architecture, React Native setup, review |
| **Backend** | Pipeline | API, database, AI Lead Scoring, sync |
| **Mobile Dev** | TapTap | React Native UI, mobile features, builds |
| **QA** | BugCatcher | Testing, device testing, release validation |

---

## Existing CREAM Features to Port

### Core Modules
1. **Plan Business**
   - Business goal setting
   - Milestone tracking
   - Coaching prompts

2. **Lead & Database Management**
   - Lead import/capture
   - Contact management
   - Database segmentation

3. **Appointment Tracker**
   - Calendar integration
   - "Did you land it?" follow-up prompts
   - Meeting notes

4. **Letter Generator**
   - Template library
   - Custom letter creation
   - Print/email integration

5. **Revenue & Profit Tracking**
   - Transaction logging
   - P&L statements
   - Cash flow analysis

6. **Community Farming**
   - Geographic farming
   - Neighbor tracking
   - Campaign management

7. **Website/Landing Page Portal**
   - Site management
   - Lead capture forms
   - Analytics

8. **Premium Tools**
   - **AI Lead Scoring** (Pipeline API)
   - **Tax Export** (IRS Schedule E format)
   - Advanced analytics

### Pricing Integration
- **Initial:** $699.00 (one-time)
- **Annual Update:** $99.00
- In-app purchase handling (Apple/Google)

---

## Technical Architecture

### Frontend (React Native)
```
cream-mobile/
├── src/
│   ├── components/          # Reusable UI components
│   ├── screens/             # App screens (by module)
│   │   ├── auth/
│   │   ├── dashboard/
│   │   ├── leads/
│   │   ├── appointments/
│   │   ├── transactions/
│   │   ├── planning/
│   │   ├── letters/
│   │   ├── community/
│   │   ├── websites/
│   │   └── premium/
│   ├── navigation/          # React Navigation
│   ├── state/               # Redux Toolkit / Zustand
│   ├── api/                 # API client (Axios)
│   ├── utils/               # Helpers
│   ├── constants/           # Config, colors, fonts
│   └── types/               # TypeScript types
├── ios/                     # iOS-specific config
├── android/                 # Android-specific config
├── assets/                  # Images, fonts
├── __tests__/               # Test files
├── App.tsx                  # Entry point
├── index.js
├── package.json
├── tsconfig.json
└── README.md
```

### Dependencies
```json
{
  "react-native": "~0.72.0",
  "react-navigation": "~6.x",
  "react-redux": "~8.x",
  "redux-toolkit": "~1.9.x",
  "axios": "~1.5.x",
  "react-native-reanimated": "~3.x",
  "react-native-gesture-handler": "~2.x",
  "react-native-chart-kit": "~6.x",
  "react-native-calendars": "~1.x",
  "@react-native-async-storage": "~1.x",
  "react-native-biometrics": "~3.x",
  "react-native-print": "~0.x"
}
```

### Backend API (Pipeline)

#### Authentication
```
POST /auth/login
POST /auth/register
POST /auth/refresh
POST /auth/logout
```

#### Core Endpoints
```
# Dashboard
GET  /dashboard/stats

# Leads
GET    /leads
POST   /leads
PUT    /leads/{id}
DELETE /leads/{id}
POST   /leads/{id}/score      # AI Lead Scoring

# Appointments
GET    /appointments
POST   /appointments
PUT    /appointments/{id}
DELETE /appointments/{id}

# Transactions
GET    /transactions
POST   /transactions
PUT    /transactions/{id}
GET    /transactions/pnl

# Planning
GET    /plans
POST   /plans
PUT    /plans/{id}/milestones

# Community Farming
GET    /farming/zones
POST   /farming/campaigns
GET    /farming/analytics

# Letters
GET    /letters/templates
POST   /letters/generate
GET    /letters/{id}/download

# Premium
GET    /premium/lead-score/{lead_id}
GET    /premium/tax-export
```

#### AI Lead Scoring (Pipeline)
```python
# Model integration
POST /api/v1/ai/lead-score
Body: { lead_data: {...} }
Response: { score: 85, factors: [...] }
```

#### Database
- PostgreSQL (users, leads, transactions)
- Redis (caching, sessions)
- S3 (documents, exports)

---

## Milestones

| Week | Deliverable | Owner |
|------|-------------|-------|
| 1 | Architecture + RN setup + auth | Spindle + TapTap |
| 2 | Dashboard + Leads module | TapTap |
| 3 | Appointments + Transactions | TapTap |
| 4 | Backend API + AI scoring | Pipeline |
| 5 | Planning + Community + Letters | TapTap |
| 6 | Premium tools + polish | TapTap |
| 7 | Testing + bug fixes | BugCatcher |
| 8 | App Store submission | Spindle |

---

## Deliverables Checklist

### Mobile App
- [ ] React Native project setup (Spindle)
- [ ] Navigation structure (TapTap)
- [ ] Authentication flow (TapTap)
- [ ] Dashboard screen (TapTap)
- [ ] Leads module (CRUD + AI scoring) (TapTap)
- [ ] Appointments module (TapTap)
- [ ] Transactions + P&L (TapTap)
- [ ] Planning module (TapTap)
- [ ] Community Farming (TapTap)
- [ ] Letter Generator (TapTap)
- [ ] Websites portal (TapTap)
- [ ] Premium tools (TapTap)
- [ ] In-app purchases (TapTap)

### Backend
- [ ] API server setup (Pipeline)
- [ ] Authentication service (Pipeline)
- [ ] Database schema (Pipeline)
- [ ] Leads API (Pipeline)
- [ ] AI Lead Scoring integration (Pipeline)
- [ ] Appointments API (Pipeline)
- [ ] Transactions API (Pipeline)
- [ ] Tax export service (Pipeline)
- [ ] Real-time sync (WebSocket) (Pipeline)

### Release
- [ ] Android APK built (TapTap)
- [ ] iOS IPA built (TapTap)
- [ ] Play Store submission (Spindle)
- [ ] App Store submission (Spindle)
- [ ] Documentation complete (Spindle)

---

## Acceptance Criteria

1. **Functional**
   - [ ] All 8 core modules working
   - [ ] AI Lead Scoring returns scores
   - [ ] Tax export generates valid Schedule E
   - [ ] In-app purchases process correctly
   - [ ] Sync works across devices

2. **Performance**
   - [ ] App launch < 3 seconds
   - [ ] Screen transitions < 300ms
   - [ ] API response < 1 second (cached)
   - [ ] Works offline (cached data)

3. **Platforms**
   - [ ] Android 8.0+ support
   - [ ] iOS 14+ support
   - [ ] Tablets supported (responsive)

4. **Store Requirements**
   - [ ] App Store guidelines met
   - [ ] Play Store guidelines met
   - [ ] Privacy policy linked
   - [ ] Terms of service linked

---

## Resources

### Existing Code
- DroidScript CREAM code exists in workspace
- Can reference logic, not copy UI

### Documentation
- CREAM_Documentation.md (existing)
- This task file

---

## Questions?

Contact Spindle for technical architecture or Captain for business requirements.

**Status:** 🟡 Awaiting kickoff  
**Approach:** React Native (confirm with Spindle)  
**Target:** Play Store + App Store submission in 8 weeks