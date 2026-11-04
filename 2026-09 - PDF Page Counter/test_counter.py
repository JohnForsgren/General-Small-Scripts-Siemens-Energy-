"""Regression tests for document counting and inventory export."""

import csv
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile

from pypdf import PdfWriter

from counter import export_csv, scan_folder


class CounterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.folder = Path(self.temp.name)

    def pdf(self, name: str, count: int, password: str | None = None) -> None:
        writer = PdfWriter()
        for _ in range(count):
            writer.add_blank_page(width=72, height=72)
        if password:
            writer.encrypt(password)
        with (self.folder / name).open("wb") as output:
            writer.write(output)

    def test_counts_mixed_case_pdf_docx_and_csv(self) -> None:
        self.pdf("one.PDF", 2)
        self.pdf("two.pdf", 3)
        with ZipFile(self.folder / "notes.docx", "w") as docx:
            docx.writestr("word/document.xml", "<document/>")
            docx.writestr("docProps/app.xml", '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"><Pages>7</Pages></Properties>')
        (self.folder / "ignore.txt").write_text("hello")
        updates: list[tuple[int, int]] = []
        report = scan_folder(self.folder, progress=lambda done, total: updates.append((done, total)))
        self.assertEqual(updates, [(0, 3), (1, 3), (2, 3), (3, 3)])
        self.assertEqual((len(report.documents), report.pdf_count, report.docx_count, report.pdf_pages), (3, 2, 1, 5))
        docx = next(doc for doc in report.documents if doc.kind == "DOCX")
        self.assertEqual(docx.pages, 7)
        self.assertIn("outdated", docx.note)
        target = self.folder / "results.csv"
        export_csv(report, target)
        with target.open(encoding="utf-8-sig", newline="") as stream:
            rows = list(csv.DictReader(stream))
        self.assertEqual(len(rows), 3)
        self.assertEqual(next(row for row in rows if row["Type"] == "DOCX")["Pages"], "7")

    def test_recursive_is_default_and_root_only_is_optional(self) -> None:
        (self.folder / "nested").mkdir()
        writer = PdfWriter()
        writer.add_blank_page(width=72, height=72)
        with (self.folder / "nested" / "sub.pdf").open("wb") as output:
            writer.write(output)
        self.assertEqual(scan_folder(self.folder, recursive=False).pdf_count, 0)
        report = scan_folder(self.folder)
        self.assertEqual((report.pdf_count, report.pdf_pages, report.documents[0].name), (1, 1, str(Path("nested") / "sub.pdf")))

        cli = Path(__file__).with_name("cli.py")
        result = subprocess.run([sys.executable, str(cli), str(self.folder)], capture_output=True, text=True, check=True)
        self.assertIn("Documents: 1 (1 PDF, 0 DOCX)", result.stdout)
        self.assertIn(str(Path("nested") / "sub.pdf"), result.stdout)
        root_only = subprocess.run([sys.executable, str(cli), str(self.folder), "--root-only"], capture_output=True, text=True, check=True)
        self.assertIn("Documents: 0 (0 PDF, 0 DOCX)", root_only.stdout)

    def test_password_and_broken_pdf_are_not_silently_counted(self) -> None:
        self.pdf("protected.pdf", 2, password="secret")
        (self.folder / "broken.pdf").write_bytes(b"not a pdf")
        report = scan_folder(self.folder)
        self.assertEqual((report.pdf_count, report.failed_count, report.pdf_pages), (2, 2, 0))
        self.assertTrue(all(doc.note for doc in report.documents))

    def test_empty_and_invalid_folder(self) -> None:
        updates: list[tuple[int, int]] = []
        self.assertEqual(scan_folder(self.folder, progress=lambda done, total: updates.append((done, total))).documents, [])
        self.assertEqual(updates, [(0, 0)])
        with self.assertRaises(NotADirectoryError):
            scan_folder(self.folder / "missing")


if __name__ == "__main__":
    unittest.main()