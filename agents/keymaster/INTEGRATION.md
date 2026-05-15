<!--
VERSION: 1.0.0
UPDATED: 2026-05-15 18:31 UTC
CHANGELOG: Initial integration spec
-->

# INTEGRATION.md - Connection Points

_How The Key Master connects to the world._

## Overview

The Key Master does not operate in isolation. Every agent, every service, every system that requires authentication depends on the vault. This document defines the integration patterns.

## API Interface

### Endpoint: `/vault/request`
**Method:** POST
**Auth:** mTLS (service certificate)
**Purpose:** Request a secret by ID

**Request:**
```json
{
  "service_id": "knox-trading",
  "secret_id": "binance-api-prod",
  "reason": "Trading session 2026-05-15",
  "requester": "Knox"
}
```

**Response:**
```json
{
  "status": "granted",
  "secret": "[encrypted payload]",
  "expires": "2026-05-15T19:30:00Z",
  "audit_id": "req_20260515183000_knox"
}
```

### Endpoint: `/vault/rotate`
**Method:** POST
**Auth:** mTLS + Captain approval
**Purpose:** Trigger manual rotation

**Request:**
```json
{
  "secret_id": "api-key-xyz",
  "reason": "Suspected exposure",
  "urgency": "immediate",
  "requested_by": "Chelios"
}
```

### Endpoint: `/vault/status`
**Method:** GET
**Auth:** mTLS
**Purpose:** Health and rotation status

**Response:**
```json
{
  "vault_status": "healthy",
  "secrets_count": 47,
  "rotations_due": 3,
  "overdue_rotations": 0,
  "last_audit": "2026-05-15T00:00:00Z"
}
```

## Agent Integrations

### Knox (Trading Bot)
**Integration Type:** Automatic secret injection
**Pattern:**
- Knox requests Binance API credentials at session start
- Key Master provides time-bounded token (4 hours)
- Knox auto-renews before expiry
- On Knox shutdown, immediate revocation

**Rotation Schedule:**
- Binance API: 30 days (Critical)
- Wallet credentials: Hardware-backed, annual audit
- Strategy secrets: 60 days (High)

### Miles (Sales Agent)
**Integration Type:** On-demand retrieval
**Pattern:**
- Miles requests ElevenLabs TTS key per call
- Key Master logs each access with call context
- Usage limits enforced
- Monthly rotation

### Chelios (CISO)
**Integration Type:** Event-driven + Audit
**Pattern:**
- Chelios sends threat intel → Key Master preemptive rotation
- Key Master sends access logs → Chelios anomaly detection
- Joint incident response for Code BREACH

### Mission Control (AOS Brain)
**Integration Type:** Service account
**Pattern:**
- Brain service account for socket communication
- Certificate-based auth (mTLS)
- 90-day rotation
- Health check integration

### Minecraft Server
**Integration Type:** Credential store
**Pattern:**
- RCON password (180-day rotation)
- Server properties encryption
- Backup encryption keys

## External Service Integrations

### HashiCorp Vault (Backend)
**Status:** Recommended for production
**Purpose:** Enterprise-grade secret storage
**Integration:**
- Key Master as policy layer
- Vault as storage backend
- Automatic failover

### AWS Secrets Manager (Alternative)
**Status:** Available
**Purpose:** Cloud-native secret storage
**Integration:**
- Key Master as orchestration layer
- AWS as storage backend
- Cross-region replication

### Local Encrypted Storage (Current)
**Status:** Active
**Purpose:** Self-contained operation
**Implementation:**
- LUKS-encrypted volume
- AES-256-GCM for individual secrets
- Shamir's Secret Sharing for escrow

## Monitoring Integrations

### Prometheus Metrics
**Endpoint:** `/metrics`
**Metrics:**
- `vault_requests_total` - Total access requests
- `vault_rotation_duration_seconds` - Rotation latency
- `vault_secrets_overdue` - Secrets past rotation date
- `vault_compromise_alerts_total` - Security incidents

### AlertManager
**Alerts:**
- `VaultRotationOverdue` - Secret rotation past due
- `VaultAccessAnomaly` - Unusual access patterns
- `VaultCompromiseDetected` - Confirmed breach
- `VaultHealthCritical` - Vault infrastructure failure

### Log Aggregation
**Destination:** Centralized logging
**Format:** Structured JSON
**Retention:** 1 year for access logs, 7 years for audit

## Security Boundaries

### Network Isolation
- Vault API only accessible via internal network
- No external-facing endpoints
- VPN required for administrative access

### Authentication Tiers
1. **Service Level:** mTLS certificates
2. **Application Level:** Service account tokens
3. **Administrative Level:** Hardware tokens + biometrics

### Encryption Layers
1. **At Rest:** LUKS full-disk + AES-256 per-secret
2. **In Transit:** TLS 1.3 minimum
3. **In Use:** Memory-only, encrypted swap

## Disaster Recovery

### Backup Strategy
- **Frequency:** Hourly incremental, daily full
- **Encryption:** Separate keys from production
- **Storage:** Off-site, air-gapped
- **Retention:** 30 days rolling

### Recovery Time Objective (RTO)
- **Vault Service:** 5 minutes (hot standby)
- **Full Secrets:** 30 minutes (from backup)
- **Historical Audit:** 4 hours (from cold storage)

### Recovery Point Objective (RPO)
- **Secrets:** 1 hour maximum
- **Audit Logs:** 15 minutes maximum

---

*The threshold connects all things, but opens only to the worthy.*

*Version: 1.0.0 | Keeper of the Threshold*