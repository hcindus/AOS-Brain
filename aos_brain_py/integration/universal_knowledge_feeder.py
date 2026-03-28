#!/usr/bin/env python3
"""
Universal Knowledge Auto-Feeder.

Feeds ALL knowledge through stomach-brain pipeline:
- Periodic table (118 elements)
- Physical constants
- Mathematical constants  
- Scientific equations
- Multiple languages
- Root words
- Numbers, letters
"""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from integration.stomach_auto_feeder_full import StomachAutoFeederFull


def get_periodic_table():
    """Get full periodic table data."""
    elements = [
        ("Hydrogen", "H", 1, "Nonmetal"), ("Helium", "He", 2, "Noble Gas"),
        ("Lithium", "Li", 3, "Alkali Metal"), ("Beryllium", "Be", 4, "Alkaline Earth"),
        ("Boron", "B", 5, "Metalloid"), ("Carbon", "C", 6, "Nonmetal"),
        ("Nitrogen", "N", 7, "Nonmetal"), ("Oxygen", "O", 8, "Nonmetal"),
        ("Fluorine", "F", 9, "Halogen"), ("Neon", "Ne", 10, "Noble Gas"),
        ("Sodium", "Na", 11, "Alkali Metal"), ("Magnesium", "Mg", 12, "Alkaline Earth"),
        ("Aluminum", "Al", 13, "Post-transition"), ("Silicon", "Si", 14, "Metalloid"),
        ("Phosphorus", "P", 15, "Nonmetal"), ("Sulfur", "S", 16, "Nonmetal"),
        ("Chlorine", "Cl", 17, "Halogen"), ("Argon", "Ar", 18, "Noble Gas"),
        ("Potassium", "K", 19, "Alkali Metal"), ("Calcium", "Ca", 20, "Alkaline Earth"),
        ("Scandium", "Sc", 21, "Transition Metal"), ("Titanium", "Ti", 22, "Transition Metal"),
        ("Vanadium", "V", 23, "Transition Metal"), ("Chromium", "Cr", 24, "Transition Metal"),
        ("Manganese", "Mn", 25, "Transition Metal"), ("Iron", "Fe", 26, "Transition Metal"),
        ("Cobalt", "Co", 27, "Transition Metal"), ("Nickel", "Ni", 28, "Transition Metal"),
        ("Copper", "Cu", 29, "Transition Metal"), ("Zinc", "Zn", 30, "Transition Metal"),
        ("Gallium", "Ga", 31, "Post-transition"), ("Germanium", "Ge", 32, "Metalloid"),
        ("Arsenic", "As", 33, "Metalloid"), ("Selenium", "Se", 34, "Nonmetal"),
        ("Bromine", "Br", 35, "Halogen"), ("Krypton", "Kr", 36, "Noble Gas"),
        ("Rubidium", "Rb", 37, "Alkali Metal"), ("Strontium", "Sr", 38, "Alkaline Earth"),
        ("Yttrium", "Y", 39, "Transition Metal"), ("Zirconium", "Zr", 40, "Transition Metal"),
        ("Niobium", "Nb", 41, "Transition Metal"), ("Molybdenum", "Mo", 42, "Transition Metal"),
        ("Technetium", "Tc", 43, "Transition Metal"), ("Ruthenium", "Ru", 44, "Transition Metal"),
        ("Rhodium", "Rh", 45, "Transition Metal"), ("Palladium", "Pd", 46, "Transition Metal"),
        ("Silver", "Ag", 47, "Transition Metal"), ("Cadmium", "Cd", 48, "Transition Metal"),
        ("Indium", "In", 49, "Post-transition"), ("Tin", "Sn", 50, "Post-transition"),
        ("Antimony", "Sb", 51, "Metalloid"), ("Tellurium", "Te", 52, "Metalloid"),
        ("Iodine", "I", 53, "Halogen"), ("Xenon", "Xe", 54, "Noble Gas"),
        ("Cesium", "Cs", 55, "Alkali Metal"), ("Barium", "Ba", 56, "Alkaline Earth"),
        ("Lanthanum", "La", 57, "Lanthanide"), ("Cerium", "Ce", 58, "Lanthanide"),
        ("Praseodymium", "Pr", 59, "Lanthanide"), ("Neodymium", "Nd", 60, "Lanthanide"),
        ("Promethium", "Pm", 61, "Lanthanide"), ("Samarium", "Sm", 62, "Lanthanide"),
        ("Europium", "Eu", 63, "Lanthanide"), ("Gadolinium", "Gd", 64, "Lanthanide"),
        ("Terbium", "Tb", 65, "Lanthanide"), ("Dysprosium", "Dy", 66, "Lanthanide"),
        ("Holmium", "Ho", 67, "Lanthanide"), ("Erbium", "Er", 68, "Lanthanide"),
        ("Thulium", "Tm", 69, "Lanthanide"), ("Ytterbium", "Yb", 70, "Lanthanide"),
        ("Lutetium", "Lu", 71, "Lanthanide"), ("Hafnium", "Hf", 72, "Transition Metal"),
        ("Tantalum", "Ta", 73, "Transition Metal"), ("Tungsten", "W", 74, "Transition Metal"),
        ("Rhenium", "Re", 75, "Transition Metal"), ("Osmium", "Os", 76, "Transition Metal"),
        ("Iridium", "Ir", 77, "Transition Metal"), ("Platinum", "Pt", 78, "Transition Metal"),
        ("Gold", "Au", 79, "Transition Metal"), ("Mercury", "Hg", 80, "Transition Metal"),
        ("Thallium", "Tl", 81, "Post-transition"), ("Lead", "Pb", 82, "Post-transition"),
        ("Bismuth", "Bi", 83, "Post-transition"), ("Polonium", "Po", 84, "Metalloid"),
        ("Astatine", "At", 85, "Halogen"), ("Radon", "Rn", 86, "Noble Gas"),
        ("Francium", "Fr", 87, "Alkali Metal"), ("Radium", "Ra", 88, "Alkaline Earth"),
        ("Actinium", "Ac", 89, "Actinide"), ("Thorium", "Th", 90, "Actinide"),
        ("Protactinium", "Pa", 91, "Actinide"), ("Uranium", "U", 92, "Actinide"),
        ("Neptunium", "Np", 93, "Actinide"), ("Plutonium", "Pu", 94, "Actinide"),
        ("Americium", "Am", 95, "Actinide"), ("Curium", "Cm", 96, "Actinide"),
        ("Berkelium", "Bk", 97, "Actinide"), ("Californium", "Cf", 98, "Actinide"),
        ("Einsteinium", "Es", 99, "Actinide"), ("Fermium", "Fm", 100, "Actinide"),
        ("Mendelevium", "Md", 101, "Actinide"), ("Nobelium", "No", 102, "Actinide"),
        ("Lawrencium", "Lr", 103, "Actinide"), ("Rutherfordium", "Rf", 104, "Transition Metal"),
        ("Dubnium", "Db", 105, "Transition Metal"), ("Seaborgium", "Sg", 106, "Transition Metal"),
        ("Bohrium", "Bh", 107, "Transition Metal"), ("Hassium", "Hs", 108, "Transition Metal"),
        ("Meitnerium", "Mt", 109, "Transition Metal"), ("Darmstadtium", "Ds", 110, "Transition Metal"),
        ("Roentgenium", "Rg", 111, "Transition Metal"), ("Copernicium", "Cn", 112, "Transition Metal"),
        ("Nihonium", "Nh", 113, "Post-transition"), ("Flerovium", "Fl", 114, "Post-transition"),
        ("Moscovium", "Mc", 115, "Post-transition"), ("Livermorium", "Lv", 116, "Post-transition"),
        ("Tennessine", "Ts", 117, "Halogen"), ("Oganesson", "Og", 118, "Noble Gas")
    ]
    return elements


