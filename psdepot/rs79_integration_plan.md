# RS-79 → psdepot.com Integration Plan

**Date:** 2026-05-07  
**Target:** ReggieStarr POS v7.9 customers  
**Goal:** Frictionless supply ordering from POS terminal

---

## Option 1: Quick Win (Low Effort)

### Desktop Shortcut + QR Code
- **Desktop Icon:** `Order Supplies.ps1` → Opens psdepot.com/RS79
- **QR Code:** Thermal-printable sticker for counter
  - URL: `psdepot.com/order?ref=rs79&quick=1`
  - Pre-fills compatible supplies for RS-79 systems

**Implementation:**
```powershell
# Order Supplies.ps1
Start-Process "https://psdepot.com/order?ref=rs79&source=desktop"
```

---

## Option 2: In-POS Integration (Medium Effort)

### Custom Menu Item in RS-79
Add to ReggieStarr menu system:
```
[Main Menu] → [Utilities] → [Order Supplies]
    ↓
[Launch Browser] → psdepot.com/rs79-dashboard
```

**Parameters to pass:**
- Store ID (if available from RS-79)
- Last order date (reminder timing)
- Common items (thermal paper, ribbons)

---

## Option 3: Embedded Widget (Higher Effort)

### WebView Component
Embed a lightweight psdepot ordering widget directly in RS-79:

```html
<!-- psdepot mini-widget -->
<iframe src="https://psdepot.com/widget?compact=1&theme=dark" 
        width="400" height="600" 
        style="border:none;">
</iframe>
```

**Features:**
- One-click reorder previous items
- Low-stock alerts (if RS-79 exposes inventory API)
- Thermal paper calculator (rolls per month estimator)

---

## Recommended Rollout

### Phase 1: Link Integration (This Week)
1. Create branded landing page: `psdepot.com/RS79`
2. Provide desktop shortcut installer
3. Print QR code stickers for merchant counters

### Phase 2: Deep Integration (Next Month)
1. API handshake with RS-79 (if they expose endpoints)
2. Auto-detect printer model → suggest correct ribbons
3. Pre-filled checkout with store details

---

## Technical Requirements

### From PSD Side:
- [ ] Landing page: `psdepot.com/RS79`
- [ ] URL params: `?store_id=XXX&printer_model=YYY`
- [ ] Quick-order SKU packs (thermal paper bundles)

### From RS-79 Side:
- [ ] Menu customization (if supported)
- [ ] Browser control (Edge/Chrome/WebView)
- [ ] Store identification in URL

---

## Pitch for ReggieStarr

**Subject:** Partnership Opportunity — Supplies Integration

> "Hey [Name],
> 
> We noticed RS-79 merchants constantly run out of paper at the worst times. Want to add a 'Reorder Supplies' button right in the POS? We handle fulfillment, you get affiliate rev/share. Takes 30 mins to integrate."

---

*Ready to implement Phase 1?*
