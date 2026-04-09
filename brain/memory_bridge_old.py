"""
Memory Bridge: Connects AOS Brain to Workspace Memory Files
Lightweight version - uses Ollama embeddings directly, no ChromaDB required
"""

import os
import time
import json
import hashlib
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import numpy as np

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False


class MemoryBridge:
    """
    Bridges workspace memory files to the brain's retrieval system.
    
    When limbic detects high novelty, this queries:
    - /root/.openclaw/workspace/MEMORY.md (long-term curated memory)
    - /root/.openclaw/workspace/memory/*.md (daily logs)
    
    Uses Ollama nomic-embed-text for semantic similarity.
    """
    
    def __init__(self, workspace_path: str = "/root/.openclaw/workspace"):
        self.workspace = Path(workspace_path)
        self.memory_dir = self.workspace / "memory"
        self.memory_file = self.workspace / "MEMORY.md"
        
        # In-memory index of memory chunks with embeddings
        self.index: List[Dict] = []
        self.indexed_hashes: Dict[str, str] = {}
        
        # Embedding model
        self.embed_model = "nomic-embed-text:latest"
        
        # Similarity threshold for retrieval (lower = more permissive)
        self.similarity_threshold = 0.5
        
    def _get_embedding(self, text: str, timeout: float = 5.0) -> Optional[List[float]]:
        """Get embedding via Ollama's nomic-embed-text with fallback."""
        if not REQUESTS_AVAILABLE:
            return self._fallback_embedding(text)
            
        try:
            # Truncate long texts for embedding
            text = text[:2000] if len(text) > 2000 else text
            
            resp = requests.post(
                "http://localhost:11434/api/embeddings",
                json={"model": self.embed_model, "prompt": text},
                timeout=timeout  # Short timeout to prevent hangs
            )
            resp.raise_for_status()
            embedding = resp.json().get("embedding")
            if embedding:
                return embedding
        except Exception as e:
            print(f"[MemoryBridge] Ollama embedding failed (timeout={timeout}s): {e}")
        
        # Fallback to hash-based deterministic embedding
        print("[MemoryBridge] Using fallback embedding")
        return self._fallback_embedding(text)
    
    def _fallback_embedding(self, text: str, dimension: int = 384) -> List[float]:
        """Generate deterministic pseudo-embedding from text hash.
        
        Used when Ollama is unavailable or timing out.
        Ensures brain can always start and form memories.
        """
        # Create hash of text
        hash_val = hashlib.sha256(text.encode()).hexdigest()
        
        # Convert to vector
        vector = []
        for i in range(0, len(hash_val), 2):
            byte_val = int(hash_val[i:i+2], 16)
            # Normalize to [-1, 1]
            normalized = (byte_val / 255.0) * 2 - 1
            vector.append(normalized)
        
        # Expand to target dimension
        while len(vector) < dimension:
            vector.extend(vector)
        
        return vector[:dimension]
    
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
        Returns stats: {'indexed': N, 'skipped': M, 'errors': K}
        """
        stats = {"indexed": 0, "skipped": 0, "errors": 0}
        
        # Files to index
        files_to_index = []
        if self.memory_file.exists():
            files_to_index.append(self.memory_file)
        if self.memory_dir.exists():
            files_to_index.extend(sorted(self.memory_dir.glob("*.md")))
        
        new_index = []
        
        for file_path in files_to_index:
            file_id = str(file_path.relative_to(self.workspace))
            current_hash = self._file_hash(file_path)
            
            # Skip if unchanged and not forcing reindex
            if not force_reindex and file_id in self.indexed_hashes:
                if self.indexed_hashes[file_id] == current_hash:
                    stats["skipped"] += 1
                    # Keep existing entries for this file
                    new_index.extend([e for e in self.index if e.get("source") == file_id])
                    continue
            
            try:
                content = file_path.read_text(encoding="utf-8")
                chunks = self._chunk_text(content)
                
                for chunk_text, line_num in chunks:
                    if len(chunk_text) < 100:
                        continue
                    
                    embedding = self._get_embedding(chunk_text)
                    if embedding:
                        new_index.append({
                            "text": chunk_text,
                            "source": file_id,
                            "line": line_num,
                            "hash": current_hash,
                            "embedding": embedding,
                            "indexed_at": time.time()
                        })
                        stats["indexed"] += 1
                    else:
                        stats["errors"] += 1
                
                self.indexed_hashes[file_id] = current_hash
                
            except Exception as e:
                print(f"[MemoryBridge] Error indexing {file_id}: {e}")
                stats["errors"] += 1
        
        self.index = new_index
        print(f"[MemoryBridge] Index complete: {stats['indexed']} chunks, {stats['skipped']} skipped, {stats['errors']} errors")
        return stats
    
    def query(self, query_text: str, n_results: int = 3, novelty: float = 0.0) -> Dict:
        """
        Query workspace memory when limbic signals high novelty.
        
        Args:
            query_text: The current observation/context to match against
            n_results: Number of memory snippets to return
            novelty: Current novelty score (for logging)
            
        Returns:
            Dict with 'results', 'novelty_trigger', 'source_count'
        """
        if not self.index:
            # Auto-index on first query
            stats = self.index_memory_files()
            if stats["indexed"] == 0:
                return {
                    "results": [],
                    "novelty_trigger": novelty,
                    "source_count": 0,
                    "error": "No memory files indexed"
                }
        
        # Get query embedding
        query_embedding = self._get_embedding(query_text)
        if not query_embedding:
            return {
                "results": [],
                "novelty_trigger": novelty,
                "source_count": 0,
                "error": "Failed to embed query"
            }
        
        # Calculate similarities
        scored = []
        for entry in self.index:
            sim = self._cosine_similarity(query_embedding, entry["embedding"])
            if sim >= self.similarity_threshold:
                scored.append({**entry, "similarity": sim})
        
        # Sort by similarity and take top N
        scored.sort(key=lambda x: x["similarity"], reverse=True)
        top_results = scored[:n_results]
        
        # Format results
        formatted = []
        for r in top_results:
            formatted.append({
                "text": r["text"][:600],  # Truncate for context
                "source": r["source"],
                "line": r["line"],
                "relevance": round(r["similarity"], 3)
            })
        
        return {
            "results": formatted,
            "novelty_trigger": novelty,
            "source_count": len(formatted),
            "total_indexed": len(self.index),
            "query": query_text[:100]  # Truncated for debug
        }
    
    def should_query_memory(self, novelty: float, novelty_avg: float) -> bool:
        """
        Determine if we should query workspace memory based on limbic signals.
        
        Query when:
        - Current novelty is high (>0.75)
        - Novelty is significantly above average (> avg + 0.15)
        """
        threshold = 0.75
        above_avg = novelty > (novelty_avg + 0.15) if novelty_avg > 0 else novelty > threshold
        return novelty > threshold or above_avg


# Singleton instance for brain integration
_memory_bridge = None

def get_memory_bridge() -> MemoryBridge:
    """Get or create the memory bridge singleton."""
    global _memory_bridge
    if _memory_bridge is None:
        _memory_bridge = MemoryBridge()
    return _memory_bridge


if __name__ == "__main__":
    # Test the bridge
    bridge = MemoryBridge()
    print("Testing Memory Bridge...")
    
    # Index files
    stats = bridge.index_memory_files()
    print(f"\nIndex stats: {stats}")
    
    # Query
    if bridge.index:
        result = bridge.query("persistence memory recall consciousness", n_results=2, novelty=0.8)
        print(f"\nQuery result:")
        print(json.dumps(result, indent=2))
    else:
        print("\nNo documents indexed")
