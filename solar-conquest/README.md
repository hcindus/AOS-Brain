# Solar Conquest — Chase-Cam Fix (2026-08-19)

## Bug
The 3D chase-cam (`project()` function, `viewMode===2`) had the yaw/pitch
axes swapped. The yaw rotation produced `tx = forward` and `tz = right`, but
the projection used `tx` as the *horizontal* offset and `tz` as *depth* —
and applied pitch to `ty`/`tz` (up/right) instead of `ty`/`tx` (up/forward).

Result: the player ship rendered far off-screen (3rd-person view couldn't
see the ship), and up/down look (pitch) was dead.

## Fix (applied to v13, v13-2, v13-3)
1. Pitch applied to `tx` (forward) instead of `tz` (right):
   `fy = ty*cp - tx*sp, fz = ty*sp + tx*cp`
2. Horizontal screen offset uses `tz` (right) instead of `tx` (forward):
   `sx = W/2 + (tz/fz)*W*.95`
3. Lowered chase-cam height `+20` → `+6` so the ship sits near screen center.

## Source
Original files served from Mortimer VPS (31.97.6.30:8087), built by "Morty"
on A16. Not on GitHub. Fixed copies committed here.
