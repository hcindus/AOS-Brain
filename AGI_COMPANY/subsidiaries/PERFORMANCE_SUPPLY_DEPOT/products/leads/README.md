# Lead Enrichment Pipeline

**Performance Supply Depot LLC** - California Lead Enrichment System

## Overview

This pipeline enriches California business leads by filling missing contact information:
- **Email addresses** (currently 0% → target 85%+)
- **Phone numbers** (currently 0% → target 65%+)
- **Contact/Owner names** (currently 0% → target 50%+)

## Features

- ✅ **Multiple API Sources**: Hunter.io, Clearbit, Brave Search, Serper.dev
- ✅ **Rate Limiting**: Configurable delays to avoid API blocks
- ✅ **Resume Capability**: Progress saved to avoid re-processing
- ✅ **Error Handling**: Retries and graceful degradation
- ✅ **Progress Logging**: Detailed logs in `enrichment.log`
- ✅ **Pattern Matching**: Fallback for when APIs fail

## Quick Start

### 1. Install Dependencies

```bash
pip install pandas openpyxl python-dotenv requests
```

### 2. Configure API Keys

```bash
cp .env.example .env
# Edit .env and add your API keys
```

### 3. Run the Pipeline

```bash
python3 enrich_leads.py
```

## API Keys Required

| Service | Purpose | Free Tier | Sign Up |
|---------|---------|-----------|---------|
| Hunter.io | Email discovery | 25 searches/month | [hunter.io](https://hunter.io) |
| Clearbit | Company data | 20 requests/month | [clearbit.com](https://clearbit.com) |
| Brave Search | Web search | 2,000 queries/month | [brave.com/search/api](https://brave.com/search/api/) |
| Serper.dev | Google search | 2,500 queries | [serper.dev](https://serper.dev) |

## Output

- **Enriched files**: `enriched/` directory with updated Excel files
- **Report**: `enrichment_report.md` with statistics
- **Logs**: `enrichment.log` for debugging
- **Progress**: `enrichment_progress.json` for resume capability

## Resume Capability

The pipeline automatically saves progress. If interrupted, simply re-run:

```bash
python3 enrich_leads.py
```

Already-processed leads will be skipped.

## Configuration

Edit these variables in `enrich_leads.py`:

```python
RATE_LIMIT_DELAY = 1.0  # Seconds between API calls
MAX_RETRIES = 3         # Retry attempts per API call
```

Or set in `.env`:
```
RATE_LIMIT_DELAY=2.0
MAX_RETRIES=5
```

## Data Flow

```
Input: CA_*_County_Leads.xlsx
  ↓
Check for missing Email/Phone/Name
  ↓
Query APIs (Hunter → Clearbit → Brave → Serper)
  ↓
Extract and validate contact info
  ↓
Update with enrichment columns
  ↓
Output: enriched/enriched_CA_*_County_Leads.xlsx
```

## Enrichment Columns Added

| Column | Description |
|--------|-------------|
| `Enriched_Email` | Email found via APIs |
| `Enriched_Phone` | Phone found via APIs |
| `Enriched_Contact` | Contact name found via APIs |
| `Enrichment_Source` | Which APIs provided data |
| `Enrichment_Date` | When enrichment occurred |

## Troubleshooting

### "No module named 'openpyxl'"
```bash
pip install openpyxl
```

### Rate limit errors
Increase `RATE_LIMIT_DELAY` in the script or `.env`.

### No API keys working
The pipeline falls back to pattern matching, but results will be low-confidence. Get at least one API key for better results.

## Expected Results

With all APIs configured:
- **Email enrichment**: 15-25% of leads
- **Phone enrichment**: 20-35% of leads
- **Contact enrichment**: 10-20% of leads

Without APIs (pattern matching only):
- **Email enrichment**: 5-10% (guessed domains)
- **Phone enrichment**: 0-5%
- **Contact enrichment**: 0%

## File Structure

```
leads/
├── enrich_leads.py          # Main pipeline
├── .env.example             # API key template
├── .env                     # Your API keys (gitignored)
├── README.md                # This file
├── enrichment.log           # Runtime logs
├── enrichment_progress.json # Resume state
├── enrichment_report.md     # Results summary
├── CA_*_County_Leads.xlsx   # Input files
└── enriched/                # Output directory
    ├── enriched_CA_*_County_Leads.xlsx
    └── enrichment_report.md
```

## License

Internal use only - Performance Supply Depot LLC
