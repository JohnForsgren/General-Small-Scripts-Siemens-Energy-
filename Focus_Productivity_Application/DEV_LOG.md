# Dev Log

## Current direction: ambient audio

- The intended solution is to download ambient audio with yt-dlp and listen to the files locally—not to stream or listen to ambient audio on YouTube.
- YouTube may still be used to discover recordings and manage the matching playlists. The user may organize downloaded files locally too, with optional copies to Google Drive.
- yt-dlp is installed at `C:\YT-DLP`; the user reports IT approval for this intended use.
- The version-controlled portable configuration is [yt-dlp.conf](yt-dlp.conf); it matches the live config at `C:\YT-DLP\yt-dlp.conf`. Keep this backup current so the setup can be restored from GitHub.
- To restore on another Windows laptop, place `yt-dlp.exe`, `ffmpeg.exe`, `ffprobe.exe`, `deno.exe`, and a copy of [yt-dlp.conf](yt-dlp.conf) together in `C:\YT-DLP`. The config is loaded from the executable's directory. It saves MP3s under `C:\YT-DLP\AMBIENT_SOUNDS`; edit `--paths` if choosing another location. Use official sources and follow IT approval requirements; do not commit executables or downloaded audio to this repo.
- Current settings: MP3 extraction, JPG thumbnail conversion and embedding, full-playlist downloads, continue past unavailable items, and filename format `%(title)s [%(id)s].%(ext)s`. They are also summarized in [UPDATE 2 - New solutions](User%20Files/UPDATE%202%20-%20New%20solutions.md).
- At the time the config was changed, the active playlist download retained its explicit `C:\YT-DLP\Downloads` destination; config changes apply to later runs, and a command-line `-P` destination overrides the config.
- Verified on 2026-11-24: a single-video test used the configured `C:\YT-DLP\AMBIENT_SOUNDS` destination, converted the source to MP3, converted its thumbnail to JPG, and logged FFmpeg embedding it as cover art. The user confirmed the result worked. Playlist completion remains unconfirmed.
- Config changes affect future downloads only; existing MP3s are not changed. For a test download of a previously downloaded video, use a distinct output template to avoid overwriting the existing MP3.
- Keep yt-dlp within the approved scope. Security and maintenance notes are in [GPT 6 - Assessment of yt-dlp](User%20Files/GPT%206%20-%20Assessment%20of%20yt-dlp.md).

## Separate browser-extension experiment

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