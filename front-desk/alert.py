"""Structured dispatch — send the route to an agent inbox (Telegram now; extensible)."""
import requests


class Alert:
    def __init__(self, cfg):
        a = cfg.get("alert", {})
        self.bot_token = _expand(a.get("telegram_bot_token", ""))
        self.chat_id = _expand(a.get("telegram_chat_id", ""))

    def dispatch(self, event, route):
        """Notify the routed agent(s). Returns True if sent."""
        if not self.bot_token or not self.chat_id:
            return False
        text = (
            f"🔔 Front-desk inbound\n"
            f"To: {', '.join(route.agents)}\n"
            f"Intent: {route.intent} · Urgency: {route.urgency} · Qualified: {route.qualified}\n"
            f"From: {event.from_} ({event.channel})\n"
            f"Entity: {_entity_str(route.entity)}\n"
            f"Summary: {route.summary}"
        )
        try:
            requests.post(
                f"https://api.telegram.org/bot{self.bot_token}/sendMessage",
                json={"chat_id": self.chat_id, "text": text}, timeout=10)
            return True
        except Exception:
            return False


def _entity_str(entity):
    if not entity:
        return "(none)"
    parts = []
    for k in ("name", "business", "phone", "email"):
        if entity.get(k):
            parts.append(f"{k}={entity[k]}")
    return ", ".join(parts) or "(none)"


def _expand(s):
    import os, re
    def rep(m):
        name, _, default = m.group(1).partition(":-")
        return os.environ.get(name, default or "")
    return re.sub(r"\$\{([^}]+)\}", rep, str(s))
