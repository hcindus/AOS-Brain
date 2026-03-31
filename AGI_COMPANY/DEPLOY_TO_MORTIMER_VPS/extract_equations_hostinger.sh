#!/bin/bash
# extract_equations_hostinger.sh - Run in Hostinger Browser Terminal
# Extracts Mortimer's equations, weights, and constants

echo "═══════════════════════════════════════════════════════════"
echo "🔍 EXTRACTING MORTIMER'S EQUATIONS & CONSTANTS"
echo "═══════════════════════════════════════════════════════════"
echo "Target: Mortimer VPS (31.97.6.30)"
echo "Time: $(date)"
echo ""

mkdir -p /tmp/mortimer-equations
cd /tmp/mortimer-equations

# 1. Find equation files
echo "[1/5] Scanning for equations..."
find ~ -type f \( \
    -name "*equation*" -o \
    -name "*formula*" -o \
    -name "*constant*" -o \
    -name "*param*" -o \
    -name "*weight*" -o \
    -name "*logic*" -o \
    -name "*gate*" -o \
    -name "*pattern*" \
    \) 2>/dev/null | head -50 > equation_files.txt

# 2. Find Python files with mathematical functions
echo "[2/5] Scanning Python files..."
grep -r -l "def.*formula\|def.*equation\|def.*calculate\|def.*compute\|weights\|constants\|bias\|threshold" \
    ~ --include="*.py" 2>/dev/null | head -50 > python_equations.txt

# 3. Find brain configuration files
echo "[3/5] Finding brain configs..."
find ~ -type f \( \
    -name "brain*.json" -o \
    -name "brain*.yaml" -o \
    -name "brain*.py" -o \
    -name "config*.json" -o \
    -name "model*.json" \
    \) 2>/dev/null | head -30 > brain_configs.txt

# 4. Search specific directories
echo "[4/5] Checking common locations..."
for dir in ~/.brain ~/brain /opt/brain /var/lib/brain ~/data/brain ~/models ~/.models; do
    if [ -d "$dir" ]; then
        echo "$dir" >> brain_locations.txt
        ls -la "$dir" >> brain_locations.txt 2>/dev/null
        echo "---" >> brain_locations.txt
    fi
done

# 5. Extract actual equation content
echo "[5/5] Extracting equation content..."

# Extract from Python files
while read -r file; do
    if [ -f "$file" ]; then
        echo "=== $file ===" >> equations_extracted.txt
        grep -A5 -B2 "def\|class\|formula\|equation\|weight\|constant\|bias" "$file" 2>/dev/null | head -50 >> equations_extracted.txt
        echo "" >> equations_extracted.txt
    fi
done < python_equations.txt 2>/dev/null

# Create master tarball
echo ""
echo "📦 Creating equation archive..."
tar -czf mortimer-equations.tar.gz \
    equation_files.txt \
    python_equations.txt \
    brain_configs.txt \
    brain_locations.txt \
    equations_extracted.txt \
    $(cat brain_configs.txt 2>/dev/null | head -20) \
    2>/dev/null

# Create manifest
cat > equation_manifest.json << EOF
{
  "source": "Mortimer VPS",
  "extraction_date": "$(date -Iseconds)",
  "files_found": {
    "equations": $(wc -l < equation_files.txt 2>/dev/null || echo 0),
    "python_files": $(wc -l < python_equations.txt 2>/dev/null || echo 0),
    "brain_configs": $(wc -l < brain_configs.txt 2>/dev/null || echo 0)
  },
  "archive": "mortimer-equations.tar.gz",
  "location": "/tmp/mortimer-equations/"
}
EOF

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "✅ EXTRACTION COMPLETE"
echo "═══════════════════════════════════════════════════════════"
echo ""
ls -lh /tmp/mortimer-equations/
echo ""
echo "Download command (from Miles VPS):"
echo "  scp mortimer@31.97.6.30:/tmp/mortimer-equations/mortimer-equations.tar.gz ./"
echo ""
echo "═══════════════════════════════════════════════════════════"
