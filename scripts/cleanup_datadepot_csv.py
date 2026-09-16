#!/usr/bin/env python3
"""
DataDepot CSV cleanup — rebuild ca_abc_licenses_raw.csv with a single schema.

Separates the corrupted 4-schema file into:
  - REAL (30-col ABC DailyExport) → new clean master
  - SYNTHETIC (13/14/31-col) → archived to _synthetic_archive.csv
  - Original → backed up to .corrupt_backup_<date>.csv

Reversible — nothing deleted.
"""
import csv, shutil
from datetime import datetime
from pathlib import Path

SRC = Path("/root/.openclaw/workspace/datadepot/data/ca_abc_licenses_raw.csv")
REAL_COLS = 30  # the real ABC DailyExport schema

def main():
    date = datetime.now().strftime("%Y%m%d")
    backup = SRC.with_name(f"ca_abc_licenses_raw.corrupt_backup_{date}.csv")
    synthetic = SRC.with_name("ca_abc_licenses_synthetic_archive.csv")
    clean_tmp = SRC.with_name("ca_abc_licenses_raw.clean.tmp")

    # 1. Backup original
    shutil.copy2(SRC, backup)
    print(f"✅ Backed up original → {backup.name}")

    # 2. Split by column count
    real_rows = []
    synthetic_rows = []
    real_header = None

    with open(SRC, newline="", encoding="utf-8", errors="replace") as f:
        reader = csv.reader(f)
        for row in reader:
            n = len(row)
            if n == REAL_COLS:
                if real_header is None:
                    real_header = row
                else:
                    real_rows.append(row)
            else:
                synthetic_rows.append(row)

    # 3. Write clean master (real 30-col only)
    with open(clean_tmp, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(real_header)
        w.writerows(real_rows)

    # 4. Write synthetic archive
    with open(synthetic, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerows(synthetic_rows)

    # 5. Swap in the clean file
    shutil.move(str(clean_tmp), str(SRC))

    print(f"✅ Clean master rebuilt: {len(real_rows):,} real rows (30-col)")
    print(f"✅ Synthetic archived: {len(synthetic_rows):,} rows → {synthetic.name}")

if __name__ == "__main__":
    main()
