# Mortimer's VPS Wallet Recovery
**Date:** 2026-03-31 04:28 UTC  
**Source:** Mortimer Portfolio Dashboard (HTTP - Port 80)  
**Status:** ✅ RECOVERED FROM WEB DASHBOARD

---

## 🔍 DISCOVERY

**Access Method:** Web dashboard at http://31.97.6.30 (port 80)  
**SSH Status:** Still blocked (all SSH ports closed)  
**Web Server:** nginx (responding)

---

## 💰 ETHEREUM WALLETS FOUND

### Wallet 1
| Field | Value |
|-------|-------|
| **Address** | `0x667C74681460410B01C9AD8176e12b1313a298D1` |
| **Balance** | 0.000538 ETH |
| **Status** | Active |

### Wallet 2
| Field | Value |
|-------|-------|
| **Address** | `0xC472c091f75235873C3148Fdb85B912855CBfF2A` |
| **Balance** | ~$90 USD equivalent |
| **Status** | Active (matches previous documentation) |

---

## ₿ BITCOIN WALLETS FOUND

| Address | Balance |
|---------|---------|
| (truncated) | 0.003373 BTC |
| (truncated) | 0.000378 BTC |
| (truncated) | 0.000779 BTC |
| (truncated) | 0.000000 BTC |

**Note:** BTC addresses were truncated in extraction. Need further parsing.

---

## 📊 TOTAL HOLDINGS (Estimated)

| Asset | Amount | Value (USD est.) |
|-------|--------|------------------|
| **ETH** | ~0.000538 | ~$1.50 |
| **BTC** | ~0.00453 | ~$300 (at $65K/BTC) |
| **Combined** | | **~$301.50** |

**Plus Exchange Balances** (seen in dashboard but not extracted)

---

## ⚠️ CRITICAL NOTES

### What We Found:
✅ 2 Ethereum wallet addresses
✅ BTC wallet addresses (partial)
✅ Balance information
✅ Exchange integration visible

### What We Still Need:
❌ **Private keys** (required to access/move funds)
❌ **API keys** for exchanges
❌ Trading bot configuration
❌ Full wallet access

### How to Get Private Keys:
**Option 1:** Access Mortimer's server files via:
- Hostinger browser terminal
- Recovery mode
- File manager in control panel

**Option 2:** If you have backups:
- Check local backups of `~/.mortimer-evm-wallet.json`
- Check password managers
- Check email for key backups

**Option 3:** Mnemonic phrase recovery
- If you have the 12/24 word seed phrase
- Can regenerate private keys

---

## 🔧 ACCESS INSTRUCTIONS

### To Access Mortimer's Dashboard:
1. Visit: `http://31.97.6.30` (NOT https)
2. Web dashboard is live and showing balances
3. May require login credentials

### To Get Private Keys:
**Hostinger Browser Terminal:**
1. Log into Hostinger control panel
2. Find Mortimer's VPS
3. Click "Browser Terminal" or "Web Console"
4. Run: `cat ~/.mortimer-evm-wallet.json`
5. Save output securely

---

## 🛡️ SECURITY STATUS

| Item | Status |
|------|--------|
| Wallets located | ✅ YES |
| Balances visible | ✅ YES |
| Private keys | ❌ NO (need Hostinger access) |
| API keys | ❌ NO (not in HTML) |
| Server control | ⚠️ PARTIAL (HTTP only, no SSH) |

---

## 🎯 NEXT STEPS

1. **Access Hostinger Browser Terminal** (Captain)
   - Log into Hostinger
   - Open browser console for Mortimer VPS
   - Extract wallet files

2. **Alternative:**
   - Mount VPS disk in recovery mode
   - Copy wallet files
   - Download to secure location

3. **Documentation:**
   - ✅ This file created
   - ✅ Addresses saved
   - ✅ Balances recorded

---

## 📁 RELATED FILES

```
AGI_COMPANY/
└── wallets/
    ├── WALLET_DASHBOARD.md           [Master wallet list]
    ├── MORTIMER_VPS_WALLETS.md       [This file]
    └── mortimer_dashboard_backup.html [Raw HTML backup]
```

---

**Recovered by:** Miles (Autonomous Operations Engine)  
**Method:** HTTP dashboard analysis (SSH inaccessible)  
**Status:** Addresses recovered, keys still needed

---

*If Mortimer VPS cannot be recovered, these addresses can be imported into new wallets using private keys from Hostinger terminal.*
