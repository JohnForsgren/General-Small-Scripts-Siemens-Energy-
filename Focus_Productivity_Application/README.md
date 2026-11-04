# Focus Productivity Application

Minimal browser focus tool for YouTube.

## What it does

- Hides the YouTube home feed.
- Hides watch-page recommendations.
- Hides end-screen cards and overlay suggestions.
- Keeps settings local to the browser.

## How to use

If extension installation is allowed:

1. Open Chrome extension management.
2. Enable Developer mode.
3. Load this folder as an unpacked extension.
4. Open YouTube and adjust settings from the popup or options page.

If extension installation is blocked by policy:

1. Open [bookmarklet.html](bookmarklet.html) in Chrome.
2. Drag the apply link to your bookmarks bar, or copy the apply code into a bookmark URL.
3. Open YouTube and click the apply bookmarklet to hide the home feed and recommendations.
4. Use the remove bookmarklet if you want to restore the page.

The apply bookmarklet keeps working across YouTube SPA navigation in the same tab, but a full reload still needs one more click.

## Current scope

This is intentionally narrow: YouTube first, with local-only controls and no account, server, or telemetry layer.