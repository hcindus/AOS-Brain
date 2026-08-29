#!/usr/bin/env python3
"""
Scrape emails for Santa Rosa, CA restaurants (from Yelp list).
For each restaurant: search Bing -> find website -> fetch site + contact page -> extract emails.
Output: santa_rosa_leads.json
"""
import requests, re, json, base64, time, sys
from urllib.parse import unquote, urlparse, urljoin

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36"
S = requests.Session()
S.headers.update({"User-Agent": UA, "Accept-Language": "en-US,en;q=0.9"})

RESTAURANTS = [
    {"name":"Sweet T's Restaurant + Bar","phone":"(707) 595-3935","address":"2097 Stagecoach Rd Ste 100","zip":"95404","category":"Restaurant/Bar","type":"family style / bar"},
    {"name":"Union Hotel Restaurant","phone":"(707) 538-6000","address":"280 Mission Blvd","zip":"95409","category":"American / Pizza","type":"restaurant"},
    {"name":"Carlos' Country Kitchen","phone":"(707) 569-9734","address":"90 W College Ave","zip":"95401","category":"Home Cooking / American","type":"restaurant"},
    {"name":"Ting Hau Restaurant","phone":"(707) 545-5204","address":"717 4th St","zip":"95404","category":"Chinese","type":"restaurant"},
    {"name":"Kirin Restaurant","phone":"(707) 525-1957","address":"2700 Yulupa Ave Ste 3","zip":"95405","category":"Asian / Family Style","type":"restaurant"},
    {"name":"Lita's Cafe","phone":"(707) 575-1628","address":"1973 Mendocino Ave","zip":"95401","category":"American / Coffee","type":"cafe"},
    {"name":"John Ash & Co","phone":"(707) 527-7687","address":"4330 Barnes Rd","zip":"95403","category":"American / Cocktail","type":"fine dining"},
    {"name":"Shogun Japanese Restaurant","phone":"(707) 575-5557","address":"2350 Midway Dr","zip":"95405","category":"Japanese","type":"restaurant"},
    {"name":"Zazu Restaurant & Farm","phone":"(707) 523-4814","address":"3535 Guerneville Rd","zip":"95401","category":"Family Style / Catering","type":"restaurant"},
    {"name":"Taqueria El Rodeo","phone":"(707) 528-1964","address":"3577 Industrial Dr","zip":"95403","category":"Mexican","type":"restaurant"},
    {"name":"Monti's Rotisserie & Bar","phone":"(707) 568-4404","address":"714 Village Ct","zip":"95405","category":"American / Chicken","type":"restaurant"},
    {"name":"El Charro Mexican Restaurant","phone":"(707) 570-2387","address":"1529 Farmers Ln","zip":"95405","category":"Mexican","type":"restaurant"},
    {"name":"Bellys Left Coast and Tap Room","phone":"(707) 526-5787","address":"523 4th St","zip":"95401","category":"American","type":"restaurant/bar"},
    {"name":"Cafe Citti","phone":"(707) 523-2690","address":"2792 4th St","zip":"95405","category":"Coffee / Italian","type":"cafe"},
    {"name":"Crepevine","phone":"(707) 577-8822","address":"740 Farmers Ln","zip":"95405","category":"American / Breakfast","type":"restaurant"},
    {"name":"Johnny Garlics","phone":"(707) 571-1800","address":"1460 Farmers Ln","zip":"95405","category":"American","type":"restaurant"},
    {"name":"Trattoria Cattaneo","phone":"(707) 542-9050","address":"2700 Yulupa Ave Ste 10","zip":"95405","category":"Italian","type":"restaurant"},
    {"name":"Mel's Fish & Chips","phone":"(707) 578-1954","address":"1016 Hopper Ave","zip":"95403","category":"Seafood","type":"restaurant"},
    {"name":"Ca'Bianca Ristorante Italiano","phone":"(707) 542-5800","address":"835 2nd St","zip":"95404","category":"Italian","type":"fine dining"},
    {"name":"Toyo Restaurant","phone":"(707) 527-8871","address":"3082 Marlow Rd Ste B3","zip":"95403","category":"Japanese / Sushi","type":"restaurant"},
    {"name":"Fabianis Ristorante","phone":"(707) 595-1177","address":"505 Mendocino Ave","zip":"95401","category":"Italian","type":"restaurant"},
    {"name":"BJ's Restaurants","phone":"(707) 303-1980","address":"334 Coddingtown Ctr","zip":"95401","category":"American / Pizza","type":"restaurant (chain)"},
    {"name":"The BBQ Spot","phone":"(707) 585-2616","address":"3448 Santa Rosa Ave","zip":"95407","category":"Barbecue","type":"restaurant"},
    {"name":"Norm Kitchen","phone":"(707) 579-4007","address":"478 Larkfield Ctr","zip":"95403","category":"Family Style","type":"restaurant"},
    {"name":"The Terrace Grille","phone":"(707) 523-4745","address":"2777 4th St","zip":"95405","category":"Family Style","type":"restaurant"},
    {"name":"Thai House","phone":"(707) 526-3939","address":"525 4th St","zip":"95401","category":"Thai","type":"restaurant"},
    {"name":"Ike's Place","phone":"(707) 293-9814","address":"1780 Mendocino Ave","zip":"95401","category":"American / Sandwiches","type":"restaurant (chain)"},
    {"name":"Sea Thai Bistro","phone":"(707) 528-8333","address":"2350 Midway Dr","zip":"95405","category":"Thai","type":"restaurant"},
    {"name":"Chelino's Mexican Restaurant","phone":"(707) 571-7478","address":"1079 4th St","zip":"95404","category":"Mexican","type":"restaurant"},
    {"name":"Royal China Restaurant","phone":"(707) 545-2911","address":"3080 Marlow Rd Ste A4","zip":"95403","category":"Chinese","type":"restaurant"},
]

