#!/usr/bin/env python3
"""Performance Supply Depot — master product catalog builder.

Reads the LIVE local product pages under /var/www/psdepot-v0/products/ (recursive,
excluding _archive / _archive_thin / staging / dot-dirs) and emits:
  * /var/www/psdepot-v0/catalog.csv         (7 columns; the future single source of truth)
  * /root/.openclaw/workspace/datadepot/catalog_gaps.md   (honest coverage & gaps report)

Policy:
  - USE WHAT WE HAVE. We never invent a part number; we only lift ones already on a
    page (json-ld sku / filename / schema "sku"). A missing tier is left blank & flagged.
  - Tier1 "our" part number = any sku / identifier with a PSD- prefix.
  - Tier2 "internal" part number = the numeric lookup code (XX-XXX, XXXX, model codes).
  - Category & brand are best-effort inferences (documented differences possible).
  - Pages that are category/index/tile landing pages (not a single sellable part number)
    are excluded from the catalog rows and listed with a reason in the gaps report.
"""
import re, json, os, csv, html as H

ROOT      = '/var/www/psdepot-v0/products/'
SITE      = 'https://psdepot.com'
CSV_OUT   = '/var/www/psdepot-v0/catalog.csv'
GAPS_OUT  = '/root/.openclaw/workspace/datadepot/catalog_gaps.md'

EXCLUDE_DIRS = {'_archive','_archive_thin','staging'}
# Catalog-page .html files that are category/index/tile landing pages (no own SKU)
UTILITY_FILES = {
    'index.html',
    'printer-ribbons.html',        # collection hub (ribbons gallery)
    'cash-drawers.html',           # collection hub
    'thermal-paper.html',          # CollectionPage hub listing other paper SKUs
    'capton-pouring-systems.html', # brand intro/landing
    'lucki-tile.html',             # embedded "product tile" UI component demo
}
GENERIC_IMG = {'og-image.png','og-image.jpg','og-image.webp','logo.png',
               'ms-cashdrawer-logo.png','capton-logo.png','clarion-logo.jpg'}
RETAILER_BRANDS = {'performance supply depot','performance supply','psd'}

# ---------------- tiny text helpers ----------------------------------------
def clean(v):
    if v is None: return ''
    if isinstance(v,(int,float)): return str(v)
    return re.sub(r'[ \t\r\n]+',' ',str(v)).strip()

def unesc(s): return H.unescape(s)

def meta_attr(html, attr, val):
    pat = re.compile(r'<meta\b[^>]*?\b'+re.escape(attr)+r'\s*=\s*["\']'+re.escape(val)+
                     r'["\'][^>]*?\bcontent\s*=\s*["\'](.*?)["\']', re.S|re.I)
    m   = pat.search(html)
    if not m:
        pat = re.compile(r'<meta\b[^>]*?\bcontent\s*=\s*["\'](.*?)["\'][^>]*?\b'+
                         re.escape(attr)+r'\s*=\s*["\']'+re.escape(val)+r'["\']', re.S|re.I)
        m = pat.search(html)
    return unesc(m.group(1)).strip() if m else None

def og_image(html):
    for a in ('property','name'):
        v = meta_attr(html,a,'og:image') or meta_attr(html,a,'twitter:image')
        if v: return v
    return None

def site_desc(html):
    return meta_attr(html,'name','description') or meta_attr(html,'property','og:description') or None

def parse_items(html):
    """every Product/IndividualProduct/Service json-ld node, flattened."""
    out=[]
    for b in re.findall(r'<script[^>]*application/ld\+json[^>]*>(.*?)</script>',html,re.S):
        try: d=json.loads(b)
        except Exception: continue
        def walk(o):
            if isinstance(o,dict):
                t=o.get('@type')
                if isinstance(t,str) and t in ('Product','IndividualProduct','Service'):
                    out.append(o)
                for v in o.values(): walk(v)
            elif isinstance(o,list):
                for x in o: walk(x)
        walk(d)
    return out

def h1_text(html):
    m=re.search(r'<h1[^>]*>(.*?)</h1>',html,re.S)
    return clean(re.sub(r'<[^>]+>',' ',m.group(1))) if m else ''

