# Exchange Terms of Service Compliance Matrix

**Version:** 1.0  
**Last Updated:** 2026-07-03  
**Status:** Phase 1 Complete

---

## 1. Supported Exchanges

| Exchange | Status | Compliance Level | Notes |
|----------|--------|------------------|-------|
| **Binance.US** | ✅ Operational | Full | US-regulated, restricted states |
| **Coinbase** | ✅ Operational | Full | Public company, highest compliance |
| **Kraken** | ✅ Operational | Full | US-regulated, strong security |
| **Bitgert** | ⚠️ Limited | Partial | Smaller exchange, higher risk |

---

## 2. Exchange-Specific Requirements

### Binance.US

| Requirement | Status | Action |
|-------------|--------|--------|
| KYC Verification | ✅ Required | All users complete before trading |
| US Residency | ✅ Required | SSN verification |
| Restricted States | ✅ Blocked | NY, TX, VT blocked at registration |
| API Rate Limits | ⚠️ Monitored | 1200 requests/min |
| IP Whitelisting | ✅ Implemented | Office IPs only |

**Prohibited Activities:**
- Wash trading
- Market manipulation
- Using bots without approval
- Account sharing

---

### Coinbase

| Requirement | Status | Action |
|-------------|--------|--------|
| KYC Verification | ✅ Required | Full identity verification |
| Address Verification | ✅ Required | Proof of residence |
| Source of Funds | ✅ Documented | Trading capital source |
| API Access | ✅ Approved | Institutional account |
| Trading Limits | ✅ Monitored | Daily/weekly limits enforced |

**Prohibited Activities:**
- Arbitrage abuse
- Front-running
- Layering
- Spoofing

---

### Kraken

| Requirement | Status | Action |
|-------------|--------|--------|
| KYC Verification | ✅ Required | Tier 3 for our volume |
| Proof of Address | ✅ Required | Utility bill acceptable |
| API Access | ✅ Approved | Secure key management |
| Withdrawal Limits | ✅ Monitored | Daily limits tracked |
| Margin Trading | ❌ Not Used | Spot trading only |

**Prohibited Activities:**
- Abusive API usage
- Coordinated trading
- Pump and dump schemes

---

### Bitgert

| Requirement | Status | Action |
|-------------|--------|--------|
| KYC Verification | ⚠️ Basic | Limited verification |
| Trading Volume | ⚠️ Limited | Low liquidity concern |
| Security | ⚠️ Review | 2FA required |
| Withdrawal Limits | ⚠️ Monitored | Small amounts only |
| Risk Rating | 🟡 Medium | Higher risk, use caution |

**Recommendations:**
- Minimal exposure
- Fast in/out only
- Monitor for delisting

---

## 3. Compliance Monitoring

### Daily Checks

- [ ] API key status (all exchanges)
- [ ] Rate limit utilization
- [ ] Account standing (no warnings)
- [ ] IP access logs reviewed

### Weekly Checks

- [ ] Exchange policy updates reviewed
- [ ] New restriction announcements
- [ ] API documentation changes
- [ ] Trading pattern analysis

### Monthly Checks

- [ ] Full ToS review (all exchanges)
- [ ] Compliance score update
- [ ] Risk assessment refresh
- [ ] Escalation procedures tested

---

## 4. Violation Response

| Severity | Exchange Response | Our Response |
|----------|-------------------|--------------|
| Warning | Email notification | Immediate review |
| Suspension | Temporary freeze | Halt operations |
| Termination | Account closure | Emergency protocol |

---

## 5. Policy Updates Log

| Date | Exchange | Change | Action Taken |
|------|----------|--------|--------------|
| 2026-07-03 | All | Initial matrix | Baseline established |

---

**Document Owner:** Mortimer  
**Review:** Monthly  
**Next Review:** August 2026
