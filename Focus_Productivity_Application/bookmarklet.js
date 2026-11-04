const STYLE_ID = "focus-productivity-bookmarklet-style";

const CSS_TEXT = [
  'ytd-browse[page-subtype="home"] #primary',
  'ytd-browse[page-subtype="home"] ytd-rich-grid-renderer',
  'ytd-browse[page-subtype="home"] #chips-wrapper',
  'ytd-watch-next-secondary-results-renderer',
  '.ytp-endscreen-content',
  '.ytp-ce-element',
  '.ytp-pause-overlay',
  'ytd-watch-flexy ytd-item-section-renderer ytd-compact-video-renderer'
].join(',\n') + ' { display: none !important; }\n\n' + [
  'ytd-browse[page-subtype="home"]::after { content: "Focus mode enabled. Use search to start intentionally."; display: block; margin: 140px auto 0; width: fit-content; font-family: Roboto, Arial, sans-serif; font-size: 22px; color: var(--yt-spec-text-secondary); }',
].join('\n\n');

const APPLY_BOOKMARKLET = `javascript:(()=>{const styleId=${JSON.stringify(STYLE_ID)};const cssText=${JSON.stringify(CSS_TEXT)};const apply=()=>{let style=document.getElementById(styleId);if(!style){style=document.createElement("style");style.id=styleId;document.documentElement.appendChild(style);}style.textContent=cssText;};const cleanup=window.__focusProductivityBookmarkletCleanup;if(typeof cleanup==="function"){cleanup();}const onNavigate=()=>apply();window.__focusProductivityBookmarkletCleanup=()=>{window.removeEventListener("yt-navigate-finish",onNavigate);window.removeEventListener("popstate",onNavigate);const style=document.getElementById(styleId);if(style){style.remove();}delete window.__focusProductivityBookmarkletCleanup;};apply();window.addEventListener("yt-navigate-finish",onNavigate);window.addEventListener("popstate",onNavigate);})();`;

const REMOVE_BOOKMARKLET = `javascript:(()=>{const styleId=${JSON.stringify(STYLE_ID)};const cleanup=window.__focusProductivityBookmarkletCleanup;if(typeof cleanup==="function"){cleanup();return;}const style=document.getElementById(styleId);if(style){style.remove();}})();`;

function init() {
  const applyCode = document.getElementById("applyCode");
  const removeCode = document.getElementById("removeCode");
  const applyLink = document.getElementById("applyLink");
  const removeLink = document.getElementById("removeLink");
  const copyButton = document.getElementById("copy");
  const copyRemoveButton = document.getElementById("copyRemove");

  applyCode.value = APPLY_BOOKMARKLET;
  removeCode.value = REMOVE_BOOKMARKLET;
  applyLink.href = APPLY_BOOKMARKLET;
  removeLink.href = REMOVE_BOOKMARKLET;

  copyButton.addEventListener("click", async () => {
    await navigator.clipboard.writeText(APPLY_BOOKMARKLET);
    copyButton.textContent = "Copied";
    window.setTimeout(() => {
      copyButton.textContent = "Copy code";
    }, 1200);
  });

  copyRemoveButton.addEventListener("click", async () => {
    await navigator.clipboard.writeText(REMOVE_BOOKMARKLET);
    copyRemoveButton.textContent = "Copied";
    window.setTimeout(() => {
      copyRemoveButton.textContent = "Copy code";
    }, 1200);
  });
}

init();