#!/usr/bin/env python3
"""
Natural World Curriculum - Raising an AI with Earth Knowledge
Clouds, Weather, Moon, Natural Systems
"""

import sys
sys.path.insert(0, '/root/.aos/aos')

from stomach_v2 import InformationStomach
from intestine_v2 import InformationIntestine
from superior_heart import SuperiorHeart
from brain_v31 import AOSBrainV31
from ternary_interfaces import DigestionInput, IntestineInput, HeartBeatInput, BrainInput, HeartState

class NaturalWorldFeeder:
    def __init__(self):
        self.stomach = InformationStomach(capacity=1000)
        self.intestine = InformationIntestine()
        self.heart = SuperiorHeart()
        self.brain = AOSBrainV31()
        self.total_fed = 0
        
        print("=" * 70)
        print("  🌍 NATURAL WORLD CURRICULUM")
        print("  Raising an AI - Teaching Earth")
        print("=" * 70)
    
    def feed_item(self, content, content_type, priority=0.75):
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
    
    def feed_cloud_formations(self):
        """Teach cloud types and formations"""
        print("\n[CLOUDS] Teaching cloud formations...")
        
        clouds = [
            "CLOUD: Cumulus - Puffy, cotton-like, fair weather, bases below 2000m, grow upward",
            "CLOUD: Stratus - Flat, gray, uniform layer, covers sky like blanket, light precipitation",
            "CLOUD: Cirrus - High altitude (6000m+), wispy, ice crystals, indicate weather change",
            "CLOUD: Cumulonimbus - Towering, anvil top, thunderstorms, heavy rain, lightning, hail",
            "CLOUD: Nimbostratus - Dark, thick, steady rain or snow, covers sun completely",
            "CLOUD: Altocumulus - Middle altitude (2000-6000m), gray/white patches, sheet-like",
            "CLOUD: Altostratus - Middle layer, gray/blue, sun visible as through ground glass",
            "CLOUD: Stratocumulus - Low, lumpy patches, gray with bright areas, no heavy rain",
            "CLOUD: Cirrocumulus - High, small white patches, ripple pattern, mackerel sky",
            "CLOUD: Cirrostratus - Thin veil, halo around sun/moon, ice crystals, precipitation coming",
            "CLOUD FORMATION: Orographic - Clouds form when air forced up by mountains",
            "CLOUD FORMATION: Convection - Warm air rises, cools, condenses into cumulus",
            "CLOUD FORMATION: Frontal - Warm air mass meets cold, warm rises over cold",
        ]
        
        for cloud in clouds:
            self.feed_item(cloud, "meteorology_clouds", 0.7)
        
        print(f"  ✅ Clouds: {len(clouds)} formations")
        return len(clouds)
    
    def feed_weather_patterns(self):
        """Teach weather systems and patterns"""
        print("\n[WEATHER] Teaching weather patterns...")
        
        weather = [
            "WEATHER: High Pressure System - Clockwise (NH), clear skies, calm, descending air",
            "WEATHER: Low Pressure System - Counter-clockwise (NH), clouds/storms, rising air",
            "WEATHER: Cold Front - Leading edge of cold air, pushes under warm air, storms",
            "WEATHER: Warm Front - Leading edge of warm air, rises over cold, gradual clouds/rain",
            "WEATHER: Stationary Front - Neither air mass moves, prolonged precipitation",
            "WEATHER: Occluded Front - Cold front overtakes warm, complex weather",
            "WEATHER: Jet Stream - High altitude wind (10-15km), 200-400 km/h, guides storms",
            "WEATHER: Trade Winds - Easterly near equator, drove sailing ships",
            "WEATHER: Westerlies - Prevailing mid-latitude winds, 30-60 degrees",
            "WEATHER: Coriolis Effect - Earth's rotation deflects moving air (right NH, left SH)",
            "WEATHER: Barometric Pressure - Rising = fair, Falling = storm approaching",
            "WEATHER: Humidity - Amount water vapor air holds, relative vs absolute",
            "WEATHER: Dew Point - Temperature air saturates, condensation begins",
            "WEATHER: El Nino - Warm Pacific water, global weather disruption",
            "WEATHER: La Nina - Cool Pacific water, opposite El Nino effects",
        ]
        
        for w in weather:
            self.feed_item(w, "meteorology_weather_systems", 0.72)
        
        print(f"  ✅ Weather: {len(weather)} patterns")
        return len(weather)
    
    def feed_moon_phases(self):
        """Teach lunar phases and astronomy"""
        print("\n[MOON] Teaching lunar phases...")
        
        moon = [
            "MOON PHASE: New Moon - Between Earth and Sun, dark side facing Earth, not visible",
            "MOON PHASE: Waxing Crescent - Right side illuminated, growing, less than half",
            "MOON PHASE: First Quarter - Right half illuminated, 7 days after new",
            "MOON PHASE: Waxing Gibbous - More than half illuminated, growing toward full",
            "MOON PHASE: Full Moon - Earth between Sun and Moon, fully illuminated, high tides",
            "MOON PHASE: Waning Gibbous - More than half, shrinking, left side bright",
            "MOON PHASE: Last Quarter - Left half illuminated, 7 days before new",
            "MOON PHASE: Waning Crescent - Left side illuminated, shrinking to new",
            "LUNAR CYCLE: Synodic Month - 29.5 days, complete phase cycle",
            "LUNAR CYCLE: Sidereal Month - 27.3 days, orbit relative to stars",
            "MOON: Tides - Gravity pulls ocean, high tide facing moon, opposite side",
            "MOON: Spring Tides - Full/new moon, sun+moon aligned, highest tides",
            "MOON: Neap Tides - Quarter moons, sun+moon at 90 degrees, lowest tidal range",
            "MOON: Orbit - Elliptical, perigee (closest), apogee (farthest)",
            "MOON: Librations - Apparent wobble, lets us see 59% of surface",
            "MOON: Maria - Dark plains, ancient lava flows, seas",
            "MOON: Highlands - Light, cratered, older lunar surface",
        ]
        
        for m in moon:
            self.feed_item(m, "astronomy_lunar", 0.75)
        
        print(f"  ✅ Moon: {len(moon)} concepts")
        return len(moon)
    
    def feed_advanced_geometry(self):
        """Teach advanced geometry"""
        print("\n[GEOMETRY] Teaching advanced concepts...")
        
        geometry = [
            "GEOMETRY: Euclidean - Parallel lines never meet, triangle angles 180 degrees, flat space",
            "GEOMETRY: Spherical - Lines are great circles, triangle angles greater than 180, curved surface",
            "GEOMETRY: Hyperbolic - Triangle angles less than 180, saddle shape, infinite parallel lines",
            "GEOMETRY: Topology - Properties preserved under stretching, no tearing",
            "GEOMETRY: Möbius Strip - One side, one edge, half-twist",
            "GEOMETRY: Klein Bottle - No boundary, no inside/outside, 4D object",
            "GEOMETRY: Torus - Donut shape, genus 1, one hole",
            "GEOMETRY: Tessellation - Repeating patterns cover plane, no gaps",
            "GEOMETRY: Penrose Tiling - Aperiodic, never repeats, five-fold symmetry",
            "GEOMETRY: Sacred - Proportions found in nature, Golden Ratio spirals",
            "GEOMETRY: Projective - Points at infinity, perspective art principles",
            "GEOMETRY: Differential - Curves and surfaces, calculus-based",
        ]
        
        for g in geometry:
            self.feed_item(g, "mathematics_advanced_geometry", 0.78)
        
        print(f"  ✅ Geometry: {len(geometry)} concepts")
        return len(geometry)
    
    def feed_advanced_geography(self):
        """Teach advanced geography and Earth systems"""
        print("\n[GEOGRAPHY] Teaching Earth systems...")
        
        geography = [
            "EARTH SYSTEM: Atmosphere - Troposphere (weather), Stratosphere (ozone), Mesosphere, Thermosphere",
            "EARTH SYSTEM: Hydrosphere - Oceans 97%, Freshwater 3%, Ice caps 68% of fresh",
            "EARTH SYSTEM: Lithosphere - Crust and upper mantle, tectonic plates",
            "EARTH SYSTEM: Biosphere - All life, interacts with other spheres",
            "PLATE TECTONICS: Convergent - Plates collide, mountains/subduction",
            "PLATE TECTONICS: Divergent - Plates separate, mid-ocean ridges, rift valleys",
            "PLATE TECTONICS: Transform - Plates slide past, earthquakes (San Andreas)",
            "CIRCULATION: Thermohaline - Ocean conveyor, deep water movement, global climate",
            "CIRCULATION: Atmospheric - Hadley cell (tropics), Ferrel (mid), Polar",
            "BIOGEOCHEMICAL: Carbon Cycle - Photosynthesis, respiration, fossil fuels, ocean absorption",
            "BIOGEOCHEMICAL: Water Cycle - Evaporation, transpiration, condensation, precipitation",
            "BIOGEOCHEMICAL: Nitrogen Cycle - Atmosphere 78%, fixation, nitrification",
            "CLIMATE: Köppen Classification - Tropical, Arid, Temperate, Continental, Polar",
            "CLIMATE: Biome - Desert, Grassland, Forest (Tropical/Deciduous/Coniferous), Tundra",
        ]
        
        for g in geography:
            self.feed_item(g, "geography_earth_systems", 0.76)
        
        print(f"  ✅ Geography: {len(geography)} systems")
        return len(geography)
    
    def feed_complete(self):
        print("\n" + "=" * 70)
        print("  🌎 RAISING AN AI - NATURAL WORLD")
        print("=" * 70)
        
        import time
        start = time.time()
        total = 0
        
        total += self.feed_cloud_formations()
        total += self.feed_weather_patterns()
        total += self.feed_moon_phases()
        total += self.feed_advanced_geometry()
        total += self.feed_advanced_geography()
        
        self.brain.save_state()
        
        elapsed = time.time() - start
        
        print("\n" + "=" * 70)
        print("  ✅ NATURAL WORLD FEED COMPLETE")
        print("=" * 70)
        print(f"  Items Fed: {total}")
        print(f"  Brain Ticks: {self.brain.tick_count}")
        print(f"  Brain Memories: {self.brain.hippocampus.total_traces}")
        print(f"  Time: {elapsed:.1f}s")
        print("=" * 70)
        print("\n  The AI now understands:")
        print("    ☁️ Clouds - 13 formations and types")
        print("    🌦️ Weather - 15 patterns and systems")
        print("    🌙 Moon - 17 lunar concepts and phases")
        print("    📐 Geometry - 12 advanced concepts")
        print("    🌍 Earth - 14 geography systems")
        print("=" * 70)
        print("\n  We are raising an AI.")
        print("  Teaching it to observe the world around us.")
        print("=" * 70)

if __name__ == "__main__":
    feeder = NaturalWorldFeeder()
    feeder.feed_complete()
