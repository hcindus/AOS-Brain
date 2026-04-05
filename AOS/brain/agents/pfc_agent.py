import requests

class PFCAgent:
    def __init__(self, cfg):
        self.cfg = cfg
        self.backend = cfg["models"]["backend"]
        self.ollama_model = cfg["models"]["ollama"]["pfc_left"]
        # Load fallback models from config
        self.fallback_models = cfg["models"].get("fallbacks", [])
        # Parse fallback models (remove "ollama:" prefix)
        self.fallbacks = []
        for fb in self.fallback_models:
            if fb.startswith("ollama:"):
                self.fallbacks.append(fb.replace("ollama:", ""))
            else:
                self.fallbacks.append(fb)

    def _ollama_chat(self, prompt: str, model: str = None) -> str:
        """Call Ollama with fallback support."""
        target_model = model or self.ollama_model
        
        try:
            resp = requests.post(
                "http://localhost:11434/api/generate",
                json={"model": target_model, "prompt": prompt, "stream": False},
                timeout=60,
            )
            resp.raise_for_status()
            return resp.json().get("response", "").strip()
        except Exception as e:
            return f"{{\"raw\": \"error\", \"reason\": \"{str(e)}\"}}"

    def _ollama_chat_with_fallback(self, prompt: str) -> str:
        """Try primary model, then fallbacks if needed."""
        # Try primary model first
        result = self._ollama_chat(prompt, self.ollama_model)
        
        # Check if primary failed
        if '"error"' in result or result.startswith('{"raw": "error"'):
            print(f"[PFC] Primary model {self.ollama_model} failed, trying fallbacks...")
            
            # Try each fallback model
            for fallback_model in self.fallbacks:
                try:
                    print(f"[PFC] Trying fallback: {fallback_model}")
                    fb_result = self._ollama_chat(prompt, fallback_model)
                    
                    # Check if fallback succeeded
                    if '"error"' not in fb_result and not fb_result.startswith('{"raw": "error"'):
                        print(f"[PFC] Fallback {fallback_model} succeeded")
                        return fb_result
                        
                except Exception as e:
                    print(f"[PFC] Fallback {fallback_model} failed: {e}")
                    continue
            
            # All fallbacks failed
            print("[PFC] All fallback models exhausted")
            return result  # Return original error
        
        return result

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
            # Use fallback-enabled chat method
            text = self._ollama_chat_with_fallback(prompt)
            return {"raw": text}
        else:
            # GGUF path would call a local runner; stub for now
            return {"raw": "noop", "reason": "gguf_stub"}