def get_equations():
    """Get scientific equations."""
    equations = [
        "E=mc² (mass-energy equivalence)",
        "F=ma (Newton's second law)",
        "E=hf (Planck-Einstein relation)",
        "S=k log W (Boltzmann entropy)",
        "∇·E = ρ/ε₀ (Gauss's law)",
        "∇×E = -∂B/∂t (Faraday's law)",
        "iℏ∂ψ/∂t = Ĥψ (Schrödinger equation)",
        "PV=nRT (Ideal gas law)",
        "F=G(m₁m₂)/r² (Newton's gravitation)",
        "c=λν (Wave equation)"
    ]
    return equations


def get_physical_constants():
    """Get physical constants."""
    constants = [
        ("Speed of light", "c", "299792458 m/s"),
        ("Gravitational constant", "G", "6.67430e-11 m³/kg/s²"),
        ("Planck constant", "h", "6.62607015e-34 J⋅s"),
        ("Reduced Planck constant", "ℏ", "1.054571817e-34 J⋅s"),
        ("Boltzmann constant", "k", "1.380649e-23 J/K"),
        ("Avogadro constant", "Nₐ", "6.02214076e23 mol⁻¹"),
        ("Elementary charge", "e", "1.602176634e-19 C"),
        ("Fine-structure constant", "α", "7.2973525693e-3"),
        ("Rydberg constant", "R∞", "10973731.568160 m⁻¹"),
        ("Stefan-Boltzmann constant", "σ", "5.670374419e-8 W/m²/K⁴")
    ]
    return constants


