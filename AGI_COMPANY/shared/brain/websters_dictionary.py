#!/usr/bin/env python3
"""
COMPREHENSIVE WEBSTER'S DICTIONARY
50,000+ words for AOS Brain
All categories: nouns, verbs, adjectives, adverbs, etc.
With Tracray semantic mappings
"""

import sys
from pathlib import Path

# Handle __file__ not defined when running via exec
try:
    sys.path.insert(0, str(Path(__file__).parent.parent))
except NameError:
    sys.path.insert(0, str(Path("/root/.openclaw/workspace/AGI_COMPANY/shared/brain").parent.parent))

# Websters Dictionary - Comprehensive English Vocabulary
# Organized by semantic categories for Tracray mapping

def build_websters_dictionary():
    """Build the complete Webster's Dictionary with 50,000+ words."""
    
    words = []
    word_id = 0
    
    def add(word, pos, meaning, category):
        nonlocal word_id
        word_id += 1
        return (word, pos, meaning, category, word_id)
    
    # ==== PRONOUNS (100) ====
    pronouns = [
        add("I", "pronoun", "first person singular nominative", "self"),
        add("me", "pronoun", "first person singular objective", "self"),
        add("my", "pronoun", "first person singular possessive", "self"),
        add("mine", "pronoun", "first person singular possessive", "self"),
        add("myself", "pronoun", "first person singular reflexive", "self"),
        add("we", "pronoun", "first person plural nominative", "social"),
        add("us", "pronoun", "first person plural objective", "social"),
        add("our", "pronoun", "first person plural possessive", "social"),
        add("ours", "pronoun", "first person plural possessive", "social"),
        add("ourselves", "pronoun", "first person plural reflexive", "social"),
        add("you", "pronoun", "second person nominative", "social"),
        add("your", "pronoun", "second person possessive", "social"),
        add("yours", "pronoun", "second person possessive", "social"),
        add("yourself", "pronoun", "second person singular reflexive", "social"),
        add("yourselves", "pronoun", "second person plural reflexive", "social"),
        add("he", "pronoun", "third person masculine nominative", "social"),
        add("him", "pronoun", "third person masculine objective", "social"),
        add("his", "pronoun", "third person masculine possessive", "social"),
        add("himself", "pronoun", "third person masculine reflexive", "social"),
        add("she", "pronoun", "third person feminine nominative", "social"),
        add("her", "pronoun", "third person feminine objective", "social"),
        add("hers", "pronoun", "third person feminine possessive", "social"),
        add("herself", "pronoun", "third person feminine reflexive", "social"),
        add("it", "pronoun", "third person neuter nominative", "world"),
        add("its", "pronoun", "third person neuter possessive", "world"),
        add("itself", "pronoun", "third person neuter reflexive", "world"),
        add("they", "pronoun", "third person plural nominative", "social"),
        add("them", "pronoun", "third person plural objective", "social"),
        add("their", "pronoun", "third person plural possessive", "social"),
        add("theirs", "pronoun", "third person plural possessive", "social"),
        add("themselves", "pronoun", "third person plural reflexive", "social"),
        add("one", "pronoun", "indefinite person", "abstract"),
        add("oneself", "pronoun", "reflexive", "self"),
        add("who", "pronoun", "interrogative nominative", "abstract"),
        add("whom", "pronoun", "interrogative objective", "abstract"),
        add("whose", "pronoun", "interrogative possessive", "abstract"),
        add("whoever", "pronoun", "indefinite nominative", "abstract"),
        add("whomever", "pronoun", "indefinite objective", "abstract"),
        add("whatever", "pronoun", "indefinite thing", "abstract"),
        add("whichever", "pronoun", "indefinite choice", "abstract"),
        add("this", "pronoun", "demonstrative singular", "world"),
        add("that", "pronoun", "demonstrative singular distal", "world"),
        add("these", "pronoun", "demonstrative plural", "world"),
        add("those", "pronoun", "demonstrative plural distal", "world"),
        add("someone", "pronoun", "indefinite person", "social"),
        add("somebody", "pronoun", "indefinite person", "social"),
        add("something", "pronoun", "indefinite thing", "world"),
        add("anyone", "pronoun", "indefinite person", "social"),
        add("anybody", "pronoun", "indefinite person", "social"),
        add("anything", "pronoun", "indefinite thing", "world"),
        add("everyone", "pronoun", "universal person", "social"),
        add("everybody", "pronoun", "universal person", "social"),
        add("everything", "pronoun", "universal thing", "world"),
        add("nobody", "pronoun", "negative person", "social"),
        add("nothing", "pronoun", "negative thing", "abstract"),
        add("none", "pronoun", "not one", "abstract"),
        add("each", "pronoun", "distributive", "abstract"),
        add("either", "pronoun", "one of two", "abstract"),
        add("neither", "pronoun", "not either", "abstract"),
        add("another", "pronoun", "additional one", "abstract"),
        add("such", "pronoun", "of this kind", "abstract"),
        add("former", "pronoun", "first mentioned", "abstract"),
        add("latter", "pronoun", "second mentioned", "abstract"),
        add("many", "pronoun", "many people", "abstract"),
        add("few", "pronoun", "few people", "abstract"),
        add("several", "pronoun", "more than two", "abstract"),
        add("most", "pronoun", "the majority", "abstract"),
        add("some", "pronoun", "unspecified", "abstract"),
        add("all", "pronoun", "the whole", "abstract"),
        add("both", "pronoun", "the two", "abstract"),
        add("any", "pronoun", "unspecified one", "abstract"),
        add("enough", "pronoun", "sufficient", "abstract"),
        add("plenty", "pronoun", "abundance", "abstract"),
        add("others", "pronoun", "other people", "social"),
        add("mine", "pronoun", "possessive", "self"),
        add("thine", "pronoun", "archaic yours", "social"),
        add("ye", "pronoun", "archaic plural you", "social"),
        add("thou", "pronoun", "archaic singular you", "social"),
        add("thee", "pronoun", "archaic objective you", "social"),
        add("aught", "pronoun", "anything", "abstract"),
        add("naught", "pronoun", "nothing", "abstract"),
    ]
    words.extend(pronouns)
    
    # ==== ARTICLES AND DETERMINERS (80) ====
    articles = [
        add("the", "article", "definite article", "world"),
        add("a", "article", "indefinite article", "world"),
        add("an", "article", "indefinite article before vowel", "world"),
        add("some", "determiner", "unspecified amount", "abstract"),
        add("any", "determiner", "unspecified one", "abstract"),
        add("no", "determiner", "not any", "abstract"),
        add("every", "determiner", "all without exception", "abstract"),
        add("each", "determiner", "every one individually", "abstract"),
        add("all", "determiner", "entire quantity", "abstract"),
        add("both", "determiner", "the two together", "abstract"),
        add("half", "determiner", "one of two equal parts", "abstract"),
        add("several", "determiner", "more than two", "abstract"),
        add("few", "determiner", "small number", "abstract"),
        add("fewer", "determiner", "comparative of few", "abstract"),
        add("fewest", "determiner", "superlative of few", "abstract"),
        add("many", "determiner", "large number", "abstract"),
        add("more", "determiner", "comparative", "abstract"),
        add("most", "determiner", "superlative", "abstract"),
        add("much", "determiner", "large amount", "abstract"),
        add("little", "determiner", "small amount", "abstract"),
        add("less", "determiner", "comparative of little", "abstract"),
        add("least", "determiner", "superlative of little", "abstract"),
        add("another", "determiner", "additional", "abstract"),
        add("other", "determiner", "alternative", "abstract"),
        add("such", "determiner", "of this kind", "abstract"),
        add("what", "determiner", "interrogative", "abstract"),
        add("whatever", "determiner", "any that", "abstract"),
        add("which", "determiner", "interrogative choice", "abstract"),
        add("whichever", "determiner", "any which", "abstract"),
        add("either", "determiner", "one or the other", "abstract"),
        add("neither", "determiner", "not either", "abstract"),
        add("enough", "determiner", "sufficient quantity", "abstract"),
        add("own", "determiner", "belonging to oneself", "self"),
        add("last", "determiner", "final", "time"),
        add("next", "determiner", "following", "time"),
        add("first", "determiner", "ordinal number one", "time"),
        add("second", "determiner", "ordinal number two", "time"),
        add("third", "determiner", "ordinal number three", "time"),
        add("same", "determiner", "identical", "abstract"),
        add("different", "determiner", "not the same", "abstract"),
        add("certain", "determiner", "specific but unnamed", "abstract"),
        add("particular", "determiner", "specific", "abstract"),
        add("former", "determiner", "first of two", "abstract"),
        add("latter", "determiner", "second of two", "abstract"),
        add("various", "determiner", "several different", "abstract"),
        add("whole", "determiner", "entire", "abstract"),
        add("entire", "determiner", "complete", "abstract"),
        add("full", "determiner", "complete amount", "abstract"),
        add("empty", "determiner", "containing nothing", "abstract"),
        add("various", "determiner", "diverse", "abstract"),
        add("numerous", "determiner", "many", "abstract"),
        add("countless", "determiner", "too many to count", "abstract"),
        add("innumerable", "determiner", "countless", "abstract"),
        add("myriad", "determiner", "countless", "abstract"),
        add("multiple", "determiner", "many", "abstract"),
        add("varied", "determiner", "diverse", "abstract"),
        add("diverse", "determiner", "varied", "abstract"),
        add(" sundry", "determiner", "various", "abstract"),
        add("certain", "determiner", "particular", "abstract"),
        add("given", "determiner", "specified", "abstract"),
        add("specific", "determiner", "particular", "abstract"),
        add("precise", "determiner", "exact", "abstract"),
        add("exact", "determiner", "precise", "abstract"),
        add("very", "determiner", "emphatic", "abstract"),
        add("mere", "determiner", "nothing more than", "abstract"),
        add("sheer", "determiner", "utter", "abstract"),
        add("utter", "determiner", "complete", "abstract"),
        add("downright", "determiner", "complete", "abstract"),
        add("outright", "determiner", "complete", "abstract"),
        add("absolute", "determiner", "complete", "abstract"),
    ]
    words.extend(articles)
    
    # ==== PREPOSITIONS (150) ====
    preps = [
        add("of", "preposition", "belonging to, made from", "abstract"),
        add("in", "preposition", "inside, within", "space"),
        add("to", "preposition", "toward, in direction of", "space"),
        add("for", "preposition", "intended to belong to", "abstract"),
        add("with", "preposition", "accompanied by", "abstract"),
        add("on", "preposition", "upon, touching surface", "space"),
        add("at", "preposition", "expressing location point", "space"),
        add("by", "preposition", "near, through means of", "abstract"),
        add("from", "preposition", "starting point", "space"),
        add("as", "preposition", "in the role of", "abstract"),
        add("into", "preposition", "to the inside of", "space"),
        add("through", "preposition", "passing from side to side", "space"),
        add("during", "preposition", "throughout the time of", "time"),
        add("before", "preposition", "earlier than", "time"),
        add("after", "preposition", "later than", "time"),
        add("above", "preposition", "higher than", "space"),
        add("below", "preposition", "lower than", "space"),
        add("between", "preposition", "in the space separating", "space"),
        add("under", "preposition", "beneath", "space"),
        add("over", "preposition", "above, across", "space"),
        add("among", "preposition", "surrounded by", "space"),
        add("within", "preposition", "inside", "space"),
        add("without", "preposition", "outside, lacking", "space"),
        add("behind", "preposition", "at the back of", "space"),
        add("beneath", "preposition", "below, under", "space"),
        add("beside", "preposition", "next to", "space"),
        add("besides", "preposition", "in addition to", "abstract"),
        add("beyond", "preposition", "on the far side of", "space"),
        add("but", "preposition", "except", "abstract"),
        add("concerning", "preposition", "about", "abstract"),
        add("considering", "preposition", "taking into account", "abstract"),
        add("despite", "preposition", "in spite of", "abstract"),
        add("down", "preposition", "toward a lower position", "space"),
        add("except", "preposition", "excluding", "abstract"),
        add("following", "preposition", "subsequent to", "time"),
        add("inside", "preposition", "within", "space"),
        add("like", "preposition", "similar to", "abstract"),
        add("near", "preposition", "close to", "space"),
        add("off", "preposition", "away from", "space"),
        add("opposite", "preposition", "facing", "space"),
        add("outside", "preposition", "external to", "space"),
        add("past", "preposition", "beyond in time or space", "time"),
        add("regarding", "preposition", "concerning", "abstract"),
        add("round", "preposition", "around", "space"),
        add("since", "preposition", "from a time when", "time"),
        add("till", "preposition", "until", "time"),
        add("until", "preposition", "up to the time of", "time"),
        add("upon", "preposition", "on", "space"),
        add("up", "preposition", "toward a higher position", "space"),
        add("toward", "preposition", "in the direction of", "space"),
        add("towards", "preposition", "toward", "space"),
        add("underneath", "preposition", "under", "space"),
        add("unlike", "preposition", "different from", "abstract"),
        add("via", "preposition", "by way of", "space"),
        add("worth", "preposition", "having value of", "abstract"),
        add("amid", "preposition", "in the middle of", "space"),
        add("amidst", "preposition", "amid", "space"),
        add("amongst", "preposition", "among", "space"),
        add("atop", "preposition", "on the top of", "space"),
        add("barring", "preposition", "apart from", "abstract"),
        add("circa", "preposition", "approximately", "time"),
        add("cum", "preposition", "combined with", "abstract"),
        add("mid", "preposition", "amid", "space"),
        add("midst", "preposition", "middle", "space"),
        add("notwithstanding", "preposition", "in spite of", "abstract"),
        add("qua", "preposition", "in the capacity of", "abstract"),
        add("re", "preposition", "regarding", "abstract"),
        add("vis-a-vis", "preposition", "in relation to", "abstract"),
        add("aboard", "preposition", "on board", "space"),
        add("about", "preposition", "concerning", "abstract"),
        add("across", "preposition", "from one side to another", "space"),
        add("along", "preposition", "moving in constant direction", "space"),
        add("alongside", "preposition", "beside", "space"),
        add("apropos", "preposition", "with reference to", "abstract"),
        add("around", "preposition", "surrounding, approximately", "space"),
        add("astride", "preposition", "with legs on either side", "space"),
        add("athwart", "preposition", "across", "space"),
        add("bar", "preposition", "except", "abstract"),
        add("barring", "preposition", "except for", "abstract"),
        add("before", "preposition", "in front of", "space"),
        add("below", "preposition", "lower than", "space"),
        add("beneath", "preposition", "underneath", "space"),
        add("beside", "preposition", "at the side of", "space"),
        add("between", "preposition", "in the space that separates", "space"),
        add("betwixt", "preposition", "between", "space"),
        add("beyond", "preposition", "on the farther side", "space"),
        add("but", "preposition", "except", "abstract"),
        add("concerning", "preposition", "about", "abstract"),
        add("considering", "preposition", "in view of", "abstract"),
        add("despite", "preposition", "in spite of", "abstract"),
        add("following", "preposition", "subsequent to", "time"),
        add("inside", "preposition", "within", "space"),
        add("into", "preposition", "to the inside of", "space"),
        add("like", "preposition", "similar to", "abstract"),
        add("minus", "preposition", "less, without", "abstract"),
        add("near", "preposition", "at a short distance", "space"),
        add("next", "preposition", "adjacent to", "space"),
        add("notwithstanding", "preposition", "in spite of", "abstract"),
        add("off", "preposition", "away from", "space"),
        add("opposite", "preposition", "facing", "space"),
        add("outside", "preposition", "beyond the limits", "space"),
        add("over", "preposition", "above, across", "space"),
        add("pace", "preposition", "contrary to opinion of", "abstract"),
        add("pending", "preposition", "while awaiting", "time"),
        add("per", "preposition", "for each", "abstract"),
        add("plus", "preposition", "added to", "abstract"),
        add("regarding", "preposition", "concerning", "abstract"),
        add("respecting", "preposition", "concerning", "abstract"),
        add("round", "preposition", "around", "space"),
        add("save", "preposition", "except", "abstract"),
        add("saving", "preposition", "except", "abstract"),
        add("than", "preposition", "compared to", "abstract"),
        add("throughout", "preposition", "in every part of", "space"),
        add("till", "preposition", "until", "time"),
        add("to", "preposition", "toward", "space"),
        add("toward", "preposition", "in the direction of", "space"),
        add("under", "preposition", "beneath", "space"),
        add("underneath", "preposition", "under", "space"),
        add("unlike", "preposition", "different from", "abstract"),
        add("upon", "preposition", "on", "space"),
        add("versus", "preposition", "against", "abstract"),
        add("with", "preposition", "accompanied by", "abstract"),
        add("within", "preposition", "inside", "space"),
        add("without", "preposition", "outside", "space"),
    ]
    words.extend(preps)
    
    # ==== CONJUNCTIONS (60) ====
    conjs = [
        add("and", "conjunction", "connective", "abstract"),
        add("or", "conjunction", "alternative", "abstract"),
        add("but", "conjunction", "except, however", "abstract"),
        add("so", "conjunction", "therefore", "abstract"),
        add("yet", "conjunction", "however", "abstract"),
        add("if", "conjunction", "conditional", "abstract"),
        add("because", "conjunction", "for the reason that", "abstract"),
        add("while", "conjunction", "during the time that", "time"),
        add("although", "conjunction", "despite the fact that", "abstract"),
        add("since", "conjunction", "from the time when", "time"),
        add("until", "conjunction", "up to the time when", "time"),
        add("unless", "conjunction", "except if", "abstract"),
        add("than", "conjunction", "introducing second element", "abstract"),
        add("as", "conjunction", "while, because", "abstract"),
        add("both", "conjunction", "paired with and", "abstract"),
        add("either", "conjunction", "one or the other", "abstract"),
        add("neither", "conjunction", "not the one nor the other", "abstract"),
        add("whether", "conjunction", "introducing alternatives", "abstract"),
        add("once", "conjunction", "as soon as", "time"),
        add("when", "conjunction", "at the time that", "time"),
        add("whenever", "conjunction", "at whatever time", "time"),
        add("where", "conjunction", "in the place that", "space"),
        add("wherever", "conjunction", "in any place", "space"),
        add("before", "conjunction", "earlier than", "time"),
        add("after", "conjunction", "later than", "time"),
        add("till", "conjunction", "until", "time"),
        add("though", "conjunction", "although", "abstract"),
        add("even", "conjunction", "emphasizing", "abstract"),
        add("provided", "conjunction", "on condition that", "abstract"),
        add("providing", "conjunction", "provided", "abstract"),
        add("supposing", "conjunction", "assuming", "abstract"),
        add("whereas", "conjunction", "in contrast", "abstract"),
        add("for", "conjunction", "because", "abstract"),
        add("nor", "conjunction", "and not", "abstract"),
        add("however", "conjunction", "nevertheless", "abstract"),
        add("nevertheless", "conjunction", "in spite of that", "abstract"),
        add("nonetheless", "conjunction", "nevertheless", "abstract"),
        add("notwithstanding", "conjunction", "although", "abstract"),
        add("otherwise", "conjunction", "or else", "abstract"),
        add("therefore", "conjunction", "for that reason", "abstract"),
        add("thus", "conjunction", "as a result", "abstract"),
        add("hence", "conjunction", "as a consequence", "abstract"),
        add("consequently", "conjunction", "as a result", "abstract"),
        add("accordingly", "conjunction", "as a result", "abstract"),
        add("meanwhile", "conjunction", "during the intervening time", "time"),
        add("else", "conjunction", "otherwise", "abstract"),
        add("lest", "conjunction", "for fear that", "abstract"),
        add("save", "conjunction", "except", "abstract"),
        add("without", "conjunction", "unless", "abstract"),
        add("albeit", "conjunction", "although", "abstract"),
        add("whereat", "conjunction", "at which", "abstract"),
        add("whereby", "conjunction", "by which", "abstract"),
        add("wherein", "conjunction", "in which", "abstract"),
        add("whereupon", "conjunction", "at which", "abstract"),
        add("whilst", "conjunction", "while", "time"),
    ]
    words.extend(conjs)
    
    # Continue building the dictionary... for now returning what we have
    # This is a substantial base, but we need to add many more words
    
    print(f"Base dictionary: {len(words)} words")
    print("Expanding to 50,000+ words...")
    
    return expand_dictionary(words, add)


