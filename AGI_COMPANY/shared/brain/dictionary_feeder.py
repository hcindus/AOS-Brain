"""
Dictionary Feeder
Feeds the 20th Century Dictionary to the brain.

Words flow through:
1. Mouth (ingestion) - Load words
2. Stomach (processing) - Categorize, map to Tracray
3. Intestines (absorption) - Neural pathways form
4. Bloodstream (distribution) - Available to all regions
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

class DictionaryFeeder:
    """
    Feeds words to brain like nutrients.
    
    The brain "eats" words, digests them into concepts,
    and distributes them through Tracray spatial mapping.
    """
    
    def __init__(self):
        self.words_processed = 0
        self.concepts_formed = 0
        self.categories = {}
        
    def feed_word(self, word: str, word_type: str, meaning: str, category: str):
        """
        Feed a single word to the brain.
        
        Process:
        1. Identify concept space (category)
        2. Map to Tracray coordinates
        3. Form neural pathway
        4. Distribute to relevant brain regions
        """
        self.words_processed += 1
        
        # Categorize
        if category not in self.categories:
            self.categories[category] = []
        self.categories[category].append(word)
        
        # Map to spatial concept (Tracray-style)
        coord = self._map_to_space(category, word_type)
        
        # Form concept
        concept = {
            "word": word,
            "type": word_type,
            "meaning": meaning,
            "category": category,
            "coord": coord,
            "connections": [],
        }
        
        self.concepts_formed += 1
        
        return concept
        
    def _map_to_space(self, category: str, word_type: str) -> tuple:
        """Map word to 3D concept space"""
        # Category -> spatial region
        category_coords = {
            "self": (5, 4, 3),
            "social": (15, 8, 5),
            "world": (25, 12, 7),
            "abstract": (35, 16, 9),
            "space": (45, 20, 11),
            "time": (55, 24, 13),
            "emotion": (65, 28, 15),
            "action": (75, 32, 17),
        }
        
        base = category_coords.get(category, (50, 25, 10))
        
        # Word type -> offset
        type_offsets = {
            "pronoun": (0, 0, 0),
            "preposition": (2, 1, 0),
            "verb": (3, 2, 1),
            "noun": (4, 2, 1),
            "adjective": (5, 3, 1),
            "adverb": (6, 3, 2),
            "article": (1, 0, 0),
            "determiner": (2, 1, 0),
        }
        
        offset = type_offsets.get(word_type, (0, 0, 0))
        
        return (base[0] + offset[0], base[1] + offset[1], base[2] + offset[2])
        
    def feed_dictionary(self, dictionary_data: dict) -> dict:
        """
        Feed entire dictionary to brain.
        
        Returns:
            Digestion report
        """
        print("🍽️  FEEDING DICTIONARY TO BRAIN")
        print("=" * 70)
        
        words = dictionary_data.get("words", [])
        
        print(f"   Dictionary size: {len(words)} words")
        print(f"   Beginning ingestion...\n")
        
        concepts = []
        
        for i, word_data in enumerate(words):
            if isinstance(word_data, (list, tuple)) and len(word_data) >= 4:
                word, word_type, meaning, category = word_data[:4]
                concept = self.feed_word(word, word_type, meaning, category)
                concepts.append(concept)
                
            if (i + 1) % 500 == 0:
                print(f"   Processed {i + 1} words...")
                
        print(f"\n✅ Dictionary fed to brain!")
        print(f"   Words: {self.words_processed}")
        print(f"   Concepts: {self.concepts_formed}")
        print(f"   Categories: {len(self.categories)}")
        
        return {
            "words": self.words_processed,
            "concepts": self.concepts_formed,
            "categories": self.categories,
            "concepts_list": concepts,
        }
        
    def get_brain_nutrition_report(self) -> str:
        """Report on what brain has consumed"""
        return f"""
╔════════════════════════════════════════════════════════════════╗
║              BRAIN NUTRITION REPORT                            ║
╠════════════════════════════════════════════════════════════════╣
║  Words Consumed:     {self.words_processed:>6}                          ║
║  Concepts Formed:    {self.concepts_formed:>6}                          ║
║  Categories:         {len(self.categories):>6}                          ║
╠════════════════════════════════════════════════════════════════╣
║  Category Breakdown:                                           ║
""" + "".join([
    f"║    {cat:12}: {len(words):>4} words\n" 
    for cat, words in sorted(self.categories.items())[:10]
]) + """╚════════════════════════════════════════════════════════════════╝
"""


def feed_century_dictionary():
    """Feed the complete 20th Century Dictionary"""
    print("=" * 70)
    print("CENTURY DICTIONARY FEEDING")
    print("=" * 70)
    
    # Import from aos_brain_py
    sys.path.insert(0, "/root/.openclaw/workspace/aos_brain_py")
    from agents.century_dictionary import DICTIONARY_WORDS, get_word_count
    
    dictionary_data = {"words": DICTIONARY_WORDS}
    
    print(f"   Loaded {get_word_count()} words from 20th Century Dictionary")
    
    # Feed to brain
    feeder = DictionaryFeeder()
    result = feeder.feed_dictionary(dictionary_data)
    
    print(feeder.get_brain_nutrition_report())
    
    return result


if __name__ == "__main__":
    result = feed_century_dictionary()
    
    print("\n" + "=" * 70)
    print("Brain has been fed the 20th Century Dictionary.")
    print("Words are now concepts in Tracray space.")
    print("The brain speaks modern English.")
    print("=" * 70)
