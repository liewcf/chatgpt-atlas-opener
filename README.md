# ChatGPT Atlas Opener

> Open any webpage in ChatGPT Atlas with a single click or keyboard shortcut.

A Chrome extension for macOS that seamlessly opens the current webpage in the [ChatGPT Atlas](https://chatgpt.com/atlas) browser app.

## Features

- 🚀 One-click opening of current page in ChatGPT Atlas
- ⌨️ Keyboard shortcut: `⌘ Command + ⇧ Shift + A`
- 🔒 Privacy-focused: No data collection, no external requests
- ⚡ Fast and lightweight

## Requirements

- **macOS 14+** with Apple Silicon (M1 or better)
- **ChatGPT Atlas** installed in Applications folder ([Download](https://persistent.oaistatic.com/atlas/public/ChatGPT_Atlas.dmg))
- **Google Chrome** or Chromium-based browser
- **Python 3** (pre-installed on macOS)

## Installation

### 1. Clone or Download

```bash
git clone https://github.com/liewcf/chatgpt-atlas-opener.git
cd chatgpt-atlas-opener
```

Or download and extract the ZIP from GitHub releases.

### 2. Load the Chrome Extension

1. Open Chrome and navigate to `chrome://extensions/`
2. Enable **Developer mode** (toggle in the top right)
3. Click **Load unpacked**
4. Select the `chatgpt-atlas-opener` folder
5. **Copy the Extension ID** shown under the extension name (you'll need this next)

### 3. Install Native Messaging Host

The extension uses a native messaging host to communicate with macOS.

Run the installation script:

```bash
./install.sh
```

When prompted, paste the Extension ID you copied in step 2.

### 4. Test It Out

1. Navigate to any webpage (e.g., https://www.github.com)
2. Click the extension icon or press `⌘ Command + ⇧ Shift + A`
3. The page should open in ChatGPT Atlas! 🎉

## How It Works

This extension uses **native messaging** to communicate with macOS:

1. Chrome extension captures the current tab's URL
2. Extension sends URL to native messaging host (Python script)
3. Native host uses macOS's `open` command to launch URL in ChatGPT Atlas
4. This bypasses Chrome's restrictions on custom URL schemes

## Troubleshooting

### "Native messaging error" message

**Solution:** Make sure you ran `install.sh` with the correct Extension ID.

Verify the native host is installed:
```bash
cat ~/Library/Application\ Support/Google/Chrome/NativeMessagingHosts/com.chatgpt.atlas_opener.json
```

Check that the `allowed_origins` Extension ID matches your actual extension ID from `chrome://extensions/`.

### Atlas doesn't open

**Solution:** Verify ChatGPT Atlas is installed correctly.

Test the command manually:
```bash
open -a "ChatGPT Atlas" "https://www.example.com"
```

If this fails, make sure Atlas is in your `/Applications` folder.

### View extension logs

1. Go to `chrome://extensions/`
2. Click **Details** on ChatGPT Atlas Opener
3. Click **Inspect views: service worker**
4. Check the Console tab for error messages

## Uninstallation

### Remove the extension

1. Go to `chrome://extensions/`
2. Click **Remove** on ChatGPT Atlas Opener

### Remove native messaging host

```bash
rm ~/Library/Application\ Support/Google/Chrome/NativeMessagingHosts/com.chatgpt.atlas_opener.json
```

## Project Structure

```
chatgpt-atlas-opener/
├── manifest.json              # Chrome extension configuration
├── background.js              # Service worker (native messaging client)
├── options.html               # Extension info page
├── options.css                # Styling for options page
├── native-host/
│   ├── atlas_opener.py        # Native messaging host (Python)
│   └── com.chatgpt.atlas_opener.json  # Host manifest template
├── install.sh                 # Installation script
├── LICENSE                    # MIT License
└── README.md                  # This file
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Disclaimer

This is an unofficial, community-created extension. It is not affiliated with, endorsed by, or connected to OpenAI or ChatGPT Atlas.
