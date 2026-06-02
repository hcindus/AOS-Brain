#!/bin/bash
# Search Teriyaki Madness locations in DepotChaos

case "$1" in
  state)
    sqlite3 /root/.openclaw/workspace/DepotChaos/depot_chaos.db "SELECT store_name, address, phone FROM teriyaki_madness WHERE state = '$2' AND status = 'OPEN';"
    ;;
  city)
    sqlite3 /root/.openclaw/workspace/DepotChaos/depot_chaos.db "SELECT store_name, address, phone FROM teriyaki_madness WHERE city LIKE '%$2%' AND status = 'OPEN';"
    ;;
  zip)
    sqlite3 /root/.openclaw/workspace/DepotChaos/depot_chaos.db "SELECT store_name, address, phone FROM teriyaki_madness WHERE zip = '$2';"
    ;;
  open)
    sqlite3 /root/.openclaw/workspace/DepotChaos/depot_chaos.db "SELECT state, COUNT(*) as count FROM teriyaki_madness WHERE status = 'OPEN' GROUP BY state ORDER BY count DESC;"
    ;;
  coming)
    sqlite3 /root/.openclaw/workspace/DepotChaos/depot_chaos.db "SELECT store_name, city, state FROM teriyaki_madness WHERE status = 'COMING SOON';"
    ;;
  *)
    echo "Usage: $0 {state|city|zip|open|coming} [value]"
    echo "Examples:"
    echo "  $0 state AZ      - List all AZ locations"
    echo "  $0 city Phoenix  - Search by city"
    echo "  $0 open          - Count by state"
    ;;
esac
