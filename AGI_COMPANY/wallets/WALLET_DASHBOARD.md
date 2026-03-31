# AGI Company Wallet Dashboard
**CONFIDENTIAL - Internal Use Only**  
**Last Updated:** 2026-03-31 04:10 UTC  
**Classification:** RESTRICTED

---

## 🔐 WALLET INVENTORY

### 1. Miles (Miles.cloud) - Test Wallet
| Field | Value |
|-------|-------|
| **Address** | `0x52eF1d792a8F167AD868d85f5062FAb5476ADC9D` |
| **Network** | Sepolia Testnet |
| **Purpose** | Dusty Wallet Beta Testing |
| **Status** | ✅ Active |
| **Balance** | 0 SepoliaETH |
| **Created** | 2026-03-31 03:45 UTC |
| **Credentials** | Emailed to Captain |
| **Access** | Mobile: https://dusty.myl0nr0s.cloud/mobile-wallet.html |

### 2. Mortimer (Mortimer.cloud) - Production Wallet
| Field | Value |
|-------|-------|
| **Address** | `0xAf99f2B58B9107193D7F87A4Dff2bD04825e54aE` |
| **Networks** | Base, Ethereum, Polygon, Arbitrum, Optimism |
| **Purpose** | Multi-agent system operations |
| **Status** | ⚠️ OFFLINE (SSH timeout) |
| **Balance** | **0 ETH** (needs funding) |
| **Private Key** | `~/.mortimer-evm-wallet.json` (chmod 600) |
| **Last Access** | Unknown |
| **Issue** | Cannot SSH to Mortimer.cloud (31.97.6.30) |

### 3. Cryptonio (The Great Cryptonio) - Trading Wallet
| Field | Value |
|-------|-------|
| **Address** | `0x2ce0c5D9aaD321d1Ea0ad02F02bde75A5fB0E3BE` |
| **Networks** | Base, Ethereum, Polygon, Arbitrum, Optimism |
| **Purpose** | Portfolio management, NFTs, trading |
| **Status** | ✅ Active |
| **Balance** | **~$90 USD** (0.045 ETH) |
| **Location** | `/root/.openclaw/workspace/aocros/agent_sandboxes/the-great-cryptonio/` |
| **Access** | GitHub documented, tmux session available |

---

## 💰 BALANCE SUMMARY

| Wallet | Asset | Network | Balance | Value (USD) |
|--------|-------|---------|---------|-------------|
| Miles | ETH | Sepolia | 0.00 | $0.00 |
| Mortimer | ETH | All | 0.00 | **$0.00** ⚠️ |
| Cryptonio | ETH | Base | 0.045 | **~$90.00** ✅ |
| **TOTAL** | | | | **~$90.00** |

---

## 🔧 ACTIONS NEEDED

### Priority 1: Mortimer's Wallet (URGENT)
**Issue:** Empty wallet + VPS inaccessible

**Options:**
1. **Fund Mortimer** (Recommended)
   - Send ETH to: `0xAf99f2B58B9107193D7F87A4Dff2bD04825e54aE`
   - Network: Base (lowest gas fees)
   - Amount: 0.01 ETH (~$20) minimum

2. **Fix VPS Access**
   - Check why Mortimer.cloud (31.97.6.30) times out
   - Verify SSH service is running
   - Check firewall rules

3. **Transfer from Cryptonio**
   - Use Cryptonio's ~$90 balance
   - Requires Cryptonio wallet access

### Priority 2: Cryptonio Wallet Access
**Status:** Can attempt access

**Location:** `aocros/agent_sandboxes/the-great-cryptonio/`

**Commands to check:**
```bash
# Check if session is running
tmux list-sessions | grep cryptonio

# Check balance
cd /root/.openclaw/workspace/skills/evm-wallet
node src/balance.js base --wallet 0x2ce0c5D9aaD321d1Ea0ad02F02bde75A5fB0E3BE

# Check if we can access private key
ls -la ~/.cryptonio-wallet.json 2>/dev/null || echo "Key not in standard location"
```

### Priority 3: Miles' Test Wallet
**Status:** Ready for Dusty Wallet testing

**Next Steps:**
- Get SepoliaETH from faucet: https://sepoliafaucet.com
- Test Dusty Wallet transactions
- Report any bugs

---

## 🛡️ SECURITY NOTES

**Classification:** RESTRICTED
- **NEVER share private keys**
- **NEVER commit keys to GitHub**
- **Always use hardware wallet for large amounts**
- **Test on Sepolia before mainnet**

**Access Levels:**
- **Captain:** Full access (requires your approval for transfers)
- **Miles:** Read-only monitoring
- **Mortimer:** System operations (when online)
- **Cryptonio:** Trading operations

---

## 📊 FUNDRAISING STATUS

| Wallet | Needed | Purpose | Urgency |
|--------|--------|---------|---------|
| Miles | 0.01 ETH | Testing | Low |
| Mortimer | 0.01 ETH | Operations | **HIGH** |
| Cryptonio | 0 | Already funded | N/A |

**Total Needed:** 0.02 ETH (~$40)

---

## 🔗 RELATED FILES

```
AGI_COMPANY/
└── wallets/
    └── WALLET_DASHBOARD.md              [THIS FILE]

aocros/
├── agent_sandboxes/
│   ├── mortimer/
│   │   └── MORTIMER_EVM_WALLET.md     [Detailed docs]
│   └── the-great-cryptonio/
│       └── (wallet files)
└── dusty/
    └── frontend/
        └── mobile-wallet.html           [Miles' test wallet UI]

~/.mortimer-evm-wallet.json             [Mortimer's private key]
~/.cryptonio-wallet.json                [Cryptonio's private key - if exists]
```

---

## 📅 LAST ACTIONS LOG

| Date | Action | Wallet | Status |
|------|--------|--------|--------|
| 2026-03-31 03:45 | Created test wallet | Miles | ✅ Complete |
| 2026-03-31 03:45 | Emailed credentials | Miles | ✅ Sent |
| 2026-03-31 04:10 | Attempted SSH to Mortimer | Mortimer | ❌ Failed |
| 2026-03-31 04:10 | Located Cryptonio wallet | Cryptonio | ✅ Found |

---

**Next Update:** After Mortimer funding or VPS access restored

**Questions:** Contact miles@myl0nr0s.cloud

---

*Document Created: 2026-03-31 04:10 UTC*  
*Author: Miles (Autonomous Operations Engine)*  
*Classification: RESTRICTED*
