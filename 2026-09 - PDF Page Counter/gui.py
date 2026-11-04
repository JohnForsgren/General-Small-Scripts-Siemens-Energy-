"""Small desktop window for counting PDF pages."""

from __future__ import annotations

import queue
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from PIL import ImageTk

from counter import Report, export_csv, scan_folder
from icon_art import render_icon


class CounterApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Document page counter")
        self.icon = ImageTk.PhotoImage(render_icon(64), master=root)
        self.root.iconphoto(True, self.icon)
        self.root.geometry("880x600")
        self.root.minsize(650, 420)
        self.root.configure(bg="#f2f5f9")
        self.folder = tk.StringVar()
        self.recursive = tk.BooleanVar(value=True)
        self.status = tk.StringVar(value="Choose a folder to get started.")
        self.progress_title = tk.StringVar(value="Finding documents…")
        self.progress_percent = tk.StringVar(value="…")
        self.count = tk.StringVar(value="—")
        self.pages = tk.StringVar(value="—")
        self.subtitle = tk.StringVar(value="PDF and DOCX documents")
        self.page_subtitle = tk.StringVar(value="PDF pages only")
        self.messages: queue.Queue[tuple[str, object]] = queue.Queue()
        self.report: Report | None = None
        self.details_open = False
        self._build()

    def _build(self) -> None:
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Details.Treeview", rowheight=29, background="white", fieldbackground="white", foreground="#23324a", borderwidth=0, font=("Segoe UI", 10))
        style.configure("Details.Treeview.Heading", font=("Segoe UI", 10, "bold"), background="#e7edf5", foreground="#24344b", padding=(10, 8))
        style.map("Details.Treeview", background=[("selected", "#dbeafe")], foreground=[("selected", "#152d50")])
        style.configure("Scan.Horizontal.TProgressbar", background="#168aab", troughcolor="#dce7f1", borderwidth=0, thickness=18)

        main = tk.Frame(self.root, bg="#f2f5f9", padx=30, pady=22)
        main.pack(fill="both", expand=True)
        tk.Label(main, text="Document page counter", bg="#f2f5f9", fg="#15243c", font=("Segoe UI", 22, "bold")).pack(anchor="w")
        tk.Label(main, text="A quick overview of the documents in a folder", bg="#f2f5f9", fg="#617085", font=("Segoe UI", 11)).pack(anchor="w", pady=(2, 20))

        picker = tk.Frame(main, bg="#f2f5f9")
        picker.pack(fill="x")
        self.entry = ttk.Entry(picker, textvariable=self.folder, font=("Segoe UI", 11))
        self.entry.pack(side="left", fill="x", expand=True, ipady=7)
        ttk.Button(picker, text="Browse…", command=self.browse).pack(side="left", padx=(10, 0), ipady=4)
        self.scan_button = ttk.Button(picker, text="Count pages", command=self.scan)
        self.scan_button.pack(side="left", padx=(10, 0), ipady=4)
        self.subfolders_button = tk.Checkbutton(
            main, variable=self.recursive, command=self._update_scope_button,
            indicatoron=False, font=("Segoe UI", 13, "bold"),
            bg="white", fg="#174893", selectcolor="#dceeff",
            activebackground="#dceeff", activeforeground="#174893",
            relief="solid", bd=1, padx=15, pady=9,
        )
        self.subfolders_button.pack(anchor="w", pady=(12, 18))
        self._update_scope_button()

        self.progress_panel = tk.Frame(main, bg="white", padx=20, pady=15, highlightbackground="#d6e5f0", highlightthickness=1)
        progress_header = tk.Frame(self.progress_panel, bg="white")
        progress_header.pack(fill="x", pady=(0, 10))
        tk.Label(progress_header, textvariable=self.progress_title, bg="white", fg="#193c68", font=("Segoe UI", 12, "bold")).pack(side="left")
        tk.Label(progress_header, textvariable=self.progress_percent, bg="white", fg="#136886", font=("Segoe UI", 16, "bold")).pack(side="right")
        self.progress_bar = ttk.Progressbar(self.progress_panel, style="Scan.Horizontal.TProgressbar", maximum=100, value=0)
        self.progress_bar.pack(fill="x")

        self.cards = tk.Frame(main, bg="#f2f5f9")
        self.cards.pack(fill="x")
        self._card(self.cards, "DOCUMENTS", self.count, self.subtitle).pack(side="left", fill="x", expand=True, padx=(0, 9))
        self._card(self.cards, "TOTAL PAGES", self.pages, self.page_subtitle).pack(side="left", fill="x", expand=True, padx=(9, 0))

        bar = tk.Frame(main, bg="#f2f5f9")
        bar.pack(fill="x", pady=(19, 6))
        self.details_button = ttk.Button(bar, text="Show document details ▾", command=self.toggle_details)
        self.details_button.pack(side="left")
        self.export_button = ttk.Button(bar, text="Export CSV", command=self.export, state="disabled")
        self.export_button.pack(side="right")

        self.detail_frame = tk.Frame(main, bg="white")
        self.tree = ttk.Treeview(self.detail_frame, columns=("name", "type", "size", "pages", "note"), show="headings", style="Details.Treeview")
        for column, heading, width, anchor in [
            ("name", "Document", 320, "w"), ("type", "Type", 65, "center"),
            ("size", "Size", 95, "e"), ("pages", "Pages", 70, "e"), ("note", "Note", 245, "w"),
        ]:
            self.tree.heading(column, text=heading)
            self.tree.column(column, width=width, minwidth=55, anchor=anchor, stretch=column in ("name", "note"))
        scroll = ttk.Scrollbar(self.detail_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        tk.Label(main, textvariable=self.status, bg="#f2f5f9", fg="#617085", font=("Segoe UI", 10), anchor="w", wraplength=780).pack(side="bottom", fill="x", pady=(12, 0))

    def _card(self, parent: tk.Widget, title: str, value: tk.StringVar, caption: tk.StringVar) -> tk.Frame:
        card = tk.Frame(parent, bg="white", padx=23, pady=17, highlightbackground="#e1e8f1", highlightthickness=1)
        tk.Label(card, text=title, bg="white", fg="#566c89", font=("Segoe UI", 10, "bold")).pack(anchor="w")
        tk.Label(card, textvariable=value, bg="white", fg="#174893", font=("Segoe UI", 34, "bold")).pack(anchor="w", pady=(3, 0))
        tk.Label(card, textvariable=caption, bg="white", fg="#617085", font=("Segoe UI", 10)).pack(anchor="w")
        return card

    def _update_scope_button(self) -> None:
        self.subfolders_button.configure(text="✓  Include subfolders" if self.recursive.get() else "○  Include subfolders")

    def browse(self) -> None:
        selected = filedialog.askdirectory(title="Select document folder", initialdir=self.folder.get() if Path(self.folder.get()).is_dir() else None)
        if selected:
            self.folder.set(selected)
            self.scan()

    def scan(self) -> None:
        folder = Path(self.folder.get().strip().strip('"'))
        if not self.folder.get().strip() or not folder.is_dir():
            messagebox.showerror("Folder not found", "Choose an existing folder first.")
            return
        self.report = None
        self.export_button.configure(state="disabled")
        self.scan_button.configure(state="disabled")
        self.count.set("…")
        self.pages.set("…")
        self.status.set("Counting pages…")
        self.progress_title.set("Finding documents…")
        self.progress_percent.set("…")
        self.progress_bar.configure(mode="indeterminate", value=0)
        self.progress_panel.pack(fill="x", pady=(0, 18), before=self.cards)
        self.progress_bar.start(12)
        recursive = self.recursive.get()

        def worker() -> None:
            try:
                result = scan_folder(folder, recursive, lambda done, total: self.messages.put(("progress", (done, total))))
                self.messages.put(("done", result))
            except Exception as exc:
                self.messages.put(("error", exc))

        threading.Thread(target=worker, daemon=True).start()
        self.root.after(100, self._poll)

    def _poll(self) -> None:
        try:
            for _ in range(100):
                kind, data = self.messages.get_nowait()
                if kind == "progress":
                    done, total = data
                    self.progress_bar.stop()
                    self.progress_bar.configure(mode="determinate", value=round(100 * done / total) if total else 0)
                    self.progress_percent.set(f"{round(100 * done / total) if total else 0}%")
                    self.progress_title.set(f"Reading documents: {done:,} of {total:,}")
                    self.status.set(f"Reading document {done:,} of {total:,}…")
                elif kind == "done":
                    self._show_report(data)
                    return
                else:
                    self.progress_bar.stop()
                    self.progress_bar.configure(mode="determinate", value=0)
                    self.progress_title.set("Scan failed")
                    self.progress_percent.set("—")
                    self.scan_button.configure(state="normal")
                    self.count.set("—")
                    self.pages.set("—")
                    self.status.set(f"Scan failed: {data}")
                    return
        except queue.Empty:
            self.root.after(100, self._poll)
        else:
            self.root.after(30, self._poll)

    def _show_report(self, report: Report) -> None:
        self.report = report
        self.progress_bar.stop()
        self.progress_bar.configure(mode="determinate", value=100)
        self.progress_percent.set("100%")
        self.progress_title.set(f"Complete: {len(report.documents):,} documents")
        self.count.set(f"{len(report.documents):,}")
        self.pages.set(f"{report.pdf_pages:,}" + ("+" if report.failed_count else ""))
        self.subtitle.set(f"{report.pdf_count} PDF · {report.docx_count} DOCX")
        self.page_subtitle.set("PDF pages only" + (" · incomplete" if report.failed_count else ""))
        self.scan_button.configure(state="normal")
        self.export_button.configure(state="normal")
        self.status.set(f"Finished · {report.folder}" + (f" · {report.failed_count} PDF(s) unreadable; see details" if report.failed_count else ""))
        self.tree.delete(*self.tree.get_children())
        for doc in report.documents:
            self.tree.insert("", "end", values=(doc.name, doc.kind, f"{doc.size / 1024:,.1f} KB", doc.pages if doc.pages is not None else "—", doc.note))

    def toggle_details(self) -> None:
        self.details_open = not self.details_open
        if self.details_open:
            self.detail_frame.pack(fill="both", expand=True, pady=(3, 0))
            self.details_button.configure(text="Hide document details ▴")
        else:
            self.detail_frame.pack_forget()
            self.details_button.configure(text="Show document details ▾")

    def export(self) -> None:
        if self.report is None:
            return
        destination = filedialog.asksaveasfilename(title="Save document list", defaultextension=".csv", filetypes=[("CSV files", "*.csv")], initialfile="document-pages.csv")
        if destination:
            try:
                export_csv(self.report, Path(destination))
                self.status.set(f"Saved document list to {destination}")
            except OSError as exc:
                messagebox.showerror("Could not save CSV", str(exc))


def main() -> None:
    root = tk.Tk()
    CounterApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()