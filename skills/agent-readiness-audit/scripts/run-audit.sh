#!/usr/bin/env bash
# Agent Readiness Audit Runner
# Usage: ./run-audit.sh <domain> [competitor1] [competitor2] ...
# Output: Structured JSON report + human-readable summary
# Part of: skills/agent-readiness-audit

set -euo pipefail

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
CYAN='\033[0;36m'; NC='\033[0m'; BOLD='\033[1m'

usage() {
    echo "Usage: $0 <domain> [competitor_domains...]"
    echo "Example: $0 psdepot.com pospaper.com staples.com"
    exit 1
}

[[ $# -lt 1 ]] && usage

DOMAIN="${1:-}"
shift
COMPETITORS=("$@")

# Strip protocol and path
DOMAIN_CLEAN=$(echo "$DOMAIN" | sed -E 's|^https?://||; s|/.*$||')
BASE_URL="https://${DOMAIN_CLEAN}"

TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
TMPDIR=$(mktemp -d)
trap 'rm -rf "$TMPDIR"' EXIT

echo -e "${BOLD}${CYAN}╔══════════════════════════════════════════╗${NC}"
echo -e "${BOLD}${CYAN}║   AGENT READINESS AUDIT                 ║${NC}"
echo -e "${BOLD}${CYAN}║   Target: ${DOMAIN_CLEAN}${NC}"
echo -e "${BOLD}${CYAN}╚══════════════════════════════════════════╝${NC}"
echo ""

# ─── Helper: quick HTTP check ───
check_url() {
    local url="$1"
    local code
    code=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 -L "$url" 2>/dev/null || echo "000")
    local size
    size=$(curl -s -o /dev/null -w "%{size_download}" --max-time 10 -L "$url" 2>/dev/null || echo "0")
    echo "$code:$size"
}

# ─── Helper: grade emoji ───
grade_emoji() {
    local score=$1
    if (( score >= 8 )); then echo "✅"; 
    elif (( score >= 5 )); then echo "⚠️"; 
    else echo "❌"; fi
}

# ─── 1. Agent-Native Files ───
echo -e "${BOLD}[1/7] Agent-Native Files${NC}"

LLMS_RESULT=$(check_url "${BASE_URL}/llms.txt")
LLMS_CODE="${LLMS_RESULT%%:*}"
LLMS_SIZE="${LLMS_RESULT##*:}"

PRODUCTS_JSON_RESULT=$(check_url "${BASE_URL}/products.json")
PJ_CODE="${PRODUCTS_JSON_RESULT%%:*}"
PJ_SIZE="${PRODUCTS_JSON_RESULT##*:}"

ROBOTS_RESULT=$(check_url "${BASE_URL}/robots.txt")
ROBOTS_CODE="${ROBOTS_RESULT%%:*}"

SITEMAP_RESULT=$(check_url "${BASE_URL}/sitemap.xml")
SITEMAP_CODE="${SITEMAP_RESULT%%:*}"

# Fetch llms.txt content if available
LLMS_CONTENT=""
[[ "$LLMS_CODE" == "200" ]] && LLMS_CONTENT=$(curl -s --max-time 10 "${BASE_URL}/llms.txt" 2>/dev/null | head -60)

# Fetch robots.txt
ROBOTS_CONTENT=""
[[ "$ROBOTS_CODE" == "200" ]] && ROBOTS_CONTENT=$(curl -s --max-time 10 "${BASE_URL}/robots.txt" 2>/dev/null)

echo "  llms.txt:       HTTP $LLMS_CODE ($LLMS_SIZE bytes)"
echo "  products.json:  HTTP $PJ_CODE ($PJ_SIZE bytes)"
echo "  robots.txt:     HTTP $ROBOTS_CODE"
echo "  sitemap.xml:    HTTP $SITEMAP_CODE"

AGENT_FILES_SCORE=0
[[ "$LLMS_CODE" == "200" ]] && ((AGENT_FILES_SCORE+=4))
[[ "$PJ_CODE" == "200" ]] && ((AGENT_FILES_SCORE+=3))
[[ "$ROBOTS_CODE" == "200" ]] && ((AGENT_FILES_SCORE+=2))
[[ "$SITEMAP_CODE" == "200" ]] && ((AGENT_FILES_SCORE+=1))

echo -e "  → Score: ${AGENT_FILES_SCORE}/10 $(grade_emoji $AGENT_FILES_SCORE)\n"

# ─── 2. Schema.org Markup ───
echo -e "${BOLD}[2/7] Schema.org Structured Data${NC}"

HOMEPAGE_HTML=$(curl -s --max-time 15 -L "$BASE_URL" 2>/dev/null || echo "")
SCHEMA_COUNT=$(echo "$HOMEPAGE_HTML" | grep -c '<script type="application/ld+json">' || echo "0")
SCHEMA_COUNT=0
[[ "$SCHEMA_COUNT" =~ ^[0-9]+$ ]] || SCHEMA_COUNT=0
SCHEMA_TYPES=$(echo "$HOMEPAGE_HTML" | grep -oP '"@type":\s*"[^"]+"' 2>/dev/null | sort | uniq -c | sort -rn || echo "None found")

echo "  JSON-LD blocks: $SCHEMA_COUNT"
echo "  Schema types found:"
echo "$SCHEMA_TYPES" | while read -r line; do
    [[ -n "$line" ]] && echo "    $line"
done

# Count unique schema types
UNIQUE_TYPES=$(echo "$SCHEMA_TYPES" | wc -l)
HAS_PRODUCT=$(echo "$SCHEMA_TYPES" | grep -c '"Product"' 2>/dev/null || echo "0")
HAS_FAQ=$(echo "$SCHEMA_TYPES" | grep -c '"FAQPage"' 2>/dev/null || echo "0")
HAS_LOCAL=$(echo "$SCHEMA_TYPES" | grep -c '"LocalBusiness"' 2>/dev/null || echo "0")
HAS_BREADCRUMB=$(echo "$SCHEMA_TYPES" | grep -c '"BreadcrumbList"' 2>/dev/null || echo "0")
HAS_REVIEW=$(echo "$SCHEMA_TYPES" | grep -c '"Review"\|"AggregateRating"' 2>/dev/null || echo "0")
# Clean up any newlines
HAS_PRODUCT=$(echo "$HAS_PRODUCT" | tr -d '\n\r ')
HAS_FAQ=$(echo "$HAS_FAQ" | tr -d '\n\r ')
HAS_LOCAL=$(echo "$HAS_LOCAL" | tr -d '\n\r ')
HAS_BREADCRUMB=$(echo "$HAS_BREADCRUMB" | tr -d '\n\r ')
HAS_REVIEW=$(echo "$HAS_REVIEW" | tr -d '\n\r ')

SCHEMA_SCORE=0
[[ "$SCHEMA_COUNT" -ge 1 ]] && ((SCHEMA_SCORE+=3))
[[ "$HAS_PRODUCT" -ge 1 ]] && ((SCHEMA_SCORE+=3))
[[ "$HAS_FAQ" -ge 1 ]] && ((SCHEMA_SCORE+=1))
[[ "$HAS_LOCAL" -ge 1 ]] && ((SCHEMA_SCORE+=1))
[[ "$HAS_BREADCRUMB" -ge 1 ]] && ((SCHEMA_SCORE+=1))
[[ "$HAS_REVIEW" -ge 1 ]] && ((SCHEMA_SCORE+=1))
[[ "$SCHEMA_SCORE" -gt 10 ]] && SCHEMA_SCORE=10

echo -e "  → Score: ${SCHEMA_SCORE}/10 $(grade_emoji $SCHEMA_SCORE)\n"

# ─── 3. Meta & Social Tags ───
echo -e "${BOLD}[3/7] Meta Tags & Social Cards${NC}"

META_DESC=$(echo "$HOMEPAGE_HTML" | grep -oP '<meta\s+name="description"\s+content="[^"]+"' | head -1 || echo "Missing")
OG_TITLE=$(echo "$HOMEPAGE_HTML" | grep -oP '<meta\s+property="og:title"\s+content="[^"]+"' | head -1 || echo "Missing")
OG_DESC=$(echo "$HOMEPAGE_HTML" | grep -oP '<meta\s+property="og:description"\s+content="[^"]+"' | head -1 || echo "Missing")
OG_IMAGE=$(echo "$HOMEPAGE_HTML" | grep -oP '<meta\s+property="og:image"\s+content="[^"]+"' | head -1 || echo "Missing")
TITLE_TAG=$(echo "$HOMEPAGE_HTML" | grep -oP '<title>[^<]+</title>' | head -1 | sed 's/<[^>]*>//g' || echo "Missing")
CANONICAL=$(echo "$HOMEPAGE_HTML" | grep -oP '<link\s+rel="canonical"\s+href="[^"]+"' | head -1 || echo "Missing")

echo "  Title:         ${TITLE_TAG:0:80}"
echo "  Meta Desc:     ${META_DESC:0:80}"
echo "  OG Title:      ${OG_TITLE:0:80}"
echo "  OG Image:      $( [[ "$OG_IMAGE" != "Missing" ]] && echo '✅ Present' || echo '❌ Missing' )"
echo "  Canonical:     $( [[ "$CANONICAL" != "Missing" ]] && echo '✅ Present' || echo '❌ Missing' )"

META_SCORE=5
[[ "$META_DESC" == "Missing" ]] && ((META_SCORE-=2))
[[ "$OG_TITLE" == "Missing" ]] && ((META_SCORE-=1))
[[ "$OG_IMAGE" == "Missing" ]] && ((META_SCORE-=1))
[[ "$CANONICAL" == "Missing" ]] && ((META_SCORE-=1))

echo -e "  → Score: ${META_SCORE}/5 (scaled to 10: $((META_SCORE*2))/10)\n"

# ─── 4. Content Clarity ───
echo -e "${BOLD}[4/7] Content Clarity for AI Parsing${NC}"

# Extract readable text (strip HTML tags)
READABLE_TEXT=$(echo "$HOMEPAGE_HTML" | sed 's/<[^>]*>//g' | tr -s ' \n' ' ' | head -c 3000)
WORD_COUNT=$(echo "$READABLE_TEXT" | wc -w)
HAS_PRICING=$(echo "$HOMEPAGE_HTML" | grep -ci '\$[0-9]' 2>/dev/null || echo "0")
HAS_PHONE=$(echo "$HOMEPAGE_HTML" | grep -ci '[0-9]\{3\}[)-. ][0-9]\{3\}[)-. ][0-9]\{4\}' 2>/dev/null || echo "0")
HAS_ADDRESS=$(echo "$HOMEPAGE_HTML" | grep -ci 'CA\|California\|Street\|Ave\|Suite' 2>/dev/null || echo "0")
HAS_PRICING=$(echo "$HAS_PRICING" | tr -d '\n\r ')
HAS_PHONE=$(echo "$HAS_PHONE" | tr -d '\n\r ')
HAS_ADDRESS=$(echo "$HAS_ADDRESS" | tr -d '\n\r ')

echo "  Homepage text: ~${WORD_COUNT} words"
echo "  Pricing visible in HTML: $( [[ "$HAS_PRICING" -gt 0 ]] && echo '✅ Yes' || echo '❌ No' )"
echo "  Phone visible: $( [[ "$HAS_PHONE" -gt 0 ]] && echo '✅ Yes' || echo '❌ No' )"
echo "  Location visible: $( [[ "$HAS_ADDRESS" -gt 0 ]] && echo '✅ Yes' || echo '❌ No' )"

CONTENT_SCORE=4
[[ "$WORD_COUNT" -gt 200 ]] && ((CONTENT_SCORE+=2))
[[ "$HAS_PRICING" -gt 0 ]] && ((CONTENT_SCORE+=2))
[[ "$HAS_PHONE" -gt 0 ]] && ((CONTENT_SCORE+=1))
[[ "$HAS_ADDRESS" -gt 0 ]] && ((CONTENT_SCORE+=1))
[[ "$CONTENT_SCORE" -gt 10 ]] && CONTENT_SCORE=10

echo -e "  → Score: ${CONTENT_SCORE}/10 $(grade_emoji $CONTENT_SCORE)\n"

# ─── 5. Structured Product Data ───
echo -e "${BOLD}[5/7] Structured Product Data${NC}"

# Check first product page if found
PRODUCT_URLS=$(echo "$HOMEPAGE_HTML" | grep -oP 'href="[^"]*product[^"]*\.html"' | head -3 | sed 's/href="//;s/"//' || echo "")
PRODUCT_SCORE=0

if [[ -n "$PRODUCT_URLS" ]]; then
    SAMPLE_URL="${PRODUCT_URLS%%$'\n'*}"
    [[ "$SAMPLE_URL" != http* ]] && SAMPLE_URL="${BASE_URL}${SAMPLE_URL}"
    
    PRODUCT_HTML=$(curl -s --max-time 10 -L "$SAMPLE_URL" 2>/dev/null || echo "")
    PRODUCT_SCHEMA=$(echo "$PRODUCT_HTML" | grep -c '"@type".*"Product"' || echo "0")
    HAS_PRICE_SCHEMA=$(echo "$PRODUCT_HTML" | grep -c '"price":' || echo "0")
    HAS_SKU=$(echo "$PRODUCT_HTML" | grep -c '"sku":' || echo "0")
    HAS_AVAIL=$(echo "$PRODUCT_HTML" | grep -c '"availability":' || echo "0")
    HAS_SHIPPING=$(echo "$PRODUCT_HTML" | grep -c '"shippingDetails":' || echo "0")
    HAS_RETURN=$(echo "$PRODUCT_HTML" | grep -c '"hasMerchantReturnPolicy":' || echo "0")
    
    echo "  Sample product page: $SAMPLE_URL"
    echo "  Product schema: $( [[ "$PRODUCT_SCHEMA" -gt 0 ]] && echo '✅ Present' || echo '❌ Missing' )"
    echo "  Price in schema: $( [[ "$HAS_PRICE_SCHEMA" -gt 0 ]] && echo '✅ Yes' || echo '❌ No' )"
    echo "  SKU: $( [[ "$HAS_SKU" -gt 0 ]] && echo '✅ Yes' || echo '❌ No' )"
    echo "  Shipping details: $( [[ "$HAS_SHIPPING" -gt 0 ]] && echo '✅ Yes' || echo '❌ No' )"
    echo "  Return policy: $( [[ "$HAS_RETURN" -gt 0 ]] && echo '✅ Yes' || echo '❌ No' )"
    
    [[ "$PRODUCT_SCHEMA" -gt 0 ]] && ((PRODUCT_SCORE+=3))
    [[ "$HAS_PRICE_SCHEMA" -gt 0 ]] && ((PRODUCT_SCORE+=2))
    [[ "$HAS_SKU" -gt 0 ]] && ((PRODUCT_SCORE+=1))
    [[ "$HAS_AVAIL" -gt 0 ]] && ((PRODUCT_SCORE+=1))
    [[ "$HAS_SHIPPING" -gt 0 ]] && ((PRODUCT_SCORE+=1))
    [[ "$HAS_RETURN" -gt 0 ]] && ((PRODUCT_SCORE+=1))
    [[ "$HAS_SHIPPING" -gt 0 && "$HAS_RETURN" -gt 0 ]] && ((PRODUCT_SCORE+=1))
    [[ "$PRODUCT_SCORE" -gt 10 ]] && PRODUCT_SCORE=10
else
    echo "  No product pages found on homepage"
    PRODUCT_SCORE=2
fi

echo -e "  → Score: ${PRODUCT_SCORE}/10 $(grade_emoji $PRODUCT_SCORE)\n"

# ─── 6. Competitor Check ───
echo -e "${BOLD}[6/7] Competitive Agent Visibility${NC}"

COMPETITOR_DATA=""
COMP_SCORE=10  # Start high, deduct for each competitor ahead

if [[ ${#COMPETITORS[@]} -gt 0 ]]; then
    for comp in "${COMPETITORS[@]}"; do
        comp_clean=$(echo "$comp" | sed -E 's|^https?://||; s|/.*$||')
        comp_url="https://${comp_clean}"
        
        comp_llms=$(check_url "${comp_url}/llms.txt")
        comp_llms_code="${comp_llms%%:*}"
        comp_pj=$(check_url "${comp_url}/products.json")
        comp_pj_code="${comp_pj%%:*}"
        comp_schema_raw=$(curl -s --max-time 10 -L "$comp_url" 2>/dev/null | grep -c 'application/ld\+json' || echo "0")
        comp_schema=$(echo "$comp_schema_raw" | tr -d '\n\r ')
        
        comp_advantage=0
        [[ "$comp_llms_code" == "200" ]] && ((comp_advantage+=1))
        [[ "$comp_pj_code" == "200" ]] && ((comp_advantage+=1))
        
        ahead="="
        if [[ "$comp_llms_code" == "200" && "$LLMS_CODE" != "200" ]]; then ahead="↑"; ((COMP_SCORE-=2)); fi
        if [[ "$comp_pj_code" == "200" && "$PJ_CODE" != "200" ]]; then ahead="↑"; ((COMP_SCORE-=2)); fi
        
        echo "  ${comp_clean}: llms=${comp_llms_code} p.json=${comp_pj_code} schemas=${comp_schema} ${ahead}"
        
        COMPETITOR_DATA+=$(printf '    {
      "domain": "%s",
      "llms_txt": "%s",
      "products_json": "%s",
      "schema_blocks": %s,
      "ahead": %s
    },
'             "${comp_clean}" "${comp_llms_code}" "${comp_pj_code}" "${comp_schema}"             "$([[ "$ahead" == "↑" ]] && echo "true" || echo "false")")
    done
    COMPETITOR_DATA="${COMPETITOR_DATA%,}"
    COMPETITOR_JSON="[${COMPETITOR_DATA}]"
else
    COMPETITOR_JSON="[]"
  echo "  No competitors specified for comparison"
fi
[[ "$COMP_SCORE" -lt 1 ]] && COMP_SCORE=1
[[ "$COMP_SCORE" -gt 10 ]] && COMP_SCORE=10

echo -e "  → Score: ${COMP_SCORE}/10 $(grade_emoji $COMP_SCORE)\n"

# ─── 7. Trust Signals ───
echo -e "${BOLD}[7/7] Trust Signals${NC}"

HAS_REVIEWS=$(echo "$HOMEPAGE_HTML" | grep -ci '"review"\|"aggregateRating"\|testimonial\|"ratingValue"' 2>/dev/null || echo "0")
HAS_SSL=$( [[ "$BASE_URL" == https://* ]] && echo "1" || echo "0" )
HAS_PHONE_VISIBLE="$HAS_PHONE"
HAS_POLICY=$(echo "$HOMEPAGE_HTML" | grep -ci 'privacy\|terms\|return\|refund' 2>/dev/null || echo "0")
HAS_REVIEWS=$(echo "$HAS_REVIEWS" | tr -d '\n\r ')
HAS_POLICY=$(echo "$HAS_POLICY" | tr -d '\n\r ')

echo "  Review/rating schema: $( [[ "$HAS_REVIEWS" -gt 0 ]] && echo '✅ Present' || echo '❌ Missing' )"
echo "  SSL: $( [[ "$HAS_SSL" == "1" ]] && echo '✅ Yes' || echo '❌ No' )"
echo "  Phone visible: $( [[ "$HAS_PHONE_VISIBLE" -gt 0 ]] && echo '✅ Yes' || echo '❌ No' )"
echo "  Policy pages: $( [[ "$HAS_POLICY" -gt 0 ]] && echo '✅ Referenced' || echo '❌ Not found' )"

TRUST_SCORE=3
[[ "$HAS_REVIEWS" -gt 0 ]] && ((TRUST_SCORE+=4))
[[ "$HAS_SSL" == "1" ]] && ((TRUST_SCORE+=1))
[[ "$HAS_PHONE_VISIBLE" -gt 0 ]] && ((TRUST_SCORE+=1))
[[ "$HAS_POLICY" -gt 0 ]] && ((TRUST_SCORE+=1))
[[ "$TRUST_SCORE" -gt 10 ]] && TRUST_SCORE=10

echo -e "  → Score: ${TRUST_SCORE}/10 $(grade_emoji $TRUST_SCORE)\n"

# ─── OVERALL SCORE ───
OVERALL=$(( (AGENT_FILES_SCORE + SCHEMA_SCORE + (META_SCORE*2) + CONTENT_SCORE + PRODUCT_SCORE + COMP_SCORE + TRUST_SCORE) / 7 ))

echo -e "${BOLD}${CYAN}╔══════════════════════════════════════════╗${NC}"
echo -e "${BOLD}${CYAN}║   OVERALL SCORE: ${OVERALL}/10                     ║${NC}"
echo -e "${BOLD}${CYAN}╚══════════════════════════════════════════╝${NC}"
echo ""

# ─── Clean up all numeric variables ───
SCHEMA_COUNT=$(echo "${SCHEMA_COUNT:-0}" | tr -d '\n\r ')
AGENT_FILES_SCORE=$(echo "${AGENT_FILES_SCORE:-0}" | tr -d '\n\r ')
SCHEMA_SCORE=$(echo "${SCHEMA_SCORE:-0}" | tr -d '\n\r ')
META_SCORE=$(echo "${META_SCORE:-0}" | tr -d '\n\r ')
CONTENT_SCORE=$(echo "${CONTENT_SCORE:-0}" | tr -d '\n\r ')
PRODUCT_SCORE=$(echo "${PRODUCT_SCORE:-0}" | tr -d '\n\r ')
COMP_SCORE=$(echo "${COMP_SCORE:-0}" | tr -d '\n\r ')
TRUST_SCORE=$(echo "${TRUST_SCORE:-0}" | tr -d '\n\r ')
OVERALL=$(echo "${OVERALL:-0}" | tr -d '\n\r ')
LLMS_SIZE=$(echo "${LLMS_SIZE:-0}" | tr -d '\n\r ')
PJ_SIZE=$(echo "${PJ_SIZE:-0}" | tr -d '\n\r ')
WORD_COUNT=$(echo "${WORD_COUNT:-0}" | tr -d '\n\r ')
comp_schema=$(echo "${comp_schema:-0}" | tr -d '\n\r ')

# ─── Final variable cleanup ───
for var in SCHEMA_COUNT AGENT_FILES_SCORE SCHEMA_SCORE META_SCORE CONTENT_SCORE PRODUCT_SCORE COMP_SCORE TRUST_SCORE OVERALL LLMS_SIZE PJ_SIZE WORD_COUNT HAS_PRODUCT HAS_FAQ HAS_LOCAL HAS_BREADCRUMB HAS_REVIEW HAS_PRICING HAS_PHONE HAS_ADDRESS HAS_REVIEWS HAS_POLICY HAS_SSL PRODUCT_SCHEMA HAS_PRICE_SCHEMA HAS_SKU HAS_AVAIL HAS_SHIPPING HAS_RETURN; do
    val="${!var}"
    val=$(echo "$val" | tr -d '\n\r ' | grep -oP '^\d+' || echo "0")
    [[ -z "$val" ]] && val=0
    eval "$var=$val"
done

# ─── Generate JSON Report ───
# Export all variables for python3 JSON generator
export DOMAIN_CLEAN BASE_URL TIMESTAMP OVERALL
export AGENT_FILES_SCORE SCHEMA_SCORE META_SCORE CONTENT_SCORE PRODUCT_SCORE COMP_SCORE TRUST_SCORE
export LLMS_CODE PJ_CODE ROBOTS_CODE SITEMAP_CODE LLMS_SIZE PJ_SIZE
export SCHEMA_COUNT HAS_PRODUCT HAS_FAQ HAS_LOCAL HAS_BREADCRUMB HAS_REVIEW
export TITLE_TAG META_DESC OG_TITLE OG_IMAGE CANONICAL
export WORD_COUNT HAS_PRICING HAS_PHONE HAS_ADDRESS
export PRODUCT_SCHEMA HAS_PRICE_SCHEMA HAS_SKU HAS_AVAIL HAS_SHIPPING HAS_RETURN
export HAS_REVIEWS HAS_POLICY HAS_SSL
export LLMS_CONTENT ROBOTS_CONTENT COMPETITOR_JSON

# Generate JSON report using python3 (avoids all shell escaping issues)
python3 << 'PYJSON' > "$TMPDIR/report.json"
import json, os, datetime

SCHEMA_COUNT = int(os.environ.get("SCHEMA_COUNT", "0").strip() or "0")
AGENT_FILES_SCORE = int(os.environ.get("AGENT_FILES_SCORE", "0").strip() or "0")
SCHEMA_SCORE = int(os.environ.get("SCHEMA_SCORE", "0").strip() or "0")
META_SCORE = int(os.environ.get("META_SCORE", "0").strip() or "0")
CONTENT_SCORE = int(os.environ.get("CONTENT_SCORE", "0").strip() or "0")
PRODUCT_SCORE = int(os.environ.get("PRODUCT_SCORE", "0").strip() or "0")
COMP_SCORE = int(os.environ.get("COMP_SCORE", "0").strip() or "0")
TRUST_SCORE = int(os.environ.get("TRUST_SCORE", "0").strip() or "0")
LLMS_SIZE = int(os.environ.get("LLMS_SIZE", "0").strip() or "0")
PJ_SIZE = int(os.environ.get("PJ_SIZE", "0").strip() or "0")
WORD_COUNT = int(os.environ.get("WORD_COUNT", "0").strip() or "0")

report = {
    "audit": {
        "domain": os.environ.get("DOMAIN_CLEAN", ""),
        "url": os.environ.get("BASE_URL", ""),
        "timestamp": os.environ.get("TIMESTAMP", ""),
        "overall_score": int(os.environ.get("OVERALL", "0").strip() or "0")
    },
    "scores": {
        "agent_files": {"score": AGENT_FILES_SCORE, "max": 10},
        "schema_markup": {"score": SCHEMA_SCORE, "max": 10},
        "meta_tags": {"score": META_SCORE * 2, "max": 10},
        "content_clarity": {"score": CONTENT_SCORE, "max": 10},
        "product_data": {"score": PRODUCT_SCORE, "max": 10},
        "competitive": {"score": COMP_SCORE, "max": 10},
        "trust_signals": {"score": TRUST_SCORE, "max": 10}
    },
    "details": {
        "agent_files": {
            "llms_txt": {"status": os.environ.get("LLMS_CODE","")},
            "products_json": {"status": os.environ.get("PJ_CODE","")},
            "robots_txt": {"status": os.environ.get("ROBOTS_CODE","")},
            "sitemap_xml": {"status": os.environ.get("SITEMAP_CODE","")}
        },
        "schema": {
            "jsonld_blocks": SCHEMA_COUNT,
            "has_product": os.environ.get("HAS_PRODUCT","0").strip() != "0",
            "has_faq": os.environ.get("HAS_FAQ","0").strip() != "0",
            "has_local_business": os.environ.get("HAS_LOCAL","0").strip() != "0",
            "has_breadcrumb": os.environ.get("HAS_BREADCRUMB","0").strip() != "0",
            "has_review": os.environ.get("HAS_REVIEW","0").strip() != "0"
        },
        "meta": {
            "title": os.environ.get("TITLE_TAG","")[:200],
            "description_present": os.environ.get("META_DESC","Missing") != "Missing",
            "og_title_present": os.environ.get("OG_TITLE","Missing") != "Missing",
            "og_image_present": os.environ.get("OG_IMAGE","Missing") != "Missing",
            "canonical_present": os.environ.get("CANONICAL","Missing") != "Missing"
        },
        "content": {
            "word_count": WORD_COUNT,
            "pricing_visible": os.environ.get("HAS_PRICING","0").strip() != "0",
            "phone_visible": os.environ.get("HAS_PHONE","0").strip() != "0",
            "location_visible": os.environ.get("HAS_ADDRESS","0").strip() != "0"
        },
        "product_sample": {
            "has_product_schema": os.environ.get("PRODUCT_SCHEMA","0").strip() != "0",
            "has_price": os.environ.get("HAS_PRICE_SCHEMA","0").strip() != "0",
            "has_sku": os.environ.get("HAS_SKU","0").strip() != "0",
            "has_availability": os.environ.get("HAS_AVAIL","0").strip() != "0",
            "has_shipping": os.environ.get("HAS_SHIPPING","0").strip() != "0",
            "has_return_policy": os.environ.get("HAS_RETURN","0").strip() != "0"
        },
        "competitors": json.loads(os.environ.get("COMPETITOR_JSON", "[]")),
        "trust": {
            "review_schema": os.environ.get("HAS_REVIEWS","0").strip() != "0",
            "ssl": os.environ.get("HAS_SSL","0").strip() == "1",
            "phone_visible": os.environ.get("HAS_PHONE","0").strip() != "0",
            "policy_pages": os.environ.get("HAS_POLICY","0").strip() != "0"
        },
        "raw": {
            "llms_content": os.environ.get("LLMS_CONTENT","")[:500],
            "robots_content": os.environ.get("ROBOTS_CONTENT","")[:500]
        }
    }
}
json.dump(report, sys.stdout, indent=2)
PYJSON

# Pretty print
python3 -m json.tool "$TMPDIR/report.json" > "$TMPDIR/report_pretty.json" 2>/dev/null
cp "$TMPDIR/report_pretty.json" "$TMPDIR/report.json"


# Clean JSON and save using python3
OUTFILE="/tmp/audit-${DOMAIN_CLEAN}-$(date +%Y%m%d-%H%M%S).json"
if [ -s "${TMPDIR}/report_pretty.json" ]; then
    cp "${TMPDIR}/report_pretty.json" "$OUTFILE"
else
    echo '{"error": "JSON generation failed"}' > "$OUTFILE"
fi

echo -e "${GREEN}✅ Audit complete. Report saved to: ${OUTFILE}${NC}"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "  1. Review the JSON report"
echo "  2. Feed the report + discovery call transcript to Claude using the analysis prompt"
echo "  3. Build the client-facing report from the analysis"
echo ""
echo -e "${CYAN}Report JSON: ${OUTFILE}${NC}"

# Also output the JSON to stdout for piping
cat "$OUTFILE"
