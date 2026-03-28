# Dusty Wallet — Technical Roadmap

**Product**: Dusty Wallet  
**Version**: 1.0  
**Last Updated**: 2026-02-18  
**Owner**: STACKTRACE (Chief Software Architect)  
**Team**: TAPTAP (Mobile), PIPELINE (Backend), BUGCATCHER (QA), SENTINEL (Security)

---

## Overview

Dusty Wallet is a cross-chain cryptocurrency wallet designed to:
1. Aggregate crypto dust from multiple exchanges and wallets
2. Consolidate small balances into usable amounts
3. Provide multi-chain support with a focus on low-fee chains (Bitgert)
4. Enable agents to receive payments and pay rent

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                        Mobile App (TAPTAP)                  │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐      │
│  │ Wallet  │  │ Balance │  │ Convert │  │ Settings│      │
│  │ Screen  │  │ Screen  │  │ Screen  │  │ Screen  │      │
│  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘      │
│       └──────────────┴──────────────┴──────────────┘       │
│                          │                                  │
│                    ┌─────▼─────┐                           │
│                    │  API Layer │                           │
│                    └─────┬─────┘                           │
└──────────────────────────┼──────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
┌───────▼───────┐  ┌──────▼──────┐  ┌──────▼──────┐
│  Exchange     │  │  Blockchain  │  │  Price Feed │
│  API Service  │  │  Node Service│  │  Service    │
│  (PIPELINE)   │  │  (PIPELINE) │  │  (PIPELINE) │
└───────────────┘  └─────────────┘  └─────────────┘
```

---

## Phase 1 — Prototype (COMPLETED)

### Features
- Static UI with network selector
- Mock balance display
- Basic layout and theme
- Placeholder dust list

### Technical
- React Native scaffold
- Basic navigation
- Mock data structures
- Static components

### Status: ✅ Complete (Reference Implementation)

---

## Phase 2 — Real Wallet Integration

### Timeline: Weeks 1-4

### Features
| Feature | Description |
|---------|-------------|
| **Wallet Connection** | Connect via private key, seed phrase, or wallet connect |
| **Multi-Chain Support** | Ethereum, BSC, Bitgert, Solana |
| **Balance Fetching** | Read token balances from connected wallets |
| **Dust Detection** | Identify balances below threshold per asset |
| **Network Switching** | Seamless network selection |

### Technical Implementation

#### Backend (PIPELINE)
```
Endpoints:
- GET /api/v1/wallets/:address/balances
- GET /api/v1/wallets/:address/dust
- GET /api/v1/networks
- POST /api/v1/wallets/connect

Services:
- BlockchainScanner: Indexes balances across chains
- DustDetector: Applies thresholds per token
- NetworkManager: Manages RPC connections
```

#### Mobile (TAPTAP)
```
Screens:
- ConnectWalletScreen (QR scan, manual entry)
- DashboardScreen (total balance, network selector)
- WalletDetailScreen (per-network breakdown)
- DustListScreen (identified dust)

Components:
- NetworkSelector
- BalanceCard
- DustItem
- ConnectWalletModal
```

### Security (SENTINEL)
- Private keys never stored in plain text
- Use secure enclave / keychain
- Encrypted local storage
- Connection logging

### Testing (BUGCATCHER)
- Unit tests for dust detection logic
- Integration tests for all chains
- UI tests for all screens

---

## Phase 3 — Price & Conversion Logic

### Timeline: Weeks 5-8

### Features
| Feature | Description |
|---------|-------------|
| **Price Feeds** | Real-time prices from CoinGecko |
| **USD Valuation** | Display dust value in USD |
| **Total Dust View** | Aggregate value across all networks |
| **Conversion Quotes** | Get quote for consolidating dust |
| **Target Token Selection** | Choose output token (BRISE, USDT, etc.) |

### Technical Implementation

#### Backend (PIPELINE)
```
Services:
- PriceService: Aggregates from CoinGecko, CoinMarketCap
- ConverterService: Calculates conversion quotes
- ExchangeRateCache: Caches rates with TTL

Endpoints:
- GET /api/v1/prices/:token
- GET /api/v1/convert/quote
- GET /api/v1/portfolio/summary
```

#### Mobile (TAPTAP)
```
Screens:
- PortfolioScreen (total value, breakdown)
- ConvertScreen (quote display, confirm)
- PriceAlertScreen (set alerts)

Components:
- PriceTicker
- ConversionQuoteCard
- PortfolioSummary
```

### Data Flow
```
1. User selects "View Dust"
2. App calls /dust endpoint
3. Backend fetches balances from chains
4. Backend fetches prices
5. Backend calculates dust threshold ($1 USD default)
6. Returns aggregated dust list with USD values
7. App displays sorted by value
```

---

## Phase 4 — Transaction & Security

### Timeline: Weeks 9-12

### Features
| Feature | Description |
|---------|-------------|
| **Transaction Signing** | Sign consolidation transactions |
| **Broadcast to Network** | Submit to blockchain |
| **Transaction History** | Track all transactions |
| **Confirmation Flow** | Clear confirm/reject workflow |
| **Error Handling** | Graceful failure handling |

### Technical Implementation

#### Backend (PIPELINE)
```
Services:
- TransactionBuilder: Creates unsigned txs
- TransactionSigner: Signs with encrypted key (never exposed)
- BroadcastService: Submits to network
- TransactionIndexer: Tracks history

Endpoints:
- POST /api/v1/transactions/build
- POST /api/v1/transactions/sign
- POST /api/v1/transactions/broadcast
- GET /api/v1/transactions/history

