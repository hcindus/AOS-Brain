#!/bin/bash
# Build script for AOS Cortex Rust extension

cd "$(dirname "$0")"

echo "Building AOS Cortex Rust extension..."

# Check for Rust
if ! command -v rustc &> /dev/null; then
    echo "Error: Rust not found. Install with: curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh"
    exit 1
fi

# Install maturin if not present
if ! command -v maturin &> /dev/null; then
    echo "Installing maturin..."
    pip install maturin
fi

# Build with optimizations
echo "Building release extension..."
RUSTFLAGS="-C target-cpu=native" maturin build --release

# Install
echo "Installing..."
pip install target/wheels/*.whl --force-reinstall

echo "Build complete!"