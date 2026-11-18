"""InboundEvent -> structured Route (the intent engine). Model-agnostic."""
import json
from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone

from llm import LLM
from router import Router


@dataclass
class InboundEvent:
    channel: str          # voice / email / text / web / dm
    from_: str            # phone number or email or handle
    body: str             # the raw message / transcript
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class Route:
    intent: str
    urgency: str          # low / normal / high
    entity: dict          # {name, business, phone, email}
    qualified: str        # lead / support / spam / unknown
    agents: list
    summary: str


SYSTEM = (
    "You are a front-desk intake classifier. Given an inbound message, return JSON only:\n"
    '{"intent": "sales|support|hr|legal|security|logistics|other", '
    '"urgency": "low|normal|high", '
    '"entity": {"name": "", "business": "", "phone": "", "email": ""}, '
    '"qualified": "lead|support|spam|unknown", '
    '"summary": "one short sentence"}\n\n'
    "Intent rules:\n"
    "- 'applying for a job / position / employment' = hr (NOT sales, even if the job is 'sales')\n"
    "- 'contract / legal review / compliance' = legal (NOT sales or support)\n"
    "- 'want to buy / quote / order / pricing' = sales\n"
    "- 'broken / repair / technician / help' = support\n"
    "- 'shipping / delivery / where is my order' = logistics\n"
    "- 'breach / threat / hacked / security' = security\n"
    "- obvious spam or solicitation = other, qualified=spam\n\n"
    "Extract any name/business/phone/email you can find. Be conservative — leave blank if unknown."
)


class Engine:
    def __init__(self, cfg=None):
        import yaml, os
        if cfg is None:
            cfg = yaml.safe_load(open(os.path.join(os.path.dirname(__file__), "config.yaml")))
        self.llm = LLM(cfg)
        self.router = Router(cfg)

    def classify(self, event: InboundEvent) -> Route:
        msg = f"[channel: {event.channel}] [from: {event.from_}]\n{event.body}"
        raw = self.llm.complete([
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": msg},
        ], json_mode=True)
        try:
            d = json.loads(raw)
        except Exception:
            d = {"intent": "other", "urgency": "normal", "entity": {}, "qualified": "unknown", "summary": raw[:80]}
        intent = (d.get("intent") or "other").lower()
        agents = self.router.route(intent)
        return Route(
            intent=intent,
            urgency=(d.get("urgency") or "normal").lower(),
            entity=d.get("entity") or {},
            qualified=(d.get("qualified") or "unknown").lower(),
            agents=agents,
            summary=d.get("summary") or "",
        )
