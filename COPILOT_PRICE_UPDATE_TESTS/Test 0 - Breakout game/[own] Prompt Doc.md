



## Session 4 
Bricks/Tiles
- The bricks can come in 3 different colors, requiring 1, 2 and 3 collisions with a ball, respectively. 
- The bricks are 1x4 units wide, and each layer has a 2 unit long displacement. This means that in each layer, each brick has 2 bricks touching directly above it, each covering half the distance of the brick under it. Here is a basic pattern example: "XXXX" and "YYYY" are representations of bricks, "_" represent nothing (air).  
YYYYXXXXYYYYXXXXYYYY
__XXXXYYYYXXXXYYYY__


Interface
There is to be a main menu, but initially there doesn't have to be much there. Minimum features include: 

Main Game -> Goes to the main game 

Debug mode  - A version of the game for testing. Here you can: 
- Gain any powerup by simply clicking on it 
- Modify the speed of the paddle and ball [Multipliers: 0.25, 0.5,1, 1.5, 2] 
- Place bricks down with a brick-placing tool which, once toggled on, places bricks where on the screen as the user clicks and holds down on the screen.

## Session 5 

And now for the next session:

**Powerup: Multiball

Gives a new ball which the paddle "holds" until released with space.

Ball Enhancement: Radioactive Ball

The ball becomes radioactive (glowing green) and is able to destroy any brick it collides with instantly without getting pushed back; it simply goes through all bricks it comes in contact with.

Ball Enhancement: Electric Ball

The ball becomes electric (Yellow). When it strikes a brick, it electrocutes that brick and all adjacent bricks, turning them yellow, which destroys them after 5 seconds.

Powerup: Probe

A small allied particle is released. When released, it flies to the nearest ball, damaging any bricks it comes in contact with. Once it is at the ball, it spins around the center of the ball repeatedly, damaging any bricks it comes in contact with.

### Session 5b

- BUG: Electric ball works strangely. It appears to extend its destruction timer every time the ball collides which is incoirrect 
- Press a button to destroy a brick with a guaranteed chance to get a powerup. The powerup that is dropped is based on a dropdown UI: "Random" is selected by default here. This drop down menu sets which upgrade is dropped. 
- Debug tool: Place bricks down with a brick-placing tool which, once toggled on, places bricks where on the screen as the user clicks and holds down on the screen. The bricks are only placed in the same pattern as regular bricks; i.e in the same "YYYYXXXX"-formation as described above; i.e holding down doesn't place a bunch of bricks on the same tile. 



### SESSION 6 

- BUG: It appears that electrified bricks do not drop any powerups. A brick should always have a 15% chance to destroy a powerup regardless of how it is destroyed with the only exception being that th chance is 100% if using the special feature. 
Perhaps this is caused when the powerup debug feature is active. Not sure. 
- SMALL BUG: Pressing space should not trigger the Debug Upgrade drop,. 
- BUG: Multiballs fail, at least in debug mode; Nothing happens when pressing space once the ball is one the paddlle. Perhaps this is due to the previous bug. 

- Ball enhancements (radiactive / electric) affect one unaffected ball when picked up. They last for 15 seconds. 

NEW POWERUPS: 
Powerup: Dwarf
The dwarf is a power up, consisting of two rectangular shaped hitboxes (1) The dwarf (2) His arm and pickaxe.
When obtaining the powerup, he appears on top of the paddle and is released by pressing space. He then flies straight upward and, when coming in contact with a brick, he stops for 2 seconds and takes up his pickaxe; The pickaxe emerges from around his shoulders (i.e 75% of the height of the rectangle). The pickaxe has a rectangular hitbox, and only the pickaxe (not the dwarf) destroys bricks). The dwarf continues floating upwards as his pickaxe rotates around his shoulder in 360 degrees, crushing all blocks which the pickaxe touches. 

Powerup: Alien
When obtaining the powerup, it appears on top of the paddle and is released by pressing space. It then flies straight upwards and stops at the first brick it comes in contact with. The brick then becomes infected after 3 seconds, turning purple. Then, the infected brick infects any other adjacent bricks above it, i.e any brick which touches the infected brick and is above it, will be infected and then continue to infect bricks above it - leading to a "V"-shaped infection upwards. Infected bricks are destroyed after 5 seconds (i.e 2 seconds after infecting the ones above).



