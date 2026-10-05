#!/usr/bin/env bash

set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ISO_DIR="$PROJECT_DIR/iso"
BUILDER_IMAGE="markos-builder"

RAW_ISO="$ISO_DIR/MarkOS-0.1-amd64.hybrid.iso"
FINAL_ISO="$ISO_DIR/MarkOS-0.1-amd64.iso"

run_live_build() {
    sudo podman run --rm --privileged \
        -v "$ISO_DIR:/workspace" \
        -w /workspace \
        "$BUILDER_IMAGE" \
        "$@"
}

echo "======================================"
echo "            MarkOS Builder"
echo "======================================"
echo
echo "Project: $PROJECT_DIR"
echo "ISO dir: $ISO_DIR"
echo

echo "[1/3] Cleaning previous build..."
run_live_build lb clean --purge

rm -f "$RAW_ISO" "$FINAL_ISO"

echo
echo "[2/3] Configuring MarkOS..."
run_live_build lb config

echo
echo "[3/3] Building MarkOS..."
run_live_build lb build

if [ ! -f "$RAW_ISO" ]; then
    echo
    echo "ERROR: Expected ISO was not created:"
    echo "$RAW_ISO"
    exit 1
fi

mv "$RAW_ISO" "$FINAL_ISO"

echo
echo "======================================"
echo "      MarkOS build completed"
echo "======================================"
echo
echo "Output:"
echo "$FINAL_ISO"
echo
