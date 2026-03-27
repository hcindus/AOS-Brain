# brain/cortex.py
"""
Shared neural substrate (Cortex).
Can be dropped into multiple brains (original OODA, ternary OODA).
"""

from typing import Optional, Dict, Any
from brain.models.tinyllama_local import TinyLlamaLocal, QwenLocal


class Cortex:
    """
    Shared neural substrate.
    Drop-in module for both brains.
    """
    
    def __init__(self, model_path: str, use_qwen: bool = False):
        """
        Initialize cortex with model.
        
        Args:
            model_path: Path to GGUF model
            use_qwen: If True, use Qwen instead of TinyLlama
        """
        if use_qwen:
            self.engine = QwenLocal(model_path=model_path)
        else:
            self.engine = TinyLlamaLocal(model_path=model_path)
        
        self.stats = {
            "calls": 0,
            "total_tokens": 0,
        }
    
    def activate(
        self,
        prompt: str,
        max_tokens: int = 150,
        context: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Core neural call.
        Optionally enrich prompt with context.
        """
        if context:
            ctx_str = "\n".join(f"{k}: {v}" for k, v in context.items())
            full_prompt = f"[CONTEXT]\n{ctx_str}\n\n[INPUT]\n{prompt}"
        else:
            full_prompt = prompt
        
        result = self.engine.generate(full_prompt, max_tokens=max_tokens)
        
        self.stats["calls"] += 1
        self.stats["total_tokens"] += len(result.split())
        
        return result
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cortex usage stats."""
        return self.stats.copy()
