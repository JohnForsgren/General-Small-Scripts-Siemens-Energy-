## How To Use The App

### If Chrome extension install is allowed
1. Open `chrome://extensions`.
2. Turn on Developer mode.
3. Click Load unpacked.
4. Select the `Focus_Productivity_Application` folder.
5. Open YouTube and use the popup to enable or disable focus mode.

### If extension install is blocked by policy
1. Open `bookmarklet.html` in Chrome.
2. Drag the generated link to your bookmarks bar, or copy the code into a new bookmark URL.
3. Open YouTube.
4. Click the bookmarklet to hide the home feed and recommendations.
5. Click it again to remove the focus styling.

### What to expect
- Works best on the current YouTube tab.
- Keeps working across YouTube page navigation in the same tab.
- A full reload or browser restart means you click the bookmarklet again.

### Current wider-solution status
- Chrome's organization policy blocks extension installation, including local unpacked extensions.
- Therefore, the extension cannot currently apply the rules automatically across YouTube tabs or other websites.
- The bookmarklet only affects the active tab and must be clicked again after a reload or in a new tab.
- A wider automatic solution requires IT to allowlist or internally distribute the extension; the policy cannot be bypassed through code.


