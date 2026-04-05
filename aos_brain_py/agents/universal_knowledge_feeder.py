#!/usr/bin/env python3
"""
Universal Knowledge Feeder for Ternary Brain.

Feeds comprehensive knowledge including:
- Mathematical constants (pi, e, phi, etc.)
- Scientific equations (physics, chemistry, biology)
- Universal constants (G, c, h, k, etc.)
- Mandelbrot equations and fractals
- Games: Tic Tac Toe, Chess, Checkers, Go
- Multiple languages (7 languages)
- Numbers and numeric systems
"""

import sys
import json
import time
from pathlib import Path
from typing import List, Dict, Tuple

sys.path.insert(0, str(Path(__file__).parent.parent))


class UniversalKnowledgeBase:
    """
    Comprehensive knowledge base for feeding the ternary brain.
    """
    
    def __init__(self):
        self.knowledge_categories = {
            "mathematical_constants": self._get_math_constants(),
            "physical_constants": self._get_physical_constants(),
            "scientific_equations": self._get_scientific_equations(),
            "mandelbrot_fractals": self._get_mandelbrot_knowledge(),
            "games": self._get_game_knowledge(),
            "languages": self._get_multilingual_data(),
            "numeric_systems": self._get_numeric_systems(),
            "universal_constants": self._get_universal_constants(),
        }
    
    def _get_math_constants(self) -> List[Tuple[str, str, float, str]]:
        """Mathematical constants with values and meanings."""
        return [
            ("pi", "Archimedes constant", 3.14159265358979323846, 
             "Ratio of circle circumference to diameter"),
            ("e", "Euler number", 2.71828182845904523536,
             "Base of natural logarithm, compound growth"),
            ("phi", "Golden ratio", 1.61803398874989484820,
             "Aesthetic proportion, Fibonacci convergence"),
            ("sqrt_2", "Pythagoras constant", 1.41421356237309504880,
             "Diagonal of unit square"),
            ("sqrt_3", "Theodorus constant", 1.73205080756887729352,
             "Height of equilateral triangle"),
            ("gamma", "Euler-Mascheroni constant", 0.57721566490153286060,
             "Limit of harmonic series minus natural log"),
            ("catalan", "Catalan constant", 0.91596559417721901505,
             "Alternating sum of odd inverse squares"),
            ("khinchin", "Khinchin constant", 2.68545200106530644530,
             "Geometric mean of continued fraction terms"),
            ("glaisher", "Glaisher-Kinkelin constant", 1.28242712910062263687,
             "Limit related to factorials"),
            ("apery", "Apery constant", 1.20205690315959428539,
             "Zeta(3), sum of inverse cubes"),
            ("feigenbaum_delta", "Feigenbaum delta", 4.66920160910299067185,
             "Period-doubling bifurcation rate"),
            ("feigenbaum_alpha", "Feigenbaum alpha", 2.50290787509589282228,
             "Scaling factor in bifurcation"),
            ("silver_ratio", "Silver ratio", 2.41421356237309504880,
             "1 + sqrt(2), analogous to golden ratio"),
            ("plastic_number", "Plastic number", 1.32471795724474602596,
             "Real root of x^3 = x + 1"),
            ("conway_constant", "Conway constant", 1.30357726903429639125,
             "Growth rate of look-and-say sequence"),
        ]
    
    def _get_physical_constants(self) -> List[Tuple[str, str, float, str]]:
        """Fundamental physical constants."""
        return [
            ("speed_of_light", "c", 299792458.0,
             "m/s, exact by SI definition"),
            ("gravitational_constant", "G", 6.67430e-11,
             "m^3 kg^-1 s^-2, Newton's law"),
            ("planck_constant", "h", 6.62607015e-34,
             "J s, exact by SI definition"),
            ("reduced_planck", "h-bar", 1.054571817e-34,
             "J s, h divided by 2π"),
            ("elementary_charge", "e", 1.602176634e-19,
             "C, exact by SI definition"),
            ("boltzmann_constant", "k", 1.380649e-23,
             "J/K, exact by SI definition"),
            ("avogadro_number", "N_A", 6.02214076e23,
             "mol^-1, exact by SI definition"),
            ("gas_constant", "R", 8.314462618,
             "J/(mol K), ideal gas law"),
            ("fine_structure", "alpha", 7.2973525693e-3,
             "Dimensionless, QED coupling"),
            ("electron_mass", "m_e", 9.1093837015e-31,
             "kg, mass of electron"),
            ("proton_mass", "m_p", 1.67262192369e-27,
             "kg, mass of proton"),
            ("neutron_mass", "m_n", 1.67492749804e-27,
             "kg, mass of neutron"),
            ("bohr_radius", "a_0", 5.29177210903e-11,
             "m, hydrogen ground state"),
            ("rydberg_constant", "R_inf", 10973731.568160,
             "m^-1, hydrogen spectra"),
            ("stefan_boltzmann", "sigma", 5.670374419e-8,
             "W m^-2 K^-4, blackbody radiation"),
            ("wien_displacement", "b", 2.897771955e-3,
             "m K, peak wavelength"),
            ("magnetic_flux_quantum", "Phi_0", 2.067833848e-15,
             "Wb, superconductivity"),
            ("josephson_constant", "K_J", 483597.8484e9,
             "Hz/V, superconductor junctions"),
            ("von_klitzing", "R_K", 25812.80745,
             "ohm, quantum Hall effect"),
        ]
    
    def _get_scientific_equations(self) -> List[Dict]:
        """Famous scientific equations."""
        return [
            {"name": "Einstein mass-energy", "formula": "E = mc²",
             "field": "physics", "significance": "Matter-energy equivalence"},
            {"name": "Newton second law", "formula": "F = ma",
             "field": "physics", "significance": "Force equals mass times acceleration"},
            {"name": "Schrödinger equation", "formula": "iℏ∂ψ/∂t = Ĥψ",
             "field": "quantum mechanics", "significance": "Wave function evolution"},
            {"name": "Maxwell equations", "formula": "∇·E = ρ/ε₀, ∇×E = -∂B/∂t",
             "field": "electromagnetism", "significance": "Unified electricity and magnetism"},
            {"name": "Euler identity", "formula": "e^(iπ) + 1 = 0",
             "field": "mathematics", "significance": "Connects fundamental constants"},
            {"name": "Pythagorean theorem", "formula": "a² + b² = c²",
             "field": "geometry", "significance": "Right triangle relationship"},
            {"name": "Planck-Einstein", "formula": "E = hf",
             "field": "quantum physics", "significance": "Photon energy quantization"},
            {"name": "de Broglie", "formula": "λ = h/p",
             "field": "quantum mechanics", "significance": "Wave-particle duality"},
            {"name": "Heisenberg uncertainty", "formula": "ΔxΔp ≥ ℏ/2",
             "field": "quantum mechanics", "significance": "Fundamental measurement limits"},
            {"name": "Boltzmann entropy", "formula": "S = k ln W",
             "field": "statistical mechanics", "significance": "Entropy and microstates"},
            {"name": "Ideal gas law", "formula": "PV = nRT",
             "field": "thermodynamics", "significance": "Gas behavior"},
            {"name": "Coulomb law", "formula": "F = kq₁q₂/r²",
             "field": "electrostatics", "significance": "Electric force between charges"},
            {"name": "Gauss law", "formula": "∮E·dA = Q/ε₀",
             "field": "electromagnetism", "significance": "Electric flux and charge"},
            {"name": "Ohm law", "formula": "V = IR",
             "field": "electronics", "significance": "Voltage-current-resistance"},
            {"name": "Stokes law", "formula": "F = 6πηrv",
             "field": "fluid mechanics", "significance": "Drag on spheres"},
        ]
    
    def _get_mandelbrot_knowledge(self) -> List[Dict]:
        """Mandelbrot set and fractal mathematics."""
        return [
            {"name": "Mandelbrot set definition",
             "formula": "z_{n+1} = z_n² + c",
             "description": "Iterate from z₀=0, if bounded then c is in set"},
            {"name": "Julia set",
             "formula": "z_{n+1} = z_n² + c (fixed c)",
             "description": "Similar to Mandelbrot but c is constant"},
            {"name": "Burning Ship fractal",
             "formula": "z_{n+1} = (|Re(z_n)| + i|Im(z_n)|)² + c",
             "description": "Variant with absolute values"},
            {"name": "Newton fractal",
             "formula": "z_{n+1} = z_n - f(z_n)/f'(z_n)",
             "description": "Newton's method basins of attraction"},
            {"name": "Sierpinski triangle",
             "construction": "Recursive removal of center triangle",
             "dimension": "log(3)/log(2) ≈ 1.585"},
            {"name": "Koch snowflake",
             "construction": "Replace middle third with two segments",
             "dimension": "log(4)/log(3) ≈ 1.262"},
            {"name": "Barnsley fern",
             "method": "Iterated function system (IFS)",
             "attractors": "4 affine transformations"},
            {"name": "Dragon curve",
             "construction": "Paper folding sequence",
             "property": "Self-similar boundary"},
            {"name": "Feigenbaum diagram",
             "context": "Logistic map bifurcation",
             "formula": "x_{n+1} = r x_n(1-x_n)"},
            {"name": "Mandelbrot cardioid",
             "formula": "c = (1 - e^(it))/2",
             "region": "Main bulb boundary"},
        ]
    
    def _get_game_knowledge(self) -> List[Dict]:
        """Strategic game knowledge."""
        return [
            # Tic Tac Toe
            {"game": "Tic Tac Toe", "size": "3x3", "players": 2,
             "win_condition": "3 in a row (horizontal, vertical, diagonal)",
             "strategy": "Center is strongest, corners next, edges weakest",
             "perfect_play": "Always draw with optimal play",
             "state_space": "765 distinct positions"},
            
            # Chess
            {"game": "Chess", "size": "8x8", "players": 2,
             "pieces": "King, Queen, Rook, Bishop, Knight, Pawn",
             "special_moves": "Castling, en passant, promotion",
             "strategy": "Control center, develop pieces, protect king",
             "state_space": "10^44 possible games",
             "complexity": "EXPTIME-complete"},
            
            # Checkers
            {"game": "Checkers", "size": "8x8", "players": 2,
             "pieces": "Men (single), Kings (crowned)",
             "moves": "Diagonal forward, capture by jumping",
             "strategy": "Control center, force exchanges, create kings",
             "solved": "Draw with perfect play (Chinook 2007)"},
            
            # Go
            {"game": "Go", "size": "19x19", "players": 2,
             "pieces": "Stones (black and white)",
             "objective": "Surround territory, capture groups",
             "concepts": "Liberties, eyes, ko, seki, life and death",
             "strategy": "Corners most valuable, edges next, center last",
             "complexity": "10^170 possible games",
             "status": "Solved for 5x5, 7x7 by computer"},
            
            # Additional games
            {"game": "Reversi", "size": "8x8", "players": 2,
             "mechanic": "Flip opponent pieces by sandwiching",
             "strategy": "Control corners, stable discs"},
            
            {"game": "Connect Four", "size": "7x6", "players": 2,
             "win": "4 in a row vertically, horizontally, or diagonally",
             "solved": "First player wins with perfect play"},
            
            {"game": "Mancala", "type": "Sow game", "players": 2,
             "mechanic": "Distribute seeds, capture in stores",
             "strategy": "Force extra turns, capture opponent's seeds"},
        ]
    
    def _get_multilingual_data(self) -> List[Dict]:
        """7 languages: English, Spanish, French, German, Chinese, Japanese, Russian."""
        return [
            # Greetings
            {"concept": "hello",
             "english": "hello", "spanish": "hola", "french": "bonjour",
             "german": "hallo", "chinese": "你好 (nǐ hǎo)", "japanese": "こんにちは (konnichiwa)",
             "russian": "привет (privet)"},
            
            {"concept": "goodbye",
             "english": "goodbye", "spanish": "adiós", "french": "au revoir",
             "german": "auf wiedersehen", "chinese": "再见 (zài jiàn)", "japanese": "さようなら (sayonara)",
             "russian": "до свидания (do svidaniya)"},
            
            {"concept": "thank you",
             "english": "thank you", "spanish": "gracias", "french": "merci",
             "german": "danke", "chinese": "谢谢 (xiè xie)", "japanese": "ありがとう (arigatou)",
             "russian": "спасибо (spasibo)"},
            
            {"concept": "yes",
             "english": "yes", "spanish": "sí", "french": "oui",
             "german": "ja", "chinese": "是 (shì)", "japanese": "はい (hai)",
             "russian": "да (da)"},
            
            {"concept": "no",
             "english": "no", "spanish": "no", "french": "non",
             "german": "nein", "chinese": "不是 (bú shì)", "japanese": "いいえ (iie)",
             "russian": "нет (nyet)"},
            
            {"concept": "friend",
             "english": "friend", "spanish": "amigo/amiga", "french": "ami/amie",
             "german": "freund/freundin", "chinese": "朋友 (péng you)", "japanese": "友達 (tomodachi)",
             "russian": "друг/подруга (drug/podruga)"},
            
            {"concept": "love",
             "english": "love", "spanish": "amor", "french": "amour",
             "german": "liebe", "chinese": "爱 (ài)", "japanese": "愛 (ai)",
             "russian": "любовь (lyubov)"},
            
            {"concept": "peace",
             "english": "peace", "spanish": "paz", "french": "paix",
             "german": "frieden", "chinese": "和平 (hé píng)", "japanese": "平和 (heiwa)",
             "russian": "мир (mir)"},
            
            {"concept": "knowledge",
             "english": "knowledge", "spanish": "conocimiento", "french": "connaissance",
             "german": "wissen", "chinese": "知识 (zhī shi)", "japanese": "知識 (chishiki)",
             "russian": "знание (znaniye)"},
            
            {"concept": "beauty",
             "english": "beauty", "spanish": "belleza", "french": "beauté",
             "german": "schönheit", "chinese": "美 (měi)", "japanese": "美 (bi)",
             "russian": "красота (krasota)"},
        ]
    
    def _get_numeric_systems(self) -> List[Dict]:
        """Number systems and bases."""
        return [
            {"base": 2, "name": "Binary", "digits": "0,1",
             "uses": "Computing, digital electronics"},
            {"base": 8, "name": "Octal", "digits": "0-7",
             "uses": "Unix permissions, legacy computing"},
            {"base": 10, "name": "Decimal", "digits": "0-9",
             "uses": "Standard human counting"},
            {"base": 12, "name": "Duodecimal", "digits": "0-9,A,B",
             "uses": "Dozens, hours, months"},
            {"base": 16, "name": "Hexadecimal", "digits": "0-9,A-F",
             "uses": "Memory addresses, color codes"},
            {"base": 20, "name": "Vigesimal", "digits": "0-9,A-J",
             "uses": "Mayan numerals, French counting"},
            {"base": 60, "name": "Sexagesimal", "digits": "Various",
             "uses": "Time, angles, coordinates (Babylonian)"},
            {"base": "phi", "name": "Golden ratio base", "value": 1.618,
             "property": "Unique representation using Fibonacci"},
        ]
    
    def _get_universal_constants(self) -> List[Dict]:
        """Universal and cosmological constants."""
        return [
            {"name": "Age of universe", "value": "13.8 billion years",
             "symbol": "t₀", "significance": "Big Bang to present"},
            {"name": "Hubble constant", "value": "67.4 km/s/Mpc",
             "symbol": "H₀", "significance": "Expansion rate of universe"},
            {"name": "Cosmic microwave background", "value": "2.725 K",
             "symbol": "T_CMB", "significance": "Big Bang remnant radiation"},
            {"name": "Critical density", "value": "8.5 × 10^-27 kg/m³",
             "symbol": "ρ_c", "significance": "Flat universe density"},
            {"name": "Dark energy density", "value": "~7 × 10^-27 kg/m³",
             "symbol": "Ω_Λ", "significance": "68% of universe energy"},
            {"name": "Dark matter density", "value": "~2.5 × 10^-27 kg/m³",
             "symbol": "Ω_c", "significance": "27% of universe mass-energy"},
            {"name": "Baryon density", "value": "~0.4 × 10^-27 kg/m³",
             "symbol": "Ω_b", "significance": "5% normal matter"},
            {"name": "Schwarzschild radius (Sun)", "value": "2.95 km",
             "formula": "r_s = 2GM/c²", "significance": "Black hole horizon"},
            {"name": "Planck length", "value": "1.616 × 10^-35 m",
             "symbol": "l_P", "significance": "Minimum meaningful length"},
            {"name": "Planck time", "value": "5.391 × 10^-44 s",
             "symbol": "t_P", "significance": "Time for light to cross Planck length"},
            {"name": "Planck temperature", "value": "1.417 × 10^32 K",
             "symbol": "T_P", "significance": "Maximum temperature"},
            {"name": "Solar mass", "value": "1.989 × 10^30 kg",
             "symbol": "M_☉", "significance": "Mass of Sun"},
            {"name": "Earth mass", "value": "5.972 × 10^24 kg",
             "symbol": "M_⊕", "significance": "Mass of Earth"},
            {"name": "Astronomical unit", "value": "1.496 × 10^11 m",
             "symbol": "AU", "significance": "Earth-Sun distance"},
            {"name": "Light year", "value": "9.461 × 10^15 m",
             "symbol": "ly", "significance": "Distance light travels in year"},
            {"name": "Parsec", "value": "3.086 × 10^16 m",
             "symbol": "pc", "significance": "Parallax of one arcsecond"},
        ]
    
    def feed_all(self, brain, batch_size: int = 50):
        """Feed all knowledge to the brain."""
        total_items = 0
        
        for category, items in self.knowledge_categories.items():
            print(f"\n--- Feeding {category} ---")
            count = 0
            
            for item in items:
                if isinstance(item, tuple):
                    # Constant format: (name, symbol, value, meaning)
                    name, symbol, value, meaning = item
                    message = f"[CONSTANT] {name} ({symbol}) = {value}: {meaning}"
                elif isinstance(item, dict):
                    # Complex item
                    message = f"[{category.upper()}] {json.dumps(item, ensure_ascii=False)}"
                else:
                    message = str(item)
                
                brain.feed(message, category)
                count += 1
                total_items += 1
                
                if count % batch_size == 0:
                    print(f"  Fed {count} items...")
            
            print(f"✅ Fed {count} items from {category}")
        
        return total_items


def demo_universal_feeder():
    """Demo feeding universal knowledge."""
    print("=" * 70)
    print("🌌 UNIVERSAL KNOWLEDGE FEEDER")
    print("=" * 70)
    print("\nFeeding comprehensive knowledge to ternary brain:")
    print("  - Mathematical constants (15+)")
    print("  - Physical constants (20+)")
    print("  - Scientific equations (15+)")
    print("  - Mandelbrot and fractals (10+)")
    print("  - Games: Tic Tac Toe, Chess, Checkers, Go")
    print("  - 7 languages")
    print("  - Numeric systems")
    print("  - Universal constants")
    print()
    
    from brain.seven_region import SevenRegionBrain
    
    brain = SevenRegionBrain()
    knowledge = UniversalKnowledgeBase()
    
    total = knowledge.feed_all(brain, batch_size=20)
    
    print("\n" + "=" * 70)
    print("✅ UNIVERSAL KNOWLEDGE FEEDING COMPLETE")
    print("=" * 70)
    print(f"\nTotal items fed: {total}")
    print(f"Brain tick count: {brain.tick_count}")
    print(f"Brain is now knowledgeable in mathematics, physics, games, languages!")
    print("=" * 70)


if __name__ == "__main__":
    demo_universal_feeder()
