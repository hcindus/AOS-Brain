"""Deterministic fast-path intake — keyword intent + regex entity extraction.

Bottled from the Frontline n8n "Pick Agent" pattern: route obvious intents with a
regex before spending an LLM call. Cheap, instant, explainable. Falls back to the LLM
classifier (engine.classify) when nothing matches.

Pure functions — no DB, no LLM, no network, no side effects. Safe to import and test.
"""
import re

# intent -> keyword pattern (case-insensitive). Order matters: first match wins.
KEYWORD_INTENTS = [
    ("hr",       r"\b(applying|apply|job|position|employment|hiring|hired|resume|\bcv\b|career|open role|vacancy)\b"),
    ("legal",    r"\b(contract|legal|compliance|attorney|lawyer|nda|liability|terms|arbitration|lawsuit)\b"),
    ("security", r"\b(breach|threat|hacked|hack|intrusion|ransomware|phishing|compromised|unauthorized)\b"),
    ("logistics",r"\b(shipping|delivery|shipment|tracking|in transit|where is my order|out for delivery)\b"),
    ("sales",    r"\b(quote|pricing|price|cost|how much|buy|purchase|order|interested in|bulk|wholesale)\b"),
    ("support",  r"\b(broken|repair|technician|not working|issue|fix|replace|malfunction|defective|error|down)\b"),
]

# obvious spam / solicitation -> qualified=spam, intent=other
SPAM_RE = re.compile(
    r"\b(followers|buy.*(followers|likes)|cheap.*(?!printer|paper|ribbon)|click here|"
    r"winner|congratulations|free (money|bitcoin|crypto)|casino|viagra|work from home.*\\$\\d{3,})\b"
)

URGENT_RE = re.compile(r"\b(asap|urgent|emergency|immediately|right now|today|stat)\b")

PHONE_RE = re.compile(r"(\+?\d[\d\s().\-]{7,}\d)")
EMAIL_RE = re.compile(r"([\w.+-]+@[\w-]+\.[\w.-]+)")


def fast_intent(text):
    """Return (intent, urgency, qualified) or None if no confident keyword match."""
    t = (text or "").lower()
    if SPAM_RE.search(t):
        return ("other", "normal", "spam")
    for intent, pat in KEYWORD_INTENTS:
        if re.search(pat, t):
            urgency = "high" if URGENT_RE.search(t) else "normal"
            qualified = "lead" if intent in ("sales", "support", "logistics") else "unknown"
            return (intent, urgency, qualified)
    return None


def extract_entity(text):
    """Best-effort entity extraction via regex (phone + email only)."""
    entity = {}
    m = PHONE_RE.search(text or "")
    if m:
        entity["phone"] = m.group(1).strip()
    m = EMAIL_RE.search(text or "")
    if m:
        entity["email"] = m.group(1).strip()
    return entity
