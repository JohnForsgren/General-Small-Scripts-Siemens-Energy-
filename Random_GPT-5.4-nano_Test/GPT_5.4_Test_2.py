# CRITICAL INSIGHT: THe previous test got truncated (i.e it was blocked from writing out its full message). THis second test allows the Ai tow rite the full message( by breaking it into 2 messages)

'''
CONCLUSION: Impressively, it completed the assignment almost without any errors. This is impressive considering it is a very compact model (Nano)

PRICING: 
If you run the math, here is exactly what it costs to process one A4 document:

GPT-5.4 Nano: $0.0002584 per document (roughly 1/40th of a cent)

GPT-5.4 Mini: $0.0009503 per document (roughly 1/10th of a cent)

If you were to process 10,000 A4 documents, it would cost you just $2.58 on Nano and $9.50 on Mini. Both models are remarkably cheap, but Nano is definitely the choice if cost is your absolute top priority and the tasks are simpler (like basic extraction or routing).

SOURCE: https://gemini.google.com/app/56497fdd4fd899a8  (Gemini 3.1 Pro asked to look up the relevant data and write python scripts)

'''



import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import csv
import os
from datetime import datetime
import uuid


APP_TITLE = "Task Manager (GUI)"


def now_iso():
    """Return an ISO timestamp for stable sorting and storage."""
    return datetime.now().isoformat(timespec="seconds")


class Task:
    """Simple task model for in-memory storage."""

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
    """Main GUI application."""

    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("980x620")

        self.tasks = []  # list[Task]

        self.filter_var = tk.StringVar(value="all")  # all/open/done
        self.search_var = tk.StringVar(value="")
        self.sort_var = tk.StringVar(value="created")  # created/title

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

        ttk.Radiobutton(filter_box, text="All", variable=self.filter_var, value="all",
                        command=self.refresh_table).pack(anchor="w")
        ttk.Radiobutton(filter_box, text="Open", variable=self.filter_var, value="open",
                        command=self.refresh_table).pack(anchor="w")
        ttk.Radiobutton(filter_box, text="Done", variable=self.filter_var, value="done",
                        command=self.refresh_table).pack(anchor="w")

        search_box = ttk.LabelFrame(row2, text="Search", padding=10)
        search_box.pack(side="left", padx=(0, 10), fill="x", expand=True)

        search_entry = ttk.Entry(search_box, textvariable=self.search_var)
        search_entry.pack(fill="x")

        sort_box = ttk.LabelFrame(row2, text="Sort", padding=10)
        sort_box.pack(side="left")

        ttk.Radiobutton(sort_box, text="Created", variable=self.sort_var, value="created",
                        command=self.refresh_table).pack(anchor="w")
        ttk.Radiobutton(sort_box, text="Title", variable=self.sort_var, value="title",
                        command=self.refresh_table).pack(anchor="w")

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

        quick = ttk.Frame(frame)
        quick.pack(fill="x", pady=(8, 0))

        self.clear_search_btn = ttk.Button(quick, text="Clear Search", command=self.clear_search)
        self.clear_search_btn.pack(side="left")

        self.demo_btn = ttk.Button(quick, text="Add Sample Tasks", command=self._seed_more_samples)
        self.demo_btn.pack(side="left", padx=(10, 0))

        self.remove_done_btn = ttk.Button(
            quick, text="Remove Done Tasks", command=self.remove_done_tasks
        )
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
        for i, t in enumerate(examples):
            self.tasks.append(Task(title=t, done=(i % 3 == 2)))

    # -------------------------
    # Continuation starts here
    # -------------------------
    def _seed_more_samples(self):
        templates = [
            "Review publishing workflow",
            "Check accessibility labels (ARIA)",
            "Optimize performance for SPA",
            "Validate PDF generation output",
            "Investigate failing build scripts",
        ]
        # Add only a subset to avoid too many tasks on repeated clicks
        for t in templates[:3]:
            self.tasks.append(Task(title=t, done=False))
        self.status_label.config(text="Added sample tasks.")
        self.refresh_table()


