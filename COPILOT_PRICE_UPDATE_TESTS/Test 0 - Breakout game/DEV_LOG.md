# Breakout Game Dev Log

Current status:
- Basic Tkinter breakout game added in `breakout_game.py`.
- Uses the repo `.venv`; no extra install was needed.
- Keyboard input is bound globally within the app and forced into focus for reliability.
- Brick drops can now spawn laser powerups; collecting one enables Space-fired laser shots for 10 seconds with a 1-shot-per-second cap.
- Brick drops can also spawn double-ball powerups; collecting one adds a copied ball, and both powerups show a text label near the drop.
- Session 4 added: main menu, debug mode, powerup click-to-collect in debug, speed multipliers, brick tool, and health-based staggered brick layers.
- Next session mechanics added: multiball, radioactive ball, electric ball, and probe behavior with electrified brick timers.
- Validation passed with `get_errors` and `python -m py_compile`.
- Session 5b added: electric bricks no longer refresh their destruction timer on repeated hits.
- Session 5b added: debug destroy tool with dropdown-selected forced powerup drops, plus snapped brick placement that follows the regular brick grid.
- Session 5c adjusted the debug UI so the dropdown/button sit below the brick health controls, and the destroy button now performs a one-shot random brick destroy instead of toggling.
- Session 6 added: electric brick expiry drops powerups again, radioactive/electric enhancements last 15s on one unaffected ball, Space releases held multiballs and special powerups, and dwarf/alien powerups were added.

Run:
- `.\.venv\Scripts\python.exe ".\COPILOT_PRICE_UPDATE_TESTS\Test 0 - Breakout game\breakout_game.py"`

Notes:
- Keep this folder self-contained.