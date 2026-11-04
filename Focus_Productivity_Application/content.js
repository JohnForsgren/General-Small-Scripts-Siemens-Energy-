const STORAGE_KEY = "focusProductivitySettings";

const DEFAULT_SETTINGS = {
  enabled: true,
  hideHomeFeed: true,
  hideWatchSidebar: true,
  hideEndScreenCards: true,
  hideShortsShelf: false,
  hideComments: false,
};

const STYLE_ID = "focus-productivity-manager-style";

function buildCss(settings) {
  if (!settings.enabled) {
    return "";
  }

  const rules = [];

  if (settings.hideHomeFeed) {
    rules.push(
      'ytd-browse[page-subtype="home"] #primary',
      'ytd-browse[page-subtype="home"] ytd-rich-grid-renderer',
      'ytd-browse[page-subtype="home"] #chips-wrapper'
    );
    rules.push(
      'ytd-browse[page-subtype="home"]::after { content: "Focus mode enabled. Use search to start intentionally."; display: block; margin: 140px auto 0; width: fit-content; font-family: Roboto, Arial, sans-serif; font-size: 22px; color: var(--yt-spec-text-secondary); }'
    );
  }

  if (settings.hideWatchSidebar) {
    rules.push('ytd-watch-next-secondary-results-renderer');
  }

  if (settings.hideEndScreenCards) {
    rules.push('.ytp-endscreen-content', '.ytp-ce-element', '.ytp-pause-overlay');
  }

  if (settings.hideShortsShelf) {
    rules.push('ytd-rich-shelf-renderer[is-shorts]');
    rules.push('ytd-reel-shelf-renderer');
  }

  if (settings.hideComments) {
    rules.push('ytd-comments', 'ytd-engagement-panel-section-list-renderer[target-id="comments-section"]');
  }

  const selectorBlocks = [];
  const groupedSelectors = rules.filter((rule) => !rule.includes('{'));
  if (groupedSelectors.length > 0) {
    selectorBlocks.push(`${groupedSelectors.join(",\n")} { display: none !important; }`);
  }

  selectorBlocks.push(...rules.filter((rule) => rule.includes('{')));

  return selectorBlocks.join("\n\n");
}

async function getSettings() {
  const stored = await chrome.storage.local.get(STORAGE_KEY);
  return { ...DEFAULT_SETTINGS, ...(stored[STORAGE_KEY] || {}) };
}

function applyCss(cssText) {
  let style = document.getElementById(STYLE_ID);

  if (!cssText) {
    if (style) {
      style.remove();
    }
    return;
  }

  if (!style) {
    style = document.createElement("style");
    style.id = STYLE_ID;
    document.documentElement.appendChild(style);
  }

  style.textContent = cssText;
}

async function refresh() {
  const settings = await getSettings();
  applyCss(buildCss(settings));
}

chrome.storage.onChanged.addListener((changes, areaName) => {
  if (areaName !== "local" || !changes[STORAGE_KEY]) {
    return;
  }

  applyCss(buildCss({ ...DEFAULT_SETTINGS, ...(changes[STORAGE_KEY].newValue || {}) }));
});

refresh().catch(() => {
  applyCss("");
});