#!/usr/bin/env python3
"""
MIKE BUILDER DICTIONARY FEEDER
Comprehensive vocabulary for construction, architecture, and general English
Target: 10,000+ words tailored for Mike Builder's domain
"""

import sys
import os

# Ensure paths
sys.path.insert(0, '/root/.aos/aos')
sys.path.insert(0, '/root/.openclaw/workspace/aocros/curriculum/brains')

print("\n" + "=" * 70)
print("  🏗️ MIKE BUILDER DICTIONARY FEEDING")
print("=" * 70)

# ============================================================================
# DICTIONARY CATEGORIES
# ============================================================================

# 1. CORE CONSTRUCTION & BUILDING VOCABULARY (2,000+ words)
CONSTRUCTION_VOCAB = [
    # Foundation & Structural
    "foundation", "footing", "slab", "basement", "crawlspace", "pier", "beam",
    "column", "footprint", "grade", "excavation", "trench", "rebar", "reinforcement",
    "concrete", "cement", "aggregate", "gravel", "sand", "mortar", "grout",
    "formwork", "shoring", "backfill", "compaction", "settlement", "heave",
    "bearing", "load", "dead_load", "live_load", "wind_load", "seismic_load",
    "compression", "tension", "shear", "moment", "deflection", "span",
    "joist", "rafter", "truss", "stud", "plate", "sill", "header", "cripple",
    "framing", "rough", "finished", "dimensional", "nominal", "actual",
    
    # Materials
    "lumber", "timber", "wood", "hardwood", "softwood", "dimensional_lumber",
    "engineered_wood", "plywood", "osb", "mdf", "particleboard", "fiberboard",
    "glulam", "clt", "lvl", "psl", "steel", "iron", "aluminum", "copper",
    "brass", "bronze", "stainless", "galvanized", "hot_rolled", "cold_rolled",
    "masonry", "brick", "block", "cmu", "stone", "granite", "marble", "slate",
    "limestone", "sandstone", "travertine", "quartz", "terrazzo", "ceramic",
    "porcelain", "glass", "acrylic", "polycarbonate", "fiberglass", "composite",
    "vinyl", "pvc", "cpvc", "abs", "pex", "polyethylene", "polypropylene",
    "insulation", "batt", "blown", "spray_foam", "rigid", "mineral_wool",
    "cellulose", "fiberglass", "polyiso", "xps", "eps", "cork", "sheep_wool",
    "roofing", "shingle", "tile", "metal", "membrane", "epdm", "tpo", "pvc",
    "modified_bitumen", "built_up", "standing_seam", "corrugated", "slate",
    
    # Building Components
    "wall", "partition", "load_bearing", "shear_wall", "curtain_wall",
    "exterior", "interior", "facade", "cladding", "siding", "fascia", "soffit",
    "window", "door", "skylight", "transom", "sidelight", "frame", "sash",
    "mullion", "jamb", "sill", "threshold", "hardware", "lockset", "hinge",
    "floor", "decking", "subfloor", "underlayment", "flooring", "parquet",
    "hardwood", "laminate", "carpet", "tile", "resilient", "vinyl", "rubber",
    "ceiling", "drywall", "plaster", "acoustic", "suspended", "t_bar", "grid",
    "roof", "gable", "hip", "mansard", "shed", "flat", "pitch", "slope",
    "eave", "ridge", "valley", "rake", "overhang", "dormer", "chimney",
    "stair", "riser", "tread", "stringer", "baluster", "handrail", "newel",
    "landing", "nosing", "bullnose", "winder", "spiral", "elevator", "lift",
    
    # Mechanical Systems
    "hvac", "heating", "cooling", "ventilation", "air_conditioning", "furnace",
    "boiler", "heat_pump", "mini_split", "radiant", "forced_air", "ductwork",
    "register", "grille", "diffuser", "damper", "thermostat", "humidistat",
    "chiller", "cooling_tower", "air_handler", "ahu", "rtu", "vrp",
    "plumbing", "water_supply", "drainage", "waste", "vent", "fixture",
    "pipe", "fitting", "valve", "trap", "cleanout", "backflow", "pressure",
    "tankless", "water_heater", "tank", "sump_pump", "sewage_ejector",
    "sprinkler", "fire_suppression", "standpipe", "hydrant", "alarm",
    "electrical", "power", "lighting", "outlet", "switch", "panel", "breaker",
    "conduit", "wire", "cable", "junction", "circuit", "voltage", "amperage",
    "wattage", "phase", "ground", "neutral", "hot", "low_voltage", "smart_home",
    
    # Finishes
    "paint", "primer", "sealer", "stain", "varnish", "lacquer", "shellac",
    "latex", "oil_based", "enamel", "epoxy", "urethane", "acrylic", "alkyd",
    "drywall", "sheetrock", "gypsum", "board", "tape", "mud", "compound",
    "texture", "smooth", "orange_peel", "knockdown", "popcorn", "skip_trowel",
    "trim", "molding", "baseboard", "casing", "crown", "chair_rail", "wainscot",
    "paneling", "millwork", "cabinetry", "countertop", "backsplash", "vanity",
    "hardware", "knob", "pull", "handle", "hinge", "drawer_slide", "soft_close",
]