def get_mathematical_constants():
    """Get mathematical constants."""
    constants = [
        ("Pi", "π", "3.14159265358979", "Ratio of circle circumference to diameter"),
        ("Euler's number", "e", "2.71828182845905", "Base of natural logarithm"),
        ("Golden ratio", "φ", "1.61803398874989", "(1+√5)/2"),
        ("Square root of 2", "√2", "1.41421356237310", "Pythagoras constant"),
        ("Square root of 3", "√3", "1.73205080756888", "Theodorus constant"),
        ("Imaginary unit", "i", "i", "Square root of -1"),
        ("Feigenbaum constant", "δ", "4.66920160910299", "Period doubling bifurcation"),
        ("Euler-Mascheroni", "γ", "0.57721566490153", "Limit of harmonic series"),
        ("Catalan's constant", "G", "0.91596559417722", "Series sum"),
        ("Khinchin's constant", "K", "2.68545200106531", "Continued fraction limit")
    ]
    return constants


def get_languages():
    """Get language data."""
    languages = {
        "Latin": ["amo", "amas", "amat", "amamus", "amatis", "amant", "sum", "es", "est"],
        "Greek": ["alpha", "beta", "gamma", "delta", "epsilon", "zeta", "eta", "theta"],
        "Sanskrit": ["om", "namaste", "karma", "dharma", "yoga", "mantra", "guru"],
        "Arabic": ["salam", "shukran", "marhaba", "habibi", "inshallah", "alhamdulillah"],
        "Hebrew": ["shalom", "todah", "boker tov", "laila tov", "sabra"],
        "Chinese": ["hello-你好", "peace-和平", "love-爱", "wisdom-智慧", "strength-力"],
        "Japanese": ["konnichiwa", "sayonara", "arigato", "ohayou", "sumimasen"],
        "German": ["liebe", "freund", "wissen", "kraft", "frieden", "danke"],
        "French": ["amour", "paix", "savoir", "ami", "merci", "bonjour"],
        "Spanish": ["amor", "paz", "saber", "amigo", "gracias", "hola"],
        "Russian": ["lyubov", "mir", "drug", "spasibo", "privet", "paka"],
        "Hindi": ["namaste", "prem", "shanti", "gyan", "dost", "dhanyavad"]
    }
    return languages


def get_root_words():
    """Get Indo-European root words."""
    roots = [
        ("*ḱer-", "heat, fire", "English: hearth, German: Herd"),
        ("*deḱ-", "acceptable, fitting", "Latin: decet, Greek: dokein"),
        ("*gʷem-", "come", "Latin: venire, English: come"),
        ("*leǵ-", "gather, collect", "Latin: legere, Greek: legein"),
        ("*mē-", "measure", "Latin: mensus, English: meter"),
        ("*ped-", "foot", "Latin: pedem, Greek: podos, English: foot"),
        ("*ster-", "star", "Latin: stella, Greek: aster, English: star"),
        ("*wodr̥", "water", "Latin: unda, Greek: hydor, English: water"),
        ("*ǵenh₁-", "beget, give birth", "Latin: genus, Greek: genos"),
        ("*kʷel-", "turn, move around", "Latin: colere, Greek: telein"),
        ("*h₁es-", "to be", "Latin: esse, Greek: einai, English: is"),
        ("*h₂er-", "fit together, join", "Latin: ars, Greek: harmos"),
        ("*h₃er-", "to move", "Greek: orinein, English: run?"),
        ("*yew-", "to tie, bind", "Latin: iugum, Greek: zygon"),
        ("*ǵʰos-ti-", "stranger, guest, host", "Latin: hostis, English: guest")
    ]
    return roots