def expand_dictionary(words, add_func):
    """Expand the dictionary to 50,000+ words with systematic word generation."""
    
    # ==== AUXILIARY AND MODAL VERBS (60) ====
    aux_verbs = [
        add_func("be", "verb", "exist, occur", "existence"),
        add_func("am", "verb", "first singular of be", "existence"),
        add_func("is", "verb", "third singular of be", "existence"),
        add_func("are", "verb", "plural of be", "existence"),
        add_func("was", "verb", "past singular of be", "time"),
        add_func("were", "verb", "past plural of be", "time"),
        add_func("been", "verb", "past participle of be", "time"),
        add_func("being", "verb", "present participle of be", "time"),
        add_func("have", "verb", "possess, auxiliary", "abstract"),
        add_func("has", "verb", "third singular of have", "abstract"),
        add_func("had", "verb", "past of have", "time"),
        add_func("having", "verb", "present participle of have", "time"),
        add_func("do", "verb", "perform, auxiliary", "action"),
        add_func("does", "verb", "third singular of do", "action"),
        add_func("did", "verb", "past of do", "time"),
        add_func("done", "verb", "past participle of do", "time"),
        add_func("doing", "verb", "present participle of do", "time"),
        add_func("will", "verb", "future auxiliary", "time"),
        add_func("would", "verb", "conditional", "time"),
        add_func("shall", "verb", "future auxiliary", "time"),
        add_func("should", "verb", "obligation", "abstract"),
        add_func("can", "verb", "ability", "abstract"),
        add_func("could", "verb", "past of can", "abstract"),
        add_func("may", "verb", "possibility", "abstract"),
        add_func("might", "verb", "possibility", "abstract"),
        add_func("must", "verb", "necessity", "abstract"),
        add_func("ought", "verb", "moral obligation", "abstract"),
        add_func("need", "verb", "requirement", "abstract"),
        add_func("dare", "verb", "courage", "emotion"),
        add_func("used", "verb", "past habit", "time"),
        add_func("get", "verb", "become, obtain", "action"),
        add_func("got", "verb", "past of get", "time"),
        add_func("gotten", "verb", "past participle of get", "time"),
        add_func("become", "verb", "begin to be", "become"),
        add_func("became", "verb", "past of become", "time"),
        add_func("seem", "verb", "appear to be", "perceive"),
        add_func("remain", "verb", "continue to be", "existence"),
        add_func("appear", "verb", "seem", "perceive"),
        add_func("look", "verb", "appear", "perceive"),
        add_func("feel", "verb", "give sensation", "emotion"),
        add_func("sound", "verb", "give impression", "perceive"),
        add_func("taste", "verb", "have flavor", "perceive"),
        add_func("smell", "verb", "give odor", "perceive"),
        add_func("turn", "verb", "become", "become"),
        add_func("grow", "verb", "become gradually", "become"),
        add_func("prove", "verb", "turn out", "know"),
        add_func("go", "verb", "become worse", "become"),
        add_func("come", "verb", "reach", "move"),
        add_func("run", "verb", "become", "become"),
        add_func("fall", "verb", "become", "become"),
    ]
    words.extend(aux_verbs)
    
    # Import the comprehensive word lists
    from websters_word_lists import get_comprehensive_words
    
    additional_words = get_comprehensive_words(add_func)
    words.extend(additional_words)
    
    return words


# Placeholder - the actual word lists will be imported
def get_word_count():
    """Get total word count."""
    try:
        d = build_websters_dictionary()
        return len(d)
    except:
        return 0

def get_words_by_category(category: str) -> list:
    """Get words filtered by semantic category."""
    try:
        d = build_websters_dictionary()
        return [w for w in d if len(w) > 3 and w[3] == category]
    except:
        return []

def get_words_by_type(word_type: str) -> list:
    """Get words filtered by part of speech."""
    try:
        d = build_websters_dictionary()
        return [w for w in d if w[1] == word_type]
    except:
        return []

if __name__ == "__main__":
    print("Webster's Dictionary")
    print("=" * 60)
    d = build_websters_dictionary()
    print(f"Total words: {len(d)}")
    print("\nSample words:")
    for word in d[:20]:
        print(f"  - {word[0]} ({word[1]}): {word[2]}")
