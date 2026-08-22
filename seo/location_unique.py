#!/usr/bin/env python3
"""
PSDepot location-page de-duplicator.
Generates genuinely unique, real, varied copy for each geo/location page
so Google stops treating them as doorway pages.

Design goals:
  1. Real per-location facts (cities, industries, local flavor) -> genuine uniqueness
  2. Heavy synonym + sentence-template rotation -> no two pages read alike
  3. Deterministic (hash-seeded) so output is stable across runs
  4. Keeps the PSD brand voice: fast shipping, bulk/volume, emergency orders,
     multi-location, free nationwide delivery, (888) 881-6834
"""

import hashlib
import json
import os

# ---------------------------------------------------------------------------
# 1. REAL PER-LOCATION DATA
# ---------------------------------------------------------------------------
# Each entry: dict(name=display name, type=State/City/Province/etc,
#                 cities=[real major cities], industries=real economic note,
#                 flavor=distinctive local line)
# ---------------------------------------------------------------------------

LOCATIONS = {
    # ---- US STATES ----
    "alabama": {
        "name": "Alabama", "type": "State",
        "cities": ["Birmingham", "Huntsville", "Montgomery", "Mobile", "Tuscaloosa", "Hoover", "Auburn", "Dothan", "Decatur", "Madison"],
        "industries": "Birmingham's steel and manufacturing legacy and Huntsville's aerospace and defense corridor (NASA Marshall, Redstone Arsenal) keep checkout counters ringing all year.",
        "flavor": "From the Tennessee Valley to the Gulf Coast, Alabama businesses move fast — so do we.",
    },
    "alaska": {
        "name": "Alaska", "type": "State",
        "cities": ["Anchorage", "Fairbanks", "Juneau", "Sitka", "Ketchikan", "Wasilla"],
        "industries": "Tourism, fishing, and oil-and-gas outposts in Anchorage and Fairbanks need rugged, reliable point-of-sale gear that can survive remote logistics.",
        "flavor": "We ship to the Last Frontier — freight that's built to make the journey.",
    },
    "arizona": {
        "name": "Arizona", "type": "State",
        "cities": ["Phoenix", "Tucson", "Mesa", "Chandler", "Scottsdale", "Glendale", "Tempe", "Gilbert"],
        "industries": "Phoenix's booming logistics and tech corridor and Tucson's aerospace and defense base keep high-volume retail and hospitality transacting around the clock.",
        "flavor": "Desert heat, steady receipts. We keep the paper flowing in every Valley of the Sun storefront.",
    },
    "arkansas": {
        "name": "Arkansas", "type": "State",
        "cities": ["Little Rock", "Fort Smith", "Fayetteville", "Springdale", "Jonesboro", "Rogers"],
        "industries": "Walmart-anchored retail and poultry and agriculture supply chains make Arkansas a steady, high-volume market for thermal rolls and receipt paper.",
        "flavor": "From the Ozarks to the Delta, Arkansas runs on retail — and retail runs on paper.",
    },
    "california": {
        "name": "California", "type": "State",
        "cities": ["Los Angeles", "San Francisco", "San Diego", "San Jose", "Sacramento", "Fresno", "Oakland", "Long Beach"],
        "industries": "The largest state economy in the U.S. — tech in the Bay Area, entertainment and trade in L.A., agriculture in the Central Valley — means relentless transaction volume.",
        "flavor": "From Silicon Valley startups to Central Valley diners, California keeps receipts moving.",
    },
    "colorado": {
        "name": "Colorado", "type": "State",
        "cities": ["Denver", "Colorado Springs", "Aurora", "Boulder", "Fort Collins", "Pueblo"],
        "industries": "Denver's aerospace and tech scene, Boulder's startups, and a booming tourism economy drive a fast-moving retail and hospitality market.",
        "flavor": "A mile high and always open — we keep Colorado's counters printing.",
    },
    "connecticut": {
        "name": "Connecticut", "type": "State",
        "cities": ["Bridgeport", "New Haven", "Hartford", "Stamford", "Norwalk", "Waterbury"],
        "industries": "Insurance, finance, and aerospace manufacturing — plus a dense hedge-fund corridor — keep Connecticut's point-of-sale traffic steady and demanding.",
        "flavor": "Small state, big transaction volume. We deliver to every county.",
    },
    "delaware": {
        "name": "Delaware", "type": "State",
        "cities": ["Wilmington", "Dover", "Newark", "Middletown", "Smyrna"],
        "industries": "A corporate-registration and banking hub with a growing logistics footprint keeps Wilmington-area retailers busy.",
        "flavor": "The First State gets first-rate shipping on every POS order.",
    },
    "florida": {
        "name": "Florida", "type": "State",
        "cities": ["Miami", "Orlando", "Tampa", "Jacksonville", "Fort Lauderdale", "Tallahassee", "St. Petersburg"],
        "industries": "Tourism, hospitality, and international trade power one of the highest-volume retail economies in the country, from Miami's ports to Orlando's theme-park corridor.",
        "flavor": "Sunshine, tourism, and millions of transactions — Florida never sleeps.",
    },
    "georgia": {
        "name": "Georgia", "type": "State",
        "cities": ["Atlanta", "Augusta", "Columbus", "Savannah", "Athens", "Macon"],
        "industries": "Atlanta's logistics, film, and corporate headquarters, plus Savannah's port, drive a massive distribution-driven retail economy.",
        "flavor": "The Peach State's supply chains run on steady, reliable receipt paper.",
    },
    "hawaii": {
        "name": "Hawaii", "type": "State",
        "cities": ["Honolulu", "Hilo", "Kailua", "Pearl City", "Waipahu"],
        "industries": "Tourism and hospitality dominate, with every resort, restaurant, and retail shop on the islands transacting daily.",
        "flavor": "Island pace, mainland reliability. We ship to every island in the chain.",
    },
    "idaho": {
        "name": "Idaho", "type": "State",
        "cities": ["Boise", "Meridian", "Nampa", "Idaho Falls", "Pocatello", "Coeur d'Alene"],
        "industries": "Boise's fast-growing tech and agribusiness base, plus a booming outdoor-recreation economy, keep Idaho retail steady.",
        "flavor": "From Boise's tech boom to mountain-town general stores, we've got Idaho covered.",
    },
    "illinois": {
        "name": "Illinois", "type": "State",
        "cities": ["Chicago", "Springfield", "Peoria", "Rockford", "Naperville", "Joliet"],
        "industries": "Chicago's finance, logistics, and manufacturing muscle — one of the nation's largest metro economies — anchors the state's transaction volume.",
        "flavor": "From the Loop to downstate, Illinois businesses run on reliable receipts.",
    },
    "indiana": {
        "name": "Indiana", "type": "State",
        "cities": ["Indianapolis", "Fort Wayne", "Evansville", "South Bend", "Carmel", "Fishers"],
        "industries": "Manufacturing, logistics, and motorsports anchor Indianapolis and the surrounding corridor, driving steady B2B and retail transactions.",
        "flavor": "The Crossroads of America needs a supply partner that's always in gear.",
    },
    "iowa": {
        "name": "Iowa", "type": "State",
        "cities": ["Des Moines", "Cedar Rapids", "Davenport", "Sioux City", "Iowa City", "Waterloo"],
        "industries": "Agriculture, insurance, and a growing data-center and logistics sector keep Iowa's small towns and metros transacting.",
        "flavor": "Heartland hustle — we keep Iowa's counters moving from harvest to checkout.",
    },
    "kansas": {
        "name": "Kansas", "type": "State",
        "cities": ["Wichita", "Overland Park", "Kansas City", "Topeka", "Olathe", "Lawrence"],
        "industries": "Aerospace in Wichita and a strong agribusiness base keep Kansas retail and B2B steady.",
        "flavor": "The Sunflower State gets dependable delivery, field to register.",
    },
    "kentucky": {
        "name": "Kentucky", "type": "State",
        "cities": ["Louisville", "Lexington", "Bowling Green", "Owensboro", "Covington"],
        "industries": "Louisville's logistics and bourbon economy, plus automotive manufacturing, keep Kentucky businesses busy.",
        "flavor": "From bourbon country to the Bluegrass, Kentucky runs on steady supply.",
    },
    "louisiana": {
        "name": "Louisiana", "type": "State",
        "cities": ["New Orleans", "Baton Rouge", "Shreveport", "Lafayette", "Lake Charles"],
        "industries": "Ports, energy, and a legendary hospitality scene make New Orleans and the Gulf Coast high-volume transaction markets.",
        "flavor": "Big flavor, big volume. Louisiana's registers never stop.",
    },
    "maine": {
        "name": "Maine", "type": "State",
        "cities": ["Portland", "Lewiston", "Bangor", "Auburn", "South Portland"],
        "industries": "Tourism, seafood, and a growing craft economy keep coastal Maine's shops and restaurants busy.",
        "flavor": "Vacationland's seasonal rush needs a supply partner that's ready on day one.",
    },
    "maryland": {
        "name": "Maryland", "type": "State",
        "cities": ["Baltimore", "Annapolis", "Rockville", "Gaithersburg", "Silver Spring"],
        "industries": "Federal contracting, biotech, and a dense Baltimore-Washington corridor keep Maryland's point-of-sale traffic high.",
        "flavor": "From the Bay to the Beltway, Maryland stays in motion.",
    },
    "massachusetts": {
        "name": "Massachusetts", "type": "State",
        "cities": ["Boston", "Worcester", "Springfield", "Cambridge", "Lowell"],
        "industries": "Higher ed, biotech, and finance in the Boston metro drive a dense, high-value retail and hospitality economy.",
        "flavor": "The Bay State's innovation economy runs on precision — so does our shipping.",
    },
    "michigan": {
        "name": "Michigan", "type": "State",
        "cities": ["Detroit", "Grand Rapids", "Ann Arbor", "Lansing", "Flint", "Sterling Heights"],
        "industries": "Automotive manufacturing and a resurgent Detroit keep Michigan's industrial and retail sectors transacting heavily.",
        "flavor": "Motor City grit meets rock-solid supply. Michigan is in our DNA.",
    },
    "minnesota": {
        "name": "Minnesota", "type": "State",
        "cities": ["Minneapolis", "St. Paul", "Rochester", "Duluth", "Bloomington"],
        "industries": "Healthcare, retail (Target, Best Buy HQ), and finance anchor the Twin Cities' high-volume economy.",
        "flavor": "The North Star State keeps receipts bright through every long winter.",
    },
    "mississippi": {
        "name": "Mississippi", "type": "State",
        "cities": ["Jackson", "Gulfport", "Southaven", "Biloxi", "Hattiesburg"],
        "industries": "Gulf Coast tourism and casinos, plus agriculture, keep Mississippi's hospitality and retail sectors busy.",
        "flavor": "From the Delta to the Gulf, Mississippi transacts with Southern speed.",
    },
    "missouri": {
        "name": "Missouri", "type": "State",
        "cities": ["Kansas City", "St. Louis", "Springfield", "Columbia", "Independence"],
        "industries": "St. Louis and Kansas City anchor agribusiness, logistics, and manufacturing across the Show-Me State.",
        "flavor": "Show-Me reliability: we prove it on every delivery.",
    },
    "montana": {
        "name": "Montana", "type": "State",
        "cities": ["Billings", "Missoula", "Bozeman", "Great Falls", "Helena"],
        "industries": "Tourism, agriculture, and a fast-growing tech and outdoor economy keep Big Sky Country's towns transacting.",
        "flavor": "Wide-open spaces, tight delivery windows. We handle both.",
    },
    "nebraska": {
        "name": "Nebraska", "type": "State",
        "cities": ["Omaha", "Lincoln", "Bellevue", "Grand Island", "Kearney"],
        "industries": "Omaha's insurance and finance hub, plus a powerhouse agriculture sector, keep Nebraska steady.",
        "flavor": "The Cornhusker State's work ethic meets same-speed supply.",
    },
    "nevada": {
        "name": "Nevada", "type": "State",
        "cities": ["Las Vegas", "Henderson", "Reno", "North Las Vegas", "Sparks"],
        "industries": "Las Vegas's hospitality and gaming economy runs 24/7, demanding nonstop transaction support.",
        "flavor": "A city that never closes needs supplies that never run out.",
    },
    "new-hampshire": {
        "name": "New Hampshire", "type": "State",
        "cities": ["Manchester", "Nashua", "Concord", "Dover", "Portsmouth"],
        "industries": "A no-sales-tax retail draw and strong tech and manufacturing base keep southern New Hampshire busy.",
        "flavor": "Live Free and transact freely — we keep the Granite State stocked.",
    },
    "new-jersey": {
        "name": "New Jersey", "type": "State",
        "cities": ["Newark", "Jersey City", "Paterson", "Elizabeth", "Trenton"],
        "industries": "Pharma, logistics, and dense commuter retail across the NYC metro keep New Jersey's volume enormous.",
        "flavor": "The Garden State's density demands fast, reliable POS supply.",
    },
    "new-mexico": {
        "name": "New Mexico", "type": "State",
        "cities": ["Albuquerque", "Las Cruces", "Santa Fe", "Rio Rancho", "Roswell"],
        "industries": "Federal research labs, film production, and a strong tourism and art economy anchor the Land of Enchantment.",
        "flavor": "Enchantment and enterprise — New Mexico's shops stay stocked with us.",
    },
    "new-york": {
        "name": "New York", "type": "State",
        "cities": ["New York City", "Buffalo", "Rochester", "Syracuse", "Albany", "Yonkers"],
        "industries": "Finance, media, and retail — NYC alone is one of the world's largest transaction markets, and upstate adds manufacturing and agriculture.",
        "flavor": "From Wall Street to the Finger Lakes, the Empire State never stops transacting.",
    },
    "north-carolina": {
        "name": "North Carolina", "type": "State",
        "cities": ["Charlotte", "Raleigh", "Greensboro", "Durham", "Winston-Salem", "Asheville"],
        "industries": "Charlotte's banking hub, the Research Triangle, and a booming manufacturing base keep North Carolina's economy humming.",
        "flavor": "First in flight, first in line for fast POS delivery.",
    },
    "north-dakota": {
        "name": "North Dakota", "type": "State",
        "cities": ["Fargo", "Bismarck", "Grand Forks", "Minot", "West Fargo"],
        "industries": "Energy and agriculture drive a resilient, high-volume economy across the Peace Garden State.",
        "flavor": "Tough winters, tougher supply chain. We deliver either way.",
    },
    "ohio": {
        "name": "Ohio", "type": "State",
        "cities": ["Columbus", "Cleveland", "Cincinnati", "Toledo", "Akron", "Dayton"],
        "industries": "Manufacturing, healthcare, and logistics anchor three major metros, keeping Ohio's retail and B2B sectors busy.",
        "flavor": "The Heart of It All — and we keep the heart of its commerce beating.",
    },
    "oklahoma": {
        "name": "Oklahoma", "type": "State",
        "cities": ["Oklahoma City", "Tulsa", "Norman", "Broken Arrow", "Edmond"],
        "industries": "Energy, aerospace, and logistics keep Oklahoma City and Tulsa transacting steadily.",
        "flavor": "Sooner service — fast, dependable, and always on time.",
    },
    "oregon": {
        "name": "Oregon", "type": "State",
        "cities": ["Portland", "Eugene", "Salem", "Gresham", "Hillsboro"],
        "industries": "Tech and footwear in Portland, plus agriculture and timber, keep Oregon's economy diverse and active.",
        "flavor": "From Portland's food carts to Willamette Valley wineries, Oregon stays busy.",
    },
    "pennsylvania": {
        "name": "Pennsylvania", "type": "State",
        "cities": ["Philadelphia", "Pittsburgh", "Allentown", "Erie", "Reading", "Harrisburg"],
        "industries": "Philadelphia's healthcare and education, plus Pittsburgh's tech and manufacturing renaissance, drive a massive state economy.",
        "flavor": "The Keystone State — and we're the keystone of its POS supply.",
    },
    "rhode-island": {
        "name": "Rhode Island", "type": "State",
        "cities": ["Providence", "Warwick", "Cranston", "Pawtucket", "Newport"],
        "industries": "Healthcare, education, and a strong coastal tourism economy keep the Ocean State's shops and restaurants busy.",
        "flavor": "The smallest state with the fastest delivery promise.",
    },
    "south-carolina": {
        "name": "South Carolina", "type": "State",
        "cities": ["Charleston", "Columbia", "Greenville", "Spartanburg", "Myrtle Beach"],
        "industries": "Charleston's port and tourism, plus advanced manufacturing in the Upstate, keep South Carolina growing fast.",
        "flavor": "Palmetto pride, steady supply. We serve every corner of the state.",
    },
    "south-dakota": {
        "name": "South Dakota", "type": "State",
        "cities": ["Sioux Falls", "Rapid City", "Aberdeen", "Brookings", "Watertown"],
        "industries": "Banking, healthcare, and tourism (Mount Rushmore) keep South Dakota's economy resilient.",
        "flavor": "Great faces, great service. We deliver to the Mount Rushmore State.",
    },
    "tennessee": {
        "name": "Tennessee", "type": "State",
        "cities": ["Nashville", "Memphis", "Knoxville", "Chattanooga", "Clarksville"],
        "industries": "Nashville's healthcare and music, Memphis's logistics hub (FedEx), and automotive manufacturing keep Tennessee booming.",
        "flavor": "From Music City to Beale Street, Tennessee keeps the beat — and the receipts.",
    },
    "texas": {
        "name": "Texas", "type": "State",
        "cities": ["Houston", "Dallas", "Austin", "San Antonio", "Fort Worth", "El Paso"],
        "industries": "Energy, tech (Austin), and a massive logistics and manufacturing base make Texas the second-largest state economy in the U.S.",
        "flavor": "Everything's bigger in Texas — including our delivery map.",
    },
    "utah": {
        "name": "Utah", "type": "State",
        "cities": ["Salt Lake City", "Provo", "Ogden", "St. George", "West Valley City"],
        "industries": "A booming tech scene (Silicon Slopes), outdoor recreation, and tourism keep Utah transacting at a fast clip.",
        "flavor": "Silicon Slopes, steady supply. Utah's growth is our growth.",
    },
    "vermont": {
        "name": "Vermont", "type": "State",
        "cities": ["Burlington", "South Burlington", "Rutland", "Montpelier", "Barre"],
        "industries": "Tourism, craft food and beverage, and a strong ski economy keep the Green Mountain State busy.",
        "flavor": "Green mountains, green receipts. We keep Vermont stocked year-round.",
    },
    "virginia": {
        "name": "Virginia", "type": "State",
        "cities": ["Virginia Beach", "Richmond", "Norfolk", "Chesapeake", "Arlington", "Alexandria"],
        "industries": "Federal contracting, defense, and a massive port economy anchor Virginia's steady transaction volume.",
        "flavor": "From the Pentagon to the port, Virginia runs on reliable supply.",
    },
    "washington": {
        "name": "Washington", "type": "State",
        "cities": ["Seattle", "Spokane", "Tacoma", "Vancouver", "Bellevue", "Everett"],
        "industries": "Tech giants, aerospace (Boeing), and international trade through Puget Sound keep Washington's economy enormous.",
        "flavor": "From Amazon to aviation, the Evergreen State never powers down.",
    },
    "west-virginia": {
        "name": "West Virginia", "type": "State",
        "cities": ["Charleston", "Huntington", "Morgantown", "Parkersburg", "Wheeling"],
        "industries": "Energy, healthcare, and a growing tourism and outdoor economy keep the Mountain State moving.",
        "flavor": "Wild and wonderful — and wonderfully well-supplied.",
    },
    "wisconsin": {
        "name": "Wisconsin", "type": "State",
        "cities": ["Milwaukee", "Madison", "Green Bay", "Kenosha", "Racine", "Appleton"],
        "industries": "Manufacturing, agriculture (dairy), and healthcare anchor Milwaukee and Madison's steady economy.",
        "flavor": "America's Dairyland keeps things fresh — and we keep the registers fresh too.",
    },
    "wyoming": {
        "name": "Wyoming", "type": "State",
        "cities": ["Cheyenne", "Casper", "Laramie", "Gillette", "Rock Springs"],
        "industries": "Energy, tourism (Yellowstone, Grand Teton), and agriculture keep the Equality State transacting.",
        "flavor": "Big sky, reliable supply. We reach every corner of Wyoming.",
    },

    # ---- MAJOR US CITIES ----
    "atlanta": {
        "name": "Atlanta", "type": "City",
        "cities": ["Downtown", "Buckhead", "Midtown", "Sandy Springs", "Marietta", "Decatur"],
        "industries": "A logistics, film, and corporate-headquarters powerhouse, Atlanta is the Southeast's transaction engine.",
        "flavor": "The ATL runs on hustle — and on receipts that never jam.",
    },
    "austin": {
        "name": "Austin", "type": "City",
        "cities": ["Downtown", "Round Rock", "Cedar Park", "Georgetown", "Pflugerville", "Buda"],
        "industries": "Tech, music, and hospitality fuel one of America's fastest-growing metros.",
        "flavor": "Keep Austin weird, keep Austin's receipts printing.",
    },
    "boston": {
        "name": "Boston", "type": "City",
        "cities": ["Back Bay", "Cambridge", "Somerville", "Brookline", "Quincy", "Newton"],
        "industries": "Higher ed, biotech, and finance drive a dense, high-value urban economy.",
        "flavor": "Historic city, modern checkout. Boston transacts with precision.",
    },
    "chicago": {
        "name": "Chicago", "type": "City",
        "cities": ["The Loop", "Naperville", "Evanston", "Oak Park", "Schaumburg", "Joliet"],
        "industries": "Finance, logistics, and manufacturing make Chicago one of the nation's largest transaction markets.",
        "flavor": "The city that works needs supplies that work harder.",
    },
    "dallas": {
        "name": "Dallas", "type": "City",
        "cities": ["Downtown", "Plano", "Irving", "Frisco", "Arlington", "Garland"],
        "industries": "A corporate and logistics hub in the fast-growing DFW metro keeps Dallas transacting around the clock.",
        "flavor": "Big D, big demand. We keep the Metroplex stocked.",
    },
    "denver": {
        "name": "Denver", "type": "City",
        "cities": ["Downtown", "Aurora", "Lakewood", "Centennial", "Westminster", "Thornton"],
        "industries": "Aerospace, tech, and a booming outdoor economy anchor the Mile High City.",
        "flavor": "A mile high, always moving. Denver's registers never rest.",
    },
    "detroit": {
        "name": "Detroit", "type": "City",
        "cities": ["Downtown", "Dearborn", "Warren", "Southfield", "Livonia", "Sterling Heights"],
        "industries": "A resurgent automotive and manufacturing core keeps Motor City transacting heavily.",
        "flavor": "Built in the D — and supplied with Detroit grit.",
    },
    "houston": {
        "name": "Houston", "type": "City",
        "cities": ["Downtown", "Sugar Land", "Pasadena", "Katy", "The Woodlands", "Pearland"],
        "industries": "Energy, medical, and international trade make Houston a top-tier transaction market.",
        "flavor": "Space City's economy is out of this world — and so is our shipping.",
    },
    "las-vegas": {
        "name": "Las Vegas", "type": "City",
        "cities": ["The Strip", "Henderson", "North Las Vegas", "Summerlin", "Paradise", "Spring Valley"],
        "industries": "A 24/7 hospitality and gaming economy demands nonstop transaction support.",
        "flavor": "The city that never closes needs receipts that never run out.",
    },
    "los-angeles": {
        "name": "Los Angeles", "type": "City",
        "cities": ["Downtown", "Hollywood", "Santa Monica", "Pasadena", "Long Beach", "Glendale"],
        "industries": "Entertainment, trade through the Port of L.A., and a massive retail economy keep the Southland transacting.",
        "flavor": "From Hollywood to the harbor, L.A. keeps the receipts rolling.",
    },
    "miami": {
        "name": "Miami", "type": "City",
        "cities": ["Downtown", "Miami Beach", "Coral Gables", "Hialeah", "Doral", "Kendall"],
        "industries": "International trade, finance, and hospitality make Miami the gateway to the Americas.",
        "flavor": "The Magic City's economy is pure magic — and pure volume.",
    },
    "new-orleans": {
        "name": "New Orleans", "type": "City",
        "cities": ["French Quarter", "Metairie", "Kenner", "Gretna", "Slidell", "Marrero"],
        "industries": "Ports, energy, and a legendary hospitality scene keep the Big Easy transacting.",
        "flavor": "Big Easy charm, big-time volume. We keep NOLA stocked.",
    },
    "philadelphia": {
        "name": "Philadelphia", "type": "City",
        "cities": ["Center City", "West Philly", "Cherry Hill", "Camden", "Upper Darby", "Norristown"],
        "industries": "Healthcare, education, and finance anchor the City of Brotherly Love's dense economy.",
        "flavor": "Brotherly love, dependable supply. Philly transacts all day.",
    },
    "phoenix": {
        "name": "Phoenix", "type": "City",
        "cities": ["Downtown", "Mesa", "Chandler", "Scottsdale", "Tempe", "Gilbert"],
        "industries": "Logistics, tech, and a booming population keep the Valley of the Sun transacting fast.",
        "flavor": "The Valley's growth is relentless — so is our delivery.",
    },
    "portland": {
        "name": "Portland", "type": "City",
        "cities": ["Downtown", "Beaverton", "Gresham", "Hillsboro", "Vancouver", "Tigard"],
        "industries": "Tech, craft food, and a strong logistics base keep the Rose City busy.",
        "flavor": "Keep Portland weird, keep Portland's receipts flowing.",
    },
    "san-diego": {
        "name": "San Diego", "type": "City",
        "cities": ["Downtown", "Chula Vista", "Oceanside", "Escondido", "Carlsbad", "El Cajon"],
        "industries": "Defense, biotech, and tourism keep America's Finest City transacting steadily.",
        "flavor": "America's Finest City gets America's finest POS supply.",
    },
    "san-francisco": {
        "name": "San Francisco", "type": "City",
        "cities": ["Downtown", "Oakland", "Berkeley", "Daly City", "San Mateo", "Palo Alto"],
        "industries": "The heart of the tech economy, plus a dense hospitality scene, keeps the Bay Area transacting relentlessly.",
        "flavor": "From startups to sourdough, the City by the Bay keeps receipts moving.",
    },
    "seattle": {
        "name": "Seattle", "type": "City",
        "cities": ["Downtown", "Bellevue", "Redmond", "Kirkland", "Tacoma", "Everett"],
        "industries": "Tech, aerospace, and international trade make the Emerald City a top-tier economy.",
        "flavor": "From cloud computing to coffee, Seattle runs on reliable supply.",
    },
    "baltimore": {
        "name": "Baltimore", "type": "City",
        "cities": ["Inner Harbor", "Towson", "Ellicott City", "Glen Burnie", "Dundalk", "Catonsville"],
        "industries": "Healthcare, biotech, and a major port keep Charm City transacting.",
        "flavor": "Charm City's hustle is real — and so is our delivery speed.",
    },
    "charlotte": {
        "name": "Charlotte", "type": "City",
        "cities": ["Uptown", "Concord", "Gastonia", "Huntersville", "Matthews", "Kannapolis"],
        "industries": "A major banking hub and fast-growing metro keep the Queen City booming.",
        "flavor": "The Queen City's crown jewel? Reliable, fast POS supply.",
    },
    "columbus": {
        "name": "Columbus", "type": "City",
        "cities": ["Downtown", "Dublin", "Westerville", "Grove City", "Hilliard", "Gahanna"],
        "industries": "Insurance, logistics, and a fast-growing tech scene anchor Ohio's capital.",
        "flavor": "A city on the rise — and we rise with it, receipt by receipt.",
    },
    "indianapolis": {
        "name": "Indianapolis", "type": "City",
        "cities": ["Downtown", "Carmel", "Fishers", "Greenwood", "Noblesville", "Avon"],
        "industries": "Motorsports, logistics, and manufacturing keep the Circle City transacting.",
        "flavor": "The Racing Capital runs fast — and so do our deliveries.",
    },
    "jacksonville": {
        "name": "Jacksonville", "type": "City",
        "cities": ["Downtown", "Orange Park", "St. Augustine", "Fleming Island", "Atlantic Beach", "Fernandina Beach"],
        "industries": "Logistics, finance, and a major port anchor Florida's largest city.",
        "flavor": "The Bold City gets bold, dependable supply.",
    },
    "milwaukee": {
        "name": "Milwaukee", "type": "City",
        "cities": ["Downtown", "Waukesha", "West Allis", "Wauwatosa", "Brookfield", "Oak Creek"],
        "industries": "Manufacturing, brewing, and healthcare keep Cream City's economy strong.",
        "flavor": "Brew City's work ethic meets our supply reliability.",
    },
    "minneapolis": {
        "name": "Minneapolis", "type": "City",
        "cities": ["Downtown", "St. Paul", "Bloomington", "Brooklyn Park", "Plymouth", "Eden Prairie"],
        "industries": "Retail, finance, and healthcare anchor the Twin Cities' powerhouse economy.",
        "flavor": "The Twin Cities' skyline keeps rising — and so does our delivery record.",
    },
    "nashville": {
        "name": "Nashville", "type": "City",
        "cities": ["Downtown", "Franklin", "Murfreesboro", "Hendersonville", "Brentwood", "Smyrna"],
        "industries": "Healthcare, music, and a tourism boom keep Music City transacting around the clock.",
        "flavor": "From Broadway honky-tonks to boardrooms, Nashville stays in rhythm.",
    },
    "oklahoma-city": {
        "name": "Oklahoma City", "type": "City",
        "cities": ["Downtown", "Edmond", "Norman", "Moore", "Midwest City", "Yukon"],
        "industries": "Energy, aerospace, and logistics keep OKC transacting steadily.",
        "flavor": "The Big Friendly gets big friendly service — fast.",
    },
    "omaha": {
        "name": "Omaha", "type": "City",
        "cities": ["Downtown", "Bellevue", "Papillion", "La Vista", "Council Bluffs", "Ralston"],
        "industries": "Insurance, finance, and logistics anchor a quiet economic powerhouse.",
        "flavor": "Silicon Prairie's steady economy, matched by steady supply.",
    },
    "sacramento": {
        "name": "Sacramento", "type": "City",
        "cities": ["Downtown", "Elk Grove", "Roseville", "Folsom", "Rancho Cordova", "Citrus Heights"],
        "industries": "Government, healthcare, and a booming farm-to-fork food scene keep California's capital busy.",
        "flavor": "From farm to fork, Sacramento keeps the receipts fresh.",
    },
    "tucson": {
        "name": "Tucson", "type": "City",
        "cities": ["Downtown", "Oro Valley", "Marana", "Sahuarita", "Catalina Foothills", "Vail"],
        "industries": "Aerospace, defense, and the University of Arizona anchor the Old Pueblo.",
        "flavor": "The Old Pueblo's heritage, paired with modern supply speed.",
    },
    "tulsa": {
        "name": "Tulsa", "type": "City",
        "cities": ["Downtown", "Broken Arrow", "Owasso", "Bixby", "Jenks", "Sand Springs"],
        "industries": "Energy, aerospace, and a growing tech scene keep Tulsa transacting.",
        "flavor": "Green Country's energy, backed by our delivery energy.",
    },
    "albuquerque": {
        "name": "Albuquerque", "type": "City",
        "cities": ["Downtown", "Rio Rancho", "Los Lunas", "Bernalillo", "Corrales", "Belen"],
        "industries": "Federal labs, film, and a strong healthcare base anchor the Duke City.",
        "flavor": "The Duke City's hot air rises — and so does our service level.",
    },
    "el-paso": {
        "name": "El Paso", "type": "City",
        "cities": ["Downtown", "Socorro", "Horizon City", "Anthony", "Fabens", "Clint"],
        "industries": "Border trade, logistics, and Fort Bliss keep the Sun City transacting.",
        "flavor": "The Sun City's cross-border hustle meets our fast shipping.",
    },
    "fort-worth": {
        "name": "Fort Worth", "type": "City",
        "cities": ["Downtown", "Arlington", "Keller", "Haltom City", "Benbrook", "Saginaw"],
        "industries": "Aviation, manufacturing, and the DFW logistics corridor keep Cowtown busy.",
        "flavor": "Where the West begins, so does dependable supply.",
    },
    "fresno": {
        "name": "Fresno", "type": "City",
        "cities": ["Downtown", "Clovis", "Madera", "Sanger", "Selma", "Reedley"],
        "industries": "The heart of the Central Valley's agriculture economy, plus logistics and healthcare.",
        "flavor": "The Valley's food feeds the world — and its receipts feed our growth.",
    },
    "bakersfield": {
        "name": "Bakersfield", "type": "City",
        "cities": ["Downtown", "Oildale", "Rosedale", "Shafter", "Wasco", "Delano"],
        "industries": "Energy and agriculture anchor one of California's most productive regions.",
        "flavor": "Country roots, industrial strength. Bakersfield transacts with grit.",
    },
    "arlington": {
        "name": "Arlington", "type": "City",
        "cities": ["Downtown", "Grand Prairie", "Mansfield", "Kennedale", "Pantego", "Dalworthington Gardens"],
        "industries": "Sports and entertainment (AT&T Stadium) plus the DFW logistics base keep Arlington busy.",
        "flavor": "Home of the big game — and big, reliable POS supply.",
    },
    "raleigh": {
        "name": "Raleigh", "type": "City",
        "cities": ["Downtown", "Cary", "Durham", "Garner", "Apex", "Wake Forest"],
        "industries": "The Research Triangle's tech and biotech engine keeps Raleigh booming.",
        "flavor": "The City of Oaks keeps growing — and we keep it stocked.",
    },
    "wichita": {
        "name": "Wichita", "type": "City",
        "cities": ["Downtown", "Derby", "Andover", "Maize", "Haysville", "Park City"],
        "industries": "Aerospace manufacturing (the Air Capital) anchors Wichita's economy.",
        "flavor": "The Air Capital's precision, matched by our supply precision.",
    },
    "colorado-springs": {
        "name": "Colorado Springs", "type": "City",
        "cities": ["Downtown", "Fountain", "Monument", "Security-Widefield", "Manitou Springs", "Woodland Park"],
        "industries": "Military, aerospace, and tourism keep Olympic City transacting.",
        "flavor": "Olympic City heights, Olympic-level service.",
    },
    "virginia-beach": {
        "name": "Virginia Beach", "type": "City",
        "cities": ["Oceanfront", "Chesapeake", "Norfolk", "Suffolk", "Hampton", "Newport News"],
        "industries": "Tourism, defense, and a major port keep the coastal economy strong.",
        "flavor": "Beach-town tourism plus military precision — we supply both.",
    },

    # ---- CANADIAN PROVINCES ----
    "alberta": {
        "name": "Alberta", "type": "Province",
        "cities": ["Calgary", "Edmonton", "Red Deer", "Lethbridge", "Medicine Hat"],
        "industries": "Energy, agriculture, and a fast-growing tech scene keep Alberta's economy dynamic.",
        "flavor": "Wild Rose Country's energy drives ours.",
    },
    "british-columbia": {
        "name": "British Columbia", "type": "Province",
        "cities": ["Vancouver", "Victoria", "Surrey", "Burnaby", "Kelowna"],
        "industries": "Tech, film, and international trade through Vancouver keep B.C.'s economy diverse.",
        "flavor": "From the Coast to the Interior, B.C. stays beautifully busy.",
    },
    "manitoba": {
        "name": "Manitoba", "type": "Province",
        "cities": ["Winnipeg", "Brandon", "Steinbach", "Thompson", "Portage la Prairie"],
        "industries": "Agriculture, manufacturing, and logistics anchor the Keystone Province.",
        "flavor": "The Keystone Province keeps commerce flowing — so do we.",
    },
    "new-brunswick": {
        "name": "New Brunswick", "type": "Province",
        "cities": ["Moncton", "Saint John", "Fredericton", "Miramichi", "Edmundston"],
        "industries": "Forestry, fisheries, and a growing tech sector keep the Picture Province moving.",
        "flavor": "The Picture Province, perfectly supplied.",
    },
    "newfoundland-labrador": {
        "name": "Newfoundland and Labrador", "type": "Province",
        "cities": ["St. John's", "Corner Brook", "Mount Pearl", "Gander", "Grand Falls-Windsor"],
        "industries": "Offshore energy, fisheries, and tourism anchor this coastal economy.",
        "flavor": "The Rock's resilience, matched by our reliable delivery.",
    },
    "northwest-territories": {
        "name": "Northwest Territories", "type": "Territory",
        "cities": ["Yellowknife", "Hay River", "Inuvik", "Fort Smith", "Behchokǫ̀"],
        "industries": "Mining, government, and Indigenous-led enterprise keep the North transacting.",
        "flavor": "We reach the true North, strong and free.",
    },
    "nova-scotia": {
        "name": "Nova Scotia", "type": "Province",
        "cities": ["Halifax", "Dartmouth", "Sydney", "Truro", "New Glasgow"],
        "industries": "Ports, fisheries, and a growing tech and ocean sector keep the Maritimes busy.",
        "flavor": "Canada's Ocean Playground, always open for business.",
    },
    "nunavut": {
        "name": "Nunavut", "type": "Territory",
        "cities": ["Iqaluit", "Rankin Inlet", "Arviat", "Baker Lake", "Cambridge Bay"],
        "industries": "Government services, mining, and Indigenous-owned enterprise anchor the North.",
        "flavor": "From Iqaluit to the Kivalliq, we deliver to the far North.",
    },
    "ontario": {
        "name": "Ontario", "type": "Province",
        "cities": ["Toronto", "Ottawa", "Mississauga", "Hamilton", "London"],
        "industries": "Canada's economic engine — finance, tech, and manufacturing keep Ontario transacting at national scale.",
        "flavor": "From Toronto's towers to Ottawa's corridors, Ontario never stops.",
    },
    "prince-edward-island": {
        "name": "Prince Edward Island", "type": "Province",
        "cities": ["Charlottetown", "Summerside", "Stratford", "Cornwall", "Montague"],
        "industries": "Tourism, agriculture (potatoes), and a growing tech sector keep the Island busy.",
        "flavor": "The Gentle Island, gently but reliably supplied.",
    },
    "quebec": {
        "name": "Quebec", "type": "Province",
        "cities": ["Montreal", "Quebec City", "Laval", "Gatineau", "Sherbrooke"],
        "industries": "Aerospace, tech, and a vibrant cultural economy anchor Quebec's distinct market.",
        "flavor": "La Belle Province — vibrant, dynamic, and always transacting.",
    },
    "saskatchewan": {
        "name": "Saskatchewan", "type": "Province",
        "cities": ["Saskatoon", "Regina", "Prince Albert", "Moose Jaw", "Swift Current"],
        "industries": "Agriculture, mining (potash, uranium), and energy keep the Land of Living Skies strong.",
        "flavor": "Land of Living Skies, land of steady supply.",
    },
    "yukon": {
        "name": "Yukon", "type": "Territory",
        "cities": ["Whitehorse", "Dawson City", "Watson Lake", "Haines Junction", "Carmacks"],
        "industries": "Mining, tourism, and government keep the Klondike territory transacting.",
        "flavor": "From Whitehorse to the Klondike, we deliver to the frontier.",
    },

    # ---- MEXICAN STATES ----
    "aguascalientes": {
        "name": "Aguascalientes", "type": "State",
        "cities": ["Aguascalientes", "Jesús María", "Calvillo", "Pabellón de Arteaga", "Rincón de Romos"],
        "industries": "Automotive manufacturing and a fast-growing logistics base anchor the state's economy.",
        "flavor": "Small state, industrial might. Aguascalientes transacts with precision.",
    },
    "baja-california": {
        "name": "Baja California", "type": "State",
        "cities": ["Tijuana", "Mexicali", "Ensenada", "Tecate", "Rosarito"],
        "industries": "Maquiladora manufacturing and cross-border trade with California drive a high-volume economy.",
        "flavor": "Cross-border hustle, borderless service.",
    },
    "baja-california-sur": {
        "name": "Baja California Sur", "type": "State",
        "cities": ["La Paz", "Cabo San Lucas", "San José del Cabo", "Loreto", "Ciudad Constitución"],
        "industries": "Tourism (Los Cabos), fisheries, and agriculture keep this coastal state transacting.",
        "flavor": "Resort luxury needs reliable supply — we deliver to paradise.",
    },
    "campeche": {
        "name": "Campeche", "type": "State",
        "cities": ["San Francisco de Campeche", "Ciudad del Carmen", "Champotón", "Escárcega", "Calkiní"],
        "industries": "Energy, fisheries, and a growing tourism sector anchor the economy.",
        "flavor": "Fortified history, modern supply.",
    },
    "chihuahua": {
        "name": "Chihuahua", "type": "State",
        "cities": ["Chihuahua", "Ciudad Juárez", "Cuauhtémoc", "Delicias", "Parral"],
        "industries": "Manufacturing, maquiladoras, and agriculture drive a major border economy.",
        "flavor": "The largest state, with the largest work ethic.",
    },
    "coahuila": {
        "name": "Coahuila", "type": "State",
        "cities": ["Saltillo", "Torreón", "Monclova", "Piedras Negras", "Ciudad Acuña"],
        "industries": "Automotive and steel manufacturing anchor a powerhouse industrial economy.",
        "flavor": "Industrial strength, dependable supply.",
    },
    "colima": {
        "name": "Colima", "type": "State",
        "cities": ["Colima", "Manzanillo", "Villa de Álvarez", "Tecomán", "Armería"],
        "industries": "Port logistics (Manzanillo) and agriculture keep this small state productive.",
        "flavor": "Small but mighty — and always well-supplied.",
    },
    "durango": {
        "name": "Durango", "type": "State",
        "cities": ["Durango", "Gómez Palacio", "Lerdo", "Santiago Papasquiaro", "El Salto"],
        "industries": "Forestry, mining, and agriculture anchor the economy.",
        "flavor": "Land of scorpions and cinema — and steady commerce.",
    },
    "guanajuato": {
        "name": "Guanajuato", "type": "State",
        "cities": ["León", "Irapuato", "Celaya", "Salamanca", "Guanajuato"],
        "industries": "Automotive manufacturing and agriculture drive one of Mexico's most industrialized states.",
        "flavor": "Colonial beauty, industrial backbone.",
    },
    "guerrero": {
        "name": "Guerrero", "type": "State",
        "cities": ["Acapulco", "Chilpancingo", "Iguala", "Taxco", "Zihuatanejo"],
        "industries": "Tourism (Acapulco, Ixtapa-Zihuatanejo) and agriculture anchor the economy.",
        "flavor": "From silver to sunsets, Guerrero keeps transacting.",
    },
    "hidalgo": {
        "name": "Hidalgo", "type": "State",
        "cities": ["Pachuca", "Tulancingo", "Tula", "Huejutla", "Ixmiquilpan"],
        "industries": "Manufacturing, mining, and agriculture keep the state steady.",
        "flavor": "Industrial corridor, dependable service.",
    },
    "jalisco": {
        "name": "Jalisco", "type": "State",
        "cities": ["Guadalajara", "Zapopan", "Tlaquepaque", "Tonalá", "Puerto Vallarta"],
        "industries": "Tech (Silicon Valley of Mexico), tequila, and tourism anchor a major economy.",
        "flavor": "From Guadalajara's tech to the agave fields, Jalisco thrives.",
    },
    "michoacan": {
        "name": "Michoacan", "type": "State",
        "cities": ["Morelia", "Uruapan", "Zamora", "Lázaro Cárdenas", "Pátzcuaro"],
        "industries": "Agriculture (avocados), mining, and tourism keep the state productive.",
        "flavor": "From avocados to the port, Michoacán transacts year-round.",
    },
    "morelos": {
        "name": "Morelos", "type": "State",
        "cities": ["Cuernavaca", "Cuautla", "Jiutepec", "Temixco", "Yautepec"],
        "industries": "Manufacturing, agriculture, and tourism (Cuernavaca) anchor the economy.",
        "flavor": "The city of eternal spring, eternally busy.",
    },
    "nayarit": {
        "name": "Nayarit", "type": "State",
        "cities": ["Tepic", "Nuevo Vallarta", "Bahía de Banderas", "Santiago Ixcuintla", "Tuxpan"],
        "industries": "Tourism (Riviera Nayarit) and agriculture drive the economy.",
        "flavor": "Riviera sunshine, reliable supply.",
    },
    "nuevo-leon": {
        "name": "Nuevo León", "type": "State",
        "cities": ["Monterrey", "Guadalupe", "San Nicolás", "Apodaca", "San Pedro Garza García"],
        "industries": "A manufacturing and industrial powerhouse anchored by Monterrey.",
        "flavor": "The industrial heart of Mexico, beating strong.",
    },
    "oaxaca": {
        "name": "Oaxaca", "type": "State",
        "cities": ["Oaxaca de Juárez", "Salina Cruz", "Juchitán", "Tuxtepec", "Huajuapan de León"],
        "industries": "Tourism, agriculture, and a rich artisan economy keep Oaxaca vibrant.",
        "flavor": "Rich culture, rich commerce. Oaxaca keeps its counters busy.",
    },
    "puebla": {
        "name": "Puebla", "type": "State",
        "cities": ["Puebla", "Tehuacán", "Cholula", "Atlixco", "San Martín Texmelucan"],
        "industries": "Automotive and manufacturing anchor one of Mexico's key industrial states.",
        "flavor": "Cinco de Mayo's origin, with year-round commerce.",
    },
    "queretaro": {
        "name": "Querétaro", "type": "State",
        "cities": ["Querétaro", "San Juan del Río", "Corregidora", "El Marqués", "Tequisquiapan"],
        "industries": "A booming aerospace, automotive, and tech hub in central Mexico.",
        "flavor": "A fast-growing economy, matched by fast delivery.",
    },
    "quintana-roo": {
        "name": "Quintana Roo", "type": "State",
        "cities": ["Cancún", "Playa del Carmen", "Chetumal", "Tulum", "Cozumel"],
        "industries": "Tourism (Cancún, Riviera Maya) drives a massive hospitality economy.",
        "flavor": "Caribbean paradise, nonstop transactions.",
    },
    "sinaloa": {
        "name": "Sinaloa", "type": "State",
        "cities": ["Culiacán", "Mazatlán", "Los Mochis", "Guasave", "Guamúchil"],
        "industries": "Agriculture, fisheries, and tourism (Mazatlán) anchor the economy.",
        "flavor": "From the fields to the Pacific, Sinaloa stays productive.",
    },
    "sonora": {
        "name": "Sonora", "type": "State",
        "cities": ["Hermosillo", "Ciudad Obregón", "Nogales", "San Luis Río Colorado", "Guaymas"],
        "industries": "Manufacturing, agriculture, and cross-border trade anchor a strong economy.",
        "flavor": "Desert strength, border hustle.",
    },
    "tabasco": {
        "name": "Tabasco", "type": "State",
        "cities": ["Villahermosa", "Cárdenas", "Comalcalco", "Paraíso", "Macuspana"],
        "industries": "Energy and agriculture anchor the tropical Gulf state.",
        "flavor": "Tropical climate, tropical transaction volume.",
    },
    "tamaulipas": {
        "name": "Tamaulipas", "type": "State",
        "cities": ["Reynosa", "Matamoros", "Nuevo Laredo", "Tampico", "Ciudad Victoria"],
        "industries": "Maquiladora manufacturing and border trade drive a major economy.",
        "flavor": "Border commerce at its busiest, supplied with speed.",
    },
    "tlaxcala": {
        "name": "Tlaxcala", "type": "State",
        "cities": ["Tlaxcala", "Apizaco", "Huamantla", "Chiautempan", "Calpulalpan"],
        "industries": "Manufacturing and agriculture anchor this compact industrial state.",
        "flavor": "Small in size, big in industry.",
    },
    "veracruz": {
        "name": "Veracruz", "type": "State",
        "cities": ["Veracruz", "Xalapa", "Coatzacoalcos", "Córdoba", "Poza Rica"],
        "industries": "Ports, energy, and agriculture anchor one of Mexico's largest states.",
        "flavor": "The gateway port, always in motion.",
    },
    "yucatan": {
        "name": "Yucatán", "type": "State",
        "cities": ["Mérida", "Valladolid", "Progreso", "Tizimín", "Ticul"],
        "industries": "Tourism (Mérida, Chichén Itzá) and manufacturing keep the peninsula thriving.",
        "flavor": "Mayan heritage, modern commerce.",
    },
    "zacatecas": {
        "name": "Zacatecas", "type": "State",
        "cities": ["Zacatecas", "Fresnillo", "Guadalupe", "Jerez", "Río Grande"],
        "industries": "Mining and agriculture anchor the economy.",
        "flavor": "Silver heritage, solid supply.",
    },
}

