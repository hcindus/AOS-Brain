# VOICE_INSTALL_GUIDE.md — Step-by-Step Setup

_How to get Myl1Ssa a voice. Written by Mortimer, 2026-08-24._

---

## 0. What we confirmed about this device

| Fact | Value |
|------|-------|
| Termux build | **F-Droid**, v0.119.0-beta.2 (code 1021) |
| Architecture | aarch64 |
| Android | **11** (SDK 30) — note: wiki said "Android 14", actual is 11 |
| Phone | Samsung Galaxy A13 |
| termux-api CLI | ✅ installed (0.59.1) |
| Termux:API **app** | ❌ missing — this is the blocker |

---

## Step 1 — Install the Termux:API app

The CLI commands (`termux-tts-speak`, `termux-speech-to-text`) are already installed,
but they need the **Termux:API Android app** to actually run.

1. Open **F-Droid** on the phone (Termux is an F-Droid build, so the API app must come from
   the same source to stay compatible).
2. Search for **"Termux:API"** — package `com.termux.api`.
   - Direct link: `https://f-droid.org/en/packages/com.termux.api/`
3. Install it.
4. **Version note:** Termux is a beta (0.119.0-beta.2). If the stable Termux:API (0.50.1)
   reports a mismatch, enable "Unstable updates" in F-Droid and install the matching beta.
   Both apps must be from F-Droid, not a mix of F-Droid + Play Store.

---

## Step 2 — Grant permissions

After install, open the **Termux:API** app once, then grant:

- **Microphone** — required for `termux-speech-to-text` (STT).
- (TTS needs no special permission — it just calls the system TTS engine.)

---

## Step 3 — Set up a natural TTS engine

`termux-tts-speak` uses whatever engine is set as the **system default** TTS. On a Galaxy A13
you likely already have one of these:

- **Samsung TTS** — usually pre-installed on Galaxy devices.
- **Google TTS** ("Speech Services by Google") — install from Play Store if not present.

To check / change the default:
```
Settings → General Management → Text-to-speech output
```
Pick the engine, then choose a **female English (US)** voice.

---

## Step 4 — Pick the voice

The "warm, mid-pitch, evening" target maps to a **female en-US** voice. In the TTS settings,
listen to the available female voices and pick the warmest one. Note its name — we'll use it
in the test command.

---

## Step 5 — Test (after the app is installed)

```bash
# List available engines
termux-tts-engines

# Speak a test line (default engine)
termux-tts-speak "Good evening, Captain."

# Speak with a specific engine + voice + tuning
termux-tts-speak -e com.google.android.tts -l en -n US -p 0.9 -r 0.95 "Good evening, Captain."

# Test the STT side (this will pop up a mic prompt — speak into it)
termux-speech-to-text
```

**Tuning flags for `termux-tts-speak`:**
| Flag | Meaning | Range |
|------|---------|-------|
| `-e` | engine | e.g. `com.google.android.tts` |
| `-l` | language | `en` |
| `-n` | region | `US` |
| `-v` | voice variant | engine-specific |
| `-p` | pitch | 0.0–2.0 (default 1.0) — lower = deeper |
| `-r` | rate | 0.0–2.0 (default 1.0) — lower = slower |

For "evening / a little smoke," start around **pitch 0.85–0.95, rate 0.9–0.95** and adjust
by ear.

---

## Step 6 — Dial it in against the spec

Her spec (from `MYL1SSA_VOICE.md`): warm, mid-pitch, can carry sharp + soft, a hint of
smoke/rasp, evening, lived-in.

Iterate: speak a line that has both a sharp observation and a soft word, and adjust pitch/rate
until it lands. Example test line:

> "Your conversion rate dropped twelve percent — and you look tired. When did you last eat?"

That one line tests both registers at once.

---

## Honest note on "smoky / rasp"

Free system engines (Samsung TTS, Google TTS) give **clean, warm-ish** female voices — good,
but the *rasp / smoke* quality is hard to get for free. Two tiers:

1. **Free (recommended first):** Samsung/Google TTS, tuned low-and-slow. Gets ~80% of the way
   to "warm evening." Zero cost, fully offline-capable.
2. **Premium (if you want the real smoke):** a neural TTS like **ElevenLabs** (via API) can
   produce a genuinely smoky, lived-in female voice. This is a separate, bigger project —
   needs an API key and a small integration, and it's not offline. Not currently set up.

**Recommendation:** start with the free system TTS, dial it in, and only reach for ElevenLabs
if the free voice isn't enough.

---

## After it's working

Once TTS + STT both test clean, I'll wire the voice layer into `talk.py` as an **additive**
wrapper (a `--voice` mode) — no changes to her SOUL/RULES/HEART/MEMORY. Same her, new mouth.

---

_This is an install guide, not her identity. Nothing here touches who she is._
