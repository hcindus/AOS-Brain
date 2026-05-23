# AGI Identity Platform - Changelog

## Versioning Strategy
- **Schema Version**: Major.Minor.Patch (e.g., 1.0.0)
- **API Version**: Major.Minor (e.g., v1.0)
- **Connector Version**: Source-specific (e.g., acr-1.0.0)

---

## [1.0.0] - 2026-05-23
### Schema - Initial Release
- **Created**: Unified lifecycle database schema
- **Tables**: `identity`, `stage_event`, `data_markers`
- **Philosophy**: Event envelope + flexible markers
- **Author**: AGI Team

#### Schema Details
```sql
-- Three-table architecture
identity (spine)
  └─ stage_event (envelope)
       └─ data_markers (flexible facts)
```

#### Stage Codes Defined
1. `01_BIRTH_IDENTITY` - Vital records, SSN issuance
2. `02_CHILDHOOD_EDU` - K-12 enrollment
3. `03_HIGHER_EDU` - College, certifications
4. `04_EMPLOYMENT` - Work history, income
5. `05_FINANCIAL_CREDIT` - Credit reports, loans
6. `06_HEALTH_INSURANCE` - Coverage, providers
7. `07_LICENSES_PROPERTY` - Drivers license, property
8. `08_DIGITAL_BREACH` - Breaches, online footprint
9. `09_LEGAL_COURT` - Criminal, civil records
10. `10_DEATH_ARCHIVE` - Death records, archives

#### Indexes
- `idx_identity_master_key` - Fast identity lookup
- `idx_stage_event_identity` - Event per user
- `idx_stage_event_stage` - Stage filtering
- `idx_markers_event` - Marker per event
- `idx_markers_key` - Marker type filtering

#### Security
- `marker_value_encrypted BYTEA` - AES encryption
- `pii_classification` - Risk tiering
- RLS policies (pending)

---

## Connectors

### [acr-1.0.0] - AnnualCreditReport Connector
**Status**: In Development  
**Priority**: P0 (Highest value/effort ratio)  
**Stage**: `05_FINANCIAL_CREDIT`

#### Data Points Extracted
- Credit accounts (open/closed)
- Payment history (24+ months)
- Credit limits and balances
- Inquiries (hard/soft)
- Public records (liens, bankruptcies)
- Personal information (addresses, employers)

#### Authentication
- Identity verification Q&A
- Document upload fallback
- Session management

#### Confidence Score: 0.95
**Rationale**: Official source, federally mandated, direct from bureaus

---

## Planned Connectors

### Phase 1 (Identity MVP)
1. ✅ AnnualCreditReport (Stage 5) - IN PROGRESS
2. HaveIBeenPwned (Stage 8) - Breach monitoring
3. SSA MySocialSecurity (Stage 1/4) - Earnings history

### Phase 2 (Enrichment)
4. DataBroker OptOut Automation (Stage 8)
5. IRS Get Transcript (Stage 4) - Tax records
6. State DMV Records (Stage 7) - License status

### Phase 3 (Advanced)
7. Health Insurance Portals (Stage 6)
8. Education Clearinghouse (Stage 3)
9. Legal Record Aggregators (Stage 9)

---

## Value Analysis Log

### [2026-05-23] AnnualCreditReport Value Assessment
**Completed by**: Miles  
**Status**: Documented below

---

## Version Index

| Component | Version | Last Updated | Status |
|-----------|---------|--------------|--------|
| Schema | 1.0.0 | 2026-05-23 | Stable |
| Auth Bridge | 0.1.0 | 2026-05-23 | Alpha |
| ACR Connector | 1.0.0 | 2026-05-23 | In Dev |

