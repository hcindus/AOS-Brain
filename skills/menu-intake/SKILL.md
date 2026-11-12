---
name: menu-intake
description: Use when programming a cash register keyboard cover / PLU menu for a customer — fill every slot, group the items, and color-code the keys by group. Applies to any POS register, not just Sam4s.
---

# Menu Intake — Register Programming

**KPI:** A register fully programmed — every PLU/key slot filled with a coherent menu, every key color-coded by group, text legible on every key. No dead keys, no placeholders.

**Source lesson (Captain, 2026-11-12):** A register is just a blank grid until you give it a menu and a story. Fill every slot, make it real enough to ring up an order. (His first test, ~30 yrs ago: "Toney's Tasty Dogs" in Weed, CA — a hotdog shop where every key was a bun / weiner / frank / sausage / condiment / for-here / to-go.)

## Process

1. **Read the register layout** — find the keyboard grid. For Sam4s files this is the `Register` sheet (the key squares) and the PLU list. Keys are cells; item names flow via formulas.
2. **Identify the item source** — the PLU sheet holds the menu items (one per row, sequentially). For Sam4s: `PCPOLL_PLU` column C holds the item names (row 2 = first item), and `Register` squares pull from it via formula chains (`'PLU's'!$E$XX` → `PCPOLL_PLU!C(XX-11)`).
3. **Fill every slot** — write one item per row, going straight down the column. Start wherever the Captain says (e.g. "row 2: Milk, OJ, Apple Juice"). Do NOT skip rows, group, or leave blanks.
4. **Group the items** — assign each item to a category (beverages, breakfast, sandwiches, salads, extras, kids, etc.).
5. **Pick a color per group** — cold drinks blue, hot items red, salads green, beer/wine yellow, etc. Be consistent.
6. **Color the squares** — apply the group color as each key's background fill.
7. **Fix text contrast** — see rules below. Reverse text on dark backgrounds.
8. **Output both** — an editable file (`.xlsx`) the customer/Captain can tweak, plus a rendered visual (`.png`) to eyeball it.

## Rules

- **Fill every slot.** No dead keys, no `PLU114`/`PLU115` placeholders. Every key gets a real item + real price.
- **One item per row, sequential.** The next item goes in the next row down. No gaps, no grouping.
- **Color by group, consistently.** Same group = same color everywhere.
- **Cold = blue, hot = red, salad = green** are the safe defaults; adapt to the actual menu (no beer → drop yellow; add amber for hot drinks, purple for sandwiches, pink for desserts, gray for extras, yellow for kids).
- **Text/background contrast — this is the trap:**
  - *Green background + orange text (or reverse) is hell on the eyes.* Keep text monochrome — white or black only, never a competing hue.
  - *Dark background → reverse the text to light.* Dark bg + dark text = invisible. Compute background luminance and flip: white text if dark, black text if light.
- **Function / numeric / payment keys stay neutral** (slate / navy / olive) so the food groups pop.
- **Avoid green next to orange** when you can — but the real rule is text-on-bg contrast, not adjacency.

## Reference — Sam4s file structure

- `PCPOLL_PLU` — the PLU data. **Column C = item name** (row 2 = first item), column I = `Price1`.
- `PLU's` — department list; column E pulls from `PCPOLL_PLU!C` via formula.
- `Register` — the keyboard layout. Keys live in **even rows (2,4,6…) and even columns (B,D,F,H…)**; odd rows/columns are spacers. Item cells are `='PLU''s'!$E$XX` formulas.
- Formula map: `'PLU's'!$E$XX` → `PCPOLL_PLU!C(XX-11)` → menu item at index `XX-13` (0-based, where item 0 = `PCPOLL_PLU!C2`).

## Color palette (tested)

| Group | Hex | Text |
|-------|-----|------|
| Cold drinks | `5B9BD5` | black |
| Hot drinks | `E8A33D` | black |
| Breakfast (hot food) | `E74C3C` | white |
| Sandwiches | `8E6FB5` | white |
| Salads & soups | `70AD47` | black |
| Pastries/desserts | `F4B6C2` | black |
| Extras/sides | `A6A6A6` | black |
| Kids | `FFD966` | black |
| Function keys | `44546A` | white |
| Numeric pad | `2F5597` | white |
| Payment (SBTL/SEND) | `548235` | white |
