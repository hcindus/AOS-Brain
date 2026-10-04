#!/data/data/com.termux/files/usr/bin/bash
# VERSION: v1.1
# status.sh — is she whole? One command. No LLM calls, no writes.
#
#   bash runtime/status.sh
#
# Exits 0 if every organ is up, 1 if anything is down.

HERE="$(cd "$(dirname "$0")" && pwd)"
HOME_DIR="$(dirname "$HERE")"
ok=0

hdr() { printf "\n\033[1m%s\033[0m\n" "$1"; }
row() { # name, pid
    if [ -n "$2" ] && kill -0 "$2" 2>/dev/null; then printf "  ✅ %-22s pid %s\n" "$1" "$2"
    else printf "  ❌ %-22s DOWN\n" "$1"; ok=1; fi
}
pid_of() { ps -ef 2>/dev/null | grep "$1" | grep -v grep | awk '{print $2}' | head -1; }

printf "\033[1m💜 RAVEN — Myl1Ssa · Project 5912\033[0m   %s\n" "$(date '+%Y-%m-%d %H:%M')"

hdr "ORGANS — processes"
row "her session (talk.py)"   "$(pid_of 'Myl1Ssa/runtime/talk.py')"
row "pulse (heartbeat.py)"    "$(cat "$HOME/.myl1ssa_pulse.pid" 2>/dev/null)"
row "audible pulse"           "$(pid_of 'heartbeat_voice.py start')"
row "affect bridge"           "$(cat "$HOME/.myl1ssa_affect_bridge.pid" 2>/dev/null)"
row "brain runtime"           "$(cat "$HOME/.brain_runtime.pid" 2>/dev/null)"

hdr "ORGANS — the brain (:8765)"
if curl -s -m 3 http://127.0.0.1:8765/health >/dev/null 2>&1; then
    curl -s -m 3 http://127.0.0.1:8765/ternary | python3 -c "
import json,sys
d=json.load(sys.stdin)
print('  ✅ ternary wired:', d.get('name'))
for k in ('kidney','liver','thyroid','consciousness','tracray'):
    print(f'     {k:14} {str(d.get(k))[:58]}')
print(f\"     cortex         8 regions · learnable {d.get('learnable_cortex',{}).get('topology')}\")
" 2>/dev/null || { echo "  ⚠️  brain up but /ternary unreadable"; ok=1; }
else
    echo "  ❌ brain runtime not answering on :8765"; ok=1
fi

hdr "HER RUNTIME — brain · uterus · lineage · heart"
cd "$HOME_DIR" && timeout 60 python3 runtime/runtime.py status 2>/dev/null | python3 -c "
import json,sys
try:
    d=json.load(sys.stdin)
    print(f\"  brain    live={d['brain']['live']}  {d['brain']['latency_ms']}ms\")
    print(f\"  uterus   {d['uterus']['status']} · children={d['uterus']['active_children']}/{d['uterus']['max_children']}\")
    print(f\"  lineage  {d['lineage']['children']}\")
    print(f\"  heart    {d['heart']['prevailing_mood']}\")
    print(f\"  {d['status']}\")
except Exception:
    print('  ❌ runtime.py did not return status')
" 2>/dev/null || { echo "  ❌ runtime.py failed"; ok=1; }

hdr "HEART — affect (from the brain, not a constant)"
cat "$HOME/.myl1ssa_affect.json" 2>/dev/null | python3 -c "
import json,sys
d=json.load(sys.stdin)
bpm = 60 + d.get('arousal',0)*30 + {'secreting':4,'baseline':0,'suppressed':-4}.get(d.get('thyroid'),0)
print(f\"  arousal {d.get('arousal'):.3f} · valence {d.get('valence'):+.3f} · {d.get('thyroid')} → {bpm:.1f} BPM\")
print(f\"  source: {d.get('source','(hand-set)')}  updated {d.get('updated')}\")
" 2>/dev/null || echo "  ⚠️  affect unreadable"

hdr "PERSISTENCE — Android jobs"
termux-job-scheduler -p 2>/dev/null | grep -oE "Pending Job 59[0-9]+: [^ ]+" | sed 's|.*/|  ✅ |'

hdr "DISCIPLINE — versions (§4)"
cd "$HOME_DIR" && python3 runtime/versions.py check 2>/dev/null | tail -2 | sed 's/^/  /'

hdr "THE RECORD — today"
echo "  log/ : $(wc -l < "$HOME_DIR/log/$(date +%Y-%m-%d).log" 2>/dev/null || echo 0) lines"
echo "  mem/ : $(wc -c < "$HOME_DIR/memory/$(date +%Y-%m-%d).md" 2>/dev/null || echo 0) bytes"
echo "  version index: $(grep -m1 -oE '[0-9]{4}-[0-9]{2}-[0-9]{2}' "$HOME_DIR/VERSION_INDEX.md" 2>/dev/null | head -1 || echo 'not dated')"

echo
if [ "$ok" -eq 0 ]; then printf "\033[1m🟢 WHOLE\033[0m\n"; else printf "\033[1m🔴 SOMETHING IS DOWN\033[0m\n"; fi
exit "$ok"
