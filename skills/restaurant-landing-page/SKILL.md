---
name: restaurant-landing-page
description: Build a single-page demo landing site for a local restaurant/business from a Yelp listing (name, menu, photos, contact). Use whenever the Captain shares a Yelp/business link + menu and asks to "do something similar" or build a landing page.
---

# Restaurant Landing Page

**KPI:** a live, deployable, mobile-responsive landing page in under 10 minutes — every section filled, photos wired, deployed to a working URL.

This is the 4th+ time we've done this (Sac's Tasty Hot Dogs, Joe's Buffet, …). It's now a repeatable SOP.

## When to use
- Captain pastes a Yelp link + menu text (and/or photos) for a local business.
- He says "do something similar" / "build a landing page" for a restaurant/cafe/deli.
- Any "give this local business a web presence" ask.

## Reference sites (canonical templates)
- `skills/restaurant-landing-page/template.html` — starter template (copy of the Joe's Buffet build). Copy it, swap content.
- `workspace/sacstastyhotdogs/index.html` — the original (hot dog theme, logo + 5 photos).
- `workspace/joesbuffet/index.html` — most recent (deli theme, 11-photo gallery).

## Process

### 1. Gather inputs
- **Menu** — from the Captain's pasted text (name → price → description). Preserve exact prices and category groupings (Sandwiches / Sides / Drinks / Extras).
- **Photos** — inbound media lands in `/root/.openclaw/media/inbound/` as `file_NN---<uuid>.jpg`. Identify the newest batch by `ls -lat`. Rename to `photo1.jpg … photoN.jpg`.
- **Business details** — Yelp **blocks direct scraping** (403). Get address/phone/hours via search instead:
  - `web_fetch` a DuckDuckGo query: `https://duckduckgo.com/html/?q="<Name>"+<City>+CA+phone`
  - Follow through to `usarestaurants.info` pages for address/phone/hours.
  - Pull: street address, city/state/zip, phone, hours, and any tagline ("Try Our New Menu").

### 2. Pick a theme
Map the cuisine → color palette (CSS variables in the template):
- Hot dogs → red + mustard (`#d92b2b` / `#f5a623`)
- Roast beef / deli / buffet → beef red + mustard + pickle green (`#a0322a` / `#e3a53b` / `#6f8f3a`)
- Keep the cream/brown neutrals consistent across all builds.
- Swap the hero SVG illustration to match the food (sandwich, hot dog, etc.).

### 3. Build the page
Start from `template.html`, fill in:
1. **Hero** — name, badge/tagline, one-line sub, phone + directions CTA, food SVG.
2. **Ticker** — 6–8 punchy phrases (duplicate the list once for the loop).
3. **Stats** — 4 cards; use ONLY facts you actually have (review counts, roll choices, menu size). Never invent a rating or "est." year.
4. **Story** — 2–3 short paragraphs + a "fresh-list" of 4–5 feature bullets.
5. **Menu** — one `.menu-card` per item: category tag, emoji, name, description, price. Tag the signature item "Fan Favorite".
6. **Gallery** — `.gallery-item` per photo, one `feature` (2×2). Use `object-fit:cover` (photos come as small square thumbnails).
7. **Reviews** — 3 generic quote cards marked "— Yelp Review" / "— Local Regular" (illustrative).
8. **CTA banner**, **Visit Us** (location/call/hours/good-to-know), **footer**, **sticky mobile CTA**.

### 4. Deploy
```bash
mkdir -p /var/www/psdepot.com/<slug>/ && cp -r workspace/<slug>/* /var/www/psdepot.com/<slug>/
```
- `slug` = kebab-case business name (`joesbuffet`, `sacstastyhotdogs`).
- Live URL = `https://psdepot.com/<slug>/` (root is `/var/www/psdepot.com`, path-served).
- Also mirror to `/var/www/psdepot-v0/<slug>/` if prior builds live there.

### 5. Verify
```bash
web_fetch https://psdepot.com/<slug>/   # expect 200 + the <title>
```

## Rules
- **Never fabricate** a rating, review count, "est." year, or menu item you don't have. Use only provided/scraped facts; leave unknowns generic.
- **Surfacing caveats is a feature** — e.g. Joe's "au jus not auto-included." Put real operational notes in the menu footer.
- **Photos are usually Yelp thumbnails** (258–348px, low-res). Caption by best guess, then ask the Captain to confirm the 1→N labels.
- **No logo?** Use a styled monogram (`JB`, `S`) in the `.logo` / `.hero-logo` divs, not a broken `<img>`.
- **Phone/maps** — `tel:` links use `+1<10 digits>`; maps use `https://www.google.com/maps/dir/?api=1&destination=<url-encoded address>`.
- One skill = this one job. Don't fold in domain/DNS/deployment-infra work.
