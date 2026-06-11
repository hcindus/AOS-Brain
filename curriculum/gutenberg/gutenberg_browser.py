#!/usr/bin/env python3
"""
Project Gutenberg Bookshelf Browser
Systematically browse categories and extract text links
"""

import json
from pathlib import Path
from typing import List, Dict
from datetime import datetime

# Known Project Gutenberg Bookshelf IDs for our categories
BOOKSHELF_IDS = {
    # Engineering & Technology
    "engineering_technology": [
        671,  # Engineering
        672,  # Technology
        673,  # Electrical Engineering
        674,  # Mechanical Engineering
        675,  # Civil Engineering
    ],
    # Philosophy & Ethics
    "philosophy_ethics": [
        57,   # Philosophy
        58,   # Ethics
        59,   # Logic
        60,   # Metaphysics
    ],
    # Science
    "science_biology": [
        39,   # Biology
        40,   # Botany
        41,   # Zoology
        42,   # Anatomy
    ],
    "science_physics": [
        44,   # Physics
        45,   # Astronomy
        46,   # Chemistry
    ],
    # Mathematics
    "mathematics": [
        47,   # Mathematics
        48,   # Geometry
        49,   # Algebra
        50,   # Calculus
    ],
    # Business
    "business": [
        35,   # Business
        36,   # Economics
        37,   # Accounting
    ],
    # Psychology
    "psychology": [
        62,   # Psychology
        63,   # Psychiatry
    ],
    # History
    "history": [
        18,   # History
        19,   # Ancient History
        20,   # Medieval History
        21,   # Modern History
    ],
}

class GutenbergBrowser:
    """Browse and catalog Project Gutenberg bookshelves"""
    
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.catalog_file = output_dir / "bookshelf_catalog.json"
        self.catalog = self._load_catalog()
    
    def _load_catalog(self) -> Dict:
        if self.catalog_file.exists():
            return json.loads(self.catalog_file.read_text())
        return {
            "created": datetime.now().isoformat(),
            "categories": {},
            "total_books": 0
        }
    
    def _save_catalog(self):
        self.catalog["last_updated"] = datetime.now().isoformat()
        self.catalog_file.write_text(json.dumps(self.catalog, indent=2))
    
    def generate_urls(self) -> List[Dict]:
        """Generate URLs to browse"""
        urls = []
        for category_name, shelf_ids in BOOKSHELF_IDS.items():
            for shelf_id in shelf_ids:
                urls.append({
                    "category": category_name,
                    "shelf_id": shelf_id,
                    "url": f"https://www.gutenberg.org/ebooks/bookshelf/{shelf_id}",
                    "status": "pending"
                })
        return urls
    
    def add_manual_entry(self, category: str, title: str, author: str, 
                        book_id: int, notes: str = ""):
        """Add manually discovered book"""
        if category not in self.catalog["categories"]:
            self.catalog["categories"][category] = {
                "books": [],
                "shelf_ids": BOOKSHELF_IDS.get(category, [])
            }
        
        book = {
            "title": title,
            "author": author,
            "id": book_id,
            "url": f"https://www.gutenberg.org/ebooks/{book_id}",
            "text_url": f"https://www.gutenberg.org/files/{book_id}/{book_id}-0.txt",
            "added": datetime.now().isoformat(),
            "notes": notes,
            "ingested": False
        }
        
        self.catalog["categories"][category]["books"].append(book)
        self.catalog["total_books"] += 1
        self._save_catalog()
        
        return book
    
    def get_reading_list(self, priority_categories: List[str] = None) -> List[Dict]:
        """Get prioritized reading list"""
        if priority_categories is None:
            priority_categories = [
                "engineering_technology",
                "philosophy_ethics",
                "science_biology",
                "mathematics",
                "business",
                "psychology"
            ]
        
        reading_list = []
        for category in priority_categories:
            if category in self.catalog["categories"]:
                cat_data = self.catalog["categories"][category]
                for book in cat_data["books"]:
                    if not book.get("ingested", False):
                        reading_list.append({
                            "category": category,
                            **book
                        })
        
        return reading_list
    
    def mark_ingested(self, book_id: int):
        """Mark book as ingested"""
        for category, data in self.catalog["categories"].items():
            for book in data["books"]:
                if book["id"] == book_id:
                    book["ingested"] = True
                    book["ingested_date"] = datetime.now().isoformat()
                    self._save_catalog()
                    return True
        return False
    
    def export_summary(self) -> Dict:
        """Export catalog summary"""
        summary = {
            "total_books": self.catalog["total_books"],
            "categories": len(self.catalog["categories"]),
            "pending": sum(
                1 for cat in self.catalog["categories"].values()
                for book in cat["books"]
                if not book.get("ingested", False)
            ),
            "ingested": sum(
                1 for cat in self.catalog["categories"].values()
                for book in cat["books"]
                if book.get("ingested", False)
            ),
            "category_breakdown": {
                cat: len(data["books"])
                for cat, data in self.catalog["categories"].items()
            }
        }
        
        summary_file = self.output_dir / "catalog_summary.json"
        summary_file.write_text(json.dumps(summary, indent=2))
        
        return summary

if __name__ == "__main__":
    output = Path("/root/.openclaw/workspace/curriculum/gutenberg")
    browser = GutenbergBrowser(output)
    
    # Add priority texts we know exist
    priority_additions = [
        ("engineering_technology", "Kinematics of Machinery", "Franz Reuleaux", 33631, "Classic mechanical engineering"),
        ("engineering_technology", "Mechanical Movements and Novelties of Construction", "Gardner D. Hiscox", 34866, "Mechanical design patterns"),
        ("mathematics", "Flatland", "Edwin Abbott", 201, "Dimensionality"),
        ("philosophy_ethics", "The Republic", "Plato", 1497, "Governance structures"),
        ("philosophy_ethics", "Nicomachean Ethics", "Aristotle", 8438, "Virtue ethics"),
        ("science_biology", "On the Origin of Species", "Charles Darwin", 1228, "Evolution"),
        ("business", "The Art of War", "Sun Tzu", 132, "Strategy"),
        ("business", "The Wealth of Nations", "Adam Smith", 3300, "Economics"),
        ("psychology", "The Interpretation of Dreams", "Sigmund Freud", 66048, "Psychoanalysis"),
    ]
    
    for category, title, author, book_id, notes in priority_additions:
        try:
            browser.add_manual_entry(category, title, author, book_id, notes)
            print(f"✓ Added: {title}")
        except Exception as e:
            print(f"✗ Failed: {title} - {e}")
    
    # Export URLs to browse
    urls = browser.generate_urls()
    urls_file = output / "bookshelf_urls.json"
    urls_file.write_text(json.dumps(urls, indent=2))
    
    # Export summary
    summary = browser.export_summary()
    
    print("\n" + "="*60)
    print("GUTENBERG BROWSER CATALOG")
    print("="*60)
    print(f"\nTotal books: {summary['total_books']}")
    print(f"Pending: {summary['pending']}")
    print(f"Ingested: {summary['ingested']}")
    print(f"\nCategory breakdown:")
    for cat, count in summary['category_breakdown'].items():
        print(f"  {cat}: {count}")
    
    print(f"\nNext to ingest:")
    for book in browser.get_reading_list()[:5]:
        print(f"  - {book['title']} ({book['category']})")
    
    print(f"\nFiles:")
    print(f"  Catalog: {browser.catalog_file}")
    print(f"  URLs: {urls_file}")
    print(f"  Summary: {output / 'catalog_summary.json'}")
