# psdepot.com — Site Inventory & IA Map

**Last verified:** 2026-08-20 15:00 UTC (by Miles, with Beets)
**Purpose:** Single source of truth for what already exists, to prevent duplicate page/content creation during the SEO + competitive-gap program.

---

## Sitemap status
- **Total URLs: 424** (valid XML, `sitemap.xml`)
- Last re-verify pending in Google Search Console (see `docs/GOOGLE_SEARCH_CONSOLE_SUBMISSION.md`)

---

## Top-level structure (root .html)
- **268 root-level landing pages** (state/city geo pages, `*-spanish.html` variants, robotics pages, etc.)
- Key root pages: `index.html`, `about.html`, `contact.html`, `locations.html`, `services.html`, `security.html`, `testimonials.html`, `independent-grocer.html`, `electronic-shelf-labels.html`, `self-checkout.html`

## Subdirectories (html counts)
| Dir | Count | Notes |
|-----|-------|-------|
| `products/` | 30 | Product detail pages (schema in progress) |
| `industries/` | 20 | Vertical landing pages (see list below) |
| `blog/` | 10 | 8 posts + index + `_template.html` |
| `guides/` | 9 | How-to / buyer guides |
| `categories/` | 11 subdirs | POS category hubs (cas-cash-registers, pos-systems, etc.) |
| `resources/` | 4 | faq (canonical), bulk-ordering-guide, shipping-delivery, thermal-paper-guide |
| `services/` | 1 | `installation.html` (POS installation detail) |
| `capton/` | 1 | Capton pourers hub |
| `pos/` | 1 | ReggieStarr POS systems |
| `landing/` | 1 | Landing index |
| `sentinel-shield/` | 1 | Security product |
| `collections/` | 1 | |
| `cream/` | 1 | CREAM POS |
| `reggiestarr/` | 4 | |
| `reggiestarr-pos/` | 1 | |
| `rs-80/` | 1 | RS-80 POS |
| `locations/` | 4 | CA city detail pages |
| `sales/` | 5 | |
| `ecom/` | 7 | |
| `depotchaos/` | 6 | internal tool |
| `events/` | 3 | |
| `appointments/` | 6 | |
| `credit-card/` | 1 | |
| `invoices/` | 1 | |
| `partners/`, `orders/`, `newsletter/`, `net30/` | 1 ea | |
| `admin/`, `api/`, `data/`, `scripts/`, `widget/`, `pages/`, `downloads/`, `docs/`, `games/`, `images/`, `assets/`, `leads-*`, `ivoire-auto/` etc. | — | Non-HTML / backend / utility |

---

## industries/ (20 vertical pages)
auto-repair-shops, bakeries, bars-nightclubs, cannabis-dispensaries, car-washes-detailing, catering-event-services, coffee-shops, convenience-stores, food-trucks-mobile-vendors, gas-stations, **grocery-stores**, gyms-fitness, hotels-motels, liquor-stores, medical-offices, pharmacies, pizzerias, restaurants, retail-stores, salons-spas

## guides/ (9)
pos-starter-kit, pos-supplies-checklist, printer-compatibility, receipt-paper-sizes, thermal-vs-bond-paper, which-capton-pourer, which-cash-drawer, which-printer-ribbon, which-thermal-paper

## blog/ (8 posts)
about-captain, bpa-free-thermal-paper-benefits, california-pos-supply-guide, choose-receipt-paper-size, how-to-clean-thermal-printer, pos-paper-restaurants-2024, thermal-paper-chemistry-explained, thermal-vs-bond-paper-guide

## categories/ (11)
cas-cash-registers, cf-series-cash-drawers, compact-cash-drawers, crs-sam4s-cash-registers, heavy-duty-cash-drawers, pos-scales, pos-systems, printer-ribbons, receipt-printers, standard-cash-drawers, thermal-paper

## resources/ (4)
faq (**canonical FAQ**), bulk-ordering-guide, shipping-delivery, thermal-paper-guide

---

## NEW pages added (2026-08-20, SEO/competitive program)
- `services.html` — Services HUB (Consulting/Implementation, Support/Maintenance, Repair, Training) — cross-links to `services/installation.html`
- `security.html` — Cybersecurity, PCI Compliance, Shrink Prevention
- `testimonials.html` — **testimonial quotes are ILLUSTRATIVE PLACEHOLDERS** (need real quotes)
- `independent-grocer.html` — full technology-partner vertical (differentiated from `industries/grocery-stores.html`)
- `electronic-shelf-labels.html` — ESL vertical landing
- `self-checkout.html` — self-checkout vertical landing
- `blog/_template.html` — production-ready post template (INSERT: markers)

---

## Known gaps / open items
1. **Nav consistency** — ~52 existing pages missing the standard 9-link nav (industries 20, guides 9, blog 8, categories 12, resources 3). Only `services/installation.html` retro-fitted so far.
2. **Testimonial quotes** — placeholder, need real customer quotes + permission.
3. **Product schema** — 6 SKUs completed (15-741, 30-150, 54-230, 62245, 67240, CC-235). `lucki-tile.html` + 6 mscashdrawer pages still missing meta descriptions.
4. **Pre-existing uncommitted files** — `locations.html`, `robotics-*.html` (6), `thank-you-payment-*.html` (7) — Captain's cleanup target.
5. **Competitive intel** — InStore Technology analysis done; top-10 recommendations pending prioritization.

---

## Competitive reference (InStore Technology — instoretech.com)
- Vertical: "for the independent grocer"
- Full stack: hardware + software + ESL + e-comm/loyalty/payments + security + managed services (MRR)
- Trust: named testimonials, logo wall, 24/7 HelpDesk, dual phone/email routing
- Their SEO gaps (our opportunity): no blog, missing meta descriptions, weak slugs
