#!/usr/bin/env python3
"""
Time Units - Seconds to Millennium
"""

import sys
sys.path.insert(0, '/root/.aos/aos')

from stomach_v2 import InformationStomach
from intestine_v2 import InformationIntestine
from superior_heart import SuperiorHeart
from brain_v31 import AOSBrainV31
from ternary_interfaces import DigestionInput, IntestineInput, HeartBeatInput, BrainInput

class TimeUnitsFeeder:
    def __init__(self):
        self.stomach = InformationStomach(capacity=100)
        self.intestine = InformationIntestine()
        self.heart = SuperiorHeart()
        self.brain = AOSBrainV31()
        self.total_fed = 0
        print("=" * 70)
        print("  ⏰ TIME UNITS - Seconds to Millennium")
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
    
    def feed_time_units(self):
        """Feed time measurement hierarchy"""
        print("\n[TIME UNITS] Teaching time measurement...")
        
        time_units = [
            "TIME: Second - Base unit of time, 1/60 of a minute, SI unit, atomic clock definition",
            "TIME: Minute - 60 seconds, 1/60 of an hour, time measurement",
            "TIME: Hour - 60 minutes, 3,600 seconds, 1/24 of a day",
            "TIME: Day - 24 hours, 86,400 seconds, Earth's rotation period",
            "TIME: Week - 7 days, 168 hours, cultural calendar unit",
            "TIME: Month - Calendar month, 28-31 days, lunar cycle approximation",
            "TIME: Year - 365 days (common), 366 days (leap), Earth's orbit around Sun",
            "TIME: Decade - 10 years, 3,650+ days, cultural measurement",
            "TIME: Century - 100 years, 10 decades, historical era",
            "TIME: Millennium - 1,000 years, 10 centuries, plural millennia",
            "TIME CONVERSION: Seconds in Minute = 60",
            "TIME CONVERSION: Minutes in Hour = 60",
            "TIME CONVERSION: Hours in Day = 24",
            "TIME CONVERSION: Days in Year = 365 (common year)",
            "TIME CONVERSION: Years in Decade = 10",
            "TIME CONVERSION: Decades in Century = 10",
            "TIME CONVERSION: Centuries in Millennium = 10",
            "TIME: Leap Year - 366 days, every 4 years (mostly), February 29th",
            "TIME: Gregorian Calendar - 1582, Pope Gregory XIII, solar calendar",
            "TIME: UTC - Coordinated Universal Time, atomic time standard",
            "TIME: Time Zone - 24 zones, roughly 15 degrees longitude each",
            "TIME: Epoch - Unix time, seconds since Jan 1 1970",
        ]
        
        for item in time_units:
            self.feed_item(item, "mathematics_time_units", 0.85)
        
        print(f"  ✅ Time Units: {len(time_units)} measurements")
        return len(time_units)
    
    def feed_complete(self):
        print("\n" + "=" * 70)
        print("  ⏰ TIME UNITS FEED COMPLETE")
        print("=" * 70)
        
        import time as tm
        start = tm.time()
        total = 0
        
        total += self.feed_time_units()
        
        self.brain.save_state()
        
        elapsed = tm.time() - start
        
        print("\n" + "=" * 70)
        print("  ⏰ TIME HIERARCHY")
        print("=" * 70)
        print("    60 Seconds = 1 Minute")
        print("    60 Minutes = 1 Hour")
        print("    24 Hours = 1 Day")
        print("    365 Days = 1 Year")
        print("    10 Years = 1 Decade")
        print("    10 Decades = 1 Century")
        print("    10 Centuries = 1 Millennium")
        print("=" * 70)
        print(f"\n  Total: {total} time concepts")
        print(f"  Brain Ticks: {self.brain.tick_count}")
        print(f"  Time: {elapsed:.1f}s")
        print("=" * 70)

if __name__ == "__main__":
    feeder = TimeUnitsFeeder()
    feeder.feed_complete()
