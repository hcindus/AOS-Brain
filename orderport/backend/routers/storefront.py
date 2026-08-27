"""Storefront router — public, per-business ordering endpoints."""
from fastapi import APIRouter, HTTPException, Depends

import db

router = APIRouter(prefix="/s", tags=["storefront"])


def get_conn():
    conn = db.get_conn()
    try:
        yield conn
    finally:
        conn.close()


@router.get("/{slug}")
def storefront(slug: str, conn=Depends(get_conn)):
    acc = conn.execute(
        "SELECT * FROM accounts WHERE slug=? AND status='active'", (slug,)
    ).fetchone()
    if not acc:
        raise HTTPException(404, "Business not found")
    cats = conn.execute(
        "SELECT * FROM categories WHERE account_id=? ORDER BY sort_order", (acc["id"],)
    ).fetchall()
    items = conn.execute(
        """SELECT mi.*, c.name AS category_name FROM menu_items mi
           LEFT JOIN categories c ON c.id = mi.category_id
           WHERE mi.account_id=? AND mi.available=1 ORDER BY c.sort_order, mi.sort_order""",
        (acc["id"],),
    ).fetchall()
    return {
        "business": dict(acc),
        "categories": [dict(c) for c in cats],
        "items": [dict(i) for i in items],
    }


@router.post("/{slug}/order")
def place_order(slug: str, payload: dict, conn=Depends(get_conn)):
    acc = conn.execute(
        "SELECT * FROM accounts WHERE slug=? AND status='active'", (slug,)
    ).fetchone()
    if not acc:
        raise HTTPException(404, "Business not found")

    items = payload.get("items", [])
    if not items:
        raise HTTPException(400, "No items")

    subtotal = 0
    for it in items:
        row = conn.execute(
            "SELECT * FROM menu_items WHERE id=? AND account_id=? AND available=1",
            (it.get("id"), acc["id"]),
        ).fetchone()
        if not row:
            raise HTTPException(400, f"Item {it.get('id')} unavailable")
        qty = max(1, int(it.get("quantity", 1)))
        subtotal += row["price_cents"] * qty

    tax = round(subtotal * 0.0)  # TODO: wire tax by locale (reuse CDTFA logic)
    total = subtotal + tax

    order_ref = f"{slug[:3].upper()}-{acc['id'] * 1000 + (conn.execute('SELECT COUNT(*) c FROM orders').fetchone()['c'] + 1)}"

    cur = conn.execute(
        """INSERT INTO orders (account_id, order_ref, customer_name, customer_phone,
           customer_email, subtotal_cents, tax_cents, total_cents, pickup_time, note)
           VALUES (?,?,?,?,?,?,?,?,?,?)""",
        (acc["id"], order_ref, payload.get("name"), payload.get("phone"),
         payload.get("email"), subtotal, tax, total,
         payload.get("pickup_time"), payload.get("note", "")),
    )
    order_id = cur.lastrowid
    for it in items:
        row = conn.execute(
            "SELECT * FROM menu_items WHERE id=?", (it["id"],)
        ).fetchone()
        qty = max(1, int(it.get("quantity", 1)))
        conn.execute(
            "INSERT INTO order_items (order_id, item_name, unit_price_cents, quantity) VALUES (?,?,?,?)",
            (order_id, row["name"], row["price_cents"], qty),
        )
    conn.commit()

    # Create payment intent + record payout split
    import money
    pi = money.create_payment_intent(dict(acc), total, order_ref)
    conn.execute(
        "UPDATE orders SET stripe_payment_intent=? WHERE id=?", (pi["id"], order_id)
    )
    money.record_payout(conn, order_id, acc["id"], total, acc["rep_id"])

    return {
        "order_id": order_id,
        "order_ref": order_ref,
        "subtotal_cents": subtotal,
        "tax_cents": tax,
        "total_cents": total,
        "payment_intent": pi,
    }
