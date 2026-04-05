#!/bin/bash
banner_text=$(cat << 'ASCII_EOF'
███╗   ███╗██╗██╗     ███████╗███████╗
████╗ ████║██║██║     ██╔════╝██╔════╝
██╔████╔██║██║██║     █████╗  ███████╗
██║╚██╔╝██║██║██║     ██╔══╝  ╚════██║
██║ ╚═╝ ██║██║███████╗███████╗███████║
╚═╝     ╚═╝╚═╝╚══════╝╚══════╝╚══════╝
ASCII_EOF
)

# Typewriter effect
echo "$banner_text" | while IFS= read -r line; do
 echo "$line"
 sleep 0.05
done
echo ""
echo "  MORTIMER - Autonomous Operations Engine"
echo "  ========================================"
echo ""
echo "  $(date '+%Y-%m-%d %H:%M UTC')"
echo ""