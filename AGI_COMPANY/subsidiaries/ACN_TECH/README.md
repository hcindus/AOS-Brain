# ACN-Tech Automation

Automated order processing for ribbons and toner from acn-tech.com with Performance Supply Depot pricing integration.

## Quick Start

```bash
# Check current prices
cd /root/.openclaw/workspace/AGI_COMPANY/subsidiaries/ACN_TECH
python3 scripts/scraper.py --check-prices

# Analyze opportunities
python3 scripts/order_automation.py --check

# Create an order
python3 scripts/order_automation.py --create-order --sku ERC-32 --qty 10
```

## Directory Structure

```
ACN_TECH/
├── acn_tech_config.json      # Main configuration
├── README.md                 # This file
├── products/                 # Scraped price data
│   ├── acn_tech_prices.json
│   └── price_history.json
├── orders/                   # Draft orders
│   └── ACN-YYYYMMDD-HHMMSS.json
└── scripts/
    ├── scraper.py           # Price scraper
    └── order_automation.py  # Order creation & monitoring
```

## Configuration

Edit `acn_tech_config.json`:

- `automation.enabled`: Enable/disable automation
- `automation.check_interval_minutes`: How often to check prices
- `pricing.markup_percent`: Your markup over ACN-Tech prices
- `pricing.min_margin_percent`: Minimum acceptable margin

## Products Tracked

### Ribbons
- Epson ERC-32
- Epson ERC-38
- Epson ERC-30/34/38
- Epson ERC-23
- Epson ERC-09

### Toner
- Brother TN-450, TN-660, TN-730, TN-760
- HP 83A (CF283A), 80A (CF280A), 85A (CE285A)

## Automation Flow

1. **Scraper** runs hourly to check ACN-Tech prices
2. **Analyzer** compares ACN-Tech cost + your markup vs PSDEPOT pricing
3. **Orders** are created as drafts when profitable deals found
4. **Notifications** sent via Telegram for review

## Manual Commands

```bash
# Full catalog scan
python3 scripts/scraper.py --full-scan

# Search specific product
python3 scripts/scraper.py --product ERC-32

# List all pending orders
python3 scripts/order_automation.py --list

# Start continuous monitoring
python3 scripts/order_automation.py --monitor
```

## Integration with PSDEPOT

The system syncs with your Performance Supply Depot pricing to ensure competitive margins.

## Status

- ✅ Scraper: Ready
- ✅ Order automation: Ready
- ⏳ Credentials: Pending (add to config when available)
- ⏳ Cron scheduling: Optional
