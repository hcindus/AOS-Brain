#!/usr/bin/env python3
"""
AOS Embedding Orchestrator
Non-blocking, local, cached embedding subsystem

Priority order:
1. Cache hit (memory/disk)
2. Local embedder (GGUF/fast)
3. Remote/Ollama (async, best-effort)
4. Stub vector (guaranteed return)

Never blocks the OODA loop.
"""

import asyncio
import hashlib
import json
import time
import pickle
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from pathlib import Path
from collections import OrderedDict
import threading


@dataclass
class EmbeddingCacheEntry:
    """Cached embedding with metadata"""
    vector: List[float]
    model_id: str
    timestamp: float
    access_count: int = 0


@dataclass
class EmbeddingConfig:
    """Configuration for embedding orchestrator"""
    dimension: int = 384
    cache_size: int = 10000  # Max in-memory entries
    
    # Timeout settings (milliseconds)
    local_timeout_ms: float = 150
    remote_timeout_ms: float = 500
    
    # Priority order
    priority_order: List[str] = field(default_factory=lambda: [
        "cache", "local", "remote", "stub"
    ])
    
    # Feature flags
    enable_local: bool = True
    enable_remote: bool = True
    enable_stub: bool = True
    
    # Paths
    disk_cache_path: Path = field(default_factory=lambda: Path.home() / ".aos" / "cache" / "embeddings")
    
    # Model IDs
    local_model_id: str = "local-hash-v1"
    remote_model_id: str = "ollama-nomic"


class DiskCache:
    """Persistent disk cache for embeddings"""
    
    def __init__(self, cache_dir: Path, dimension: int = 384):
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.dimension = dimension
        self._lock = threading.RLock()
        
    def _get_path(self, key: str) -> Path:
        """Get file path for cache key"""
        # Hash the key for filename
        hashed = hashlib.md5(key.encode()).hexdigest()[:16]
        return self.cache_dir / f"{hashed}.emb"
    
    def get(self, key: str) -> Optional[List[float]]:
        """Get embedding from disk cache"""
        path = self._get_path(key)
        try:
            with self._lock:
                if path.exists():
                    with open(path, 'rb') as f:
                        entry = pickle.load(f)
                        if len(entry['vector']) == self.dimension:
                            return entry['vector']
        except Exception:
            pass
        return None
    
    def put(self, key: str, vector: List[float], model_id: str):
        """Store embedding in disk cache"""
        path = self._get_path(key)
        try:
            entry = {
                'vector': vector,
                'model_id': model_id,
                'timestamp': time.time()
            }
            with self._lock:
                with open(path, 'wb') as f:
                    pickle.dump(entry, f)
        except Exception:
            pass
    
    def clear(self):
        """Clear disk cache"""
        try:
            for f in self.cache_dir.glob("*.emb"):
                f.unlink()
        except Exception:
            pass


class MemoryCache:
    """LRU in-memory cache for embeddings"""
    
    def __init__(self, maxsize: int = 10000):
        self.maxsize = maxsize
        self._cache: OrderedDict[str, EmbeddingCacheEntry] = OrderedDict()
        self._lock = threading.RLock()
    
    def get(self, key: str) -> Optional[List[float]]:
        """Get from memory cache (LRU)"""
        with self._lock:
            if key in self._cache:
                entry = self._cache.pop(key)
                entry.access_count += 1
                self._cache[key] = entry  # Move to end (most recent)
                return entry.vector
        return None
    
    def put(self, key: str, vector: List[float], model_id: str):
        """Store in memory cache"""
        with self._lock:
            if key in self._cache:
                self._cache.pop(key)
            elif len(self._cache) >= self.maxsize:
                self._cache.popitem(last=False)  # Remove oldest
            
            self._cache[key] = EmbeddingCacheEntry(
                vector=vector,
                model_id=model_id,
                timestamp=time.time(),
                access_count=1
            )
    
    def stats(self) -> Dict:
        """Get cache statistics"""
        with self._lock:
            total_accesses = sum(e.access_count for e in self._cache.values())
            return {
                'size': len(self._cache),
                'maxsize': self.maxsize,
                'total_accesses': total_accesses
            }


