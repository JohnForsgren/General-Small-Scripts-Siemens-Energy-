# Document page counter

Counts PDF pages in a selected folder and lists PDF and DOCX documents. **Includes all subfolders by default**, even if the selected folder has no documents directly inside it. Everything runs locally; no files are uploaded.

## Desktop app (Windows)

Run **Document Page Counter.exe** from the `dist` folder. Browse to a folder (or paste its path), select **Count pages**, and optionally expand **Show document details** or **Export CSV**. The prominent **Include subfolders** button is enabled by default; click it to scan only files directly in the selected folder. A progress bar shows the percentage of documents read. While the app finds files, the bar animates until the total is known. The EXE and its window have a custom document icon. The desktop EXE is a self-contained, single Windows file; Python is not needed on the recipient's computer. If company policy blocks unsigned executables, use the script instead. Do not bypass company security policy.

## Script (Windows/macOS/Linux)

Run `python document-page-counter.pyz` from the `dist` folder. This is a **single file with no pip dependencies**, but **not a standalone executable**: it requires Python **3.10+** on the recipient's computer. The PDF parser is inside the archive. It asks whether to scan the folder **containing the script**, including all its subfolders; answer Y or paste another folder path (quotes are optional). If the archive remains in `dist`, answering Y scans `dist`, **not its parent folder**. Move the archive into the intended folder or paste the path. It prints totals and the per-document list.

For noninteractive use, pass the folder directly, e.g. `python document-page-counter.pyz "C:\path\to\documents" --csv "C:\path\to\results.csv"`. Subfolders are included automatically; pass `--root-only` if you want to exclude them. The archive works with local paths; it does not connect to TPS or retrieve documents from it. Download/export the documents from TPS first.

**Totals:** Documents includes PDF and DOCX files. Total pages counts **PDF pages only**. When PDFs cannot be read (including password-protected ones), the page total is marked incomplete and details explain why. DOCX page counts are shown only when stored in DOCX metadata; these values may be stale and are never added to the PDF total. A DOCX without such metadata shows “—”. File extensions are matched case-insensitively.

## Build from source

Use Python 3.10+ on Windows. Install dependencies with `python -m pip install -r requirements.txt`, then run `python build.py --exe` to create both distributable files in `dist`. Run `python build.py` to build just the single-file script (on any supported OS). Each file can be shared separately. To run source directly after installing dependencies: `python gui.py` or `python cli.py`.

Tests: `python -m unittest discover -s . -p "test_*.py"`. Sample documents are in `Test Cases`; expected sample results: **2 PDFs, 1 DOCX, 12 PDF pages** (4 and 8 respectively). The sample DOCX currently reports 9 stored pages, which may not reflect actual rendered pages.