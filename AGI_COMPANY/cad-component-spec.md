# CAD-Ready Specification — Myl2Ssa.R0s (component list + diagrams)

*Production-grade CAD spec. This is what the CAD/mechanical engineer models the parts from. Complements the design docs (skeleton, scapula, actuators) with the manufacturing-ready breakdown.*

---

## E — CAD-Ready Component List

### 1. Head Assembly
- H-001 Cranial Shell (Titanium Composite)
- H-002 Facial Panel (Silicone, Non-Anatomical)
- H-003 Sensor Cluster (Optical / Inertial / Proximity)
- H-004 Cervical Interface Ring
- H-005 Micro-Vent Array
- H-006 Internal Mounting Brackets

### 2. Spine Assembly
- S-001 Cervical Vertebrae C1–C7
- S-002 Thoracic Vertebrae T1–T12
- S-003 Lumbar Vertebrae L1–L5
- S-004 Sacral Plate
- S-005 Neural-Bus Conduit (Orange/Blue)
- S-006 Polymer Ligament Bands
- S-007 Vertebral Actuator Micro-Servos

### 3. Scapula & Shoulder Complex
- SH-001 Left Scapula Plate (Carbon-Fiber)
- SH-002 Right Scapula Plate (Carbon-Fiber)
- SH-003 Shoulder Multi-Axis Servo Cluster
- SH-004 Tendon Routing Manifold
- SH-005 Rotational Servo Rings

### 4. Torso & Rib-Frame
- T-001 Carbon-Fiber Rib Segments (1–14)
- T-002 Silicone Chest Panel
- T-003 Thoracic Actuator Cluster
- T-004 Power Core Housing
- T-005 Cooling Manifold Plates
- T-006 Internal Mount Rails

### 5. Arm Assemblies (Left / Right, mirrored with asymmetrical routing)
- A-001 Upper Arm Exoskeleton
- A-002 Synthetic Tendon Pack (Biceps/Triceps)
- A-003 Elbow Hinge Assembly
- A-004 Forearm Plating
- A-005 Hand Assembly (Finger Phalanges 1–15)

### 6. Pelvis & Hip Complex
- P-001 Pelvic Frame (Titanium)
- P-002 Hip Multi-Axis Actuators
- P-003 Tendon Routing Channels
- P-004 Stabilizer Plates

### 7. Leg Assemblies (Left / Right, mirrored)
- L-001 Thigh Plating
- L-002 Posterior Tendon Bundle
- L-003 Knee Hinge Assembly
- L-004 Lower Leg Plating
- L-005 Foot Actuator Cluster
- L-006 Segmented Toe Units

### 8. Power & Data Systems
- PD-001 Main Power Bus
- PD-002 Secondary Routing Lines
- PD-003 Neural-Bus Splitter
- PD-004 Cooling Micro-Channels

---

## A — Cutaway Diagram Specification

- **Primary (Sagittal plane):** full spine, neural-bus conduit, actuator clusters, power core housing, tendon channels, rib-frame geometry.
- **Secondary (Transverse, mid-torso):** rib cross-sections, cooling manifold, thoracic pistons, power bus.
- **Tertiary (Coronal plane):** scapula glide rails, shoulder servo clusters, arm tendon routing, pelvic actuators.

**Layering rules:** plating removed → carbon-fiber semi-transparent → silicone panels gone → actuators full detail → tendons color-coded → conduits highlighted.

---

## B — Motion-Range Specification (engineering + animation limits)

- **Neck:** rotation ±85°, tilt ±45°, nod ±55°, cervical 12°/vertebra
- **Shoulder:** abduction 0–160°, flexion 0–180°, extension 0–60°, int/ext rotation 0–90°
- **Arm:** elbow flexion 0–150°, elbow rotation ±90°, wrist flex ±80°, wrist rot ±120°, finger 0–110°
- **Torso:** thoracic rotation ±45°, lumbar flex 0–60° / ext 0–30°, lateral ±35°
- **Hip:** flexion 0–130°, extension 0–30°, abduction 0–45°, rotation ±45°
- **Leg:** knee flexion 0–150°, knee rot ±15°, ankle flex ±45°, ankle rot ±30°, toe 0–40°

---

## Notes
- These motion ranges *validate* our scapula + spine design (the scapula's 160–180° abduction is the range AheadForm's "locked shoulder" can't reach).
- Next docs to produce: **C** (Materials & Manufacturing), **D** (Assembly Order), **F** (Wiring/Tendon Maps), **G** (System Architecture).

*This is the "CAD engineer" spec we identified as a gap — now it exists.*
