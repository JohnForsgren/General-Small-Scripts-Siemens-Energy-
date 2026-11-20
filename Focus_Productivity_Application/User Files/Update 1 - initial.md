# Reducing YouTube Doomscrolling on My Work Computer

*Decision notes — 4 November 2026*

## Problem description

While working from home, I have developed a recurring habit: when I get stuck on a task, I automatically open YouTube and start scrolling through the homepage recommendations. This was not previously a major problem, but it has become more frequent on my work computer. Chrome Extensions are Disabled, and efforts to create a working solution has NOT Worked: It is confirmed that thet current solution wherein i have the "Click to Activate youtube Focus" is NOT sufficient as it doesnt persist across new tabs and there is no way to do that. 

## Option 1 — Use the separate **Mordaut** account (recommended first)
**Idea:** Use my existing secondary YouTube/Google account, **Mordaut**, on the work computer. Disable and clear YouTube watch history on that account so YouTube stops populating the homepage with personalized video recommendations.

BASICALLY: 
* (R) Turn of Version History so that the front page doesn't include recommendations. 
* (R) To use the Ambient Sounds folders:
    * (R) Simply Share this playlist with Mordaut -> This can be done using the "Collaborate" feature in the youtube playlists. 

### Issue: Googles configuration.
* ISSUE: Because of google's genious design; signing out automatically signs out from ALL accounts, and all accounts are also used across all platforms; Google Drive, Gmail, Youtube etc. So when i signed out, i lost access to my main account's gdrive. So by default, i need to be logged in as John for my main account as i dont want to switch account all the time in order to use Gdrive. So i need John to be the first account, meaning that whenever i login to youtube, it will not be Mordaut by default. 


* SOLUTION: Login First with Mordaut [The main intended account] and THEN with John [My original account that i used up until now]. Then, Whenever i open youtube (now that the history is disabled) the front page gives no recommendations. 

    * This creates a small hassle wherein i by default get sent to Mordaut when going into my gdrive, BUT, this can be managed by removing historical references to the "u0" in the gdrive; I.e so that the main link that gets suggested when typing drive, becomes: 
    https://drive.google.com/drive/u/1/home


## OPTION 1b
If i have later issues with this, I guess we can simply disable the main page programmetically, as indicated in Option 3 below. 

## Option 2 — Brave browser with built-in content filtering

**Idea:** Install [Brave Browser](https://brave.com/download/), which has native page-element blocking. Hide YouTube's homepage recommendations, related-video panels, and potentially Shorts using **Shields → Content filtering**. This is built into Brave and does not depend on Chrome extensions.

**Advantages:**
- Free; no additional blocker extension is required.
- Works with my existing YouTube account without changing watch history or playlists.
- Can hide **parts of YouTube** rather than block the entire site.
- Browser-level cosmetic filters persist across tabs.

**Limitations:**
- Requires changing browsers, at least for YouTube.
- Although Brave is Chromium-based and Google services generally work, company authentication or managed-browser requirements may interfere; test rather than assume.
- YouTube interface changes can break filters, requiring adjustments.
- Filtering can be disabled, so it is not strict enforcement.


## Option 3 — FocusMe desktop application

**Idea:** Install [FocusMe](https://focusme.com/website-blocker/), a dedicated Windows website/app blocker that can operate across browsers, including Chrome. Configure work-hour restrictions for distracting YouTube URLs while leaving essential video links accessible where possible.

Cost: 10 USD per month. This seems like overkill, but could actually be worth it. Especially since it has a lifetime purchase of 250 USD.

HOWEVER: A different solution rather than paying for this is to simply do the basic things needed to solve my problem, basically: 

    * Disable specifically the Youtube Home Page
    * Remove the Recommendation feed -> This can already be done using the existing "Click to activate" javascript script i added. 

