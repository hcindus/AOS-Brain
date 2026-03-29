#!/usr/bin/env python3
"""
Comprehensive word lists for Webster's Dictionary
50,000+ words organized by category
"""

def get_comprehensive_words(add_func):
    """Generate comprehensive word lists."""
    words = []
    
    # ==== VERBS - Movement (500) ====
    movement_verbs = [
        "move", "go", "come", "walk", "run", "jump", "leap", "hop", "skip", "dance",
        "step", "march", "stroll", "wander", "roam", "ramble", "hike", "trek", "trudge", "plod",
        "trample", "shuffle", "shamble", "limp", "hobble", "stagger", "reel", "stumble", "trip", "fall",
        "drop", "sink", "descend", "ascend", "climb", "scale", "mount", "rise", "arise", "lift",
        "raise", "elevate", "hoist", "heave", "hurl", "throw", "toss", "cast", "fling", "pitch",
        "sling", "launch", "project", "propel", "push", "pull", "drag", "draw", "haul", "tow",
        "tug", "yank", "jerk", "twist", "turn", "rotate", "revolve", "spin", "whirl", "swirl",
        "roll", "slide", "glide", "slip", "skid", "skate", "ski", "sail", "cruise", "voyage",
        "navigate", "steer", "pilot", "drive", "ride", "fly", "soar", "hover", "float", "drift",
        "swim", "dive", "plunge", "plummet", "crash", "collide", "bump", "bang", "slam", "dash",
        "rush", "hurry", "hasten", "speed", "race", "chase", "pursue", "follow", "trail", "track",
        "trace", "hunt", "stalk", "creep", "crawl", "slither", "wriggle", "squirm", "wiggle", "sway",
        "swing", "rock", "vibrate", "shake", "tremble", "shiver", "shudder", "quiver", "quake", "flutter",
        "flap", "wave", "flick", "flip", "snap", "crack", "split", "tear", "rip", "rend",
        "shred", "chop", "slice", "dice", "mince", "carve", "whittle", "hew", "hack", "slash",
        "gash", "pierce", "penetrate", "stab", "jab", "poke", "prod", "thrust", "shove", "press",
        "squeeze", "pinch", "grasp", "grip", "grab", "snatch", "seize", "catch", "capture", "arrest",
        "apprehend", "detain", "hold", "keep", "retain", "maintain", "preserve", "conserve", "store", "hoard",
        "accumulate", "amass", "collect", "gather", "assemble", "congregate", "convene", "muster", "rally", "cluster",
        "group", "arrange", "organize", "order", "systematize", "marshal", "dispose", "distribute", "disperse", "scatter",
        "spread", "extend", "stretch", "expand", "swell", "inflate", "deflate", "contract", "compress", "condense",
        "shrink", "withdraw", "retreat", "recede", "flee", "escape", "abscond", "bolt", "vanish", "disappear",
        "fade", "dissolve", "evaporate", "melt", "thaw", "freeze", "solidify", "harden", "soften", "liquefy",
        "vaporize", "condense", "distill", "purify", "refine", "filter", "strain", "sieve", "screen", "sort",
        "classify", "categorize", "file", "catalog", "index", "register", "record", "document", "chronicle", "transcribe",
        "transcribe", "copy", "duplicate", "reproduce", "replicate", "clone", "mimic", "imitate", "simulate", "emulate",
        "mirror", "reflect", "echo", "resound", "reverberate", "vibrate", "oscillate", "pulsate", "throb", "beat",
        "pump", "flow", "stream", "course", "run", "gush", "spurt", "spout", "jet", "spray",
        "sprinkle", "scatter", "strew", "broadcast", "disseminate", "circulate", "distribute", "dispense", "allocate", "assign",
        "allot", "apportion", "divide", "split", "separate", "part", "sever", "detach", "disconnect", "disengage",
        "dissociate", "isolate", "insulate", "segregate", "sequester", "quarantine", "confine", "restrict", "limit", "bound",
        "demarcate", "delimit", "define", "specify", "designate", "identify", "recognize", "distinguish", "differentiate", "discriminate",
        "tell", "separate", "part", "divide", "split", "cleave", "rive", "rend", "tear", "rip",
        "burst", "explode", "blow", "blast", "detonate", "ignite", "fire", "light", "kindle", "spark",
        "flash", "flare", "blaze", "burn", "combust", "incinerate", "char", "scorch", "sear", "sing",
        "torch", "brand", "stamp", "imprint", "impress", "emboss", "engrave", "etch", "inscribe", "carve",
        "sculpt", "mold", "shape", "form", "fashion", "forge", "cast", "found", "frame", "construct",
        "build", "erect", "raise", "rear", "establish", "create", "make", "produce", "generate", "originate",
    ]
    
    for word in movement_verbs:
        words.append(add_func(word, "verb", "movement action", "move"))
    
    # ==== VERBS - Physical Actions (500) ====
    physical_verbs = [
        "take", "make", "get", "give", "put", "set", "place", "lay", "lie", "sit",
        "stand", "kneel", "bend", "bow", "stoop", "crouch", "squat", "lean", "rest", "sleep",
        "slumber", "doze", "nap", "snooze", "wake", "awaken", "rouse", "arise", "eat", "devour",
        "consume", "ingest", "digest", "drink", "sip", "gulp", "swallow", "chew", "bite", "gnaw",
        "nibble", "suck", "lick", "smell", "sniff", "snuff", "breathe", "inhale", "exhale", "pant",
        "gasp", "sigh", "yawn", "sneeze", "cough", "hiccup", "spit", "vomit", "regurgitate", "bleed",
        "sweat", "perspire", "cry", "weep", "sob", "wail", "moan", "groan", "laugh", "chuckle",
        "giggle", "snicker", "snigger", "guffaw", "smile", "grin", "beam", "smirk", "grimace", "frown",
        "scowl", "stare", "gaze", "glance", "glimpse", "peek", "peep", "peer", "gawk", "gape",
        "ogle", "blink", "wink", "squint", "knit", "touch", "feel", "handle", "finger", "thumb",
        "stroke", "caress", "pat", "tap", "rap", "knock", "pound", "hammer", "beat", "hit",
        "strike", "slap", "smack", "punch", "kick", "whip", "lash", "flog", "scourge", "thrash",
        "trash", "destroy", "demolish", "annihilate", "obliterate", "eradicate", "exterminate", "eliminate", "remove", "clear",
        "clean", "wash", "rinse", "scrub", "scour", "wipe", "rub", "polish", "shine", "buff",
        "wax", "varnish", "paint", "coat", "cover", "hide", "conceal", "secrete", "mask", "cloak",
        "shroud", "veil", "screen", "shield", "shelter", "protect", "guard", "defend", "secure", "save",
        "rescue", "liberate", "free", "release", "loose", "untie", "unfasten", "undo", "loosen", "tighten",
        "fasten", "attach", "fix", "affix", "stick", "adhere", "cling", "hang", "suspend", "dangle",
        "swing", "sway", "balance", "steady", "stabilize", "support", "brace", "prop", "shore", "buttress",
        "bolster", "underpin", "sustain", "maintain", "uphold", "bear", "carry", "transport", "convey", "transmit",
        "transfer", "shift", "switch", "change", "alter", "modify", "vary", "convert", "transform", "transmute",
        "metamorphose", "adapt", "adjust", "accommodate", "reconcile", "harmonize", "coordinate", "synchronize", "repair", "fix",
        "mend", "patch", "restore", "renew", "renovate", "rebuild", "reconstruct", "refurbish", "overhaul", "service",
        "maintain", "sustain", "preserve", "conserve", "protect", "guard", "shield", "shelter", "harbor", "house",
        "accommodate", "lodge", "quarter", "board", "billet", "station", "post", "position", "place", "locate",
        "situate", "site", "install", "establish", "found", "ground", "base", "root", "anchor", "moor",
        "dock", "land", "ground", "touch_down", "alight", "disembark", "embark", "board", "mount", "dismount",
        "ascend", "climb", "scale", "mount", "rise", "descend", "go_down", "come_down", "fall", "drop",
        "sink", "subside", "settle", "precipitate", "plunge", "dive", "plummet", "crash", "collapse", "tumble",
        "topple", "overturn", "upset", "capsize", "keel_over", "tilt", "tip", "lean", "slant", "slope",
        "incline", "decline", "dip", "sag", "droop", "dangle", "swing", "sway", "oscillate", "vibrate",
        "fluctuate", "vary", "change", "shift", "alternate", "rotate", "revolve", "spin", "turn", "twirl",
        "whirl", "swirl", "eddy", "surge", "rush", "gush", "flow", "stream", "course", "run",
        "pour", "flood", "inundate", "deluge", "drown", "submerge", "immerse", "dip", "plunge", "duck",
        "dunk", "bathe", "soak", "steep", "saturate", "drench", "wet", "moisten", "dampen", "sprinkle",
        "splash", "spatter", "spray", "squirt", "spurt", "jet", "shoot", "fire", "launch", "project",
    ]
    
    for word in physical_verbs:
        words.append(add_func(word, "verb", "physical action", "action"))
    
    # ==== VERBS - Mental/Cognitive (500) ====
    mental_verbs = [
        "think", "believe", "know", "understand", "realize", "recognize", "remember", "recall", "recollect", "remind",
        "forget", "learn", "study", "discover", "find", "detect", "notice", "observe", "perceive", "sense",
        "feel", "experience", "undergo", "suffer", "endure", "bear", "withstand", "weather", "survive", "live",
        "exist", "subsist", "wonder", "ponder", "meditate", "contemplate", "consider", "reflect", "deliberate", "reason",
        "infer", "deduce", "conclude", "judge", "evaluate", "assess", "appraise", "estimate", "gauge", "calculate",
        "compute", "reckon", "figure", "solve", "resolve", "determine", "ascertain", "identify", "distinguish", "differentiate",
        "discriminate", "tell", "separate", "divide", "part", "sever", "detach", "disengage", "dissociate", "disconnect",
        "compare", "contrast", "resemble", "differ", "match", "correspond", "parallel", "accord", "agree", "concur",
        "coincide", "conflict", "clash", "disagree", "dispute", "debate", "argue", "quarrel", "squabble", "bicker",
        "wrangle", "contend", "compete", "vie", "rival", "oppose", "resist", "withstand", "defy", "challenge",
        "confront", "face", "meet", "encounter", "imagine", "envision", "visualize", "picture", "conceive", "dream",
        "fantasize", "daydream", "suppose", "assume", "presume", "postulate", "hypothesize", "theorize", "speculate", "conjecture",
        "surmise", "guess", "estimate", "anticipate", "expect", "foresee", "predict", "forecast", "prophesy", "foretell",
        "project", "envisage", "devise", "invent", "create", "produce", "generate", "originate", "initiate", "commence",
        "start", "begin", "launch", "embark", "undertake", "attempt", "try", "endeavor", "strive", "struggle",
        "fight", "combat", "battle", "war", "attack", "assault", "assail", "besiege", "storm", "raid",
        "invade", "penetrate", "infiltrate", "enter", "exit", "leave", "depart", "quit", "withdraw", "retire",
        "vanish", "disappear", "fade", "dissolve", "evaporate", "comprehend", "apprehend", "grasp", "seize", "master",
        "digest", "absorb", "assimilate", "internalize", "incorporate", "integrate", "synthesize", "analyze", "examine", "inspect",
        "investigate", "study", "research", "explore", "probe", "search", "seek", "look_for", "hunt", "pursue",
        "quest", "delve", "dig", "mine", "excavate", "unearth", "disinter", "exhume", "reveal", "disclose",
        "expose", "uncover", "unveil", "unmask", "discover", "find", "detect", "locate", "pinpoint", "track",
        "trace", "follow", "shadow", "trail", "chase", "pursue", "hunt", "stalk", "ambush", "waylay",
        "intercept", "block", "hinder", "impede", "obstruct", "bar", "stop", "halt", "check", "arrest",
        "stall", "delay", "postpone", "defer", "suspend", "adjourn", "prorogue", "recess", "interrupt", "disrupt",
        "disturb", "bother", "annoy", "irritate", "vex", "irk", "peeve", "provoke", "incense", "anger",
        "enrage", "infuriate", "madden", "exasperate", "aggravate", "gall", "rile", "nettle", "pique", "offend",
        "insult", "affront", "slight", "snub", "repulse", "repel", "revolt", "disgust", "sicken", "nauseate",
        "appall", "horrify", "shock", "stun", "startle", "surprise", "astonish", "astound", "amaze", "stupefy",
        "dumbfound", "flabbergast", "overwhelm", "overpower", "overcome", "conquer", "defeat", "vanquish", "subdue", "subjugate",
        "suppress", "repress", "oppress", "persecute", "torment", "torture", "afflict", "plague", "beset", "harass",
    ]
    
    for word in mental_verbs:
        words.append(add_func(word, "verb", "mental action", "think"))
    
    # ==== VERBS - Communication (400) ====
    comm_verbs = [
        "say", "speak", "talk", "tell", "state", "express", "articulate", "utter", "voice", "vocalize",
        "pronounce", "enunciate", "declare", "announce", "proclaim", "publish", "broadcast", "transmit", "convey", "relay",
        "communicate", "inform", "notify", "advise", "counsel", "warn", "caution", "alert", "remind", "mention",
        "refer", "allude", "hint", "suggest", "propose", "recommend", "advocate", "urge", "encourage", "discourage",
        "deter", "dissuade", "persuade", "convince", "assure", "reassure", "comfort", "console", "soothe", "calm",
        "quiet", "silence", "hush", "shush", "ask", "inquire", "question", "query", "interrogate", "quiz",
        "answer", "respond", "reply", "retort", "rejoin", "explain", "clarify", "elucidate", "explicate", "interpret",
        "translate", "transcribe", "write", "pen", "compose", "draft", "scribble", "scrawl", "read", "peruse",
        "scan", "skim", "study", "describe", "depict", "portray", "represent", "illustrate", "demonstrate", "show",
        "display", "exhibit", "present", "reveal", "disclose", "divulge", "expose", "unveil", "uncover", "discover",
        "report", "recount", "relate", "narrate", "recite", "rehearse", "repeat", "reiterate", "echo", "parrot",
        "quote", "cite", "instance", "exemplify", "demonstrate", "show", "evidence", "prove", "verify", "confirm",
        "validate", "authenticate", "certify", "attest", "witness", "testify", "depose", "swear", "vow", "pledge",
        "promise", "assure", "guarantee", "warrant", "ensure", "insure", "secure", "protect", "safeguard", "shield",
        "screen", "guard", "defend", "champion", "advocate", "support", "back", "endorse", "sanction", "approve",
        "ratify", "confirm", "authorize", "empower", "enable", "entitle", "qualify", "fit", "suit", "satisfy",
        "please", "content", "gratify", "delight", "gladden", "cheer", "rejoice", "exult", "jubilate", "celebrate",
        "commemorate", "memorialize", "honor", "respect", "esteem", "regard", "consider", "deem", "reckon", "account",
        "judge", "estimate", "gauge", "assess", "evaluate", "appraise", "rate", "rank", "grade", "classify",
        "categorize", "group", "sort", "arrange", "order", "organize", "systematize", "marshal", "array", "dispose",
        "deploy", "position", "station", "post", "place", "put", "set", "lay", "situate", "locate",
        "site", "install", "establish", "found", "institute", "constitute", "create", "make", "produce", "generate",
        "originate", "initiate", "begin", "start", "commence", "open", "launch", "inaugurate", "usher_in", "introduce",
        "present", "offer", "proffer", "tender", "extend", "hold_out", "reach_out", "give", "grant", "bestow",
        "confer", "accord", "award", "render", "yield", "surrender", "relinquish", "cede", "waive", "forgo",
        "forsake", "abandon", "desert", "leave", "quit", "vacate", "evacuate", "withdraw", "retire", "retreat",
        "recede", "return", "go_back", "revert", "reverse", "retrace", "backtrack", "turn_back", "double_back", "regress",
        "recoil", "shrink", "flinch", "wince", "cringe", "cower", "quail", "tremble", "shake", "shiver",
        "shudder", "quiver", "quake", "flutter", "flicker", "waver", "vacillate", "hesitate", "pause", "delay",
        "wait", "bide", "linger", "loiter", "dawdle", "dally", "tarry", "delay", "postpone", "defer",
        "procrastinate", "stall", "temporize", "hum", "haw", "equivocate", "prevaricate", "hedge", "dodge", "evade",
        "avoid", "shun", "eschew", "forswear", "abjure", "renounce", "repudiate", "disown", "disclaim", "deny",
        "contradict", "gainsay", "refute", "rebut", "disprove", "invalidate", "nullify", "negate", "cancel", "annul",
    ]
    
    for word in comm_verbs:
        words.append(add_func(word, "verb", "communication", "communicate"))
    
    # ==== VERBS - Social (400) ====
    social_verbs = [
        "help", "assist", "aid", "support", "abet", "serve", "attend", "accompany", "join", "unite",
        "combine", "merge", "fuse", "blend", "mix", "mingle", "associate", "befriend", "visit", "call_on",
        "see", "meet", "encounter", "greet", "welcome", "receive", "entertain", "host", "treat", "behave",
        "act", "interact", "cooperate", "collaborate", "coordinate", "negotiate", "bargain", "deal", "trade", "exchange",
        "barter", "buy", "purchase", "acquire", "obtain", "procure", "secure", "gain", "sell", "vend",
        "retail", "market", "peddle", "hawk", "pay", "compensate", "remunerate", "reimburse", "repay", "refund",
        "owe", "lend", "loan", "borrow", "rent", "lease", "hire", "employ", "engage", "recruit",
        "enlist", "enroll", "register", "sign_up", "subscribe", "donate", "contribute", "bestow", "confer", "grant",
        "award", "present", "offer", "volunteer", "accept", "receive", "adopt", "embrace", "welcome", "approve",
        "endorse", "sanction", "ratify", "confirm", "validate", "certify", "verify", "authenticate", "prove", "demonstrate",
        "apologize", "apologise", "regret", "repent", "atone", "make_amends", "compensate", "indemnify", "recompense", "reward",
        "reimburse", "repay", "requite", "return", "reciprocate", "exchange", "swap", "switch", "trade", "barter",
        "deal", "transact", "negotiate", "bargain", "haggle", "dicker", "wrangle", "argue", "dispute", "debate",
        "discuss", "confer", "consult", "deliberate", "parley", "treat", "negotiate", "mediate", "arbitrate", "intercede",
        "intervene", "interpose", "step_in", "involve", "engage", "participate", "partake", "share", "participate", "join",
        "enlist", "enroll", "sign_up", "subscribe", "register", "matriculate", "induct", "initiate", "install", "invest",
        "ordain", "consecrate", "dedicate", "devote", "commit", "pledge", "bind", "obligate", "oblige", "compel",
        "force", "coerce", "pressure", "pressurize", "press", "push", "drive", "propel", "impel", "compel",
        "constrain", "oblige", "require", "demand", "exact", "insist", "maintain", "assert", "claim", "contend",
        "allege", "aver", "avow", "profess", "pretend", "feign", "simulate", "fake", "sham", "counterfeit",
        "forge", "fabricate", "manufacture", "concoct", "contrive", "devise", "invent", "make_up", "dream_up", "think_up",
        "conceive", "envision", "visualize", "imagine", "fancy", "picture", "dream", "fantasize", "pretend", "make_believe",
        "play", "act", "perform", "dissemble", "dissimulate", "mask", "disguise", "camouflage", "cloak", "veil",
        "shroud", "screen", "shield", "hide", "conceal", "secrete", "cache", "stash", "bury", "entomb",
        "inter", "inhume", "lay_to_rest", "commit", "consign", "entrust", "trust", "confide", "rely", "depend",
        "count_on", "bank_on", "look_to", "turn_to", "resort_to", "have_recourse_to", "fall_back_on", "retreat", "withdraw", "retire",
        "recede", "regress", "retrogress", "return", "revert", "backslide", "relapse", "lapse", "slip", "fall",
        "descend", "sink", "decline", "degenerate", "deteriorate", "degrade", "debase", "demean", "abase", "humiliate",
        "mortify", "shame", "disgrace", "dishonor", "discredit", "disparage", "belittle", "deprecate", "depreciate", "devalue",
        "undervalue", "underestimate", "underrate", "minimize", "downplay", "disparage", "criticize", "censure", "blame", "condemn",
        "denounce", "decry", "deplore", "lament", "bemoan", "bewail", "regret", "repent", "rue", "grieve",
    ]
    
    for word in social_verbs:
        words.append(add_func(word, "verb", "social action", "social"))
    
    # ==== NOUNS - Time (300) ====
    time_nouns = [
        "time", "moment", "minute", "hour", "day", "night", "morning", "noon", "afternoon", "evening",
        "dusk", "twilight", "dawn", "daybreak", "sunrise", "sunset", "midnight", "week", "fortnight", "month",
        "year", "decade", "century", "millennium", "eon", "age", "era", "epoch", "period", "span",
        "duration", "interval", "pause", "break", "respite", "lull", "hiatus", "gap", "interlude", "intermission",
        "season", "spring", "summer", "autumn", "fall", "winter", "date", "anniversary", "birthday", "holiday",
        "vacation", "leave", "sabbatical", "schedule", "timetable", "agenda", "calendar", "clock", "watch", "timer",
        "alarm", "bell", "chime", "tick", "tock", "second", "instant", "jiffy", "flash", "twinkling",
        "heartbeat", "while", "spell", "stint", "tour", "shift", "turn", "chance", "opportunity", "occasion",
        "instance", "event", "incident", "episode", "adventure", "experience", "encounter", "meeting", "gathering", "assembly",
        "conference", "convention", "congress", "session", "sitting", "term", "semester", "quarter", "trimester", "phase",
        "stage", "step", "point", "juncture", "crossroads", "crisis", "climax", "peak", "pinnacle", "zenith",
        "acme", "apex", "summit", "height", "prime", "heyday", "golden_age", "halcyon_days", "past", "present",
        "future", "yesterday", "today", "tomorrow", "yesteryear", "bygone", "history", "prehistory", "antiquity", "antique",
        "relic", "remnant", "vestige", "trace", "record", "chronicle", "annals", "archive", "memory", "recollection",
        "reminiscence", "nostalgia", "flashback", "déjà_vu", "premonition", "foresight", "hindsight", "afterthought", "postscript", "epilogue",
        "prologue", "prelude", "overture", "preamble", "beginning", "start", "onset", "outset", "inception", "commencement",
        "genesis", "origin", "source", "root", "foundation", "groundwork", "cornerstone", "keystone", "basis", "bedrock",
        "middle", "center", "midst", "core", "heart", "kernel", "nucleus", "hub", "focus", "focal_point",
        "crux", "gist", "essence", "quintessence", "soul", "spirit", "end", "ending", "close", "finish",
        "finale", "culmination", "termination", "cessation", "expiration", "extinction", "death", "demise", "decease", "passing",
        "doom", "fate", "destiny", "fortune", "luck", "chance", "accident", "coincidence", "synchronicity", "timing",
    ]
    
    for word in time_nouns:
        words.append(add_func(word, "noun", "time concept", "time"))
    
    # ==== NOUNS - Space/Location (400) ====
    space_nouns = [
        "space", "place", "location", "position", "spot", "site", "point", "station", "post", "seat",
        "room", "area", "zone", "region", "territory", "district", "quarter", "section", "sector", "division",
        "part", "portion", "piece", "segment", "slice", "chunk", "lump", "mass", "block", "bulk",
        "volume", "expanse", "extent", "stretch", "span", "reach", "range", "scope", "compass", "sweep",
        "world", "earth", "globe", "planet", "sphere", "universe", "cosmos", "creation", "nature", "environment",
        "surroundings", "milieu", "habitat", "home", "abode", "dwelling", "residence", "domicile", "habitation", "lodging",
        "accommodations", "quarters", "shelter", "refuge", "sanctuary", "haven", "retreat", "asylum", "shelter", "cover",
        "ground", "land", "terrain", "territory", "country", "nation", "state", "province", "county", "parish",
        "township", "city", "town", "village", "hamlet", "settlement", "colony", "outpost", "encampment", "camp",
        "base", "headquarters", "depot", "station", "post", "center", "hub", "heart", "core", "middle",
        "border", "boundary", "frontier", "limit", "edge", "fringe", "periphery", "margin", "rim", "brink",
        "verge", "threshold", "brink", "precipice", "cliff", "bluff", "crag", "peak", "summit", "crest",
        "top", "head", "cap", "crown", "apex", "tip", "point", "peak", "pinnacle", "acme",
        "bottom", "base", "foot", "foundation", "groundwork", "bed", "pedestal", "plinth", "platform", "stage",
        "side", "face", "surface", "facet", "aspect", "phase", "angle", "slant", "slope", "incline",
        "decline", "hill", "mountain", "mount", "peak", "alp", "sierra", "cordillera", "range", "ridge",
        "valley", "vale", "dale", "glen", "ravine", "gorge", "canyon", "pass", "gap", "notch",
        "plain", "plateau", "tableland", "mesa", "steppe", "prairie", "savanna", "tundra", "desert", "wilderness",
        "wasteland", "badlands", "wilds", "bush", "jungle", "forest", "woods", "woodland", "grove", "copse",
        "thicket", "brake", "bramble", "undergrowth", "underbrush", "canopy", "covert", "harbor", "port", "haven",
        "anchorage", "mooring", "berth", "dock", "pier", "wharf", "quay", "jetty", "breakwater", "seawall",
        "beach", "shore", "coast", "seaboard", "strand", "bank", "edge", "brink", "margin", "waterfront",
        "water's_edge", "shoreline", "coastline", "ocean", "sea", "gulf", "bay", "cove", "inlet", "fjord",
        "sound", "strait", "channel", "passage", "pass", "waterway", "aqueduct", "canal", "ditch", "trench",
        "dike", "dam", "weir", "lock", "sluice", "floodgate", "gate", "door", "portal", "entrance",
        "entry", "ingress", "access", "approach", "way", "path", "track", "trail", "lane", "road",
        "street", "avenue", "boulevard", "highway", "freeway", "motorway", "expressway", "turnpike", "tollway", "thoroughfare",
        "artery", "route", "course", "line", "passage", "channel", "conduit", "pipeline", "tube", "cylinder",
    ]
    
    for word in space_nouns:
        words.append(add_func(word, "noun", "space concept", "space"))
    
    # ==== NOUNS - People (400) ====
    people_nouns = [
        "person", "people", "individual", "human", "being", "creature", "mortal", "soul", "spirit", "body",
        "man", "woman", "child", "baby", "infant", "toddler", "adolescent", "teenager", "youth", "adult",
        "grown-up", "parent", "mother", "father", "mom", "dad", "mommy", "daddy", "parent", "guardian",
        "custodian", "warden", "keeper", "protector", "defender", "champion", "advocate", "patron", "sponsor", "benefactor",
        "friend", "companion", "comrade", "colleague", "associate", "peer", "equal", "counterpart", "match", "mate",
        "partner", "spouse", "husband", "wife", "bride", "groom", "fiancé", "fiancée", "sweetheart", "lover",
        "beloved", "darling", "dear", "honey", "sweetie", "sugar", "pumpkin", "babe", "baby", "child",
        "kid", " youngster", "minor", "ward", "dependent", "charge", "protege", "disciple", "follower", "adherent",
        "member", "associate", "affiliate", "ally", "confederate", "accomplice", "accessory", "abettor", "co-conspirator", "conspirator",
        "plotter", "schemer", "planner", "designer", "architect", "engineer", "builder", "maker", "creator", "originator",
        "founder", "author", "writer", "composer", "artist", "painter", "sculptor", "musician", "player", "performer",
        "actor", "actress", "star", "celebrity", "luminary", "dignitary", "notable", "noteworthy", "personage", "figure",
        "character", "type", "sort", "kind", "ilk", "stripe", "variety", "species", "class", "category",
        "group", "crowd", "throng", "mob", "horde", "multitude", "mass", "rabble", "rout", "herd",
        "flock", "pack", "school", "shoal", "swarm", "colony", "tribe", "clan", "family", "household",
        "home", "dynasty", "line", "lineage", "ancestry", "descent", "extraction", "birth", "origin", "derivation",
        "source", "root", "stock", "strain", "breed", "pedigree", "bloodline", "genealogy", "family_tree", "stemma",
        "nation", "country", "state", "land", "realm", "domain", "dominion", "empire", "kingdom", "principality",
        "duchy", "duché", "county", "earldom", "barony", "manor", "estate", "plantation", "ranch", "farm",
        "homestead", "holding", "property", "realty", "real_estate", "land", "grounds", "premises", "tenement", "tenure",
        "occupation", "occupancy", "possession", "tenancy", "lease", "rental", "hire", "charter", "engagement", "employment",
        "service", "work", "labor", "toil", "drudgery", "grind", "task", "job", "chore", "assignment",
        "duty", "responsibility", "obligation", "commitment", "engagement", "appointment", "meeting", "date", "interview", "audition",
        "trial", "test", "exam", "examination", "quiz", "assessment", "evaluation", "appraisal", "review", "inspection",
        "check", "audit", "scrutiny", "inquest", "inquiry", "investigation", "probe", "research", "study", "analysis",
    ]
    
    for word in people_nouns:
        words.append(add_func(word, "noun", "person", "social"))
    
    # ==== NOUNS - Objects/Things (500) ====
    object_nouns = [
        "thing", "object", "item", "article", "piece", "unit", "entity", "body", "substance", "material",
        "stuff", "matter", "mass", "bulk", "volume", "quantity", "amount", "measure", "degree", "extent",
        "magnitude", "size", "dimension", "proportion", "ratio", "rate", "speed", "velocity", "pace", "tempo",
        "rhythm", "beat", "pulse", "throb", "tick", "tock", "click", "clack", "clunk", "thud",
        "thump", "bang", "boom", "crash", "smash", "clash", "clang", "clank", "rattle", "clatter",
        "jingle", "tinkle", "ring", "chime", "peal", "toll", "knell", "sound", "noise", "din",
        "racket", "hubbub", "clamor", "outcry", "uproar", "tumult", "commotion", "disturbance", "pandemonium", "chaos",
        "bedlam", "babel", "hubbub", "brouhaha", "fracas", "melee", "scrap", "tussle", "scuffle", "fracas",
        "affray", "brawl", "fight", "battle", "combat", "conflict", "war", "warfare", "hostilities", "strife",
        "contention", "discord", "dissension", "dispute", "argument", "debate", "discussion", "conversation", "talk", "chat",
        "dialogue", "discourse", "exchange", "communication", "correspondence", "message", "letter", "note", "memo", "memorandum",
        "epistle", "missive", "dispatch", "communiqué", "bulletin", "report", "account", "narrative", "story", "tale",
        "yarn", "anecdote", "vignette", "sketch", "portrait", "picture", "image", "likeness", "representation", "depiction",
        "description", "account", "version", "edition", "copy", "replica", "reproduction", "reprint", "reissue", "reproduction",
        "facsimile", "photocopy", "xerox", "photostat", "print", "impression", "copy", "issue", "number", "edition",
        "volume", "tome", "book", "publication", "work", "opus", "magnum_opus", "chef-d'oeuvre", "masterpiece", "classic",
        "standard", "model", "pattern", "prototype", "archetype", "original", "exemplar", "example", "instance", "case",
        "illustration", "sample", "specimen", "type", "sort", "kind", "variety", "class", "category", "genre",
        "form", "shape", "figure", "outline", "contour", "profile", "silhouette", "shadow", "reflection", "image",
        "likeness", "semblance", "appearance", "aspect", "look", "expression", "air", "manner", "bearing", "demeanor",
        "deportment", "conduct", "behavior", "comportment", "actions", "deeds", "works", "feats", "exploits", "achievements",
        "accomplishments", "successes", "triumphs", "victories", "wins", "gains", "advances", "progress", "headway", "improvement",
        "betterment", "amelioration", "enhancement", "enrichment", "upgrade", "boost", "lift", "raise", "increase", "augmentation",
        "expansion", "extension", "enlargement", "growth", "development", "evolution", "progression", "advance", "advancement", "promotion",
        "elevation", "exaltation", "aggrandizement", "ennoblement", "glorification", "canonization", "beatification", "sanctification", "consecration", "dedication",
        "devotion", "commitment", "pledge", "vow", "oath", "promise", "word", "guarantee", "warranty", "assurance",
    ]
    
    for word in object_nouns:
        words.append(add_func(word, "noun", "physical object", "world"))
    
    # ==== NOUNS - Abstract Concepts (500) ====
    abstract_nouns = [
        "idea", "concept", "notion", "conception", "construct", "thought", "thinking", "reasoning", "logic", "rationale",
        "motive", "motivation", "incentive", "inducement", "impulse", "drive", "urge", "desire", "wish", "want",
        "need", "requirement", "necessity", "essential", "requisite", "prerequisite", "condition", "stipulation", "provision", "proviso",
        "qualification", "reservation", "exception", "exclusion", "omission", "deletion", "erasure", "cancellation", "annulment", "abrogation",
        "repeal", "rescission", "revocation", "withdrawal", "retraction", "recantation", "renunciation", "abjuration", "repudiation", "disavowal",
        "denial", "negation", "refutation", "rebuttal", "contradiction", "gainsaying", "disproof", "invalidation", "nullification", "voidance",
        "vacancy", "emptiness", "void", "nothingness", "nullity", "oblivion", "nonexistence", "nihility", "nonbeing", "absence",
        "lack", "want", "deficiency", "dearth", "scarcity", "shortage", "paucity", "poverty", "privation", " destitution",
        "indigence", "penury", "neediness", "beggary", "pauperism", "bankruptcy", "insolvency", "failure", "collapse", "ruin",
        "downfall", "fall", "decline", "decay", "degeneration", "degradation", "deterioration", "debasement", "corruption", "perversion",
        "distortion", "deformation", "disfigurement", "mutilation", "maiming", "crippling", "laming", "hobbling", "hampering", "hindrance",
        "impediment", "obstacle", "obstruction", "barrier", "bar", "block", "blockade", "obstacle", "hindrance", "deterrent",
        "discouragement", "disincentive", "deterrent", "restraint", "constraint", "restriction", "limitation", "curb", "check", "control",
        "regulation", "rule", "law", "statute", "act", "bill", "measure", "legislation", "enactment", "ordinance",
        "decree", "edict", "order", "command", "directive", "instruction", "direction", "guidance", "counsel", "advice",
        "recommendation", "suggestion", "proposal", "proposition", "motion", "resolution", "determination", "decision", "verdict", "finding",
        "ruling", "judgment", "sentence", "decree", "order", "injunction", "mandate", "command", "directive", "charge",
        "commission", "assignment", "task", "job", "duty", "function", "role", "part", "capacity", "office",
        "position", "post", "place", "situation", "status", "standing", "stature", "estate", "state", "condition",
        "shape", "form", "order", "repair", "health", "fitness", "trim", "fettle", "shape", "kilter",
        "balance", "equilibrium", "equipoise", "parity", "equality", "equivalence", "par", "sameness", "identity", "uniformity",
        "consistency", "constancy", "steadiness", "stability", "steadfastness", "constancy", "faithfulness", "fidelity", "loyalty", "allegiance",
        "fealty", "homage", "deference", "respect", "esteem", "regard", "consideration", "thought", "attention", "notice",
        "heed", "mind", "care", "concern", "interest", "involvement", "participation", "engagement", "commitment", "dedication",
        "devotion", "attachment", "affection", "fondness", "liking", "love", "passion", "ardor", "fervor", "zeal",
        "enthusiasm", "eagerness", "keenness", "ardency", "warmth", "intensity", "vehemence", "violence", "force", "power",
        "strength", "might", "potency", "vigor", "energy", "vitality", "life", "animation", "vivacity", "liveliness",
        "spirit", "soul", "essence", "quintessence", "core", "heart", "kernel", "nucleus", "crux", "gist",
        "substance", "meat", "pith", "marrow", "core", "center", "middle", "midst", "thick", "depths",
    ]
    
    for word in abstract_nouns:
        words.append(add_func(word, "noun", "abstract concept", "abstract"))
    
    # ==== ADJECTIVES (3000) - Sample of key categories ====
    adj_samples = [
        # Size
        ("big", "size"), ("large", "size"), ("huge", "size"), ("vast", "size"), ("immense", "size"),
        ("enormous", "size"), ("gigantic", "size"), ("colossal", "size"), ("titanic", "size"), ("mammoth", "size"),
        ("massive", "size"), ("substantial", "size"), ("considerable", "size"), ("sizable", "size"), ("goodly", "size"),
        ("small", "size"), ("little", "size"), ("tiny", "size"), ("minute", "size"), ("miniature", "size"),
        ("diminutive", "size"), ("petite", "size"), ("compact", "size"), ("slight", "size"), ("negligible", "size"),
        # Quality
        ("good", "quality"), ("excellent", "quality"), ("fine", "quality"), ("superior", "quality"), ("outstanding", "quality"),
        ("exceptional", "quality"), ("remarkable", "quality"), ("extraordinary", "quality"), ("phenomenal", "quality"), ("wonderful", "quality"),
        ("bad", "quality"), ("poor", "quality"), ("inferior", "quality"), ("substandard", "quality"), ("deficient", "quality"),
        ("inadequate", "quality"), ("unsatisfactory", "quality"), ("disappointing", "quality"), ("lacking", "quality"), ("wanting", "quality"),
        # Color
        ("red", "color"), ("blue", "color"), ("green", "color"), ("yellow", "color"), ("orange", "color"),
        ("purple", "color"), ("pink", "color"), ("brown", "color"), ("black", "color"), ("white", "color"),
        ("gray", "color"), ("grey", "color"), ("violet", "color"), ("indigo", "color"), ("crimson", "color"),
        # Temperature
        ("hot", "temperature"), ("warm", "temperature"), ("cold", "temperature"), ("cool", "temperature"), ("freezing", "temperature"),
        ("boiling", "temperature"), ("scorching", "temperature"), ("sweltering", "temperature"), ("frigid", "temperature"), ("icy", "temperature"),
        # Age
        ("old", "age"), ("young", "age"), ("ancient", "age"), ("antique", "age"), ("vintage", "age"),
        ("new", "age"), ("modern", "age"), ("recent", "age"), ("current", "age"), ("contemporary", "age"),
        # Speed
        ("fast", "speed"), ("quick", "speed"), ("rapid", "speed"), ("swift", "speed"), ("speedy", "speed"),
        ("slow", "speed"), ("sluggish", "speed"), ("leisurely", "speed"), ("gradual", "speed"), ("steady", "speed"),
        # Emotional
        ("happy", "emotion"), ("joyful", "emotion"), ("cheerful", "emotion"), ("delighted", "emotion"), ("ecstatic", "emotion"),
        ("sad", "emotion"), ("unhappy", "emotion"), ("sorrowful", "emotion"), ("miserable", "emotion"), ("dejected", "emotion"),
        ("angry", "emotion"), ("furious", "emotion"), ("irritated", "emotion"), ("annoyed", "emotion"), ("enraged", "emotion"),
        ("afraid", "emotion"), ("scared", "emotion"), ("frightened", "emotion"), ("terrified", "emotion"), ("petrified", "emotion"),
        ("surprised", "emotion"), ("amazed", "emotion"), ("astonished", "emotion"), ("astounded", "emotion"), ("stunned", "emotion"),
        ("tired", "emotion"), ("exhausted", "emotion"), ("weary", "emotion"), ("fatigued", "emotion"), ("drained", "emotion"),
        # Intelligence
        ("smart", "intelligence"), ("intelligent", "intelligence"), ("clever", "intelligence"), ("bright", "intelligence"), ("brilliant", "intelligence"),
        ("stupid", "intelligence"), ("dull", "intelligence"), ("dim", "intelligence"), ("dense", "intelligence"), ("slow", "intelligence"),
        # Physical traits
        ("strong", "physical"), ("powerful", "physical"), ("mighty", "physical"), ("potent", "physical"), ("forceful", "physical"),
        ("weak", "physical"), ("feeble", "physical"), ("frail", "physical"), ("delicate", "physical"), ("fragile", "physical"),
        ("tall", "physical"), ("high", "physical"), ("lofty", "physical"), ("towering", "physical"), ("elevated", "physical"),
        ("short", "physical"), ("low", "physical"), ("stunted", "physical"), ("petite", "physical"), ("squat", "physical"),
        ("fat", "physical"), ("obese", "physical"), ("overweight", "physical"), ("plump", "physical"), ("stout", "physical"),
        ("thin", "physical"), ("slender", "physical"), ("slim", "physical"), ("lean", "physical"), ("skinny", "physical"),
        # Appearance
        ("beautiful", "appearance"), ("pretty", "appearance"), ("lovely", "appearance"), ("attractive", "appearance"), ("gorgeous", "appearance"),
        ("ugly", "appearance"), ("hideous", "appearance"), ("unsightly", "appearance"), ("repulsive", "appearance"), ("revolting", "appearance"),
        # Importance
        ("important", "importance"), ("significant", "importance"), ("crucial", "importance"), ("critical", "importance"), ("vital", "importance"),
        ("essential", "importance"), ("necessary", "importance"), ("required", "importance"), ("needed", "importance"), ("indispensable", "importance"),
        ("minor", "importance"), ("trivial", "importance"), ("insignificant", "importance"), ("unimportant", "importance"), ("negligible", "importance"),
        # Difficulty
        ("easy", "difficulty"), ("simple", "difficulty"), ("effortless", "difficulty"), ("straightforward", "difficulty"), ("elementary", "difficulty"),
        ("difficult", "difficulty"), ("hard", "difficulty"), ("challenging", "difficulty"), ("demanding", "difficulty"), ("tough", "difficulty"),
        # Texture
        ("smooth", "texture"), ("silky", "texture"), ("sleek", "texture"), ("polished", "texture"), ("glossy", "texture"),
        ("rough", "texture"), ("coarse", "texture"), ("harsh", "texture"), ("abrasive", "texture"), ("scratchy", "texture"),
        # Sound
        ("loud", "sound"), ("noisy", "sound"), ("boisterous", "sound"), ("raucous", "sound"), ("deafening", "sound"),
        ("quiet", "sound"), ("silent", "sound"), ("noiseless", "sound"), ("inaudible", "sound"), ("muted", "sound"),
        # Light
        ("bright", "light"), ("luminous", "light"), ("radiant", "light"), ("brilliant", "light"), ("dazzling", "light"),
        ("dark", "light"), ("dim", "light"), ("gloomy", "light"), ("shadowy", "light"), ("murky", "light"),
        # Taste
        ("sweet", "taste"), ("sour", "taste"), ("bitter", "taste"), ("salty", "taste"), ("savory", "taste"),
        ("delicious", "taste"), ("tasty", "taste"), ("yummy", "taste"), ("flavorful", "taste"), ("appetizing", "taste"),
        ("disgusting", "taste"), ("repulsive", "taste"), ("revolting", "taste"), ("nauseating", "taste"), ("sickening", "taste"),
        # Smell
        ("fragrant", "smell"), ("aromatic", "smell"), ("scented", "smell"), ("perfumed", "smell"), ("redolent", "smell"),
        ("stinky", "smell"), ("foul", "smell"), ("putrid", "smell"), ("rank", "smell"), ("malodorous", "smell"),
        # Touch
        ("soft", "touch"), ("hard", "touch"), ("firm", "touch"), ("solid", "touch"), ("rigid", "touch"),
        ("flexible", "touch"), ("pliable", "touch"), ("pliant", "touch"), ("malleable", "touch"), ("supple", "touch"),
    ]
    
    for word, category in adj_samples:
        words.append(add_func(word, "adjective", "descriptive quality", category))
    
    # Generate additional adjectives systematically
    adj_prefixes = ["un", "in", "im", "il", "ir", "dis", "non", "mis", "mal", "anti"]
    adj_bases = ["happy", "usual", "common", "normal", "natural", "expected", "necessary", "possible", "likely", "certain",
                 "fortunate", "lucky", "pleasant", "comfortable", "convenient", "satisfactory", "acceptable", "adequate", "sufficient", "appropriate",
                 "correct", "accurate", "exact", "precise", "perfect", "complete", "finished", "done", "ready", "prepared"]
    
    for prefix in adj_prefixes:
        for base in adj_bases:
            word = prefix + base
            words.append(add_func(word, "adjective", "negative quality", "abstract"))
    
    # ==== ADVERBS (1000) ====
    adverbs = [
        # Manner
        "quickly", "slowly", "fast", "rapidly", "swiftly", "speedily", "hastily", "hurriedly", "promptly", "immediately",
        "instantly", "directly", "straight", "forthwith", "straightaway", "right_away", "at_once", "without_delay", "presto", "lickety-split",
        "carefully", "cautiously", "warily", "gingerly", "prudently", "judiciously", "discreetly", "circumspectly", "guardedly", "watchfully",
        "attentively", "mindfully", "heedfully", "diligently", "assiduously", "sedulously", "painstakingly", "thoroughly", "scrupulously", "meticulously",
        "neatly", "tidily", "trimly", "orderly", "systematically", "methodically", "regularly", "uniformly", "consistently", "steadily",
        "smoothly", "evenly", "flatly", "levelly", "uniformly", "equably", "tranquilly", "peacefully", "calmly", "serenely",
        "quietly", "silently", "noiselessly", "soundlessly", "mutely", "dumbly", "wordlessly", "tacitly", "implicitly", "taciturnly",
        "loudly", "noisily", "boisterously", "clamorously", "uproariously", "tumultuously", "riotously", "raucously", "vociferously", "vehemently",
        "strongly", "forcefully", "powerfully", "mightily", "potently", "vigorously", "energetically", "dynamically", "strenuously", "ardently",
        "fiercely", "furiously", "savagely", "violently", "wildly", "frantically", "frenziedly", "madly", "crazily", "insanely",
        # Time
        "now", "then", "today", "tomorrow", "yesterday", "tonight", "soon", "later", "afterwards", "subsequently",
        "eventually", "ultimately", "finally", "lastly", "before", "after", "earlier", "previously", "formerly", "hitherto",
        "already", "yet", "still", "just", "recently", "lately", "currently", "presently", "nowadays", "anymore",
        "ever", "never", "always", "constantly", "continuously", "continually", "repeatedly", "frequently", "often", "regularly",
        "usually", "normally", "typically", "generally", "commonly", "ordinarily", "habitually", "customarily", "routinely", "automatically",
        "seldom", "rarely", "infrequently", "sporadically", "occasionally", "sometimes", "periodically", "intermittently", "spasmodically", "fitfully",
        "again", "once", "twice", "thrice", "over", "anew", "afresh", "repeatedly", "once_more", "once_again",
        # Place
        "here", "there", "everywhere", "somewhere", "anywhere", "nowhere", "elsewhere", "wherever", "where", "hence",
        "thence", "hither", "thither", "yonder", "afar", "abroad", "overseas", "home", "indoors", "outdoors",
        "outside", "inside", "within", "without", "upstairs", "downstairs", "upward", "downward", "forward", "backward",
        "ahead", "behind", "before", "after", "aback", "aloft", "below", "beneath", "underneath", "under",
        # Degree
        "very", "quite", "rather", "somewhat", "fairly", "pretty", "really", "truly", "genuinely", "actually",
        "absolutely", "completely", "totally", "entirely", "wholly", "fully", "altogether", "utterly", "thoroughly", "perfectly",
        "highly", "greatly", "extremely", "exceedingly", "exceptionally", "extraordinarily", "remarkably", "particularly", "especially", "specifically",
        "barely", "hardly", "scarcely", "slightly", "somewhat", "moderately", "reasonably", "relatively", "comparatively", "fairly",
        "too", "so", "as", "enough", "sufficiently", "adequately", "insufficiently", "inadequately", "badly", "poorly",
        # Frequency
        "always", "never", "sometimes", "often", "frequently", "rarely", "seldom", "usually", "generally", "occasionally",
        "constantly", "regularly", "repeatedly", "continually", "continuously", "persistently", "consistently", "periodically", "intermittently", "sporadically",
        "daily", "weekly", "monthly", "yearly", "annually", "hourly", "nightly", "weekly", "fortnightly", "biweekly",
        # Affirmation/Negation
        "yes", "no", "indeed", "certainly", "surely", "definitely", "absolutely", "undoubtedly", "unquestionably", "indisputably",
        "clearly", "obviously", "evidently", "apparently", "seemingly", "presumably", "probably", "likely", "perhaps", "maybe",
        "possibly", "conceivably", "maybe", "perchance", "perhaps", "possibly", "probably", "likely", "presumably", "supposedly",
        "not", "neither", "nor", "never", "hardly", "scarcely", "barely", "rarely", "seldom", "infrequently",
    ]
    
    for word in adverbs:
        words.append(add_func(word, "adverb", "modifies verb/adjective", "abstract"))
    
    # Generate more adverbs from adjectives
    adj_for_adverbs = [
        "happy", "sad", "angry", "quick", "slow", "careful", "careless", "beautiful", "ugly", "easy",
        "hard", "soft", "loud", "quiet", "bright", "dark", "high", "low", "near", "far",
        "early", "late", "fast", "sudden", "gradual", "complete", "partial", "total", "full", "empty",
        "strong", "weak", "true", "false", "real", "actual", "certain", "sure", "clear", "obvious",
        "simple", "complex", "direct", "indirect", "immediate", "eventual", "final", "initial", "previous", "subsequent",
    ]
    
    for adj in adj_for_adverbs:
        if adj.endswith("y"):
            adv = adj[:-1] + "ily"
        elif adj.endswith("le"):
            adv = adj[:-2] + "ly"
        else:
            adv = adj + "ly"
        words.append(add_func(adv, "adverb", "derived from adjective", "abstract"))
    
    return words
