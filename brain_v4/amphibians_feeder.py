#!/usr/bin/env python3
"""
Amphibians - The Forgotten Class
"""

import sys
sys.path.insert(0, '/root/.aos/aos')

from stomach_v2 import InformationStomach
from intestine_v2 import InformationIntestine
from superior_heart import SuperiorHeart
from brain_v31 import AOSBrainV31
from ternary_interfaces import DigestionInput, IntestineInput, HeartBeatInput, BrainInput

class AmphibiansFeeder:
    def __init__(self):
        self.stomach = InformationStomach(capacity=100)
        self.intestine = InformationIntestine()
        self.heart = SuperiorHeart()
        self.brain = AOSBrainV31()
        self.total_fed = 0
        print("=" * 70)
        print("  🐸 AMPHIBIANS - The Forgotten Class!")
        print("=" * 70)
    
    def feed_item(self, content, content_type, priority=0.8):
        self.stomach.ingest(content_type, content, priority=priority)
        stomach_inputs = DigestionInput(input_amount=0.03, heart_energy_demand=0.7, stress_level=0.1)
        stomach_output = self.stomach.digest(stomach_inputs)
        digested_batch = self.stomach.get_digested_batch(n=1)
        if digested_batch:
            stomach_output.__dict__['digested_queue'] = digested_batch
            intestine_inputs = IntestineInput(from_stomach=stomach_output, heart_needs=0.7, brain_needs=0.9, system_needs=0.2)
            intestine_output = self.intestine.process(intestine_inputs)
            self.heart.rhythm.bpm += intestine_output.nutrients_to_heart * 0.05
            heart_inputs = HeartBeatInput(brain_arousal=0.6, safety=0.9, stress=0.1, connection=0.8, cognitive_load=0.7)
            heart_output = self.heart.beat(heart_inputs)
            brain_inputs = BrainInput(heart_bpm=heart_output.bpm, heart_state=heart_output.state, heart_coherence=heart_output.coherence, heart_arousal=heart_output.arousal, emotional_tone=heart_output.emotional_tone, observation=content[:100], observation_type=content_type)
            self.brain.tick(brain_inputs)
            self.total_fed += 1
            return True
        return False
    
    def feed_amphibians(self):
        """Amphibian class"""
        print("\n[AMPHIBIANS] Teaching amphibian class...")
        
        amph = [
            "AMPHIBIAN: Class Amphibia - Cold-blooded vertebrates, dual life, water and land",
            "AMPHIBIAN: Etymology - Greek 'amphi' (both) + 'bios' (life), two lives",
            "AMPHIBIAN: Characteristics - Moist skin, permeable, cutaneous respiration",
            "AMPHIBIAN: Metamorphosis - Egg to larva (gills) to adult (lungs), complete transformation",
            "AMPHIBIAN: Skin - Permeable, must stay moist, mucus glands, no scales",
            "AMPHIBIAN: Respiration - Larvae: gills, Adults: lungs + skin, cutaneous gas exchange",
            "AMPHIBIAN: Reproduction - External fertilization (mostly), jelly eggs, water required",
            "AMPHIBIAN: Senses - Lateral line (larvae), keen smell, hearing via eardrum",
            "AMPHIBIAN ORDER: Anura - Frogs and toads, tailless adults, jumping, 7,000+ species",
            "AMPHIBIAN: Frogs - Smooth moist skin, longer hind legs, leap, aquatic, croaking",
            "AMPHIBIAN: Toads - Dry warty skin, shorter legs, walk, terrestrial, parotoid glands",
            "FROG: Lifecycle - Egg → Tadpole (herbivore) → Metamorphosis → Adult (carnivore)",
            "FROG: Tadpole - Aquatic larva, gills, tail, herbivore, algae eater",
            "FROG: Anatomy - Powerful hind legs, webbed feet, protrusible tongue, bulging eyes",
            "FROG: Croaking - Males vocalize, vocal sac, mating calls, territorial",
            "AMPHIBIAN ORDER: Caudata - Salamanders and newts, long tails, 700+ species",
            "SALAMANDER: Body - Long tail, four legs equal size, lizard-like, moist skin",
            "SALAMANDER: Regeneration - Remarkable ability, limbs, tail, heart, lens, spinal cord",
            "SALAMANDER: Habitat - Moist woodlands, streams, nocturnal, hide under objects",
            "NEWT - Aquatic salamander, rough skin, breeding season colors, Europe/Asia",
            "AXOLOTL - Mexican salamander, neotenic, keeps gills, popular pet, endangered wild",
            "AMPHIBIAN ORDER: Gymnophiona - Caecilians, legless, burrowing, 200+ species",
            "CAECILIAN: Appearance - Worm-like, snake-like, segmented, tiny eyes (skin-covered)",
            "CAECILIAN: Lifestyle - Burrowing, tropical, soil, prey on worms/termites",
            "AMPHIBIAN: Toxins - Many poisonous, skin secretions, bufotoxin (toads), tetrodotoxin",
            "POISON DART FROG - Bright warning colors, most toxic, indigenous darts, Phyllobates",
            "AMPHIBIAN: Decline - Global population crash, chytrid fungus, habitat loss, climate",
            "CHYTRID FUNGUS - Batrachochytrium dendrobatidis, amphibian killer, skin infection",
            "AMPHIBIAN: Indicator Species - Sensitive to pollution, environmental health",
            "AMPHIBIAN: Evolution - First tetrapods, Devonian, 370 MYA, Ichthyostega",
            "AMPHIBIAN: Species Count - 8,000+ species, most threatened vertebrate class",
            "BULLFROG - Largest North American frog, invasive, deep call, voracious",
            "TREE FROG - Adhesive toe pads, climbing, arboreal, many species worldwide",
            "GLASS FROG - Transparent abdominal skin, visible organs, Central/South America",
            "PAEDOPHRYNE - Smallest vertebrate, 7.7mm frog, Papua New Guinea",
            "GOLIATH FROG - Largest frog, 32cm, 3.3kg, Cameroon, Africa",
            "HELLBENDER - Giant salamander, 74cm, North America, aquatic, wrinkly skin",
        ]
        
        for item in amph:
            self.feed_item(item, "biology_amphibians", 0.82)
        
        print(f"  ✅ Amphibians: {len(amph)} concepts")
        return len(amph)
    
    def feed_complete(self):
        print("\n" + "=" * 70)
        print("  🐸 AMPHIBIANS COMPLETE")
        print("=" * 70)
        
        import time
        start = time.time()
        total = 0
        
        total += self.feed_amphibians()
        
        self.brain.save_state()
        
        elapsed = time.time() - start
        
        print("\n" + "=" * 70)
        print(f"  Total: {total} amphibian concepts")
        print(f"  Brain Ticks: {self.brain.tick_count}")
        print("=" * 70)
        print("\n  The AI now knows:")
        print("    🐸 Frogs and Toads (Anura)")
        print("    🦎 Salamanders and Newts (Caudata)")
        print("    🐍 Caecilians (Gymnophiona)")
        print("    💧 Dual life - water and land")
        print("    🔄 Complete metamorphosis")
        print("    ☠️ Poison dart frogs")
        print("    🚨 Global decline (chytrid fungus)")
        print("=" * 70)

if __name__ == "__main__":
    feeder = AmphibiansFeeder()
    feeder.feed_complete()
