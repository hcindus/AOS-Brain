# Wooden Nickel / Silver Dollar / Silver Peso Search Report

**Date:** 2026-06-12
**Target:** Bars with names containing "Wooden Nickel", "Silver Dollar", or "Silver Peso"
**Scope:** All 50 US States + Mexico

## Search Status

### Phase 1: Existing Databases (COMPLETE)
**Result:** 0 matches found
- Searched all restaurant databases (6 states)
- Searched all lead databases (37+ files)
- Searched Mexico databases (8 states)
- **Finding:** No businesses with these exact names in existing data

### Phase 2: Web Search (IN PROGRESS)
**Challenge:** Yelp and Google block automated scraping
**Solution needed:** API access or manual search

### Phase 3: Data Collection Strategy

#### Option A: API-Based Collection (Recommended)
**Google Places API**
- Search each target name in each major city
- Cost: $200 free credit covers ~400 searches
- Output: Name, address, phone, website, rating
- Time: 2-3 hours to complete all 50 states

**Yelp Fusion API**
- Free tier: 5,000 calls/day
- Good for: Business details, reviews
- Limit: 50 results per call

#### Option B: Manual Targeted Search
Focus on high-probability regions:
1. **Southwest US** (CA, TX, AZ, NM) - Western/saloon theme
2. **Midwest** (IL, MO, KS) - Traditional bar names
3. **South** (TN, KY, LA) - Honky-tonk/country bars
4. **Mexico border regions** - "Peso" theme

## Known Wooden Nickel Locations (Common Knowledge)
- **The Wooden Nickel** - Bloomington, IN
- **Wooden Nickel** - Various college towns
- Often found in university areas

## Next Steps
To complete this search, we need:
1. **Google Places API key** OR
2. **Yelp Fusion API key** OR
3. **Manual web search** by region

## Files Created
- `/root/.openclaw/workspace/wooden_nickel_search.py` - Search framework
- `/root/.openclaw/workspace/bar_search_wooden_nickel/` - Results directory

## Recommendation
**Proceed with Google Places API** - provides best coverage for all 50 states + Mexico, with complete business details ready for DepotChaos import.

**API Key Required:** `GOOGLE_PLACES_API_KEY` environment variable
