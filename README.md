# General Small Scripts

Sandbox repo for testing small projects without setting up new infrastructure every time.
Usually only one project is worked on at a time; i.e typically only one folder will be relevant to look at in any given session.


Shared infrastructure:
- Root `.venv` for Python packages and script execution.
- Repo-level GitHub Copilot instructions in `.github/instructions/`.
- Optional shared frontend toolchain if small React experiments start to repeat.

Project layout:
- Each experiment lives in its own folder.
- `2026-09 - PDF Page Counter/`: local PDF page totals, DOCX inventory, Tkinter desktop app, Python zipapp CLI, CSV export. See that project's README and DEV_LOG for usage and build details.
- Other folders are independent experiments; see each project's README or DEV_LOG where available.

Run the fixed Python sample:

```powershell
.\.venv\Scripts\python.exe .\Random_GPT-5.4-nano_Test\GPT_5.4_Test_fixed.py
```