#!/bin/bash

# Installation script for ChatGPT Atlas Opener native messaging host

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
NATIVE_HOST_DIR="$SCRIPT_DIR/native-host"
HOST_MANIFEST="$NATIVE_HOST_DIR/com.chatgpt.atlas_opener.json"
CHROME_NATIVE_MESSAGING_DIR="$HOME/Library/Application Support/Google/Chrome/NativeMessagingHosts"

echo "ChatGPT Atlas Opener - Native Messaging Host Installation"
echo "=========================================================="
echo ""

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not found."
    echo "Please install Python 3 and try again."
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"
echo ""

# Get extension ID from user
echo "To complete the installation, you need your Chrome extension ID."
echo ""
echo "How to find your extension ID:"
echo "1. Open Chrome and go to chrome://extensions/"
echo "2. Enable 'Developer mode' (toggle in top right)"
echo "3. Find 'ChatGPT Atlas Opener' in the list"
echo "4. Copy the Extension ID (it looks like: abcdefghijklmnopqrstuvwxyz123456)"
echo ""
read -p "Enter your extension ID: " EXTENSION_ID

if [ -z "$EXTENSION_ID" ]; then
    echo "Error: Extension ID cannot be empty"
    exit 1
fi

echo ""
echo "Using Extension ID: $EXTENSION_ID"
echo ""

# Create Chrome native messaging directory if it doesn't exist
mkdir -p "$CHROME_NATIVE_MESSAGING_DIR"

# Create a temporary manifest with the correct extension ID and path
TEMP_MANIFEST=$(mktemp)
PYTHON_SCRIPT_PATH="$NATIVE_HOST_DIR/atlas_opener.py"

# Replace both the extension ID and the path
sed -e "s|EXTENSION_ID_PLACEHOLDER|$EXTENSION_ID|g" \
    -e "s|PATH_PLACEHOLDER|$PYTHON_SCRIPT_PATH|g" \
    "$HOST_MANIFEST" > "$TEMP_MANIFEST"

# Copy the manifest to Chrome's native messaging directory
cp "$TEMP_MANIFEST" "$CHROME_NATIVE_MESSAGING_DIR/com.chatgpt.atlas_opener.json"
rm "$TEMP_MANIFEST"

echo "✓ Native messaging host manifest installed to:"
echo "  $CHROME_NATIVE_MESSAGING_DIR/com.chatgpt.atlas_opener.json"
echo ""

# Make the Python script executable
chmod +x "$NATIVE_HOST_DIR/atlas_opener.py"
echo "✓ Native host script made executable"
echo ""

echo "=========================================================="
echo "Installation complete!"
echo ""
echo "Next steps:"
echo "1. Reload the Chrome extension at chrome://extensions/"
echo "2. Test the extension by clicking its icon or using Cmd+Shift+A"
echo ""
echo "If you encounter issues, check the Chrome extension console for error messages."
