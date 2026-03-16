import json
import re

class CerebellumAgent:
    def __init__(self, cfg):
        self.cfg = cfg

    def format(self, plan):
        """
        Parse PFC plan output and format into executable action.
        Extracts JSON from raw text if present.
        """
        raw = plan.get("raw", "noop") if isinstance(plan, dict) else str(plan)
        
        # Try to extract JSON from the raw text
        action_type = "noop"
        action_reason = "No explicit reason provided"
        
        # Look for JSON in the response
        try:
            # Find JSON block if present
            json_match = re.search(r'\{[^}]+\}', raw)
            if json_match:
                parsed = json.loads(json_match.group())
                action_type = parsed.get("action", "noop")
                action_reason = parsed.get("reason", action_reason)
            else:
                # Check if raw is just a simple action word
                clean = raw.strip().lower()
                if clean in ["noop", "act", "halt", "wait", "query"]:
                    action_type = clean
                    action_reason = f"PFC suggested: {clean}"
        except (json.JSONDecodeError, AttributeError):
            # Fallback: use raw as reason
            action_reason = raw[:200] if len(raw) > 200 else raw
        
        return {
            "type": action_type,
            "plan": plan,
            "reason": action_reason,
            "parsed": True
        }
