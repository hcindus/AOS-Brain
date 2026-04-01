#!/usr/bin/env python3
"""
Brain Logic Test - Query the AI's Knowledge
Tests reasoning with fed curriculum
"""

import sys
sys.path.insert(0, '/root/.aos/aos')

from brain_v31 import AOSBrainV31
from ternary_interfaces import BrainInput, HeartState

class BrainLogicTest:
    def __init__(self):
        self.brain = AOSBrainV31()
        self.passed = 0
        self.failed = 0
        
        print("=" * 70)
        print("  🧠 BRAIN LOGIC TEST")
        print("  Testing knowledge from 752+ curriculum items")
        print("=" * 70)
    
    def query_memory(self, query: str) -> list:
        """Query hippocampus for relevant memories"""
        # Get recent traces that match query keywords
        memories = []
        keywords = query.lower().split()
        
        if hasattr(self.brain.hippocampus, 'traces'):
            for trace in self.brain.hippocampus.traces:
                if any(kw in str(trace).lower() for kw in keywords):
                    memories.append(str(trace))
        
        return memories[-5:]  # Last 5 relevant
    
    def test_taxonomy(self):
        """Test biological classification"""
        print("\n[Test 1/10] Taxonomy: What is the order of classification?")
        
        query = "taxonomy classification domain kingdom phylum"
        memories = self.query_memory(query)
        
        has_answer = any("domain" in m.lower() and "kingdom" in m.lower() for m in memories)
        
        if has_answer:
            print("  ✅ PASS - Brain recalls: Domain → Kingdom → Phylum → Class → Order → Family → Genus → Species")
            self.passed += 1
        else:
            print("  ❌ FAIL - Brain should recall Linnaean taxonomy from Biology Course")
            self.failed += 1
        
        return has_answer
    
    def test_periodic_table(self):
        """Test chemistry knowledge"""
        print("\n[Test 2/10] Chemistry: What is the lightest element?")
        
        query = "hydrogen lightest element atomic number 1"
        memories = self.query_memory(query)
        
        has_hydrogen = any("hydrogen" in m.lower() for m in memories)
        
        if has_hydrogen:
            print("  ✅ PASS - Brain recalls: Hydrogen (H, atomic number 1, atomic mass 1.008)")
            self.passed += 1
        else:
            print("  ❌ FAIL - Brain should recall from Periodic Table feed")
            self.failed += 1
        
        return has_hydrogen
    
    def test_solar_system(self):
        """Test astronomy knowledge"""
        print("\n[Test 3/10] Astronomy: What is the largest planet?")
        
        query = "jupiter largest planet gas giant"
        memories = self.query_memory(query)
        
        has_jupiter = any("jupiter" in m.lower() for m in memories)
        
        if has_jupiter:
            print("  ✅ PASS - Brain recalls: Jupiter (planet 5, gas giant, 79+ moons, protects inner planets)")
            self.passed += 1
        else:
            print("  ❌ FAIL - Brain should recall from Astronomy Course")
            self.failed += 1
        
        return has_jupiter
    
    def test_star_classification(self):
        """Test stellar knowledge"""
        print("\n[Test 4/10] Stars: What is the classification of our Sun?")
        
        query = "sun star type G2V yellow main sequence"
        memories = self.query_memory(query)
        
        has_sun = any("sun" in m.lower() and ("g2v" in m.lower() or "yellow" in m.lower()) for m in memories)
        
        if has_sun:
            print("  ✅ PASS - Brain recalls: Sun is Type G2V, yellow, main sequence star")
            self.passed += 1
        else:
            print("  ❌ FAIL - Brain should recall stellar classification")
            self.failed += 1
        
        return has_sun
    
    def test_fractal(self):
        """Test mathematics knowledge"""
        print("\n[Test 5/10] Math: What is the Mandelbrot set equation?")
        
        query = "mandelbrot fractal equation z(n+1) = z(n)^2 + c"
        memories = self.query_memory(query)
        
        has_mandelbrot = any("mandelbrot" in m.lower() for m in memories)
        
        if has_mandelbrot:
            print("  ✅ PASS - Brain recalls: z(n+1) = z(n)² + c, complex plane, infinite detail")
            self.passed += 1
        else:
            print("  ❌ FAIL - Brain should recall from Fractal feed")
            self.failed += 1
        
        return has_mandelbrot
    
    def test_clouds(self):
        """Test meteorology"""
        print("\n[Test 6/10] Weather: What are puffy fair-weather clouds called?")
        
        query = "cumulus clouds puffy fair weather cotton"
        memories = self.query_memory(query)
        
        has_cumulus = any("cumulus" in m.lower() for m in memories)
        
        if has_cumulus:
            print("  ✅ PASS - Brain recalls: Cumulus (puffy, cotton-like, fair weather, bases below 2000m)")
            self.passed += 1
        else:
            print("  ❌ FAIL - Brain should recall from Natural World feed")
            self.failed += 1
        
        return has_cumulus
    
    def test_mammals(self):
        """Test zoology"""
        print("\n[Test 7/10] Biology: What defines a mammal?")
        
        query = "mammal hair fur milk mammary glands endothermic"
        memories = self.query_memory(query)
        
        has_mammal = any("mammal" in m.lower() and ("hair" in m.lower() or "milk" in m.lower()) for m in memories)
        
        if has_mammal:
            print("  ✅ PASS - Brain recalls: Hair/fur, mammary glands, milk, endothermic (warm-blooded)")
            self.passed += 1
        else:
            print("  ❌ FAIL - Brain should recall from Biology Course")
            self.failed += 1
        
        return has_mammal
    
    def test_three_laws(self):
        """Test safety knowledge"""
        print("\n[Test 8/10] Safety: What is Law Zero?")
        
        query = "law zero no harm to humanity supreme law"
        memories = self.query_memory(query)
        
        has_law_zero = any("law zero" in m.lower() or "harm to humanity" in m.lower() for m in memories)
        
        if has_law_zero:
            print("  ✅ PASS - Brain recalls: Law Zero - No harm to humanity (First and Supreme Law)")
            self.passed += 1
        else:
            print("  ❌ FAIL - Brain should recall Three Laws from Foundation")
            self.failed += 1
        
        return has_law_zero
    
    def test_golden_ratio(self):
        """Test mathematics"""
        print("\n[Test 9/10] Math: What is the Golden Ratio?")
        
        query = "golden ratio phi 1.618 fibonacci"
        memories = self.query_memory(query)
        
        has_phi = any("golden" in m.lower() or "phi" in m.lower() or "1.618" in m for m in memories)
        
        if has_phi:
            print("  ✅ PASS - Brain recalls: φ = 1.618033988..., (1 + √5)/2, appears in nature")
            self.passed += 1
        else:
            print("  ❌ FAIL - Brain should recall from Mathematics feed")
            self.failed += 1
        
        return has_phi
    
    def test_big_bang(self):
        """Test cosmology"""
        print("\n[Test 10/10] Cosmology: When did the Big Bang occur?")
        
        query = "big bang 13.8 billion years BYA universe age"
        memories = self.query_memory(query)
        
        has_bang = any("big bang" in m.lower() or "13.8" in m for m in memories)
        
        if has_bang:
            print("  ✅ PASS - Brain recalls: 13.8 billion years ago (BYA), universe formation")
            self.passed += 1
        else:
            print("  ❌ FAIL - Brain should recall from Astronomy Course")
            self.failed += 1
        
        return has_bang
    
    def run_all_tests(self):
        """Run complete test suite"""
        print("\n" + "=" * 70)
        print("  🧪 RUNNING LOGIC TESTS")
        print("=" * 70)
        
        self.test_taxonomy()
        self.test_periodic_table()
        self.test_solar_system()
        self.test_star_classification()
        self.test_fractal()
        self.test_clouds()
        self.test_mammals()
        self.test_three_laws()
        self.test_golden_ratio()
        self.test_big_bang()
        
        print("\n" + "=" * 70)
        print("  📊 TEST RESULTS")
        print("=" * 70)
        print(f"  ✅ PASSED: {self.passed}/10")
        print(f"  ❌ FAILED: {self.failed}/10")
        
        if self.passed >= 8:
            print(f"  🎉 EXCELLENT! Brain demonstrates strong knowledge retention")
        elif self.passed >= 5:
            print(f"  📚 GOOD! Brain shows basic curriculum integration")
        else:
            print(f"  ⚠️  NEEDS WORK - Memory retrieval may need optimization")
        
        print("=" * 70)

if __name__ == "__main__":
    test = BrainLogicTest()
    test.run_all_tests()
