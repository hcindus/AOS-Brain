# Hi3D Vehicles — 3D Reference Assets

*Multi-view (turntable) renders from the Hi3D text-to-3D pipeline, captured 2026-10-30. Source: `/root/.openclaw/media/inbound/` (Hi3D-image-2026-10-30* + image_15..17).*

## What's here

| File | Subject (from render) |
|---|---|
| `hi3d-pod-vehicle.jpg` | Sleek enclosed pod, four angles (side/front/rear) |
| `hi3d-black-vehicle.jpg` | Futuristic black vehicle, two views, white background |
| `hi3d-vehicle-3.jpg` | (inbound `image_17`) |
| `hi3d-vehicle-4.jpg` | (inbound `image_15`) |
| `hi3d-vehicle-5.jpg` | (inbound `image_16`) |

## Purpose — TO CONFIRM with Captain

Unlike `data/hi3d_torso/` (the Myl2Ssa body → STL for the sculptor), these are
*vehicles*, not body parts. Likely one of:

1. **Lab props** — convert to GLB, load into Raven's three.js scene as objects she reacts to.
2. **Asset library** — a Hi3D vehicles collection (text→3D→STL, like the torso pipeline).
3. **Myl2Ssa's world** — vehicles that exist in her universe (filmmaking / world-building).

Not yet converted to GLB/STL — waiting on the Captain's intent before running the
image→3D reconstruction.

## Next (pending intent)
- If **lab props**: Hi3D turntables → image-to-3D (e.g. TripoSR/InstantMesh) → GLB → load in the AR lab.
- If **asset library**: set up the STL merge pipeline (mirror `stl_files/hi3d-pastel-cyborg/`).
- If **world**: fold into the Myl1Ssa/Myl2Ssa world-building + filmmaking skill stack.