def first_title(html):
    m=re.search(r'<title[^>]*>(.*?)</title>',html,re.S)
    return clean(m.group(1)) if m else ''

def img_srcs(html):
    return [m for m in re.findall(r'<img[^>]*?\bsrc=["\']([^"\']+)["\']',html,re.I)]

def is_generic(url):
    b=os.path.basename(unesc(url).split('?')[0]).lower()
    return (b in GENERIC_IMG) or ('/vendor' in url) or (b.startswith('logo')) or (b=='favicon.svg')

def normalize_url(u, path):
    u=unesc(u).strip()
    if not u or u.startswith('data:'): return ''
    if u.startswith('//'): u='https:'+u
    elif u.startswith('/'): u=SITE+u
    elif not u.startswith('http'):
        d=os.path.dirname(path).replace(ROOT,'').lstrip('/')
        pre=('/products/'+d+'/') if d else '/products/'
        u=SITE+pre+u if not u.startswith('/') else SITE+u
    return u.split('#')[0].strip()

def numeric_price(it):
    off=it.get('offers')
    def _one(o):
        if not isinstance(o,dict): return None
        return o.get('price')
    p=None
    if isinstance(off,dict): p=_one(off)
    elif isinstance(off,list):
        for o in off:
            q=_one(o)
            if q is not None: p=q; break
    try: return float(p)
    except Exception: return None

# ---------------- word token utilities -------------------------------------
def tok_list(*texts):
    s=' '.join(x for x in texts if x)
    return re.findall(r'[a-z0-9]+', s.lower())

def phrase_in(words, text, phrase):
    """phrase e.g. 'cash register' (dash or space insensitive)"""
    ph=phrase.lower().replace('-',' ').split()
    n=len(words); L=len(ph)
    for i in range(n-L+1):
        if words[i:i+L]==ph: return True
    return False

# ---------------- BRAND ----------------------------------------------------
BRAND_TOKEN=[('sam4s','SAM4S'),('sam4','SAM4S'),
 ('mscashdrawer','MS Cash Drawer'),('mscash','MS Cash Drawer'),('cashdrawer','MS Cash Drawer'),
 ('epson','Epson'),('bixolon','Bixolon'),('star','Star'),('capton','Capton'),('cas','CAS'),
 ('godex','Godex'),('datamax','Datamax'),('maxstick','MaxStick'),('iconex','Iconex'),
 ('icon','Iconex'),('berkel','Berkel'),('hobart','Hobart'),('kilotech','Kilotech'),
 ('tec','TEC'),('poynt','Poynt'),('ncc','NCC'),('microsale','Microsale'),('maitre','Clover'),
 ('datacap','Datacap'),('code','Code'),('orionstar','OrionStar'),('clarion','Clarion'),
 ('dell','Dell'),('cisco','Cisco'),('apple','Apple'),('quantum','Hobart')]

def infer_brand(filename_words, title_words, name_words, prods):
    hits=set()
    for w in list(filename_words)+list(title_words)+list(name_words):
        for tok,lab in BRAND_TOKEN:
            if w==tok: hits.add(lab)
    for it in prods:
        br=it.get('brand')
        if isinstance(br,list) and br and isinstance(br[0],dict): br=br[0].get('name')
        elif isinstance(br,dict): br=br.get('name')
        bb=clean(br).strip()
        if bb and bb.lower() not in RETAILER_BRANDS: hits.add(bb)
    if not hits: return 'other'
    # If only PSD-ish removed, other
    # deterministic: prefer shortest manufacturer or one appearing in filename?
    # Pick first matching in the fixed order that is actually present
    for tok,lab in BRAND_TOKEN:
        if lab in hits: return lab
    return sorted(hits)[0]