# ---- core UI actions ----
    def add_task(self):
        title = self.title_entry.get().strip()
        if not title:
            messagebox.showwarning("Missing title", "Please enter a task title.")
            return
        self.tasks.append(Task(title=title, done=False))
        self.title_entry.delete(0, tk.END)
        self.status_label.config(text="Task added.")
        self.refresh_table()

    def clear_search(self):
        self.search_var.set("")
        self.status_label.config(text="Search cleared.")
        self.refresh_table()

    def remove_done_tasks(self):
        before = len(self.tasks)
        self.tasks = [t for t in self.tasks if not t.done]
        removed = before - len(self.tasks)
        self.status_label.config(text=f"Removed {removed} done task(s).")
        self.refresh_table()

    def get_selected_task(self):
        """Return the Task instance for the currently selected row, or None."""
        selection = self.tree.selection()
        if not selection:
            return None
        item_id = selection[0]
        # We store the actual task id in the tree item's 'iid' field
        # by inserting with iid=task.id in refresh_table().
        for t in self.tasks:
            if t.id == item_id:
                return t
        return None

    def toggle_selected_done(self, event=None):
        task = self.get_selected_task()
        if task is None:
            self.status_label.config(text="No task selected.")
            return
        task.done = not task.done
        self.status_label.config(text=f"Task marked {'done' if task.done else 'open'}.")
        self.refresh_table(select_task_id=task.id)

    def on_select_changed(self, event=None):
        task = self.get_selected_task()
        if task is None:
            self.status_label.config(text="Ready.")
            return
        self.status_label.config(
            text=f"Selected: {task.title} ({'done' if task.done else 'open'})"
        )

    # ---- table rendering & filtering ----
    def filtered_tasks(self):
        """Apply filter/search; return a list of tasks."""
        f = (self.filter_var.get() or "all").lower()
        s = self.search_var.get() or ""

        if f == "open":
            base = [t for t in self.tasks if not t.done]
        elif f == "done":
            base = [t for t in self.tasks if t.done]
        else:
            base = list(self.tasks)

        base = [t for t in base if t.matches_search(s)]
        return base

    def refresh_table(self, select_task_id=None):
        """Rebuild the tree contents based on current filter/search/sort."""
        # Clear existing rows
        for child in self.tree.get_children():
            self.tree.delete(child)

        items = self.filtered_tasks()

        # Sorting
        sort_mode = (self.sort_var.get() or "created").lower()
        if sort_mode == "title":
            items.sort(key=lambda t: (t.title or "").lower())
        else:
            # created_at is ISO string so lexicographic sort works correctly here
            items.sort(key=lambda t: t.created_at, reverse=True)

        # Insert new rows
        for t in items:
            done_text = "Yes" if t.done else "No"
            self.tree.insert(
                parent="",
                index="end",
                iid=t.id,  # store task id for easy retrieval
                values=(done_text, t.title, t.created_at),
            )

        # Optional selection
        if select_task_id:
            if self.tree.exists(select_task_id):
                self.tree.selection_set(select_task_id)
                self.tree.see(select_task_id)

        self.status_label.config(
            text=f"{len(items)} task(s) shown."
        )

    # ---- CSV import/export ----
    def export_csv(self):
        default_path = os.path.join(os.getcwd(), "tasks.csv")
        path = filedialog.asksaveasfilename(
            title="Export tasks to CSV",
            defaultextension=".csv",
            initialfile=os.path.basename(default_path),
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if not path:
            return

        items = self.filtered_tasks()
        try:
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=["id", "title", "done", "created_at"])
                writer.writeheader()
                for t in items:
                    writer.writerow(t.to_row())
            self.status_label.config(text=f"Exported {len(items)} task(s) to CSV.")
            messagebox.showinfo("Export complete", f"Exported {len(items)} task(s).")
        except Exception as e:
            messagebox.showerror("Export failed", f"Could not export CSV:\n{e}")

    def import_csv(self):
        path = filedialog.askopenfilename(
            title="Import tasks from CSV",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if not path:
            return

        try:
            with open(path, "r", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                required = {"title", "done", "created_at", "id"}
                # We can be forgiving if columns are missing.
                rows = list(reader)

            if not rows:
                messagebox.showwarning("Import", "CSV file is empty or has no rows.")
                return

            imported_count = 0
            seen_ids = {t.id for t in self.tasks}

            for row in rows:
                # Skip blank titles
                title = (row.get("title") or "").strip()
                if not title:
                    continue

                # If CSV lacks id, create one; if it has id, de-duplicate.
                task_id = (row.get("id") or "").strip() or None
                if task_id and task_id in seen_ids:
                    # De-dup policy: skip existing id
                    continue

                t = Task.from_row(row)
                if task_id:
                    t.id = task_id
                self.tasks.append(t)
                imported_count += 1
                if t.id not in seen_ids:
                    seen_ids.add(t.id)

            self.status_label.config(text=f"Imported {imported_count} task(s) from CSV.")
            messagebox.showinfo("Import complete", f"Imported {imported_count} task(s).")
            self.refresh_table()
        except FileNotFoundError:
            messagebox.showerror("Import failed", "File not found.")
        except Exception as e:
            messagebox.showerror("Import failed", f"Could not import CSV:\n{e}")

    # ---- window lifecycle ----
    def on_close(self):
        # No persistent storage in this script; just confirm.
        if messagebox.askyesno("Exit", "Do you want to close the Task Manager?"):
            self.destroy()


if __name__ == "__main__":
    app = TaskManagerApp()
    app.mainloop()