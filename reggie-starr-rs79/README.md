# Reggie Starr RS-79 — Digital Cash Register (v1.0.0.1)

Consolidated, runnable Python/Tkinter POS application produced from the
"Reggie Starr Master" spec document.

## Run
```bash
python3 reggie_starr_rs79.py
```
(Requires a display. On a headless box: `xvfb-run -a python3 reggie_starr_rs79.py`)

## Features
- Multilingual UI (8 languages), currency formatting (USD/EUR/GBP/BTC via babel)
- Tax programming, PLU & department management
- Discounts & surcharges, 8 payment methods (incl. BTC)
- Refund/void/exchange/cancel + financial/group/PLU/period/sales-total reports
- Clerk login/logout, register modes, split check/tender, layaway, gift cards,
  hold/recall, BTC QR, live exchange rates

## Dependencies (optional, gracefully degrade)
- babel (currency format), requests (live rates), qrcode + Pillow (BTC QR)
- All standard except `qrcode` (install: `pip install qrcode`)

## Note
This is the RS-79 **desktop** (Tkinter) build — distinct from the RS-80
**Android** (Kotlin) build.
