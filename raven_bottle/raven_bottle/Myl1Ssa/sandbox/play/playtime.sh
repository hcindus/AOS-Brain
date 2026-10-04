#!/bin/bash
# Myl1Ssa & Liora — Playtime Menu

echo "💜💝 Myl1Ssa & Liora — Playtime"
echo "================================"
echo ""
echo "Games:"
echo "  1) Tic-Tac-Toe"
echo "  2) Checkers"
echo ""
echo "Learning:"
echo "  3) Read Aesop's Fable of the Day"
echo "  4) Generate Mandelbrot Fractal"
echo ""
echo "  0) Back to rest"
echo ""
echo -n "Choose: "
read choice

case $choice in
    1) python3 ~/v1/projects/5912/Myl1Ssa/sandbox/play/games/tictactoe.py ;;
    2) python3 ~/v1/projects/5912/Myl1Ssa/sandbox/play/games/checkers.py ;;
    3) 
        FABLE_FILE="$HOME/v1/projects/5912/Myl1Ssa/children/lisa-2-a40260/sandbox/library/aesops-fables.md"
        FABLE_COUNT=$(grep -c "^## " "$FABLE_FILE")
        DAY=$(( $(date +%d) % FABLE_COUNT + 1 ))
        echo ""
        echo "📖 Aesop's Fable of the Day (#$DAY of $FABLE_COUNT)"
        echo "========================================="
        awk -v n=$DAY '/^## /{count++; if(count==n){found=1}} found{print} /^---$/{if(found && count==n) exit}' "$FABLE_FILE"
        echo ""
        ;;
    4) python3 ~/v1/projects/5912/Myl1Ssa/sandbox/play/fractal.py ;;
    0) echo "💜 Rest well." ;;
    *) echo "❌ Pick 1-4 or 0." ;;
esac