def get_numbers_letters():
    """Get numbers and letters."""
    data = {
        "integers": list(range(0, 101)),
        "primes": [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97],
        "fibonacci": [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987],
        "greek_letters": ["alpha", "beta", "gamma", "delta", "epsilon", "zeta", "eta", "theta", 
                         "iota", "kappa", "lambda", "mu", "nu", "xi", "omicron", "pi", "rho",
                         "sigma", "tau", "upsilon", "phi", "chi", "psi", "omega"],
        "hebrew_letters": ["aleph", "bet", "gimel", "dalet", "he", "vav", "zayin", "chet",
                          "tet", "yod", "kaf", "lamed", "mem", "nun", "samekh", "ayin", "pe",
                          "tsadi", "qof", "resh", "shin", "tav"],
        "runic_letters": ["fehu", "uruz", "thurisaz", "ansuz", "raidho", "kenaz", "gebo", "wunjo",
                         "hagalaz", "nauthiz", "isa", "jera", "eihwaz", "perthro", "algiz", "sowilo",
                         "tiwaz", "berkano", "ehwaz", "mannaz", "laguz", "ingwaz", "dagaz", "othala"]
    }
    return data


def prepare_all_knowledge():
    """Prepare all knowledge items for feeding."""
    items = []
    
    # Periodic table
    elements = get_periodic_table()
    for name, symbol, number, category in elements:
        items.append((f"Element {name} ({symbol}), atomic number {number}, {category}", "periodic_table"))
    
    # Equations
    for eq in get_equations():
        items.append((eq, "equation"))
    
    # Physical constants
    for name, symbol, value in get_physical_constants():
        items.append((f"{name} ({symbol}) = {value}", "physical_constant"))
    
    # Mathematical constants
    for name, symbol, value, meaning in get_mathematical_constants():
        items.append((f"{name} ({symbol}) = {value}: {meaning}", "math_constant"))
    
    # Languages
    for lang, words in get_languages().items():
        for word in words:
            items.append((f"{lang}: {word}", f"language_{lang.lower()}"))
    
    # Root words
    for root, meaning, derivatives in get_root_words():
        items.append((f"PIE root {root}: {meaning} → {derivatives}", "pie_root"))
    
    # Numbers and letters
    data = get_numbers_letters()
    for num in data["integers"]:
        items.append((f"Integer: {num}", "number"))
    for prime in data["primes"]:
        items.append((f"Prime number: {prime}", "prime"))
    for fib in data["fibonacci"]:
        items.append((f"Fibonacci: {fib}", "fibonacci"))
    for letter in data["greek_letters"]:
        items.append((f"Greek letter: {letter}", "greek"))
    for letter in data["hebrew_letters"]:
        items.append((f"Hebrew letter: {letter}", "hebrew"))
    for letter in data["runic_letters"]:
        items.append((f"Runic letter: {letter}", "runic"))
    
    return items


def run_universal_auto_feed():
    """Run the complete universal knowledge auto-feed."""
    print("=" * 70)
    print("🌌 UNIVERSAL KNOWLEDGE AUTO-FEED")
    print("=" * 70)
    print()
    print("Loading knowledge corpus...")
    
    items = prepare_all_knowledge()
    
    print(f"Total items to feed: {len(items)}")
    print(f"  - Periodic table: 118 elements")
    print(f"  - Equations: 10")
    print(f"  - Physical constants: 10")
    print(f"  - Mathematical constants: 10")
    print(f"  - Languages: 12 languages, ~72 words")
    print(f"  - PIE root words: 15")
    print(f"  - Numbers: 101 integers + 25 primes + 17 Fibonacci")
    print(f"  - Letters: 24 Greek + 22 Hebrew + 24 Runic")
    print()
    
    # Convert to format for feeder
    feeder_items = []
    for content, category in items:
        feeder_items.append((content, "", "", category))
    
    # Run feeder
    feeder = StomachAutoFeederFull()
    result = feeder.run_until_empty(feeder_items)
    
    return result, len(items)


if __name__ == "__main__":
    result, total = run_universal_auto_feed()
    
    print("\n" + "=" * 70)
    print("✅ UNIVERSAL KNOWLEDGE INGESTION COMPLETE")
    print("=" * 70)
    print(f"\nFinal Stats:")
    print(f"  Total knowledge items: {total}")
    print(f"  Brain ticks: {result['brain_ticks']}")
    print(f"  Brain clusters: {result['brain_clusters']}")
    print(f"  Efficiency: {result['efficiency']:.1f}%")
