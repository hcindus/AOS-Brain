#!/usr/bin/env python3
"""Find emails for Santa Rosa restaurants via direct domain guessing + fetch."""
import requests, re, json, time
from urllib.parse import urljoin

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36"
S = requests.Session()
S.headers.update({"User-Agent": UA, "Accept-Language": "en-US,en;q=0.9"})

# name -> [candidate domains]
CANDS = {
 "Sweet T's Restaurant + Bar": ["sweettssr.com"],
 "Union Hotel Restaurant": ["theunionhotel.com","unionhotelsantarosa.com","unionhotel.com","unionhotelsr.com"],
 "Carlos' Country Kitchen": ["carloscountrykitchen.com","carloscountrykitchensantarosa.com"],
 "Ting Hau Restaurant": ["tinghau.com","tinghaurestaurant.com"],
 "Kirin Restaurant": ["kirinsantarosa.com","kirinrestaurant.com","kirinrestaurantsr.com"],
 "Lita's Cafe": ["litascafe.com","litascafesr.com"],
 "John Ash & Co": ["johnashandco.com","vintnersinn.com","johnash.com"],
 "Shogun Japanese Restaurant": ["shogunjapanesesr.com","shogunsr.com","shogunsantarosa.com"],
 "Zazu Restaurant & Farm": ["zazurestaurant.com","zazukitchen.com","zazufarm.com"],
 "Taqueria El Rodeo": ["taqueriaelrodeo.com","elrodeotaqueria.com"],
 "Monti's Rotisserie & Bar": ["montisrestaurant.com","montisrotisserie.com","montissr.com"],
 "El Charro Mexican Restaurant": ["elcharrosr.com","elcharrosantarosa.com","elcharromexican.com"],
 "Bellys Left Coast and Tap Room": ["bellysleftcoast.com","bellysleftcoasttaproom.com","bellysleftcoastsr.com"],
 "Cafe Citti": ["cafecitti.com","caffecitti.com","cafecittisr.com"],
 "Crepevine": ["crepevine.com"],
 "Johnny Garlics": ["johnnygarlics.com"],
 "Trattoria Cattaneo": ["trattoriacattaneo.com","trattoriacattaneosr.com"],
 "Mel's Fish & Chips": ["melsfishandchips.com","melsfishchips.com","melsfishandchipssr.com"],
 "Ca'Bianca Ristorante Italiano": ["cabianca.com","cabiancaristorante.com","cabiancasr.com"],
 "Toyo Restaurant": ["toyosr.com","toyorestaurant.com","toyosushi.com","toyosantarosa.com"],
 "Fabianis Ristorante": ["fabianis.com","fabianisristorante.com","fabianisr.com"],
 "BJ's Restaurants": ["bjsrestaurants.com"],
 "The BBQ Spot": ["thebbqspot.com","bbqspotsr.com","bbqspotsantarosa.com"],
 "Norm Kitchen": ["normkitchen.com","normkitchensr.com"],
 "The Terrace Grille": ["theterracegrille.com","terracegrillesr.com","flamingoresort.com"],
 "Thai House": ["thaihousesr.com","thaihousesantarosa.com","thaihouserestaurant.com"],
 "Ike's Place": ["ikesloveandsandwiches.com","ikesplace.com"],
 "Sea Thai Bistro": ["seathaibistro.com","seathaibistrosr.com"],
 "Chelino's Mexican Restaurant": ["chelinos.com","chelinosmexican.com","chelinosr.com"],
 "Royal China Restaurant": ["royalchinasr.com","royalchinasantarosa.com","royalchinarestaurant.com"],
}

JUNK = {"sentry.io","wixpress.com","example.com","schema.org","s3.amazonaws.com","cloudinary.com",
 "wix.com","squarespace.com","godaddy.com","w3.org","doubleclick.net","google.com","gstatic.com",
 "facebook.com","instagram.com","yelp.com","tripadvisor.com","grubhub.com","doordash.com","ubereats.com",
 "opentable.com","toasttab.com","squareup.com","square.site","clover.com","gravatar.com","twimg.com",
 "cdn.shopify.com","pinterest.com","linkedin.com","twitter.com","x.com","wixstatic.com","sndcdn.com"}
EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}")

def emails_from(text):
    out=set()
    for e in EMAIL_RE.findall(text or ""):
        e=e.strip().strip(".").lower()
        if not e or e.endswith((".png",".jpg",".jpeg",".gif",".webp",".svg",".css",".js")): continue
        dom=e.split("@")[-1]
        if dom in JUNK or any(d in dom for d in JUNK): continue
        out.add(e)
    return sorted(out)

def fetch(u):
    try:
        r=S.get(u, timeout=12, allow_redirects=True)
        if r.status_code==200: return r.text
    except Exception: pass
    return ""

def probe(name, domains):
    for d in domains:
        for scheme in ("https://","http://"):
            base=scheme+d
            try:
                r=S.get(base, timeout=12, allow_redirects=True)
            except Exception:
                continue
            if r.status_code==200:
                final=r.url
                em=emails_from(r.text)
                site=base
                # check contact/about
                for suf in ("/contact","/contact-us","/about","/about-us","/contact.html","/contact-us.html"):
                    ch=fetch(urljoin(final, suf))
                    e2=emails_from(ch)
                    em=list(set(em)|set(e2))
                return {"website":site,"final":final,"emails":sorted(em)}
        time.sleep(0.3)
    return {"website":None,"final":None,"emails":[]}

def main():
    out={}
    for name, doms in CANDS.items():
        r=probe(name, doms)
        out[name]=r
        print(f"{name}: {r['website']} emails={r['emails']}", flush=True)
        time.sleep(0.5)
    with open("/root/.openclaw/workspace/datadepot/scrapers/santa_rosa_emails2.json","w") as f:
        json.dump(out,f,indent=2)
    print("DONE")

if __name__=="__main__":
    main()
