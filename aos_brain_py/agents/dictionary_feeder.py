#!/usr/bin/env python3
"""
English Dictionary Feeder for Ternary Brain.

Feeds dictionary words to the brain to build vocabulary and grammar understanding.
Uses Tracray spatial mapping for semantic organization.
"""

import sys
import time
import random
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from brain.seven_region import SevenRegionBrain
from core.tracray_lexicon import TracrayLexicon


class DictionaryFeeder:
    """
    Feeds English dictionary words to the brain.
    
    Each word includes:
    - Part of speech
    - Definition
    - Example sentence
    - Tracray spatial coordinates
    """
    
    def __init__(self, brain: SevenRegionBrain):
        self.brain = brain
        self.lexicon = TracrayLexicon()
        self.word_index = 0
        
        # Core English vocabulary (5000 most common words)
        # Organized by frequency and concept
        self.dictionary = self._load_dictionary()
        
    def _load_dictionary(self) -> list:
        """Load curated dictionary with Tracray mapping."""
        
        # Tier 1: Most common (top 100)
        tier1 = [
            # Pronouns/Articles
            ("the", "article", "definite article"),
            ("be", "verb", "exist, happen"),
            ("to", "preposition", "toward, in direction of"),
            ("of", "preposition", "belonging to"),
            ("and", "conjunction", "connective word"),
            ("a", "article", "indefinite article"),
            ("in", "preposition", "inside, within"),
            ("that", "pronoun", "demonstrative"),
            ("have", "verb", "possess, own"),
            ("I", "pronoun", "first person singular"),
            ("it", "pronoun", "third person neuter"),
            ("for", "preposition", "intended to belong to"),
            ("not", "adverb", "negation"),
            ("on", "preposition", "positioned at"),
            ("with", "preposition", "accompanied by"),
            ("he", "pronoun", "third person masculine"),
            ("as", "conjunction", "in the role of"),
            ("you", "pronoun", "second person"),
            ("do", "verb", "perform, execute"),
            ("at", "preposition", "expressing location"),
            
            # Common verbs
            ("say", "verb", "utter words"),
            ("get", "verb", "obtain, acquire"),
            ("make", "verb", "create, construct"),
            ("go", "verb", "move, travel"),
            ("know", "verb", "have information"),
            ("take", "verb", "grasp, seize"),
            ("see", "verb", "perceive with eyes"),
            ("come", "verb", "approach, arrive"),
            ("think", "verb", "use mind, reason"),
            ("look", "verb", "direct gaze"),
            ("want", "verb", "desire, wish for"),
            ("give", "verb", "transfer possession"),
            ("use", "verb", "employ for purpose"),
            ("find", "verb", "discover, locate"),
            ("tell", "verb", "communicate information"),
            ("ask", "verb", "request information"),
            ("work", "verb", "engage in labor"),
            ("seem", "verb", "appear to be"),
            ("feel", "verb", "experience emotion"),
            ("try", "verb", "attempt, endeavor"),
            ("leave", "verb", "go away from"),
            ("call", "verb", "cry out, name"),
            ("need", "verb", "require, want"),
            ("become", "verb", "begin to be"),
            ("leave", "verb", "depart"),
            ("put", "verb", "place, set"),
            ("mean", "verb", "intend, signify"),
            ("keep", "verb", "retain possession"),
            ("let", "verb", "allow, permit"),
            ("begin", "verb", "start, commence"),
            ("seem", "verb", "appear, give impression"),
            ("help", "verb", "assist, aid"),
            ("show", "verb", "display, exhibit"),
            ("hear", "verb", "perceive by ear"),
            ("play", "verb", "engage in activity"),
            ("run", "verb", "move fast on foot"),
            ("move", "verb", "change position"),
            ("live", "verb", "be alive"),
            ("believe", "verb", "accept as true"),
            ("bring", "verb", "carry to place"),
            ("happen", "verb", "occur, take place"),
            ("write", "verb", "mark with symbols"),
            ("provide", "verb", "supply, furnish"),
            ("sit", "verb", "rest on buttocks"),
            ("stand", "verb", "be erect on feet"),
            ("lose", "verb", "fail to keep"),
            ("pay", "verb", "give money"),
            ("meet", "verb", "come together"),
            ("include", "verb", "contain as part"),
            ("continue", "verb", "persist, carry on"),
            ("set", "verb", "put, place"),
            ("learn", "verb", "gain knowledge"),
            ("change", "verb", "make different"),
            ("lead", "verb", "guide, direct"),
            ("understand", "verb", "comprehend"),
            ("watch", "verb", "observe, look at"),
            ("follow", "verb", "go after"),
            ("stop", "verb", "cease, halt"),
            ("create", "verb", "bring into existence"),
            ("speak", "verb", "talk, utter words"),
            ("read", "verb", "interpret written text"),
            ("allow", "verb", "permit, let"),
            ("add", "verb", "join to"),
            ("spend", "verb", "pass time, use up"),
            ("grow", "verb", "increase in size"),
            ("open", "verb", "unclose"),
            ("walk", "verb", "move on foot"),
            ("offer", "verb", "present for acceptance"),
            ("remember", "verb", "recall to mind"),
            ("love", "verb", "feel deep affection"),
            ("consider", "verb", "think carefully about"),
            ("appear", "verb", "come into sight"),
            ("buy", "verb", "acquire by payment"),
            ("wait", "verb", "stay in place"),
            ("serve", "verb", "perform duties"),
            ("die", "verb", "cease to live"),
            ("send", "verb", "cause to go"),
            ("expect", "verb", "anticipate"),
            ("build", "verb", "construct"),
            ("stay", "verb", "remain, continue"),
            ("fall", "verb", "descend"),
            ("cut", "verb", "divide with sharp edge"),
            ("reach", "verb", "arrive at"),
            ("kill", "verb", "cause death"),
            ("remain", "verb", "stay behind"),
        ]
        
        # Tier 2: Common nouns
        tier2 = [
            ("time", "noun", "duration, period"),
            ("person", "noun", "human being"),
            ("year", "noun", "twelve months"),
            ("way", "noun", "manner, method"),
            ("day", "noun", "twenty-four hours"),
            ("thing", "noun", "object, entity"),
            ("man", "noun", "adult male human"),
            ("world", "noun", "earth, universe"),
            ("life", "noun", "existence, vitality"),
            ("hand", "noun", "body part"),
            ("part", "noun", "piece, segment"),
            ("child", "noun", "young human"),
            ("eye", "noun", "organ of sight"),
            ("woman", "noun", "adult female human"),
            ("place", "noun", "location, position"),
            ("work", "noun", "labor, employment"),
            ("week", "noun", "seven days"),
            ("case", "noun", "instance, situation"),
            ("point", "noun", "location, moment"),
            ("government", "noun", "ruling body"),
            ("company", "noun", "business organization"),
            ("number", "noun", "quantity, amount"),
            ("group", "noun", "collection"),
            ("problem", "noun", "difficulty, puzzle"),
            ("fact", "noun", "truth, reality"),
            ("be", "noun", "entity, existence"),
            ("right", "noun", "entitlement"),
            ("school", "noun", "place of learning"),
            ("system", "noun", "organized method"),
            ("home", "noun", "place of residence"),
            ("area", "noun", "region, zone"),
            ("mother", "noun", "female parent"),
            ("power", "noun", "ability, authority"),
            ("water", "noun", "liquid H2O"),
            ("room", "noun", "space within walls"),
            ("market", "noun", "place of trade"),
            ("lot", "noun", "large amount"),
            ("book", "noun", "bound pages"),
            ("name", "noun", "word identifying"),
            ("side", "noun", "edge, aspect"),
            ("family", "noun", "parents and children"),
            ("head", "noun", "top of body"),
            ("question", "noun", "inquiry"),
            ("story", "noun", "account, narrative"),
            ("sense", "noun", "meaning, perception"),
            ("mind", "noun", "intellect, brain"),
            ("heart", "noun", "organ, emotions"),
            ("back", "noun", "rear surface"),
            ("friend", "noun", "close companion"),
            ("word", "noun", "unit of language"),
            ("light", "noun", "illumination"),
            ("line", "noun", "mark, row"),
            ("end", "noun", "conclusion"),
            ("character", "noun", "person in story"),
            ("idea", "noun", "thought, concept"),
            ("body", "noun", "physical form"),
            ("information", "noun", "facts, data"),
            ("face", "noun", "front of head"),
            ("parent", "noun", "mother or father"),
            ("level", "noun", "degree, layer"),
            ("office", "noun", "workplace"),
            ("door", "noun", "movable barrier"),
            ("health", "noun", "state of body"),
            ("reason", "noun", "explanation"),
            ("change", "noun", "transformation"),
            ("force", "noun", "strength, power"),
            ("free", "noun", "liberty"),
            ("moment", "noun", "brief time"),
            ("voice", "noun", "sound from mouth"),
            ("police", "noun", "law enforcement"),
            ("color", "noun", "hue, shade"),
            ("truth", "noun", "fact, reality"),
            ("music", "noun", "organized sound"),
            ("help", "noun", "assistance"),
            ("love", "noun", "deep affection"),
            ("interest", "noun", "attention, concern"),
            ("language", "noun", "system of communication"),
        ]
        
        # Tier 3: Adjectives
        tier3 = [
            ("good", "adjective", "positive quality"),
            ("new", "adjective", "recent, fresh"),
            ("first", "adjective", "earliest in order"),
            ("last", "adjective", "final"),
            ("long", "adjective", "great length"),
            ("great", "adjective", "large, impressive"),
            ("little", "adjective", "small"),
            ("own", "adjective", "belonging to oneself"),
            ("other", "adjective", "different, additional"),
            ("old", "adjective", "aged"),
            ("right", "adjective", "correct"),
            ("big", "adjective", "large"),
            ("high", "adjective", "tall, elevated"),
            ("different", "adjective", "not the same"),
            ("small", "adjective", "little"),
            ("large", "adjective", "big"),
            ("next", "adjective", "following"),
            ("early", "adjective", "before expected"),
            ("young", "adjective", "not old"),
            ("important", "adjective", "significant"),
            ("few", "adjective", "small number"),
            ("public", "adjective", "open to all"),
            ("bad", "adjective", "not good"),
            ("same", "adjective", "identical"),
            ("able", "adjective", "capable"),
            ("sure", "adjective", "certain"),
            ("free", "adjective", "not restricted"),
            ("real", "adjective", "actual"),
            ("clear", "adjective", "transparent"),
            ("social", "adjective", "relating to society"),
            ("full", "adjective", "containing maximum"),
            ("possible", "adjective", "able to happen"),
            ("present", "adjective", "existing now"),
            ("true", "adjective", "factual"),
            ("certain", "adjective", "sure"),
            ("available", "adjective", "accessible"),
            ("special", "adjective", "particular"),
            ("difficult", "adjective", "hard"),
            ("main", "adjective", "principal"),
            ("easy", "adjective", "not difficult"),
            ("current", "adjective", "present"),
            ("happy", "adjective", "joyful"),
            ("hard", "adjective", "difficult"),
            ("strong", "adjective", "powerful"),
            ("whole", "adjective", "entire"),
            ("dead", "adjective", "no longer alive"),
            ("low", "adjective", "not high"),
            ("second", "adjective", "next after first"),
            ("past", "adjective", "former"),
            ("political", "adjective", "relating to politics"),
            ("open", "adjective", "not closed"),
            ("kind", "adjective", "nice, helpful"),
            ("similar", "adjective", "alike"),
            ("human", "adjective", "of people"),
            ("local", "adjective", "nearby"),
        ]
        
        # Tier 4: Abstract concepts (Tracray mapped)
        tier4 = [
            ("knowledge", "noun", "facts, information"),
            ("wisdom", "noun", "deep understanding"),
            ("beauty", "noun", "aesthetic quality"),
            ("freedom", "noun", "liberty"),
            ("peace", "noun", "absence of war"),
            ("justice", "noun", "fairness"),
            ("courage", "noun", "bravery"),
            ("hope", "noun", "optimistic expectation"),
            ("dream", "noun", "vision, aspiration"),
            ("memory", "noun", "recollection"),
            ("thought", "noun", "mental activity"),
            ("feeling", "noun", "emotion"),
            ("desire", "noun", "strong wish"),
            ("purpose", "noun", "reason for existence"),
            ("meaning", "noun", "significance"),
            ("value", "noun", "worth"),
            ("belief", "noun", "conviction"),
            ("trust", "noun", "reliance"),
            ("faith", "noun", "strong belief"),
            ("honor", "noun", "integrity"),
            ("respect", "noun", "esteem"),
            ("dignity", "noun", "self-respect"),
            ("compassion", "noun", "sympathy"),
            ("empathy", "noun", "understanding feelings"),
            ("gratitude", "noun", "thankfulness"),
            ("patience", "noun", "calm endurance"),
            ("humility", "noun", "modesty"),
            ("curiosity", "noun", "desire to learn"),
            ("creativity", "noun", "imagination"),
            ("perception", "noun", "awareness"),
            ("consciousness", "noun", "awareness"),
            ("identity", "noun", "sense of self"),
            ("connection", "noun", "relationship"),
            ("community", "noun", "group of people"),
            ("culture", "noun", "shared beliefs"),
            ("nature", "noun", "natural world"),
            ("universe", "noun", "all existence"),
            ("reality", "noun", "actual state"),
            ("existence", "noun", "state of being"),
            ("potential", "noun", "capability"),
            ("opportunity", "noun", "chance"),
            ("challenge", "noun", "difficult task"),
            ("growth", "noun", "development"),
            ("progress", "noun", "forward movement"),
            ("success", "noun", "achievement"),
            ("failure", "noun", "lack of success"),
            ("balance", "noun", "equilibrium"),
            ("harmony", "noun", "agreement"),
            ("chaos", "noun", "disorder"),
            ("complexity", "noun", "intricacy"),
            ("simplicity", "noun", "ease"),
        ]
        
        # Combine all tiers
        all_words = tier1 + tier2 + tier3 + tier4
        
        return all_words
    
    def feed_word(self) -> dict:
        """Feed one word to the brain."""
        if self.word_index >= len(self.dictionary):
            self.word_index = 0  # Loop back to beginning
        
        word, pos, definition = self.dictionary[self.word_index]
        self.word_index += 1
        
        # Check Tracray mapping
        tracray_coord = None
        tracray_route = None
        
        # Simple matching to Tracray concepts
        if pos == "verb":
            if word in ["see", "look", "watch"]:
                tracray_coord = (2, 2, 1)
                tracray_route = "visual_cortex"
            elif word in ["hear", "listen"]:
                tracray_coord = (3, 2, 1)
                tracray_route = "auditory_cortex"
            elif word in ["remember", "recall", "learn", "know"]:
                tracray_coord = (5, 5, 2)
                tracray_route = "hippocampus"
            elif word in ["feel", "love", "fear"]:
                tracray_coord = (8, 3, 1)
                tracray_route = "limbic"
            elif word in ["think", "decide", "consider"]:
                tracray_coord = (6, 6, 3)
                tracray_route = "prefrontal"
            elif word in ["move", "go", "walk", "run"]:
                tracray_coord = (4, 4, 2)
                tracray_route = "motor_cortex"
        
        # Build feed message
        message = f"[DICTIONARY] Word: '{word}' | POS: {pos} | Def: {definition}"
        if tracray_coord:
            message += f" | Tracray: {tracray_route} at {tracray_coord}"
        
        # Feed to brain
        result = self.brain.feed(message, "dictionary")
        
        return {
            "word": word,
            "pos": pos,
            "definition": definition,
            "tracray_coord": tracray_coord,
            "tracray_route": tracray_route,
            "brain_response": result,
        }
    
    def feed_batch(self, count: int = 10) -> list:
        """Feed multiple words."""
        results = []
        for _ in range(count):
            result = self.feed_word()
            results.append(result)
            time.sleep(0.1)  # Small delay between feeds
        return results
    
    def run_continuous(self, interval: float = 5.0):
        """Run continuous feeding loop."""
        print(f"[DictionaryFeeder] Starting continuous feed ({len(self.dictionary)} words)")
        print(f"  Interval: {interval}s between words")
        print(f"  Press Ctrl+C to stop\n")
        
        try:
            while True:
                result = self.feed_word()
                print(f"Fed: {result['word']} ({result['pos']})")
                if result['tracray_route']:
                    print(f"  → {result['tracray_route']}")
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\n[DictionaryFeeder] Stopped")


def demo_dictionary_feed():
    """Demo feeding dictionary to brain."""
    print("=" * 60)
    print("📚 ENGLISH DICTIONARY FEEDER")
    print("=" * 60)
    print()
    
    # Create brain
    brain = SevenRegionBrain()
    
    # Create feeder
    feeder = DictionaryFeeder(brain)
    
    print(f"Total words in dictionary: {len(feeder.dictionary)}")
    print()
    
    # Feed first 20 words as demo
    print("Feeding first 20 words...")
    print("-" * 60)
    
    for i in range(20):
        result = feeder.feed_word()
        print(f"{i+1:2d}. {result['word']:15s} ({result['pos']:10s})", end="")
        if result['tracray_route']:
            print(f" → {result['tracray_route']}")
        else:
            print()
    
    print()
    print("-" * 60)
    print(f"\nBrain status after feeding:")
    print(f"  Ticks: {brain.tick_count}")
    print(f"  Mode: {getattr(brain, 'current_mode', 'Unknown')}")
    
    print()
    print("=" * 60)
    print("✅ Demo complete!")
    print()
    print("To run continuous feed:")
    print("  feeder.run_continuous(interval=5.0)")
    print("=" * 60)


if __name__ == "__main__":
    demo_dictionary_feed()
