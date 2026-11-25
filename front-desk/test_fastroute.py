"""Offline test for the deterministic fast-path — no DB, no LLM, no network."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastroute import fast_intent, extract_entity

samples = [
    "Hi, I need a quote for thermal paper for my restaurant.",
    "Our receipt printer is broken and we need a technician ASAP.",
    "Can you send me a copy of our contract for legal review?",
    "buy followers now cheap!!! click here",
    "I'm applying for the open sales position.",
    "Where is my order? It's been in transit for a week.",
    "There's been a security breach, call me at 555-123-4567 immediately.",
    "Just browsing, thanks anyway.",
]

for body in samples:
    fast = fast_intent(body)
    ent = extract_entity(body)
    if fast:
        i, u, q = fast
        print(f"FAST  [{i:9}] urgen={u:6} qual={q:8} entity={ent}  <- {body[:55]}")
    else:
        print(f"LLM   (no keyword match)                    entity={ent}  <- {body[:55]}")
