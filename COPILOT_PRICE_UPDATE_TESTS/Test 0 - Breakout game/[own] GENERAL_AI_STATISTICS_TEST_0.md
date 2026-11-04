

Credits are based on the "Tokenyst" vsCode extension. 

MODEL: GPT-5.4-mini (high)

## === OVERALL EVALUATION === 

## PROS: 
* The quality seems PRETTY GOOD - I remember running this with Opus 4.1 previously (which is clearly a great model) and got fairly similar results but for WAY less monney.
    * Most features succeeded on first attempt, including the Dwarf, Probe, Electric ball, and Alien
    * I ran a long chat with many iterations and run commands by the agent, ending up with a code file that is 1700 lines long
* Price: 340 Credits. Usage went from 13% -> 20%. While this does take a chunk of the monthly budget, it should be MANAGABLE if we have $100 a month.  
* All was done in a single session; No need to switch. 

### CONS: 
* Multitude of bugs encountered; i would say about 6-7 fatal bugs were encountered in total, and it is possible that some bugs remain. 
* The game is somewhat laggy; likely not optimized fully. 
* I have some concern that the costs might radically increase if the AI is tasked to read lots of files and documentation, since this was a clean project from scratch. 

### GENERAL COMMENTS: 
* Sometimes limited ability to follow instructions, but also there were several instances where it fully delivered on vague requests. 



# ====== Chat 1 ======
It is useful to track the token count per chat, as reloading a new chat causes all input tokens to be read withotut Cache

## === Session 1 & 2 ===
Total creits spent: 49 Credits. 
- Small initial bug: Game crashes when pressing pace 
- Has a working player field and 

## === Session 3 ===
Total creits spent: 73.9
- Has multiball 

## === Session 4 ===  
Total creits spent: 108.1
Current context window filled: 129k (32% )

(Note: Sesion 4 is done on the day after Session 1-3, so the initial prompt might cost more due to the cache being lot? ANSWER: Does not seem likely; This was a large change and it only increased by a comparable amount of tokens to the previous session.  )

- TASK: Asked to add the following (see the "[own] Prompt Doc.md")
    * Main menu 
    * Basic Test mode
    * Switch placement of bricks so that they overlap.

- ISSUE: Multiple errors in the file. 


### Session 4b (small bug fix)
Total creits spent: (Something like 115)

- The file no longer has the error. However, game crashes and there is no paddle when starting it from the main menu 

### Session 4C 
Total creits spent: 119.6 
- The paddle still doesn't exist and the game crashes immediately. I simply sent the log message as response. 

### Session 4D 
Total creits spent: 125.8 
TOKENS IN CONTEXT WINDOW: 136k (34 %) 


### Session 4E
TOTAL CRETITS SPENT      : 167
TOKENS IN CONTEXT WINDOW : 39% 
- Solved bug of window being too small 

This caused a lot of iterations, which could explain why the cretits jumped. 


Bug: The window is too small: In the real mode, we cannot see the edge of the window where the bricks end (i.e they cut into the wall) . this isespecially devastating in the debug mode, where the menu takes up even more space. So the screen must change. 


## === Session 5 ===
TOTAL CRETITS SPENT      :  244.6 Credits
TOKENS IN CONTEXT WINDOW : Chat was summarized to 14% (was about 40%)


New powerups: 

- Radioactive ball
- Electric ball 
- Probe. 



### Session 5b 
TOTAL CRETITS SPENT      : 281.8 
TOKENS IN CONTEXT WINDOW : 25% 
SPENT TOKENS: 37; This is DESPITE the fact that the token count was reset. However i HOPE that this was primarily because new (non-cached tokens were read into the chat )

NOTE: The code is 1400 lines at this point (single file). 

- Fixed electric ball bug
- Added feature to debug mode to destroy bricks for powerups
- Fixed debug tool brick placement. 



### Session 5c
TOTAL CRETITS SPENT      : 294 
TOKENS IN CONTEXT WINDOW : 24% 
SPENT TOKENS IN SESSION  : 12

- Fixed bug with the destroy bricks for powerups. 



## === SESSION 6 ===
TOTAL CRETITS SPENT      : 343 
TOKENS IN CONTEXT WINDOW : 39% 
SPENT TOKENS IN SESSION  : 48.9 


- Bug fixes
- 2 New powerups (See prompt doc)

IMPRESSIVE: The game appears to work largely fine now. There are a few minor bugs, but from my initial 5 minutes of playing i see no obvious issues 