# Language-variant targets (Spanish and other locales) are handled separately;
# see generate_language_variant() below.


# ---------------------------------------------------------------------------
# 2. SYNONYM + TEMPLATE BANKS (the "thesaurus")
# ---------------------------------------------------------------------------

SYN = {
    "deliver": ["deliver", "ship", "send", "get", "rush", "dispatch"],
    "fast": ["fast", "rapid", "quick", "swift", "same-week", "expedited"],
    "reliable": ["reliable", "dependable", "rock-solid", "consistent", "steady"],
    "businesses": ["businesses", "merchants", "storefronts", "retailers", "operators", "shops"],
    "supplies": ["POS supplies", "point-of-sale supplies", "receipt paper", "thermal rolls", "checkout supplies"],
    "statewide": ["statewide", "across the state", "to every county", "corner to corner", "state line to state line"],
    "call": ["Call", "Reach", "Phone", "Ring", "Dial"],
}

TITLE_TEMPLATES = [
    "POS Supplies in {name} | Thermal Paper, Receipt Paper & Printer Ribbons",
    "{name} POS Supplies | Fast Shipping of Thermal & Receipt Paper",
    "Thermal Paper & POS Supplies Shipped to {name} | Performance Supply Depot",
    "{name} Receipt Paper & Printer Ribbons | {type}wide Delivery",
    "POS & Checkout Supplies for {name} | Fast, Reliable Delivery",
    "Thermal Rolls & Receipt Paper in {name} | Performance Supply Depot",
]

