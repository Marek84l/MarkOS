	#!/usr/bin/env bash

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ISO_DIR="$PROJECT_DIR/iso"
BUILDER_IMAGE="marekos-builder"

RAW_ISO="$ISO_DIR/MarkOS-0.1-amd64.hybrid.iso"
FINAL_ISO="$ISO_DIR/MarkOS-0.1-amd64.iso"

echo "======================================"
echo "            MarkOS Builder"
echo "======================================"
echo
echo "Project: $PROJECT_DIR"
echo "ISO dir: $ISO_DIR"
echo
echo "Starting MarkOS build..."
echo

sudo podman run --rm --privileged \
    -v "$ISO_DIR:/workspace" \
    -w /workspace \
    "$BUILDER_IMAGE" \
    lb build

if [ -f "$RAW_ISO" ]; then
    mv -f "$RAW_ISO" "$FINAL_ISO"

    echo
    echo "======================================"
    echo "      MarkOS build completed"
    echo "======================================"
    echo
    echo "Output:"
    echo "$FINAL_ISO"
    echo
else
    echo
    echo "ERROR: Expected ISO was not created:"
    echo "$RAW_ISO"
    exit 1
fi