class LocalEmbedder:
    """Local hash-based embedder (fast, deterministic)"""
    
    def __init__(self, dimension: int = 384):
        self.dimension = dimension
        
    def embed(self, text: str) -> List[float]:
        """Generate deterministic embedding from text hash"""
        # Normalize text
        text = text.lower().strip()
        
        # Create hash
        hash_val = hashlib.sha256(text.encode()).hexdigest()
        
        # Convert to vector
        vector = []
        for i in range(0, len(hash_val), 2):
            byte_val = int(hash_val[i:i+2], 16)
            # Normalize to [-1, 1]
            normalized = (byte_val / 255.0) * 2 - 1
            vector.append(normalized)
        
        # Expand to target dimension
        while len(vector) < self.dimension:
            vector.extend(vector)
        
        return vector[:self.dimension]
    
    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Embed multiple texts"""
        return [self.embed(t) for t in texts]


class RemoteEmbedder:
    """Remote Ollama embedder (async, best-effort)"""
    
    def __init__(self, model: str = "nomic-embed-text:latest", 
                 timeout_ms: float = 500):
        self.model = model
        self.timeout = timeout_ms / 1000.0  # Convert to seconds
        self._session = None
        
    async def embed(self, text: str) -> Optional[List[float]]:
        """Get embedding from Ollama (async, with timeout)"""
        try:
            import aiohttp
            
            if self._session is None:
                self._session = aiohttp.ClientSession()
            
            async with asyncio.timeout(self.timeout):
                async with self._session.post(
                    "http://localhost:11434/api/embeddings",
                    json={"model": self.model, "prompt": text}
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return data.get("embedding")
        except Exception:
            pass
        return None
    
    def embed_sync(self, text: str) -> Optional[List[float]]:
        """Synchronous wrapper (uses thread)"""
        try:
            import requests
            resp = requests.post(
                "http://localhost:11434/api/embeddings",
                json={"model": self.model, "prompt": text},
                timeout=self.timeout
            )
            if resp.status_code == 200:
                return resp.json().get("embedding")
        except Exception:
            pass
        return None


class EmbeddingOrchestrator:
    """
    Main orchestrator for embeddings
    Non-blocking, fault-tolerant
    """
    
    def __init__(self, config: Optional[EmbeddingConfig] = None):
        self.config = config or EmbeddingConfig()
        
        # Initialize components
        self.memory_cache = MemoryCache(maxsize=self.config.cache_size)
        self.disk_cache = DiskCache(
            self.config.disk_cache_path,
            self.config.dimension
        )
        self.local_embedder = LocalEmbedder(self.config.dimension)
        self.remote_embedder = RemoteEmbedder(
            timeout_ms=self.config.remote_timeout_ms
        ) if self.config.enable_remote else None
        
        # Statistics
        self.stats = {
            'cache_hits': 0,
            'local_hits': 0,
            'remote_hits': 0,
            'stub_hits': 0,
            'errors': 0
        }
        
    def _compute_key(self, text: str) -> str:
        """Compute cache key for text"""
        return hashlib.sha256(text.encode()).hexdigest()
    
    def _get_stub(self) -> List[float]:
        """Get stub embedding (zeros with small noise)"""
        import random
        return [random.uniform(-0.01, 0.01) for _ in range(self.config.dimension)]
    
    def get_sync(self, text: str, allow_stub: bool = True) -> Tuple[List[float], str]:
        """
        Get embedding synchronously
        Returns: (vector, source)
        """
        if not text:
            return self._get_stub(), "stub"
        
        key = self._compute_key(text)
        
        # Try each source in priority order
        for source in self.config.priority_order:
            if source == "cache":
                # Try memory cache
                vec = self.memory_cache.get(key)
                if vec:
                    self.stats['cache_hits'] += 1
                    return vec, "memory_cache"
                
                # Try disk cache
                vec = self.disk_cache.get(key)
                if vec:
                    self.stats['cache_hits'] += 1
                    self.memory_cache.put(key, vec, "disk_cached")
                    return vec, "disk_cache"
            
            elif source == "local" and self.config.enable_local:
                vec = self.local_embedder.embed(text)
                if vec:
                    self.stats['local_hits'] += 1
                    # Cache it
                    self.memory_cache.put(key, vec, self.config.local_model_id)
                    self.disk_cache.put(key, vec, self.config.local_model_id)
                    return vec, "local"
            
            elif source == "remote" and self.config.enable_remote:
                vec = self.remote_embedder.embed_sync(text)
                if vec:
                    self.stats['remote_hits'] += 1
                    # Cache it
                    self.memory_cache.put(key, vec, self.config.remote_model_id)
                    self.disk_cache.put(key, vec, self.config.remote_model_id)
                    return vec, "remote"
        
        # Fallback to stub
        if allow_stub:
            self.stats['stub_hits'] += 1
            return self._get_stub(), "stub"
        
        raise RuntimeError("No embedding source available and stub not allowed")
    
    async def get_async(self, text: str, allow_stub: bool = True) -> Tuple[List[float], str]:
        """
        Get embedding asynchronously
        Returns: (vector, source)
        """
        if not text:
            return self._get_stub(), "stub"
        
        key = self._compute_key(text)
        
        for source in self.config.priority_order:
            if source == "cache":
                vec = self.memory_cache.get(key)
                if vec:
                    self.stats['cache_hits'] += 1
                    return vec, "memory_cache"
                
                vec = self.disk_cache.get(key)
                if vec:
                    self.stats['cache_hits'] += 1
                    self.memory_cache.put(key, vec, "disk_cached")
                    return vec, "disk_cache"
            
            elif source == "local" and self.config.enable_local:
                vec = self.local_embedder.embed(text)
                if vec:
                    self.stats['local_hits'] += 1
                    self.memory_cache.put(key, vec, self.config.local_model_id)
                    self.disk_cache.put(key, vec, self.config.local_model_id)
                    return vec, "local"
            
            elif source == "remote" and self.config.enable_remote:
                vec = await self.remote_embedder.embed(text)
                if vec:
                    self.stats['remote_hits'] += 1
                    self.memory_cache.put(key, vec, self.config.remote_model_id)
                    self.disk_cache.put(key, vec, self.config.remote_model_id)
                    return vec, "remote"
        
        if allow_stub:
            self.stats['stub_hits'] += 1
            return self._get_stub(), "stub"
        
        raise RuntimeError("No embedding source available and stub not allowed")
    
    def get_stats(self) -> Dict:
        """Get orchestrator statistics"""
        return {
            **self.stats,
            'memory_cache': self.memory_cache.stats(),
            'config': {
                'enable_local': self.config.enable_local,
                'enable_remote': self.config.enable_remote,
                'priority_order': self.config.priority_order
            }
        }
    
    def clear_cache(self):
        """Clear all caches"""
        self.memory_cache._cache.clear()
        self.disk_cache.clear()


# Singleton instance
_orchestrator: Optional[EmbeddingOrchestrator] = None

def get_orchestrator(config: Optional[EmbeddingConfig] = None) -> EmbeddingOrchestrator:
    """Get or create global orchestrator instance"""
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = EmbeddingOrchestrator(config)
    return _orchestrator


if __name__ == "__main__":
    print("=" * 60)
    print("Embedding Orchestrator Test")
    print("=" * 60)
    
    # Create orchestrator
    config = EmbeddingConfig(
        enable_local=True,
        enable_remote=False,  # Don't test Ollama in unit test
        enable_stub=True
    )
    orch = EmbeddingOrchestrator(config)
    
    # Test texts
    texts = [
        "This is a test sentence",
        "Another test sentence",
        "This is a test sentence",  # Duplicate
        "Something completely different",
    ]
    
    print("\nTesting synchronous embedding:")
    for text in texts:
        vec, source = orch.get_sync(text)
        print(f"  '{text[:30]}...' -> {source}, dim={len(vec)}, first_val={vec[0]:.4f}")
    
    print("\nStatistics:")
    stats = orch.get_stats()
    print(f"  Cache hits: {stats['cache_hits']}")
    print(f"  Local hits: {stats['local_hits']}")
    print(f"  Stub hits: {stats['stub_hits']}")
    print(f"  Memory cache size: {stats['memory_cache']['size']}")
    
    print("\n" + "=" * 60)
    print("Test complete")
    print("=" * 60)
