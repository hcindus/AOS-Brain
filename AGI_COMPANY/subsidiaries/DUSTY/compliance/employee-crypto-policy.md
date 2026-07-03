# Employee Crypto Handling Policy

**Version:** 1.0  
**Effective Date:** 2026-07-03  
**Applies to:** All employees handling cryptocurrency

---

## 1. Purpose

This policy establishes guidelines for employees who handle cryptocurrency as part of their job duties, ensuring security, compliance, and proper custody procedures.

---

## 2. Scope

This policy applies to:
- All employees with access to crypto wallets
- Employees processing crypto payments
- Employees with exchange API access
- Contractors with system access

---

## 3. Key Principles

### 3.1 Separation of Duties

- No single employee has full control over crypto assets
- Multi-signature wallets required for amounts over $10,000
- Transaction approval requires 2+ authorized personnel

### 3.2 Access Controls

| Access Level | Requirements | Approval |
|--------------|--------------|----------|
| Read-only | Employment verification | Manager |
| Transaction signing | Background check, training | Captain |
| Wallet creation | Full clearance, 90-day tenure | Executive |

### 3.3 Key Management

- **Hardware wallets:** Stored in secure location, access logged
- **API keys:** Rotated every 90 days minimum
- **Private keys:** Never stored in plaintext, encrypted at rest
- **Seed phrases:** Split using Shamir's Secret Sharing (2-of-3)

---

## 4. Transaction Procedures

### 4.1 Receiving Crypto

1. Verify sender address
2. Confirm transaction details in writing
3. Use dedicated receiving addresses per transaction
4. Confirm 3+ blockchain confirmations before crediting

### 4.2 Sending Crypto

1. Requestor submits signed request
2. Manager reviews and approves
3. Compliance checks destination (sanctions screening)
4. Transaction signed by authorized personnel
5. TXID recorded in transaction log

### 4.3 Thresholds

| Amount | Approval Required | Documentation |
|--------|-------------------|---------------|
| < $1,000 | Single manager | Email confirmation |
| $1,000 - $10,000 | Manager + Compliance | Written request |
| > $10,000 | Captain + 2 signatures | Board approval |

---

## 5. Security Requirements

### 5.1 Personal Devices

- Company-issued hardware wallets only
- No personal wallets for company funds
- 2FA required on all accounts

### 5.2 Work Environment

- Private keys never displayed on screen in public
- No screen sharing during wallet operations
- Secure, private workspace for transaction signing

### 5.3 Incident Reporting

Employees must immediately report:
- Lost or stolen devices with wallet access
- Suspected unauthorized transactions
- Phishing attempts or suspicious communications
- Any policy violations

---

## 6. Training Requirements

| Topic | Frequency | Method |
|-------|-----------|--------|
| Key security | Onboarding + Annual | In-person + Test |
| Exchange procedures | Onboarding + Quarterly | Video + Quiz |
| Incident response | Onboarding + Semi-annual | Drill |
| Regulatory updates | As needed | Newsletter |

---

## 7. Violations

| Violation | Consequence |
|-----------|-------------|
| Unreported key exposure | Suspension pending investigation |
| Unauthorized transaction | Termination + legal action |
| Policy bypass | Written warning (first), termination (repeat) |
| Failure to complete training | Suspension of crypto access |

---

## 8. Acknowledgment

All employees with crypto access must sign acknowledgment:

```
I, ____________, have read and understand the Employee Crypto Handling Policy.
I agree to comply with all provisions and understand that violations may result in disciplinary action.

Signature: ____________ Date: ____________
```

---

**Document Owner:** Mortimer  
**Review:** Quarterly  
**Next Review:** October 2026
