#!/usr/bin/env bash

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ISO_DIR="$PROJECT_DIR/iso"
BUILDER_IMAGE="marekos-builder"

echo "======================================"
echo "          MarekOS Builder"
echo "======================================"
echo
echo "Project: $PROJECT_DIR"
echo "ISO dir: $ISO_DIR"
echo
echo "Starting MarekOS build..."
echo

sudo podman run --rm --privileged \
    -v "$ISO_DIR:/workspace" \
    -w /workspace \
    "$BUILDER_IMAGE" \
    lb build
