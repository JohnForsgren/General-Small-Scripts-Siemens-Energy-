const STORAGE_KEY = "focusProductivitySettings";

const DEFAULT_SETTINGS = {
  enabled: true,
  hideHomeFeed: true,
  hideWatchSidebar: true,
  hideEndScreenCards: true,
  hideShortsShelf: false,
  hideComments: false,
};

const ids = Object.keys(DEFAULT_SETTINGS);

async function loadSettings() {
  const stored = await chrome.storage.local.get(STORAGE_KEY);
  return { ...DEFAULT_SETTINGS, ...(stored[STORAGE_KEY] || {}) };
}

function readForm() {
  return Object.fromEntries(ids.map((id) => [id, document.getElementById(id).checked]));
}

function writeForm(settings) {
  ids.forEach((id) => {
    document.getElementById(id).checked = Boolean(settings[id]);
  });
}

async function saveSettings(settings) {
  await chrome.storage.local.set({ [STORAGE_KEY]: settings });
}

async function init() {
  writeForm(await loadSettings());

  document.getElementById("save").addEventListener("click", async () => {
    await saveSettings(readForm());
  });

  document.getElementById("reset").addEventListener("click", async () => {
    writeForm(DEFAULT_SETTINGS);
    await saveSettings(DEFAULT_SETTINGS);
  });
}

init().catch(() => {});