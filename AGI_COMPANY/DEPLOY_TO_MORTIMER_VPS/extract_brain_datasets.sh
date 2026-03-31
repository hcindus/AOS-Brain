#!/bin/bash
# extract_brain_datasets.sh - Extract Mortimer's brain training data
# Run on Mortimer VPS via Hostinger Browser Terminal

echo "🧠 EXTRACTING MORTIMER'S BRAIN DATASETS"
echo "========================================"

mkdir -p /tmp/mortimer-datasets
cd /tmp/mortimer-datasets

# 1. Find brain data directories
echo "[1/5] Searching for brain training data..."
find ~ -type d \( \
    -name "*brain*" -o \
    -name "*training*" -o \
    -name "*dataset*" -o \
    -name "*data*" -o \
    -name "*knowledge*" -o \
    -name "*memory*" -o \
    -name "*patterns*" \
    \) 2>/dev/null | head -50 > brain_dirs.txt

# 2. Find brain configuration files
echo "[2/5] Extracting brain configurations..."
find ~ -type f \( \
    -name "*brain*.json" -o \
    -name "*brain*.yaml" -o \
    -name "*brain*.py" -o \
    -name "*config*.json" -o \
    -name "*training*.json" -o \
    -name "*weights*.bin" -o \
    -name "*model*.pt" -o \
    -name "*embeddings*.npy" \
    \) 2>/dev/null | grep -v node_modules | head -100 > brain_files.txt

# 3. Find pattern libraries
echo "[3/5] Extracting pattern libraries..."
find ~ -type f \( \
    -name "*pattern*.json" -o \
    -name "*pattern*.txt" -o \
    -name "*logic*.json" -o \
    -name "*rule*.json" -o \
    -name "*behavior*.json" \
    \) 2>/dev/null | head -50 > pattern_files.txt

# 4. Find Memosyne/knowledge bases
echo "[4/5] Extracting knowledge bases..."
find ~ -type f \( \
    -name "*.md" -o \
    -name "*.txt" \
    \) -path "*knowledge*" 2>/dev/null | head -100 > knowledge_files.txt

find ~ -type f \( \
    -name "*.md" -o \
    -name "*.txt" \
    \) -path "*memosyne*" 2>/dev/null | head -100 >> knowledge_files.txt

# 5. Extract specific brain data locations
echo "[5/5] Checking common brain data locations..."

# Check if Mortimer has specific brain directories
for dir in ~/.brain ~/brain /opt/brain /var/lib/brain ~/data/brain ~/training; do
    if [ -d "$dir" ]; then
        echo "$dir" >> brain_dirs.txt
        ls -la "$dir" >> brain_dirs.txt 2>/dev/null
    fi
done

# Create comprehensive archive
echo ""
echo "📦 Creating dataset archive..."

# Create tarball of all found data
tar -czf mortimer-brain-datasets.tar.gz \
    brain_dirs.txt \
    brain_files.txt \
    pattern_files.txt \
    knowledge_files.txt \
    $(cat brain_dirs.txt 2>/dev/null | head -20) \
    $(cat brain_files.txt 2>/dev/null | head -50) \
    $(cat pattern_files.txt 2>/dev/null | head -20) \
    $(cat knowledge_files.txt 2>/dev/null | head -50) \
    2>/dev/null

# Also create a simple data manifest
cat > dataset_manifest.json << 'EOF'
{
  "source": "Mortimer VPS",
  "extraction_date": "$(date -Iseconds)",
  "datasets_found": {
    "brain_directories": $(wc -l < brain_dirs.txt 2>/dev/null || echo 0),
    "brain_files": $(wc -l < brain_files.txt 2>/dev/null || echo 0),
    "pattern_files": $(wc -l < pattern_files.txt 2>/dev/null || echo 0),
    "knowledge_files": $(wc -l < knowledge_files.txt 2>/dev/null || echo 0)
  },
  "archive": "mortimer-brain-datasets.tar.gz"
}
EOF

echo ""
echo "========================================"
echo "✅ EXTRACTION COMPLETE"
echo "========================================"
echo ""
echo "Files:"
ls -lh /tmp/mortimer-datasets/
echo ""
echo "Summary:"
echo "  Brain dirs: $(wc -l < brain_dirs.txt 2>/dev/null || echo 0)"
echo "  Brain files: $(wc -l < brain_files.txt 2>/dev/null || echo 0)"
echo "  Patterns: $(wc -l < pattern_files.txt 2>/dev/null || echo 0)"
echo "  Knowledge: $(wc -l < knowledge_files.txt 2>/dev/null || echo 0)"
echo ""
echo "Download: /tmp/mortimer-datasets/mortimer-brain-datasets.tar.gz"
echo "========================================"
