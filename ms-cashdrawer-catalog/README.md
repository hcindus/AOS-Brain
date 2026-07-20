# M-S Cash Drawer Product Catalog

**Performance Supply Depot LLC** - Authorized M-S Cash Drawer Dealer  
**Last Updated:** 2026-07-20  
**Catalog Version:** 1.0.0

---

## Overview

This is a comprehensive product catalog for M-S Cash Drawer, featuring 35+ vendor partnerships and industry-leading POS hardware solutions.

## Files Structure

```
ms-cashdrawer-catalog/
├── README.md                         # This file
├── products-catalog.json            # Master product data (JSON)
├── product-page-template.html       # HTML template for product pages
├── generate-product-pages.py      # Python script to generate pages
└── generated/                       # Output directory
    └── (generated HTML files)
```

## Catalog Statistics

| Category | Products | Price Range |
|----------|----------|-------------|
| Cash Drawers | 4 | $149 - $349 |
| Receipt Printers | 3 | $349 - $425 |
| POS Systems | 3 | $1,295 - $2,499 |
| Label Printers | 2 | $495 - $895 |
| Retail Scales | 2 | $795 - $1,495 |
| Barcode Scanners | 1 | $295 |
| Mobile Printers | 1 | $395 |

**Total: 16 flagship products** (35+ vendors available via dealer portal)

## Featured Products

### 🏆 Cash Drawers (M-S Cash Drawer)
- **Smart Cord 100** - Entry-level, plug-and-play ($149)
- **Smart Cord 200** - Mid-size, high-traffic ($199)
- **mC-Connect** - Revolutionary 4-drawer controller ($249) ⭐ NEW
- **Heavy Duty 400** - Industrial grade ($349)

### 🖨️ Receipt Printers
- **Star Micronics mC-Label** - Label + receipt printing ($379)
- **Star Micronics CT-S601IIR** - Ultra-high speed ($425)
- **Epson Omnilink TM-L100** - Hub-capable ($349)

### 💻 POS Systems
- **Pioneer S413** - IP54 all-in-one ($1,299)
- **Touch Dynamic Summit** - Android self-service kiosk ($2,499) ⭐ NEW
- **SAM4S SAP-630** - Android POS terminal ($1,395)

### 📦 Label Printers
- **Bixolon XQ-840II** - Android tablet integrated ($895) ⭐ NEW
- **Citizen CL-E300** - Reliable desktop ($495)

### ⚖️ Scales
- **CAS PDN Series** - Retail dual-display ($795)
- **CAS LP-1000N** - NTEP label printing ($1,495)

### 📱 Other
- **Datalogic Magellan 900i** - 2D scanner ($295)
- **Custom Alpha-3R** - Bluetooth mobile printer ($395)

## M-S Cash Drawer Vendor Info

- **12-time RSPA Vendor Award of Excellence** (2025)
- **Technology Distributor Category Excellence**
- **35+ vendor partnerships**
- **Dealer Portal:** https://mscashdrawerus.focuspointsap.com
- **ISV Partners:** Square, RPOWER, OrderCounter, Pecan POS, Diner Daddy, RMH, CerTek

## Generating Product Pages

```bash
# Navigate to catalog directory
cd ms-cashdrawer-catalog

# Run the generator
python3 generate-product-pages.py

# Output will be in ../psdepot/products/mscashdrawer/
```

## Template Variables

The `product-page-template.html` supports these variables:

- `{{PRODUCT_NAME}}` - Product name
- `{{PRODUCT_DESCRIPTION_SHORT}}` - 160 char description
- `{{PRODUCT_DESCRIPTION_FULL}}` - Full description
- `{{PRODUCT_IMAGE}}` - Primary image URL
- `{{CATEGORY_NAME}}` - Category name
- `{{BRAND_NAME}}` - Manufacturer brand
- `{{SKU}}` - Product SKU
- `{{MPN}}` - Manufacturer part number
- `{{PRICE}}` - Dealer price
- `{{MSRP}}` - List price
- `{{WARRANTY}}` - Warranty period
- `{{AVAILABILITY}}` - Stock status
- Plus specifications, features, compatibility...

## Schema.org Markup

All generated pages include:
- ✅ Product schema with pricing, availability
- ✅ Organization schema (Performance Supply Depot)
- ✅ BreadcrumbList schema
- ✅ Offer shipping details
- ✅ Merchant return policy

## Notes

- **Dealer pricing** is available upon request via phone/email
- Prices shown in catalog are MSRP
- Contact 888-881-6834 or info@psdepot.com for dealer quotes
- All products carry manufacturer warranty (2-5 years)

## To Do

- [ ] Import actual dealer pricing from portal
- [ ] Add product images from M-S Cash Drawer
- [ ] Create category landing pages
- [ ] Add comparison tools
- [ ] Implement shopping cart integration
- [ ] Add customer reviews system

---

*Powered by Performance Supply Depot LLC*  
*Authorized M-S Cash Drawer Dealer*
