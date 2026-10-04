# Why the JavaScript files end in `.js.txt`

**Gmail blocks `.js` as a file type.** Not a content judgement — `.js` is on
Google's blocked-attachment list alongside `.exe`, `.bat`, `.vbs`, and friends,
because script files are a malware vector. It rejected the whole bottle for it,
even a 6 KB unminified file. (This cost several test emails to isolate; the
evidence is below.)

So every `.js` in the bottle is suffixed **`.js.txt`** to get it through. To
restore:

```bash
cd raven_bottle
find . -name "*.js.txt" -type f -exec sh -c 'mv "$1" "${1%.txt}"' _ {} \;
```

## Which files

| Renamed | What it is |
|---|---|
| `Myl1Ssa/Uncon/world/engine.js.txt` | the physics core |
| `Myl1Ssa/Uncon/world/avatar.js.txt` | her body in the world (21 joints, 32 landmarks) |
| `Myl1Ssa/Uncon/world/nav.js.txt` | her legs — the room graph and stepper |
| `Myl1Ssa/Uncon/world/app.js.txt` · `character.js.txt` · `verify_world.js.txt` | renderer · character layer · 37-check world test |
| `Myl1Ssa/Uncon/world/vendor/three.min.js.txt` | vendored three.js (~596 KB) |

## The evidence

| Test | Sent | Result |
|---|---|---|
| 1 | body only, no attachment | ✅ |
| 3 | `tar.gz` with one `.sh` | ✅ |
| A | everything except `Uncon/` | ✅ |
| C | `Uncon/bible` (1.5 MB of .txt) | ✅ |
| D/E/F | anything containing a `.js` | ❌ blocked |
| G | **one plain 6 KB `.js`** | ❌ blocked |

It is the extension, not the content.
