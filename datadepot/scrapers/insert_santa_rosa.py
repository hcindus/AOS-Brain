#!/usr/bin/env python3
"""Insert Santa Rosa restaurant leads into DepotChaos unified.db (leads table)."""
import sqlite3, json, datetime

DB = "/root/.openclaw/workspace/data/depot_chaos/unified.db"

LEADS = [
 # name, phone, address, zip, category, business_type, website, email
 ("Sweet T's Restaurant + Bar","(707) 595-3935","2097 Stagecoach Rd Ste 100","95404","Restaurant / Bar","family style restaurant + bar","https://sweettssr.com","sweettssr@sweettssr.com"),
 ("Union Hotel Restaurant","(707) 538-6000","280 Mission Blvd","95409","American / Pizza","restaurant","https://theunionhotel.com",""),
 ("Carlos' Country Kitchen","(707) 569-9734","90 W College Ave","95401","Home Cooking / American","restaurant","",""),
 ("Ting Hau Restaurant","(707) 545-5204","717 4th St","95404","Chinese","restaurant","https://tinghau.com",""),
 ("Kirin Restaurant","(707) 525-1957","2700 Yulupa Ave Ste 3","95405","Asian / Family Style","restaurant","https://kirinsantarosa.com",""),
 ("Lita's Cafe","(707) 575-1628","1973 Mendocino Ave","95401","American / Coffee","cafe","https://litascafe.com",""),
 ("John Ash & Co","(707) 527-7687","4330 Barnes Rd","95403","American / Cocktail","fine dining","https://johnashandco.com",""),
 ("Shogun Japanese Restaurant","(707) 575-5557","2350 Midway Dr","95405","Japanese","restaurant","",""),
 ("Zazu Restaurant & Farm","(707) 523-4814","3535 Guerneville Rd","95401","Family Style / Catering","restaurant","http://zazurestaurant.com",""),
 ("Taqueria El Rodeo","(707) 528-1964","3577 Industrial Dr","95403","Mexican","restaurant","https://taqueriaelrodeo.com",""),
 ("Monti's Rotisserie & Bar","(707) 568-4404","714 Village Ct","95405","American / Chicken","restaurant","",""),
 ("El Charro Mexican Restaurant","(707) 570-2387","1529 Farmers Ln","95405","Mexican","restaurant","https://elcharromexican.com",""),
 ("Bellys Left Coast and Tap Room","(707) 526-5787","523 4th St","95401","American","restaurant / bar","",""),
 ("Cafe Citti","(707) 523-2690","2792 4th St","95405","Coffee / Italian","cafe","",""),
 ("Crepevine","(707) 577-8822","740 Farmers Ln","95405","American / Breakfast","restaurant","https://crepevine.com",""),
 ("Johnny Garlics","(707) 571-1800","1460 Farmers Ln","95405","American","restaurant","https://johnnygarlics.com",""),
 ("Trattoria Cattaneo","(707) 542-9050","2700 Yulupa Ave Ste 10","95405","Italian","restaurant","https://trattoriacattaneo.com","juliecattaneo@mac.com"),
 ("Mel's Fish & Chips","(707) 578-1954","1016 Hopper Ave","95403","Seafood","restaurant","https://melsfishandchips.com",""),
 ("Ca'Bianca Ristorante Italiano","(707) 542-5800","835 2nd St","95404","Italian","fine dining","https://cabianca.com",""),
 ("Toyo Restaurant","(707) 527-8871","3082 Marlow Rd Ste B3","95403","Japanese / Sushi","restaurant","https://toyosushi.com",""),
 ("Fabianis Ristorante","(707) 595-1177","505 Mendocino Ave","95401","Italian","restaurant","",""),
 ("BJ's Restaurants","(707) 303-1980","334 Coddingtown Ctr","95401","American / Pizza","restaurant (chain)","https://bjsrestaurants.com",""),
 ("The BBQ Spot","(707) 585-2616","3448 Santa Rosa Ave","95407","Barbecue","restaurant","http://thebbqspot.com",""),
 ("Norm Kitchen","(707) 579-4007","478 Larkfield Ctr","95403","Family Style","restaurant","",""),
 ("The Terrace Grille","(707) 523-4745","2777 4th St","95405","Family Style","restaurant","https://flamingoresort.com","hello@flamingoresort.com"),
 ("Thai House","(707) 526-3939","525 4th St","95401","Thai","restaurant","https://thaihousesantarosa.com","thaihousesantarosa@gmail.com"),
 ("Ike's Place","(707) 293-9814","1780 Mendocino Ave","95401","American / Sandwiches","restaurant (chain)","https://ikesloveandsandwiches.com",""),
 ("Sea Thai Bistro","(707) 528-8333","2350 Midway Dr","95405","Thai","restaurant","https://seathaibistro.com","info@seathaibistro.com"),
 ("Chelino's Mexican Restaurant","(707) 571-7478","1079 4th St","95404","Mexican","restaurant","https://chelinos.com","contactus@chelinos.net"),
 ("Royal China Restaurant","(707) 545-2911","3080 Marlow Rd Ste A4","95403","Chinese","restaurant","",""),
]

SOURCE = "Santa_Rosa_Yelp"
now = datetime.datetime.utcnow().isoformat()

conn = sqlite3.connect(DB)
cur = conn.cursor()

inserted = 0
skipped = []
for name, phone, address, zipc, category, btype, website, email in LEADS:
    # dedupe by business_name + city
    cur.execute("SELECT id FROM leads WHERE business_name = ? AND city = 'Santa Rosa' AND state = 'CA'", (name,))
    if cur.fetchone():
        skipped.append(name)
        continue
    tags = "santa-rosa,restaurant"
    notes = None
    if website:
        notes = f"Website: {website}"
    cur.execute("""
        INSERT INTO leads (
            business_name, city, state, zip, phone, email, category, business_type,
            address, source, source_type, status, priority, tier, tags, assigned_dept,
            notes, created_at, deleted, is_customer
        ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (name, "Santa Rosa", "CA", zipc, phone, email, category, btype,
          address, SOURCE, "yelp_directory", "new", "normal", None, tags, "datadepot_sales",
          notes, now, 0, 0))
    inserted += 1

conn.commit()
total = cur.execute("SELECT COUNT(*) FROM leads WHERE deleted = 0").fetchone()[0]
conn.close()

print(f"Inserted: {inserted}")
print(f"Skipped (already exists): {len(skipped)}")
for s in skipped: print("  -", s)
print(f"Total leads in DB: {total}")
