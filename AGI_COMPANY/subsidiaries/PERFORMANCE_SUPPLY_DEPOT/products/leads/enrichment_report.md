# Lead Enrichment Report

**Generated:** 2026-03-16 05:59:22

## Summary Statistics

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Total Leads | 238 | 238 | - |
| Emails | 0 (0.0%) | 233 (97.9%) | +233 |
| Phones | 0 (0.0%) | 0 (0.0%) | +0 |
| Contacts | 0 (0.0%) | 0 (0.0%) | +0 |

## Data Sources Used

- **Pattern Matching**: Domain guessing based on business name
- Hunter.io: Email discovery (requires API key)
- Clearbit: Company data enrichment (requires API key)
- Brave Search: Web search for contact info (requires API key)
- Serper.dev: Google search results (requires API key)

## Completion Rates by County

- **Colusa**: 10 leads | Email: 10/10 (100%) | Phone: 0/10 (0%) | Contact: 0/10 (0%)\n- **Alameda**: 183 leads | Email: 182/183 (99%) | Phone: 0/183 (0%) | Contact: 0/183 (0%)\n- **Amador**: 11 leads | Email: 10/11 (91%) | Phone: 0/11 (0%) | Contact: 0/11 (0%)\n- **Calaveras**: 4 leads | Email: 4/4 (100%) | Phone: 0/4 (0%) | Contact: 0/4 (0%)\n- **Butte**: 30 leads | Email: 27/30 (90%) | Phone: 0/30 (0%) | Contact: 0/30 (0%)\n
## Notes

- This is a **demonstration run** with pattern matching only
- With API keys configured, enrichment rates will be significantly higher
- Pattern-matched emails are guessed based on business name and should be verified
- Resume capability allows re-running without duplicating work

## Output Files

Enriched files saved to: `enriched/` directory

## Next Steps

1. Configure API keys in `.env` file
2. Re-run pipeline for better enrichment
3. Verify pattern-matched emails before outreach

## Sample Enriched Data

```
                Business Name     City                  Enriched_Email Enrichment_Source
      Lumberjack's Restaurant   Colusa info@lumberjacks-restaurant.com     pattern_match
         Los Charros Taqueria   Colusa           info@los-taqueria.com     pattern_match
                  Colusa Club   Colusa             info@colusaclub.com     pattern_match
             Wintun Mini Mart   Colusa            info@wintun-mart.com     pattern_match
Wintun Mini Mart Fuel Station   Colusa         info@wintun-station.com     pattern_match
        Williams Chinese Food Williams    info@williamschinesefood.com     pattern_match
           Camp Williams Cafe Williams              info@camp-cafe.com     pattern_match
               Super Taqueria Williams                  info@super.com     pattern_match
            The Creperie Cafe Williams                info@thecafe.com     pattern_match
           Babaloo Cuban Cafe Williams       info@babaloocubancafe.com     pattern_match
```
