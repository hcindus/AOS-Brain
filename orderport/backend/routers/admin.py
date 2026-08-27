"""Admin portal router — Company/Rep view: all accounts, activate/deactivate,
billing, and fund distribution ledger."""
from fastapi import APIRouter, HTTPException, Depends, Header

import db
import auth as authmod
import config

router = APIRouter(prefix="/a", tags=["admin"])


def get_conn():
    conn = db.get_conn()
    try:
        yield conn
    finally:
        conn.close()


def require_admin(authorization: str = Header(None), conn=Depends(get_conn)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(401, "Missing token")
    tok = authmod.parse_token(authorization[7:])
    if not tok or tok["role"] not in ("admin", "rep"):
        raise HTTPException(403, "Admin required")
    return tok


@router.get("/accounts")
def list_accounts(tok=Depends(require_admin), conn=Depends(get_conn)):
    rows = conn.execute(
        """SELECT a.*, r.name AS rep_name, r.share_bps AS rep_share_bps,
                  (SELECT COUNT(*) FROM orders o WHERE o.account_id=a.id) AS order_count,
                  (SELECT COALESCE(SUM(total_cents),0) FROM orders o WHERE o.account_id=a.id) AS total_volume_cents
           FROM accounts a LEFT JOIN reps r ON r.id=a.rep_id ORDER BY a.id DESC"""
    ).fetchall()
    return {"accounts": [dict(r) for r in rows]}


@router.post("/accounts/{account_id}/status")
def set_status(account_id: int, payload: dict, tok=Depends(require_admin), conn=Depends(get_conn)):
    status = payload.get("status")
    if status not in ("active", "suspended"):
        raise HTTPException(400, "status must be active or suspended")
    conn.execute("UPDATE accounts SET status=? WHERE id=?", (status, account_id))
    conn.commit()
    return {"ok": True, "account_id": account_id, "status": status}


@router.get("/payouts")
def list_payouts(tok=Depends(require_admin), conn=Depends(get_conn)):
    rows = conn.execute(
        """SELECT p.*, a.business_name, r.name AS rep_name
           FROM payouts p
           LEFT JOIN accounts a ON a.id=p.account_id
           LEFT JOIN reps r ON r.id=p.rep_id
           ORDER BY p.id DESC LIMIT 500"""
    ).fetchall()
    return {"payouts": [dict(r) for r in rows]}


@router.get("/summary")
def summary(tok=Depends(require_admin), conn=Depends(get_conn)):
    s = conn.execute(
        """SELECT
             COALESCE(SUM(total_cents),0) AS total_volume,
             COALESCE(SUM(business_cents),0) AS business_total,
             COALESCE(SUM(company_cents),0) AS company_total,
             COALESCE(SUM(rep_cents),0) AS rep_total,
             COUNT(*) AS order_count
           FROM payouts"""
    ).fetchone()
    return dict(s)


@router.post("/reps")
def add_rep(payload: dict, tok=Depends(require_admin), conn=Depends(get_conn)):
    cur = conn.execute(
        "INSERT INTO reps (name, email, share_bps) VALUES (?,?,?)",
        (payload["name"], payload.get("email", ""),
         int(payload.get("share_bps", config.REP_SHARE_BPS))),
    )
    conn.commit()
    return {"id": cur.lastrowid}
