#!/usr/bin/env python3
"""
GUTENBERG CORPUS FEEDER v1.0
Feeds Project Gutenberg literature into AOS Brain v4.5

Categories prioritized:
1. Classics of Literature
2. American/British/German/French/Russian Literature
3. Science & Technology
4. Philosophy & Ethics
5. History (all periods)
6. Biographies
7. Essays, Letters & Speeches
8. Poetry
9. Plays/Films/Dramas
10. Adventure

Pipeline: Gutenberg → Liver (filter) → Stomach (digest) → Brain (learn) → Kidneys (recycle)
"""

import json
import socket
import time
import random
import sys
import os
from pathlib import Path
from urllib.parse import urljoin, quote
from typing import Optional, Dict, List, Tuple

# Configuration
GUTENBERG_BASE = "https://www.gutenberg.org"
BRAIN_SOCKET = "/tmp/aos_brain.sock"
FEED_LOG = "/var/log/aos/gutenberg_feed.log"
PROGRESS_FILE = "/var/lib/aos/brain_state/gutenberg_progress.json"

# High-priority categories with their Gutenberg browse IDs
PRIORITY_CATEGORIES = [
    ("Classics of Literature", "books/search/?query=classics&sort_order=downloads"),
    ("American Literature", "ebooks/bookshelf/48"),  # American
    ("British Literature", "ebooks/bookshelf/62"),  # British
    ("German Literature", "ebooks/bookshelf/78"),   # German
    ("French Literature", "ebooks/bookshelf/75"),     # French
    ("Russian Literature", "ebooks/bookshelf/88"),    # Russian
    ("Poetry", "ebooks/bookshelf/21"),
    ("Adventure", "ebooks/bookshelf/6"),
    ("Biographies", "ebooks/bookshelf/10"),
    ("Philosophy", "ebooks/bookshelf/88"),
    ("History", "ebooks/bookshelf/28"),
    ("Essays", "ebooks/bookshelf/33"),
    ("Plays/Dramas", "ebooks/bookshelf/20"),
    ("Science", "ebooks/bookshelf/83"),
    ("Technology", "ebooks/bookshelf/100"),
    ("Short Stories", "ebooks/bookshelf/25"),
]

# Classic must-reads (book IDs from Gutenberg)
ESSENTIAL_WORKS = [
    # Literature
    (1342, "Pride and Prejudice - Jane Austen", 0.95),
    (11, "Alice's Adventures in Wonderland - Lewis Carroll", 0.9),
    (1661, "The Adventures of Sherlock Holmes - Arthur Conan Doyle", 0.92),
    (74, "The Adventures of Tom Sawyer - Mark Twain", 0.88),
    (76, "Adventures of Huckleberry Finn - Mark Twain", 0.9),
    (844, "The Picture of Dorian Gray - Oscar Wilde", 0.88),
    (98, "A Tale of Two Cities - Charles Dickens", 0.9),
    (2701, "Moby Dick - Herman Melville", 0.88),
    (120, "Treasure Island - Robert Louis Stevenson", 0.87),
    (174, "The Count of Monte Cristo - Alexandre Dumas", 0.9),
    (1400, "Great Expectations - Charles Dickens", 0.88),
    (1260, "Jane Eyre - Charlotte Brontë", 0.88),
    (5197, "Little Women - Louisa May Alcott", 0.85),
    (2641, "A Room with a View - E.M. Forster", 0.83),
    (145, "Middlemarch - George Eliot", 0.85),
    
    # Philosophy & Science
    (1228, "Thus Spake Zarathustra - Nietzsche", 0.92),
    (1497, "The Republic - Plato", 0.95),
    (1232, "Leviathan - Thomas Hobbes", 0.88),
    (35, "The Time Machine - H.G. Wells", 0.85),
    (36, "The War of the Worlds - H.G. Wells", 0.85),
    (84, "Frankenstein - Mary Shelley", 0.88),
    (55, "The Wonderful Wizard of Oz - L. Frank Baum", 0.82),
    (5200, "Metamorphosis - Franz Kafka", 0.9),
    (203, "Uncle Tom's Cabin - Harriet Beecher Stowe", 0.87),
    (205, "Walden - Henry David Thoreau", 0.9),
    (12341, "Democracy in America - Tocqueville", 0.88),
    (3300, "The Prince - Machiavelli", 0.88),
    
    # Science
    (164, "The Origin of Species - Charles Darwin", 0.95),
    (5001, "The Art of War - Sun Tzu", 0.9),
    (2814, "Dialogues Concerning Natural Religion - Hume", 0.85),
    (1659, "Meditations - Marcus Aurelius", 0.9),
    (3825, "The Confessions of St. Augustine", 0.85),
]


