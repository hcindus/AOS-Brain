---
name: blender-blockout-modeling
description: Calm, low-pressure hard-surface modeling workflow — block out primary shapes first, then secondary, then tertiary detail. Use whenever modeling any object (prop, chair, ship part) in Blender and want to avoid getting lost or overstressing topology.
---

# Block-Out-First Modeling (No-Stress Workflow)

**KPI:** Finish a model without getting lost — big shapes locked before any detail. (Inspired by rileyb3d's folding-chair walkthrough.)

## Core Idea
Modeling doesn't have to be stressful. The trick is a strict **primary → secondary → tertiary** shape order: lock the silhouette first, then add mid-scale forms, then micro-detail. Never jump straight to detail — that's what makes you feel lost.

## Process

### 1. Block out primary shapes (the silhouette)
1. Add only big, simple primitives (cube, cylinder, plane) to rough out the *overall* form and proportions.
2. Don't care about topology, edge flow, or detail yet — just mass and proportion.
3. Nail the silhouette from all views (front/side/top) before moving on.

### 2. Secondary shapes (mid-scale forms)
1. Cut in the medium-sized features — panels, legs, handles, seat/back joins, major transitions.
2. Keep using a small toolset: **loop cuts (Ctrl+R), extrude (E), inset (I), bevel (Ctrl+B), and bridge**.
3. Keep topology clean by *not overthinking it* — these five tools cover ~90% of needs.

### 3. Tertiary shapes (micro-detail)
1. Only now add small detail — edge wear, small bevels, screws, seams, final proportions.
2. If a detail doesn't read at a glance, skip it.

## The small toolset (most-used)
| Op | Hotkey | Use |
|----|--------|-----|
| Loop cut | Ctrl+R | add edge loops |
| Extrude | E | pull faces/edges out |
| Inset | I | inset faces for panels |
| Bevel | Ctrl+B | round/soften edges |
| Bridge | — | connect edge loops |

## Rules
- **Primary → secondary → tertiary.** Never detail before the silhouette is locked.
- **Block out first so you never feel lost.** If proportions are wrong at the end, it's because you skipped the block-out.
- **Small toolset, repeated.** Master 5 tools instead of hunting through 100.
- **Clean topology without overthinking.** Use quads naturally; don't obsess — the next model gets easier from the habits you build here.
- **Calm, low pressure.** Follow along at your own pace; there's no wrong speed.
