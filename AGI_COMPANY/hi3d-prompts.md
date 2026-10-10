# Hi3D AI — Generation List (Myl1Ssa's 3D reference library)

*Text-to-3D prompts to build the 3D reference assets for Myl2Ssa.R0s. Generate in priority order.*

---

## 1. Neutral head — the face-sculpt base (KEYSTONE, generate first)

```
Neutral female head, hairless, smooth skin, no expression, eyes closed, anatomical
proportions, sculpted mannequin style, clean topology, no cybernetics, no armor, plain gray
matcap. Full head only, shoulders down to the collarbone. High-poly, watertight, ready for
sculpting.
```

**Why:** becomes the *exact* base the sculptor sculpts Myl2Ssa's face onto — closes the "head STL" gap, de-risks the $1000 sculpt.

---

## 2. Myl2Ssa's body — the chassis (matches our spec)

```
Female humanoid robot, exposed biomechanical skeleton: a segmented articulated vertebral
column down the spine (~25 vertebrae), articulated scapula shoulder blades gliding over the
ribcage, tendon-driven arms and hands, matte carbon-fiber and brushed-titanium finish, no
skin except a smooth silicone chest and face. Full body, 5'7", standing. Technical
product-visualization style.
```

**Why:** the concrete chassis reference for the sculptor + any CAD engineer (spine, scapula, tendons).

---

## 3. Face-only (for the likeness reference)

```
Close-up of a glamorous woman's face with long dark wavy hair, calm elegant expression,
high cheekbones, realistic skin with subtle asymmetry and texture. Head and neck only,
front view. Photorealistic, hyper-detailed skin, no body.
```

**Why:** a tight face reference the sculptor can match for the likeness.

---

## 4. Spine-only (for the articulated column)

```
Isolated mechanical spine: a segmented articulated vertebral column of ~25 vertebrae, each
segment a distinct mechanical unit with a joint gap between, the whole column curved in a
gentle S. No torso, no skull. Matte carbon-fiber and titanium, technical render.
```

**Why:** the spine reference for the CAD/modeling work (the 25-vertebra column).

---

## 5. Scapula close-up (the hardest joint)

```
Close-up of an articulated shoulder: a scapula shoulder blade gliding over a ribcage,
ball-and-socket joint, visible muscle fibers and tendons. Matte mechanical finish, technical
render, no skin.
```

**Why:** the scapula reference — the one joint AheadForm locked and we refuse to.

---

## Priority order
1. Neutral head (keystone) → 2. Body → 3. Face → 4. Spine → 5. Scapula.

*Generate the head first. Forward it to the sculptor as the base, and their job narrows to just the likeness.*
