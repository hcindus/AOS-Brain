# AOCROS FLEET — Master Manifest

**Last updated:** 2026-10-15
**Scope:** Every vessel, unit, character, and 3D asset in the AOCROS fleet.

---

## 1. FLAGSHIP & VESSELS

### SEED ONE — Flagship Colony Vessel
- **Class:** Seed Ship One · alias **La Razonati** · 2,500m · 235 crew + civilians
- **Role:** interstellar colonization — a mobile, defensible city (not a warship)
- **Spec:** `fleet/SEED_ONE_SHIP_SPEC.md`
- **3D mesh:** `fleet/SEED_ONE_3D_MESH_SPEC.md`
- **Source data:** `nog_extraction/ship_database_v2.json` + `nogship.mm` ⚠️ *(pending extraction — not yet in workspace)*

### MORTIMER — AOCROS Fleet flagship (reference)
- Referenced as the source of the ship database (`ship_database_v2.json` + `nogship.mm`).

---

## 2. MYL*N ROS FLEET (7 units)

| Unit | Product dir |
|------|-------------|
| MYL0N | `aocros/products/myl0n_ros` |
| MYL1N | `aocros/products/myl1n_ros` |
| MYL2N | `aocros/products/myl2n_ros` |
| MYL3N | `aocros/products/myl3n_ros` |
| MYL4N | `aocros/products/myl4n_ros` |
| MYL5N | `aocros/products/myl5n_ros` |
| MYL6N | `aocros/products/myl6n_ros` |

*(Agent profiles: `aocros/agent_profiles/MYL0N-1_PROFILE_v2.yaml`, `MYL0N-2_PROFILE_v2.yaml`)*

---

## 3. CHARACTERS & 3D MODELS

| Character | Type | Source |
|-----------|------|--------|
| **Raven** (Myl1Ssa.R8s) | Character — bottle + skeleton + facial + manifest | email 2026-09-24 |
| **Android** | 3D model — Hi3D segmented modular female cyborg torso | email 2026-10-12 |
| **Cyborg** | 3D model — glossy black realistic female cyborg | email 2026-10-12 (Hi3D link) |

---

## 4. FLEET ASSETS (images)

| Asset | File |
|-------|------|
| SEED ONE — spacecraft (massive grey) | `fleet/images/` |
| SEED ONE — corridor | `fleet/images/` |
| Hi3D renders (×4) | `fleet/images/` |
| Copilot renders (×3) | `fleet/images/` |
| Misc fleet renders | `fleet/images/` |

---

## 5. SOURCE DATA STATUS

| File | Status |
|------|--------|
| `nog_extraction/ship_database_v2.json` | ⚠️ **Not yet in workspace** — needs extraction from MORTIMER/N'og nog |
| `nogship.mm` | ⚠️ **Not yet in workspace** |

**Action needed:** locate/pull `ship_database_v2.json` + `nogship.mm` from the MORTIMER extraction so the SEED ONE spec can be cross-referenced against the canonical ship database.

---

## 6. EXISTING FLEET DOCS (aocros)

- `FLEET_STATUS_REPORT.md`
- `FLEET_ACTIVATION_BATCH_20260222.md`
- `FLEET_SKILL_DEPLOYMENT_BATCH_2.md`
- `FLEET_NEW_SKILLS_AVAILABLE.md`
- `FLEET_PORTAL_SECURITY_POLICY.md`
- `operations/FLEET_LOCATIONS_REPORT.md`
- `operations/FLEET_ENRICHMENT_ANNOUNCEMENT.md`
