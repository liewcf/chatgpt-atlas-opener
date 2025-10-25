# Release Notes Template

Copy this template when creating a GitHub release.

---

## ChatGPT Atlas Opener v1.0.0

Open any webpage directly in the ChatGPT Atlas macOS app with one click or keyboard shortcut.

### Installation

1. Download `chatgpt-atlas-opener-v1.0.0.zip`
2. Unzip the file
3. Open Chrome and go to `chrome://extensions/`
4. Enable "Developer mode" (toggle in top-right corner)
5. Click "Load unpacked" and select the unzipped folder
6. Note your Extension ID (looks like: `abcdefghijklmnopqrstuvwxyz123456`)
7. Open Terminal and navigate to the extension folder
8. Run: `./install.sh` and enter your Extension ID when prompted
9. Reload the extension in Chrome

### Usage

- Click the extension icon in your toolbar
- Or use keyboard shortcut: `Cmd+Shift+A` (macOS)

### Requirements

- macOS (ChatGPT Atlas is macOS-only)
- ChatGPT Atlas app installed
- Python 3
- Google Chrome

### What's Changed

- Initial release with core functionality
- Fixed ChatGPT Atlas bundle ID for proper app launching

### Assets

- `chatgpt-atlas-opener-v1.0.0.zip` - Complete extension package with native host
