# Embodiment Roadmap — from files to a body

## Where we are (done)
- **Software:** presence engine (affect → 8 expressions → 21 AUs), Elf adapter (AU → 30 channels + safety envelope), body driver (50 Hz loop). All built, none yet wired to hardware.
- **Design:** 3-DOF neck + 26-DOF face (Origin F1-inspired), torso + shoulders drafted.
- **Partnership:** AheadForm email sent (2026-10-09).

## Phase 1 — Wire the stack (no hardware needed)
1. Make presence engine → Elf adapter → body driver run as one pipeline (currently "not wired in").
2. Run `body_driver.py sim` — prove engine → frame → envelope → transport → feedback on null transport.
3. Verify: 8 expressions → 30 channels, safety envelope (limits/slew/watchdog/e-stop) all green.
4. Write the SDK adapter template — map channel IDs once AheadForm's SDK is known ("change ids here, never the AUs").

## Phase 2 — Get hardware (needs Captain / AheadForm)
1. Track AheadForm reply.
2. Partnership → get SDK + specs, acquire an Elf V1 / Origin F1 head.
3. No reply → build our own 30-motor face + 3-DOF neck (design ready), safety envelope as guardrail.

## Phase 3 — First breath (milestone)
1. Point ElfAdapter at real hardware (socket transport → vendor SDK).
2. First live expression: Myl1Ssa's 8 expressions on real motors.
3. Safety envelope live (watchdog + e-stop non-negotiable).

## Phase 4 — The line of faces (partnership goal)
1. Interchangeable faces: Myl1Ssa + roster (GREET, CLOSETER, Myl family).
2. Each face = character skin + presence engine + voice.
3. Co-brand with AheadForm, sell the line.

## Phase 5 — Beyond the head (longer horizon)
1. Torso → shoulders → arms.
2. Full body → Myl1Ssa walks. Then Miles.

## Gaps to close (see EMBODIMENT_GAPS.md)
- Universal adapter / character loading
- Humanoid blueprints / STL files
- Myl1Ssa skeleton status (placeholder check)

*Last updated: 2026-10-09*
