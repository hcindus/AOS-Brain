# OrderPort — multi-tenant online ordering SaaS

Build two ways: hand-written reference (this repo) vs Dark Factory. Compare.

## What it does
Per-business pickup ordering with a three-way revenue split:
**Business 85% · Company (PSDepot) 10% · Rep 5%** (configurable in `config.py`).

## Components
| Piece | Path | Notes |
|---|---|---|
| Backend (FastAPI) | `backend/main.py` | one service, all routers |
| DB schema | `backend/db.py` | SQLite (→ Postgres later) |
| Money split + Stripe | `backend/money.py` | Connect destination charges |
| Notifications | `backend/notify.py` | email (SMTP) / SMS (Twilio) / ESC-POS printer |
| Storefront | `backend/routers/storefront.py` | `GET /s/{slug}`, `POST /s/{slug}/order` |
| Merchant portal | `backend/routers/merchant.py` | menu CRUD, orders, settings |
| Admin portal | `backend/routers/admin.py` | accounts, activate/deactivate, payouts, reps |
| Auth | `backend/routers/auth_routes.py` + `backend/auth.py` | login + bootstrap admin |
| Deploy | `deploy/orderport.service` + `deploy/nginx-orderport.conf` | systemd + nginx |

## Run locally
```bash
cd backend
pip install -r requirements.txt
python3 -c "import db; db.init_db()"
uvicorn main:app --reload --port 8088
```

Bootstrap first admin (once):
```bash
curl -X POST localhost:8088/auth/bootstrap \
  -H 'Content-Type: application/json' \
  -d '{"email":"admin@psdepot.com","password":"CHANGE_ME"}'
```

## Revenue split (basis points)
- `COMPANY_SHARE_BPS=1000` (10%)
- `REP_SHARE_BPS=500` (5%)
- business = remainder (85%)

## URL map (once nginx + systemd live)
- Storefront: `psdepot.com/order/{slug}`
- Merchant: `psdepot.com/portal/`
- Admin: `psdepot.com/admin-portal/`
- API: `psdepot.com/api/orderport/`

## Not yet built (next)
- Frontend UI (storefront/merchant/admin HTML)
- Stripe webhook → mark order paid + settle payout + fire notifications
- Live tax (reuse existing CDTFA logic from `payment_server.py`)
- ESC/POS printer config per-account (IP + port + channel)
- Monthly subscription billing (Stripe recurring) + dunning
- Fund distribution: auto-payout rep share (Stripe Connect transfers)
