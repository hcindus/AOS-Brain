"""Phase 0 validation — does the engine classify + route correctly?

Run: python3 validate.py
Feeds a few sample inbound messages and prints the classified Route for each.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from engine import Engine, InboundEvent
from store import Store
from alert import Alert
import yaml


def main():
    cfg = yaml.safe_load(open(os.path.join(os.path.dirname(__file__), "config.yaml")))
    engine = Engine(cfg)
    store = Store(cfg["store"]["db_path"])
    alert = Alert(cfg)

    samples = [
        ("voice", "+14155552671", "Hi, I need a quote for thermal paper for my restaurant."),
        ("email", "joe@diner.com", "Our receipt printer is broken and we need a technician ASAP."),
        ("text", "+12025550123", "Can you send me a copy of our contract for legal review?"),
        ("dm", "@random_spam", "buy followers now cheap!!! click here"),
        ("email", "hr@company.com", "I'm applying for the open sales position."),
    ]

    for channel, from_, body in samples:
        event = InboundEvent(channel=channel, from_=from_, body=body)
        route = engine.classify(event)
        store.log(event, route)
        alert.dispatch(event, route)
        print(f"\n[{channel}] {body}")
        print(f"  -> intent={route.intent} urgency={route.urgency} qualified={route.qualified} agents={route.agents}")
        print(f"     entity={route.entity} | {route.summary}")

    # repeat-contact history check
    hist = store.prior_contacts("+14155552671")
    print(f"\nPrior contacts for +14155552671: {len(hist)}")


if __name__ == "__main__":
    main()