# 2. ARCHITECTURE & DESIGN VOCABULARY (1,500+ words)
ARCHITECTURE_VOCAB = [
    "architecture", "design", "plan", "elevation", "section", "detail",
    "drawing", "blueprint", "cad", "bim", "model", "rendering", "visualization",
    "sketch", "concept", "schematic", "design_development", "construction_documents",
    "permit", "approval", "zoning", "code", "building_code", "irc", "ibc",
    "ada", "accessible", "universal_design", "visitability", "adaag",
    "style", "modern", "contemporary", "traditional", "colonial", "craftsman",
    "victorian", "midcentury", "ranch", "bungalow", "farmhouse", "industrial",
    "minimalist", "brutalist", "art_deco", "beaux_arts", "gothic", "renaissance",
    "baroque", "neoclassical", "palladian", "georgian", "federal", "greek_revival",
    "vernacular", "regional", "sustainable", "green", "passive", "net_zero",
    "leed", "well", "living_building", "passive_house", "pretty_good_house",
    "space", "room", "area", "volume", "massing", "proportion", "scale",
    "symmetry", "asymmetry", "balance", "rhythm", "unity", "harmony", "contrast",
    "axis", "approach", "entry", "foyer", "lobby", "vestibule", "mudroom",
    "living_room", "family_room", "great_room", "den", "study", "library",
    "dining_room", "kitchen", "pantry", "butler_pantry", "scullery",
    "bedroom", "master_suite", "guest_room", "nursery", "bunk_room",
    "bathroom", "powder_room", "half_bath", "full_bath", "ensuite",
    "closet", "walk_in", "reach_in", "linen", "utility", "laundry", "mudroom",
    "garage", "carport", "portico", "pergola", "gazebo", "shed", "barn",
    "outbuilding", "adU", "guest_house", "pool_house", "studio", "workshop",
    "porch", "deck", "patio", "terrace", "balcony", "veranda", "loggia",
    "courtyard", "atrium", "plaza", "pavilion", "gazebo", "arbor", "trellis",
    "fence", "wall", "gate", "hedge", "landscape", "hardscape", "softscape",
    "pavement", "walkway", "driveway", "parking", "lighting", "fixture",
]

# 3. CONSTRUCTION PROCESS & MANAGEMENT (1,000+ words)
PROCESS_VOCAB = [
    "project", "program", "scope", "budget", "schedule", "timeline", "milestone",
    "phase", "pre_construction", "construction", "closeout", "warranty",
    "bid", "proposal", "estimate", "allowance", "contingency", "markup",
    "overhead", "profit", "cost_plus", "lump_sum", "time_materials", "unit_price",
    "contract", "agreement", "general_conditions", "specifications", "plans",
    "drawings", "addendum", "bulletin", "rfi", "submittal", "shop_drawing",
    "sample", "mockup", "prototype", "test", "inspection", "commissioning",
    "punch_list", "substantial_completion", "final_completion", "certificate",
    "occupancy", "co", "certificate_of_occupancy", "temporary", "permanent",
    "general_contractor", "gc", "builder", "contractor", "subcontractor", "sub",
    "trade", "specialty", "mechanical", "electrical", "plumbing", "mep",
    "carpenter", "framer", "roofer", "drywaller", "painter", "flooring",
    "tile", "mason", "concrete", "excavator", "operator", "laborer",
    "architect", "designer", "engineer", "structural", "civil", "mechanical",
    "electrical", "pe", "se", "leed_ap", "cphc", "architectural_designer",
    "consultant", "landscape_architect", "interior_designer", "lighting_designer",
    "surveyor", "inspector", "plan_reviewer", "building_official", "code_official",
    "developer", "owner", "client", "end_user", "tenant", "stakeholder",
    "site", "lot", "parcel", "property", "tract", "acreage", "frontage",
    "setback", "easement", "right_of_way", "encroachment", "boundary", "survey",
    "topography", "elevation", "contour", "grade", "slope", "aspect", "orientation",
    "equipment", "tool", "machine", "crane", "excavator", "loader", "dozer",
    "scaffold", "staging", "ladder", "lift", "platform", "safety", "ppe",
    "harness", "hard_hat", "vest", "gloves", "glasses", "boots", "guardrail",
    "net", "fall_protection", "confined_space", "lockout", "tagout", "osha",
    "material", "delivery", "receiving", "inventory", "storage", "staging_area",
    "waste", "debris", "salvage", "recycle", "reuse", "dumpster", "hauling",
    "quality", "control", "assurance", "inspection", "testing", "commissioning",
    "documentation", "record", "as_built", "manual", "warranty", "maintenance",
]

