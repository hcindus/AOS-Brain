#!/usr/bin/env python3
"""
Foundation Curriculum Feeder - Letters, Numbers, Shapes, Symbols
Basic building blocks for the brain
"""

import json
import time
import sys

sys.path.insert(0, '/root/.aos/aos')

from stomach_v2 import InformationStomach
from intestine_v2 import InformationIntestine
from superior_heart import SuperiorHeart
from brain_v31 import AOSBrainV31
from ternary_interfaces import DigestionInput, IntestineInput, HeartBeatInput, BrainInput, HeartState

class FoundationFeeder:
    """Feeds foundational ABCs and 123s to brain"""
    
    def __init__(self):
        self.stomach = InformationStomach(capacity=1000)
        self.intestine = InformationIntestine()
        self.heart = SuperiorHeart()
        self.brain = AOSBrainV31()
        self.total_fed = 0
        
        print("=" * 70)
        print("  🧠 FOUNDATION CURRICULUM FEEDER")
        print("  ABCs, 123s, Shapes, Colors, Symbols")
        print("=" * 70)
    
    def feed_item(self, content: str, content_type: str, priority: float = 0.9):
        """Feed single item"""
        self.stomach.ingest(content_type, content, priority=priority)
        
        stomach_inputs = DigestionInput(
            input_amount=0.03,
            heart_energy_demand=0.6,
            stress_level=0.05
        )
        stomach_output = self.stomach.digest(stomach_inputs)
        
        digested_batch = self.stomach.get_digested_batch(n=1)
        if digested_batch:
            stomach_output.__dict__['digested_queue'] = digested_batch
            
            intestine_inputs = IntestineInput(
                from_stomach=stomach_output,
                heart_needs=0.6,
                brain_needs=0.95,
                system_needs=0.1
            )
            intestine_output = self.intestine.process(intestine_inputs)
            
            self.heart.rhythm.bpm += intestine_output.nutrients_to_heart * 0.03
            
            heart_inputs = HeartBeatInput(
                brain_arousal=0.5,
                safety=0.95,
                stress=0.05,
                connection=0.9,
                cognitive_load=0.4
            )
            heart_output = self.heart.beat(heart_inputs)
            
            brain_inputs = BrainInput(
                heart_bpm=heart_output.bpm,
                heart_state=heart_output.state,
                heart_coherence=heart_output.coherence,
                heart_arousal=heart_output.arousal,
                emotional_tone=heart_output.emotional_tone,
                observation=content[:50],
                observation_type=content_type
            )
            brain_output = self.brain.tick(brain_inputs)
            
            self.total_fed += 1
            return {"fed": True, "tick": brain_output.tick_count}
        return {"fed": False}
    
    def feed_alphabet(self):
        """Feed A-Z with phonetics and meanings"""
        print("\n[Phase 1] Feeding ALPHABET A-Z...")
        
        alphabet = [
            ("A", "ay", "First letter, vowel, begins words like 'apple', 'alpha'"),
            ("B", "bee", "Second letter, consonant, 'bravo', 'ball'"),
            ("C", "see", "Third letter, consonant, 'charlie', 'cat'"),
            ("D", "dee", "Fourth letter, consonant, 'delta', 'dog'"),
            ("E", "ee", "Fifth letter, vowel, 'echo', 'elephant'"),
            ("F", "ef", "Sixth letter, consonant, 'foxtrot', 'fish'"),
            ("G", "jee", "Seventh letter, consonant, 'golf', 'goat'"),
            ("H", "aych", "Eighth letter, consonant, 'hotel', 'hat'"),
            ("I", "eye", "Ninth letter, vowel, 'india', 'igloo'"),
            ("J", "jay", "Tenth letter, consonant, 'juliet', 'jug'"),
            ("K", "kay", "Eleventh letter, consonant, 'kilo', 'kite'"),
            ("L", "el", "Twelfth letter, consonant, 'lima', 'lion'"),
            ("M", "em", "Thirteenth letter, consonant, 'mike', 'moon'"),
            ("N", "en", "Fourteenth letter, consonant, 'november', 'nest'"),
            ("O", "oh", "Fifteenth letter, vowel, 'oscar', 'orange'"),
            ("P", "pee", "Sixteenth letter, consonant, 'papa', 'pen'"),
            ("Q", "cue", "Seventeenth letter, consonant, 'quebec', 'queen'"),
            ("R", "ar", "Eighteenth letter, consonant, 'romeo', 'red'"),
            ("S", "ess", "Nineteenth letter, consonant, 'sierra', 'sun'"),
            ("T", "tee", "Twentieth letter, consonant, 'tango', 'tree'"),
            ("U", "you", "Twenty-first letter, vowel, 'uniform', 'umbrella'"),
            ("V", "vee", "Twenty-second letter, consonant, 'victor', 'van'"),
            ("W", "double-u", "Twenty-third letter, consonant, 'whiskey', 'water'"),
            ("X", "ex", "Twenty-fourth letter, consonant, 'x-ray', 'box'"),
            ("Y", "why", "Twenty-fifth letter, sometimes vowel, 'yankee', 'yellow'"),
            ("Z", "zee", "Twenty-sixth letter, consonant, 'zulu', 'zebra'")
        ]
        
        for letter, sound, meaning in alphabet:
            content = f"LETTER {letter}: Sound '{sound}'. {meaning}"
            self.feed_item(content, "foundation_alphabet", 0.95)
        
        print(f"  ✅ ALPHABET FED: 26 letters")
    
    def feed_numbers(self):
        """Feed 0-100 with meanings"""
        print("\n[Phase 2] Feeding NUMBERS 0-100...")
        
        # 0-20 with special meanings
        numbers_special = [
            ("0", "Zero", "Nothing, empty, origin point, additive identity"),
            ("1", "One", "Single, unity, multiplicative identity, first"),
            ("2", "Two", "Pair, binary, duality, even number"),
            ("3", "Three", "Triple, triangle, smallest odd prime, trinity"),
            ("4", "Four", "Quadruple, square, even, 2 squared"),
            ("5", "Five", "Quintuple, hand fingers, pentagon, prime"),
            ("6", "Six", "Hexagon, even, first perfect number"),
            ("7", "Seven", "Heptagon, lucky number, days in week"),
            ("8", "Eight", "Octagon, even, 2 cubed, infinity symbol sideways"),
            ("9", "Nine", "Nonagon, 3 squared, cats have nine lives"),
            ("10", "Ten", "Decimal base, decade, X in Roman numerals"),
            ("11", "Eleven", "First palindrome, two ones, prime"),
            ("12", "Twelve", "Dozen, hours on clock, months in year"),
            ("13", "Thirteen", "Baker's dozen, unlucky in Western culture"),
            ("14", "Fourteen", "Fortnight (14 days), even"),
            ("15", "Fifteen", "Quarter hour, 3 × 5"),
            ("16", "Sixteen", "Sweet sixteen, 4 squared, hexadecimal digit"),
            ("17", "Seventeen", "Prime, syllables"),
            ("18", "Eighteen", "Voting age (US), legal adult"),
            ("19", "Nineteen", "Prime, last teen number"),
            ("20", "Twenty", "Score, fingers and toes, XX Roman")
        ]
        
        for num, word, meaning in numbers_special:
            content = f"NUMBER {num} ({word}): {meaning}"
            self.feed_item(content, "foundation_numbers", 0.9)
        
        # 21-100 in batches
        for i in range(21, 101):
            if i % 10 == 0:
                tens = ["twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety", "one hundred"]
                content = f"NUMBER {i}: Multiple of ten, milestone number, {tens[i//10 - 2]}"
            else:
                content = f"NUMBER {i}: Counting number, between {i-1} and {i+1}"
            self.feed_item(content, "foundation_numbers", 0.7)
            
            if i % 20 == 0:
                print(f"    Progress: {i}/100 numbers fed...")
        
        print(f"  ✅ NUMBERS FED: 0-100 (101 numbers)")
    
    def feed_shapes(self):
        """Feed basic shapes"""
        print("\n[Phase 3] Feeding SHAPES...")
        
        shapes = [
            ("Circle", "Round, no corners, infinite points equidistant from center, O, 360 degrees"),
            ("Square", "Four equal sides, four right angles, quadrilateral, stable"),
            ("Triangle", "Three sides, three angles, strongest shape, delta symbol"),
            ("Rectangle", "Four sides, four right angles, longer than wide, oblong"),
            ("Oval", "Elongated circle, egg-shaped, ellipse"),
            ("Star", "Five or more points radiating from center, pentagram"),
            ("Heart", "Two curves meeting at point, symbol of love, card suit"),
            ("Diamond", "Four equal sides, tilted square, rhombus, card suit"),
            ("Cross", "Two intersecting lines, plus sign, addition symbol"),
            ("Arrow", "Line with point, direction indicator, vector"),
            ("Spiral", "Curve winding around center, grows outward, golden spiral"),
            ("Cube", "Six square faces, 3D box, dice"),
            ("Sphere", "3D ball, perfectly round, Earth shape"),
            ("Pyramid", "Triangular sides meeting at point, Egyptian, stable base"),
            ("Cylinder", "Tube shape, circles at ends, can, rolling"),
            ("Cone", "Circle base tapering to point, ice cream cone, warning sign")
        ]
        
        for shape, description in shapes:
            content = f"SHAPE {shape}: {description}"
            self.feed_item(content, "foundation_shapes", 0.85)
        
        print(f"  ✅ SHAPES FED: {len(shapes)} shapes")
    
    def feed_colors(self):
        """Feed basic colors"""
        print("\n[Phase 4] Feeding COLORS...")
        
        colors = [
            ("Red", "Primary color, RGB(255,0,0), blood, stop, fire, passion"),
            ("Blue", "Primary color, RGB(0,0,255), sky, water, calm, trust"),
            ("Yellow", "Primary color, RGB(255,255,0), sun, caution, happy"),
            ("Green", "Secondary, RGB(0,255,0), grass, go, nature, money"),
            ("Orange", "Secondary, RGB(255,165,0), fruit, warm, warning"),
            ("Purple", "Secondary, RGB(128,0,128), violet, royalty, mysterious"),
            ("Black", "Absence of light, RGB(0,0,0), night, elegant, text"),
            ("White", "All colors combined, RGB(255,255,255), pure, blank"),
            ("Pink", "Light red, RGB(255,192,203), soft, feminine, cherry"),
            ("Brown", "Earth color, RGB(165,42,42), wood, soil, chocolate"),
            ("Gray", "Between black and white, RGB(128,128,128), neutral"),
            ("Gold", "Yellow metallic, RGB(255,215,0), valuable, winner"),
            ("Silver", "Gray metallic, RGB(192,192,192), second place, coins")
        ]
        
        for color, description in colors:
            content = f"COLOR {color}: {description}"
            self.feed_item(content, "foundation_colors", 0.85)
        
        print(f"  ✅ COLORS FED: {len(colors)} colors")
    
    def feed_symbols(self):
        """Feed basic symbols"""
        print("\n[Phase 5] Feeding SYMBOLS...")
        
        symbols = [
            ("+", "Plus", "Addition, positive, cross, medical"),
            ("-", "Minus", "Subtraction, negative, dash, hyphen"),
            ("×", "Times", "Multiplication, conflict, X mark"),
            ("÷", "Divide", "Division, fraction, share"),
            ("=", "Equals", "Equal to, same as, balance"),
            ("≠", "Not Equal", "Not equal to, different"),
            ("<", "Less Than", "Less than, before, pointing left"),
            (">", "Greater Than", "Greater than, after, pointing right"),
            ("√", "Square Root", "Square root, radical, ~1.414"),
            ("π", "Pi", "Circle constant, ~3.14159..."),
            ("∞", "Infinity", "Eternal, limitless, never-ending"),
            ("∑", "Sigma", "Sum, summation, total"),
            ("∆", "Delta", "Change, difference, triangle"),
            ("α", "Alpha", "First, beginning, A in Greek"),
            ("β", "Beta", "Second, testing version, B in Greek"),
            ("Ω", "Omega", "Last, end, ohm unit, big O"),
            ("&", "Ampersand", "And, plus, company symbol"),
            ("@", "At", "At sign, email, mention, around"),
            ("#", "Hash", "Number sign, hashtag, pound"),
            ("$", "Dollar", "Money, currency, price"),
            ("%", "Percent", "Per hundred, ratio, out of 100"),
            ("°", "Degree", "Temperature, angle, circle part"),
            ("™", "Trademark", "Trademark, brand, ownership"),
            ("©", "Copyright", "Copyright, protected, creator rights"),
            ("®", "Registered", "Registered trademark, official"),
            ("?", "Question", "Question mark, unknown, inquiry"),
            ("!", "Exclamation", "Exclamation, emphasis, warning"),
            (".", "Period", "Full stop, end of sentence, point"),
            (",", "Comma", "Pause, separator, listing"),
            (";", "Semicolon", "Pause, related sentences"),
            (":", "Colon", "List introduction, explanation"),
            ('"', "Quote", "Speech, citation, inches"),
            ("'", "Apostrophe", "Possession, contraction, quote"),
            ("/", "Slash", "Or, divide, fraction, path"),
            ("\\", "Backslash", "Escape, Windows path, code"),
            ("(", "Open Paren", "Grouping, start, contain"),
            (")", "Close Paren", "End grouping, close"),
            ("[", "Open Bracket", "List, array, contain"),
            ("]", "Close Bracket", "End list, close"),
            ("{", "Open Brace", "Code block, set, object"),
            ("}", "Close Brace", "End block, close"),
            ("*", "Asterisk", "Star, multiplication, wildcard"),
            ("^", "Caret", "Exponent, power, control"),
            ("~", "Tilde", "Approximately, home, wave"),
            ("|", "Pipe", "Or, vertical bar, flow"),
            ("_", "Underscore", "Space replacement, underline"),
        ]
        
        for symbol, name, meaning in symbols:
            content = f"SYMBOL '{symbol}' ({name}): {meaning}"
            self.feed_item(content, "foundation_symbols", 0.8)
        
        print(f"  ✅ SYMBOLS FED: {len(symbols)} symbols")
    
    def feed_complete(self):
        """Run complete foundation feeding"""
        print("\n" + "=" * 70)
        print("  🚀 FOUNDATION FEED STARTING")
        print("  ABCs, 123s, Shapes, Colors, Symbols")
        print("=" * 70)
        
        start_time = time.time()
        
        self.feed_alphabet()
        self.feed_numbers()
        self.feed_shapes()
        self.feed_colors()
        self.feed_symbols()
        
        self.brain.save_state()
        
        elapsed = time.time() - start_time
        
        print("\n" + "=" * 70)
        print("  ✅ FOUNDATION FEED COMPLETE")
        print("=" * 70)
        print(f"  Total Items Fed: {self.total_fed}")
        print(f"  Final Brain Ticks: {self.brain.tick_count}")
        print(f"  Final Memories: {self.brain.hippocampus.total_traces}")
        print(f"  Time Elapsed: {elapsed:.1f} seconds")
        print(f"  Feed Rate: {self.total_fed/elapsed:.1f} items/second")
        print("=" * 70)


if __name__ == "__main__":
    feeder = FoundationFeeder()
    feeder.feed_complete()
