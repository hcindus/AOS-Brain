#!/usr/bin/env python3
"""
Auto-Crawl RAG System for psdepot.com
Crawls website content and stores in vector knowledge base for AI retrieval
"""

import sqlite3
import json
import re
import requests
from urllib.parse import urljoin, urlparse
from datetime import datetime
from pathlib import Path
import hashlib
import time

class PSDepotCrawler:
    """Crawler for psdepot.com knowledge base"""
    
    BASE_URL = "https://psdepot.com"
    DB_PATH = "/root/.openclaw/workspace/data/psdepot_kb.db"
    
    # Pages to crawl
    PAGES_TO_CRAWL = [
        "/",
        "/about.html",
        "/products/",
        "/products/thermal-paper.html",
        "/products/ink-ribbons.html",
        "/products/pos-systems.html",
        "/products/scales.html",
        "/services.html",
        "/contact.html",
        "/support.html",
    ]
    
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.init_db()
    
    def init_db(self):
        """Initialize the knowledge base database"""
        Path(self.DB_PATH).parent.mkdir(parents=True, exist_ok=True)
        
        self.conn = sqlite3.connect(self.DB_PATH)
        self.cursor = self.conn.cursor()
        
        # Documents table - stores crawled content
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT UNIQUE NOT NULL,
                title TEXT,
                content TEXT,
                content_hash TEXT,
                crawled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Chunks table - stores searchable chunks
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS chunks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                doc_id INTEGER,
                chunk_text TEXT,
                chunk_hash TEXT UNIQUE,
                FOREIGN KEY (doc_id) REFERENCES documents(id)
            )
        """)
        
        # Crawl log
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS crawl_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP,
                pages_crawled INTEGER DEFAULT 0,
                pages_failed INTEGER DEFAULT 0,
                status TEXT DEFAULT 'running'
            )
        """)
        
        self.conn.commit()
    
    def crawl_page(self, path: str) -> dict:
        """Crawl a single page and extract content"""
        url = urljoin(self.BASE_URL, path)
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (compatible; PSDepotBot/1.0)'
            }
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            html = response.text
            
            # Extract title
            title_match = re.search(r'<title[^>]*>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
            title = title_match.group(1).strip() if title_match else "No title"
            
            # Clean title
            title = re.sub(r'\s+', ' ', title)
            
            # Extract main content (simplified)
            # Remove script and style tags
            content = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
            content = re.sub(r'<style[^>]*>.*?</style>', '', content, flags=re.DOTALL | re.IGNORECASE)
            
            # Extract text from common content areas
            content = re.sub(r'<[^>]+>', ' ', content)
            content = re.sub(r'\s+', ' ', content)
            content = content.strip()
            
            # Calculate hash
            content_hash = hashlib.sha256(content.encode()).hexdigest()[:32]
            
            return {
                'url': url,
                'title': title,
                'content': content,
                'content_hash': content_hash,
                'success': True
            }
            
        except Exception as e:
            return {
                'url': url,
                'error': str(e),
                'success': False
            }
    
    def chunk_content(self, content: str, chunk_size: int = 500) -> list:
        """Split content into searchable chunks"""
        # Simple sentence-based chunking
        sentences = re.split(r'(?<=[.!?])\s+', content)
        chunks = []
        current_chunk = []
        current_size = 0
        
        for sentence in sentences:
            if current_size + len(sentence) > chunk_size and current_chunk:
                chunks.append(' '.join(current_chunk))
                current_chunk = [sentence]
                current_size = len(sentence)
            else:
                current_chunk.append(sentence)
                current_size += len(sentence) + 1
        
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        return chunks
    
    def store_document(self, doc: dict) -> bool:
        """Store or update a document in the database"""
        if not doc.get('success'):
            return False
        
        try:
            # Check if document exists and content changed
            self.cursor.execute(
                "SELECT id, content_hash FROM documents WHERE url = ?",
                (doc['url'],)
            )
            existing = self.cursor.fetchone()
            
            if existing:
                doc_id, old_hash = existing
                if old_hash == doc['content_hash']:
                    # Content unchanged, just update timestamp
                    self.cursor.execute(
                        "UPDATE documents SET last_updated = CURRENT_TIMESTAMP WHERE id = ?",
                        (doc_id,)
                    )
                    self.conn.commit()
                    return True
                else:
                    # Content changed, delete old chunks and update
                    self.cursor.execute("DELETE FROM chunks WHERE doc_id = ?", (doc_id,))
                    self.cursor.execute(
                        """UPDATE documents 
                           SET title = ?, content = ?, content_hash = ?, last_updated = CURRENT_TIMESTAMP
                           WHERE id = ?""",
                        (doc['title'], doc['content'], doc['content_hash'], doc_id)
                    )
            else:
                # New document
                self.cursor.execute(
                    """INSERT INTO documents (url, title, content, content_hash)
                       VALUES (?, ?, ?, ?)""",
                    (doc['url'], doc['title'], doc['content'], doc['content_hash'])
                )
                doc_id = self.cursor.lastrowid
            
            # Create chunks
            chunks = self.chunk_content(doc['content'])
            for chunk in chunks:
                chunk_hash = hashlib.sha256(chunk.encode()).hexdigest()[:32]
                self.cursor.execute(
                    """INSERT OR IGNORE INTO chunks (doc_id, chunk_text, chunk_hash)
                       VALUES (?, ?, ?)""",
                    (doc_id, chunk, chunk_hash)
                )
            
            self.conn.commit()
            return True
            
        except Exception as e:
            print(f"Error storing document: {e}")
            return False
    
    def crawl_all(self) -> dict:
        """Crawl all pages and store in knowledge base"""
        # Start crawl log
        self.cursor.execute(
            "INSERT INTO crawl_log (status) VALUES ('running')"
        )
        crawl_id = self.cursor.lastrowid
        self.conn.commit()
        
        results = {
            'crawled': 0,
            'failed': 0,
            'pages': []
        }
        
        for path in self.PAGES_TO_CRAWL:
            print(f"Crawling: {path}")
            doc = self.crawl_page(path)
            
            if doc['success']:
                if self.store_document(doc):
                    results['crawled'] += 1
                    results['pages'].append({
                        'url': doc['url'],
                        'title': doc['title'],
                        'status': 'success'
                    })
                    print(f"  ✓ {doc['title']}")
                else:
                    results['failed'] += 1
                    results['pages'].append({
                        'url': doc['url'],
                        'status': 'storage_failed'
                    })
            else:
                results['failed'] += 1
                results['pages'].append({
                    'url': doc['url'],
                    'error': doc.get('error'),
                    'status': 'failed'
                })
                print(f"  ✗ Failed: {doc.get('error')}")
            
            time.sleep(0.5)  # Be nice to the server
        
        # Update crawl log
        self.cursor.execute(
            """UPDATE crawl_log 
               SET completed_at = CURRENT_TIMESTAMP, 
                   pages_crawled = ?, 
                   pages_failed = ?, 
                   status = 'completed'
               WHERE id = ?""",
            (results['crawled'], results['failed'], crawl_id)
        )
        self.conn.commit()
        
        return results
    
    def search(self, query: str, limit: int = 5) -> list:
        """Search the knowledge base for relevant content"""
        query_lower = query.lower()
        
        # Simple keyword search (can be enhanced with embeddings)
        self.cursor.execute("""
            SELECT c.chunk_text, d.title, d.url
            FROM chunks c
            JOIN documents d ON c.doc_id = d.id
            WHERE LOWER(c.chunk_text) LIKE ?
            ORDER BY LENGTH(c.chunk_text) DESC
            LIMIT ?
        """, (f'%{query_lower}%', limit))
        
        results = []
        for row in self.cursor.fetchall():
            results.append({
                'text': row[0],
                'title': row[1],
                'url': row[2]
            })
        
        return results
    
    def get_stats(self) -> dict:
        """Get knowledge base statistics"""
        self.cursor.execute("SELECT COUNT(*) FROM documents")
        doc_count = self.cursor.fetchone()[0]
        
        self.cursor.execute("SELECT COUNT(*) FROM chunks")
        chunk_count = self.cursor.fetchone()[0]
        
        self.cursor.execute(
            "SELECT MAX(crawled_at) FROM documents"
        )
        last_crawl = self.cursor.fetchone()[0]
        
        return {
            'documents': doc_count,
            'chunks': chunk_count,
            'last_crawl': last_crawl
        }
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()


def main():
    """Main entry point for CLI usage"""
    import sys
    
    crawler = PSDepotCrawler()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'crawl':
            print("Starting crawl of psdepot.com...")
            results = crawler.crawl_all()
            print(f"\nCrawl complete!")
            print(f"  Pages crawled: {results['crawled']}")
            print(f"  Pages failed: {results['failed']}")
            
        elif command == 'search':
            if len(sys.argv) < 3:
                print("Usage: auto_crawl_rag.py search <query>")
                return
            query = ' '.join(sys.argv[2:])
            results = crawler.search(query)
            print(f"Search results for: {query}\n")
            for i, r in enumerate(results, 1):
                print(f"{i}. [{r['title']}]")
                print(f"   {r['text'][:200]}...")
                print(f"   URL: {r['url']}\n")
                
        elif command == 'stats':
            stats = crawler.get_stats()
            print(f"Knowledge Base Stats:")
            print(f"  Documents: {stats['documents']}")
            print(f"  Chunks: {stats['chunks']}")
            print(f"  Last crawl: {stats['last_crawl']}")
            
        else:
            print(f"Unknown command: {command}")
            print("Commands: crawl, search, stats")
    else:
        print("PSDepot Auto-Crawl RAG System")
        print("Commands:")
        print("  crawl           - Crawl all pages")
        print("  search <query>  - Search knowledge base")
        print("  stats           - Show statistics")
    
    crawler.close()


if __name__ == "__main__":
    main()