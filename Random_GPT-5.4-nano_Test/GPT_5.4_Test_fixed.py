# Original issues found in GPT_5.4_Test.py:
# - The file stops after `self.refresh`, so `_seed_more_samples` is incomplete.
# - Several UI callbacks referenced by buttons and tree events are missing.
# - There is no `__main__` entry point, so running the file exits without launching the app.

import argparse
import csv
import os
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
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
            "created_at": self.created_at,
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
        self.default_csv_path = os.path.join(os.path.dirname(__file__), DEFAULT_CSV_NAME)

        self.tasks = []

        self.filter_var = tk.StringVar(value="all")
        self.search_var = tk.StringVar(value="")
        self.sort_var = tk.StringVar(value="created")

        self._build_style()
        self._build_top_controls()
        self._build_task_entry()
        self._build_table()
        self._build_bottom_controls()

        self._seed_demo_tasks()
        self.refresh_table()

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def _build_style(self):
        style = ttk.Style(self)
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

        row2 = ttk.Frame(frame)
        row2.pack(fill="x", pady=(8, 0))

        filter_box = ttk.LabelFrame(row2, text="Filter", padding=10)
        filter_box.pack(side="left", padx=(0, 10))

        ttk.Radiobutton(
            filter_box,
            text="All",
            variable=self.filter_var,
            value="all",
            command=self.refresh_table,
        ).pack(anchor="w")
        ttk.Radiobutton(
            filter_box,
            text="Open",
            variable=self.filter_var,
            value="open",
            command=self.refresh_table,
        ).pack(anchor="w")
        ttk.Radiobutton(
            filter_box,
            text="Done",
            variable=self.filter_var,
            value="done",
            command=self.refresh_table,
        ).pack(anchor="w")

        search_box = ttk.LabelFrame(row2, text="Search", padding=10)
        search_box.pack(side="left", padx=(0, 10), fill="x", expand=True)

        search_entry = ttk.Entry(search_box, textvariable=self.search_var)
        search_entry.pack(fill="x")

        sort_box = ttk.LabelFrame(row2, text="Sort", padding=10)
        sort_box.pack(side="left")

        ttk.Radiobutton(
            sort_box,
            text="Created",
            variable=self.sort_var,
            value="created",
            command=self.refresh_table,
        ).pack(anchor="w")
        ttk.Radiobutton(
            sort_box,
            text="Title",
            variable=self.sort_var,
            value="title",
            command=self.refresh_table,
        ).pack(anchor="w")

        def on_search_change(*_):
            self.refresh_table()

        self.search_var.trace_add("write", on_search_change)
        search_entry.focus_set()

    def _build_task_entry(self):
        frame = ttk.Frame(self, padding=12)
        frame.pack(fill="x")

        ttk.Label(frame, text="Add a new task:", style="Header.TLabel").pack(anchor="w")

        row = ttk.Frame(frame)
        row.pack(fill="x", pady=(8, 0))

        self.title_entry = ttk.Entry(row)
        self.title_entry.pack(side="left", fill="x", expand=True)
        self.title_entry.bind("<Return>", self.add_task)

        self.add_button = ttk.Button(row, text="Add Task", style="Big.TButton", command=self.add_task)
        self.add_button.pack(side="left", padx=(10, 0))

        quick = ttk.Frame(frame)
        quick.pack(fill="x", pady=(8, 0))

        self.clear_search_btn = ttk.Button(quick, text="Clear Search", command=self.clear_search)
        self.clear_search_btn.pack(side="left")

        self.demo_btn = ttk.Button(quick, text="Add Sample Tasks", command=self._seed_more_samples)
        self.demo_btn.pack(side="left", padx=(10, 0))

        self.remove_done_btn = ttk.Button(quick, text="Remove Done Tasks", command=self.remove_done_tasks)
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

        vsb = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        self.tree.bind("<Double-1>", self.toggle_selected_done)
        self.tree.bind("<<TreeviewSelect>>", self.on_select_changed)

    def _build_bottom_controls(self):
        frame = ttk.Frame(self, padding=12)
        frame.pack(fill="x")

        self.status_label = ttk.Label(frame, text="Ready.")
        self.status_label.pack(side="left")

        right = ttk.Frame(frame)
        right.pack(side="right")

        self.export_button = ttk.Button(right, text="Export CSV", command=self.export_csv)
        self.export_button.pack(side="left", padx=(0, 8))

        self.import_button = ttk.Button(right, text="Import CSV", command=self.import_csv)
        self.import_button.pack(side="left")

    def _seed_demo_tasks(self):
        examples = [
            "Implement stylesheet pipeline",
            "Verify SPA DB generation",
            "Fix edge cases in coversheet templates",
            "Write regression tests",
        ]
        for index, title in enumerate(examples):
            self.tasks.append(Task(title=title, done=(index % 3 == 2)))

    def _seed_more_samples(self):
        templates = [
            "Review publishing workflow",
            "Check accessibility labels (ARIA)",
            "Optimize performance for SPA",
            "Validate PDF generation output",
            "Investigate failing build scripts",
        ]
        for title in templates[:3]:
            self.tasks.append(Task(title=title, done=False))
        self.status_label.config(text="Added sample tasks.")
        self.refresh_table()

    def _filtered_tasks(self):
        items = [task for task in self.tasks if task.matches_search(self.search_var.get())]

        if self.filter_var.get() == "open":
            items = [task for task in items if not task.done]
        elif self.filter_var.get() == "done":
            items = [task for task in items if task.done]

        if self.sort_var.get() == "title":
            items.sort(key=lambda task: (task.title or "").lower())
        else:
            items.sort(key=lambda task: task.created_at)

        return items

    def _selected_task(self):
        selection = self.tree.selection()
        if not selection:
            return None

        selected_id = selection[0]
        for task in self.tasks:
            if task.id == selected_id:
                return task
        return None

    def refresh_table(self):
        for item_id in self.tree.get_children():
            self.tree.delete(item_id)

        visible_tasks = self._filtered_tasks()
        for task in visible_tasks:
            self.tree.insert(
                "",
                "end",
                iid=task.id,
                values=("Yes" if task.done else "No", task.title, task.created_at),
            )

        open_count = sum(1 for task in self.tasks if not task.done)
        done_count = len(self.tasks) - open_count
        self.status_label.config(
            text=f"Showing {len(visible_tasks)} of {len(self.tasks)} tasks | Open: {open_count} | Done: {done_count}"
        )

    def add_task(self, _event=None):
        title = self.title_entry.get().strip()
        if not title:
            messagebox.showwarning(APP_TITLE, "Enter a task title before adding it.")
            return

        self.tasks.append(Task(title=title))
        self.title_entry.delete(0, tk.END)
        self.refresh_table()

    def clear_search(self):
        self.search_var.set("")
        self.refresh_table()

    def remove_done_tasks(self):
        removed = sum(1 for task in self.tasks if task.done)
        if not removed:
            self.status_label.config(text="No completed tasks to remove.")
            return

        self.tasks = [task for task in self.tasks if not task.done]
        self.refresh_table()
        self.status_label.config(text=f"Removed {removed} completed task(s).")

    def toggle_selected_done(self, _event=None):
        task = self._selected_task()
        if task is None:
            return

        task.done = not task.done
        self.refresh_table()
        state = "done" if task.done else "open"
        self.status_label.config(text=f"Marked '{task.title}' as {state}.")

    def on_select_changed(self, _event=None):
        task = self._selected_task()
        if task is None:
            return

        state = "done" if task.done else "open"
        self.status_label.config(text=f"Selected: {task.title} ({state})")

    def export_csv(self):
        save_path = filedialog.asksaveasfilename(
            title="Export tasks",
            defaultextension=".csv",
            initialdir=os.path.dirname(self.default_csv_path),
            initialfile=os.path.basename(self.default_csv_path),
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
        )
        if not save_path:
            return

        with open(save_path, "w", newline="", encoding="utf-8") as file_handle:
            writer = csv.DictWriter(file_handle, fieldnames=["id", "title", "done", "created_at"])
            writer.writeheader()
            writer.writerows(task.to_row() for task in self.tasks)

        self.status_label.config(text=f"Exported {len(self.tasks)} task(s) to {os.path.basename(save_path)}.")

    def import_csv(self):
        open_path = filedialog.askopenfilename(
            title="Import tasks",
            initialdir=os.path.dirname(self.default_csv_path),
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
        )
        if not open_path:
            return

        with open(open_path, newline="", encoding="utf-8") as file_handle:
            reader = csv.DictReader(file_handle)
            self.tasks = [Task.from_row(row) for row in reader]

        self.refresh_table()
        self.status_label.config(text=f"Imported {len(self.tasks)} task(s) from {os.path.basename(open_path)}.")

    def on_close(self):
        self.destroy()


def main():
    parser = argparse.ArgumentParser(description="Run the sample task manager GUI.")
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="Create and tear down the window immediately to validate startup.",
    )
    args = parser.parse_args()

    app = TaskManagerApp()

    if args.self_test:
        app.update_idletasks()
        app.update()
        app.destroy()
        return 0

    app.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())