META_TEMPLATES = [
    "Fast shipping of thermal paper rolls, receipt paper, and printer ribbons to {name}. Serving {cities}. Call (888) 881-6834.",
    "Reliable {type}wide delivery of POS supplies to {name} businesses — thermal rolls, receipt paper, printer ribbons. {phone}.",
    "{name} merchants trust us for thermal paper, receipt paper, and printer ribbons, shipped fast. {phone}.",
    "Order POS supplies for {name} — thermal paper, receipt rolls, and ribbons with free nationwide delivery. {phone}.",
    "From {city1} to {city2}, we ship POS supplies to {name} fast. Thermal paper, receipt paper, ribbons. {phone}.",
]

HERO_H1 = [
    "POS Supplies Delivered {statewide}",
    "{name} Businesses Run on Our Receipt Paper",
    "Thermal Paper & Ribbons for {name}",
    "Checkout Supplies {name} Can Count On",
    "Keeping {name} in Business, One Receipt at a Time",
]

FEATURE_HEADINGS = [
    "{name}-Sized Service",
    "Built for {name} Businesses",
    "The {name} Supply Standard",
    "Why {name} Chooses Us",
    "Supply Support for {name}",
]

CTA_HEADINGS = [
    "Everything's Bigger in {name}",
    "Ready When {name} Needs You",
    "{name} Runs on Us",
    "The Fast Track for {name} Businesses",
    "Your {name} Supply Partner",
]

