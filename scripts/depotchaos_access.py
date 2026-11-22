#!/usr/bin/env python3
"""
DepotChaos Access Layer — unified, documented interface for AGI Company agents
(Sales team + others) to access DepotChaos and work new & existing leads.

Databases:
  LEADS_DB = data/depot_chaos/unified.db   -> `leads` table (34K+ leads)
  CRM_DB   = DepotChaos/depot_chaos.db     -> `vendors`, `sales_contacts`,
                                             `psd_clients`, `psd_client_products`

Usage (import from any agent sandbox or script):
    import sys; sys.path.insert(0, '/root/.openclaw/workspace/scripts')
    import depotchaos_access as dc

    dc.list_leads(status='new', limit=10)      # new unassigned leads
    dc.claim_lead(70210, 'Jane')               # assign a lead to an agent
    dc.update_lead(70210, status='contacted', notes='Left voicemail')
    dc.log_contact(70210, 'Jane', 'voicemail', 'no answer')
    dc.stats('Jane')                           # agent's pipeline summary
    dc.get_customer_history(name='Piedmont')   # customer + purchase history

Also usable as a CLI:  python3 depotchaos_access.py stats [agent]
"""
import sqlite3
from datetime import datetime, timezone

LEADS_DB = "/root/.openclaw/workspace/data/depot_chaos/unified.db"
CRM_DB = "/root/.openclaw/workspace/DepotChaos/depot_chaos.db"

# Synthetic / demo databases (kept separate from live).
LEADS_DB_DEMO = "/root/.openclaw/workspace/data/depot_chaos/unified_demo.db"
CRM_DB_DEMO = "/root/.openclaw/workspace/DepotChaos/depot_chaos_demo.db"

_DEMO = False


def use_demo(on=True):
    """Switch the access layer to the demo (synthetic) databases. Returns new state."""
    global _DEMO
    _DEMO = bool(on)
    return _DEMO


def _leads_db():
    return LEADS_DB_DEMO if _DEMO else LEADS_DB


def _crm_db():
    return CRM_DB_DEMO if _DEMO else CRM_DB


def _conn(db):
    con = sqlite3.connect(db)
    con.row_factory = sqlite3.Row
    return con


def _now():
    return datetime.now(timezone.utc).isoformat()


# ---------------------------------------------------------------- LEADS

def list_leads(agent=None, status='new', limit=50, priority=None, city=None):
    """List leads. Filter by assigned agent, status, priority, city."""
    q = ("SELECT id, business_name, city, state, phone, email, business_type, "
         "status, tier, priority, assigned_agent, last_contact, next_contact, notes "
         "FROM leads WHERE deleted=0")
    args = []
    if agent:
        q += " AND assigned_agent=?"; args.append(agent)
    if status:
        q += " AND status=?"; args.append(status)
    if priority:
        q += " AND priority=?"; args.append(priority)
    if city:
        q += " AND city LIKE ?"; args.append(f"%{city}%")
    q += " ORDER BY id DESC LIMIT ?"; args.append(limit)
    con = _conn(_leads_db())
    rows = [dict(r) for r in con.execute(q, args).fetchall()]
    con.close()
    return rows


def get_lead(lead_id):
    con = _conn(_leads_db())
    r = con.execute("SELECT * FROM leads WHERE id=?", (lead_id,)).fetchone()
    con.close()
    return dict(r) if r else None


def claim_lead(lead_id, agent):
    """Assign a lead to an agent (idempotent). Sets assigned_agent + last_contact."""
    con = _conn(_leads_db())
    con.execute(
        "UPDATE leads SET assigned_agent=?, last_contact=COALESCE(last_contact, ?) WHERE id=?",
        (agent, _now(), lead_id))
    con.commit(); con.close()
    return get_lead(lead_id)


_UNSET = object()