def log(message: str):
    """Log to console and file"""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())
    line = f"[{timestamp}] {message}"
    print(line)
    
    os.makedirs(os.path.dirname(FEED_LOG), exist_ok=True)
    with open(FEED_LOG, "a") as f:
        f.write(line + "\n")


def send_to_brain(cmd: str, params: Optional[Dict] = None) -> Dict:
    """Send command to brain via Unix socket"""
    try:
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.settimeout(10)
        sock.connect(BRAIN_SOCKET)
        
        request = {"cmd": cmd}
        if params:
            request["params"] = params
        
        sock.sendall(json.dumps(request).encode() + b'\n')
        
        response = b''
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            response += chunk
            if len(chunk) < 4096:
                break
        
        sock.close()
        return json.loads(response.decode())
    except Exception as e:
        return {"error": str(e)}


def get_book_text(gutenberg_id: int) -> Optional[str]:
    """Fetch book text from Gutenberg (plain text .txt)"""
    import urllib.request
    import urllib.error
    
    # Try multiple URL formats
    urls = [
        f"{GUTENBERG_BASE}/files/{gutenberg_id}/{gutenberg_id}-0.txt",
        f"{GUTENBERG_BASE}/files/{gutenberg_id}/{gutenberg_id}.txt",
        f"{GUTENBERG_BASE}/ebooks/{gutenberg_id}.txt.utf-8",
    ]
    
    headers = {
        'User-Agent': 'GutenbergFeeder/1.0 (Educational Research)',
        'Accept': 'text/plain, text/html',
    }
    
    for url in urls:
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=30) as response:
                text = response.read().decode('utf-8', errors='ignore')
                # Skip Project Gutenberg header/license
                lines = text.split('\n')
                content_start = 0
                for i, line in enumerate(lines):
                    if "*** START OF" in line or "***START OF" in line:
                        content_start = i + 1
                        break
                return '\n'.join(lines[content_start:content_start + 5000])  # First ~5000 lines
        except:
            continue
    
    return None


def chunk_text(text: str, chunk_size: int = 2000) -> List[str]:
    """Split text into digestible chunks"""
    chunks = []
    words = text.split()
    current_chunk = []
    current_len = 0
    
    for word in words:
        current_chunk.append(word)
        current_len += len(word) + 1
        if current_len >= chunk_size:
            chunks.append(' '.join(current_chunk))
            current_chunk = []
            current_len = 0
    
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    
    return chunks


def feed_content_to_brain(source: str, content: str, importance: float = 0.7) -> bool:
    """Feed content through brain pipeline"""
    try:
        # Send to brain's ingest command
        result = send_to_brain("ingest", {
            "source": source,
            "content": content[:2000],  # Truncate for brain processing
            "priority": importance
        })
        
        if result.get('ingested'):
            return True
        else:
            log(f"  ⚠️ Ingest failed: {result.get('error', 'unknown')}")
            return False
            
    except Exception as e:
        log(f"  ❌ Error feeding content: {e}")
        return False


def load_progress() -> Dict:
    """Load feeding progress"""
    try:
        with open(PROGRESS_FILE, 'r') as f:
            return json.load(f)
    except:
        return {
            "fed_books": [],
            "fed_categories": [],
            "total_chunks_fed": 0,
            "started_at": time.time()
        }


def save_progress(progress: Dict):
    """Save feeding progress"""
    os.makedirs(os.path.dirname(PROGRESS_FILE), exist_ok=True)
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(progress, f, indent=2)


