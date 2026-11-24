


# ======= CURRENT STATUS ======= 

## === UPDATE regarding solutions discussed in the previous (first) update ===

### SOLUTION 1: Mordaut account

This solves the issue of the distracting youtube start page, but does not fix the issue with ads. 

* YOUTUBE SUBSCRIPTION: Costs 150 SEK per month. Not at all feasible. The sub i already have for Google Pro (20 USD per month) provides some sort of access to youtube premium lite, but this doesn't apply fully for ambient sounds and also doesnt solve the issue of the distracting start page (as it is on my main youtube account, not mordaut). Not viable. 


### SOLUTION 2: Brave browser
* I contacted IT after it was blocked by IT. They confirmed that oinly chrome and edge are allowed browsers, eliminating this option as well. 


### SOLUTION 3: FocusMe desktop application
* Not ideal since it is costing money and it is not confirmed that it will actually work on the laptop due to restrictions. 




## === NEW SOLUTION: yt-dlp === 

An assessment by GPT is written in : GPT 6 - Assessment of yt-dlp.md, citing the program as highly secure assuming that i only use it for the limited intended scope for downloading specific ambient sounds, which is the intention. 


# ======= USING THE APP =======

* The vision of using the app is basically: 
    1. I find new ambient sounds on youtube and listen to them locally instead.
    2. I sort them into categories (e.g "BEST" or "Decent") locally AS WELL AS in the corresponding youtube playlist. 
    3. Optionally, i upload them to gdrive (advantage: makes it re-usable; Distadvantage - can potentially clutter gdrive space.)




# ======= UPDATES ======= 

## SESSION 1 

* I have downloaded and run an initial run of the app here (approved by IT): 
C:\YT-DLP

Example run [POWERSHELL]: 
.\yt-dlp.exe --no-playlist -x --audio-format mp3 "https://www.youtube.com/watch?v=JAQ6kxyx7es&list=PLntykjs-tuy7IHk8I78imQYi_Shk0M57y" 

* Topic: I need to be able to download entire playlists at once
* Topic: Ideally the files should be downloaded to a subfolder , i.e not in the same folder as the exe files 


### SOLUTION: 


* GPT suggested to create a "yt-dlp.conf" which i have added to the file, containing: 
    # Download audio as MP3
    --extract-audio
    --audio-format mp3
    --embed-thumbnail
    --convert-thumbnails jpg

    # Download complete playlists
    --yes-playlist
    --ignore-errors

    # One folder for all MP3 files
    --paths "C:\YT-DLP\AMBIENT_SOUNDS"
    --output "%(title)s [%(id)s].%(ext)s"

The live config is `C:\YT-DLP\yt-dlp.conf`; the version-controlled backup for restoring this setup is [yt-dlp.conf](../yt-dlp.conf). Keep the backup synchronized if the live settings change.

* Playlists can be downloaded using commands like: C:\YT-DLP\yt-dlp.exe --yes-playlist --ignore-errors -x --audio-format mp3 --embed-thumbnail --convert-thumbnails jpg -P "C:\YT-DLP\AMBIENT_SOUNDS" -o "%(title)s [%(id)s].%(ext)s" "https://www.youtube.com/playlist?list=PLntykjs-tuy7IHk8I78imQYi_Shk0M57y"



## SESSION 2
* CRITICAL CONCERN: Security updates: what do i do here; how often should i do this, and is it really needed if i only download directly from yotuube? 
GPT 6 answer: For your specific use case—downloading selected YouTube playlists as MP3 files—the security risk is very low. I would still recommend occasional updates, but there's no reason to constantly monitor releases.

ADDITIONAL INFO was put inside the GPT 6 assessment on security.