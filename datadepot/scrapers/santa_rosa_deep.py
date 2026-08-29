#!/usr/bin/env python3
"""Deeper email extraction for Santa Rosa restaurant sites already found."""
import requests, re, json, time
from urllib.parse import urljoin

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36"
S = requests.Session()
S.headers.update({"User-Agent": UA, "Accept-Language": "en-US,en;q=0.9"})

SITES = {
 "Sweet T's Restaurant + Bar":"https://sweettssr.com",
 "Union Hotel Restaurant":"https://theunionhotel.com",
 "Ting Hau Restaurant":"https://tinghau.com",
 "Kirin Restaurant":"https://kirinsantarosa.com",
 "Lita's Cafe":"https://litascafe.com",
 "John Ash & Co":"https://johnashandco.com",
 "Zazu Restaurant & Farm":"http://zazurestaurant.com",
 "Taqueria El Rodeo":"https://taqueriaelrodeo.com",
 "El Charro Mexican Restaurant":"https://elcharromexican.com",
 "Crepevine":"https://crepevine.com",
 "Johnny Garlics":"https://johnnygarlics.com",
 "Trattoria Cattaneo":"https://trattoriacattaneo.com",
 "Mel's Fish & Chips":"https://melsfishandchips.com",
 "Ca'Bianca Ristorante Italiano":"https://cabianca.com",
 "Toyo Restaurant":"https://toyosushi.com",
 "BJ's Restaurants":"https://bjsrestaurants.com",
 "The BBQ Spot":"http://thebbqspot.com",
 "The Terrace Grille":"https://flamingoresort.com",
 "Thai House":"https://thaihousesantarosa.com",
 "Ike's Place":"https://ikesloveandsandwiches.com",
 "Sea Thai Bistro":"https://seathaibistro.com",
 "Chelino's Mexican Restaurant":"https://chelinos.com",
}

JUNK = {"sentry.io","wixpress.com","example.com","schema.org","s3.amazonaws.com","cloudinary.com",
 "wix.com","squarespace.com","godaddy.com","w3.org","doubleclick.net","google.com","gstatic.com",
 "facebook.com","instagram.com","yelp.com","tripadvisor.com","grubhub.com","doordash.com","ubereats.com",
 "opentable.com","toasttab.com","squareup.com","square.site","clover.com","gravatar.com","twimg.com",
 "cdn.shopify.com","pinterest.com","linkedin.com","twitter.com","x.com","wixstatic.com","sndcdn.com",
 "kwickpos.com","posupgrades.com","gmail.com","mail.com","mac.com","gstatic.com","schema.org",
 "fonts.googleapis.com","google-analytics.com","googletagmanager.com"}
EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}")

def emails_from(text):
    out=set()
    for e in EMAIL_RE.findall(text or ""):
        e=e.strip().strip(".").lower()
        if not e or e.endswith((".png",".jpg",".jpeg",".gif",".webp",".svg",".css",".js")): continue
        dom=e.split("@")[-1]
        if dom in JUNK: continue
        # skip emails whose domain is a known free/provider, unless it's the actual contact
        out.add(e)
    return sorted(out)

def fetch(u):
    try:
        r=S.get(u, timeout=12, allow_redirects=True)
        if r.status_code==200: return r.text
    except Exception: pass
    return ""

SUFFIXES = ["/contact","/contact-us","/about","/about-us","/contact.html","/contact-us.html",
            "/reservations","/reservation","/location","/locations","/order","/order-online",
            "/menu","/hours","/info","/pages/contact","/pages/contact-us"]

def crawl(base):
    final_emails=set()
    pages=[base]
    # homepage first
    h=fetch(base)
    if h:
        em=emails_from(h)
        final_emails.update(em)
        # collect internal links
        links=set()
        for m in re.findall(r'href=["\']([^"\']+)["\']', h):
            if m.startswith("/") or base.rstrip('/') in m:
                links.add(urljoin(base, m))
        # add contact-ish links
        for l in links:
            if any(k in l.lower() for k in ("contact","about","location","info","hours","reserv")):
                pages.append(l)
    # suffixes
    for suf in SUFFIXES:
        pages.append(urljoin(base, suf))
    # fetch pages (dedup, limit)
    seen=set()
    for p in pages:
        if p in seen: continue
        seen.add(p)
        t=fetch(p)
        if t:
            em=emails_from(t)
            final_emails.update(em)
            # mailto
            for mm in re.findall(r'mailto:([^"\'\s>]+)', t):
                e=mm.split("?")[0].strip().lower()
                if "@" in e: final_emails.add(e)
    return sorted(final_emails)

def main():
    out={}
    for name, base in SITES.items():
        em=crawl(base)
        out[name]=em
        print(f"{name}: {em}", flush=True)
        time.sleep(0.4)
    with open("/root/.openclaw/workspace/datadepot/scrapers/santa_rosa_deep.json","w") as f:
        json.dump(out,f,indent=2)
    print("DONE")

if __name__=="__main__":
    main()
