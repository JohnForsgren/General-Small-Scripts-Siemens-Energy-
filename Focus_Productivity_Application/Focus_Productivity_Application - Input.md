

So my company  is preventing chrome extensions and installing programs from untrusted sources. But I have got a legal workaround for the untrusted sources: For productivity apps like promodoro timers and todo-list, i have vibe coded my own apps which is allowed. But now i would also like to reduce distraction by setting up an own productivity manager for the web browser. Notably: 


- For youtube: 
-- Hide front page, I.e make it so that only the search bar appears  
-- Hide recommended video feed 
Worked for 42s

Yes—this is feasible. The most reliable design is a small, company-approved Manifest V3 extension that only modifies YouTube. A normal standalone web app cannot modify another site’s tab because browsers isolate different origins.

Do not disable or work around the company’s Chrome policies. Chrome administrators can allowlist a particular extension or distribute an internal extension through the organisation’s private Chrome Web Store.

Option 1: Proper internal extension

Create a folder named:

focus-browser/
├── manifest.json
└── youtube-focus.css
manifest.json
{
  "manifest_version": 3,
  "name": "Focus Browser",
  "version": "1.0.0",
  "description": "Removes distracting elements from selected websites.",
  "content_scripts": [
    {
      "matches": [
        "https://www.youtube.com/*"
      ],
      "css": [
        "youtube-focus.css"
      ],
      "run_at": "document_start"
    }
  ]
}
youtube-focus.css
/* =========================================================
   YOUTUBE HOME PAGE
   Keep the top navigation and search bar, but remove the feed.
   ========================================================= */

ytd-browse[page-subtype="home"] #primary,
ytd-browse[page-subtype="home"] ytd-rich-grid-renderer,
ytd-browse[page-subtype="home"] #chips-wrapper {
    display: none !important;
}

/* Make an otherwise empty homepage look intentional. */

ytd-browse[page-subtype="home"]::after {
    content: "Search for something intentionally.";
    display: block;

    margin: 140px auto 0;
    width: fit-content;

    font-family: Roboto, Arial, sans-serif;
    font-size: 22px;
    font-weight: 400;

    color: var(--yt-spec-text-secondary);
}


/* =========================================================
   VIDEO PAGES
   Remove the recommended-video column beside the video.
   ========================================================= */

ytd-watch-flexy #secondary,
ytd-watch-next-secondary-results-renderer {
    display: none !important;
}


/* Let the main video area use the available width. */

ytd-watch-flexy:not([theater]) #primary {
    max-width: none !important;
}


/* =========================================================
   RECOMMENDATIONS INSIDE THE PLAYER
   Remove end-screen cards and floating recommendations.
   ========================================================= */

.ytp-endscreen-content,
.ytp-ce-element,
.ytp-pause-overlay {
    display: none !important;
}


/* =========================================================
   OPTIONAL: RECOMMENDED VIDEOS BELOW THE PLAYER
   Used by YouTube in narrow-window layouts.
   ========================================================= */

ytd-watch-flexy ytd-item-section-renderer
    ytd-compact-video-renderer {
    display: none !important;
}

Content scripts and their styles are specifically intended to read or modify the DOM of matching webpages.

This extension would:

Leave YouTube’s header and search field visible.
Hide the entire front-page recommendation feed.
Hide the recommended-video sidebar on video pages.
Hide recommendation cards appearing over the player.
Continue working when navigating between YouTube pages.
Require access only to youtube.com, not every website.

YouTube occasionally changes its internal element names, so individual selectors may eventually need updating.

Option 2: Prototype without installing an extension

You can test the behaviour using a bookmarklet, provided company policy permits user-authored browser scripts.

Create a bookmark and paste the following into its URL field:

javascript:(()=>{const id="focus-browser-youtube";const existing=document.getElementById(id);if(existing){existing.remove();return;}const style=document.createElement("style");style.id=id;style.textContent=`ytd-browse[page-subtype="home"] #primary,ytd-browse[page-subtype="home"] ytd-rich-grid-renderer,ytd-browse[page-subtype="home"] #chips-wrapper,ytd-watch-flexy #secondary,ytd-watch-next-secondary-results-renderer,.ytp-endscreen-content,.ytp-ce-element,.ytp-pause-overlay{display:none!important}ytd-browse[page-subtype="home"]::after{content:"Search for something intentionally.";display:block;margin:140px auto 0;width:fit-content;font-family:Roboto,Arial,sans-serif;font-size:22px;color:var(--yt-spec-text-secondary)}ytd-watch-flexy:not([theater]) #primary{max-width:none!important}`;document.documentElement.appendChild(style)})();

Name it something like Toggle YouTube Focus.

Clicking it:

Activates focus mode on YouTube.
Clicking it again restores the hidden elements.
Usually survives YouTube’s internal page navigation.
Does not survive a complete reload or newly opened YouTube tab.

That last limitation is why an approved extension is the proper long-term implementation.

Recommended larger productivity-manager structure

Your eventual extension could remain very restricted and modular:

focus-browser/
├── manifest.json
├── sites/
│   ├── youtube.css
│   ├── reddit.css
│   ├── linkedin.css
│   └── news-sites.css
├── options/
│   ├── options.html
│   ├── options.css
│   └── options.js
└── icons/

Useful future settings could include:

Hide YouTube home feed.
Hide YouTube recommendations.
Hide comments separately.
Hide Shorts everywhere.
Remove notification counters.
Hide Reddit’s popular feed.
Hide LinkedIn’s news and suggested posts.
Activate selected rules only during working hours.
Temporarily unlock a hidden feature for 10 minutes.

Settings could be stored locally with Chrome’s extension storage, without accounts, servers, telemetry, or access to browsing history