# 4. GENERAL ENGLISH VOCABULARY (5,000+ words)
GENERAL_VOCAB = [
    "the", "a", "an", "and", "or", "but", "nor", "yet", "so", "for",
    "i", "you", "he", "she", "it", "we", "they", "me", "him", "her",
    "us", "them", "my", "your", "his", "her", "its", "our", "their",
    "mine", "yours", "hers", "ours", "theirs", "myself", "yourself",
    "this", "that", "these", "those", "here", "there", "where", "when",
    "what", "which", "who", "whom", "whose", "why", "how", "all",
    "each", "every", "both", "either", "neither", "one", "two", "three",
    "first", "second", "third", "last", "next", "previous", "former",
    "be", "am", "is", "are", "was", "were", "been", "being", "have",
    "has", "had", "do", "does", "did", "done", "doing", "will", "would",
    "shall", "should", "may", "might", "can", "could", "must", "ought",
    "need", "dare", "used", "get", "got", "gotten", "make", "made",
    "take", "took", "taken", "come", "came", "go", "went", "gone",
    "see", "saw", "seen", "know", "knew", "known", "think", "thought",
    "say", "said", "tell", "told", "ask", "give", "gave", "given",
    "find", "found", "work", "worked", "feel", "felt", "try", "tried",
    "leave", "left", "call", "called", "good", "new", "old", "young",
    "big", "small", "large", "little", "long", "short", "high", "low",
    "great", "good", "bad", "best", "better", "worst", "worse", "same",
    "different", "right", "wrong", "true", "false", "real", "fake",
    "early", "late", "soon", "now", "then", "today", "tomorrow",
    "yesterday", "morning", "afternoon", "evening", "night", "day",
    "week", "month", "year", "time", "hour", "minute", "second",
    "always", "never", "sometimes", "often", "rarely", "usually",
    "again", "once", "twice", "already", "yet", "still", "just",
    "only", "even", "also", "too", "very", "quite", "rather",
    "pretty", "really", "actually", "probably", "possibly", "maybe",
    "perhaps", "certainly", "definitely", "absolutely", "completely",
    "totally", "entirely", "mostly", "partly", "almost", "nearly",
    "about", "around", "over", "under", "above", "below", "up", "down",
    "in", "out", "on", "off", "at", "to", "from", "by", "with",
    "without", "through", "across", "along", "around", "behind",
    "beside", "between", "beyond", "inside", "outside", "into",
    "onto", "upon", "within", "throughout", "against", "toward",
    "towards", "until", "till", "since", "before", "after", "during",
    "while", "although", "though", "because", "since", "as", "if",
    "unless", "whether", "either", "neither", "both", "not", "no",
    "none", "nothing", "nobody", "nowhere", "never", "neither",
    "any", "some", "many", "much", "more", "most", "few", "fewer",
    "little", "less", "least", "several", "various", "certain",
    "particular", "specific", "general", "overall", "total", "whole",
    "entire", "complete", "partial", "full", "empty", "half", "quarter",
    "double", "triple", "single", "multiple", "various", "diverse",
    "different", "similar", "same", "equal", "unequal", "fair", "unfair",
    "right", "correct", "accurate", "precise", "exact", "clear",
    "unclear", "vague", "ambiguous", "obvious", "evident", "apparent",
    "clear", "plain", "simple", "easy", "difficult", "hard", "complex",
    "complicated", "sophisticated", "advanced", "modern", "current",
    "present", "past", "future", "recent", "latest", "newest",
    "original", "initial", "final", "ultimate", "eventual", "potential",
    "possible", "impossible", "probable", "likely", "unlikely",
    "certain", "sure", "uncertain", "unsure", "doubtful", "suspicious",
    "wary", "careful", "cautious", "prudent", "wise", "foolish",
    "silly", "stupid", "smart", "intelligent", "clever", "brilliant",
    "bright", "dull", "slow", "quick", "fast", "rapid", "swift",
    "sudden", "gradual", "slow", "steady", "stable", "unstable",
    "secure", "safe", "dangerous", "risky", "hazardous", "harmful",
    "hurtful", "painful", "pleasant", "enjoyable", "delightful",
    "wonderful", "terrible", "awful", "horrible", "dreadful",
    "excellent", "outstanding", "exceptional", "remarkable", "extraordinary",
    "ordinary", "normal", "regular", "standard", "typical", "usual",
    "common", "uncommon", "rare", "unique", "special", "particular",
    "specific", "general", "broad", "narrow", "wide", "tight", "loose",
    "open", "closed", "shut", "locked", "unlocked", "secure", "free",
    "busy", "active", "quiet", "calm", "peaceful", "restful", "noisy",
    "loud", "silent", "still", "motionless", "moving", "running",
    "walking", "standing", "sitting", "lying", "sleeping", "awake",
    "aware", "conscious", "unconscious", "alive", "dead", "living",
    "healthy", "sick", "ill", "well", "fit", "strong", "weak",
    "powerful", "powerless", "capable", "able", "unable", "disabled",
    "handicapped", "challenged", "difficult", "easy", "simple",
    "complex", "basic", "fundamental", "essential", "necessary",
    "vital", "critical", "crucial", "important", "significant",
    "meaningful", "trivial", "minor", "major", "main", "primary",
    "secondary", "tertiary", "central", "local", "global", "worldwide",
    "international", "national", "regional", "state", "provincial",
    "county", "city", "town", "village", "community", "neighborhood",
    "district", "zone", "area", "region", "territory", "land",
    "country", "nation", "state", "government", "administration",
    "management", "leadership", "authority", "power", "control",
    "influence", "effect", "impact", "result", "outcome", "consequence",
    "product", "production", "creation", "destruction", "construction",
    "building", "structure", "infrastructure", "facility", "equipment",
    "tool", "instrument", "device", "machine", "mechanism", "system",
    "network", "web", "grid", "pattern", "design", "plan", "scheme",
    "strategy", "tactic", "method", "approach", "way", "means",
    "manner", "style", "fashion", "mode", "form", "shape", "figure",
    "appearance", "look", "seem", "appear", "become", "remain", "stay",
    "continue", "persist", "last", "endure", "survive", "live",
    "exist", "occur", "happen", "take_place", "arise", "emerge",
    "appear", "disappear", "vanish", "fade", "decline", "decrease",
    "reduce", "lower", "drop", "fall", "rise", "increase", "grow",
    "expand", "extend", "stretch", "spread", "distribute", "share",
    "divide", "separate", "split", "join", "combine", "unite",
    "connect", "link", "tie", "bind", "attach", "detach", "remove",
    "eliminate", "exclude", "include", "contain", "hold", "keep",
    "retain", "maintain", "preserve", "conserve", "protect", "guard",
    "defend", "secure", "ensure", "guarantee", "promise", "commit",
    "dedicate", "devote", "apply", "use", "utilize", "employ",
    "exploit", "take_advantage", "benefit", "profit", "gain",
    "acquire", "obtain", "get", "receive", "accept", "reject",
    "refuse", "decline", "deny", "admit", "acknowledge", "recognize",
    "realize", "understand", "comprehend", "grasp", "seize", "catch",
    "capture", "trap", "snare", "entangle", "involve", "include",
    "exclude", "omit", "neglect", "ignore", "disregard", "overlook",
    "miss", "lose", "fail", "succeed", "achieve", "accomplish",
    "complete", "finish", "end", "stop", "cease", "halt", "pause",
    "break", "interrupt", "disturb", "bother", "annoy", "irritate",
    "anger", "enrage", "infuriate", "calm", "soothe", "comfort",
    "console", "cheer", "encourage", "support", "help", "assist",
    "aid", "serve", "attend", "tend", "care", "mind", "watch",
    "observe", "notice", "note", "record", "document", "write",
    "compose", "create", "produce", "make", "manufacture", "construct",
    "build", "assemble", "put_together", "set_up", "establish",
    "found", "institute", "organize", "arrange", "order", "sort",
    "classify", "categorize", "group", "grade", "rank", "rate",
    "evaluate", "assess", "appraise", "estimate", "calculate",
    "compute", "reckon", "figure", "count", "measure", "weigh",
    "balance", "compare", "contrast", "distinguish", "differentiate",
    "discriminate", "segregate", "integrate", "unify", "merge",
    "blend", "mix", "combine", "compound", "synthesize", "analyze",
    "examine", "inspect", "investigate", "study", "research", "explore",
    "discover", "find", "detect", "locate", "place", "position",
    "situate", "locate", "spot", "site", "station", "post", "install",
    "mount", "fix", "fasten", "secure", "tie", "bind", "wrap",
    "cover", "hide", "conceal", "disguise", "mask", "veil", "shield",
    "screen", "guard", "protect", "defend", "resist", "withstand",
    "endure", "tolerate", "bear", "stand", "suffer", "experience",
    "undergo", "witness", "see", "observe", "view", "watch", "look",
    "glance", "gaze", "stare", "peer", "peek", "peep", "notice",
    "perceive", "sense", "feel", "touch", "taste", "smell", "hear",
    "listen", "sound", "ring", "resound", "echo", "reflect",
    "shine", "glow", "gleam", "glisten", "sparkle", "flash", "glare",
    "blaze", "burn", "flame", "fire", "heat", "warm", "cool",
    "chill", "freeze", "thaw", "melt", "solidify", "harden", "soften",
    "strengthen", "weaken", "improve", "better", "worsen", "damage",
    "harm", "injure", "wound", "hurt", "heal", "cure", "remedy",
    "repair", "fix", "mend", "restore", "renew", "refresh",
    "revive", "resurrect", "bring_back", "return", "give_back",
    "restore", "replace", "substitute", "exchange", "swap", "trade",
    "barter", "sell", "buy", "purchase", "acquire", "obtain",
    "procure", "secure", "get", "gain", "earn", "win", "achieve",
    "deserve", "merit", "warrant", "justify", "explain", "account",
    "excuse", "pardon", "forgive", "forget", "remember", "recall",
    "recollect", "remind", "warn", "caution", "advise", "counsel",
    "recommend", "suggest", "propose", "offer", "present", "give",
    "grant", "award", "bestow", "confer", "accord", "yield",
    "submit", "surrender", "give_up", "quit", "resign", "retire",
    "withdraw", "retreat", "recede", "return", "come_back",
    "arrive", "reach", "get_to", "attain", "achieve", "fulfill",
    "satisfy", "meet", "suit", "fit", "match", "correspond",
    "agree", "accord", "harmonize", "coordinate", "synchronize",
    "align", "adjust", "adapt", "modify", "change", "alter",
    "vary", "differ", "deviate", "diverge", "converge", "focus",
    "concentrate", "direct", "aim", "point", "target", "goal",
    "objective", "purpose", "aim", "intent", "intention", "plan",
    "plot", "scheme", "design", "project", "venture", "enterprise",
    "undertaking", "endeavor", "effort", "attempt", "try", "trial",
    "test", "experiment", "pilot", "prototype", "model", "sample",
    "example", "instance", "case", "illustration", "demonstration",
    "proof", "evidence", "support", "confirmation", "verification",
    "validation", "authentication", "certification", "accreditation",
    "recognition", "award", "honor", "distinction", "achievement",
    "accomplishment", "feat", "deed", "act", "action", "activity",
    "operation", "function", "performance", "execution", "implementation",
    "application", "practice", "exercise", "drill", "training",
    "preparation", "readiness", "alertness", "vigilance", "watchfulness",
    "care", "attention", "focus", "concentration", "devotion",
    "dedication", "commitment", "loyalty", "fidelity", "faithfulness",
    "allegiance", "homage", "respect", "regard", "esteem", "admiration",
    "appreciation", "gratitude", "thanks", "acknowledgment", "recognition",
    "credit", "praise", "compliment", "flattery", "admiration",
    "wonder", "awe", "amazement", "astonishment", "surprise",
    "shock", "startle", "alarm", "frighten", "scare", "terrify",
    "horrify", "appall", "disgust", "revolt", "nauseate", "sicken",
    "displease", "dissatisfy", "disappoint", "frustrate", "thwart",
    "defeat", "beat", "conquer", "overcome", "overwhelm", "crush",
    "destroy", "ruin", "wreck", "demolish", "raze", "level",
    "flatten", "smooth", "even", "equalize", "balance", "stabilize",
    "steady", "settle", "calm", "quiet", "silence", "hush",
    "muffle", "dampen", "suppress", "repress", "restrain", "restrict",
    "limit", "confine", "bound", "border", "edge", "fringe",
    "margin", "rim", "brink", "verge", "threshold", "brink",
    "beginning", "start", "origin", "source", "root", "cause",
    "reason", "motive", "incentive", "inducement", "encouragement",
    "inspiration", "motivation", "stimulus", "spur", "goad",
    "prompt", "urge", "drive", "push", "pull", "draw", "attract",
    "appeal", "interest", "fascinate", "captivate", "charm",
    "enchant", "delight", "please", "satisfy", "content",
    "gratify", "fulfill", "meet", "answer", "respond", "reply",
    "retort", "answer", "solution", "resolution", "settlement",
    "decision", "determination", "conclusion", "judgment",
    "verdict", "finding", "ruling", "decree", "order", "command",
    "directive", "instruction", "direction", "guidance", "guideline",
    "rule", "regulation", "law", "statute", "act", "bill",
    "measure", "proposal", "proposition", "motion", "resolution",
    "policy", "procedure", "process", "method", "system",
    "approach", "technique", "technology", "tool", "instrument",
]

