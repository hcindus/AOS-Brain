#!/usr/bin/env python3
"""
Engineering Dictionary + Materials & Fundamentals + Law Dictionary
"""

import sys
sys.path.insert(0, '/root/.aos/aos')

from stomach_v2 import InformationStomach
from intestine_v2 import InformationIntestine
from superior_heart import SuperiorHeart
from brain_v31 import AOSBrainV31
from ternary_interfaces import DigestionInput, IntestineInput, HeartBeatInput, BrainInput

class EngineeringLawFeeder:
    def __init__(self):
        self.stomach = InformationStomach(capacity=1000)
        self.intestine = InformationIntestine()
        self.heart = SuperiorHeart()
        self.brain = AOSBrainV31()
        self.total_fed = 0
        print("=" * 70)
        print("  ⚙️ ENGINEERING + MATERIALS + LAW DICTIONARIES")
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
    
    def feed_engineering(self):
        """Engineering Dictionary"""
        print("\n[ENGINEERING] Teaching engineering fundamentals...")
        
        engineering = [
            "ENGINEERING: Discipline - Application of science and math to design/build, solve problems",
            "ENGINEERING: Civil - Infrastructure, bridges, roads, buildings, dams, water systems",
            "ENGINEERING: Mechanical - Machines, engines, HVAC, robotics, thermal systems",
            "ENGINEERING: Electrical - Circuits, power generation, motors, electronics",
            "ENGINEERING: Chemical - Process design, reactions, refining, pharmaceuticals",
            "ENGINEERING: Software - Code, algorithms, systems architecture, debugging",
            "ENGINEERING: Aerospace - Aircraft, spacecraft, propulsion, aerodynamics",
            "ENGINEERING: Biomedical - Medical devices, prosthetics, tissue engineering",
            "ENGINEERING: Structural - Analysis of load-bearing elements, beams, columns",
            "ENGINEERING: Thermodynamics - Heat transfer, energy conversion, entropy, laws 0-3",
            "ENGINEERING: Fluid Dynamics - Flow behavior, Bernoulli, Reynolds number, drag",
            "ENGINEERING: Statics - Forces in equilibrium, free body diagrams, moments",
            "ENGINEERING: Dynamics - Motion, kinetics, kinematics, vibration",
            "ENGINEERING: Control Systems - Feedback loops, PID controllers, automation",
            "ENGINEERING: Signal Processing - Filtering, Fourier transform, sampling",
            "ENGINEERING: CAD - Computer aided design, modeling, drafting, simulation",
            "ENGINEERING: FEA - Finite element analysis, stress simulation, meshing",
            "ENGINEERING: Tolerance - Manufacturing variance, fits, ISO standards",
            "ENGINEERING: Safety Factor - Margin above expected load, redundancy",
            "ENGINEERING: Optimization - Minimize cost/maximize performance, constraints",
        ]
        
        for item in engineering:
            self.feed_item(item, "dictionary_engineering", 0.78)
        
        print(f"  ✅ Engineering: {len(engineering)} terms")
        return len(engineering)
    
    def feed_materials(self):
        """Materials & Fundamentals"""
        print("\n[MATERIALS] Teaching materials science...")
        
        materials = [
            "MATERIALS: Science - Study of properties, processing, and performance of materials",
            "MATERIAL: Metal - Conductive, malleable, crystalline structure, dislocations",
            "METAL: Steel - Iron + carbon, strong, alloy, stainless (chromium)",
            "METAL: Aluminum - Light, corrosion resistant, aircraft, 6061, 7075 alloys",
            "METAL: Copper - Excellent conductor, wiring, plumbing, antimicrobial",
            "METAL: Titanium - Strong, light, corrosion proof, biocompatible, expensive",
            "METAL: Gold - Non-reactive, conductor, jewelry, electronics, corrosion proof",
            "MATERIAL: Polymer - Plastics, long chains, thermoplastics, thermosets",
            "POLYMER: Polyethylene - PE, versatile, HDPE, LDPE, bottles, bags",
            "POLYMER: Polypropylene - PP, tough, autoclavable, containers, automotive",
            "POLYMER: PVC - Polyvinyl chloride, pipes, vinyl, plasticized",
            "POLYMER: Nylon - Polyamide, strong, abrasion resistant, fibers, gears",
            "POLYMER: PTFE - Teflon, low friction, non-stick, chemical resistant",
            "POLYMER: Polycarbonate - PC, impact resistant, transparent, bulletproof glass",
            "MATERIAL: Ceramic - Hard, brittle, heat resistant, alumina, zirconia",
            "CERAMIC: Concrete - Cement + aggregate, compression strong, tension weak",
            "CERAMIC: Glass - Amorphous, transparent, silica, soda-lime, borosilicate",
            "MATERIAL: Composite - Combined materials, fiber reinforced, carbon fiber",
            "COMPOSITE: Carbon Fiber - CFRP, strong/light, aerospace, expensive",
            "COMPOSITE: Fiberglass - GFRP, affordable, corrosion resistant, boats",
            "COMPOSITE: Kevlar - Aramid, impact resistant, bulletproof, tires",
            "MATERIAL: Wood - Natural composite, cellulose/lignin, grain, anisotropic",
            "WOOD: Hardwood - Deciduous, oak, maple, dense, furniture",
            "WOOD: Softwood - Coniferous, pine, spruce, construction, fast growth",
            "MATERIAL: Elastomer - Rubber, elastic, vulcanization, seals, tires",
            "MATERIAL: Semiconductor - Silicon, bandgap, doping, transistors, chips",
            "MATERIAL PROPERTY: Hardness - Resistance to indentation, Mohs, Rockwell",
            "MATERIAL PROPERTY: Strength - Yield, ultimate, tensile, compressive",
            "MATERIAL PROPERTY: Ductility - Ability to deform without breaking",
            "MATERIAL PROPERTY: Conductivity - Thermal and electrical, metals best",
            "MATERIAL PROPERTY: Density - Mass per volume, aluminum light, lead heavy",
            "HEAT TREATMENT: Annealing - Softening, relieve stress, furnace cool",
            "HEAT TREATMENT: Quenching - Rapid cooling, hardening, martensite",
            "HEAT TREATMENT: Tempering - Reheat after quench, toughness, reduce brittleness",
            "CORROSION: Oxidation - Rust, galvanic, protection, coatings, anodizing",
            "WELDING: Joining - Fusion, MIG, TIG, arc, spot, brazing, soldering",
            "CASTING: Process - Mold, pour metal, solidify, sand, die, investment",
            "FORGING: Process - Hammer, press, shape hot metal, grain flow, strength",
            "MACHINING: Process - Cutting, drilling, milling, turning, lathe, CNC",
            "ADDITIVE: 3D Printing - Layer by layer, FDM, SLA, SLS, prototypes",
            "NANOMATERIALS: Scale - 1-100nm, unique properties, graphene, CNT, applications",
        ]
        
        for item in materials:
            self.feed_item(item, "dictionary_materials", 0.78)
        
        print(f"  ✅ Materials: {len(materials)} concepts")
        return len(materials)
    
    def feed_law(self):
        """Law Dictionary"""
        print("\n[LAW] Teaching legal fundamentals...")
        
        law = [
            "LAW: Definition - Rules enforced by social institutions, legislation, courts",
            "LAW: Common Law - Precedent-based, judge-made, UK origin, case law",
            "LAW: Civil Law - Codified, statute-based, Roman origin, Continental Europe",
            "LAW: Criminal - Offenses against society, prosecution, punishment",
            "LAW: Civil - Disputes between parties, contracts, torts, property",
            "LAW: Constitutional - Fundamental principles, government powers, rights",
            "LAW: Administrative - Agency regulations, executive, compliance",
            "LAW: International - Treaties, customs, between nations, Geneva, Hague",
            "LAW: Corporate - Business entities, formation, governance, mergers",
            "LAW: Intellectual Property - Patents, copyrights, trademarks, trade secrets",
            "LAW: Contract - Agreement enforceable, offer, acceptance, consideration",
            "LAW: Tort - Civil wrong, negligence, intentional harm, damages",
            "LAW: Property - Real (land) and personal (chattel), ownership, rights",
            "LEGAL: Plaintiff - Party bringing lawsuit, complainant",
            "LEGAL: Defendant - Party being sued, accused",
            "LEGAL: Burden of Proof - Standard, preponderance, beyond reasonable doubt",
            "LEGAL: Statute - Written law enacted by legislature",
            "LEGAL: Ordinance - Local law, municipal, city/county regulations",
            "LEGAL: Regulation - Agency rules, OSHA, EPA, administrative",
            "LEGAL: Precedent - Prior case guiding future, stare decisis",
            "LEGAL: Jurisdiction - Authority to hear case, geographic, subject",
            "LEGAL: Venue - Proper location for trial",
            "LEGAL: Discovery - Evidence exchange, depositions, documents",
            "LEGAL: Deposition - Sworn testimony out of court, transcript",
            "LEGAL: Subpoena - Order to appear/testify or produce documents",
            "LEGAL: Affidavit - Written sworn statement",
            "LEGAL: Tortfeasor - One who commits tort",
            "LEGAL: Liability - Legal responsibility, fault, obligation",
            "LEGAL: Damages - Monetary compensation, compensatory, punitive, nominal",
            "LEGAL: Injunction - Court order to do or stop doing something",
            "LEGAL: Writ - Formal written order",
            "LEGAL: Habeas Corpus - Challenge unlawful detention, produce the body",
            "LEGAL: Due Process - Fair treatment, notice, hearing, 14th Amendment",
            "LEGAL: Equal Protection - Laws applied equally, 14th Amendment",
            "LEGAL: Negligence - Breach of duty causing harm, reasonable person",
            "LEGAL: Strict Liability - No fault needed, abnormally dangerous, products",
            "LEGAL: Malpractice - Professional negligence, doctors, lawyers",
            "LEGAL: Defamation - Libel (written) / Slander (spoken), false statement",
            "LEGAL: Fraud - Intentional deception, misrepresentation",
            "LEGAL: Embezzlement - Theft by entrusted person",
            "LEGAL: Larceny - Theft of personal property",
            "LEGAL: Burglary - Unauthorized entry to commit crime",
            "LEGAL: Robbery - Theft by force or threat",
            "LEGAL: Homicide - Killing of one person by another, murder/manslaughter",
            "LEGAL: Mens Rea - Guilty mind, criminal intent",
            "LEGAL: Actus Reus - Guilty act, physical element of crime",
            "LEGAL: Alibi - Evidence of being elsewhere",
            "LEGAL: Miranda Rights - 5th/6th Amendment warnings on arrest",
            "LEGAL: Attorney-Client Privilege - Confidential communications",
            "LEGAL: Work Product - Attorney preparation materials, protected",
            "LEGAL: Pro Bono - Free legal service, public good",
            "LEGAL: Class Action - Group lawsuit, representative plaintiff",
            "LEGAL: Settlement - Agreement to resolve dispute, no admission",
            "LEGAL: Verdict - Jury decision, guilty/not guilty, civil award",
            "LEGAL: Judgment - Court final decision, enforceable",
            "LEGAL: Appeal - Challenge to higher court, errors of law",
            "LEGAL: Supreme Court - Highest court, precedent, constitutional",
            "LEGAL: Arbitration - Alternative dispute, binding decision, private",
            "LEGAL: Mediation - Facilitated negotiation, non-binding",
            "LEGAL: Statute of Limitations - Time limit to file suit",
            "LEGAL: Double Jeopardy - 5th Amendment, can't be tried twice",
            "LEGAL: Self-Incrimination - 5th Amendment, right to silence",
            "LEGAL: Search Warrant - Judicial authorization, 4th Amendment",
            "LEGAL: Probable Cause - Reasonable basis for belief, arrest/search",
            "LEGAL: Reasonable Suspicion - Lower standard, brief detention",
        ]
        
        for item in law:
            self.feed_item(item, "dictionary_law", 0.78)
        
        print(f"  ✅ Law: {len(law)} terms")
        return len(law)
    
    def feed_complete(self):
        print("\n" + "=" * 70)
        print("  ⚙️ ENGINEERING + MATERIALS + LAW FEED COMPLETE")
        print("=" * 70)
        
        import time
        start = time.time()
        total = 0
        
        total += self.feed_engineering()
        total += self.feed_materials()
        total += self.feed_law()
        
        self.brain.save_state()
        
        elapsed = time.time() - start
        
        print("\n" + "=" * 70)
        print("  ✅ ALL DICTIONARIES FED")
        print("=" * 70)
        print(f"  Total Items Fed: {total}")
        print(f"  Brain Ticks: {self.brain.tick_count}")
        print(f"  Brain Memories: {self.brain.hippocampus.total_traces}")
        print(f"  Time: {elapsed:.1f}s")
        print("=" * 70)

if __name__ == "__main__":
    feeder = EngineeringLawFeeder()
    feeder.feed_complete()
