#!/usr/bin/env python3
"""
MemoryBridge - Ollama Embeddings Integration
Complete Brain v4 Compatible
"""

import os
import time
import json
import hashlib
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from collections import deque

# Optional numpy
try:
    import numpy as np
    NP_AVAILABLE = True
except ImportError:
    NP_AVAILABLE = False

# Optional requests
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False


class MemoryBridge:
    """
    Memory Bridge: Ollama Embeddings + Workspace Memory
    Ported for Complete Brain v4
    """
    
    def __init__(self, workspace_path: str = "/root/.openclaw/workspace"):
        self.workspace = Path(workspace_path)
        self.memory_file = self.workspace / "MEMORY.md"
        self.memory_dir = self.workspace / "memory"
        
        self.embed_model = "nomic-embed-text:latest"
        self.index: List[Dict] = []
        self.indexed_hashes: Dict[str, str] = {}
        self.similarity_threshold = 0.5
        
        print("[MemoryBridge] Initialized")
    
    def _get_embedding(self, text: str) -> Optional[List[float]]:
        """Get embedding via Ollama"""
        if not REQUESTS_AVAILABLE:
            return None
        
        try:
            text = text[:2000] if len(text) > 2000 else text
            
            resp = requests.post(
                "http://localhost:11434/api/embeddings",
                json={"model": self.embed_model, "prompt": text},
                timeout=30
            )
            resp.raise_for_status()
            return resp.json().get("embedding")
        except Exception as e:
            print(f"[MemoryBridge] Embedding failed: {e}")
            return None
    
    def _cosine_similarity(self, a: List[float], b: List[float]) -> float:
        """Calculate cosine similarity"""
        if not NP_AVAILABLE or not a or not b or len(a) != len(b):
            return 0.0
        
        a_vec = np.array(a)
        b_vec = np.array(b)
        norm_a = np.linalg.norm(a_vec)
        norm_b = np.linalg.norm(b_vec)
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return float(np.dot(a_vec, b_vec) / (norm_a * norm_b))
    
    def query(self, query_text: str, n: int = 3) -> List[Dict]:
        """Query memory via semantic similarity"""
        if not REQUESTS_AVAILABLE:
            return []
        
        # Get query embedding
        query_embedding = self._get_embedding(query_text)
        if not query_embedding:
            return []
        
        # Index memories if not done
        if not self.index:
            self._index_memories()
        
        # Find similar memories
        results = []
        for mem in self.index:
            if "embedding" in mem:
                sim = self._cosine_similarity(query_embedding, mem["embedding"])
                if sim >= self.similarity_threshold:
                    results.append({
                        "content": mem["content"][:200],
                        "similarity": sim,
                        "source": mem.get("source", "unknown")
                    })
        
        # Sort by similarity
        results.sort(key=lambda x: x["similarity"], reverse=True)
        return results[:n]
    
    def _index_memories(self):
        """Index workspace memory files"""
        try:
            # Index MEMORY.md
            if self.memory_file.exists():
                content = self.memory_file.read_text()
                self._add_to_index(content, "MEMORY.md")
            
            # Index daily memory files
            if self.memory_dir.exists():
                for mem_file in self.memory_dir.glob("*.md"):
                    content = mem_file.read_text()
                    self._add_to_index(content, mem_file.name)
            
            print(f"[MemoryBridge] Indexed {len(self.index)} memories")
        except Exception as e:
            print(f"[MemoryBridge] Index error: {e}")
    
    def _add_to_index(self, content: str, source: str):
        """Add content to index with embedding"""
        embedding = self._get_embedding(content[:2000])
        if embedding:
            self.index.append({
                "content": content[:1000],
                "embedding": embedding,
                "source": source,
                "timestamp": time.time()
            })
    
    def get_stats(self) -> Dict:
        """Get MemoryBridge statistics"""
        return {
            "indexed_memories": len(self.index),
            "sources": list(set(m.get("source", "unknown") for m in self.index)),
            "model": self.embed_model
        }


if __name__ == "__main__":
    print("=" * 70)
    print("  MEMORYBRIDGE TEST")
    print("=" * 70)
    
    bridge = MemoryBridge()
    
    print("\nQuerying memory...")
    results = bridge.query("AOS brain status", n=3)
    
    print(f"\nFound {len(results)} relevant memories:")
    for i, mem in enumerate(results):
        print(f"\n{i+1}. [{mem['similarity']:.2f}] {mem['source']}")
        print(f"   {mem['content'][:100]}...")
    
    print("\n" + "=" * 70)