CTA_SUBHEADS = [
    "Including Our Service Area",
    "We Ship to Every Corner",
    "Free Nationwide Delivery",
    "Volume Discounts Available",
    "Dedicated Support Team",
]

# ---------------------------------------------------------------------------
# 3. DETERMINISTIC PICKER
# ---------------------------------------------------------------------------

def h(name, salt=""):
    """Stable hash -> int for deterministic variation per location."""
    return int(hashlib.md5((name + salt).encode()).hexdigest(), 16)

def pick(name, arr, salt=""):
    return arr[h(name, salt) % len(arr)]


# ---------------------------------------------------------------------------
# 4. PAGE GENERATOR
# ---------------------------------------------------------------------------

def generate_page(key, loc):
    name = loc["name"]
    ltype = loc["type"]
    cities = loc["cities"]
    industries = loc["industries"]
    flavor = loc["flavor"]
    city1, city2, city3 = cities[0], cities[1], cities[2]
    city_list = ", ".join(cities[:3])
    phone = "(888) 881-6834"

    title = pick(key, TITLE_TEMPLATES).format(name=name, type=ltype)
    meta = pick(key, META_TEMPLATES, "meta").format(
        name=name, type=ltype, cities=city_list, phone=phone,
        deliver=pick(key, SYN["deliver"], "dv"), city1=city1, city2=city2)
    h1 = pick(key, HERO_H1).format(
        name=name, deliver=pick(key, SYN["deliver"], "h1dv"),
        statewide=pick(key, SYN["statewide"], "sw"))
    feat_head = pick(key, FEATURE_HEADINGS, "fh").format(name=name)
    cta_head = pick(key, CTA_HEADINGS, "cta").format(name=name)
    cta_sub = pick(key, CTA_SUBHEADS, "ctasub").format(name=name)

    cities_label = "Cities" if ltype == "State" else "Areas"

    # vary which 3 of 6 products shown
    products = [
        ("3 1/8\" Thermal Paper", "Standard POS receipt paper", "$99/case"),
        ("2 1/4\" Credit Card Paper", "Terminal receipt rolls", "$39/case"),
        ("SAM4S Cash Registers", "Complete POS systems", "From $495"),
        ("Printer Ribbons", "Impact printer ribbons", "$12 each"),
        ("Kitchen Impact Paper", "Two-ply kitchen printers", "$59/case"),
        ("Barcode Labels", "Thermal transfer labels", "$29/roll"),
    ]
    offset = h(key, "prod") % len(products)
    shown = [(products[(offset + i) % len(products)]) for i in range(3)]

    # Build feature descriptions with synonym rotation
    features = [
        (pick(key, ["🚛", "🚚"], "f1i"), pick(key, ["2-3 Day Shipping", "Fast Delivery", "Quick Turnaround"], "f1h"),
         f"Delivery to all major {name} cities"),
        (pick(key, ["📦", "📊"], "f2i"), pick(key, ["Bulk Orders", "Volume Discounts", "Wholesale Pricing"], "f2h"),
         f"Discounts for multi-location {pick(key, SYN['businesses'],'f2b')}"),
        (pick(key, ["⚡", "🚨"], "f3i"), pick(key, ["Emergency Orders", "Rush Orders", "Expedited Service"], "f3h"),
         f"Fast shipping when you're running low"),
        (pick(key, ["🏢", "🗺️"], "f4i"), pick(key, ["Multi-Location", "One Account", "Central Billing"], "f4h"),
         f"One account, delivery to all your {name} locations"),
    ]

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{meta}">
    <link rel="canonical" href="https://psdepot.com/{key}.html">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{meta}">
    <meta property="og:image" content="https://psdepot.com/assets/images/og-image.png">
    <style>
        * {{ margin:0; padding:0; box-sizing:border-box; }}
        :root {{ --primary:#0A1A2F; --accent:#FF7A00; --bg:#F8F9FA; --text:#111111; }}
        body {{ font-family:'Inter',sans-serif; background:var(--bg); color:var(--text); line-height:1.6; }}
        .header {{ background:var(--primary); color:#fff; padding:14px 0; }}
        .header-inner {{ max-width:1200px; margin:0 auto; padding:0 24px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; }}
        .logo {{ font-size:23px; font-weight:800; color:#fff; text-decoration:none; }}
        .logo span {{ color:#63b3ed; }}
        .nav {{ background:#12283f; border-bottom:3px solid var(--accent); }}
        .nav-inner {{ max-width:1200px; margin:0 auto; padding:0 24px; display:flex; gap:4px; flex-wrap:wrap; }}
        .nav a {{ color:#bee3f8; text-decoration:none; font-weight:600; font-size:15px; padding:12px 18px; }}
        .hero {{ background:linear-gradient(135deg,#1a365d,#c53030,#002868); color:#fff; padding:80px 24px; text-align:center; }}
        .hero h1 {{ font-size:48px; font-weight:800; margin-bottom:16px; }}
        .hero .loc {{ font-size:56px; font-weight:900; text-shadow:2px 2px 4px rgba(0,0,0,.3); color:#ffd166; }}
        .features {{ padding:60px 24px; max-width:1200px; margin:0 auto; }}
        .grid {{ display:grid; grid-template-columns:repeat(4,1fr); gap:24px; margin-top:40px; }}
        .feature {{ background:#fff; border-radius:12px; padding:32px; text-align:center; box-shadow:0 2px 4px rgba(0,0,0,.1); }}
        .feature .icon {{ font-size:48px; margin-bottom:16px; }}
        .intro {{ padding:32px 24px; max-width:820px; margin:0 auto; text-align:center; font-size:17px; color:#2d3748; }}
        .cities {{ background:#fff; padding:40px 24px; max-width:1200px; margin:0 auto; border-radius:12px; }}
        .city-tag {{ background:var(--primary); color:#fff; padding:8px 20px; border-radius:20px; font-size:14px; }}
        .products {{ padding:60px 24px; max-width:1200px; margin:0 auto; }}
        .product-grid {{ display:grid; grid-template-columns:repeat(3,1fr); gap:24px; }}
        .product {{ background:#fff; border-radius:12px; padding:32px; border:1px solid #e2e8f0; text-align:center; }}
        .cta {{ background:var(--accent); color:#fff; padding:60px 24px; text-align:center; }}
        .cta a {{ display:inline-block; background:#fff; color:var(--primary); padding:16px 32px; border-radius:8px; text-decoration:none; font-weight:700; margin-top:16px; }}
        footer {{ background:var(--primary); color:#fff; padding:28px 24px; text-align:center; font-size:14px; }}
        @media(max-width:768px) {{ .hero h1 {{ font-size:26px; }} .grid {{ grid-template-columns:1fr 1fr; }} .product-grid {{ grid-template-columns:1fr; }} }}
    </style>
</head>
<body>
<header class="header"><div class="header-inner"><a href="/" class="logo">Performance<span>Supply</span>Depot</a><div style="display:flex;gap:20px;flex-wrap:wrap;align-items:center;font-size:14px;"><a href="tel:888-881-6834" style="color:#fff;text-decoration:none;font-weight:700;">📞 (888) 881-6834</a><a href="tel:415-571-9724" style="color:#bee3f8;text-decoration:none;">📞 (415) 571-9724</a><a href="mailto:info@psdepot.com" style="color:#bee3f8;text-decoration:none;">✉️ info@psdepot.com</a><a href="/checkout.html" style="background:#c53030;color:#fff;padding:8px 16px;border-radius:20px;font-weight:600;text-decoration:none;">🛒 Cart</a></div></div></header>
<nav class="nav"><div class="nav-inner"><a href="/">Home</a><a href="/products/index.html">Products</a><a href="/blog/index.html">Blog</a><a href="/services.html">Services</a><a href="/testimonials.html">Testimonials</a><a href="/about.html">About</a><a href="/resources/faq.html">FAQ</a><a href="/contact.html">Contact</a><a href="/locations.html">Service Areas</a></div></nav>

<section class="hero">
    <div class="loc">{name}</div>
    <h1>{h1}</h1>
    <p style="font-size:20px;max-width:700px;margin:0 auto;">{pick(key, SYN['fast'],'herofast').capitalize()} shipping of thermal paper rolls, receipt paper, and printer ribbons to {city1}, {city2}, {city3}, and all of {name}</p>
    <p style="margin-top:24px;font-size:18px;">📞 <a href="tel:888-881-6834" style="color:#fff;font-weight:700;text-decoration:none;">{phone}</a></p>
    <a href="tel:888-881-6834" class="cta" style="display:inline-block;padding:14px 28px;border-radius:8px;text-decoration:none;font-weight:700;margin-top:16px;color:var(--primary);background:#fff;">{pick(key, SYN['call'],'herocta')} for {name} Delivery</a>
</section>

<section class="features">
    <h2 style="text-align:center;font-size:36px;color:var(--primary);">{feat_head}</h2>
    <div class="grid">
        {''.join(f'''<div class="feature"><div class="icon">{f[0]}</div><h3>{f[1]}</h3><p>{f[2]}</p></div>''' for f in features)}
    </div>
</section>

<section class="intro">
    <h2 style="text-align:center;font-size:26px;color:var(--primary);margin-bottom:16px;">POS Supplies for {name} Businesses</h2>
    <p style="font-size:17px;line-height:1.7;color:#2d3748;">{industries} Performance Supply Depot ships thermal paper rolls, receipt paper, and printer ribbons to {name} businesses {pick(key, SYN['fast'],'introfast')} — with free nationwide delivery and a dedicated support team. {flavor}</p>
</section>

<section class="cities">
    <h2 style="text-align:center;font-size:28px;color:var(--primary);margin-bottom:16px;">Serving {name} {cities_label}</h2>
    <p style="text-align:center;color:#718096;margin-bottom:24px;">{pick(key, SYN['fast'],'cityfast').capitalize()} shipping to every major metro in {name}</p>
    <div style="display:flex;flex-wrap:wrap;gap:12px;justify-content:center;margin-top:24px;">
        {''.join(f'<span class="city-tag">{c}</span>' for c in cities)}
    </div>
</section>

<section class="products">
    <h2 style="text-align:center;font-size:32px;color:var(--primary);margin-bottom:40px;">Popular Products in {name}</h2>
    <div class="product-grid">
        {''.join(f'''<div class="product"><h3>{p[0]}</h3><p style="color:#718096;margin:16px 0;">{p[1]}</p><p style="font-size:24px;font-weight:700;color:var(--primary);">{p[2]}</p><a href="/" style="display:inline-block;margin-top:16px;color:var(--accent);font-weight:600;">Order Now →</a></div>''' for p in shown)}
    </div>
</section>

<section class="cta">
    <h2 style="font-size:42px;margin-bottom:16px;">{cta_head}</h2>
    <h3 style="font-size:28px;margin-bottom:24px;font-weight:400;">{cta_sub}</h3>
    <p style="font-size:20px;max-width:600px;margin:0 auto 24px;">We ship POS supplies to every corner of {name}. {flavor}</p>
    <a href="tel:888-881-6834">📞 {pick(key, SYN['call'],'ctacta')} {phone}</a>
</section>

<footer><div style="max-width:900px;margin:0 auto;"><p style="margin:0 0 10px;font-size:16px;"><strong>Performance Supply Depot LLC</strong></p><p style="margin:0 0 6px;">📞 <a href="tel:888-881-6834" style="color:#fff;text-decoration:none;font-weight:700;">(888) 881-6834</a> | 📞 <a href="tel:415-571-9724" style="color:#bee3f8;text-decoration:none;">(415) 571-9724</a> | ✉️ <a href="mailto:info@psdepot.com" style="color:#bee3f8;text-decoration:none;">info@psdepot.com</a></p><p style="margin:0 0 6px;color:#94a3b8;font-size:13px;">Authorized Dealer: <strong>SAM4S</strong> · <strong>CAS</strong> · <strong>ACM Technologies</strong> · <strong>TST Impresso</strong> · <strong>Capton</strong></p><p style="margin:0;color:#64748b;font-size:12px;">© 2026 Performance Supply Depot LLC. All rights reserved.</p></div></footer>

<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "Performance Supply Depot - {name}",
  "url": "https://psdepot.com/{key}.html",
  "telephone": "+1-888-881-6834",
  "areaServed": {{ "@type": "{'State' if ltype=='State' else 'City'}", "name": "{name}" }}
}}
</script>
</body>
</html>"""

    return html


if __name__ == "__main__":
    out_dir = os.path.join(os.path.dirname(__file__), "generated")
    os.makedirs(out_dir, exist_ok=True)
    for key, loc in LOCATIONS.items():
        with open(os.path.join(out_dir, f"{key}.html"), "w") as f:
            f.write(generate_page(key, loc))
    print(f"Generated {len(LOCATIONS)} unique location pages -> {out_dir}")
