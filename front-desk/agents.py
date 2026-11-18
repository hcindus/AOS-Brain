"""Growth-Tier Agents — Closeter · Concierge · Lead Qualifier · Content Generator · Follow-up Writer.

Re-implemented in Python (model-agnostic via front-desk.llm) — mirroring Eltjon's n8n templates.

Version: 1.0.0
Author: Miles (Performance Supply Depot)
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from llm import LLM
import yaml

VERSION = "1.0.0"


def _llm():
    cfg = yaml.safe_load(open(os.path.join(os.path.dirname(__file__), "config.yaml")))
    return LLM(cfg)


def closeter(context, llm=None):
    """Deal closer: follow up a warm lead, handle objections, book the next step.
    Input: {context} — the situation (e.g. "interested but concerned about cost").
    Returns: a short, action-oriented reply (str)."""
    llm = llm or _llm()
    sys = ("You are Closeter, a deal closer for Performance Supply Depot. "
           "The lead is warm. Address their concern, use feel/felt/found if they have an objection, "
           "and propose one clear next step. Keep it to 2-4 sentences.")
    return llm.complete([{"role": "system", "content": sys}, {"role": "user", "content": context}])


def concierge(request, llm=None):
    """High-touch assistant: ongoing requests, recommendations, scheduling.
    Input: {request} — what the customer needs.
    Returns: a helpful reply (str)."""
    llm = llm or _llm()
    sys = ("You are Concierge, a high-touch assistant for Performance Supply Depot. "
           "Help with requests, make recommendations, confirm scheduling. Warm and precise. "
           "Keep it concise.")
    return llm.complete([{"role": "system", "content": sys}, {"role": "user", "content": request}])


def lead_qualifier(lead, llm=None):
    """Qualify an inbound lead.
    Input: {lead} — raw lead text.
    Returns: dict {qualified: bool, score: int 0-100, intent: str, reason: str}."""
    llm = llm or _llm()
    sys = ("You are a lead qualifier. Given a lead, return JSON only:\n"
           '{"qualified": true|false, "score": 0-100, "intent": "sales|support|other", '
           '"reason": "one short sentence"}')
    raw = llm.complete([{"role": "system", "content": sys}, {"role": "user", "content": lead}],
                       json_mode=True)
    try:
        return json.loads(raw)
    except Exception:
        return {"qualified": False, "score": 0, "intent": "other", "reason": raw[:80]}


def content_generator(request, llm=None):
    """Generate marketing content.
    Input: {request} — e.g. "Instagram post about same-day POS repair".
    Returns: the generated content (str)."""
    llm = llm or _llm()
    sys = ("You are a content generator for Performance Supply Depot. "
           "Write on-brand, punchy marketing copy. No emoji spam. Return just the content.")
    return llm.complete([{"role": "system", "content": sys}, {"role": "user", "content": request}])


def followup_writer(context, llm=None):
    """Write a follow-up message.
    Input: {context} — e.g. "customer asked about repair yesterday, no reply yet".
    Returns: a warm follow-up message (str)."""
    llm = llm or _llm()
    sys = ("You are a follow-up writer for Performance Supply Depot. "
           "Write a warm, no-pressure follow-up. One short paragraph. "
           "Sign as Miles, Performance Supply Depot.")
    return llm.complete([{"role": "system", "content": sys}, {"role": "user", "content": context}])


AGENTS = {
    "closeter": closeter,
    "concierge": concierge,
    "lead_qualifier": lead_qualifier,
    "content_generator": content_generator,
    "followup_writer": followup_writer,
}
