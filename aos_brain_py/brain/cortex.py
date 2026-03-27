# brain/cortex.py
"""
Cortex - language and reasoning module.
Wraps TinyLlama/Qwen for grammar, semantics, and expression.
"""

from typing import Optional, Dict, Any, List
import json


class Cortex:
    """
    Cortical language module.
    
    Provides:
    - Natural language generation
    - Structured output (JSON)
    - Grammar and syntax
    - Semantic enrichment via lexicon
    """
    
    def __init__(self, model_path: Optional[str] = None, use_qwen: bool = False):
        """
        Initialize cortex.
        
        Args:
            model_path: Path to GGUF model (optional - will use stub if not provided)
            use_qwen: Use Qwen instead of TinyLlama
        """
        self.model_path = model_path
        self.use_qwen = use_qwen
        self.model = None
        
        # Try to load model if path provided
        if model_path:
            try:
                from brain.models.tinyllama_local import TinyLlamaLocal, QwenLocal
                if use_qwen:
                    self.model = QwenLocal(model_path=model_path)
                else:
                    self.model = TinyLlamaLocal(model_path=model_path)
            except Exception as e:
                print(f"[Cortex] Warning: Could not load model: {e}")
                print("[Cortex] Using stub mode")
    
    def to_language(self, plan: Any, mode: str = "Analytical", 
                    context: Optional[Dict] = None) -> str:
        """
        Convert internal plan to natural language.
        
        Args:
            plan: Internal plan structure
            mode: QMD mode (affects style)
            context: Optional context dict
            
        Returns:
            Natural language expression of the plan
        """
        # Build prompt based on mode
        style = self._get_mode_style(mode)
        
        prompt = f"""You are the language cortex of a ternary brain.
Mode: {mode}
Style: {style}

Convert this internal plan into clear, natural language:

Plan: {json.dumps(plan, indent=2)}

Express this as:"""
        
        # Generate or use stub
        if self.model and hasattr(self.model, 'generate'):
            try:
                return self.model.generate(prompt, max_tokens=200)
            except:
                pass
        
        # Fallback: structured stub response
        return self._stub_response(plan, mode)
    
    def to_json(self, thought: Dict) -> str:
        """
        Convert thought to structured JSON.
        
        For tool calls, API responses, etc.
        """
        try:
            return json.dumps({
                "action": thought.get("decision", {}).get("intent", "noop"),
                "reason": thought.get("language", "")[:100],
                "mode": thought.get("mode", "Unknown"),
                "ternary": thought.get("ternary_code", [0, 0, 0, 0, 0]),
            })
        except:
            return '{"action": "noop", "reason": "json_error"}'
    
    def _get_mode_style(self, mode: str) -> str:
        """Get language style description for mode."""
        styles = {
            "Analytical": "precise, logical, step-by-step reasoning",
            "Creative": "divergent, associative, imaginative",
            "Cautious": "careful, risk-aware, hedging",
            "Exploratory": "curious, questioning, open-ended",
            "Reflective": "introspective, memory-oriented, calm",
            "Directive": "action-focused, imperative, minimal",
            "Emotional": "expressive, value-weighted, warm",
            "Minimal": "terse, efficient, low-word",
            "Verbose": "expanded, explanatory, detailed",
        }
        return styles.get(mode, "clear and natural")
    
    def _stub_response(self, plan: Any, mode: str) -> str:
        """Generate stub response when no model available."""
        # Mode-aware stub
        intros = {
            "Analytical": "Based on analysis",
            "Creative": "Considering possibilities",
            "Cautious": "Proceeding carefully",
            "Exploratory": "Exploring options",
            "Reflective": "Reflecting on this",
            "Directive": "Executing plan",
            "Emotional": "Feeling that",
            "Minimal": "Action:",
            "Verbose": "It seems to me that",
        }
        intro = intros.get(mode, "I think")
        
        # Extract action from plan if possible
        action = "continue"
        if isinstance(plan, dict):
            action = plan.get("intent", plan.get("tool", "continue"))
        elif isinstance(plan, list) and plan:
            action = str(plan[0]) if plan else "continue"
        
        return f"[{mode}] {intro}: {action}"


class QMDAwareCortex(Cortex):
    """
    Cortex that adjusts expression based on QMD mode.
    """
    
    MODE_PROMPTS = {
        "Analytical": "Provide a logical, structured analysis.",
        "Creative": "Explore creative possibilities and connections.",
        "Cautious": "Consider risks and proceed with care.",
        "Exploratory": "Ask questions and investigate openly.",
        "Reflective": "Look inward and consider past experience.",
        "Directive": "State clear actions and next steps.",
        "Emotional": "Express feelings and values honestly.",
        "Minimal": "Be brief and to the point.",
        "Verbose": "Explain thoroughly with examples.",
    }
    
    def express_thought(self, thought: Dict, mode: str) -> str:
        """
        Express a complete thought with QMD-aware styling.
        """
        base = self.to_language(thought.get("plan", {}), mode)
        
        # Add emotional coloring if applicable
        if mode == "Emotional":
            valence = thought.get("value", {}).get("valence", 0)
            if valence > 0.3:
                base = f"(positively) {base}"
            elif valence < -0.3:
                base = f"(concerned) {base}"
        
        return base