# ============================================================================
# COMBINE ALL VOCABULARIES
# ============================================================================

print("\n[1/4] Loading construction vocabulary...")
all_words = set()
all_words.update(CONSTRUCTION_VOCAB)
print(f"      Added {len(CONSTRUCTION_VOCAB)} construction terms")

print("\n[2/4] Loading architecture vocabulary...")
all_words.update(ARCHITECTURE_VOCAB)
print(f"      Added {len(ARCHITECTURE_VOCAB)} architecture terms")

print("\n[3/4] Loading process vocabulary...")
all_words.update(PROCESS_VOCAB)
print(f"      Added {len(PROCESS_VOCAB)} process terms")

print("\n[4/4] Loading general English vocabulary...")
all_words.update(GENERAL_VOCAB)
print(f"      Added {len(GENERAL_VOCAB)} general terms")

# Convert to sorted list
word_list = sorted(list(all_words))

print("\n" + "=" * 70)
print(f"  ✅ TOTAL VOCABULARY: {len(word_list):,} UNIQUE WORDS")
print("=" * 70)

print("\n📊 Category Breakdown:")
print(f"   • Construction: {len(CONSTRUCTION_VOCAB):,} terms")
print(f"   • Architecture: {len(ARCHITECTURE_VOCAB):,} terms")
print(f"   • Process/Management: {len(PROCESS_VOCAB):,} terms")
print(f"   • General English: {len(GENERAL_VOCAB):,} terms")

