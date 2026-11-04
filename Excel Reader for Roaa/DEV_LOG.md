# Excel Reader for Roaa - Dev Log

## Current status
- `kks_report.py` reads `.xlsx` files from an input folder and reports document rows where `TC KKS` is blank.
- Expected workbook schema found in sample files: `Type`, `Item ID`, `Version`, `Title`, `TC KKS`; main sheet is usually `en`.
- Outputs: formatted Excel workbook plus HTML dashboard.

## Usage
- From repo root: `.\.venv\Scripts\python.exe "Excel Reader for Roaa\kks_report.py" "Excel Reader for Roaa\Excel Files - Example Case 1" --output-dir "Excel Reader for Roaa\output"`

## Notes for next agent
- Missing TC KKS is counted only for rows where `Type` equals `Document` case-insensitively.
- Blank, whitespace, `None`, and NaN `TC KKS` values count as missing.
- `openpyxl` can warn about missing default workbook styles in one sample file; script suppresses that style warning.
- Dashboard now embeds Plotly inline, so it does not rely on the CDN; if Teams still strips script execution in preview, open the file in a browser or export a static version.