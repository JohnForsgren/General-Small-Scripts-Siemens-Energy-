# Development Log

## 2026-07-31

- Read task requirements and root README.
- Configured the repository `.venv` (Python 3.10.9).
- Installed `pygame==2.6.1` into the repository virtual environment only.
- Implemented `main.py` as a self-contained neon breakout game.
- Added main menu, gameplay, debug mode, and level creator.
- Added staggered brick layouts, HP colors, scoring, combo milestones, lives, pause, and level progression.
- Added Multiball, Radioactive, Electric, Probe, Dwarf, and Alien powerups.
- Added run instructions and dependency pin in `README.md` and `requirements.txt`.
- Added focused tests for brick state, held-ball positioning, and staggered level construction.

## Validation

- `py_compile` passed for game and test modules.
- Focused test suite passed: 3 tests.
- Headless Pygame startup/render smoke test passed (`scene=menu`, 53 bricks loaded).
- Manual control exercise remains optional when a display is available.

## Levels and Space Ship - 2026-07-31

- Replaced three preset layouts with ten named, shape-based levels.
- Added level selector scene with ten compact preview cards and click-to-start behavior.
- Corrected Space Ship to launch from the paddle, remain invulnerable for three seconds, then cycle through Moving, Aiming, and Firing modes.
- Space Ship now rotates toward a target, fires two wing missiles with one shared ±20-degree error, blocks against bricks, and is removed on level changes.
- Added seven regression tests; total focused suite result: 12 passed.

## Visual and level-density pass - 2026-07-31

- Enlarged the window to 1440×900 and moved debug/editor panels to the right-side context area.
- Added permanent `S` scaffold tiles with metallic cross-braced rendering and collision reflection.
- Re-authored all ten levels with denser formations, frames, mazes, corridors, rings, and permanent wall routes.
- Expanded the level creator grid to 15 columns.
- Added one scaffold/level-transition regression test; total focused suite result: 13 passed.

## Wall-segment correction - 2026-07-31

- Replaced permanent scaffold `Brick` objects with standalone `WallSegment` bars; contiguous `S` cells now render as long structural segments.
- Walls are excluded from breakable-brick scoring, drops, infection, electric discharge, and level completion.
- Balls reflect from walls; Space Ship movement and missiles are blocked by them.
- Dwarf, Alien, Probe, and similar temporary entities disappear on wall contact without applying effects.

## Gameplay bug fixes - 2026-07-31

- Radioactive and other ball effects now clear both effect state and expiration timestamp at 15 seconds.
- Dwarf and Probe brick destruction now use the normal 23% drop chance; Debug remains guaranteed.
- Alien infection now spreads only to overlapping bricks in the immediately higher row at each timed step.
- Electric Ball now marks the struck brick and touching neighbors yellow without refreshing the five-second timer on repeated collisions.
- Probe now transitions into a persistent orbit and follows moving balls without slack.
- Added five regression tests; total focused suite result: 8 passed.
