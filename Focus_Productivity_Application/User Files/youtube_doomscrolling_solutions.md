# Reducing YouTube Doomscrolling on My Work Computer

*Decision notes — 4 November 2026*

## Problem description

While working from home, I have developed a recurring habit: when I get stuck on a task, I automatically open YouTube and start scrolling through the homepage recommendations. This was not previously a major problem, but it has become more frequent on my work computer. Chrome Extensions are Disabled, and efforts to create a working solution has NOT Worked: It is confirmed that thet current solution wherein i have the "Click to Activate youtube Focus" is NOT sufficient as it doesnt persist across new tabs and there is no way to do that. 

## Option 1 — Use the separate **Mordaut** account (recommended first)
**Idea:** Use my existing secondary YouTube/Google account, **Mordaut**, on the work computer. Disable and clear YouTube watch history on that account so YouTube stops populating the homepage with personalized video recommendations.

BASICALLY: 
* Turn of Version History so that the front page doesn't include recommendations. 
* To use the Ambient Sounds folders: 
    * Simply Share this playlist with Mordaut -> This can be done using the "Collaborate" feature in the youtube playlists. 


* OPTIONALLY: Disable the front page. 

___________________ 






**Steps:**

1. Sign into the **Mordaut** account on YouTube.
2. Open [Google My Activity — YouTube History](https://myactivity.google.com/product/youtube).
3. Turn off YouTube watch history.
4. Delete existing watch history for that account if necessary. **Check which account is selected first.**
5. Reload YouTube and confirm the homepage is mostly empty rather than filled with recommendations.

**Advantages:**
- Free and requires no installations, extensions, or custom scripts.
- The change persists across newly opened tabs and browser restarts.
- YouTube searches, subscriptions, and directly linked videos remain accessible.
- My **main account and its ambient-music playlists remain untouched**.

**Limitations:**
- History settings apply to the **entire Mordaut account across devices**, not just the work PC.
- This mainly removes the **homepage recommendation feed**; suggestions beside or after an individual video may still appear.
- It is easy to reverse manually, and I must remember to use Mordaut rather than my personal account when working.
- Clearing history is destructive for that account; it can also delete search history for the selected period.

**Assessment:** The simplest and best first experiment. It directly addresses the primary trigger without disrupting my main account.

## Option 2 — Brave browser with built-in content filtering

**Idea:** Install [Brave Browser](https://brave.com/download/), which has native page-element blocking. Hide YouTube's homepage recommendations, related-video panels, and potentially Shorts using **Shields → Content filtering**. This is built into Brave and does not depend on Chrome extensions.

**How to try it:**

1. Confirm that installing and using Brave is permitted on the work computer.
2. Open YouTube in Brave, right-click a distracting page element, then select **Brave → Block element**; alternatively configure custom rules via `brave://settings/shields/filters`.
3. Test several fresh tabs and browser restarts to verify that the recommendations remain hidden.
4. Check company sign-in and essential Google services (especially **Google Drive, Docs, and Sheets**) before adopting Brave as the daily browser.

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

**Assessment:** Best free option for *customized page cleanup*, especially if I want to keep watching videos without recommendations around them. Less convenient if work requires Chrome or Google services work less reliably in Brave.

## Option 3 — FocusMe desktop application

**Idea:** Install [FocusMe](https://focusme.com/website-blocker/), a dedicated Windows website/app blocker that can operate across browsers, including Chrome. Configure work-hour restrictions for distracting YouTube URLs while leaving essential video links accessible where possible.

Cost: 10 USD per month. This seems like overkill, but could actually be worth it. Especially since it has a lifetime purchase of 250 USD.

HOWEVER: A different solution rather than paying for this is to simply do the basic things needed to solve my problem, basically: 

    * Disable specifically the Youtube Home Page
    * Remove the Recommendation feed -> This can already be done using the existing "Click to activate" javascript script i added. 


## Quick comparison

| Criterion | Mordaut account | Brave | FocusMe |
|---|---|---|---|
| Price | Free | Free | Paid after trial |
| Works in existing Chrome | Yes | No, requires Brave | Yes |
| Persistent across new tabs | Yes | Yes | Yes |
| Main account/history unaffected | Yes, if I use Mordaut | Yes | Yes |
| Removes homepage recommendations | Yes, account setting | Yes, via page filters | Can block homepage access |
| Removes suggestions beside videos | Not reliably | Can filter these | Not its main purpose |
| Strict enforcement | No | No | Stronger enforcement possible |
| Main concern | Must use Mordaut consistently | Different browser / company compatibility | Cost, permissions, URL precision |

## Recommended order of action

1. **Try Mordaut first.** Turn off and clear watch history only on that account. Test the YouTube homepage in new tabs over a few working days.
2. **If the habit persists, try Brave.** Test YouTube element blocking and Google Drive/Docs compatibility on the work computer before switching fully.
3. **Consider FocusMe only if stronger enforcement becomes necessary.** Evaluate the trial and ensure selective URL blocking functions well without browser extensions.

**Additional habit insight:** The trigger is not usually a need to watch YouTube; it is **getting stuck on work**. A useful complementary rule is to write down the blocker and one small next action before opening another website. This does not replace technical blocking, but addresses the automatic behavior that starts the scrolling.

## References

- [YouTube Help — How recommendations work](https://support.google.com/youtube/answer/16089387?hl=en)
- [YouTube Help — Manage recommendations and search results](https://support.google.com/youtube/answer/6342839?hl=en)
- [YouTube Help — View, delete, or turn watch history on/off](https://support.google.com/youtube/answer/95725?hl=en)
- [Brave Help — Manage content filters](https://support.brave.app/hc/en-us/articles/6449369961741-How-do-I-manage-adblock-filters-in-Brave)
- [Brave Help — Block elements on a webpage](https://support.brave.app/hc/en-us/articles/360018039072-How-do-I-use-the-Content-Filter-to-block-elements-on-a-webpage)
- [FocusMe — Website blocker](https://focusme.com/website-blocker/)
- [FocusMe — Pricing](https://focusme.com/pricing/)
- [FocusMe — Blocking YouTube](https://focusme.com/blog/how-to-block-youtube/)
