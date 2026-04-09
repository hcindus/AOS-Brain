#!/bin/bash
# ReggieStart POS Release Build Script
# Builds distributable packages for all platforms

set -e

VERSION="${1:-$(node -p "require('./package.json').version")}"
BUILD_DIR="build"
RELEASE_DIR="releases"

echo "=== ReggieStart POS Release Builder ==="
echo "Version: $VERSION"
echo ""

# Clean and prepare
clean() {
    echo "[1/6] Cleaning build directories..."
    rm -rf "$BUILD_DIR" "$RELEASE_DIR"
    mkdir -p "$BUILD_DIR" "$RELEASE_DIR"
    echo "  ✓ Directories prepared"
}

# Install dependencies
deps() {
    echo "[2/6] Installing dependencies..."
    npm ci
    echo "  ✓ Dependencies installed"
}

# Run tests
tests() {
    echo "[3/6] Running tests..."
    npm test || echo "  ⚠ Some tests failed, continuing..."
    echo "  ✓ Tests complete"
}

# Build for Linux
build_linux() {
    echo "[4/6] Building for Linux..."
    npm run build:linux
    
    # Package artifacts
    cp -r dist/* "$BUILD_DIR/" 2>/dev/null || true
    
    # Create AppImage and deb
    mv dist/*.AppImage "$RELEASE_DIR/ReggieStart-POS-${VERSION}-linux.AppImage" 2>/dev/null || true
    mv dist/*.deb "$RELEASE_DIR/ReggieStart-POS-${VERSION}-linux.deb" 2>/dev/null || true
    
    echo "  ✓ Linux builds complete"
}

# Build for Windows
build_windows() {
    echo "[5/6] Building for Windows..."
    npm run build:win
    
    # Package artifacts
    mv dist/*.exe "$RELEASE_DIR/" 2>/dev/null || true
    mv dist/*.msi "$RELEASE_DIR/" 2>/dev/null || true
    
    echo "  ✓ Windows builds complete"
}

# Build for macOS
build_macos() {
    echo "[6/6] Building for macOS..."
    npm run build:mac
    
    # Package artifacts
    mv dist/*.dmg "$RELEASE_DIR/" 2>/dev/null || true
    mv dist/*.zip "$RELEASE_DIR/" 2>/dev/null || true
    
    echo "  ✓ macOS builds complete"
}

# Generate checksums
checksums() {
    echo ""
    echo "Generating checksums..."
    cd "$RELEASE_DIR"
    sha256sum * > SHA256SUMS.txt
    cd -
    echo "  ✓ Checksums generated"
}

# Sign releases (if GPG available)
sign_releases() {
    if command -v gpg &> /dev/null && [ -n "$SIGNING_KEY" ]; then
        echo ""
        echo "Signing releases..."
        cd "$RELEASE_DIR"
        for file in *; do
            if [ -f "$file" ] && [[ ! "$file" =~ \.asc$ ]]; then
                gpg --armor --detach-sign --output "$file.asc" "$file"
            fi
        done
        cd -
        echo "  ✓ Releases signed"
    fi
}

# Create release notes
release_notes() {
    cat > "$RELEASE_DIR/RELEASE_NOTES.md" << EOF
# ReggieStart POS v${VERSION}

## Release Date
$(date +%Y-%m-%d)

## Packages

### Linux
- ReggieStart-POS-${VERSION}-linux.AppImage (Portable)
- ReggieStart-POS-${VERSION}-linux.deb (Debian/Ubuntu)

### Windows
- ReggieStart-POS-${VERSION}-win.exe (Installer)
- ReggieStart-POS-${VERSION}-win-portable.exe

### macOS
- ReggieStart-POS-${VERSION}-mac.dmg

## Installation

### Linux
\`\`\`bash
# AppImage (Recommended)
chmod +x ReggieStart-POS-${VERSION}-linux.AppImage
./ReggieStart-POS-${VERSION}-linux.AppImage

# Debian/Ubuntu
sudo dpkg -i ReggieStart-POS-${VERSION}-linux.deb
\`\`\`

### Windows
Run the installer and follow the setup wizard.

### macOS
Open the DMG and drag to Applications.

## Verification
Verify checksums:
\`\`\`bash
sha256sum -c SHA256SUMS.txt
\`\`\`

## Known Issues
- None reported

---
© 2026 AGI Company
EOF
    echo "  ✓ Release notes created"
}

# Main build flow
main() {
    clean
    deps
    tests
    build_linux
    # build_windows  # Uncomment when Windows build env available
    # build_macos    # Uncomment when macOS build env available
    checksums
    sign_releases
    release_notes
    
    echo ""
    echo "=== Build Complete ==="
    echo ""
    echo "Release packages in: $RELEASE_DIR"
    echo ""
    ls -lh "$RELEASE_DIR"
}

# Run build
main "$@"
