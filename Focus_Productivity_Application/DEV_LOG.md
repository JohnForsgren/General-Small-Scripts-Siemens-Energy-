# Dev Log

## Current state

- Initial implementation scaffolded as a Manifest V3 extension.
- YouTube focus mode is active by default and can be toggled from the popup.
- Options page exposes local-only rules for feed, sidebar, end-screen cards, Shorts shelves, and comments.
- Extension loading is blocked by policy in this environment, so a bookmarklet fallback was added.
- Bookmarklet launcher lives in `bookmarklet.html` and copies a toggle script for YouTube focus mode.
- The bookmarklet injects a style tag into the current page, so it lasts for the current tab/document only.
- It is removed by a full page reload, closing the tab, or restarting the browser.
- You usually need to click it again after a reload or browser restart.
- The bookmarklet was simplified to separate apply/remove actions and no longer uses MutationObserver or history monkey-patching.

## Notes

- The implementation uses CSS injection from a content script, so YouTube SPA navigation should keep working.
- Selectors may need adjustment if YouTube changes its DOM.
- The watch-page sidebar rule was narrowed to recommendation elements so playlist panels stay visible.
- The layout expansion rule on the primary column was removed because it could collapse the playlist sidebar on watch pages.
- Confirmed behavior: playlist panels remain visible on playlist videos, while the recommendations/related-videos area is hidden.