# ---------------- CATEGORY -------------------------------------------------
def infer_category(words, name_words, price, brand, subdir):
    """Return category from product words. words = filename words + canonical name."""
    w=words
    def has(*ks): return any(k in w for k in ks)
    def has_ph(*ph):
        for p in ph:
            if phrase_in(w,' '.join(w),p): return True
        return False
    text=' '.join(w)
    # ---- strong singular product groups first ---------------------------
    if has('robot') or has('lucki'):               return 'delivery-robot'
    if has('pourer','pourlink') and not has('award'): return 'bar-supplies'
    if has('pinpad') or has_ph('payment station') or has('datacap') or has('netepay') or has_ph('net epay'):
        return 'payment-pinpad'
    if has('drawer') or has('till') or has('coin') and has('bill'):
        if has('drawer') or has('till') or has_ph('cash drawer'):
            return 'cash-drawer'
    if has('scale') or has('cl5500','cl7200','pd2z','lp-1000n','lp1000n','pdn','s2000','sw-rs','r457'):
        return 'pos-scale'
    if has('scanner') or has('barcode') or has('cr2515','cr950'):
        if has_ph('pos scanner','barcode scanner') or has('scanner') or has('barcode','cr2515','cr950'):
            return 'barcode-scanner'
    if has('register') or has('ecr') or has('journal') or has('cashreg') or has_ph('electronic journal'):
        if has('register') or has('ecr') or has('journal') or has('kiosk') or has('terminal'):
            # some ECR/register pages have keyboard ; all are e-cash-register
            return 'cash-register'
    if has('astra') or has('kiosk') or has('sapphire') or has_ph('pos terminal') or \
       (has('terminal') and (has('android') or has('pos') or has('term'))):
        if has('register') or has('ecr'): return 'cash-register'
        return 'pos-terminal'
    if has('tablet') or has_ph('pos tablet','android tablet'):
        if has('printer'): pass
        return 'pos-tablet'
    if has('workstation') or has('ws' ):
        # replacements become components
        if has('replacement','touchscreen','rear','pole','display','lcd','msr','hard drive','power brick','cable'):
            return 'pos-workstation-component'
        return 'pos-workstation'
    if has_ph('pos software') or has('software') or has('maitre') or has('microsale') or (has('ncc') and has_ph('pos software')) or has_ph('database creation','ore install'):
        return 'pos-software'
    if has_ph('kitchen video','kitchen display','video station') or has('bump') and has_ph('bump bar') :
        return 'kitchen-display-system'
    if (has('printer') and (has('thermal') or has_ph('thermal printer','pos thermal'))) or has_ph('thermal head') and has('cleaner'):
        return 'receipt-printer-thermal'
    if has('printer') and (has('impact') or has('matrix') or has_ph('impact printer','dot matrix')) or has_ph('receipt & journal','receipt & journal printers') or has('dual station') and has('receipt'):
        return 'receipt-printer-impact'
    if has('printer') and (has('label') or has('tag') or has_ph('shelf tag','label printer','tag printer')):
        if has_ph('shelf tag','label printer','tag printer') or (has('printer') and (has('label','tag','shelf'))):
            return 'label-printer'
    if has('printer') or has_ph('receipt printer','thermal printer','impact printer','report printer','office printer'):
        if has_ph('office printer','report printer') or has('office','report'):
            if has('office') or has('report'): return 'office-print-copy'
        if has('thermal') or has_ph('thermal printer'): return 'receipt-printer-thermal'
        return 'receipt-printer'
    # ---- consumables -----------------------------------------------------
    if has('ribbon') or has('erc') or has_ph('erc ribbons','ink ribbon','pos ribbon'):
        return 'printer-ribbon'
    if (has('label') and not has('printer')) or has('maxstick') or has('iconex') or has_ph('shelf tag') or has('godex'):
        return 'consumables-labels'
    # paper
    if has_ph('thermal paper','thermal-paper') or (has('thermal') and has('paper')) or has_ph('pos paper','credit card paper') :
        if (has('printer') or has_ph('thermal printer')):   # a printer page handled above
            pass
        else: return 'thermal-paper'
    if has('carbonless') or has('ply') or (has('ply') and has('paper')) or has('44mm') or has_ph('bond paper'):
        return 'paper-multipart'
    if has('paper') or has('paper-roll') or has_ph('paper roll','paper rolls','register paper'):
        return 'thermal-paper'
    # swipe / ancillary supplies
    if has_ph('swipe card') or has('swipecard') or has_ph('retractable reel'):
        return 'cash-accessory'
    if has('cleaner') or has_ph('cleaner card','cleaner pen','msr cleaner','thermal head cleaner') or has('sanitizer','gas','pen') and has('cleaner') :
        return 'maintenance-consumable'
    if has('silicone') or has_ph('cover','screen cover','keyboard cover','protective cover'):
        return 'maintenance-consumable'
    if has('security') or has('lock') : return 'cash-register-accessory'
    # network / power
    if has('switch') or has('router') or has('accesspoint') or has_ph('access point') or has('poe') or has('kvm'):
        return 'networking'
    if has('ups') or has_ph('power conditioner') or has('pwc') or has('brick'):
        if has('brick') and not (has('ups') or has('pwc') ): return 'power-supply'
        return 'power-protection'
    # labor & parts
    if has('labor') or has_ph('travel to site','help desk','day rate','database creation','in-shop','on-site') or has('hardware'):
        if has('labor'): return 'service-labor'
        if (has('review') or has('callback')): return 'service-labor'
    if has('repair') or has('part') or has('install'):
        return 'repair-parts'
    # ---- office / generic ------------------------------------------------
    if has('dell') or has('monitor') or has('office') or has('pc'):
        if has('pc') and has('monitor') and has('office'): return 'office-equipment'
        if has('monitor') and not has('workstation'):
            return 'office-equipment'
        if has('dell') or has('pc') : return 'office-equipment'
    if has('laptop') or has('cpu'): return 'office-equipment'
    # known legacy numeric families
    if brand=='Hobart' or has('quantum'): return 'pos-scale'
    if brand=='Berkel' or brand=='Kilotech' or brand=='TEC': return 'pos-scale'
    return 'other'