Security:
- Private keys encrypted at rest
- Signing happens in secure enclave
- Transaction preview before signing
- Nonce management
```

#### Mobile (TAPTAP)
```
Flow:
1. User taps "Consolidate Dust"
2. App shows preview: tokens, amounts, estimated gas
3. User confirms
4. App requests signature
5. Backend signs (key never leaves)
6. Backend broadcasts
7. App shows pending → confirmed
```

### Security (SENTINEL)
- **Key Management**: Keys encrypted, never logged
- **Transaction Validation**: Verify recipient, amount, gas before signing
- **Audit Trail**: All transactions logged with hashes
- **Rate Limiting**: Prevent spam attacks
- **Anomaly Detection**: Flag unusual patterns

### Testing (BUGCATCHER)
- Test on testnet first (Sepolia, BSC Testnet)
- Regression suite for all transaction types
- Security penetration testing
- Load testing for broadcasting

---

## Phase 5 — Polish & Growth

### Timeline: Weeks 13-16

### Features
| Feature | Description |
|---------|-------------|
| **Multi-Language Support** | i18n for global reach |
| **Analytics** | Opt-in usage analytics |
| **Theming** | Dark/light mode, custom themes |
| **App Store Prep** | iOS App Store, Google Play |
| **Onboarding Flow** | Guided first-time experience |
| **Push Notifications** | Transaction alerts |

### Technical Implementation

#### Mobile (TAPTAP)
```
i18n:
- react-i18next
- Initial: English, Spanish

Themes:
- Dark mode (default)
- Light mode
- Custom accent colors

Push:
- Firebase Cloud Messaging
- OneSignal alternative
```

#### App Store Prep
```
iOS:
- App Store Connect
- TestFlight beta
- App Store guidelines compliance

Android:
- Google Play Console
- Internal testing track
- Play Store guidelines compliance
```

---

## API Specification

### Base URL
```
Production: https://api.dustywallet.com
Staging: https://api-staging.dustywallet.com
```

### Endpoints

#### Wallet
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /v1/wallets/connect | Connect wallet |
| GET | /v1/wallets/:address | Get wallet info |
| DELETE | /v1/wallets/:address | Disconnect wallet |

#### Balances
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /v1/balances/:address | Get all balances |
| GET | /v1/balances/:address/dust | Get dust only |
| GET | /v1/networks | Get supported networks |

#### Portfolio
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /v1/portfolio/summary | Total portfolio value |
| GET | /v1/portfolio/history | Historical value |

#### Prices
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /v1/prices/:token | Get token price |
| GET | /v1/prices/batch | Get multiple prices |

#### Transactions
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /v1/transactions/build | Build transaction |
| POST | /v1/transactions/sign | Sign transaction |
| POST | /v1/transactions/broadcast | Broadcast transaction |
| GET | /v1/transactions/history | Transaction history |

---

## Supported Networks

| Network | Chain ID | RPC | Explorer |
|---------|----------|-----|----------|
| Ethereum | 1 | eth-mainnet | etherscan.io |
| BSC | 56 | bsc-mainnet | bscscan.com |
| Bitgert | 32520 | brise-mainnet | brisescan.com |
| Solana | 101 | solana-mainnet | solscan.io |

---

## Security Requirements

### All Phases
- [ ] HTTPS only
- [ ] API key rotation
- [ ] Rate limiting
- [ ] Input validation
- [ ] SQL injection prevention
- [ ] XSS prevention

### Phase 2+
- [ ] Encrypted key storage
- [ ] Secure enclave usage
- [ ] Audit logging

### Phase 4+
- [ ] Penetration testing
- [ ] SOC 2 compliance preparation
- [ ] Bug bounty program

---

## Milestones

| Phase | Milestone | Target |
|-------|-----------|--------|
| 1 | Prototype | ✅ Complete |
| 2 | Wallet Connection | Week 4 |
| 3 | Price & Convert | Week 8 |
| 4 | Transactions | Week 12 |
| 5 | App Store Ready | Week 16 |

---

## Dependencies

### Backend
- Node.js 18+
- PostgreSQL 14+
- Redis 7+
- Docker
- Kubernetes (future)

### Mobile
- React Native 0.72+
- TypeScript
- iOS 14+
- Android API 24+

### External Services
- CoinGecko API
- Infura / Alchemy (RPC)
- Ethers.js
- WalletConnect

---

## Future Enhancements (Post-Launch)

- Hardware wallet support (Ledger, Trezor)
- DeFi integrations (staking, yield)
- NFT support
- Multi-sig wallets
- Agent-to-agent payments
- Fiat on-ramp

---

## Risk Management

| Risk | Mitigation |
|------|------------|
| API rate limits | Caching, multiple providers |
| Network congestion | Fee estimation, retry logic |
| Key compromise | Hardware security module |
| Smart contract bugs | External audit, testnet first |
| Exchange API downtime | Fallback providers |

---

## Team Responsibilities

| Agent | Phase 1 | Phase 2 | Phase 3 | Phase 4 | Phase 5 |
|-------|---------|---------|--------|---------|---------|
| STACKTRACE | Arch | Arch | Arch | Arch | Review |
| TAPTAP | Build | Build | Build | Build | Polish |
| PIPELINE | Build | Build | Build | Build | Deploy |
| BUGCATCHER | Test | Test | Test | Test | Test |
| SENTINEL | Review | Review | Review | Review | Review |

---

_"Dust to dust, but with better UX."_ — The Dusty Team
