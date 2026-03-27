#!/usr/bin/env python3
"""
20th Century Dictionary Feeder with Unconscious Sleep Processing.

Feeds the complete 20th Century English vocabulary to the brain,
with sleep cycles for memory consolidation and dream generation.
"""

import sys
import time
import random
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from brain.seven_region import SevenRegionBrain
from agents.century_dictionary import get_20th_century_dictionary


class CenturyDictionaryFeeder:
    """
    Feeds the 20th Century English Dictionary to the brain.
    
    Features:
    - 455 words from 1900-2000
    - Category-based feeding
    - Semantic categories for Tracray mapping
    """
    
    def __init__(self, brain: SevenRegionBrain):
        self.brain = brain
        self.dictionary = get_20th_century_dictionary()
        self.word_index = 0
        self.words_learned = 0
        self.categories_learned = {}
        
        print(f"[CenturyFeeder] Loaded {len(self.dictionary)} words from 20th Century")
        print(f"  Categories: emotion, abstract, time, space, technology, social, think, perceive, body, world")
        
    def feed_word(self) -> dict:
        """Feed one word to the brain."""
        if self.word_index >= len(self.dictionary):
            self.word_index = 0  # Loop back
        
        word_data = self.dictionary[self.word_index]
        word, pos, definition, category = word_data
        self.word_index += 1
        
        # Build rich feed message with category context
        message = f"[20th CENTURY] Word: '{word}' | Category: {category} | POS: {pos} | {definition}"
        
        # Feed to brain
        result = self.brain.feed(message, f"century_{category}")
        
        # Track category
        self.categories_learned[category] = self.categories_learned.get(category, 0) + 1
        self.words_learned += 1
        
        return {
            "word": word,
            "pos": pos,
            "category": category,
            "definition": definition,
            "brain_tick": self.brain.tick_count,
        }
    
    def feed_batch(self, count: int = 10) -> list:
        """Feed multiple words."""
        results = []
        
        for i in range(count):
            result = self.feed_word()
            results.append(result)
            time.sleep(0.05)
        
        return results
    
    def feed_category(self, category: str, count: int = 20) -> list:
        """Feed words from specific category."""
        category_words = [w for w in self.dictionary if len(w) > 3 and w[3] == category]
        
        if not category_words:
            print(f"Category '{category}' not found")
            return []
        
        print(f"\n📚 Feeding {min(count, len(category_words))} words from category: {category}")
        
        results = []
        for word_data in category_words[:count]:
            word, pos, definition, cat = word_data
            message = f"[CATEGORY: {category}] '{word}' ({pos}) - {definition}"
            result = self.brain.feed(message, f"century_{category}")
            results.append({
                "word": word,
                "pos": pos,
                "category": cat,
            })
            time.sleep(0.05)
        
        return results
    
    def run_continuous(self, words: int = 100):
        """Run continuous feeding."""
        print(f"\n🧠 FEEDING {words} WORDS FROM 20TH CENTURY")
        print("=" * 60)
        
        for i in range(words):
            result = self.feed_word()
            if i % 20 == 0:
                print(f"  [{i+1:3d}/{words}] {result['word']:15s} ({result['category']})")
        
        self._print_summary()
    
    def _print_summary(self):
        """Print learning summary."""
        print("\n" + "=" * 60)
        print("📊 LEARNING SUMMARY")
        print("=" * 60)
        print(f"Total words learned: {self.words_learned}")
        print(f"Brain ticks: {self.brain.tick_count}")
        print(f"\nBy category:")
        for cat, count in sorted(self.categories_learned.items(), key=lambda x: -x[1]):
            print(f"  {cat:15s}: {count:3d} words")
        print("=" * 60)


def demo_century_feeder():
    """Demo the Century Dictionary Feeder."""
    print("=" * 70)
    print("📚 20TH CENTURY DICTIONARY FEEDER")
    print("=" * 70)
    print()
    print("Feeding 455 words from the 20th Century English vocabulary")
    print("to the ternary brain with Tracray spatial mapping.")
    print()
    
    # Create brain
    brain = SevenRegionBrain()
    
    # Create feeder
    feeder = CenturyDictionaryFeeder(brain)
    
    # Demo 1: Quick feed
    print("PHASE 1: Quick Learning (40 words)")
    print("-" * 70)
    
    results = feeder.feed_batch(count=40)
    print(f"✅ Fed {len(results)} words")
    print(f"Brain tick count: {brain.tick_count}")
    
    # Demo 2: Category-based feeding
    print("\n" + "=" * 70)
    print("PHASE 2: Category-Based Learning")
    print("-" * 70)
    
    categories = ["emotion", "technology", "time", "abstract", "think"]
    for cat in categories:
        results = feeder.feed_category(cat, count=5)
        print(f"  {cat}: {len(results)} words")
    
    # Final summary
    print("\n" + "=" * 70)
    print("FINAL SUMMARY")
    print("=" * 70)
    feeder._print_summary()
    
    print("\n" + "=" * 70)
    print("✅ Demo complete!")
    print()
    print("Sample categories fed:")
    print("  - emotion: fear, love, joy, anger, peace")
    print("  - technology: computer, internet, television, robot")
    print("  - time: century, decade, moment, duration")
    print("  - abstract: reality, truth, beauty, meaning")
    print("  - think: mind, thought, idea, memory, dream")
    print("=" * 70)


if __name__ == "__main__":
    demo_century_feeder()
