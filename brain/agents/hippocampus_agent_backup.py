import time
import requests
import numpy as np

try:
    import chromadb
    CHROMA_AVAILABLE = True
except ImportError:
    CHROMA_AVAILABLE = False

class HippocampusAgent:
    def __init__(self, cfg):
        self.cfg = cfg
        self.backend = cfg["models"]["backend"]
        
        # Safe extraction for nested config
        try:
            self.summarizer_model = cfg["models"]["ollama"]["pfc_right"]
        except KeyError:
            self.summarizer_model = "phi3:3.8b"

        # QMD Settings
        try:
            self.qmd_config = cfg.get("layers", {}).get("subconscious", {}).get("regions", {}).get("hippocampus", {}).get("qmd", {})
            self.threshold = self.qmd_config.get("distillation_threshold", 20)
            self.novelty_threshold = self.qmd_config.get("novelty_threshold", 0.8)
        except KeyError:
            self.threshold = 20
            self.novelty_threshold = 0.8
        
        # Memory Stores
        self.episodic_buffer = []  # Short-term raw OODA traces
        self.novelty_scores = []   # Track novelty over time
        self.total_traces = 0       # Count total traces processed
        
        # Vector Store Migration to ChromaDB
        if CHROMA_AVAILABLE:
            try:
                db_path = self.qmd_config.get("vector_store", {}).get("path", "~/.aos/memory/vector").replace("~", "/root")
                self.chroma_client = chromadb.PersistentClient(path=db_path)
                self.collection = self.chroma_client.get_or_create_collection(name="qmd_memory")
                self.using_chroma = True
                self.total_traces = self.collection.count()
                print(f"[QMD] ChromaDB Vector Memory Online. Documents: {self.total_traces}")
            except Exception as e:
                self.using_chroma = False
                self.distilled_vectors = []
                print(f"[QMD] Failed to mount ChromaDB: {e}. Falling back to mocked vectors.")
        else:
            self.using_chroma = False
            self.distilled_vectors = []

    def _ollama_summarize(self, prompt: str) -> str:
        """Calls the local Phi-3 model to compress memory traces into dense QMD concepts."""
        try:
            resp = requests.post(
                "http://localhost:11434/api/generate",
                json={"model": self.summarizer_model, "prompt": prompt, "stream": False},
                timeout=60,
            )
            resp.raise_for_status()
            response_text = resp.json().get("response", "").strip()
            
            # Validate response - reject error messages
            if response_text.startswith("[") and "Error" in response_text:
                return None
            if len(response_text) < 10:
                return None
                
            return response_text
        except Exception as e:
            print(f"[QMD] Ollama summarization failed: {e}")
            return None

    def calculate_novelty(self, trace) -> float:
        """
        Calculate novelty score by comparing to existing memories.
        Returns 0.0-1.0 where 1.0 is completely novel.
        """
        if not self.using_chroma or self.collection.count() == 0:
            return 1.0  # First trace is always novel
        
        try:
            query_str = str(trace)
            results = self.collection.query(
                query_texts=[query_str],
                n_results=1
            )
            
            if results["distances"] and len(results["distances"]) > 0:
                distance = results["distances"][0][0]
                # Normalize distance to 0-1 scale (Chroma uses cosine distance)
                novelty = min(distance, 1.0)
                return novelty
        except Exception as e:
            print(f"[QMD] Novelty calculation failed: {e}")
        
        return 0.5  # Default to medium novelty on error

    def retrieve(self, obs):
        """
        Subconscious Layer (Orient Phase): 
        Performs QMD Hybrid Search (Recent Episodic + Distilled Long-Term).
        """
        recent_context = [m["obs"] for m in self.episodic_buffer[-3:]]
        distilled_context = []

        if self.using_chroma and self.collection.count() > 0:
            # Semantic Query to ChromaDB
            try:
                query_str = str(obs)
                results = self.collection.query(
                    query_texts=[query_str],
                    n_results=2
                )
                if results["documents"]:
                    distilled_context = results["documents"][0]
            except Exception as e:
                distilled_context = [f"[Query Error: {e}]"]
        elif not self.using_chroma:
            distilled_context = self.distilled_vectors[-2:] if self.distilled_vectors else []
        
        if not recent_context and not distilled_context:
            return {"context": "none", "qmd_active": True, "chroma": self.using_chroma}
            
        context_payload = {
            "immediate_recall": recent_context,
            "distilled_wisdom": distilled_context
        }
        return {"context": str(context_payload), "qmd_active": True, "chroma": self.using_chroma}

    def store(self, obs, plan, action, affect):
        """
        Unconscious Layer (Learn Phase):
        Stores raw trace. Triggers QMD distillation if buffer is full.
        Calculates novelty for GrowingNN.
        """
        trace = {
            "timestamp": time.time(),
            "obs": obs,
            "plan": plan,
            "action": action,
            "affect": affect
        }
        
        # Calculate novelty for this trace
        novelty = self.calculate_novelty(trace)
        self.novelty_scores.append(novelty)
        
        self.episodic_buffer.append(trace)
        self.total_traces += 1
        
        if len(self.episodic_buffer) >= self.threshold:
            self._distill_memory()
        
        return {"novelty": novelty, "buffer_size": len(self.episodic_buffer)}

    def _distill_memory(self):
        """Compresses the raw episodic buffer into a dense, semantic chunk."""
        raw_text = str([t["obs"] for t in self.episodic_buffer])
        prompt = f"""You are the QMD memory compressor for AOS. 
        Extract the core concepts, decisions, and outcomes from these raw logs. 
        Discard fluff. Keep it dense and highly factual.
        Logs: {raw_text}"""
        
        if self.backend == "ollama":
            compressed_insight = self._ollama_summarize(prompt)
            
            # Only store if summarization succeeded
            if compressed_insight:
                if self.using_chroma:
                    doc_id = f"qmd_concept_{int(time.time())}"
                    try:
                        self.collection.add(
                            documents=[compressed_insight],
                            metadatas=[{
                                "source": "episodic_buffer_distillation", 
                                "timestamp": time.time(),
                                "traces_compressed": len(self.episodic_buffer)
                            }],
                            ids=[doc_id]
                        )
                        print(f"[QMD] Stored concept. Total documents: {self.collection.count()}")
                    except Exception as e:
                        print(f"[QMD] Chroma DB insert failed: {e}")
                else:
                    self.distilled_vectors.append(compressed_insight)
            else:
                print("[QMD] Skipping storage - summarization failed")
        
        self.episodic_buffer = []

    def get_novelty_stats(self):
        """Return novelty statistics for GrowingNN."""
        if not self.novelty_scores:
            return {"current": 0.0, "average": 0.0, "max": 0.0}
        
        return {
            "current": self.novelty_scores[-1],
            "average": np.mean(self.novelty_scores[-100:]),
            "max": max(self.novelty_scores),
            "total_traces": self.total_traces
        }
