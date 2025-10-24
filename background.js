const NATIVE_HOST_NAME = "com.chatgpt.atlas_opener";
const SUPPORTED_PROTOCOLS = new Set(["http:", "https:"]);

async function openInAtlas() {
  const [tab] = await chrome.tabs.query({ active: true, windowId: chrome.windows.WINDOW_ID_CURRENT });
  if (!tab || !tab.url) {
    console.warn("No active tab with a URL to open in ChatGPT Atlas");
    return;
  }

  let tabProtocol;
  try {
    tabProtocol = new URL(tab.url).protocol;
  } catch (error) {
    console.warn("ChatGPT Atlas Opener: unable to parse active tab URL", error);
    return;
  }

  if (!SUPPORTED_PROTOCOLS.has(tabProtocol)) {
    console.warn(`ChatGPT Atlas Opener: unsupported protocol ${tabProtocol}`);
    return;
  }

  try {
    const response = await chrome.runtime.sendNativeMessage(
      NATIVE_HOST_NAME,
      { url: tab.url }
    );
    
    if (response && response.success) {
      console.log("Successfully opened URL in ChatGPT Atlas");
    } else {
      console.error("Failed to open in Atlas:", response?.error || "Unknown error");
    }
  } catch (error) {
    console.error("Native messaging error:", error.message);
    console.error("Make sure the native messaging host is installed correctly.");
  }
}

chrome.action.onClicked.addListener(() => {
  openInAtlas();
});

chrome.commands.onCommand.addListener((command) => {
  if (command === "open-in-atlas") {
    openInAtlas();
  }
});