# ============================== DRIVER =====================================

def slot_of(sku):
    s = clean(sku).strip()
    if not s: return None
    if re.match(r'^PSD-', s, re.I):
        return ('our', s)
    return ('internal', s)

def collect():
    files=[]
    for dp,dn,fl in os.walk(ROOT):
        dn[:]=[d for d in dn if d not in EXCLUDE_DIRS and not d.startswith('.')]
        for f in fl:
            if f.lower().endswith('.html'):
                files.append(os.path.join(dp,f))
    return sorted(files)

def parse(path, rel):
    """Return record-dict (with per-page gap flags) for a product page."""
    fname=os.path.basename(rel)
    stem=os.path.splitext(fname)[0]
    html=open(path,encoding='utf-8',errors='replace').read()

    items=parse_items(html)
    item=next((x for x in items if x.get('sku') is not None), items[0] if items else None)

    our=''; internal=''
    if item:
        sl=slot_of(item.get('sku'))
        if sl:
            our, internal = (sl[1],'') if sl[0]=='our' else ('',sl[1])
    if not our:                       # PSD tokens elsewhere in page (e.g. body/cart js)
        for m in re.findall(r'\b(PSD-[A-Z][A-Z0-9-]*)\b', html):
            our=m; break

    # images
    json_imgs=[]
    for it in items:
        im=it.get('image')
        if isinstance(im,str): json_imgs.append(im)
        elif isinstance(im,list): json_imgs += [x for x in im if isinstance(x,str)]
    og=og_image(html)
    body=img_srcs(html)
    specific=[s for src in (json_imgs+body) for s in ([src] if src and not is_generic(src) else [])]
    generic_only=False; pic=''
    if specific: pic=specific[0]
    else:
        for cand in json_imgs:
            if cand: pic=cand; break
        if not pic: pic=og
        generic_only= bool(pic) and is_generic(pic)
    picture=normalize_url(pic,path) if pic else ''

    # description
    mdesc=clean(site_desc(html) or '')
    item_name= clean((item or {}).get('name') or '') or h1_text(html)
    json_desc=sorted([clean(it.get('description')) for it in items if it.get('description')],key=len,reverse=True)
    desc= mdesc or (json_desc[0] if json_desc else '') or item_name
    desc=clean(desc)

    title=first_title(html)
    fw=word_tokens(stem); tw=word_tokens(title); nw=word_tokens(item_name)
    brand=infer_brand(fw, tw, nw, items)
    price=numeric_price(item) if item else None
    subdir=os.path.dirname(rel).lstrip('/').split('/')[0] if os.path.dirname(rel)!='' else ''
    cat=infer_category(fw+nw, nw, price, brand, subdir)
    price_cell='' if price is None else ('%.2f'%price)

    return {'rel':rel,'stem':stem,'picture':picture,'our':our,'internal':internal,
            'brand':brand,'category':cat,'description':desc,'price':price_cell,
            'generic_only':generic_only}