def update_lead(lead_id, status=_UNSET, notes=_UNSET, priority=_UNSET, tier=_UNSET,
                next_contact=_UNSET, assigned_agent=_UNSET, **extra):
    """Update lead fields. Pass None to explicitly clear a field. Returns updated lead."""
    fields = {}
    if status is not _UNSET: fields['status'] = status
    if notes is not _UNSET: fields['notes'] = notes
    if priority is not _UNSET: fields['priority'] = priority
    if tier is not _UNSET: fields['tier'] = tier
    if next_contact is not _UNSET: fields['next_contact'] = next_contact
    if assigned_agent is not _UNSET: fields['assigned_agent'] = assigned_agent
    fields.update(extra)
    if not fields:
        return get_lead(lead_id)
    setq = ", ".join(f"{k}=?" for k in fields)
    con = _conn(_leads_db())
    con.execute(f"UPDATE leads SET {setq} WHERE id=?", (*fields.values(), lead_id))
    con.commit(); con.close()
    return get_lead(lead_id)


def stats(agent=None):
    """Pipeline summary. If agent given, break down that agent's leads by status."""
    con = _conn(_leads_db())
    if agent:
        rows = con.execute(
            "SELECT status, COUNT(*) FROM leads WHERE assigned_agent=? GROUP BY status",
            (agent,)).fetchall()
    else:
        rows = con.execute("SELECT status, COUNT(*) FROM leads GROUP BY status").fetchall()
    con.close()
    return {r[0] or '(blank)': r[1] for r in rows}


# ---------------------------------------------------------------- CONTACTS

def log_contact(lead_id, agent, outcome, notes="", want_prices=None):
    """Log an interaction to the CRM (sales_contacts), keyed to a lead."""
    lead = get_lead(lead_id)
    name = lead.get("business_name") if lead else None
    con = _conn(_crm_db())
    con.execute(
        "INSERT INTO sales_contacts (lead_name, contact_type, channel, outcome, want_prices, notes, contacted_at) "
        "VALUES (?,?,?,?,?,?,?)",
        (name or f"lead#{lead_id}", "lead", "agent", outcome, want_prices, notes, _now()))
    con.commit(); con.close()
    return True


# ---------------------------------------------------------------- CUSTOMERS

def get_customer_history(name=None, phone=None, limit=20):
    """Look up customers (+ product history) in DepotChaos. Returns list of client rows."""
    con = _conn(_crm_db())
    q = "SELECT * FROM psd_clients WHERE 1=1"
    args = []
    if name:
        q += " AND name LIKE ?"; args.append(f"%{name}%")
    if phone:
        q += " AND (contact_phone LIKE ? OR bill_phone LIKE ?)"; args += [f"%{phone}%", f"%{phone}%"]
    q += " LIMIT ?"; args.append(limit)
    rows = [dict(r) for r in con.execute(q, args).fetchall()]
    con.close()
    return rows


def get_customer_products(client_id):
    """Purchase history (paper/ribbon/label) for a psd_clients id."""
    con = _conn(_crm_db())
    rows = [dict(r) for r in con.execute(
        "SELECT category, slot, sku, raw, desc, status FROM psd_client_products "
        "WHERE client_id=? ORDER BY category, slot", (client_id,)).fetchall()]
    con.close()
    return rows


# ---------------------------------------------------------------- CLI

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(0)
    cmd = sys.argv[1]
    if cmd == "stats":
        print(stats(sys.argv[2] if len(sys.argv) > 2 else None))
    elif cmd == "list":
        print(json.dumps(list_leads(
            agent=sys.argv[2] if len(sys.argv) > 2 else None,
            status=sys.argv[3] if len(sys.argv) > 3 else 'new',
            limit=int(sys.argv[4]) if len(sys.argv) > 4 else 10), indent=2, default=str))
    elif cmd == "claim":
        print(json.dumps(claim_lead(int(sys.argv[2]), sys.argv[3]), indent=2, default=str))
    elif cmd == "update":
        print(json.dumps(update_lead(int(sys.argv[2]), status=sys.argv[3]), indent=2, default=str))
    elif cmd == "customer":
        print(json.dumps(get_customer_history(name=sys.argv[2] if len(sys.argv) > 2 else None), indent=2, default=str))
