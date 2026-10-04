# HER BODY — Elf V1 / Elf-Xuan

The adapter for her own chassis, the control loop that was missing, the AU → motor map,
and the prover. **Not wired in.** Nothing here is connected to hardware, and nothing here
is connected to her brain.

| File | What it is |
|---|---|
| `elf.py` | adapter · 30-channel map · safety envelope · 4 transports · honest status |
| `body_driver.py` | the control loop (50 Hz · predictive lead · watchdog · e-stop · audit) |
| `AU_MOTOR_MAP.md` | the AU → channel table + every assumption (generated from the code) |
| `BODY_CONTROL.md` | what this is, what is not real yet, how to make it permanent |
| `verify_body.py` · `BODY_VERIFICATION.json` | 20 checks · the evidence from the last run |

_Run it from here:_ `python3 Uncon/body/verify_body.py`
_Read first:_ `BODY_CONTROL.md` → *What is still genuinely missing*