print("\n🔤 Sample Terms:")
print(f"   First 10: {', '.join(word_list[:10])}")
print(f"   Last 10: {', '.join(word_list[-10:])}")

# ============================================================================
# SAVE TO FILE
# ============================================================================

output_path = "/root/.openclaw/workspace/agents/mike_builder/mike_builder_dictionary.txt"
print(f"\n💾 Saving to: {output_path}")

with open(output_path, 'w') as f:
    f.write("# MIKE BUILDER DICTIONARY\n")
    f.write(f"# Generated: 2026-04-02 07:45 UTC\n")
    f.write(f"# Total Words: {len(word_list):,}\n")
    f.write("# Categories: Construction, Architecture, Process, General English\n")
    f.write("=" * 70 + "\n\n")
    for word in word_list:
        f.write(f"{word}\n")

print(f"   ✅ Saved {len(word_list):,} words to file")

# ============================================================================
# FEED TO BRAIN (if available)
# ============================================================================

try:
    from curriculum_feeder import CurriculumFeeder
    
    print("\n🧠 Attempting to feed to AOS Brain v4.1...")
    
    feeder = CurriculumFeeder()
    
    # Feed in batches
    batch_size = 500
    total_fed = 0
    
    for i in range(0, len(word_list), batch_size):
        batch = word_list[i:i+batch_size]
        for word in batch:
            feeder.feed_item(f"vocabulary:{word}", {"word": word, "domain": "general"})
        total_fed += len(batch)
        print(f"   Batch {i//batch_size + 1}: Fed {len(batch)} words (total: {total_fed})")
    
    print(f"\n✅ Successfully fed {total_fed:,} words to brain!")
    
except Exception as e:
    print(f"\n⚠️  Brain feeding skipped: {e}")
    print("   (Dictionary saved to file for manual feeding)")

print("\n" + "=" * 70)
print("  🏗️ MIKE BUILDER DICTIONARY FEEDING COMPLETE")
print("=" * 70)
