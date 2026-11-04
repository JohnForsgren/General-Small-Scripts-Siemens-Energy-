# Neon Breakout

A Python/Pygame breakout game built around a neon arcade theme.

## Run

From the repository root, use the existing virtual environment:

```powershell
.\.venv\Scripts\python.exe ".\GPT 5.6 Luna Test\main.py"
```

Or activate the environment first:

```powershell
.\.venv\Scripts\Activate.ps1
python ".\GPT 5.6 Luna Test\main.py"
```

Install dependencies only into the repository environment:

```powershell
.\.venv\Scripts\python.exe -m pip install -r ".\GPT 5.6 Luna Test\requirements.txt"
```

## Controls

- **A/D** or **arrow keys**: move paddle
- **Space**: release held balls and special tools
- **P**: pause
- **Escape**: return to the main menu

## Features

- Main menu, playable game, debug mode, and level creator
- Enlarged 1440×900 arcade window with a wider playfield and dedicated right-side tool space
- Level selector with ten compact previews and click-to-start selection
- Staggered brick rows with 1, 2, and 3 hit-point bricks
- Permanent metallic wall segments that create long frames, corridors, gates, and ricochet routes; they are scenery, not bricks, and never count toward level completion
- Six powerups: Multiball, Radioactive Ball, Electric Ball, Probe, Dwarf, and Alien
- Fifteen-second ball enhancements, electric chain reactions, probe orbiting, pickaxe attacks, and upward infection spread
- Score values and combo milestones from Super Crush through Ultimate Extravaganza
- Ten denser creative preset levels with named structures: Starfall, Butterfly Array, Neon Crown, Serpent Run, Orbital Ring, Fortress Core, Arrowhead, Watcher, Diamond Vault, and Tidal Wave
- Space Ship powerup: a three-second invulnerable launch from the paddle followed by Moving, Aiming, and Firing modes; it blocks against bricks, fires two same-angle inaccurate wing missiles, is destroyed by ball contact, and is removed on level changes
- Debug powerup selector, speed multipliers, guaranteed destroy/drop button, and drag-to-place brick tool
- Custom level creator saves `custom_level.json` beside the game

The game uses geometric rendering and does not require external sprite downloads or network access.
