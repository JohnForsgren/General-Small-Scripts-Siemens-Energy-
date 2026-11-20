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

## Related ambient-audio workflow (yt-dlp)

- The user reports IT approval for the intended yt-dlp use and has installed the standalone executable under `C:\YT-DLP`.
- An initial single-video MP3 run was made. The handover does not confirm the resulting file, so verify the output before treating the test as complete.
- Current goal: download authorized ambient-sound playlists as MP3 files into `C:\YT-DLP\Downloads`; the documented command and proposed `yt-dlp.conf` settings are in [UPDATE 2 - New solutions](User%20Files/UPDATE%202%20-%20New%20solutions.md).
- Confirm the actual config-file location and that this executable reads it; verify playlist behavior, output location, and FFmpeg availability/conversion.
- Keep this as a separate local CLI workflow. It is not integrated into the browser extension/bookmarklet; local categories, YouTube playlist organization, and optional Drive copies remain manual.
- Security assessment and maintenance notes are in [GPT 6 - Assessment of yt-dlp](User%20Files/GPT%206%20-%20Assessment%20of%20yt-dlp.md). The user reports IT approval; continue using only within that approved scope and periodically update yt-dlp and FFmpeg.

## Notes

- The implementation uses CSS injection from a content script, so YouTube SPA navigation should keep working.
- Selectors may need adjustment if YouTube changes its DOM.
- The watch-page sidebar rule was narrowed to recommendation elements so playlist panels stay visible.
- The layout expansion rule on the primary column was removed because it could collapse the playlist sidebar on watch pages.
- Confirmed behavior: playlist panels remain visible on playlist videos, while the recommendations/related-videos area is hidden.