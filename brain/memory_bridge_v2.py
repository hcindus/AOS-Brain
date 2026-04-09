"""
Memory Bridge v2.0 - Non-blocking with Embedding Orchestrator
Connects AOS Brain to Workspace Memory Files

Uses EmbeddingOrchestrator for non-blocking, fault-tolerant embeddings.
Never blocks the OODA loop.
"""

import os
import time
import json
import hashlib
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import numpy as np
import threading

# Import the embedding orchestrator
from embedding_orchestrator import get_orchestrator, EmbeddingConfig


class MemoryBridge:
    """
    Bridges workspace memory files to the brain's retrieval system.
    
    Non-blocking architecture - uses EmbeddingOrchestrator for embeddings.
    When limbic detects high novelty, this queries:
    - /root/.openclaw/workspace/MEMORY.md (long-term curated memory)
    - /root/.openclaw/workspace/memory/*.md (daily logs)
    """
    
    def __init__(self, workspace_path: str = "/root/.openclaw/workspace"):
        self.workspace = Path(workspace_path)
        self.memory_dir = self.workspace / "memory"
        self.memory_file = self.workspace / "MEMORY.md"
        
        # In-memory index of memory chunks with embeddings
        self.index: List[Dict] = []
        self.indexed_hashes: Dict[str, str] = {}
        
        # Initialize embedding orchestrator (non-blocking)
        config = EmbeddingConfig(
            enable_local=True,
            enable_remote=True,  # Try Ollama if available
            enable_stub=True,    # Never block
            local_timeout_ms=150,
            remote_timeout_ms=500
        )
        self.orchestrator = get_orchestrator(config)
        
        # Similarity threshold for retrieval
        self.similarity_threshold = 0.5
        
        # Async indexing
        self._indexing_thread: Optional[threading.Thread] = None
        self._indexing_complete = False
        
    def _get_embedding(self, text: str) -> Tuple[List[float], str]:
        """Get embedding via orchestrator (never blocks)."""
        return self.orchestrator.get_sync(text, allow_stub=True)
    
    def _cosine_similarity(self, a: List[float], b: List[float]) -> float:
        """Calculate cosine similarity between two vectors."""
        if not a or not b or len(a) != len(b):
            return 0.0
        a_vec = np.array(a)
        b_vec = np.array(b)
        norm_a = np.linalg.norm(a_vec)
        norm_b = np.linalg.norm(b_vec)
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return float(np.dot(a_vec, b_vec) / (norm_a * norm_b))
    
    def _file_hash(self, path: Path) -> str:
        """Get MD5 hash of file content for change detection."""
        try:
            return hashlib.md5(path.read_bytes()).hexdigest()
        except:
            return ""
    
    def _chunk_text(self, text: str, chunk_size: int = 800, overlap: int = 200) -> List[Tuple[str, int]]:
        """Split text into overlapping chunks with line numbers."""
        chunks = []
        lines = text.split('\n')
        current_chunk = []
        current_size = 0
        line_num = 0
        
        for i, line in enumerate(lines):
            current_chunk.append(line)
            current_size += len(line) + 1
            
            if current_size >= chunk_size:
                chunks.append(('\n'.join(current_chunk), line_num))
                # Keep overlap lines for next chunk
                overlap_lines = current_chunk[-3:] if len(current_chunk) > 3 else current_chunk
                current_chunk = overlap_lines
                current_size = sum(len(l) + 1 for l in current_chunk)
                line_num = i - len(overlap_lines) + 1
        
        # Add remaining chunk
        if current_chunk and len('\n'.join(current_chunk)) > 100:
            chunks.append(('\n'.join(current_chunk), line_num))
        
        return chunks
    
    def index_memory_files(self, force_reindex: bool = False) -> Dict:
        """
        Index MEMORY.md and memory/*.md into in-memory index.
        Non-blocking - returns immediately, indexes in background.
        """
        # Start indexing in background thread
        if self._indexing_thread is None or not self._indexing_thread.is_alive():
            self._indexing_thread = threading.Thread(
                target=self._do_indexing,
                args=(force_reindex,),
                daemon=True
            )
            self._indexing_thread.start()
            print("[MemoryBridge] Indexing started in background")
        
        return {"status": "indexing", "indexed": len(self.index)}
    
    def _do_indexing(self, force_reindex: bool = False):
        """Background indexing work."""
        stats = {"indexed": 0, "skipped": 0, "errors": 0}
        
        # Files to index
        files_to_index = []
        if self.memory_file.exists():
            files_to_index.append(self.memory_file)
        if self.memory_dir.exists():
            files_to_index.extend(sorted(self.memory_dir.glob("*.md")))
        
        for file_path in files_to_index:
            try:
                content = file_path.read_text(encoding="utf-8")
                chunks = self._chunk_text(content)
                
                for chunk_text, line_num in chunks:
                    if len(chunk_text) < 100:
                        continue
                    
                    # Get embedding (non-blocking via orchestrator)
                    embedding, source = self._get_embedding(chunk_text)
                    
                    self.index.append({
                        "text": chunk_text,
                        "embedding": embedding,
                        "source": str(file_path.relative_to(self.workspace)),
                        "line": line_num,
                        "embedding_source": source
                    })
                    stats["indexed"] += 1
                    
            except Exception as e:
                print(f"[MemoryBridge] Error indexing {file_path}: {e}")
                stats["errors"] += 1
        
        self._indexing_complete = True
        print(f"[MemoryBridge] Indexing complete: {stats}")
    
    def query(self, query_text: str, n_results: int = 2, novelty: float = 0.0) -> Dict:
        """
        Query indexed memories for relevant context.
        Non-blocking - returns immediately with available results.
        """
        # Get query embedding
        query_emb, _ = self._get_embedding(query_text)
        
        # If index is empty or still building, return empty
        if not self.index:
            return {"results": [], "source_count": 0}
        
        # Score all chunks by similarity
        scored = []
        for item in self.index:
            sim = self._cosine_similarity(query_emb, item["embedding"])
            scored.append((sim, item))
        
        # Sort by similarity
        scored.sort(key=lambda x: x[0], reverse=True)
        
        # Return top N
        top_results = [
            {
                "text": item["text"][:200],
                "source": item["source"],
                "relevance": sim,
                "embedding_source": item.get("embedding_source", "unknown")
            }
            for sim, item in scored[:n_results]
        ]
        
        return {
            "results": top_results,
            "source_count": len(self.index),
            "indexing_complete": self._indexing_complete
        }
    
    def should_query_memory(self, novelty: float, novelty_avg: float, threshold: float = 0.7) -> bool:
        """Determine if we should query memory based on novelty."""
        return novelty > threshold or novelty_avg > threshold * 0.8
    
    def get_stats(self) -> Dict:
        """Get MemoryBridge statistics."""
        return {
            "indexed_items": len(self.index),
            "indexing_complete": self._indexing_complete,
            "indexing_active": self._indexing_thread is not None and self._indexing_thread.is_alive(),
            "orchestrator": self.orchestrator.get_stats()
        }


