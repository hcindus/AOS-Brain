# brain/models/tinyllama_local.py
"""
Local TinyLlama wrapper using llama.cpp (via llama-cpp-python).
Fully offline. No HTTP. No API calls.
"""

try:
    from llama_cpp import Llama
    LLAMA_CPP_AVAILABLE = True
except ImportError:
    LLAMA_CPP_AVAILABLE = False
    print("[WARNING] llama-cpp-python not installed. Using stub.")


class TinyLlamaLocal:
    """
    Local TinyLlama wrapper using llama.cpp.
    Fully offline. No HTTP. No API calls.
    """
    
    def __init__(
        self,
        model_path: str,
        n_ctx: int = 4096,
        n_threads: int = 6,
        n_gpu_layers: int = 0,
        temperature: float = 0.7,
        top_p: float = 0.9,
    ):
        self.temperature = temperature
        self.top_p = top_p
        self.model_path = model_path
        
        if LLAMA_CPP_AVAILABLE:
            try:
                self.model = Llama(
                    model_path=model_path,
                    n_ctx=n_ctx,
                    n_threads=n_threads,
                    n_gpu_layers=n_gpu_layers,
                    verbose=False
                )
                self.available = True
            except Exception as e:
                print(f"[ERROR] Failed to load model: {e}")
                self.model = None
                self.available = False
        else:
            self.model = None
            self.available = False
    
    def generate(self, prompt: str, max_tokens: int = 150) -> str:
        """Generate a completion from TinyLlama."""
        if not self.available or self.model is None:
            # Return stub response for testing
            return self._stub_response(prompt)
        
        try:
            result = self.model(
                prompt,
                max_tokens=max_tokens,
                temperature=self.temperature,
                top_p=self.top_p,
                stop=["\n\n", "Human:", "Assistant:"],
            )
            return result["choices"][0]["text"]
        except Exception as e:
            print(f"[ERROR] Generation failed: {e}")
            return self._stub_response(prompt)
    
    def _stub_response(self, prompt: str) -> str:
        """Stub response when model not available."""
        return '{"action": "respond", "reason": "stub_mode_no_model"}'


class QwenLocal:
    """
    Alternative: Qwen 2.5 (small version for CPU)
    """
    
    def __init__(
        self,
        model_path: str = "models/qwen2.5-1.5b-instruct-q4_0.gguf",
        n_ctx: int = 4096,
        n_threads: int = 6,
        temperature: float = 0.7,
        top_p: float = 0.9,
    ):
        self.temperature = temperature
        self.top_p = top_p
        self.model_path = model_path
        
        if LLAMA_CPP_AVAILABLE:
            try:
                self.model = Llama(
                    model_path=model_path,
                    n_ctx=n_ctx,
                    n_threads=n_threads,
                    verbose=False
                )
                self.available = True
            except Exception as e:
                print(f"[ERROR] Failed to load Qwen model: {e}")
                self.model = None
                self.available = False
        else:
            self.model = None
            self.available = False
    
    def generate(self, prompt: str, max_tokens: int = 150) -> str:
        """Generate using Qwen."""
        if not self.available or self.model is None:
            return self._stub_response(prompt)
        
        try:
            # Qwen works better with chat format
            messages = [
                {"role": "system", "content": "You are Qwen, a helpful AI assistant."},
                {"role": "user", "content": prompt}
            ]
            result = self.model.create_chat_completion(
                messages=messages,
                max_tokens=max_tokens,
                temperature=self.temperature,
                top_p=self.top_p,
            )
            return result["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"[ERROR] Qwen generation failed: {e}")
            return self._stub_response(prompt)
    
    def _stub_response(self, prompt: str) -> str:
        return '{"action": "respond", "reason": "qwen_stub_mode"}'