def feed_essential_works():
    """Feed essential must-read works"""
    log("=" * 70)
    log("PHASE 1: Feeding Essential Works")
    log("=" * 70)
    
    progress = load_progress()
    fed_books = set(progress.get("fed_books", []))
    total_chunks = progress.get("total_chunks_fed", 0)
    
    for book_id, title, importance in ESSENTIAL_WORKS:
        if str(book_id) in fed_books:
            log(f"  ⏭️  Already fed: {title}")
            continue
        
        log(f"\n  📖 [{book_id}] {title} (importance: {importance})")
        
        # Fetch book
        text = get_book_text(book_id)
        if not text:
            log(f"  ❌ Failed to fetch book {book_id}")
            continue
        
        log(f"  📄 Fetched {len(text):,} characters")
        
        # Chunk and feed
        chunks = chunk_text(text)
        log(f"  🍽️  Feeding {len(chunks)} chunks...")
        
        fed_count = 0
        for i, chunk in enumerate(chunks[:50]):  # Max 50 chunks per book
            success = feed_content_to_brain(
                source=f"gutenberg:{book_id}:{title}",
                content=chunk,
                importance=importance
            )
            if success:
                fed_count += 1
                total_chunks += 1
            
            if i % 10 == 9:
                log(f"    ... {i+1}/{min(len(chunks), 50)} chunks fed")
            
            time.sleep(0.5)  # Rate limiting
        
        fed_books.add(str(book_id))
        progress["fed_books"] = list(fed_books)
        progress["total_chunks_fed"] = total_chunks
        save_progress(progress)
        
        log(f"  ✅ Fed {fed_count} chunks from '{title}'")
        log(f"  📊 Total chunks fed so far: {total_chunks:,}")
        
        # Brief pause between books
        time.sleep(2)
    
    log("\n" + "=" * 70)
    log("PHASE 1 COMPLETE")
    log("=" * 70)


def feed_curriculum_categories():
    """Feed from category curriculum"""
    log("\n" + "=" * 70)
    log("PHASE 2: Category-Based Feeding")
    log("=" * 70)
    
    progress = load_progress()
    
    for category_name, browse_path in PRIORITY_CATEGORIES[:10]:
        if category_name in progress.get("fed_categories", []):
            log(f"  ⏭️  Already processed: {category_name}")
            continue
        
        log(f"\n  📚 Category: {category_name}")
        log(f"  🔗 Path: {browse_path}")
        
        # For now, feed category metadata as signal
        # In future, could scrape actual book IDs from category pages
        meta_content = f"Category: {category_name}. Literary corpus from Project Gutenberg. " \
                      f"High-value cultural and historical texts for pattern recognition and knowledge synthesis."
        
        feed_content_to_brain(
            source=f"gutenberg:category:{category_name}",
            content=meta_content,
            importance=0.85
        )
        
        progress["fed_categories"] = progress.get("fed_categories", []) + [category_name]
        save_progress(progress)
        
        time.sleep(0.5)
    
    log("\n" + "=" * 70)
    log("PHASE 2 COMPLETE")
    log("=" * 70)


def main():
    """Main feeder entry point"""
    log("=" * 70)
    log("GUTENBERG CORPUS FEEDER v1.0")
    log("Feeding Project Gutenberg literature into AOS Brain v4.5")
    log("=" * 70)
    
    # Check brain is alive
    status = send_to_brain("status")
    if status.get('error'):
        log(f"❌ Brain not responding: {status['error']}")
        sys.exit(1)
    
    tick = status.get('tick', 0)
    log(f"✅ Brain connected (tick: {tick:,})")
    log(f"📊 Current TracRay episodes: {status.get('tracray', {}).get('episodes', 0):,}")
    log(f"🫘 Kidneys bladder: {status.get('kidneys', {}).get('bladder_level', 0)}/500")
    
    progress = load_progress()
    if progress.get("fed_books"):
        log(f"📚 Previously fed: {len(progress['fed_books'])} books, {progress['total_chunks_fed']:,} chunks")
    
    log("\n" + "-" * 70)
    
    # Phase 1: Essential works
    feed_essential_works()
    
    # Phase 2: Categories
    feed_curriculum_categories()
    
    # Final status
    log("\n" + "=" * 70)
    log("FEEDING COMPLETE")
    log("=" * 70)
    
    final_status = send_to_brain("status")
    final_tick = final_status.get('tick', 0)
    
    progress = load_progress()
    log(f"\n📊 Final Statistics:")
    log(f"  Books fed: {len(progress.get('fed_books', []))}")
    log(f"  Total chunks: {progress.get('total_chunks_fed', 0):,}")
    log(f"  Categories: {len(progress.get('fed_categories', []))}")
    log(f"  Brain ticks: {tick:,} → {final_tick:,} (+{final_tick - tick:,})")
    
    log("\n✅ Gutenberg corpus feeding complete!")
    log("=" * 70)


if __name__ == "__main__":
    main()
