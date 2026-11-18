"""Model-agnostic LLM client (OpenAI-compatible). Works with Ollama / DeepSeek / OpenAI / LM Studio."""
import os
import requests


class LLM:
    def __init__(self, cfg):
        c = cfg["llm"]
        self.base_url = _expand(c.get("base_url", "http://127.0.0.1:11434/v1")).rstrip("/")
        self.api_key = _expand(c.get("api_key", "ollama"))
        self.model = _expand(c.get("model", "antoniohudnall/Mort_II:latest"))
        self.temperature = c.get("temperature", 0.2)
        self.max_tokens = c.get("max_tokens", 300)
        self.timeout = c.get("timeout_seconds", 60)

    def complete(self, messages, json_mode=False):
        """Return the assistant text (or parsed JSON object if json_mode)."""
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }
        if json_mode:
            payload["response_format"] = {"type": "json_object"}
        headers = {"Authorization": f"Bearer {self.api_key}"}
        r = requests.post(f"{self.base_url}/chat/completions", json=payload,
                          headers=headers, timeout=self.timeout)
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"].strip()


def _expand(s):
    """Expand ${VAR:-default} env references in a config string."""
    import re
    def rep(m):
        name, _, default = m.group(1).partition(":-")
        return os.environ.get(name, default or "")
    return re.sub(r"\$\{([^}]+)\}", rep, str(s))
