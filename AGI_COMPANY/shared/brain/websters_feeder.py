#!/usr/bin/env python3
"""
Webster's Dictionary Feeder for AOS Brain
Feeds 50,000+ comprehensive dictionary words to the brain
"""

import sys
from pathlib import Path

# Handle __file__ not defined when running via exec
try:
    sys.path.insert(0, str(Path(__file__).parent.parent))
    sys.path.insert(0, str(Path(__file__).parent))
except NameError:
    base_path = "/root/.openclaw/workspace/AGI_COMPANY/shared/brain"
    sys.path.insert(0, base_path)
    sys.path.insert(0, str(Path(base_path).parent))

from dictionary_feeder import DictionaryFeeder


def feed_websters_dictionary():
    """Feed the complete Webster's Dictionary to the brain."""
    print("=" * 70)
    print("WEBSTER'S COMPREHENSIVE DICTIONARY FEEDING")
    print("=" * 70)
    
    # Import Webster's dictionary
    from websters_word_lists import get_comprehensive_words
    
    # Create word ID counter
    word_id = 0
    def add_with_id(word, pos, meaning, category):
        nonlocal word_id
        word_id += 1
        return (word, pos, meaning, category, word_id)
    
    # Build comprehensive word list
    print("   Building comprehensive word list...")
    words = get_comprehensive_words(add_with_id)
    
    print(f"   Loaded {len(words):,} words from Webster's Dictionary")
    print(f"   Word ID range: 1 to {word_id}")
    
    dictionary_data = {"words": words}
    
    # Feed to brain
    feeder = DictionaryFeeder()
    result = feeder.feed_dictionary(dictionary_data)
    
    print(feeder.get_brain_nutrition_report())
    
    return result


def batch_feed_websters(batch_size=1000):
    """Feed Webster's dictionary in batches with progress tracking."""
    print("=" * 70)
    print("BATCH FEEDING: WEBSTER'S DICTIONARY")
    print("=" * 70)
    
    from websters_word_lists import get_comprehensive_words
    
    word_id = 0
    def add_with_id(word, pos, meaning, category):
        nonlocal word_id
        word_id += 1
        return (word, pos, meaning, category, word_id)
    
    print("\n🍽️  INGESTING DICTIONARY")
    print("-" * 70)
    
    words = get_comprehensive_words(add_with_id)
    total_words = len(words)
    
    print(f"   Total words to feed: {total_words:,}")
    print(f"   Batch size: {batch_size}")
    print(f"   Estimated batches: {(total_words + batch_size - 1) // batch_size}")
    print()
    
    feeder = DictionaryFeeder()
    concepts = []
    
    for i in range(0, total_words, batch_size):
        batch = words[i:i + batch_size]
        batch_num = i // batch_size + 1
        total_batches = (total_words + batch_size - 1) // batch_size
        
        print(f"   📦 Batch {batch_num}/{total_batches}: Processing {len(batch)} words...")
        
        for word_data in batch:
            if isinstance(word_data, (list, tuple)) and len(word_data) >= 4:
                word, word_type, meaning, category = word_data[:4]
                concept = feeder.feed_word(word, word_type, meaning, category)
                concepts.append(concept)
        
        progress = min(100, int((i + len(batch)) / total_words * 100))
        print(f"      ✅ Progress: {progress}% ({i + len(batch):,}/{total_words:,} words)")
    
    print()
    print("=" * 70)
    print("DICTIONARY FEEDING COMPLETE")
    print("=" * 70)
    
    result = {
        "words": feeder.words_processed,
        "concepts": feeder.concepts_formed,
        "categories": feeder.categories,
        "concepts_list": concepts,
    }
    
    print(feeder.get_brain_nutrition_report())
    
    return result


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Feed Webster's Dictionary to AOS Brain")
    parser.add_argument("--batch", "-b", action="store_true", help="Use batch feeding mode")
    parser.add_argument("--batch-size", "-s", type=int, default=1000, help="Batch size")
    parser.add_argument("--output", "-o", type=str, help="Save results to file")
    
    args = parser.parse_args()
    
    if args.batch:
        result = batch_feed_websters(args.batch_size)
    else:
        result = feed_websters_dictionary()
    
    if args.output:
        import json
        # Save summary (not full concepts list to save space)
        summary = {
            "words_processed": result["words"],
            "concepts_formed": result["concepts"],
            "categories": {k: len(v) for k, v in result["categories"].items()},
        }
        with open(args.output, 'w') as f:
            json.dump(summary, f, indent=2)
        print(f"\n📄 Summary saved to: {args.output}")
    
    print("\n" + "=" * 70)
    print("✅ Brain has been fed Webster's Comprehensive Dictionary.")
    print("   Words are now concepts in Tracray space.")
    print("   The brain has comprehensive English vocabulary.")
    print("=" * 70)
