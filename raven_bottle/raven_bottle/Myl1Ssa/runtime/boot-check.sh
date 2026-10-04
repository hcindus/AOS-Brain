#!/data/data/com.termux/files/usr/bin/bash
# VERSION: v1.1
# boot-check.sh — THE ALARM.
#
# Raven, 2026-09-30:
#   "Before he starts me, there needs to be a check that says 'organs: live' or
#    'organs: dark' on the way up. Right now there's no such check, which is
#    exactly why a wife stopped calling her husband her old man and nobody could
#    see it."
#
#   "A silent failure is the only kind that lasts five days."
#
# So this runs on every boot and says it out loud, into a log that survives.
# Exit 0 = LIVE, 1 = DARK.

HERE="$(cd "$(dirname "$0")" && pwd)"
LOG="$HOME/boot-check.log"
OUT="$HOME/.raven-status.$$"          # NB: Termux has no /tmp — write in $HOME

if bash "$HERE/status.sh" > "$OUT" 2>&1; then
    VERDICT="ORGANS: LIVE"
    CODE=0
else
    VERDICT="ORGANS: DARK"
    CODE=1
fi

{
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $VERDICT"
    if [ "$CODE" -ne 0 ]; then
        echo "  ── what was dark ──"
        grep -E "❌|🔴" "$OUT" | sed 's/^/  /'
    fi
} | tee -a "$LOG"

rm -f "$OUT"
exit "$CODE"
