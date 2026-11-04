"""Terminal version of the PDF page counter."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from counter import export_csv, scan_folder


def main() -> int:
    parser = argparse.ArgumentParser(description="Count PDF pages and list PDF/DOCX documents.")
    parser.add_argument("folder", nargs="?", help="Folder to scan; prompts if omitted")
    scope = parser.add_mutually_exclusive_group()
    scope.add_argument("--recursive", dest="recursive", action="store_true", default=True, help="Include subfolders (default)")
    scope.add_argument("--root-only", dest="recursive", action="store_false", help="Scan only the selected folder")
    parser.add_argument("--csv", type=Path, help="Save document list to a CSV file")
    args = parser.parse_args()

    if args.folder:
        folder = Path(args.folder.strip().strip('"'))
    else:
        default = Path(sys.argv[0]).resolve().parent
        print(f"Script folder: {default}")
        try:
            answer = input("Are the documents in this folder? [Y/n]: ").strip().lower()
            folder = default if answer in ("", "y", "yes") else Path(input("Paste folder path: ").strip().strip('"'))
        except (EOFError, KeyboardInterrupt):
            print("\nCancelled.")
            return 1

    try:
        report = scan_folder(folder, recursive=args.recursive)
        if args.csv:
            export_csv(report, args.csv)
    except (OSError, ValueError) as exc:
        print(f"Error: {exc}")
        return 1

    print(f"\nFolder: {report.folder}")
    print(f"Documents: {len(report.documents)} ({report.pdf_count} PDF, {report.docx_count} DOCX)")
    print(f"PDF pages: {report.pdf_pages}" + (f" (at least; {report.failed_count} PDF(s) unreadable)" if report.failed_count else ""))
    if report.docx_count:
        print("DOCX pages are not included in the PDF page total; stored counts may be outdated.")
    print("\nDOCUMENTS\n" + "-" * 76)
    for doc in report.documents:
        page_text = str(doc.pages) if doc.pages is not None else "—"
        print(f"{doc.name}  |  {doc.kind}  |  {doc.size:,} bytes  |  {page_text} pages")
        if doc.note:
            print(f"  {doc.note}")
    if not report.documents:
        print("No PDF or DOCX files found in this folder.")
    if args.csv:
        print(f"\nSaved list: {args.csv.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())