if __name__ == "__main__":
    print("=" * 60)
    print("MemoryBridge v2.0 Test")
    print("Non-blocking with Embedding Orchestrator")
    print("=" * 60)
    
    # Create bridge
    bridge = MemoryBridge()
    
    print("\n1. Starting indexing (non-blocking)...")
    result = bridge.index_memory_files()
    print(f"   Status: {result['status']}")
    
    print("\n2. Querying immediately (should return even if indexing)...")
    query_result = bridge.query("test query", n_results=2)
    print(f"   Results: {len(query_result['results'])}")
    print(f"   Sources indexed: {query_result['source_count']}")
    
    print("\n3. Waiting for indexing...")
    time.sleep(2)
    
    stats = bridge.get_stats()
    print(f"   Indexed: {stats['indexed_items']}")
    print(f"   Complete: {stats['indexing_complete']}")
    print(f"   Orchestrator cache hits: {stats['orchestrator']['cache_hits']}")
    
    print("\n4. Querying again...")
    query_result = bridge.query("neural networks", n_results=2)
    print(f"   Results: {len(query_result['results'])}")
    for r in query_result['results']:
        print(f"   - {r['source']}: {r['text'][:50]}...")
    
    print("\n" + "=" * 60)
    print("Test complete")
    print("=" * 60)
