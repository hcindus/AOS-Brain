"""OrderPort money module — Stripe Connect split + payout ledger.

Revenue split: business 85% / company 10% / rep 5% (configurable in config.py).
"""
import config

try:
    import stripe
    STRIPE_AVAILABLE = True
except ImportError:
    stripe = None
    STRIPE_AVAILABLE = False


def split_amount(total_cents: int) -> dict:
    """Compute the three-way split for a single order total."""
    company_cents = round(total_cents * config.COMPANY_SHARE_BPS / 10000)
    rep_cents = round(total_cents * config.REP_SHARE_BPS / 10000)
    business_cents = total_cents - company_cents - rep_cents
    return {
        "total_cents": total_cents,
        "business_cents": business_cents,
        "company_cents": company_cents,
        "rep_cents": rep_cents,
    }


def create_payment_intent(account, total_cents: int, order_ref: str):
    """Create a Stripe PaymentIntent. If account has a Connect destination,
    use a destination charge so the business receives funds automatically."""
    if not STRIPE_AVAILABLE or not config.STRIPE_SECRET_KEY:
        # Development fallback — no real charge.
        return {"id": f"pi_dev_{order_ref}", "client_secret": None, "dev": True}

    stripe.api_key = config.STRIPE_SECRET_KEY
    intent_kwargs = {
        "amount": total_cents,
        "currency": "usd",
        "metadata": {"order_ref": order_ref, "account_id": account["id"]},
        "automatic_payment_methods": {"enabled": True},
    }
    if account.get("stripe_account_id"):
        intent_kwargs["transfer_data"] = {
            "destination": account["stripe_account_id"],
        }
    intent = stripe.PaymentIntent.create(**intent_kwargs)
    return {"id": intent.id, "client_secret": intent.client_secret, "dev": False}


def record_payout(conn, order_id: int, account_id: int, total_cents: int, rep_id):
    s = split_amount(total_cents)
    conn.execute(
        """INSERT INTO payouts
           (order_id, account_id, total_cents, business_cents, company_cents, rep_cents, rep_id)
           VALUES (?,?,?,?,?,?,?)""",
        (order_id, account_id, s["total_cents"], s["business_cents"],
         s["company_cents"], s["rep_cents"], rep_id),
    )
    conn.commit()
    return s
