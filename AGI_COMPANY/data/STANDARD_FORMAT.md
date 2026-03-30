# Lead Database Standard Format
## Universal Format for US, Canada, Mexico

**Version:** 1.0  
**Date:** March 30, 2026  
**Status:** Active

---

## UNIVERSAL STANDARD COLUMNS

All countries use these 11 columns:

| Column | Type | Required | Description |
|--------|------|----------|-------------|
| First Name | String | Yes | Contact's first name |
| Last Name | String | Yes | Contact's last name |
| Email | String | Yes | Email address (unique) |
| Phone | String | Yes | Phone number (formatted) |
| Company | String | Yes | Business/organization name |
| City | String | Yes | City name |
| State | String | Yes | State/Province code |
| Country | String | Yes | Country code (US/CA/MX) |
| Postal Code | String | No | ZIP/Postal code |
| Tags | String | Yes | Categories, priorities |
| Notes | String | No | Additional info |
| Source | String | Yes | Where lead came from |

---

## COUNTRY-SPECIFIC FORMATS

### 🇺🇸 UNITED STATES

**State Format:** 2-letter code (CA, TX, NY)
**Phone Format:** +1 (XXX) XXX-XXXX
**Postal Code:** 5-digit or 5+4 (90210 or 90210-1234)
**Country Code:** US

**Example:**
```csv
First Name,Last Name,Email,Phone,Company,City,State,Country,Postal Code,Tags,Notes,Source
Jason,Turner,jason@realty.com,+1 (747) 239-3796,Sotheby's,San Antonio,TX,US,78205,"Priority_B, RealEstate","Experience: 4 years, 13 transactions",CREAM_RealEstate
```

---

### 🇨🇦 CANADA

**State Format:** 2-letter province code (ON, BC, AB, QC)
**Phone Format:** +1 (XXX) XXX-XXXX
**Postal Code:** ANA NAN (A1A 1A1) - letter, number, letter, space, number, letter, number
**Country Code:** CA

**Province Codes:**
- ON - Ontario
- BC - British Columbia  
- AB - Alberta
- QC - Quebec
- MB - Manitoba
- SK - Saskatchewan
- NS - Nova Scotia
- NB - New Brunswick
- NL - Newfoundland and Labrador
- PE - Prince Edward Island
- NT - Northwest Territories
- NU - Nunavut
- YT - Yukon

**Example:**
```csv
First Name,Last Name,Email,Phone,Company,City,State,Country,Postal Code,Tags,Notes,Source
Sarah,Chen,sarah@tech.ca,+1 (416) 555-1234,Toronto Tech,Toronto,ON,CA,M5V 2K8,"Priority_A, Technology","Startup, 50 employees",Canada_Business_Directory
```

---

### 🇲🇽 MEXICO

**State Format:** 3-letter code or full name (CDMX, JAL, NLE)
**Phone Format:** +52 (XX) XXXX-XXXX
**Postal Code:** 5-digit number (same format as US ZIP)
**Country Code:** MX

**State Codes:**
- CDMX - Ciudad de México
- JAL - Jalisco
- NLE - Nuevo León
- CHP - Chiapas
- GUA - Guanajuato
- PUE - Puebla
- VER - Veracruz
- YUC - Yucatán
- ... (and 24 more)

**Example:**
```csv
First Name,Last Name,Email,Phone,Company,City,State,Country,Postal Code,Tags,Notes,Source
Carlos,Ramirez,carlos@empresa.mx,+52 (33) 1234-5678,Industrias Jalisco,Guadalajara,JAL,MX,44100,"Priority_A, Manufacturing","ISO 9001 certified",Mexico_Business_Directory
```

---

## PHONE NUMBER FORMATTING

### United States
- Input: (747) 239-3796
- Output: +1 (747) 239-3796

### Canada
- Input: (416) 555-1234
- Output: +1 (416) 555-1234

### Mexico
- Input: (33) 1234-5678 or 33 1234 5678
- Output: +52 (33) 1234-5678

---

## FILE NAMING CONVENTION

### By Country
```
COMPLETED_US_[STATE]_leads.csv
COMPLETED_CA_[PROVINCE]_leads.csv
COMPLETED_MX_[STATE]_leads.csv
```

### Master Files
```
COMPLETED_US_ALL.csv
COMPLETED_CA_ALL.csv
COMPLETED_MX_ALL.csv
COMPLETED_NORTH_AMERICA.csv
```

---

## SCRAPER OUTPUT FORMAT

All scrapers must output CSV with these exact column names (case-sensitive):

```python
STANDARD_COLUMNS = [
    "First Name",
    "Last Name", 
    "Email",
    "Phone",
    "Company",
    "City",
    "State",
    "Country",
    "Postal Code",
    "Tags",
    "Notes",
    "Source"
]
```

---

## VALIDATION RULES

### Email
- Must contain @
- Must contain domain
- No duplicates within file

### Phone
- Must start with + (country code)
- Minimum 10 digits
- Remove non-numeric except +, (), -, space

### State/Province
- Must match country code
- US: 2 letters
- CA: 2 letters  
- MX: 3 letters or full name

### Country
- Must be: US, CA, or MX
- Cannot be empty

### Tags
- Comma-separated
- No spaces after commas (or trim)
- Examples: "Priority_A, CREAM, RealEstate"

---

## CONSOLIDATION SCRIPT

Location: `/scripts/consolidate_leads.py`

**Features:**
- Loads leads from any source
- Validates format
- Adds country code if missing
- Formats phone numbers
- Standardizes state codes
- Creates country-specific files
- Creates master files

**Usage:**
```bash
python3 scripts/consolidate_leads.py
```

**Output:**
- 50+ US state files
- 13 CA province files
- 32 MX state files
- 3 country master files
- 1 North America master file

---

## DATA SOURCES BY COUNTRY

### United States
- CREAM (real estate agents)
- Secretary of State (business registrations)
- County business licenses
- Chamber of Commerce

### Canada
- Industry Canada (corporations)
- Provincial business registries
- Canadian Chamber of Commerce
- Business directories

### Mexico
- SIEM (Sistema de Información Empresarial Mexicano)
- State business registries
- CANACO (Cámara Nacional de Comercio)
- Industry associations

---

## NOTES

**Country Field Required:**
All leads MUST include country code. This enables:
- Proper phone formatting
- International campaigns
- Geographic segmentation
- Compliance with regulations

**Separate by Country:**
Keep files separate per country for:
- Easier management
- Compliance (CAN-SPAM, CASL, etc.)
- Currency/pricing differences
- Language considerations

**Standardization Priority:**
1. Email (unique identifier)
2. Phone (+country code)
3. Country (US/CA/MX)
4. State (proper code)

---

**Maintained by:** Miles - Dark Factory AOS  
**Last Updated:** March 30, 2026
