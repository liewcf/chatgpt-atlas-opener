#!/bin/bash

# Package ChatGPT Atlas Opener for GitHub release

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# Get version from manifest.json
VERSION=$(python3 -c "import json; print(json.load(open('manifest.json'))['version'])")
PACKAGE_NAME="chatgpt-atlas-opener-v${VERSION}.zip"

echo "Packaging ChatGPT Atlas Opener v${VERSION}"
echo "=========================================="
echo ""

# Remove existing package if it exists
if [ -f "$PACKAGE_NAME" ]; then
    rm "$PACKAGE_NAME"
    echo "Removed existing $PACKAGE_NAME"
fi

# Create the zip file with all necessary files
zip -r "$PACKAGE_NAME" \
    manifest.json \
    background.js \
    options.html \
    options.css \
    icons/ \
    native-host/ \
    install.sh \
    README.md \
    LICENSE \
    -x "*.DS_Store" "native-host/.DS_Store"

echo ""
echo "✓ Package created: $PACKAGE_NAME"
echo ""
echo "File contents:"
unzip -l "$PACKAGE_NAME"
echo ""
echo "=========================================="
echo "Ready for GitHub release!"
echo ""
echo "Next steps:"
echo "1. Commit your changes: git add . && git commit -m 'Fix bundle ID for ChatGPT Atlas'"
echo "2. Create a tag: git tag v${VERSION}"
echo "3. Push with tags: git push origin main --tags"
echo "4. Create GitHub release and upload: $PACKAGE_NAME"
