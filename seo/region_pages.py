#!/usr/bin/env python3
"""
PSDepot regional landing pages.
5 unique, substantial geo hubs: Northwest, West, Midwest, South, East Coast.
Each page is hand-authored (distinct copy, structure, emphasis) sharing only
the site shell (header/nav/footer/style). Replaces the ~150 thin per-state/
per-city doorway pages.

State -> region map (all 50 states + DC):
  NW    : AK WA OR ID MT WY
  West  : CA NV AZ UT CO NM HI
  Midwest: ND SD NE KS MN IA MO WI IL MI IN OH
  South : TX OK AR LA MS AL TN KY GA FL SC NC VA WV
  East  : ME NH VT MA RI CT NY PA NJ DE MD DC
"""

import os

PHONE = "(888) 881-6834"

SHELL_HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{meta}">
<link rel="canonical" href="https://psdepot.com/{slug}.html">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{meta}">
<meta property="og:image" content="https://psdepot.com/assets/images/og-image.png">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
:root{{--primary:#0A1A2F;--accent:#FF7A00;--bg:#F8F9FA;--text:#111}}
body{{font-family:'Inter',sans-serif;background:var(--bg);color:var(--text);line-height:1.6}}
.header{{background:var(--primary);color:#fff;padding:14px 0}}
.header-inner{{max-width:1200px;margin:0 auto;padding:0 24px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px}}
.logo{{font-size:23px;font-weight:800;color:#fff;text-decoration:none}}
.logo span{{color:#63b3ed}}
.nav{{background:#12283f;border-bottom:3px solid var(--accent)}}
.nav-inner{{max-width:1200px;margin:0 auto;padding:0 24px;display:flex;gap:4px;flex-wrap:wrap}}
.nav a{{color:#bee3f8;text-decoration:none;font-weight:600;font-size:15px;padding:12px 18px}}
.hero{{background:{hero_bg};color:#fff;padding:80px 24px;text-align:center}}
.hero h1{{font-size:44px;font-weight:800;margin-bottom:16px}}
.hero .tag{{font-size:18px;opacity:.9;max-width:700px;margin:0 auto 20px}}
.sec{{padding:56px 24px;max-width:1100px;margin:0 auto}}
.sec h2{{font-size:30px;color:var(--primary);margin-bottom:20px;text-align:center}}
.states{{display:flex;flex-wrap:wrap;gap:10px;justify-content:center}}
.state{{background:#fff;border:1px solid #e2e8f0;border-radius:10px;padding:10px 18px;font-weight:600;color:var(--primary)}}
.metro{{background:var(--primary);color:#fff;padding:8px 18px;border-radius:20px;font-size:14px}}
.cols{{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}}
.card{{background:#fff;border-radius:12px;padding:28px;border:1px solid #e2e8f0}}
.card h3{{color:var(--primary);margin-bottom:10px}}
.cta{{background:var(--accent);color:#fff;padding:56px 24px;text-align:center}}
.cta a{{display:inline-block;background:#fff;color:var(--primary);padding:16px 32px;border-radius:8px;font-weight:700;text-decoration:none;margin-top:16px}}
footer{{background:var(--primary);color:#fff;padding:28px 24px;text-align:center;font-size:14px}}
@media(max-width:768px){{.hero h1{{font-size:28px}}.cols{{grid-template-columns:1fr}}}}
</style>
</head>
<body>
<header class="header"><div class="header-inner"><a href="/" class="logo">Performance<span>Supply</span>Depot</a><div style="display:flex;gap:20px;flex-wrap:wrap;align-items:center;font-size:14px"><a href="tel:888-881-6834" style="color:#fff;text-decoration:none;font-weight:700">📞 (888) 881-6834</a><a href="tel:415-571-9724" style="color:#bee3f8;text-decoration:none">📞 (415) 571-9724</a><a href="mailto:info@psdepot.com" style="color:#bee3f8;text-decoration:none">✉️ info@psdepot.com</a><a href="/checkout.html" style="background:#c53030;color:#fff;padding:8px 16px;border-radius:20px;font-weight:600;text-decoration:none">🛒 Cart</a></div></div></header>
<nav class="nav"><div class="nav-inner"><a href="/">Home</a><a href="/products/index.html">Products</a><a href="/blog/index.html">Blog</a><a href="/services.html">Services</a><a href="/testimonials.html">Testimonials</a><a href="/about.html">About</a><a href="/resources/faq.html">FAQ</a><a href="/contact.html">Contact</a><a href="/locations.html">Service Areas</a></div></nav>
"""

SHELL_FOOT = """
<section class="cta"><h2 style="font-size:36px;margin-bottom:12px">{cta_head}</h2><p style="font-size:19px;max-width:600px;margin:0 auto">{cta_body}</p><a href="tel:888-881-6834">📞 Call {phone}</a></section>
<footer><div style="max-width:900px;margin:0 auto"><p style="margin:0 0 10px;font-size:16px"><strong>Performance Supply Depot LLC</strong></p><p style="margin:0 0 6px">📞 <a href="tel:888-881-6834" style="color:#fff;text-decoration:none;font-weight:700">(888) 881-6834</a> | 📞 <a href="tel:415-571-9724" style="color:#bee3f8;text-decoration:none">(415) 571-9724</a> | ✉️ <a href="mailto:info@psdepot.com" style="color:#bee3f8;text-decoration:none">info@psdepot.com</a></p><p style="margin:0 0 6px;color:#94a3b8;font-size:13px">Authorized Dealer: <strong>SAM4S</strong> · <strong>CAS</strong> · <strong>ACM Technologies</strong> · <strong>TST Impresso</strong> · <strong>Capton</strong></p><p style="margin:0;color:#64748b;font-size:12px">© 2026 Performance Supply Depot LLC. All rights reserved.</p></div></footer>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"LocalBusiness","name":"Performance Supply Depot - {region_name}","url":"https://psdepot.com/{slug}.html","telephone":"+1-888-881-6834","areaServed":{schema_states}}}</script>
</body></html>
"""


def states_chips(states):
    return "".join(f'<span class="state">{s}</span>' for s in states)


def metros_chips(metros):
    return "".join(f'<span class="metro">{m}</span>' for m in metros)


REGIONS = [
    {
        "slug": "northwest",
        "region_name": "Northwest",
        "title": "POS Supplies in the Northwest | Thermal Paper & Receipt Paper",
        "meta": "Fast shipping of thermal paper, receipt paper, and printer ribbons across the Pacific Northwest and Mountain states — WA, OR, ID, MT, WY, AK. Call (888) 881-6834.",
        "hero_bg": "linear-gradient(135deg,#0f4c5c,#1a936f,#114b5f)",
        "hero_h1": "POS Supplies for the Northwest",
        "hero_tag": "From Seattle's tech towers to Boise's food scene and Anchorage's port — reliable thermal paper, receipt rolls, and ribbons delivered fast.",
        "states": ["Washington", "Oregon", "Idaho", "Montana", "Wyoming", "Alaska"],
        "metros": ["Seattle", "Portland", "Boise", "Spokane", "Anchorage", "Billings", "Missoula", "Cheyenne", "Casper", "Eugene", "Tacoma", "Coeur d'Alene"],
        "intro": (
            "The Northwest runs on a mix of heavy-hitting tech, aerospace, timber, agriculture, and tourism. "
            "Seattle anchors one of the country's largest cloud and retail economies; Portland pairs a booming food-and-beverage scene "
            "with logistics and manufacturing; Boise has become a fast-growing tech and outdoor hub; and Alaska's remote operators need "
            "supply that actually arrives. Every one of those businesses shares one need: checkout hardware that never stops."
        ),
        "cards": [
            ("Built for Remote Logistics", "Alaska, Montana, and Wyoming order volume may be smaller, but the stakes are higher — an outage in a remote store means a long wait for a resupply. We plan freight that survives the distance."),
            ("Tech-Forward Retail", "From Seattle coffee shops to Portland food carts, the Northwest's retail is high-turnover. Our 3 1/8\" thermal paper and 2 1/4\" credit-card rolls keep up with the pace."),
            ("Hospitality & Tourism", "Ski towns, national parks, and coastal resorts cycle through receipts fast. Volume discounts keep seasonal operators profitable."),
        ],
        "cta_head": "Northwest-Ready Supply",
        "cta_body": "From Puget Sound to the Last Frontier, we ship POS supplies to every corner of the Northwest — free nationwide delivery.",
    },
    {
        "slug": "west",
        "region_name": "Western States",
        "title": "POS Supplies in the Western States | Thermal Paper, Ribbons & More",
        "meta": "Thermal paper rolls, receipt paper, and printer ribbons shipped fast across CA, NV, AZ, UT, CO, NM, and HI. Volume discounts available. Call (888) 881-6834.",
        "hero_bg": "linear-gradient(135deg,#7f1d1d,#f97316,#7c2d12)",
        "hero_h1": "POS Supplies for the Western States",
        "hero_tag": "The West is the engine of the American economy — Silicon Valley, Hollywood, the Port of L.A., and the Vegas Strip all transact around the clock.",
        "states": ["California", "Nevada", "Arizona", "Utah", "Colorado", "New Mexico", "Hawaii"],
        "metros": ["Los Angeles", "San Francisco", "San Diego", "Las Vegas", "Phoenix", "Denver", "Salt Lake City", "Albuquerque", "Honolulu", "Sacramento", "Tucson", "Reno"],
        "intro": (
            "The Western States are where the country's largest transaction volume lives. California alone is the fifth-largest economy on Earth, "
            "anchored by tech, entertainment, agriculture, and the busiest container port in the hemisphere. Nevada's Las Vegas never closes; "
            "Arizona and Utah are among the fastest-growing metros in the nation; Colorado's aerospace and outdoor economies boom; and Hawaii's "
            "tourism keeps every register on the islands running daily. High volume demands a supply partner with the scale to keep up."
        ),
        "cards": [
            ("Scale for High Volume", "California and Arizona order in bulk. Multi-location restaurant groups, grocers, and big-box retailers rely on our volume discounts and consolidated billing."),
            ("24/7 Hospitality", "Las Vegas and Hawaii never power down. Emergency and expedited shipping keeps casino floors, resorts, and food-service lines printing."),
            ("Cross-Border Ready", "From the Port of L.A. to the Mexico border, the West's trade economy runs on dependable thermal rolls, labels, and ribbons."),
        ],
        "cta_head": "Built for the West's Volume",
        "cta_body": "From the Pacific Coast to the Rockies, we keep the Western States' registers rolling — with free nationwide delivery.",
    },
    {
        "slug": "midwest",
        "region_name": "Midwest",
        "title": "POS Supplies in the Midwest | Thermal Paper & Printer Ribbons",
        "meta": "Reliable delivery of thermal paper, receipt paper, and printer ribbons across the Midwest — 12 states, from Chicago to Kansas City. Call (888) 881-6834.",
        "hero_bg": "linear-gradient(135deg,#1e3a8a,#2563eb,#172554)",
        "hero_h1": "POS Supplies for the Midwest",
        "hero_tag": "America's industrial and agricultural heartland — manufacturing, automotive, and logistics that demand dependable, no-nonsense supply.",
        "states": ["North Dakota", "South Dakota", "Nebraska", "Kansas", "Minnesota", "Iowa", "Missouri", "Wisconsin", "Illinois", "Michigan", "Indiana", "Ohio"],
        "metros": ["Chicago", "Detroit", "Minneapolis", "St. Louis", "Kansas City", "Cleveland", "Columbus", "Indianapolis", "Milwaukee", "Omaha", "Des Moines", "Grand Rapids"],
        "intro": (
            "The Midwest is the country's workhorse. Chicago is a global logistics and finance hub; Detroit anchors automotive manufacturing; "
            "the Twin Cities host retail and healthcare giants; and the farm belt from Iowa to Kansas keeps the nation fed and fueled. "
            "This is a region that values reliability over flash — and that's exactly what Performance Supply Depot delivers. When a "
            "manufacturing floor or a grain-elevator co-op runs low on receipt paper, there's no room for guesswork."
        ),
        "cards": [
            ("Manufacturing & Industrial", "B2B distributors, plant floors, and warehouse operators need impact paper, ribbons, and thermal rolls in bulk — shipped on a schedule that never slips."),
            ("Agriculture & Co-ops", "From co-op counters to ag retail, the Midwest's rural economy depends on dependable point-of-sale hardware that handles the elements."),
            ("Central Logistics", "Sitting at the crossroads of America, the Midwest is where our free nationwide delivery shines — fast turns to every major metro."),
        ],
        "cta_head": "Heartland Reliability",
        "cta_body": "The Midwest doesn't do drama — it does dependability. We ship POS supplies to all 12 states, on time, every time.",
    },
    {
        "slug": "south",
        "region_name": "South",
        "title": "POS Supplies in the South | Thermal Paper, Receipt Paper & Ribbons",
        "meta": "Fast shipping of thermal paper rolls, receipt paper, and printer ribbons across the South — TX, FL, GA, and more. Volume pricing. Call (888) 881-6834.",
        "hero_bg": "linear-gradient(135deg,#0b3d2e,#059669,#064e3b)",
        "hero_h1": "POS Supplies for the South",
        "hero_tag": "The fastest-growing region in America — energy, ports, tourism, and a manufacturing boom that keeps registers ringing nonstop.",
        "states": ["Texas", "Oklahoma", "Arkansas", "Louisiana", "Mississippi", "Alabama", "Tennessee", "Kentucky", "Georgia", "Florida", "South Carolina", "North Carolina", "Virginia", "West Virginia"],
        "metros": ["Houston", "Dallas", "Austin", "San Antonio", "Atlanta", "Miami", "Orlando", "Nashville", "Charlotte", "New Orleans", "Tampa", "Raleigh"],
        "intro": (
            "The South is where America is growing fastest. Texas is the second-largest state economy, powered by energy, tech, and logistics; "
            "Atlanta and Charlotte anchor banking and distribution; Florida's tourism and hospitality run year-round; and Nashville, Austin, "
            "and the Research Triangle have become magnets for talent and commerce. Ports in Houston, New Orleans, Savannah, and Miami move "
            "goods across the hemisphere. That kind of volume doesn't tolerate downtime."
        ),
        "cards": [
            ("Energy & Industrial", "From Houston's energy corridor to Gulf Coast refineries, heavy industry needs rugged point-of-sale hardware and bulk thermal paper."),
            ("Tourism & Hospitality", "Orlando, Miami, New Orleans, and Nashville process millions of transactions a day. We keep the receipt paper flowing."),
            ("Ports & Distribution", "The South's ports and warehouses are the nation's supply backbone — and we're the supply behind the supply chain."),
        ],
        "cta_head": "Built for Southern Scale",
        "cta_body": "From the Lone Star State to the Lowcountry, we keep the South's fastest-growing businesses stocked and selling.",
    },
    {
        "slug": "east-coast",
        "region_name": "East Coast",
        "title": "POS Supplies on the East Coast | Thermal Paper & Receipt Paper",
        "meta": "Thermal paper, receipt paper, and printer ribbons shipped fast across the East Coast — NYC, Boston, Philly, DC, and more. Call (888) 881-6834.",
        "hero_bg": "linear-gradient(135deg,#1e293b,#475569,#0f172a)",
        "hero_h1": "POS Supplies for the East Coast",
        "hero_tag": "The densest, highest-value retail corridor in the country — finance, media, education, and government transacting in relentless volume.",
        "states": ["Maine", "New Hampshire", "Vermont", "Massachusetts", "Rhode Island", "Connecticut", "New York", "Pennsylvania", "New Jersey", "Delaware", "Maryland", "Washington DC"],
        "metros": ["New York City", "Boston", "Philadelphia", "Washington DC", "Baltimore", "Pittsburgh", "Providence", "Newark", "Hartford", "Buffalo", "Rochester", "Portland"],
        "intro": (
            "The East Coast packs more transactions per square mile than anywhere else in the country. New York City is the global capital of "
            "finance and retail; Boston pairs world-class universities with a booming biotech sector; Philadelphia anchors healthcare and "
            "education; and the DC-to-Baltimore corridor runs on government and defense contracting. Density means speed matters — a single "
            "midtown Manhattan deli can burn through a case of receipt paper faster than most regional chains."
        ),
        "cards": [
            ("Dense Urban Retail", "Bodegas, delis, cafés, and boutiques in NYC and Boston need rapid resupply. Our 2-3 day shipping keeps small operators from ever running dry."),
            ("Finance & Professional", "Banks, law firms, and professional offices need clean, archive-quality thermal paper for ATMs, POS, and recordkeeping."),
            ("Corridor Logistics", "From Maine to D.C., the I-95 corridor is our fastest delivery lane — next-level turnaround for the region that moves fastest."),
        ],
        "cta_head": "East Coast Speed",
        "cta_body": "In the densest retail market in America, downtime isn't an option. We ship POS supplies fast across the entire Eastern Seaboard.",
    },
]


def build_page(r):
    head = SHELL_HEAD.format(
        title=r["title"], meta=r["meta"], slug=r["slug"], hero_bg=r["hero_bg"],
    )
    states_html = states_chips(r["states"])
    metros_html = metros_chips(r["metros"])
    cards_html = "".join(
        f'<div class="card"><h3>{c[0]}</h3><p style="color:#2d3748">{c[1]}</p></div>'
        for c in r["cards"]
    )
    schema_states = '[' + ",".join(
        f'{{"@type":"State","name":"{s}"}}' for s in r["states"]
    ) + ']'

    body = f"""
<section class="hero">
<h1>{r['hero_h1']}</h1>
<div class="tag">{r['hero_tag']}</div>
<p style="font-size:18px">📞 <a href="tel:888-881-6834" style="color:#fff;font-weight:700;text-decoration:none">{PHONE}</a></p>
</section>

<section class="sec">
<h2>Covering {r['region_name']} — {len(r['states'])} States</h2>
<div class="states">{states_html}</div>
</section>

<section class="sec" style="background:#fff;border-radius:14px;border:1px solid #e2e8f0">
<h2>The {r['region_name']} Economy</h2>
<p style="font-size:17px;line-height:1.8;color:#2d3748;max-width:820px;margin:0 auto;text-align:center">{r['intro']}</p>
</section>

<section class="sec">
<h2>Why {r['region_name']} Businesses Choose Us</h2>
<div class="cols">{cards_html}</div>
</section>

<section class="sec">
<h2>Major Metros We Serve</h2>
<div class="states">{metros_html}</div>
</section>
"""
    foot = SHELL_FOOT.format(
        cta_head=r["cta_head"], cta_body=r["cta_body"], phone=PHONE,
        region_name=r["region_name"], slug=r["slug"], schema_states=schema_states,
    )
    return head + body + foot


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "generated_regions")
    os.makedirs(out, exist_ok=True)
    for r in REGIONS:
        with open(os.path.join(out, f"{r['slug']}.html"), "w") as f:
            f.write(build_page(r))
        print(f"  wrote {r['slug']}.html  ({len(r['states'])} states)")
    print(f"\nGenerated {len(REGIONS)} regional landing pages -> {out}")
