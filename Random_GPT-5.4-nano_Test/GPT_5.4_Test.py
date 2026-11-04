## File purpose: This was just a random file written by gpt-5.4-nano to test its intelligence. 

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import csv
import os
from datetime import datetime
import uuid


APP_TITLE = "Task Manager (GUI)"
DEFAULT_CSV_NAME = "tasks.csv"


def now_iso():
    """Return an ISO timestamp for stable sorting and storage."""
    return datetime.now().isoformat(timespec="seconds")


class Task:
    """
    A simple in-memory model for tasks.
    """
    def __init__(self, title, done=False, created_at=None, task_id=None):
        self.id = task_id or str(uuid.uuid4())
        self.title = title
        self.done = bool(done)
        self.created_at = created_at or now_iso()

    def matches_search(self, query: str) -> bool:
        q = (query or "").strip().lower()
        if not q:
            return True
        return q in (self.title or "").lower()

    def to_row(self):
        return {
            "id": self.id,
            "title": self.title,
            "done": "1" if self.done else "0",
            "created_at": self.created_at
        }

    @staticmethod
    def from_row(row):
        task_id = row.get("id") or str(uuid.uuid4())
        title = row.get("title", "")
        done_str = (row.get("done", "0")).strip()
        done = done_str in ("1", "true", "TRUE", "yes", "YES", "y", "Y")
        created_at = row.get("created_at") or now_iso()
        return Task(title=title, done=done, created_at=created_at, task_id=task_id)


class TaskManagerApp(tk.Tk):
    """
    Main GUI application.
    """
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("980x620")

        # Core state
        self.tasks = []  # list[Task]

        # UI State variables
        self.filter_var = tk.StringVar(value="all")  # all/open/done
        self.search_var = tk.StringVar(value="")
        self.sort_var = tk.StringVar(value="created")  # created/title

        # Layout
        self._build_style()
        self._build_top_controls()
        self._build_task_entry()
        self._build_table()
        self._build_bottom_controls()

        # Initial population
        self._seed_demo_tasks()
        self.refresh_table()

        # Window close handler
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def _build_style(self):
        style = ttk.Style(self)
        # Use a platform theme if available.
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure("Header.TLabel", font=("Segoe UI", 13, "bold"))
        style.configure("Big.TButton", padding=(10, 6))

    def _build_top_controls(self):
        frame = ttk.Frame(self, padding=12)
        frame.pack(fill="x")

        ttk.Label(frame, text="Task Manager", style="Header.TLabel").pack(anchor="w")

        # Row 2: Filter / Search / Sort
        row2 = ttk.Frame(frame)
        row2.pack(fill="x", pady=(8, 0))

        # Filter
        filter_box = ttk.LabelFrame(row2, text="Filter", padding=10)
        filter_box.pack(side="left", padx=(0, 10))

        ttk.Radiobutton(filter_box, text="All", variable=self.filter_var, value="all",
                        command=self.refresh_table).pack(anchor="w")
        ttk.Radiobutton(filter_box, text="Open", variable=self.filter_var, value="open",
                        command=self.refresh_table).pack(anchor="w")
        ttk.Radiobutton(filter_box, text="Done", variable=self.filter_var, value="done",
                        command=self.refresh_table).pack(anchor="w")

        # Search
        search_box = ttk.LabelFrame(row2, text="Search", padding=10)
        search_box.pack(side="left", padx=(0, 10), fill="x", expand=True)

        search_entry = ttk.Entry(search_box, textvariable=self.search_var)
        search_entry.pack(fill="x")

        # Sort
        sort_box = ttk.LabelFrame(row2, text="Sort", padding=10)
        sort_box.pack(side="left")

        ttk.Radiobutton(sort_box, text="Created", variable=self.sort_var, value="created",
                        command=self.refresh_table).pack(anchor="w")
        ttk.Radiobutton(sort_box, text="Title", variable=self.sort_var, value="title",
                        command=self.refresh_table).pack(anchor="w")

        # Live search
        def on_search_change(*_):
            self.refresh_table()

        self.search_var.trace_add("write", on_search_change)

    def _build_task_entry(self):
        frame = ttk.Frame(self, padding=12)
        frame.pack(fill="x")

        ttk.Label(frame, text="Add a new task:", style="Header.TLabel").pack(anchor="w")

        row = ttk.Frame(frame)
        row.pack(fill="x", pady=(8, 0))

        self.title_entry = ttk.Entry(row)
        self.title_entry.pack(side="left", fill="x", expand=True)

        self.add_button = ttk.Button(row, text="Add Task", style="Big.TButton",
                                     command=self.add_task)
        self.add_button.pack(side="left", padx=(10, 0))

        # Quick actions
        quick = ttk.Frame(frame)
        quick.pack(fill="x", pady=(8, 0))

        self.clear_search_btn = ttk.Button(quick, text="Clear Search",
                                           command=self.clear_search)
        self.clear_search_btn.pack(side="left")

        self.demo_btn = ttk.Button(quick, text="Add Sample Tasks",
                                    command=self._seed_more_samples)
        self.demo_btn.pack(side="left", padx=(10, 0))

        self.remove_done_btn = ttk.Button(quick, text="Remove Done Tasks",
                                           command=self.remove_done_tasks)
        self.remove_done_btn.pack(side="left", padx=(10, 0))

    def _build_table(self):
        frame = ttk.Frame(self, padding=12)
        frame.pack(fill="both", expand=True)

        columns = ("done", "title", "created_at")
        self.tree = ttk.Treeview(frame, columns=columns, show="headings", selectmode="browse")

        self.tree.heading("done", text="Done")
        self.tree.heading("title", text="Title")
        self.tree.heading("created_at", text="Created At")

        self.tree.column("done", width=70, anchor="center")
        self.tree.column("title", width=540, anchor="w")
        self.tree.column("created_at", width=260, anchor="w")

        # Scrollbars
        vsb = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        # Bind double click to toggle done
        self.tree.bind("<Double-1>", self.toggle_selected_done)

        # Context: single click updates selection labels or actions
        self.tree.bind("<<TreeviewSelect>>", self.on_select_changed)

    def _build_bottom_controls(self):
        frame = ttk.Frame(self, padding=12)
        frame.pack(fill="x")

        # Info label
        self.status_label = ttk.Label(frame, text="Ready.")
        self.status_label.pack(side="left")

        # Export / Import
        right = ttk.Frame(frame)
        right.pack(side="right")

        self.export_button = ttk.Button(right, text="Export CSV",
                                        command=self.export_csv)
        self.export_button.pack(side="left", padx=(0, 8))

        self.import_button = ttk.Button(right, text="Import CSV",
                                        command=self.import_csv)
        self.import_button.pack(side="left")

    def _seed_demo_tasks(self):
        examples = [
            "Implement stylesheet pipeline",
            "Verify SPA DB generation",
            "Fix edge cases in coversheet templates",
            "Write regression tests",
        ]
        for i, t in enumerate(examples):
            self.tasks.append(Task(title=t, done=(i % 3 == 2)))

    def _seed_more_samples(self):
        # Add some more tasks without clearing current ones.
        templates = [
            "Review publishing workflow",
            "Check accessibility labels (ARIA)",
            "Optimize performance for SPA",
            "Validate PDF generation output",
            "Investigate failing build scripts",
        ]
        for t in templates[:3]:
            self.tasks.append(Task(title=t, done=False))
        self.status_label.config(text="Added sample tasks.")
        self.refresh