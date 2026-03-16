import requests

class PFCAgent:
    def __init__(self, cfg):
        self.cfg = cfg
        self.backend = cfg["models"]["backend"]
        self.ollama_model = cfg["models"]["ollama"]["pfc_left"]

    def _ollama_chat(self, prompt: str) -> str:
        try:
            resp = requests.post(
                "http://localhost:11434/api/generate",
                json={"model": self.ollama_model, "prompt": prompt, "stream": False},
                timeout=60,
            )
            resp.raise_for_status()
            return resp.json().get("response", "").strip()
        except Exception as e:
            return f"{{\"raw\": \"error\", \"reason\": \"{str(e)}\"}}"

    def plan(self, obs, ctx, affect):
        # Extract workspace memory if available
        memory_context = ""
        if ctx and isinstance(ctx, dict):
            wm = ctx.get("workspace_memory", {})
            if wm.get("queried") and wm.get("source_count", 0) > 0:
                results = wm.get("results", [])
                memory_snippets = []
                for r in results[:2]:  # Top 2 memories
                    text = r.get("text", "")[:150]
                    source = r.get("source", "unknown")
                    relevance = r.get("relevance", 0)
                    memory_snippets.append(f"[{source} rel:{relevance:.2f}] {text}")
                if memory_snippets:
                    memory_context = "\nRelevant memories:\n" + "\n".join(memory_snippets)
        
        prompt = f"""You are the PFC of AOS.
Input: {obs}
Context: {ctx}
{memory_context}
Mode: {affect.get('mode')}
Generate a short, safe plan in JSON with keys: action, reason.
"""
        if self.backend == "ollama":
            text = self._ollama_chat(prompt)
            return {"raw": text}
        else:
            # GGUF path would call a local runner; stub for now
            return {"raw": "noop", "reason": "gguf_stub"}
