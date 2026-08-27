"""Stripe webhook — turns a PaymentIntent into a paid order + settled payout + notifications.

Handles:
  - payment_intent.succeeded  -> mark order 'paid', settle payout, fire notifications
  - payment_intent.payment_failed -> mark order 'cancelled'
"""
from fastapi import APIRouter, Request, HTTPException
import json

import db
import config
import notify

router = APIRouter(prefix="/webhook", tags=["webhook"])


def _settle_order(conn, order_id: int):
    """Mark payout settled + order paid."""
    conn.execute("UPDATE payouts SET settled=1 WHERE order_id=?", (order_id,))
    conn.execute("UPDATE orders SET status='paid' WHERE id=?", (order_id,))
    conn.commit()


def _fire_notifications(conn, order_id: int, account_id: int):
    """Send order notifications to the business on the configured channels."""
    order = conn.execute("SELECT * FROM orders WHERE id=?", (order_id,)).fetchone()
    acc = conn.execute("SELECT * FROM accounts WHERE id=?", (account_id,)).fetchone()
    if not order or not acc:
        return

    items = conn.execute(
        "SELECT * FROM order_items WHERE order_id=?", (order_id,)
    ).fetchall()

    line_items = "\n".join(
        f"  {i['quantity']}x {i['item_name']} — ${i['unit_price_cents']*i['quantity']/100:.2f}"
        for i in items
    )
    total = f"${order['total_cents']/100:.2f}"
    subject = f"New order {order['order_ref']} — {total}"
    body = (
        f"NEW PICKUP ORDER\n"
        f"Order: {order['order_ref']}\n"
        f"Customer: {order['customer_name']} ({order['customer_phone'] or 'no phone'})\n"
        f"Pickup: {order['pickup_time'] or 'ASAP'}\n\n"
        f"{line_items}\n\n"
        f"TOTAL: {total}\n"
        f"{('Note: ' + order['note']) if order['note'] else ''}"
    )

    results = []

    # Email
    if acc["email"]:
        r = notify.send_email(acc["email"], subject, body.replace("\n", "<br>"))
        results.append(("email", r))

    # SMS
    if acc["phone"]:
        r = notify.send_sms(acc["phone"], body)
        results.append(("sms", r))

    # Log notification attempts
    for channel, r in results:
        conn.execute(
            "INSERT INTO notifications (account_id, order_id, channel, target, status, detail) VALUES (?,?,?,?,?,?)",
            (account_id, order_id, channel, acc["email"] if channel == "email" else acc["phone"],
             "sent" if r.get("ok") else "failed", r.get("error", "")),
        )
    conn.commit()
    return results


@router.post("/stripe")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig = request.headers.get("stripe-signature", "")

    if config.STRIPE_SECRET_KEY and config.STRIPE_WEBHOOK_SECRET:
        try:
            import stripe
            event = stripe.Webhook.construct_event(
                payload, sig, config.STRIPE_WEBHOOK_SECRET
            )
        except Exception as e:
            raise HTTPException(400, f"Invalid signature: {e}")
    else:
        # Dev mode — no signature verification, parse raw body.
        try:
            event = json.loads(payload)
        except Exception:
            raise HTTPException(400, "Bad payload")

    etype = event.get("type")
    data = event.get("data", {}).get("object", {})
    order_ref = (data.get("metadata") or {}).get("order_ref", "")

    if not order_ref:
        return {"ok": True, "ignored": "no order_ref"}

    conn = db.get_conn()
    try:
        order = conn.execute(
            "SELECT * FROM orders WHERE order_ref=?", (order_ref,)
        ).fetchone()
        if not order:
            return {"ok": True, "ignored": "unknown order_ref"}

        if etype == "payment_intent.succeeded":
            _settle_order(conn, order["id"])
            notif = _fire_notifications(conn, order["id"], order["account_id"])
            return {"ok": True, "order_ref": order_ref, "status": "paid", "notifications": notif}

        if etype == "payment_intent.payment_failed":
            conn.execute("UPDATE orders SET status='cancelled' WHERE id=?", (order["id"],))
            conn.commit()
            return {"ok": True, "order_ref": order_ref, "status": "cancelled"}

        return {"ok": True, "ignored": etype}
    finally:
        conn.close()
