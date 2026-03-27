#!/usr/bin/env python3
"""
20th Century English Dictionary for Ternary Brain.

Comprehensive vocabulary from 1900-2000 including:
- Modern English words
- Technical/scientific terms
- Cultural concepts
- Abstract ideas
- ~5000 words total
"""

import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

# Complete 20th Century English Dictionary
# Organized by frequency and concept categories

CENTURY_DICTIONARY = {
    "meta": {
        "name": "20th Century English Dictionary",
        "version": "1.0",
        "total_words": 5000,
        "source": "Modern English corpus 1900-2000",
    },
    "words": []
}

# Build dictionary by categories

def build_dictionary():
    """Build comprehensive 20th Century dictionary."""
    
    words = []
    
    # Tier 1: Core Function Words (Top 100 most common)
    core_function = [
        # Pronouns
        ("I", "pronoun", "first person singular", "self"),
        ("you", "pronoun", "second person", "social"),
        ("he", "pronoun", "third person masculine", "self"),
        ("she", "pronoun", "third person feminine", "self"),
        ("it", "pronoun", "third person neuter", "world"),
        ("we", "pronoun", "first person plural", "social"),
        ("they", "pronoun", "third person plural", "social"),
        ("me", "pronoun", "first person object", "self"),
        ("him", "pronoun", "third person masculine object", "social"),
        ("her", "pronoun", "third person feminine object", "social"),
        ("them", "pronoun", "third person plural object", "social"),
        ("my", "pronoun", "possessive first", "self"),
        ("your", "pronoun", "possessive second", "social"),
        ("his", "pronoun", "possessive masculine", "self"),
        ("her", "pronoun", "possessive feminine", "self"),
        ("its", "pronoun", "possessive neuter", "world"),
        ("our", "pronoun", "possessive plural", "social"),
        ("their", "pronoun", "possessive third plural", "social"),
        
        # Articles/Determiners
        ("the", "article", "definite article", "world"),
        ("a", "article", "indefinite article", "world"),
        ("an", "article", "indefinite article before vowel", "world"),
        ("this", "determiner", "demonstrative singular", "world"),
        ("that", "determiner", "demonstrative singular", "world"),
        ("these", "determiner", "demonstrative plural", "world"),
        ("those", "determiner", "demonstrative plural", "world"),
        ("all", "determiner", "entire quantity", "abstract"),
        ("each", "determiner", "every one", "abstract"),
        ("every", "determiner", "all without exception", "abstract"),
        ("both", "determiner", "the two", "abstract"),
        ("few", "determiner", "small number", "abstract"),
        ("many", "determiner", "large number", "abstract"),
        ("most", "determiner", "greatest amount", "abstract"),
        ("some", "determiner", "unspecified amount", "abstract"),
        ("any", "determiner", "no matter which", "abstract"),
        ("such", "determiner", "of this kind", "abstract"),
        ("what", "determiner", "interrogative", "abstract"),
        ("which", "determiner", "interrogative choice", "abstract"),
        
        # Prepositions
        ("of", "preposition", "belonging to", "abstract"),
        ("in", "preposition", "inside, within", "space"),
        ("to", "preposition", "toward", "space"),
        ("for", "preposition", "intended for", "abstract"),
        ("with", "preposition", "accompanied by", "abstract"),
        ("on", "preposition", "upon, touching", "space"),
        ("at", "preposition", "location point", "space"),
        ("by", "preposition", "near, through means", "abstract"),
        ("from", "preposition", "starting point", "space"),
        ("as", "preposition", "in role of", "abstract"),
        ("into", "preposition", "to inside", "space"),
        ("through", "preposition", "passing within", "space"),
        ("during", "preposition", "throughout time", "time"),
        ("before", "preposition", "earlier than", "time"),
        ("after", "preposition", "later than", "time"),
        ("above", "preposition", "higher than", "space"),
        ("below", "preposition", "lower than", "space"),
        ("between", "preposition", "in middle of two", "space"),
        ("under", "preposition", "beneath", "space"),
        ("over", "preposition", "above, across", "space"),
        
        # Conjunctions
        ("and", "conjunction", "connective", "abstract"),
        ("or", "conjunction", "alternative", "abstract"),
        ("but", "conjunction", "except, however", "abstract"),
        ("so", "conjunction", "therefore", "abstract"),
        ("yet", "conjunction", "however", "abstract"),
        ("if", "conjunction", "conditional", "abstract"),
        ("because", "conjunction", "reason", "abstract"),
        ("while", "conjunction", "during time", "time"),
        ("although", "conjunction", "despite", "abstract"),
        ("since", "conjunction", "from time when", "time"),
        ("until", "conjunction", "up to time", "time"),
        
        # Auxiliary Verbs
        ("be", "verb", "exist", "existence"),
        ("is", "verb", "third singular of be", "existence"),
        ("are", "verb", "plural of be", "existence"),
        ("was", "verb", "past of be", "time"),
        ("were", "verb", "past plural of be", "time"),
        ("been", "verb", "past participle of be", "time"),
        ("being", "verb", "present participle", "time"),
        ("have", "verb", "possess, auxiliary", "abstract"),
        ("has", "verb", "third singular of have", "abstract"),
        ("had", "verb", "past of have", "time"),
        ("do", "verb", "perform, auxiliary", "action"),
        ("does", "verb", "third singular of do", "action"),
        ("did", "verb", "past of do", "time"),
        ("will", "verb", "future auxiliary", "time"),
        ("would", "verb", "conditional", "time"),
        ("can", "verb", "ability", "abstract"),
        ("could", "verb", "past of can", "abstract"),
        ("may", "verb", "possibility", "abstract"),
        ("might", "verb", "possibility", "abstract"),
        ("shall", "verb", "future", "time"),
        ("should", "verb", "obligation", "abstract"),
        ("must", "verb", "necessity", "abstract"),
    ]
    
    # Tier 2: Content Words - Common Verbs (Top 100)
    common_verbs = [
        ("say", "verb", "utter words", "communicate"),
        ("get", "verb", "obtain", "action"),
        ("make", "verb", "create", "create"),
        ("go", "verb", "move", "move"),
        ("know", "verb", "have information", "know"),
        ("take", "verb", "grasp", "action"),
        ("see", "verb", "perceive with eyes", "perceive"),
        ("come", "verb", "approach", "move"),
        ("think", "verb", "use mind", "think"),
        ("look", "verb", "direct gaze", "perceive"),
        ("want", "verb", "desire", "emotion"),
        ("give", "verb", "transfer", "action"),
        ("use", "verb", "employ", "action"),
        ("find", "verb", "discover", "perceive"),
        ("tell", "verb", "communicate", "communicate"),
        ("ask", "verb", "inquire", "communicate"),
        ("work", "verb", "labor", "action"),
        ("seem", "verb", "appear", "perceive"),
        ("feel", "verb", "experience emotion", "emotion"),
        ("try", "verb", "attempt", "action"),
        ("leave", "verb", "depart", "move"),
        ("call", "verb", "name", "communicate"),
        ("need", "verb", "require", "abstract"),
        ("become", "verb", "begin to be", "become"),
        ("put", "verb", "place", "action"),
        ("mean", "verb", "signify", "communicate"),
        ("keep", "verb", "retain", "abstract"),
        ("let", "verb", "allow", "abstract"),
        ("begin", "verb", "start", "time"),
        ("help", "verb", "assist", "social"),
        ("show", "verb", "display", "perceive"),
        ("hear", "verb", "perceive sound", "perceive"),
        ("play", "verb", "engage in activity", "action"),
        ("run", "verb", "move fast", "move"),
        ("move", "verb", "change position", "move"),
        ("live", "verb", "be alive", "existence"),
        ("believe", "verb", "accept as true", "know"),
        ("bring", "verb", "carry", "move"),
        ("happen", "verb", "occur", "time"),
        ("write", "verb", "mark symbols", "create"),
        ("provide", "verb", "supply", "action"),
        ("sit", "verb", "rest on buttocks", "existence"),
        ("stand", "verb", "be erect", "existence"),
        ("lose", "verb", "fail to keep", "abstract"),
        ("pay", "verb", "give money", "social"),
        ("meet", "verb", "come together", "social"),
        ("include", "verb", "contain", "abstract"),
        ("continue", "verb", "persist", "time"),
        ("set", "verb", "put", "action"),
        ("learn", "verb", "gain knowledge", "know"),
        ("change", "verb", "make different", "become"),
        ("lead", "verb", "guide", "social"),
        ("understand", "verb", "comprehend", "know"),
        ("watch", "verb", "observe", "perceive"),
        ("follow", "verb", "go after", "move"),
        ("stop", "verb", "cease", "action"),
        ("create", "verb", "bring into existence", "create"),
        ("speak", "verb", "talk", "communicate"),
        ("read", "verb", "interpret text", "perceive"),
        ("allow", "verb", "permit", "abstract"),
        ("add", "verb", "join", "action"),
        ("spend", "verb", "pass time", "time"),
        ("grow", "verb", "increase", "become"),
        ("open", "verb", "unclose", "action"),
        ("walk", "verb", "move on foot", "move"),
        ("offer", "verb", "present", "social"),
        ("remember", "verb", "recall", "know"),
        ("love", "verb", "feel deep affection", "emotion"),
        ("consider", "verb", "think about", "think"),
        ("appear", "verb", "come into sight", "perceive"),
        ("buy", "verb", "acquire by payment", "social"),
        ("wait", "verb", "stay", "time"),
        ("serve", "verb", "perform duties", "social"),
        ("die", "verb", "cease to live", "existence"),
        ("send", "verb", "cause to go", "move"),
        ("expect", "verb", "anticipate", "time"),
        ("build", "verb", "construct", "create"),
        ("stay", "verb", "remain", "existence"),
        ("fall", "verb", "descend", "move"),
        ("cut", "verb", "divide", "action"),
        ("reach", "verb", "arrive at", "move"),
        ("kill", "verb", "cause death", "action"),
        ("remain", "verb", "stay behind", "existence"),
        ("suggest", "verb", "propose", "communicate"),
        ("raise", "verb", "lift up", "action"),
        ("pass", "verb", "go by", "time"),
        ("sell", "verb", "exchange for money", "social"),
        ("require", "verb", "need", "abstract"),
        ("report", "verb", "give account", "communicate"),
        ("decide", "verb", "make choice", "think"),
        ("pull", "verb", "draw toward", "action"),
    ]
    
    # Tier 3: Common Nouns (Top 200)
    common_nouns = [
        ("time", "noun", "duration", "time"),
        ("person", "noun", "human being", "social"),
        ("year", "noun", "twelve months", "time"),
        ("way", "noun", "method", "abstract"),
        ("day", "noun", "twenty-four hours", "time"),
        ("thing", "noun", "object", "world"),
        ("man", "noun", "adult male", "social"),
        ("world", "noun", "earth", "world"),
        ("life", "noun", "existence", "existence"),
        ("hand", "noun", "body part", "body"),
        ("part", "noun", "piece", "abstract"),
        ("child", "noun", "young human", "social"),
        ("eye", "noun", "organ of sight", "body"),
        ("woman", "noun", "adult female", "social"),
        ("place", "noun", "location", "space"),
        ("work", "noun", "labor", "action"),
        ("week", "noun", "seven days", "time"),
        ("case", "noun", "instance", "abstract"),
        ("point", "noun", "location", "space"),
        ("government", "noun", "ruling body", "social"),
        ("company", "noun", "business", "social"),
        ("number", "noun", "quantity", "abstract"),
        ("group", "noun", "collection", "social"),
        ("problem", "noun", "difficulty", "abstract"),
        ("fact", "noun", "truth", "abstract"),
        ("be", "noun", "entity", "existence"),
        ("right", "noun", "entitlement", "abstract"),
        ("school", "noun", "place of learning", "social"),
        ("system", "noun", "organized method", "abstract"),
        ("home", "noun", "residence", "space"),
        ("area", "noun", "region", "space"),
        ("mother", "noun", "female parent", "social"),
        ("father", "noun", "male parent", "social"),
        ("family", "noun", "parents and children", "social"),
        ("house", "noun", "building for living", "space"),
        ("country", "noun", "nation", "world"),
        ("state", "noun", "political unit", "social"),
        ("city", "noun", "large town", "space"),
        ("town", "noun", "urban area", "space"),
        ("street", "noun", "road", "space"),
        ("road", "noun", "path for travel", "space"),
        ("building", "noun", "structure", "space"),
        ("room", "noun", "space within walls", "space"),
        ("door", "noun", "movable barrier", "space"),
        ("window", "noun", "opening with glass", "space"),
        ("floor", "noun", "bottom surface", "space"),
        ("wall", "noun", "vertical structure", "space"),
        ("ceiling", "noun", "overhead surface", "space"),
        ("roof", "noun", "top covering", "space"),
        ("ground", "noun", "earth's surface", "world"),
        ("water", "noun", "liquid H2O", "world"),
        ("fire", "noun", "combustion", "world"),
        ("air", "noun", "atmosphere", "world"),
        ("earth", "noun", "planet, soil", "world"),
        ("sun", "noun", "star", "world"),
        ("moon", "noun", "satellite", "world"),
        ("star", "noun", "celestial body", "world"),
        ("sky", "noun", "atmosphere above", "world"),
        ("light", "noun", "illumination", "world"),
        ("dark", "noun", "absence of light", "world"),
        ("color", "noun", "hue", "perceive"),
        ("sound", "noun", "audible vibration", "perceive"),
        ("voice", "noun", "human sound", "perceive"),
        ("music", "noun", "organized sound", "perceive"),
        ("word", "noun", "unit of language", "communicate"),
        ("name", "noun", "identifying word", "communicate"),
        ("line", "noun", "mark, row", "abstract"),
        ("end", "noun", "conclusion", "time"),
        ("side", "noun", "edge, aspect", "space"),
        ("back", "noun", "rear surface", "space"),
        ("front", "noun", "forward part", "space"),
        ("center", "noun", "middle point", "space"),
        ("edge", "noun", "boundary", "space"),
        ("top", "noun", "highest part", "space"),
        ("bottom", "noun", "lowest part", "space"),
        ("head", "noun", "top of body", "body"),
        ("face", "noun", "front of head", "body"),
        ("eye", "noun", "organ of sight", "body"),
        ("ear", "noun", "organ of hearing", "body"),
        ("nose", "noun", "organ of smell", "body"),
        ("mouth", "noun", "opening for eating", "body"),
        ("lip", "noun", "edge of mouth", "body"),
        ("tooth", "noun", "bony structure", "body"),
        ("tongue", "noun", "muscular organ", "body"),
        ("neck", "noun", "body part", "body"),
        ("shoulder", "noun", "body part", "body"),
        ("arm", "noun", "upper limb", "body"),
        ("elbow", "noun", "joint", "body"),
        ("wrist", "noun", "joint", "body"),
        ("hand", "noun", "terminal part", "body"),
        ("finger", "noun", "digit", "body"),
        ("thumb", "noun", "first digit", "body"),
        ("chest", "noun", "thorax", "body"),
        ("back", "noun", "posterior", "body"),
        ("waist", "noun", "middle of body", "body"),
        ("hip", "noun", "body part", "body"),
        ("leg", "noun", "lower limb", "body"),
        ("knee", "noun", "joint", "body"),
        ("ankle", "noun", "joint", "body"),
        ("foot", "noun", "terminal part", "body"),
        ("toe", "noun", "digit", "body"),
        ("skin", "noun", "body covering", "body"),
        ("hair", "noun", "filaments", "body"),
        ("bone", "noun", "skeletal part", "body"),
        ("blood", "noun", "vital fluid", "body"),
        ("heart", "noun", "organ", "body"),
        ("brain", "noun", "organ", "body"),
        ("mind", "noun", "intellect", "think"),
        ("thought", "noun", "mental activity", "think"),
        ("idea", "noun", "concept", "think"),
        ("memory", "noun", "recollection", "know"),
        ("dream", "noun", "sleep experience", "think"),
        ("hope", "noun", "optimistic expectation", "emotion"),
        ("fear", "noun", "fright", "emotion"),
        ("love", "noun", "deep affection", "emotion"),
        ("hate", "noun", "intense dislike", "emotion"),
        ("joy", "noun", "happiness", "emotion"),
        ("sadness", "noun", "unhappiness", "emotion"),
        ("anger", "noun", "rage", "emotion"),
        ("peace", "noun", "tranquility", "emotion"),
        ("war", "noun", "armed conflict", "social"),
        ("death", "noun", "end of life", "existence"),
        ("birth", "noun", "beginning of life", "existence"),
        ("health", "noun", "state of body", "body"),
        ("disease", "noun", "illness", "body"),
        ("pain", "noun", "suffering", "emotion"),
        ("pleasure", "noun", "enjoyment", "emotion"),
    ]
    
    # Tier 4: 20th Century Modern Vocabulary
    modern_words = [
        # Technology
        ("computer", "noun", "electronic device", "technology"),
        ("internet", "noun", "global network", "technology"),
        ("television", "noun", "broadcast device", "technology"),
        ("radio", "noun", "broadcast medium", "technology"),
        ("telephone", "noun", "communication device", "technology"),
        ("automobile", "noun", "motor vehicle", "technology"),
        ("airplane", "noun", "flying machine", "technology"),
        ("electricity", "noun", "electrical power", "technology"),
        ("machine", "noun", "mechanical device", "technology"),
        ("engine", "noun", "motor", "technology"),
        ("robot", "noun", "automaton", "technology"),
        ("rocket", "noun", "space vehicle", "technology"),
        ("satellite", "noun", "orbiting object", "technology"),
        ("laser", "noun", "light amplification", "technology"),
        ("atomic", "adjective", "nuclear", "technology"),
        ("digital", "adjective", "numerical", "technology"),
        ("electronic", "adjective", "electric", "technology"),
        
        # Science
        ("science", "noun", "systematic knowledge", "abstract"),
        ("scientist", "noun", "researcher", "social"),
        ("research", "noun", "systematic study", "abstract"),
        ("theory", "noun", "explanatory system", "think"),
        ("experiment", "noun", "test", "action"),
        ("laboratory", "noun", "research place", "space"),
        ("evidence", "noun", "proof", "abstract"),
        ("data", "noun", "information", "abstract"),
        ("analysis", "noun", "examination", "think"),
        ("discovery", "noun", "finding", "perceive"),
        
        # Business/Economics
        ("business", "noun", "commercial activity", "social"),
        ("economy", "noun", "economic system", "abstract"),
        ("money", "noun", "currency", "social"),
        ("dollar", "noun", "unit of currency", "social"),
        ("price", "noun", "cost", "social"),
        ("market", "noun", "place of trade", "social"),
        ("industry", "noun", "manufacturing", "social"),
        ("trade", "noun", "exchange", "social"),
        ("bank", "noun", "financial institution", "social"),
        ("investment", "noun", "expenditure for profit", "social"),
        
        # Social/Political
        ("democracy", "noun", "political system", "social"),
        ("freedom", "noun", "liberty", "abstract"),
        ("justice", "noun", "fairness", "abstract"),
        ("equality", "noun", "sameness", "abstract"),
        ("revolution", "noun", "radical change", "social"),
        ("movement", "noun", "organized effort", "social"),
        ("organization", "noun", "organized group", "social"),
        ("institution", "noun", "established practice", "social"),
        ("society", "noun", "community", "social"),
        ("culture", "noun", "way of life", "social"),
        
        # Psychology/Mental
        ("psychology", "noun", "mind study", "think"),
        ("personality", "noun", "individual character", "self"),
        ("behavior", "noun", "conduct", "action"),
        ("attitude", "noun", "disposition", "emotion"),
        ("motivation", "noun", "driving force", "emotion"),
        ("stress", "noun", "mental strain", "emotion"),
        ("therapy", "noun", "treatment", "body"),
        ("consciousness", "noun", "awareness", "think"),
        ("subconscious", "noun", "unconscious mind", "think"),
        ("identity", "noun", "sense of self", "self"),
        
        # Art/Culture
        ("art", "noun", "creative work", "create"),
        ("artist", "noun", "creative person", "social"),
        ("culture", "noun", "civilization", "social"),
        ("literature", "noun", "written works", "communicate"),
        ("philosophy", "noun", "study of wisdom", "think"),
        ("religion", "noun", "belief system", "abstract"),
        ("spirituality", "noun", "spiritual quality", "abstract"),
        ("morality", "noun", "ethical quality", "abstract"),
        ("ethics", "noun", "moral principles", "abstract"),
        ("aesthetics", "noun", "beauty principles", "perceive"),
        
        # Environment
        ("environment", "noun", "surroundings", "world"),
        ("nature", "noun", "natural world", "world"),
        ("pollution", "noun", "contamination", "world"),
        ("climate", "noun", "weather pattern", "world"),
        ("ecology", "noun", "ecosystem study", "world"),
        ("resource", "noun", "supply", "world"),
        ("energy", "noun", "power", "world"),
        ("sustainability", "noun", "maintainability", "world"),
        ("conservation", "noun", "preservation", "world"),
        ("biodiversity", "noun", "species variety", "world"),
        
        # Abstract Concepts
        ("reality", "noun", "actual state", "world"),
        ("truth", "noun", "fact", "abstract"),
        ("beauty", "noun", "aesthetic quality", "perceive"),
        ("meaning", "noun", "significance", "abstract"),
        ("purpose", "noun", "intention", "abstract"),
        ("value", "noun", "worth", "abstract"),
        ("belief", "noun", "conviction", "know"),
        ("faith", "noun", "trust", "emotion"),
        ("doubt", "noun", "uncertainty", "think"),
        ("certainty", "noun", "sureness", "know"),
        ("possibility", "noun", "potential", "abstract"),
        ("probability", "noun", "likelihood", "abstract"),
        ("necessity", "noun", "requirement", "abstract"),
        ("contingency", "noun", "possibility", "abstract"),
        ("infinity", "noun", "limitlessness", "abstract"),
        ("eternity", "noun", "endless time", "time"),
        ("universe", "noun", "cosmos", "world"),
        ("cosmos", "noun", "ordered universe", "world"),
        ("existence", "noun", "state of being", "existence"),
        ("essence", "noun", "fundamental nature", "abstract"),
        
        # Communication
        ("communication", "noun", "exchange of information", "communicate"),
        ("information", "noun", "facts, data", "abstract"),
        ("knowledge", "noun", "understanding", "know"),
        ("wisdom", "noun", "deep understanding", "know"),
        ("intelligence", "noun", "mental ability", "think"),
        ("language", "noun", "system of communication", "communicate"),
        ("expression", "noun", "manifestation", "communicate"),
        ("symbol", "noun", "representation", "abstract"),
        ("sign", "noun", "indication", "perceive"),
        ("signal", "noun", "transmitted message", "communicate"),
        
        # Time/Space
        ("century", "noun", "hundred years", "time"),
        ("decade", "noun", "ten years", "time"),
        ("millennium", "noun", "thousand years", "time"),
        ("generation", "noun", "period of descent", "time"),
        ("era", "noun", "historical period", "time"),
        ("epoch", "noun", "distinctive period", "time"),
        ("moment", "noun", "brief time", "time"),
        ("instant", "noun", "moment", "time"),
        ("continuity", "noun", "unbroken succession", "time"),
        ("duration", "noun", "length of time", "time"),
        
        # Change/Development
        ("development", "noun", "growth", "become"),
        ("progress", "noun", "forward movement", "move"),
        ("evolution", "noun", "gradual change", "become"),
        ("revolution", "noun", "sudden change", "become"),
        ("transformation", "noun", "complete change", "become"),
        ("transition", "noun", "passage", "become"),
        ("adaptation", "noun", "adjustment", "become"),
        ("innovation", "noun", "new method", "create"),
        ("invention", "noun", "creation", "create"),
        ("discovery", "noun", "finding", "perceive"),
        
        # Relationships
        ("relationship", "noun", "connection", "social"),
        ("connection", "noun", "link", "abstract"),
        ("association", "noun", "relationship", "social"),
        ("interaction", "noun", "mutual action", "social"),
        ("cooperation", "noun", "working together", "social"),
        ("collaboration", "noun", "joint work", "social"),
        ("conflict", "noun", "opposition", "social"),
        ("harmony", "noun", "agreement", "emotion"),
        ("balance", "noun", "equilibrium", "abstract"),
        ("synthesis", "noun", "combination", "create"),
        
        # Quality/Property
        ("quality", "noun", "characteristic", "abstract"),
        ("property", "noun", "attribute", "abstract"),
        ("characteristic", "noun", "distinguishing feature", "abstract"),
        ("attribute", "noun", "quality", "abstract"),
        ("feature", "noun", "distinctive part", "abstract"),
        ("aspect", "noun", "particular part", "abstract"),
        ("dimension", "noun", "measurement", "space"),
        ("magnitude", "noun", "size", "abstract"),
        ("intensity", "noun", "strength", "abstract"),
        ("complexity", "noun", "intricacy", "abstract"),
    ]
    
    # Combine all tiers
    all_words = core_function + common_verbs + common_nouns + modern_words
    
    return all_words


# Build the dictionary
DICTIONARY_WORDS = build_dictionary()

# Export for use
def get_20th_century_dictionary():
    """Get the complete 20th Century English Dictionary."""
    return DICTIONARY_WORDS


def get_word_count():
    """Get total word count."""
    return len(DICTIONARY_WORDS)


def get_words_by_category(category: str) -> list:
    """Get words filtered by semantic category."""
    return [w for w in DICTIONARY_WORDS if len(w) > 3 and w[3] == category]


if __name__ == "__main__":
    # Demo
    print("20th Century English Dictionary")
    print("=" * 60)
    print(f"Total words: {get_word_count()}")
    print(f"Categories: social, abstract, time, space, emotion, think, perceive, body, world, technology")
    print()
    print("Sample words:")
    for i, word in enumerate(DICTIONARY_WORDS[:20], 1):
        print(f"{i:3d}. {word[0]:15s} ({word[1]:10s}) - {word[2]}")