def word_tokens(s):
    return re.findall(r'[a-z0-9]+', (s or '').lower())

def csv_field(v):
    return '' if v is None else str(v)

CSV_HEADER=['picture_url','our_part_number','internal_part_number','brand','category',
            'description','price']

def run():
    records=[]; skipped=[]
    for p in collect():
        rel=p.replace(ROOT,'')
        fname=os.path.basename(rel)
        if fname in UTILITY_FILES:
            # these are inside products/ and are landing/index/tile hubs
            html=open(p,encoding='utf-8',errors='replace').read()
            what='landing/index/category'
            if not parse_items(html) and fname not in('index.html','lucki-tile.html'):
                what='landing (no Product entity)'
            skipped.append((rel,what))
            continue
        rec=parse(p,rel)
        if not rec.get('our') and not rec.get('internal') and not rec.get('price'):
            # no identifiers AND no price -> definitely not a catalog-able product
            skipped.append((rel,'no part number and no price'))
            continue
        records.append(rec)

    # write CSV
    with open(CSV_OUT,'w',newline='',encoding='utf-8') as f:
        w=csv.writer(f)
        w.writerow(CSV_HEADER)
        for r in records:
            w.writerow([r['picture'],r['our'],r['internal'],r['brand'],r['category'],
                        r['description'],r['price']])

    full7=[r for r in records if r['picture'] and r['our'] and r['internal'] and
           r['brand']!='other' and r['category']!='other' and r['description'] and r['price']]
    gap_our=[r['rel'] for r in records if not r['our']]
    gap_int=[r['rel'] for r in records if not r['internal']]
    gap_price=[r['rel'] for r in records if not r['price']]
    gap_pic=[r['rel'] for r in records if not r['picture']]
    gap_pic_gen=[r['rel'] for r in records if r['picture'] and r['generic_only']]
    gap_brand=[r['rel'] for r in records if r['brand']=='other']
    gap_cat=[r['rel'] for r in records if r['category']=='other']
    gap_desc=[r['rel'] for r in records if not r['description']]

    # duplicate detection across tiers
    from collections import defaultdict
    both=defaultdict(list)   # pages sharing same our or internal
    for r in records:
        if r['our']: both[('our',r['our'])].append(r['rel'])
        if r['internal']: both[('internal',r['internal'])].append(r['rel'])
    dup={k:v for k,v in both.items() if len(v)>1}

    # ---- write gaps markdown ----
    _g=os.path.dirname(GAPS_OUT)
    if not os.path.exists(_g): os.makedirs(_g)
    import datetime
    def sec(f,t,items,note=''):
        f.write(f"## {t} ({len(items)})\n")
        if note: f.write(note)
        for i in items:
            f.write(f"- `{i}`\n")
        f.write("\n")
    with open(GAPS_OUT,'w',encoding='utf-8') as f:
        f.write("# Performance Supply Depot — master catalog coverage & gaps\n\n")
        f.write(f"Generated {datetime.date.today().isoformat()} by a local parser that reads the "
                f"product HTML under `/var/www/psdepot-v0/products/`.\n")
        f.write(f"- File analyzed: `/var/www/psdepot-v0/catalog.csv`\n\n")
        f.write("## Headline numbers\n\n")
        f.write(f"- product pages cataloged (rows in CSV): **{len(records)}**\n")
        f.write(f"- pages with all 7 columns complete: **{len(full7)}**\n")
        f.write(f"- landing/category/index/tile pages excluded (no single SKU): **{len(skipped)}**\n\n")
        f.write("| Gap type | Count |\n|---|---|\n")
        f.write(f"| missing PSD (\"our\") part number | {len(gap_our)} |\n")
        f.write(f"| missing internal (numeric) part number | {len(gap_int)} |\n")
        f.write(f"| missing price | {len(gap_price)} |\n")
        f.write(f"| missing product picture | {len(gap_pic)} |\n")
        f.write(f"| product picture is generic shared og/default (no real photo) | {len(gap_pic_gen)} |\n")
        f.write(f"| brand left as 'other' | {len(gap_brand)} |\n")
        f.write(f"| category left as 'other' | {len(gap_cat)} |\n")
        f.write(f"| missing description | {len(gap_desc)} |\n")
        f.write(f"| pages whose part number is shared by another page (dupes) | {len(dup)} groups |\n\n")

        sec(f, "Pages missing a PSD (\"our\") part number", sorted(gap_our),
            "These pages currently only carry the numeric/internal code (or a model code). "
            "Per 'use-what-we-have' policy the cell is left blank; these are the pages that "
            "would need a PSD- alias assigned when the two-tier map is finished.\n")
        sec(f, "Pages missing an internal (numeric) part number", sorted(gap_int),
            "Mostly pages that only carry a PSD- (customer-facing) code today and have no "
            "numeric lookup yet.\n")
        sec(f, "Pages with no price (call for pricing / on request)", sorted(gap_price))
        sec(f, "Pages with no product picture found anywhere", sorted(gap_pic))
        sec(f, "Pages using only a generic shared image (og default / logo) as their picture",
            sorted(gap_pic_gen),
            "These pages carry no product-specific photo; the generic og image was used so the "
            "picture_url cell is filled, but it is NOT a real product shot and should be audited.\n")
        sec(f, "Pages where brand was not determinable (set to 'other')", sorted(gap_brand))
        sec(f, "Pages where category was not determinable (set to 'other')", sorted(gap_cat))
        sec(f, "Pages with empty description", sorted(gap_desc))
        f.write("## Excluded non-product / non-SKU files\n")
        for rel,why in skipped:
            f.write(f"- `{rel}` — {why}\n")
        f.write("\n## Part numbers shared by more than one page\n")
        f.write("In a single source of truth a part number should be unique; these groups need "
                "reconciliation (often a slim re-written template sitting beside a full page for the "
                "same product).\n")
        for (tier,code),paths in sorted(dup.items()):
            f.write(f"- **{tier}** `{code}` -> " + "; ".join(paths) + "\n")
        f.write("\n## Method notes / assumptions\n")
        f.write("- Column `picture_url` prefers the schema.org/json-ld product `image`, then the first "
                "product `<img>`, then `og:image` as a last resort. Where only the global shared "
                "`og-image.png`/logo existed it is flagged above as generic.")
        f.write("\n- Column `our_part_number` = any `PSD-…` sku/id found on the page; "
                "`internal_part_number` = the numeric/model code (sku or filename prefix). We never "
                "invent either — that is why some cells are empty.\n")
        f.write("- `brand` is inferred from product model / filename keywords (SAM4S, CAS, MS Cash "
                "Drawer, Capton, Epson, Star, Datamax, Godex, Bixolon, ...) falling back to "
                "'other'.\n")
        f.write("- `category` is inferred from the part-number family + filename/model wording. "
                "Ambiguous lines are 'other' and flagged.\n")
        f.write("- Category hubs (`index.html`, `cash-drawers.html`, `printer-ribbons.html`, "
                "`thermal-paper.html`, `capton-pouring-systems.html`, and the component tile "
                "`lucki-tile.html`) are not products and are excluded, with reasons above.\n")
    return len(records), len(full7), len(gap_our),len(gap_int),len(gap_price),len(gap_pic),skipped

if __name__=='__main__':
    a,b,c,d,e,f,sk=run()
    print('=== PSDepot catalog build ===')
    print('catalog csv:',CSV_OUT)
    print('gaps md   :',GAPS_OUT)
    print('rows      :',a)
    print('full 7 col:',b)
    print('gap our   :',c)
    print('gap internal:',d)
    print('gap price :',e)
    print('gap picture:',f)
    print('skipped   :',len(sk))

