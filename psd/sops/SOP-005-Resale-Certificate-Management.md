# SOP-005: Resale Certificate Number Management
**Standard Operating Procedure — Performance Supply Depot LLC**

| Field | Value |
|-------|-------|
| **SOP ID** | SOP-005 |
| **Version** | 1.0.0 |
| **Effective Date** | 2026-08-05 |
| **Owner** | Miles / Operations |
| **Review Cycle** | Quarterly (every 90 days) |
| **Classification** | Internal — Operational |
| **Roast Score** | Not yet scored |

---

## 1. Purpose & Scope

### 1.1 Purpose
This SOP defines the standard process for managing Performance Supply Depot's resale certificate numbers across all 50 states. It ensures certificate data is accurate, accessible, and updated in a single source of truth — eliminating the need to hunt through spreadsheets, emails, or HTML files.

### 1.2 Scope
- Applies to all PSD resale/seller's permits and tax exemption certificates
- Covers addition, update, renewal, and audit of certificate numbers
- Includes both the operational data store and the public-facing web page

### 1.3 Why This Exists
RIP GoR — the old way was "keep it in your head or in a random spreadsheet." This SOP makes cert management a 60-second operation instead of a 30-minute archaeology dig.

---

## 2. System Architecture

```
┌─────────────────────────────────────────────────┐
│              RESALE CERTIFICATE SYSTEM           │
├─────────────────────────────────────────────────┤
│                                                  │
│  ┌──────────────────────┐                       │
│  │  resale-numbers.json │  ◄── Source of Truth  │
│  │  /data/              │      (server-side)    │
│  └──────────┬───────────┘                       │
│             │                                    │
│             ▼                                    │
│  ┌──────────────────────┐                       │
│  │  Admin Manager       │  ◄── Edit Interface   │
│  │  /admin/resale-      │      (browser-based)  │
│  │  manager.html        │                       │
│  └──────────┬───────────┘                       │
│             │                                    │
│             ▼                                    │
│  ┌──────────────────────┐                       │
│  │  Public Page         │  ◄── Customer-facing  │
│  │  /resale-licenses.   │      (read-only view) │
│  │  html                │                       │
│  └──────────────────────┘                       │
│                                                  │
└─────────────────────────────────────────────────┘
```

### File Locations
| File | Path | Purpose |
|------|------|---------|
| **Data Store** | `/var/www/psdepot.com/data/resale-numbers.json` | Single source of truth |
| **Admin UI** | `/var/www/psdepot.com/admin/resale-manager.html` | Edit interface |
| **Public Page** | `/var/www/psdepot.com/resale-licenses.html` | Customer-facing directory |
| **This SOP** | `/root/.openclaw/workspace/psd/sops/SOP-005-Resale-Certificate-Management.md` | Documentation |

---

## 3. Certificate Statuses

| Status | Badge | Meaning | Action Required |
|--------|-------|---------|-----------------|
| **active** | ✅ Green | Valid certificate on file with number | None — verify at quarterly audit |
| **pending** | ⏳ Yellow | Applied but awaiting state issuance | Follow up with state every 30 days |
| **expired** | 🔴 Red | Certificate has expired | Renew immediately via state portal |
| **not_needed** | ⊘ Gray | No sales tax state (AK, DE, MT, NH, OR) | None — verify quarterly |

### State-Specific Notes
- **No sales tax states** (not_needed): Alaska, Delaware, Montana, New Hampshire, Oregon
- **Certificate naming varies by state**: "Resale Certificate," "Seller's Permit," "Sales Tax License," "Transaction Privilege Tax License," etc.
- **Some states expire annually**, others are perpetual until revoked

---

## 4. Standard Operating Procedure

### 4.1 Adding a New Certificate

**Trigger:** PSD obtains a new resale certificate from a state

**Steps:**
1. Receive certificate from state (email/portal/mail)
2. Navigate to `https://psdepot.com/admin/resale-manager.html`
3. Click the state row or search for the state
4. Click ✏️ (edit) on the target state
5. Enter the certificate number exactly as shown on the document
6. Change status from `pending` to `active`
7. Add notes: expiration date, application ID, issuing office contact
8. Click **Save**
9. Press `Ctrl+S` to download updated JSON
10. Replace `/var/www/psdepot.com/data/resale-numbers.json` with the downloaded file
11. Verify at `https://psdepot.com/admin/resale-manager.html`

**Validation Check:**
```bash
# Verify JSON is valid after update
python3 -m json.tool /var/www/psdepot.com/data/resale-numbers.json > /dev/null && echo "✅ Valid" || echo "❌ Invalid"
```

### 4.2 Updating an Existing Number

**Trigger:** Certificate renewed, number changed, or correction needed

**Steps:**
1. Open the admin manager
2. Edit the target state
3. Update the number and/or status
4. Save and replace the JSON file

### 4.3 Renewal Processing

**Trigger:** Certificate approaching or past expiration

**Steps:**
1. Identify expiring certs (quarterly audit — see Section 6)
2. Visit the state's tax department website (linked from resale-licenses.html)
3. Complete the renewal application
4. Upon receiving new certificate:
   - Update number if changed
   - Update notes with new expiration date
   - Keep status as `active`
5. If state issues new number, update accordingly

### 4.4 Adding a New State (PENDING → ACTIVE)

