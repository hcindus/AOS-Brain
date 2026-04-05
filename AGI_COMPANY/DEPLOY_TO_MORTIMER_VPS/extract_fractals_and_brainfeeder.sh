#!/bin/bash
# extract_fractals_and_brainfeeder.sh - Run on Mortimer VPS via Hostinger Browser Terminal
# Extracts fractal patterns, brainfeeder.py, and brain systems

echo "═══════════════════════════════════════════════════════════"
echo "🧠 EXTRACTING FRACTAL PATTERNS & BRAINFEEDER"
echo "═══════════════════════════════════════════════════════════"
echo "Target: Mortimer VPS"
echo "Time: $(date)"
echo ""

mkdir -p /tmp/mortimer-fractals
cd /tmp/mortimer-fractals

# 1. Find brainfeeder.py
echo "[1/6] Searching for brainfeeder.py..."
find ~ -type f -name "*brainfeeder*" 2>/dev/null | head -20 > brainfeeder_files.txt

# Also check variations
find ~ -type f \( \
    -name "*brain_feeder*" -o \
    -name "*BrainFeeder*" -o \
    -name "*feeder*.py" \
    \) 2>/dev/null | grep -v __pycache__ >> brainfeeder_files.txt

# 2. Find brain.py
echo "[2/6] Searching for brain.py..."
find ~ -type f -name "*brain*.py" 2>/dev/null | head -30 > brain_files.txt

# 3. Find fractal patterns
echo "[3/6] Searching for fractal patterns..."
find ~ -type f \( \
    -name "*fractal*" -o \
    -name "*pattern*" -o \
    -name "*fractal*.json" -o \
    -name "*pattern*.json" \
    \) 2>/dev/null | head -50 > fractal_files.txt

# 4. Search inside .aos directory specifically
echo "[4/6] Checking ~/.aos directory..."
if [ -d ~/.aos ]; then
    echo "✅ .aos directory found"
    ls -laR ~/.aos/ > aos_structure.txt 2>/dev/null
    
    # Deep search in .aos
    find ~/.aos -type f \( -name "*.py" -o -name "*.json" -o -name "*.txt" \) 2>/dev/null | head -100 > aos_files.txt
    
    # Search for "fractal" in content
    grep -r "fractal" ~/.aos --include="*.py" --include="*.json" --include="*.txt" 2>/dev/null | head -50 > fractal_content.txt
    
    # Search for "brainfeeder" in content
    grep -r "brainfeeder\|BrainFeeder" ~/.aos --include="*.py" 2>/dev/null | head -50 > brainfeeder_content.txt
else
    echo "⚠️  .aos directory not found"
fi

# 5. Search for pattern databases
echo "[5/6] Searching for pattern databases..."
find ~ -type f \( \
    -name "*patterns*.db" -o \
    -name "*fractals*.db" -o \
    -name "*brain*.db" -o \
    -name "*.sqlite" -o \
    -name "*.sqlite3" \
    \) 2>/dev/null | head -20 > database_files.txt

# 6. Extract the actual files
echo "[6/6] Extracting found files..."

# Create extraction manifest
cat > extraction_manifest.json << MANIFEST
{
  "extraction_timestamp": "$(date -Iseconds)",
  "source": "Mortimer VPS",
  "files_found": {
    "brainfeeder": $(wc -l < brainfeeder_files.txt 2>/dev/null || echo 0),
    "brain_py": $(wc -l < brain_files.txt 2>/dev/null || echo 0),
    "fractals": $(wc -l < fractal_files.txt 2>/dev/null || echo 0),
    "databases": $(wc -l < database_files.txt 2>/dev/null || echo 0),
    "aos_files": $(wc -l < aos_files.txt 2>/dev/null || echo 0)
  }
}
MANIFEST

# Create tarball with all found files
echo ""
echo "📦 Creating archive..."

# Copy found files to temp location for archiving
mkdir -p collected_files

# Copy brainfeeder files
while read -r file; do
    if [ -f "$file" ]; then
        cp "$file" collected_files/ 2>/dev/null
        echo "Copied: $file"
    fi
done < brainfeeder_files.txt 2>/dev/null

# Copy brain files
while read -r file; do
    if [ -f "$file" ]; then
        cp "$file" collected_files/ 2>/dev/null
        echo "Copied: $file"
    fi
done < brain_files.txt 2>/dev/null

# Copy fractal files
while read -r file; do
    if [ -f "$file" ]; then
        cp "$file" collected_files/ 2>/dev/null
        echo "Copied: $file"
    fi
done < fractal_files.txt 2>/dev/null

# Copy .aos content if exists
if [ -d ~/.aos ]; then
    cp -r ~/.aos collected_files/aos_backup 2>/dev/null
    echo "Copied: ~/.aos directory"
fi

# Create master tarball
tar -czf mortimer-fractals-and-brainfeeder.tar.gz \
    collected_files/ \
    brainfeeder_files.txt \
    brain_files.txt \
    fractal_files.txt \
    database_files.txt \
    aos_structure.txt \
    aos_files.txt \
    fractal_content.txt \
    brainfeeder_content.txt \
    extraction_manifest.json \
    2>/dev/null

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "✅ EXTRACTION COMPLETE"
echo "═══════════════════════════════════════════════════════════"
echo ""
ls -lh mortimer-fractals-and-brainfeeder.tar.gz
echo ""
echo "📦 Archive contents:"
tar -tzf mortimer-fractals-and-brainfeeder.tar.gz | head -30
echo ""
echo "═══════════════════════════════════════════════════════════"
echo "DOWNLOAD INSTRUCTIONS:"
echo "From Miles VPS, run:"
echo "  scp mortimer@31.97.6.30:/tmp/mortimer-fractals/mortimer-fractals-and-brainfeeder.tar.gz ./"
echo "═══════════════════════════════════════════════════════════"
