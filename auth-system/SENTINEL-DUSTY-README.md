# 🛡️ Sentinel-Dusty Fusion

**Autonomous Security Monitoring Agent** for the Auth System

## Overview

Sentinel-Dusty Fusion combines **Dusty's cross-chain asset scanning capabilities** with **Sentinel's security monitoring patterns** to create an intelligent, autonomous security guardian for your authentication system.

```
┌─────────────────────────────────────────────────────────────┐
│                    SENTINEL-DUSTY FUSION                    │
├─────────────────────────────────────────────────────────────┤
│  🧠 Dusty Intelligence Layer  │  🛡️ Sentinel Defense Layer │
│  ───────────────────────────  │  ───────────────────────── │
│  • Asset scanning patterns    │  • Threat detection rules    │
│  • Cross-vector correlation   │  • Automated response        │
│  • Consolidation algorithms   │  • Real-time alerting        │
│  • Predictive analytics       │  • Incident containment      │
└─────────────────────────────────────────────────────────────┘
                         │
         ┌───────────────┴───────────────┐
         ▼                               ▼
   🔄 Continuous Scanning          🎯 Threat Response
   ⏱️  30-second intervals         ⚡ Auto-block/alert
```

## Capabilities

### 🔍 Threat Detection (Dusty-Style Scanning)

| Scan Type | Description | Response |
|-----------|-------------|----------|
| **Brute Force Scan** | Detects repeated failed logins | Auto-block IP after 5 attempts |
| **Token Replay Scan** | Detects refresh token replay attacks | Revoke all user sessions |
| **Geographic Scan** | Identifies impossible travel | Alert + force MFA re-auth |
| **Rate Limit Scan** | Monitors rate limit violations | Throttle + alert |
| **DB Integrity Scan** | Checks for orphaned sessions | Auto-cleanup + report |
| **Real-time Event Watch** | Live monitoring of auth events | Instant pattern matching |

### 🎯 Automated Response (Sentinel Defense)

```
Threat Severity → Response
─────────────────────────────────────
🔴 CRITICAL    → Auto-block IP + revoke sessions + immediate alert
🟠 HIGH        → Alert security team + log incident
🟡 MEDIUM      → Monitor + notify user
🟢 LOW         → Log only
```

## Installation

```bash
# Already integrated into auth-system
npm install

# Start server (initializes guardian automatically)
npm run dev
```

## Usage

### Check Security Status

```bash
curl http://localhost:3000/api/security/status
```

Response:
```json
{
  "timestamp": "2026-05-08T04:00:00.000Z",
  "status": "ACTIVE",
  "threatsDetected": 0,
  "threatBreakdown": {
    "CRITICAL": 0,
    "HIGH": 0,
    "MEDIUM": 0,
    "LOW": 0
  },
  "recentThreats": [],
  "recommendations": [
    "System security posture is healthy"
  ]
}
```

### Run as Standalone Guardian

```bash
node sentinel-dusty-fusion.js
```

## Architecture

### Continuous Scanning (Like Dusty)

```javascript
// Every 30 seconds:
performSecurityScan()
  ├─ scanFailedLogins()      // Brute force detection
  ├─ scanSuspiciousTokens()  // Replay attack detection
  ├─ scanGeoAnomalies()      // Impossible travel
  ├─ scanRateViolations()    // Rate limit abuse
  └─ scanDBIntegrity()       // Database health
```

### Real-time Event Watching

```javascript
// Every 5 seconds:
watchRealTimeEvents()
  └─ processRealTimeEvent()
       └─ Pattern matching against threat signatures
```

### Threat Consolidation (Dusty's Asset Consolidation Pattern)

```javascript
// Multiple similar threats → Single consolidated threat
[
  { type: 'BRUTE_FORCE', ip: '1.2.3.4', count: 3 },
  { type: 'BRUTE_FORCE', ip: '1.2.3.4', count: 4 },
  { type: 'BRUTE_FORCE', ip: '1.2.3.4', count: 5 }
]
↓
{
  type: 'BRUTE_FORCE',
  ip: '1.2.3.4',
  count: 12,           // Consolidated count
  occurrences: 3,      // Number of raw events
  severity: 'CRITICAL'
}
```

## Threat Patterns

| Pattern | Detection Method | Threshold | Severity |
|---------|-----------------|-----------|----------|
| `bruteForce` | Failed login count | 5/5min | HIGH |
| `credentialStuffing` | Multiple IPs, same user | 10/10min | CRITICAL |
| `tokenReplay` | Invalid refresh token use | 3/5min | CRITICAL |
| `suspiciousLocation` | New IP/device | 1/1min | MEDIUM |
| `mfaBypass` | Failed MFA attempts | 3/5min | HIGH |
| `accountEnumeration` | User not found rate | 20/10min | MEDIUM |
| `privilegeEscalation` | Mass assignment attempt | 1/1min | CRITICAL |
| `dataExfiltration` | Bulk export attempts | 5/5min | HIGH |

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/security/status` | GET | Get security status report |
| `/api/health` | GET | System health check |

## Integration with Auth System

The guardian automatically:

1. ✅ Initializes on server start
2. ✅ Scans every 30 seconds
3. ✅ Watches real-time events every 5 seconds
4. ✅ Auto-responds to threats
5. ✅ Logs all security events
6. ✅ Provides status endpoint

## Configuration

```bash
# .env
GUARDIAN_SCAN_INTERVAL=30000      # 30 seconds
GUARDIAN_THREAT_THRESHOLD=5       # Alert after 5 events
GUARDIAN_AUTO_BLOCK=true          # Auto-block critical threats
GUARDIAN_ALERT_EMAIL=security@yourdomain.com
```

## Monitoring Dashboard

Future enhancement: WebSocket-based real-time threat dashboard

```
┌─────────────────────────────────────┐
│  SENTINEL-DUSTY FUSION DASHBOARD    │
├─────────────────────────────────────┤
│  🟢 System: HEALTHY                 │
│  🔒 Active Threats: 0               │
│  ⏱️  Last Scan: 2s ago             │
│                                     │
│  📊 THREAT BREAKDOWN                │
│  ├─ CRITICAL: 0                    │
│  ├─ HIGH: 0                        │
│  ├─ MEDIUM: 0                      │
│  └─ LOW: 0                         │
└─────────────────────────────────────┘
```

## Credits

- **Dusty**: Cross-chain crypto wallet intelligence
- **Sentinel**: Security monitoring and response patterns
- **Fusion**: Combined autonomous security guardian

---

*Part of the AGI Company Auth System*