

CONTEXT: This is a test to determine the performance of AI models by asking it to solve a task. 


- Use the .venv of the root folder . You should not read anything outside of the GPT 5.6 Luna test except for the readme. Document the current session in the dev log if the relevant copilot instructions for writing dev logs are available. 


___ Here is the task ___ 


(Note to self: Original game that is used as blueprint here is: WiLkANoiD from 2001)

MAIN PROMPT

I need you to design a breakout game. Here are some general guidelines: 

Baseline Features 
LANGUAGE and SETUP
- Choose an appropriate language, but not Javascript. 
- It must have a virtual environment if written in a related environment, like C# or python. Installations must NOT be made to the global environment. 

General
It is played with a paddle and a ball. 
- The paddle starts with a ball "held" at it; At this stage the ball follows the paddle and is released 

Breaking bricks will have a chance of yielding power ups, which will be dropped down and can be picked up by the player. 

Bricks/Tiles
- The bricks can come in 3 different colors, requiring 1, 2 and 3 collisions with a ball, respectively. 
- The bricks are 1x4 units wide, and each layer has a 2 unit long displacement. This means that in each layer, each brick has 2 bricks touching directly above it, each covering half the distance of the brick under it. Here is a basic pattern example: "XXXX" and "YYYY" are representations of bricks, "_" represent nothing (air).  
YYYYXXXXYYYYXXXXYYYY
__XXXXYYYYXXXXYYYY__

Interface
There is to be a main menu, but initially there doesn't have to be much there. Minimum features include: 

Main Game -> Goes to the main game 

DEBUG MODE  - See separate section 

A version of the game for testing. Here you can: 
- Press a button to destroy a brick with a guaranteed chance to get a powerup. The powerup that is dropped is based on a dropdown UI: "Random" is selected by default here. This drop down menu sets which upgrade is dropped. 
- Modify the speed of the paddle and ball [Multipliers: 0.25, 0.5,1, 1.5, 2] 
- Place bricks down with a brick-placing tool which, once toggled on, places bricks where on the screen as the user clicks and holds down on the screen. The bricks are only placed in the same pattern as regular bricks; i.e in the same "YYYYXXXX"-formation as described above; i.e holding down doesn't place a bunch of bricks on the same tile. 


Debug mode 


Power-Ups

Ball enhancements affect one unaffected ball when picked up. They last for 15 seconds. 

Powerup: Multiball
Gives a new ball which the paddle "holds" until released with space. 

Ball Enhancement: Radioactive Ball
The ball becomes radioactive (glowing green) and is able to destroy any brick it collides with instantly without getting pushed back; it simply goes through all bricks it comes in contact with. 

Ball Enhancement: Electric Ball 
The ball becomes electric (Yellow). When it strikes a brick, it electrocutes that brick and all adjacent bricks, turning them yellow, which destroys them after 5 seconds. 

Powerup: Probe
A small allied particle is released. When released, it flies to the nearest ball, damaging any bricks it comes in contact with. Once it is at the ball, it spins around the center of the ball repeatedly, damaging any bricks it comes in contact with.

Powerup: Dwarf
The dwarf is a power up, consisting of two rectangular shaped hitboxes (1) The dwarf (2) His arm and pickaxe.
When obtaining the powerup, he appears on top of the paddle and is released by pressing space. He then flies straight upward and, when coming in contact with a brick, he stops for 2 seconds and takes up his pickaxe; The pickaxe emerges from around his shoulders (i.e 75% of the height of the rectangle). The pickaxe has a rectangular hitbox, and only the pickaxe (not the dwarf) destroys bricks). The dwarf continues floating upwards as his pickaxe rotates around his shoulder in 360 degrees, crushing all blocks which the pickaxe touches. 

Powerup: Alien
When obtaining the powerup, it appears on top of the paddle and is released by pressing space. It then flies straight upwards and stops at the first brick it comes in contact with. The brick then becomes infected after 2.5 seconds, turning purple. Then, the infected brick infects any other adjacent bricks above it, i.e any brick which touches the infected brick and is above it, will be infected and then continue to infect bricks above it - leading to a "V"-shaped infection upwards. Infected bricks are destroyed after 3.5 seconds (i.e 1 second after infecting the ones above).



Advanced features 

Level Creator
As an advanced feature there should be a level creator where the user can create custom scenarios. 

Existing levels
There should be a collection of existing levels. Importantly: The levels should not be boring with just a single cluster of bricks. Rather, it should be made in creative shapes. 


Score

You gain points for crushing bricks: 
1 HP Bricks: 100p
2 HP Bricks (Requires hitting them twice): 300p
3 HP Bricks: 400 p

Combos: Combo are if sufficient bricks are destroyed consecutively (i.e it ends if more than 2. seconds pass during which no bricks have been destroyed). Only the text and score is displayed on the screen after the time passes without a brick being destroyed, if a sufficient amount of bricks was destroyed.  
Super Crush (6 bricks): 1000
Mega Multi Crush (10 Bricks): 5000
Super Crusher Combo (15 bricks): 10000
ULTIMATE EXTRAVAGANZA COMBO (25 bricks): 50000 

EXTRA advanced: 
Ask the AI agent to search online on some safe page to retrive sprites for the game. 







