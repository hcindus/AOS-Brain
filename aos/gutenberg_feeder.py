#!/usr/bin/env python3
"""
GUTENBERG FEEDER v1.0
Feeds classic literature to AOS Brain cortex
Downloads and encodes Project Gutenberg texts
"""

import urllib.request
import urllib.error
import json
import socket
import time
import re
import hashlib
import numpy as np
from typing import List, Tuple, Dict

class GutenbergFeeder:
    """
    Feeds Project Gutenberg literature to brain cortex
    """
    
    # Popular Gutenberg books (etext IDs)
    BOOKS = {
        'pride_prejudice': '1342',
        'moby_dick': '2701',
        'frankenstein': '84',
        'dracula': '345',
        'sherlock_holmes': '1661',
        'alice_wonderland': '11',
        'wizard_oz': '55',
        'dr_jekyll': '43',
        'picture_dorian': '174',
        'metamorphosis': '5200',
        'ulysses': '4300',
        'great_gatsby': '64317',
        'hamlet': '2265',
        'macbeth': '2264',
        'romeo_juliet': '2263',
        'divine_comedy': '8800',
        'iliad': '6130',
        'odyssey': '1727',
        'beowulf': '16328',
        'canterbury_tales': '2383',
    }
    
    def __init__(self, brain_socket='/tmp/aos_brain.sock', agent_id="gutenberg_reader"):
        self.brain_socket = brain_socket
        self.agent_id = agent_id
        self.cache = {}
        self.stats = {'downloaded': 0, 'fed': 0, 'bytes': 0, 'errors': 0}
        print(f"[Gutenberg] Initialized with {len(self.BOOKS)} books")
    
    def _send(self, cmd, params):
        try:
            sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect(self.brain_socket)
            sock.sendall((json.dumps({'cmd': cmd, 'params': params}) + '\n').encode())
            data = sock.recv(4096)
            sock.close()
            return json.loads(data.decode()) if data else {'error': 'empty'}
        except Exception as e:
            self.stats['errors'] += 1
            return {'error': str(e)}
    
    def download_book(self, book_id: str) -> str:
        """Download book from Project Gutenberg"""
        if book_id in self.cache:
            return self.cache[book_id]
        
        url = f"https://www.gutenberg.org/files/{book_id}/{book_id}-0.txt"
        
        try:
            print(f"[Gutenberg] Downloading book {book_id}...")
            req = urllib.request.Request(
                url,
                headers={
                    'User-Agent': 'AOS-Brain-Feeder/1.0 (Educational Research)',
                    'Accept': 'text/plain'
                }
            )
            
            with urllib.request.urlopen(req, timeout=30) as response:
                text = response.read().decode('utf-8', errors='ignore')
                
            # Clean up text
            text = self._clean_text(text)
            
            self.cache[book_id] = text
            self.stats['downloaded'] += 1
            self.stats['bytes'] += len(text)
            
            print(f"[Gutenberg] Downloaded {len(text):,} chars")
            return text
            
        except Exception as e:
            print(f"[Gutenberg] Error downloading {book_id}: {e}")
            # Return sample text if download fails
            return self._sample_text()
    
    def _clean_text(self, text: str) -> str:
        """Clean Project Gutenberg text"""
        # Remove Gutenberg headers/footers
        text = re.sub(r'\*\*\* START OF (THIS|THE) PROJECT GUTENBERG.*?\*\*\*', '', text, flags=re.DOTALL)
        text = re.sub(r'\*\*\* END OF (THIS|THE) PROJECT GUTENBERG.*?\*\*\*', '', text, flags=re.DOTALL)
        
        # Normalize whitespace
        text = re.sub(r'\n+', '\n', text)
        text = re.sub(r'[ \t]+', ' ', text)
        
        return text.strip()
    
    def _sample_text(self) -> str:
        """Sample text if download fails"""
        return """
        It is a truth universally acknowledged, that a single man in possession 
        of a good fortune, must be in want of a wife. However little known the 
        feelings or views of such a man may be on his first entering a neighbourhood, 
        this truth is so well fixed in the minds of the surrounding families, that 
        he is considered the rightful property of some one or other of their daughters.
        """
    
    def _text_to_semantic_vector(self, text: str) -> np.ndarray:
        """Convert text to semantic feature vector"""
        # Character frequency features
        text_lower = text.lower()
        
        # Letter frequencies
        letter_freq = np.array([
            text_lower.count(c) / max(len(text), 1)
            for c in 'etaoinshrdlcumwfgypbvkjxqz'
        ])
        
        # Punctuation patterns
        punct_freq = np.array([
            text.count(c) / max(len(text), 1)
            for c in '.,;:!?"\'()-'
        ])
        
        # Word length distribution
        words = text.split()
        avg_word_len = np.mean([len(w) for w in words]) if words else 0
        
        # Sentence patterns
        sentences = re.split(r'[.!?]+', text)
        avg_sent_len = np.mean([len(s.split()) for s in sentences if s.strip()]) if sentences else 0
        
        # Combine features
        features = np.concatenate([
            letter_freq,
            punct_freq,
            [avg_word_len / 20, avg_sent_len / 50, len(words) / 1000]
        ])
        
        return features[:32]  # Limit to 32 features
    
    def _encode_to_ternary(self, features: np.ndarray, book_name: str) -> List[List[int]]:
        """Encode features to 32x32x32 ternary hotspots"""
        hotspots = []
        
        # Normalize
        features = (features - features.mean()) / (features.std() + 1e-8)
        
        # Book hash for spatial distribution
        book_hash = int(hashlib.md5(book_name.encode()).hexdigest(), 16)
        z_base = book_hash % 24
        
        for i, val in enumerate(features[:32]):
            if abs(val) > 0.2:  # Threshold
                t = 1 if val > 0 else -1
                x = (book_hash + i * 17) % 32
                y = (book_hash + i * 23) % 32
                z = (z_base + i * 3) % 32
                hotspots.append([x, y, z, t])
        
        return hotspots
    
    def _chunk_text(self, text: str, chunk_size: int = 500) -> List[str]:
        """Split text into chunks"""
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), chunk_size):
            chunk = ' '.join(words[i:i+chunk_size])
            chunks.append(chunk)
        
        return chunks
    
    def feed_book(self, book_name: str, chunks: int = 10) -> Dict:
        """Feed a book to the brain"""
        print(f"\n{'='*60}")
        print(f"  FEEDING: {book_name.upper()}")
        print(f"{'='*60}")
        
        # Get book ID
        book_id = self.BOOKS.get(book_name, '1342')  # Default to Pride & Prejudice
        
        # Download
        text = self.download_book(book_id)
        
        # Chunk
        text_chunks = self._chunk_text(text, 1000)[:chunks]
        
        print(f"Feeding {len(text_chunks)} chunks...")
        
        results = []
        for i, chunk in enumerate(text_chunks):
            # Extract features
            features = self._text_to_semantic_vector(chunk)
            
            # Encode
            hotspots = self._encode_to_ternary(features, book_name)
            
            # Send to brain
            result = self._send('cortex_write', {
                'agent_id': self.agent_id,
                'regions': list(range(8)),
                'activations': hotspots,
                'priority': 0.6,
                'ephemeral': False
            })
            
            # Trigger
            self._send('cortex_tick', {})
            
            results.append({
                'chunk': i+1,
                'hotspots': len(hotspots),
                'written': result.get('write_result', {}).get('written', 0)
            })
            
            self.stats['fed'] += 1
            
            # Progress
            if (i+1) % 5 == 0:
                print(f"  Chunk {i+1}/{len(text_chunks)}: {len(hotspots)} hotspots")
            
            time.sleep(0.2)
        
        return {'book': book_name, 'chunks_fed': len(results), 'results': results}
    
    def feed_library(self, books: List[str] = None):
        """Feed multiple books"""
        if books is None:
            books = ['pride_prejudice', 'moby_dick', 'frankenstein']
        
        print(f"\n{'='*70}")
        print(f"  GUTENBERG LIBRARY FEED")
        print(f"  Books: {len(books)}")
        print(f"{'='*70}\n")
        
        # Register
        reg = self._send('cortex_register', {'agent_id': self.agent_id})
        print(f"Registration: {reg}\n")
        
        results = []
        for book in books:
            try:
                result = self.feed_book(book, chunks=5)
                results.append(result)
            except Exception as e:
                print(f"Error feeding {book}: {e}")
            time.sleep(1)
        
        # Summary
        print(f"\n{'='*70}")
        print(f"  LIBRARY FEED COMPLETE")
        print(f"  Books: {len(results)}")
        print(f"  Chunks: {self.stats['fed']}")
        print(f"  Downloaded: {self.stats['downloaded']}")
        print(f"  Bytes: {self.stats['bytes']:,}")
        print(f"{'='*70}\n")
        
        return results

def main():
    feeder = GutenbergFeeder()
    
    # Feed classic literature
    books = [
        'pride_prejudice',   # Jane Austen
        'moby_dick',         # Herman Melville
        'frankenstein',      # Mary Shelley
    ]
    
    feeder.feed_library(books)
    
    # Check brain
    print("\nChecking brain integration...")
    status = feeder._send('status', {})
    agents = status.get('cortex', {}).get('agents', {})
    
    if feeder.agent_id in agents:
        stats = agents[feeder.agent_id]
        print(f"✓ {feeder.agent_id} registered!")
        print(f"  Writes: {stats['writes']}")
        print(f"  Reads: {stats['reads']}")

if __name__ == "__main__":
    main()
