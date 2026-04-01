#!/usr/bin/env python3
"""
Astronomy Course - Solar System, Galaxies, Cosmology
"""

import sys
import time
sys.path.insert(0, '/root/.aos/aos')

from stomach_v2 import InformationStomach
from intestine_v2 import InformationIntestine
from superior_heart import SuperiorHeart
from brain_v31 import AOSBrainV31
from ternary_interfaces import DigestionInput, IntestineInput, HeartBeatInput, BrainInput

class AstronomyCourseFeeder:
    def __init__(self):
        self.stomach = InformationStomach(capacity=1000)
        self.intestine = InformationIntestine()
        self.heart = SuperiorHeart()
        self.brain = AOSBrainV31()
        self.total_fed = 0
        
        print("=" * 70)
        print("  🔭 ASTRONOMY COURSE - SOLAR SYSTEM & GALAXIES")
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
    
    def feed_solar_system(self):
        """Solar System"""
        print("\n[SOLAR SYSTEM] Teaching solar system...")
        
        solar = [
            "SOLAR SYSTEM: Overview - Sun + 8 planets, moons, asteroids, comets, Kuiper Belt, Oort Cloud",
            "SUN: Star - Type G2V, 99.86% system mass, hydrogen fusion, photosphere, corona",
            "SUN: Layers - Core, radiative zone, convective zone, photosphere, chromosphere, corona",
            "SUN: Nuclear Fusion - Hydrogen to Helium, 4 million tons/second, E=mc squared",
            "SUN: Solar Wind - Charged particles, 400 km/s, auroras, heliosphere",
            "MERCURY: Planet 1 - Closest to sun, 88 day orbit, extreme temps, no atmosphere",
            "VENUS: Planet 2 - Hottest planet, thick CO2 atmosphere, runaway greenhouse, retrograde rotation",
            "EARTH: Planet 3 - Only known life, 71% water, nitrogen-oxygen atmosphere, magnetic field",
            "EARTH: Moon - Natural satellite, 27.3 day orbit, tides, synchronous rotation",
            "MARS: Planet 4 - Red planet, iron oxide, polar ice caps, largest volcano (Olympus Mons)",
            "MARS: Moons - Phobos (fear), Deimos (terror), captured asteroids",
            "ASTEROID BELT - Between Mars/Jupiter, Ceres (dwarf planet), rocky debris",
            "JUPITER: Planet 5 - Largest, gas giant, Great Red Spot, 79+ moons, protects inner planets",
            "JUPITER: Moons - Io (volcanic), Europa (ice), Ganymede (largest), Callisto",
            "SATURN: Planet 6 - Ringed planet, gas giant, 82+ moons, less dense than water",
            "SATURN: Rings - Ice/rock particles, main rings A-B-C, shepherd moons",
            "SATURN: Titan - Largest moon, thick atmosphere, lakes of methane",
            "URANUS: Planet 7 - Ice giant, tilted 98 degrees, methane gives blue color",
            "URANUS: Moons - Miranda, Ariel, Umbriel, Titania, Oberon",
            "NEPTUNE: Planet 8 - Ice giant, winds 2100 km/h, dark blue, Triton moon",
            "NEPTUNE: Triton - Retrograde orbit, geysers, captured Kuiper Belt object",
            "PLUTO: Dwarf Planet - Kuiper Belt, demoted 2006, heart-shaped plain (Tombaugh Regio)",
            "DWARF PLANETS - Ceres (asteroid belt), Pluto, Eris, Haumea, Makemake",
            "KUIPER BELT - Beyond Neptune, Pluto, comets, icy bodies, 30-55 AU",
            "OORT CLOUD - Distant shell, 2,000-100,000 AU, long-period comets",
            "COMET - Icy body, tail near sun, nucleus, coma, ion tail, dust tail",
            "METEOROID - Space rock, meteor (burning), meteorite (ground), shooting star",
            "ASTEROID - Rocky body, Ceres largest, Near-Earth objects, impact risk",
            "SOLAR SYSTEM: Formation - 4.6 BYA, solar nebula, accretion disk, planetesimals",
        ]
        
        for item in solar:
            self.feed_item(item, "astronomy_solar_system", 0.82)
        
        print(f"  ✅ Solar System: {len(solar)} objects")
        return len(solar)
    
    def feed_stars(self):
        """Stars and stellar evolution"""
        print("\n[STARS] Teaching stellar astronomy...")
        
        stars = [
            "STAR: Formation - Nebula collapse, protostar, fusion ignition, main sequence",
            "STAR: Classification - OBAFGKM, hottest to coolest, blue to red, mass determines fate",
            "STAR TYPE: O - Blue, 40,000K, massive, short life, supernova",
            "STAR TYPE: B - Blue-white, 20,000K, Rigel, Spica",
            "STAR TYPE: A - White, 8,500K, Sirius, Vega",
            "STAR TYPE: F - Yellow-white, 6,500K, Canopus, Polaris",
            "STAR TYPE: G - Yellow, 5,800K, Sun, Alpha Centauri A",
            "STAR TYPE: K - Orange, 4,000K, Arcturus, Aldebaran",
            "STAR TYPE: M - Red, 3,000K, most common, Proxima Centauri",
            "STAR: Main Sequence - 90% of stars, hydrogen fusion, stability",
            "STAR: Red Giant - Expanded, cooled, helium burning, future Sun",
            "STAR: White Dwarf - Dead star, Earth-sized, hot, carbon/oxygen core",
            "STAR: Supernova - Exploding star, heavy elements, neutron star/black hole",
            "STAR: Neutron Star - Superdense, 1.4x Sun mass, 20km diameter, pulsars",
            "STAR: Black Hole - Infinite density, event horizon, singularity, spacetime",
            "STAR: Binary System - Two stars orbiting, 50% of stars",
            "STAR: Hertzsprung-Russell Diagram - Temperature vs luminosity, life cycle",
            "STAR: Lifecycle - Protostar to Main Sequence to Red Giant to White Dwarf (Sun-like)",
            "STAR: Massive Lifecycle - O star to Red Supergiant to Supernova to Neutron/Black Hole",
            "STAR: Constellations - Patterns, 88 official, zodiac, seasonal changes",
        ]
        
        for item in stars:
            self.feed_item(item, "astronomy_stars", 0.8)
        
        print(f"  ✅ Stars: {len(stars)} concepts")
        return len(stars)
    
    def feed_galaxies(self):
        """Galaxies"""
        print("\n[GALAXIES] Teaching galaxy types...")
        
        galaxies = [
            "GALAXY: Definition - Gravitationally bound system, billions stars, gas, dust, dark matter",
            "GALAXY: Types - Spiral, Elliptical, Irregular, Interacting",
            "GALAXY TYPE: Spiral - Flat disk, spiral arms, central bulge, young stars in arms",
            "GALAXY TYPE: Elliptical - Round/oval, old stars, little gas, M87",
            "GALAXY TYPE: Irregular - No shape, disrupted, Magellanic Clouds, starburst",
            "GALAXY TYPE: Lenticular - Disk but no arms, intermediate, S0",
            "MILKY WAY: Our Galaxy - Spiral, 100-400 billion stars, 100,000 ly diameter, Sagittarius A*",
            "MILKY WAY: Structure - Central bulge, disk, spiral arms (Orion Arm), halo",
            "MILKY WAY: Bar - Central bar structure, feeds black hole",
            "ANDROMEDA: M31 - Nearest major galaxy, 2.5 million ly, spiral, collision course",
            "TRIANGULUM: M33 - Third largest Local Group galaxy, 3 million ly",
            "MAGELLANIC CLOUDS - Irregular satellites of Milky Way, visible Southern Hemisphere",
            "GALAXY CLUSTER - Groups of galaxies, Virgo Cluster, Coma Cluster",
            "SUPERCLUSTER - Clusters of clusters, Laniakea (our home), Sloan Great Wall",
            "LOCAL GROUP - Milky Way, Andromeda, Triangulum, 54+ galaxies, 10 million ly",
            "LOCAL SHEET - Flattened arrangement, Local Group plus others",
            "VOIDS - Empty space between superclusters, Bootes Void",
            "GALAXY: Active Galactic Nucleus - Supermassive black hole accreting, quasar",
            "GALAXY: Quasar - Extremely bright distant galaxy, early universe",
            "GALAXY: Blazar - Jet pointed at Earth, variable brightness",
            "GALAXY: Seyfert - Active nucleus, visible host galaxy",
            "GALAXY: Collision - Merging galaxies, tidal tails, starburst, eventual union",
            "GALAXY: Formation - Dark matter halos, gas cooling, mergers, hierarchical",
            "DARK MATTER - Invisible mass, 27% universe, holds galaxies together, WIMPs",
            "DARK ENERGY - Accelerating expansion, 68% universe, cosmological constant",
        ]
        
        for item in galaxies:
            self.feed_item(item, "astronomy_galaxies", 0.82)
        
        print(f"  ✅ Galaxies: {len(galaxies)} concepts")
        return len(galaxies)
    
    def feed_cosmos(self):
        """Cosmology and universe"""
        print("\n[COSMOS] Teaching cosmology...")
        
        cosmos = [
            "COSMOLOGY: Big Bang - 13.8 BYA, singularity, expansion, cooling, matter formation",
            "COSMOLOGY: Inflation - 10^-36 seconds, exponential expansion, universe flat",
            "COSMOLOGY: Timeline - Planck Era to Inflation to Particles to Atoms to Stars to Galaxies",
            "COSMOLOGY: Cosmic Microwave Background - 380,000 years old, radiation remnant, WMAP",
            "COSMOLOGY: Nucleosynthesis - First 3 minutes, H, He, Li formed",
            "COSMOLOGY: Recombination - Electrons join nuclei, universe transparent, CMB released",
            "COSMOLOGY: Structure Formation - Density fluctuations, dark matter, galaxies form",
            "COSMOLOGY: Accelerating Expansion - 1998 discovery, dark energy dominates",
            "COSMOLOGY: Fate - Heat Death, Big Freeze, Big Rip, Big Crunch (unlikely)",
            "UNIVERSE: Observable - 93 billion ly diameter, 2 trillion galaxies, limits of light",
            "UNIVERSE: Age - 13.8 billion years, measured by CMB, globular clusters, expansion",
            "UNIVERSE: Composition - 68% dark energy, 27% dark matter, 5% normal matter",
            "UNIVERSE: Fundamental Forces - Gravity, Electromagnetic, Strong, Weak nuclear",
            "UNIVERSE: Standard Model - Particles, quarks, leptons, bosons, Higgs",
            "UNIVERSE: General Relativity - Einstein, gravity = spacetime curvature",
            "UNIVERSE: Quantum Mechanics - Small scales, uncertainty, wave-particle duality",
            "UNIVERSE: String Theory - Extra dimensions, vibrating strings, unification",
            "UNIVERSE: Multiverse - Many universes, bubble universes, eternal inflation",
            "EXOPLANET: Discovery - 1995 first, 5000+ confirmed, transit method, radial velocity",
            "EXOPLANET: Habitable Zone - Goldilocks zone, liquid water, Earth-like",
            "EXOPLANET: Types - Hot Jupiters, Super-Earths, Water worlds, Rogue planets",
            "LIFE: Astrobiology - Study life in universe, extremophiles, biosignatures",
            "LIFE: SETI - Search for Extraterrestrial Intelligence, radio signals, Drake Equation",
            "LIFE: Fermi Paradox - Where is everybody? Great Filter, rare Earth",
        ]
        
        for item in cosmos:
            self.feed_item(item, "astronomy_cosmology", 0.85)
        
        print(f"  ✅ Cosmology: {len(cosmos)} concepts")
        return len(cosmos)
    
    def feed_complete(self):
        print("\n" + "=" * 70)
        print("  🌌 ASTRONOMY COURSE - COMPLETE")
        print("=" * 70)
        
        start = time.time()
        total = 0
        
        total += self.feed_solar_system()
        total += self.feed_stars()
        total += self.feed_galaxies()
        total += self.feed_cosmos()
        
        self.brain.save_state()
        
        elapsed = time.time() - start
        
        print("\n" + "=" * 70)
        print("  ✅ ASTRONOMY COURSE COMPLETE")
        print("=" * 70)
        print(f"  Total Items Fed: {total}")
        print(f"  Brain Ticks: {self.brain.tick_count}")
        print(f"  Brain Memories: {self.brain.hippocampus.total_traces}")
        print(f"  Time: {elapsed:.1f}s")
        print("=" * 70)
        print("\n  The AI now understands:")
        print("    ☀️ Solar System - 8 planets, Sun, moons, asteroids, comets")
        print("    ⭐ Stars - Classification, lifecycle, OBAFGKM, supernovas")
        print("    🌌 Galaxies - Types, Milky Way, Andromeda, clusters, dark matter")
        print("    🌠 Cosmology - Big Bang, 13.8 BY, expansion, fate of universe")
        print("=" * 70)

if __name__ == "__main__":
    feeder = AstronomyCourseFeeder()
    feeder.feed_complete()
