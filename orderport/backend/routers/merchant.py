"""Merchant portal router — business owner edits menu, prices, hours, views orders."""
from fastapi import APIRouter, HTTPException, Depends, Header

import db
import auth as authmod

router = APIRouter(prefix="/m", tags=["merchant"])


def get_conn():
    conn = db.get_conn()
    try:
        yield conn
    finally:
        conn.close()


def require_merchant(authorization: str = Header(None), conn=Depends(get_conn)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(401, "Missing token")
    tok = authmod.parse_token(authorization[7:])
    if not tok or tok["role"] != "merchant":
        raise HTTPException(401, "Invalid token")
    return tok


@router.get("/menu")
def get_menu(tok=Depends(require_merchant), conn=Depends(get_conn)):
    cats = conn.execute(
        "SELECT * FROM categories WHERE account_id=? ORDER BY sort_order", (tok["account_id"],)
    ).fetchall()
    items = conn.execute(
        "SELECT * FROM menu_items WHERE account_id=? ORDER BY sort_order", (tok["account_id"],)
    ).fetchall()
    return {"categories": [dict(c) for c in cats], "items": [dict(i) for i in items]}


@router.post("/menu/item")
def add_item(payload: dict, tok=Depends(require_merchant), conn=Depends(get_conn)):
    cur = conn.execute(
        """INSERT INTO menu_items (account_id, category_id, name, description, price_cents, image_url)
           VALUES (?,?,?,?,?,?)""",
        (tok["account_id"], payload.get("category_id"), payload["name"],
         payload.get("description", ""), int(payload["price_cents"]),
         payload.get("image_url", "")),
    )
    conn.commit()
    return {"id": cur.lastrowid}


@router.put("/menu/item/{item_id}")
def update_item(item_id: int, payload: dict, tok=Depends(require_merchant), conn=Depends(get_conn)):
    row = conn.execute(
        "SELECT * FROM menu_items WHERE id=? AND account_id=?", (item_id, tok["account_id"])
    ).fetchone()
    if not row:
        raise HTTPException(404, "Item not found")
    fields = {}
    for k in ("name", "description", "image_url"):
        if k in payload:
            fields[k] = payload[k]
    if "price_cents" in payload:
        fields["price_cents"] = int(payload["price_cents"])
    if "category_id" in payload:
        fields["category_id"] = payload["category_id"]
    if "available" in payload:
        fields["available"] = 1 if payload["available"] else 0
    if fields:
        fields["updated_at"] = "datetime('now')"
        sets = ", ".join(f"{k}=?" for k in fields)
        conn.execute(f"UPDATE menu_items SET {sets} WHERE id=?", (*fields.values(), item_id))
        conn.commit()
    return {"ok": True}


@router.delete("/menu/item/{item_id}")
def delete_item(item_id: int, tok=Depends(require_merchant), conn=Depends(get_conn)):
    conn.execute("DELETE FROM menu_items WHERE id=? AND account_id=?", (item_id, tok["account_id"]))
    conn.commit()
    return {"ok": True}


@router.get("/orders")
def list_orders(tok=Depends(require_merchant), conn=Depends(get_conn)):
    rows = conn.execute(
        "SELECT * FROM orders WHERE account_id=? ORDER BY id DESC LIMIT 100", (tok["account_id"],)
    ).fetchall()
    return {"orders": [dict(r) for r in rows]}


@router.post("/settings")
def update_settings(payload: dict, tok=Depends(require_merchant), conn=Depends(get_conn)):
    allowed = ("business_name", "pickup_hours", "phone", "email", "address")
    sets = {}
    for k in allowed:
        if k in payload:
            sets[k] = payload[k]
    if sets:
        cols = ", ".join(f"{k}=?" for k in sets)
        conn.execute(f"UPDATE accounts SET {cols} WHERE id=?", (*sets.values(), tok["account_id"]))
        conn.commit()
    return {"ok": True}
