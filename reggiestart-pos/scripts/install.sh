#!/bin/bash
# ReggieStart POS Installation Script
# Installs and configures the POS system

set -e

REPO_URL="https://github.com/agi-company/reggiestart-pos"
INSTALL_DIR="${1:-$HOME/.reggiestart}"
NODE_VERSION="20"

echo "=== ReggieStart POS Installer ==="
echo "Install directory: $INSTALL_DIR"
echo ""

# Check dependencies
check_dependencies() {
    echo "[1/6] Checking dependencies..."
    
    if ! command -v git &> /dev/null; then
        echo "Error: git is required but not installed"
        exit 1
    fi
    
    if ! command -v node &> /dev/null; then
        echo "Node.js not found. Installing..."
        if command -v apt-get &> /dev/null; then
            curl -fsSL https://deb.nodesource.com/setup_${NODE_VERSION}.x | sudo -E bash -
            sudo apt-get install -y nodejs
        elif command -v yum &> /dev/null; then
            curl -fsSL https://rpm.nodesource.com/setup_${NODE_VERSION}.x | sudo bash -
            sudo yum install -y nodejs
        else
            echo "Error: Cannot install Node.js automatically. Please install manually."
            exit 1
        fi
    fi
    
    echo "  ✓ Dependencies OK"
}

# Create installation directory
create_directory() {
    echo "[2/6] Creating installation directory..."
    
    if [ -d "$INSTALL_DIR" ]; then
        echo "  Directory exists, updating..."
        rm -rf "$INSTALL_DIR"
    fi
    
    mkdir -p "$INSTALL_DIR"
    echo "  ✓ Directory created: $INSTALL_DIR"
}

# Clone or copy repository
install_source() {
    echo "[3/6] Installing source code..."
    
    if [ -d ".git" ]; then
        # Running from repo
        cp -r . "$INSTALL_DIR/"
    else
        # Download from GitHub
        git clone "$REPO_URL" "$INSTALL_DIR"
    fi
    
    echo "  ✓ Source installed"
}

# Install Node dependencies
install_deps() {
    echo "[4/6] Installing dependencies..."
    cd "$INSTALL_DIR"
    npm install
    echo "  ✓ Dependencies installed"
}

# Build application
build_app() {
    echo "[5/6] Building application..."
    cd "$INSTALL_DIR"
    npm run build:linux
    echo "  ✓ Build complete"
}

# Create launcher
create_launcher() {
    echo "[6/6] Creating launcher..."
    
    LAUNCHER_PATH="$HOME/.local/share/applications/reggiestart.desktop"
    mkdir -p "$(dirname $LAUNCHER_PATH)"
    
    cat > "$LAUNCHER_PATH" << EOF
[Desktop Entry]
Name=ReggieStart POS
Comment=Point of Sale System
Exec=$INSTALL_DIR/dist/ReggieStart POS
Icon=$INSTALL_DIR/assets/icons/icon.png
Type=Application
Categories=Office;Finance;
Terminal=false
EOF
    
    chmod +x "$LAUNCHER_PATH"
    
    # Create symlink in bin
    mkdir -p "$HOME/.local/bin"
    ln -sf "$INSTALL_DIR/dist/ReggieStart POS" "$HOME/.local/bin/reggiestart"
    
    echo "  ✓ Launcher created"
}

# Print completion message
print_completion() {
    echo ""
    echo "=== Installation Complete ==="
    echo ""
    echo "ReggieStart POS has been installed to:"
    echo "  $INSTALL_DIR"
    echo ""
    echo "To launch:"
    echo "  - GUI: Look for 'ReggieStart POS' in applications menu"
    echo "  - Terminal: reggiestart"
    echo ""
    echo "To uninstall:"
    echo "  rm -rf $INSTALL_DIR"
    echo "  rm $HOME/.local/share/applications/reggiestart.desktop"
    echo ""
}

# Main installation flow
main() {
    check_dependencies
    create_directory
    install_source
    install_deps
    build_app
    create_launcher
    print_completion
}

# Run installation
main "$@"
