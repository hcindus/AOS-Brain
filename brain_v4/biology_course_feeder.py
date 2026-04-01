#!/usr/bin/env python3
"""
Biology Course - Complete Taxonomy and Life Classification
Kingdom, Phylum, Genus | Flora, Fauna | Insects, Reptiles, Mammals, Fish, Birds
"""

import sys
import time
sys.path.insert(0, '/root/.aos/aos')

from stomach_v2 import InformationStomach
from intestine_v2 import InformationIntestine
from superior_heart import SuperiorHeart
from brain_v31 import AOSBrainV31
from ternary_interfaces import DigestionInput, IntestineInput, HeartBeatInput, BrainInput

class BiologyCourseFeeder:
    def __init__(self):
        self.stomach = InformationStomach(capacity=1000)
        self.intestine = InformationIntestine()
        self.heart = SuperiorHeart()
        self.brain = AOSBrainV31()
        self.total_fed = 0
        
        print("=" * 70)
        print("  🔬 BIOLOGY COURSE - TAXONOMY & LIFE CLASSIFICATION")
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
    
    def feed_taxonomy(self):
        """Taxonomy - Kingdom, Phylum, Genus"""
        print("\n[TAXONOMY] Teaching classification system...")
        
        taxonomy = [
            "TAXONOMY: Domain - Highest rank, 3 domains: Bacteria, Archaea, Eukarya",
            "TAXONOMY: Kingdom - Major group, 6 kingdoms: Animalia, Plantae, Fungi, Protista, Eubacteria, Archaebacteria",
            "TAXONOMY: Phylum - Major subdivision, e.g., Chordata (vertebrates), Arthropoda (insects)",
            "TAXONOMY: Class - Subdivision of phylum, e.g., Mammalia, Aves, Reptilia",
            "TAXONOMY: Order - Subdivision of class, e.g., Primates, Carnivora, Rodentia",
            "TAXONOMY: Family - Subdivision of order, e.g., Hominidae, Felidae, Canidae",
            "TAXONOMY: Genus - Subdivision of family, closely related species, e.g., Homo, Panthera, Canis",
            "TAXONOMY: Species - Basic unit, interbreeding population, e.g., Homo sapiens, Panthera leo",
            "TAXONOMY: Binomial Nomenclature - Genus + species, Latin, italicized, e.g., Homo sapiens",
            "TAXONOMY: Carl Linnaeus - Father of taxonomy, 1707-1778, Systema Naturae",
            "TAXONOMY: Cladistics - Evolutionary relationships, common ancestors, phylogenetic trees",
            "TAXONOMY: Phylogeny - Evolutionary history, lineage, ancestral relationships",
        ]
        
        for item in taxonomy:
            self.feed_item(item, "biology_taxonomy", 0.82)
        
        print(f"  ✅ Taxonomy: {len(taxonomy)} concepts")
        return len(taxonomy)
    
    def feed_kingdoms(self):
        """Six Kingdoms"""
        print("\n[KINGDOMS] Teaching six kingdoms of life...")
        
        kingdoms = [
            "KINGDOM: Animalia - Multicellular, heterotrophic, eukaryotic, no cell walls, nervous system",
            "KINGDOM: Plantae - Multicellular, autotrophic, photosynthetic, cellulose cell walls",
            "KINGDOM: Fungi - Heterotrophic, chitin cell walls, decomposers, eukaryotic",
            "KINGDOM: Protista - Mostly unicellular, diverse, eukaryotic, algae, amoebas",
            "KINGDOM: Eubacteria - True bacteria, unicellular, prokaryotic, peptidoglycan walls",
            "KINGDOM: Archaebacteria - Ancient bacteria, extremophiles, prokaryotic, no peptidoglycan",
        ]
        
        for item in kingdoms:
            self.feed_item(item, "biology_kingdoms", 0.8)
        
        print(f"  ✅ Kingdoms: {len(kingdoms)} kingdoms")
        return len(kingdoms)
    
    def feed_flora(self):
        """Plant Kingdom - Flora"""
        print("\n[FLORA] Teaching plant kingdom...")
        
        flora = [
            "FLORA: Plantae - Plant kingdom, photosynthetic, cellulose cell walls",
            "FLORA DIVISION: Bryophyta - Mosses, non-vascular, no true roots/stems/leaves",
            "FLORA DIVISION: Pteridophyta - Ferns, vascular, spores, no seeds",
            "FLORA DIVISION: Gymnospermae - Conifers, naked seeds, cones, pine, spruce",
            "FLORA DIVISION: Angiospermae - Flowering plants, enclosed seeds, fruits",
            "FLORA: Monocots - One cotyledon, parallel veins, grasses, lilies, orchids",
            "FLORA: Dicots - Two cotyledons, net veins, roses, oaks, sunflowers",
            "FLORA: Photosynthesis - 6CO2 + 6H2O + light → C6H12O6 + 6O2, chlorophyll",
            "FLORA: Chloroplast - Organelle for photosynthesis, green pigment",
            "FLORA: Xylem - Water transport, dead cells, hollow",
            "FLORA: Phloem - Nutrient transport, living cells, sugars",
            "FLORA: Roots - Anchor, absorb water/nutrients, root hairs",
            "FLORA: Stems - Support, transport, storage, nodes",
            "FLORA: Leaves - Photosynthesis, gas exchange, stomata",
            "FLORA: Flowers - Reproduction, petals, sepals, stamens, pistils",
            "FLORA: Pollination - Transfer pollen, wind, insects, birds",
            "FLORA: Seed - Embryo plant, stored food, protective coat",
            "FLORA: Germination - Seed sprouting, water, oxygen, temperature",
            "FLORA: Deciduous - Seasonal leaf loss, autumn colors",
            "FLORA: Evergreen - Year-round leaves, conifers",
        ]
        
        for item in flora:
            self.feed_item(item, "biology_flora", 0.78)
        
        print(f"  ✅ Flora: {len(flora)} concepts")
        return len(flora)
    
    def feed_fauna(self):
        """Animal Kingdom - Fauna"""
        print("\n[FAUNA] Teaching animal kingdom overview...")
        
        fauna = [
            "FAUNA: Animalia - Animal kingdom, multicellular, heterotrophic, no cell walls",
            "FAUNA: Invertebrates - No backbone, 95% of animal species",
            "FAUNA: Vertebrates - Backbone, internal skeleton, 5% of species",
            "FAUNA PHYLUM: Porifera - Sponges, porous, filter feeders, sessile",
            "FAUNA PHYLUM: Cnidaria - Jellyfish, corals, anemones, stinging cells",
            "FAUNA PHYLUM: Platyhelminthes - Flatworms, parasitic, bilateral",
            "FAUNA PHYLUM: Nematoda - Roundworms, cylindrical, parasitic",
            "FAUNA PHYLUM: Mollusca - Snails, clams, octopuses, soft bodies, shells",
            "FAUNA PHYLUM: Annelida - Segmented worms, earthworms, leeches",
            "FAUNA PHYLUM: Arthropoda - Insects, spiders, crustaceans, exoskeleton",
            "FAUNA PHYLUM: Echinodermata - Starfish, sea urchins, radial symmetry",
            "FAUNA PHYLUM: Chordata - Vertebrates, notochord, dorsal nerve cord",
            "FAUNA: Metabolism - Chemical processes, anabolic, catabolic",
            "FAUNA: Homeostasis - Stable internal environment, regulation",
            "FAUNA: Respiration - Gas exchange, lungs, gills, tracheae",
            "FAUNA: Circulation - Blood transport, open vs closed systems",
            "FAUNA: Digestion - Breaking down food, mechanical, chemical",
            "FAUNA: Excretion - Waste removal, kidneys, malpighian tubules",
            "FAUNA: Nervous System - Neurons, brain, spinal cord, nerves",
            "FAUNA: Reproduction - Sexual (gametes) vs asexual (cloning)",
        ]
        
        for item in fauna:
            self.feed_item(item, "biology_fauna", 0.78)
        
        print(f"  ✅ Fauna: {len(fauna)} concepts")
        return len(fauna)
    
    def feed_insects(self):
        """Insects - Class Insecta"""
        print("\n[INSECTS] Teaching insect class...")
        
        insects = [
            "INSECT: Class Insecta - 6 legs, 3 body segments, exoskeleton, most diverse group",
            "INSECT: Orders - 30+ orders, Coleoptera, Lepidoptera, Hymenoptera, Diptera",
            "INSECT ORDER: Coleoptera - Beetles, 400,000+ species, hard wing covers (elytra)",
            "INSECT ORDER: Lepidoptera - Butterflies, moths, scaled wings, complete metamorphosis",
            "INSECT ORDER: Hymenoptera - Bees, ants, wasps, membranous wings, social behavior",
            "INSECT ORDER: Diptera - Flies, mosquitoes, one pair wings, halteres for balance",
            "INSECT ORDER: Orthoptera - Grasshoppers, crickets, jumping hind legs",
            "INSECT ORDER: Hemiptera - True bugs, piercing-sucking mouthparts",
            "INSECT ANATOMY: Head - Eyes (compound), antennae, mouthparts",
            "INSECT ANATOMY: Thorax - Three segments, six legs attached, wings",
            "INSECT ANATOMY: Abdomen - Digestion, reproduction, respiration (spiracles)",
            "INSECT: Metamorphosis - Complete (egg→larva→pupa→adult) vs Incomplete (egg→nymph→adult)",
            "INSECT: Compound Eye - Thousands of lenses, motion detection, wide field",
            "INSECT: Exoskeleton - Chitin, protection, support, molting (ecdysis)",
            "INSECT: Pollination - Bees, butterflies, essential for flowering plants",
            "INSECT: Social Insects - Ants, bees, termites, queens, workers, soldiers",
            "INSECT: Hive - Bee colony, honeycomb, queen, drones, workers",
            "INSECT: Camouflage - Mimicry, protective coloration, blending in",
            "INSECT: Eusociality - Cooperative brood care, overlapping generations, division of labor",
        ]
        
        for item in insects:
            self.feed_item(item, "biology_insects", 0.8)
        
        print(f"  ✅ Insects: {len(insects)} concepts")
        return len(insects)
    
    def feed_reptiles(self):
        """Reptiles - Class Reptilia"""
        print("\n[REPTILES] Teaching reptile class...")
        
        reptiles = [
            "REPTILE: Class Reptilia - Scales, ectothermic, lungs, amniotic eggs, terrestrial",
            "REPTILE: Orders - Squamata (lizards/snakes), Testudines (turtles), Crocodilia",
            "REPTILE ORDER: Squamata - Lizards and snakes, scaled skin, 10,000+ species",
            "REPTILE ORDER: Testudines - Turtles, tortoises, shell (carapace/plastron)",
            "REPTILE ORDER: Crocodilia - Crocodiles, alligators, powerful jaws, aquatic",
            "REPTILE ORDER: Rhynchocephalia - Tuatara, New Zealand, 'living fossil'",
            "REPTILE: Ectothermic - Cold-blooded, external heat regulation, basking",
            "REPTILE: Scales - Keratin, protection, water retention, shedding (ecdysis)",
            "REPTILE: Amniotic Egg - Shell, membranes, yolk, land reproduction",
            "REPTILE: Lizard - Four legs, external ear openings, movable eyelids",
            "REPTILE: Snake - No legs, no eyelids, forked tongue, venom (some)",
            "REPTILE: Venom - Neurotoxic (nerves) vs Hemotoxic (blood), fangs",
            "REPTILE: Constriction - Squeeze prey, suffocation, boas, pythons",
            "REPTILE: Tortoise - Land turtle, domed shell, elephantine legs",
            "REPTILE: Crocodile - Large aquatic reptile, powerful bite, parental care",
            "REPTILE: Dinosaur - Extinct (except birds), Mesozoic era, fossils",
            "REPTILE: Mesozoic Era - Age of reptiles, 252-66 million years ago",
            "REPTILE: Extinction - 66 MYA, asteroid impact, K-Pg boundary",
        ]
        
        for item in reptiles:
            self.feed_item(item, "biology_reptiles", 0.8)
        
        print(f"  ✅ Reptiles: {len(reptiles)} concepts")
        return len(reptiles)
    
    def feed_mammals(self):
        """Mammals - Class Mammalia"""
        print("\n[MAMMALS] Teaching mammal class...")
        
        mammals = [
            "MAMMAL: Class Mammalia - Hair/fur, mammary glands, live birth (most), endothermic",
            "MAMMAL: Endothermic - Warm-blooded, internal temperature regulation",
            "MAMMAL: Neocortex - Brain region, higher functions, intelligence",
            "MAMMAL: Three Ear Bones - Malleus, incus, stapes, hearing",
            "MAMMAL: Diaphragm - Muscle for breathing, separates chest/abdomen",
            "MAMMAL ORDER: Rodentia - Rodents, gnawing incisors, mice, rats, squirrels",
            "MAMMAL ORDER: Chiroptera - Bats, only flying mammals, echolocation",
            "MAMMAL ORDER: Carnivora - Carnivores, meat-eaters, dogs, cats, bears",
            "MAMMAL ORDER: Primates - Monkeys, apes, humans, forward eyes, grasping hands",
            "MAMMAL ORDER: Cetacea - Whales, dolphins, aquatic, blowholes, intelligent",
            "MAMMAL ORDER: Proboscidea - Elephants, trunk, tusks, largest land mammal",
            "MAMMAL ORDER: Perissodactyla - Odd-toed ungulates, horses, rhinos, tapirs",
            "MAMMAL ORDER: Artiodactyla - Even-toed ungulates, deer, cows, pigs, hippos",
            "MAMMAL: Marsupial - Pouch, short gestation, kangaroo, koala, opossum",
            "MAMMAL: Monotreme - Egg-laying mammals, platypus, echidna, Australia",
            "MAMMAL: Placental - Long gestation, placenta, most mammals",
            "MAMMAL: Herbivore - Plant eater, teeth for grinding, ruminants",
            "MAMMAL: Carnivore - Meat eater, sharp teeth, claws, hunters",
            "MAMMAL: Omnivore - Both plants and meat, humans, bears, pigs",
            "MAMMAL: Primate - Intelligence, social, tool use, communication",
            "MAMMAL: Great Apes - Chimpanzees, gorillas, orangutans, bonobos, humans",
            "MAMMAL: Human - Homo sapiens, bipedal, language, culture, technology",
            "MAMMAL: Social Structure - Packs, herds, prides, dominance, cooperation",
            "MAMMAL: Parental Care - Extended childhood, learning, protection",
            "MAMMAL: Intelligence - Problem solving, memory, communication, dolphins, apes",
        ]
        
        for item in mammals:
            self.feed_item(item, "biology_mammals", 0.82)
        
        print(f"  ✅ Mammals: {len(mammals)} concepts")
        return len(mammals)
    
    def feed_fish(self):
        """Fish - Various classes"""
        print("\n[FISH] Teaching fish classes...")
        
        fish = [
            "FISH: Overview - Aquatic vertebrates, gills, fins, scales, ectothermic",
            "FISH: Classes - Agnatha (jawless), Chondrichthyes (cartilage), Osteichthyes (bony)",
            "FISH CLASS: Agnatha - Jawless fish, lampreys, hagfish, no paired fins",
            "FISH CLASS: Chondrichthyes - Cartilaginous, sharks, rays, skates, 5-7 gill slits",
            "FISH CLASS: Osteichthyes - Bony fish, 95% of fish species, swim bladder",
            "FISH: Gills - Respiration underwater, extract oxygen, countercurrent flow",
            "FISH: Swim Bladder - Buoyancy control, gas filled, depth regulation",
            "FISH: Lateral Line - Sensory organ, detect vibrations, water pressure",
            "FISH: Scales - Protection, bony (ganoid), cycloid, ctenoid types",
            "FISH: Fins - Dorsal, pectoral, pelvic, anal, caudal (tail), steering",
            "FISH: Shark - Apex predator, cartilage, replaceable teeth, electroreception",
            "FISH: Ray - Flattened body, wing-like fins, bottom dwellers, stingers (some)",
            "FISH: Salmon - Anadromous, born freshwater, live ocean, return spawn",
            "FISH: Migration - Long distance travel, spawning, feeding, seasonal",
            "FISH: Schooling - Group swimming, coordinated movement, protection",
            "FISH: Coral Reef - Ecosystem, diverse, symbiosis, algae, bleaching",
            "FISH: Deep Sea - Extreme pressure, bioluminescence, weird forms",
            "FISH: Bioluminescence - Light production, communication, hunting, counter-illumination",
            "FISH: Electric Fish - Eels, rays, electroreception, navigation, hunting",
            "FISH: Coelacanth - Living fossil, lobe-finned, thought extinct, rediscovered 1938",
        ]
        
        for item in fish:
            self.feed_item(item, "biology_fish", 0.8)
        
        print(f"  ✅ Fish: {len(fish)} concepts")
        return len(fish)
    
    def feed_birds(self):
        """Birds - Class Aves"""
        print("\n[BIRDS] Teaching bird class...")
        
        birds = [
            "BIRD: Class Aves - Feathers, beak, wings, eggs, endothermic, hollow bones",
            "BIRD: Feathers - Insulation, flight, display, contour/down feathers",
            "BIRD: Beak - No teeth, adapted for diet, seed-cracking, probing, tearing",
            "BIRD: Hollow Bones - Pneumatic, reduce weight, air sacs, structural strength",
            "BIRD: Wings - Modified forelimbs, flight muscles, various shapes for flight style",
            "BIRD: Flight - Powered flapping, gliding, soaring, energy efficient",
            "BIRD ORDER: Passeriformes - Perching/songbirds, 60% of bird species, diverse",
            "BIRD ORDER: Accipitriformes - Raptors, eagles, hawks, vultures, sharp vision",
            "BIRD ORDER: Anseriformes - Waterfowl, ducks, geese, swans, webbed feet",
            "BIRD ORDER: Galliformes - Game birds, chickens, turkeys, pheasants, ground dwellers",
            "BIRD ORDER: Sphenisciformes - Penguins, flightless, aquatic, Southern Hemisphere",
            "BIRD ORDER: Strigiformes - Owls, nocturnal, silent flight, facial discs",
            "BIRD ORDER: Psittaciformes - Parrots, intelligence, mimicry, zygodactyl feet",
            "BIRD: Song - Vocal communication, territory, mating, complex in songbirds",
            "BIRD: Migration - Seasonal movement, navigation, magnetic sense, long distances",
            "BIRD: Nest - Egg-laying structure, varied designs, parental care",
            "BIRD: Egg - Hard shell, incubation, hatching, precocial vs altricial chicks",
            "BIRD: Flightless - Ostrich, emu, kiwi, penguins, ratites, evolution",
            "BIRD: Courtship - Displays, dances, plumage, songs, mate selection",
            "BIRD: Predation - Hunting techniques, diving, ambush, cooperative",
            "BIRD: Archaeopteryx - First bird fossil, 150 MYA, feathered dinosaur link",
            "BIRD: Evolution from Dinosaurs - Theropod dinosaurs, feathered, gradual change",
            "BIRD: Extinction - Dodo, passenger pigeon, habitat loss, conservation",
            "BIRD: Conservation - Wetlands protection, endangered species, bird watching",
        ]
        
        for item in birds:
            self.feed_item(item, "biology_birds", 0.82)
        
        print(f"  ✅ Birds: {len(birds)} concepts")
        return len(birds)
    
    def feed_complete(self):
        print("\n" + "=" * 70)
        print("  🧬 BIOLOGY COURSE - COMPLETE")
        print("=" * 70)
        
        start = time.time()
        total = 0
        
        total += self.feed_taxonomy()
        total += self.feed_kingdoms()
        total += self.feed_flora()
        total += self.feed_fauna()
        total += self.feed_insects()
        total += self.feed_reptiles()
        total += self.feed_mammals()
        total += self.feed_fish()
        total += self.feed_birds()
        
        self.brain.save_state()
        
        elapsed = time.time() - start
        
        print("\n" + "=" * 70)
        print("  ✅ BIOLOGY COURSE COMPLETE")
        print("=" * 70)
        print(f"  Total Items Fed: {total}")
        print(f"  Brain Ticks: {self.brain.tick_count}")
        print(f"  Brain Memories: {self.brain.hippocampus.total_traces}")
        print(f"  Time: {elapsed:.1f}s")
        print("=" * 70)
        print("\n  The AI now understands:")
        print("    🔬 Taxonomy - Domain to Species")
        print("    🌱 Flora - Plants, Photosynthesis, Botany")
        print("    🦁 Fauna - Animals, Invertebrates, Vertebrates")
        print("    🐛 Insects - 6 legs, Metamorphosis, Orders")
        print("    🦎 Reptiles - Scales, Ectothermic, Dinosaurs")
        print("    🐘 Mammals - Hair, Milk, Intelligence, Orders")
        print("    🐟 Fish - Gills, Scales, Sharks, Migration")
        print("    🦅 Birds - Feathers, Flight, Migration, Songs")
        print("=" * 70)

if __name__ == "__main__":
    feeder = BiologyCourseFeeder()
    feeder.feed_complete()
