const STORAGE_KEY = "focusProductivitySettings";

const DEFAULT_SETTINGS = {
  enabled: true,
  hideHomeFeed: true,
  hideWatchSidebar: true,
  hideEndScreenCards: true,
  hideShortsShelf: false,
  hideComments: false,
};

async function getSettings() {
  const stored = await chrome.storage.local.get(STORAGE_KEY);
  return { ...DEFAULT_SETTINGS, ...(stored[STORAGE_KEY] || {}) };
}

async function saveSettings(settings) {
  await chrome.storage.local.set({ [STORAGE_KEY]: settings });
}

async function render() {
  const enabledInput = document.getElementById("enabled");
  const settings = await getSettings();
  enabledInput.checked = settings.enabled;

  enabledInput.addEventListener("change", async () => {
    await saveSettings({ ...settings, enabled: enabledInput.checked });
  });

  document.getElementById("openOptions").addEventListener("click", () => {
    chrome.runtime.openOptionsPage();
  });

  document.getElementById("reset").addEventListener("click", async () => {
    await saveSettings(DEFAULT_SETTINGS);
    enabledInput.checked = true;
  });
}

render().catch(() => {});