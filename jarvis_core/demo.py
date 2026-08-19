#!/usr/bin/env python3
"""End-to-end demo: create a lead → generate a quote PDF → test the PIN gate."""
from jarvis_core import LeadsStore, QuoteEngine, InvoiceEngine, PinGate


def main():
    print("=" * 60)
    print("JARVIS CORE — Performance Supply Depot (Phase 1)")
    print("=" * 60)

    # 1. Leads table
    store = LeadsStore()
    lead_id = store.add(
        name="John Doe", email="john@gmail.com", phone="510-796-9193",
        business="Oil Change Shop", product="AI Reputation Build", value=2500.0,
        notes="50% deposit to book; 50% on delivery",
    )
    lead = store.get(lead_id)
    print(f"\n✅ Lead #{lead_id} created: {lead['name']} — {lead['product']}")

    # 2. Quote PDF
    items = [
        ("AI Reputation Builder — setup & configuration", 1, 2000.0),
        ("Onboarding & staff training", 1, 500.0),
    ]
    quote_path = QuoteEngine().generate(lead, items)
    print(f"✅ Quote PDF → {quote_path}")

    # 3. Invoice PDF
    inv_path = InvoiceEngine().generate(lead, items)
    print(f"✅ Invoice PDF → {inv_path}")

    # 4. PIN gate
    gate = PinGate()
    print("\n--- PIN gate test ---")
    for code in ["1123", "9999"]:
        ok, msg = gate.check(code)
        print(f"  code {code}: {msg}")

    # 5. Query leads
    print("\n--- Leads table ---")
    for r in store.all():
        print(f"  [{r['status']:>6}] {r['name']:<12} {r['product']:<22} ${r['value']:,.2f}")


if __name__ == "__main__":
    main()