**Trigger:** PSD expands to a state where we previously had no certificate

**Steps:**
1. Visit `https://psdepot.com/resale-licenses.html`
2. Find the state and click the link to the state's tax portal
3. Complete the application
4. Record the application confirmation in the admin manager (status: `pending`, notes: application ID + date)
5. When certificate arrives → update to `active`

---

## 5. Admin Interface Usage

### 5.1 Access
- **URL:** `https://psdepot.com/admin/resale-manager.html`
- **Access:** Internal only (no login — protect via .htaccess or server-level auth if needed)
- **Browser Support:** Chrome, Firefox, Safari, Edge (modern versions)

### 5.2 Key Features
| Feature | How To |
|---------|--------|
| **Search** | Type in search box — filters by state name, abbreviation, or cert number |
| **Filter** | Click status buttons to filter: All / Active / Pending / Expired / N/A |
| **Sort** | Click column headers to sort ascending/descending |
| **Edit** | Click ✏️ on any row to open the edit modal |
| **Save** | `Ctrl+S` or click "Save Changes" — downloads updated JSON |
| **Export** | Click "Export CSV" for spreadsheet import |

### 5.3 Quick Workflow (60 seconds)
```
1. Open admin page
2. Find state (search or sort)
3. Click ✏️ → enter number → select status → save
4. Ctrl+S → download JSON
5. Replace on server
✅ Done
```

---

## 6. Audit Schedule

### 6.1 Quarterly Audit (Required)
**Frequency:** Every 90 days
**Owner:** Operations
**Checklist:**
- [ ] Open admin manager
- [ ] Verify all `active` certs still valid (check expiration dates in notes)
- [ ] Follow up on all `pending` applications older than 60 days
- [ ] Flag any certs expiring within 90 days
- [ ] Verify `not_needed` states (sales tax laws can change)
- [ ] Export CSV for records
- [ ] Document findings in `#compliance` channel or internal log

### 6.2 Annual Review
**Frequency:** Every 12 months (January)
**Additional Checks:**
- [ ] Confirm all active certificate numbers match physical/PDF copies
- [ ] Review any state law changes that may affect certificate requirements
- [ ] Archive previous year's CSV export
- [ ] Update SOP if process has changed

### 6.3 Audit Commands
```bash
# Quick audit: count certificates by status
python3 -c "
import json
with open('/var/www/psdepot.com/data/resale-numbers.json') as f:
    data = json.load(f)
from collections import Counter
statuses = Counter(c['status'] for c in data['certificates'])
for s, n in statuses.items():
    print(f'{s}: {n}')
"

# Find certificates with empty/missing numbers
python3 -c "
import json
with open('/var/www/psdepot.com/data/resale-numbers.json') as f:
    data = json.load(f)
for c in data['certificates']:
    if c['status'] == 'active' and c['number'] in ('PENDING', '', 'N/A'):
        print(f'⚠️  {c[\"state\"]} ({c[\"abbr\"]}): active but no valid number!')
"
```

---

## 7. Edge Cases & Error Handling

### 7.1 Certificate Number Format Varies by State
- Some states issue short numbers (e.g., "12345")
- Others issue long alphanumeric strings (e.g., "SUT-1234567-001")
- **Rule:** Enter the number EXACTLY as shown on the official document

### 7.2 Certificate Denied or Rejected
1. Change status to `pending`
2. Add note: "Rejected YYYY-MM-DD — [reason]"
3. Investigate and reapply within 14 days
4. Do NOT delete the certificate entry

### 7.3 Business Entity Change (LLC → Corp, etc.)
1. Old certificates may become invalid
2. Mark existing entries as `expired` with note: "Entity change — new EIN"
3. Create new applications under the new entity
4. Keep old entries for audit trail

### 7.4 State Changes Sales Tax Law
- Monitor annually (January review)
- If a no-tax state adds sales tax: change status from `not_needed` to `pending`
- If a taxed state eliminates sales tax: change status to `not_needed`

---

## 8. Roles & Responsibilities

| Role | Responsibility |
|------|---------------|
| **Operations (Miles/Agent)** | Day-to-day updates, quarterly audits, status tracking |
| **Captain** | Final approval for new state applications, entity changes |
| **Compliance** | Annual review, legal changes, verification against physical docs |

---

## 9. Metrics & KPIs

| Metric | Target | Measurement |
|--------|--------|-------------|
| Certificate accuracy | 100% | All active certs have valid numbers |
| Renewal on-time rate | 100% | Zero expired certs at any time |
| Pending-to-Active time | < 45 days | Time from application to number entry |
| Audit completion | 4/year | Quarterly audits completed on schedule |

---

## 10. Related Documents

| Document | Path |
|----------|------|
| Public Resale Directory | `https://psdepot.com/resale-licenses.html` |
| Admin Manager | `https://psdepot.com/admin/resale-manager.html` |
| Data Source | `/var/www/psdepot.com/data/resale-numbers.json` |
| SOP-001 | Lead Response & Qualification |
| SOP-002 | Quote Generation & Follow-Up |
| SOP-003 | Order Status & Customer Inquiry |

---

## 11. Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-08-05 | Miles | Initial creation. RIP GoR. JSON data store, admin UI, quarterly audit cycle. |

---

*End of SOP-005. File updates go here → https://psdepot.com/admin/resale-manager.html*