JUNK_DOMAINS = {
    "sentry.io","wixpress.com","example.com","schema.org","s3.amazonaws.com",
    "cloudinary.com","wix.com","squarespace.com","godaddy.com","w3.org",
    "doubleclick.net","google.com","gstatic.com","facebook.com","instagram.com",
    "yelp.com","tripadvisor.com","grubhub.com","doordash.com","ubereats.com",
    "opentable.com","toasttab.com","squareup.com","square.site","clover.com",
    "mealkeyway.com","sndcdn.com","gravatar.com","twimg.com","cdn.shopify.com",
    "sentry.io","wixstatic.com","pinterest.com","linkedin.com","twitter.com","x.com",
}
EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}")

def decode_bing_url(u):
    """Decode Bing /ck/a redirect u= param (base64url, prefixed a1)."""
    try:
        s = u
        if s.startswith("a1"):
            s = s[2:]
        s = s.replace("-", "+").replace("_", "/")
        s += "=" * (-len(s) % 4)
        return base64.b64decode(s).decode("utf-8", "ignore")
    except Exception:
        return None

def search_bing(query):
    out = []
    try:
        r = S.get("https://www.bing.com/search", params={"q": query}, timeout=15)
        if r.status_code != 200:
            return out
        for m in re.findall(r'href="([^"]*bing\.com/ck/a[^"]*)"', r.text):
            mm = re.search(r'[?&]u=([^&"]+)', m)
            if mm:
                url = decode_bing_url(mm.group(1))
                if url:
                    out.append(url)
    except Exception as e:
        pass
    return out

def is_candidate(url):
    try:
        host = urlparse(url).netloc.lower()
        if not host:
            return False
        if any(d in host for d in JUNK_DOMAINS):
            return False
        return True
    except Exception:
        return False

def extract_emails(text):
    found = set()
    for e in EMAIL_RE.findall(text or ""):
        e = e.strip().strip(".").lower()
        if not e or e.endswith((".png",".jpg",".jpeg",".gif",".webp",".svg")):
            continue
        dom = e.split("@")[-1]
        if dom in JUNK_DOMAINS or any(d in dom for d in JUNK_DOMAINS):
            continue
        # skip obvious asset/noise
        if dom in ("2x.png","wixpress.com","sentry.io"):
            continue
        found.add(e)
    return sorted(found)

def fetch(url, timeout=12):
    try:
        r = S.get(url, timeout=timeout, allow_redirects=True)
        if r.status_code == 200:
            return r.text
    except Exception:
        pass
    return ""

def scrape_one(rst):
    name = rst["name"]
    result = dict(rst)
    result["website"] = None
    result["emails"] = []
    result["sources"] = []
    # search
    queries = [
        f'"{name}" Santa Rosa website',
        f'{name} Santa Rosa CA',
    ]
    candidates = []
    for q in queries:
        for u in search_bing(q):
            if is_candidate(u) and u not in candidates:
                candidates.append(u)
        if candidates:
            break
        time.sleep(1)
    # rank: prefer non-yelp/non-map domains
    result["sources"] = candidates[:8]
    # fetch candidates, look for contact/email
    for u in candidates[:4]:
        html = fetch(u)
        if not html:
            continue
        # homepage emails
        em = extract_emails(html)
        if em and not result["emails"]:
            result["emails"] = em
            result["website"] = u
            break
        # try /contact, /about, /contact-us
        for suffix in ("/contact", "/contact-us", "/about", "/about-us"):
            cu = urljoin(u, suffix)
            ch = fetch(cu)
            em = extract_emails(ch)
            if em:
                result["emails"] = em
                result["website"] = u
                result["contact_url"] = cu
                break
        if result["emails"]:
            break
        time.sleep(0.5)
    return result

def main():
    results = []
    for i, rst in enumerate(RESTAURANTS):
        r = scrape_one(rst)
        results.append(r)
        print(f"[{i+1}/{len(RESTAURANTS)}] {rst['name']}: website={r.get('website')} emails={r.get('emails')}", flush=True)
        time.sleep(1)
    with open("/root/.openclaw/workspace/datadepot/scrapers/santa_rosa_leads.json", "w") as f:
        json.dump(results, f, indent=2)
    print("DONE. Saved to santa_rosa_leads.json")

if __name__ == "__main__":
    main()
