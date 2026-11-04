"""Count PDF pages in a folder; include DOCX files in the document inventory."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Callable
from xml.etree import ElementTree
from zipfile import BadZipFile, ZipFile

from pypdf import PdfReader


@dataclass(frozen=True)
class Document:
    path: Path
    name: str
    kind: str
    size: int
    pages: int | None
    note: str = ""


@dataclass(frozen=True)
class Report:
    folder: Path
    documents: list[Document]

    @property
    def pdf_pages(self) -> int:
        return sum(doc.pages or 0 for doc in self.documents if doc.kind == "PDF")

    @property
    def pdf_count(self) -> int:
        return sum(doc.kind == "PDF" for doc in self.documents)

    @property
    def docx_count(self) -> int:
        return sum(doc.kind == "DOCX" for doc in self.documents)

    @property
    def failed_count(self) -> int:
        return sum(doc.kind == "PDF" and doc.pages is None for doc in self.documents)


def _docx_pages(path: Path) -> tuple[int | None, str]:
    """Read the optional, potentially stale page count stored by the DOCX producer."""
    try:
        with ZipFile(path) as archive:
            # A valid DOCX has its document part even if it has no app properties.
            if "word/document.xml" not in archive.namelist():
                return None, "Invalid DOCX"
            if "docProps/app.xml" not in archive.namelist():
                return None, "Page count unavailable"
            root = ElementTree.fromstring(archive.read("docProps/app.xml"))
            page_node = root.find("{http://schemas.openxmlformats.org/officeDocument/2006/extended-properties}Pages")
            if page_node is not None and page_node.text:
                pages = int(page_node.text)
                if pages > 0:
                    return pages, "Stored DOCX page count (may be outdated)"
            return None, "Page count unavailable"
    except (OSError, BadZipFile, ValueError, ElementTree.ParseError) as exc:
        return None, f"Cannot read DOCX: {exc}"


def scan_folder(
    folder: Path,
    recursive: bool = True,
    progress: Callable[[int, int], None] | None = None,
) -> Report:
    folder = folder.expanduser().resolve()
    if not folder.is_dir():
        raise NotADirectoryError(f"Folder not found: {folder}")

    paths = sorted(
        (p for p in (folder.rglob("*") if recursive else folder.iterdir())
         if p.is_file() and p.suffix.lower() in {".pdf", ".docx"}),
        key=lambda p: str(p.relative_to(folder)).casefold(),
    )
    if progress:
        progress(0, len(paths))
    documents: list[Document] = []
    for index, path in enumerate(paths, 1):
        kind = path.suffix[1:].upper()
        pages = None
        note = ""
        try:
            size = path.stat().st_size
            if kind == "PDF":
                with path.open("rb") as stream:
                    reader = PdfReader(stream, strict=False)
                    if reader.is_encrypted and reader.decrypt("") == 0:
                        note = "Password-protected PDF"
                    else:
                        pages = len(reader.pages)
            else:
                pages, note = _docx_pages(path)
        except Exception as exc:
            # pypdf raises several PdfReadError/stream-specific exception types.
            size = 0
            note = f"Cannot read {kind}: {exc}"
        documents.append(Document(path, str(path.relative_to(folder)), kind, size, pages, note))
        if progress:
            progress(index, len(paths))
    return Report(folder, documents)


def export_csv(report: Report, destination: Path) -> None:
    with destination.open("w", newline="", encoding="utf-8-sig") as stream:
        writer = csv.writer(stream)
        writer.writerow(["Document", "Type", "Size (bytes)", "Pages", "Note"])
        for doc in report.documents:
            writer.writerow([doc.name, doc.kind, doc.size, doc.pages if doc.pages is not None else "", doc.note])