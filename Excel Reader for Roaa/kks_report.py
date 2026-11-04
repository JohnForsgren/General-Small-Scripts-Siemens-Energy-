from __future__ import annotations

import argparse
import html
import math
import sys
import warnings
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import pandas as pd
import plotly.graph_objects as go
from openpyxl import load_workbook
from plotly.subplots import make_subplots


REQUIRED_COLUMNS = ("Type", "Item ID", "Version", "Title", "TC KKS")
DOCUMENT_TYPE = "document"


@dataclass(frozen=True)
class ReportPaths:
    output_dir: Path
    excel_path: Path
    dashboard_path: Path


def is_missing(value: object) -> bool:
    if value is None:
        return True
    if isinstance(value, float) and math.isnan(value):
        return True
    return str(value).strip() == ""


def clean_value(value: object) -> str:
    if is_missing(value):
        return ""
    return str(value).strip()


def normalize_header(value: object) -> str:
    return str(value).strip().casefold() if value is not None else ""


def find_columns(header: Iterable[object]) -> dict[str, int]:
    normalized = {normalize_header(value): index for index, value in enumerate(header)}
    columns: dict[str, int] = {}
    missing_columns: list[str] = []

    for column in REQUIRED_COLUMNS:
        key = column.casefold()
        if key in normalized:
            columns[column] = normalized[key]
        else:
            missing_columns.append(column)

    if missing_columns:
        raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")

    return columns


def iter_excel_files(input_dir: Path) -> list[Path]:
    return sorted(
        path
        for path in input_dir.glob("*.xlsx")
        if not path.name.startswith("~$") and path.is_file()
    )


def analyze_workbook(path: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", message="Workbook contains no default style.*", category=UserWarning)
        workbook = load_workbook(path, read_only=True, data_only=True)

    for worksheet in workbook.worksheets:
        row_iterator = worksheet.iter_rows(values_only=True)
        try:
            header = next(row_iterator)
        except StopIteration:
            continue

        try:
            columns = find_columns(header)
        except ValueError as error:
            print(f"Skipping {path.name} / {worksheet.title}: {error}", file=sys.stderr)
            continue

        for excel_row_number, row in enumerate(row_iterator, start=2):
            type_value = clean_value(row[columns["Type"]] if columns["Type"] < len(row) else None)
            if type_value.casefold() != DOCUMENT_TYPE:
                continue

            tc_kks_value = row[columns["TC KKS"]] if columns["TC KKS"] < len(row) else None
            status = "Missing TC KKS" if is_missing(tc_kks_value) else "Has TC KKS"

            rows.append(
                {
                    "Source File": path.name,
                    "Sheet": worksheet.title,
                    "Excel Row": excel_row_number,
                    "Type": type_value,
                    "Item ID": clean_value(row[columns["Item ID"]] if columns["Item ID"] < len(row) else None),
                    "Version": clean_value(row[columns["Version"]] if columns["Version"] < len(row) else None),
                    "Title": clean_value(row[columns["Title"]] if columns["Title"] < len(row) else None),
                    "TC KKS": clean_value(tc_kks_value),
                    "TC KKS Status": status,
                    "Missing TC KKS": status == "Missing TC KKS",
                }
            )

    workbook.close()
    return rows


def analyze_folder(input_dir: Path) -> pd.DataFrame:
    files = iter_excel_files(input_dir)
    if not files:
        raise FileNotFoundError(f"No .xlsx files found in {input_dir}")

    rows: list[dict[str, object]] = []
    for path in files:
        rows.extend(analyze_workbook(path))

    if not rows:
        raise ValueError("No document rows were found in the input Excel files.")

    return pd.DataFrame(rows)


def build_file_summary(documents: pd.DataFrame) -> pd.DataFrame:
    summary = (
        documents.groupby("Source File", as_index=False)
        .agg(
            Total_Documents=("Item ID", "count"),
            Missing_TC_KKS=("Missing TC KKS", "sum"),
        )
        .rename(columns={"Total_Documents": "Total Documents", "Missing_TC_KKS": "Missing TC KKS"})
    )
    summary["Has TC KKS"] = summary["Total Documents"] - summary["Missing TC KKS"]
    summary["Missing %"] = (summary["Missing TC KKS"] / summary["Total Documents"]).round(4)
    summary["Present %"] = (summary["Has TC KKS"] / summary["Total Documents"]).round(4)
    return summary.sort_values(["Missing %", "Missing TC KKS", "Source File"], ascending=[False, False, True])


def build_sheet_summary(documents: pd.DataFrame) -> pd.DataFrame:
    summary = (
        documents.groupby(["Source File", "Sheet"], as_index=False)
        .agg(
            Total_Documents=("Item ID", "count"),
            Missing_TC_KKS=("Missing TC KKS", "sum"),
        )
        .rename(columns={"Total_Documents": "Total Documents", "Missing_TC_KKS": "Missing TC KKS"})
    )
    summary["Has TC KKS"] = summary["Total Documents"] - summary["Missing TC KKS"]
    summary["Missing %"] = (summary["Missing TC KKS"] / summary["Total Documents"]).round(4)
    return summary.sort_values(["Source File", "Sheet"])


def build_overall_summary(file_summary: pd.DataFrame) -> pd.DataFrame:
    total_documents = int(file_summary["Total Documents"].sum())
    missing = int(file_summary["Missing TC KKS"].sum())
    present = int(file_summary["Has TC KKS"].sum())
    missing_percent = missing / total_documents if total_documents else 0

    return pd.DataFrame(
        [
            {"Metric": "Excel files analyzed", "Value": int(file_summary.shape[0])},
            {"Metric": "Total documents", "Value": total_documents},
            {"Metric": "Documents missing TC KKS", "Value": missing},
            {"Metric": "Documents with TC KKS", "Value": present},
            {"Metric": "Overall missing %", "Value": missing_percent},
        ]
    )


def write_excel_report(
    documents: pd.DataFrame,
    file_summary: pd.DataFrame,
    sheet_summary: pd.DataFrame,
    overall_summary: pd.DataFrame,
    output_path: Path,
) -> None:
    missing_documents = documents[documents["Missing TC KKS"]].copy()
    all_documents = documents.drop(columns=["Missing TC KKS"])

    with pd.ExcelWriter(output_path, engine="xlsxwriter") as writer:
        overall_summary.to_excel(writer, sheet_name="Overall Summary", index=False)
        file_summary.to_excel(writer, sheet_name="File Summary", index=False)
        sheet_summary.to_excel(writer, sheet_name="Sheet Summary", index=False)
        missing_documents.drop(columns=["Missing TC KKS"]).to_excel(writer, sheet_name="Missing Documents", index=False)
        all_documents.to_excel(writer, sheet_name="All Documents", index=False)

        workbook = writer.book
        header_format = workbook.add_format({"bold": True, "bg_color": "#1F4E78", "font_color": "white", "border": 1})
        percent_format = workbook.add_format({"num_format": "0.0%"})
        integer_format = workbook.add_format({"num_format": "#,##0"})
        title_format = workbook.add_format({"bold": True, "font_size": 14, "font_color": "#1F4E78"})

        for sheet_name, dataframe in {
            "Overall Summary": overall_summary,
            "File Summary": file_summary,
            "Sheet Summary": sheet_summary,
            "Missing Documents": missing_documents.drop(columns=["Missing TC KKS"]),
            "All Documents": all_documents,
        }.items():
            worksheet = writer.sheets[sheet_name]
            worksheet.freeze_panes(1, 0)
            worksheet.autofilter(0, 0, len(dataframe), max(len(dataframe.columns) - 1, 0))
            for column_number, column_name in enumerate(dataframe.columns):
                worksheet.write(0, column_number, column_name, header_format)
                width = min(max(len(str(column_name)), 12), 55)
                if not dataframe.empty:
                    width = min(max(width, int(dataframe[column_name].astype(str).str.len().quantile(0.95)) + 2), 70)
                worksheet.set_column(column_number, column_number, width)

        writer.sheets["Overall Summary"].set_column("B:B", 18, integer_format)
        writer.sheets["Overall Summary"].write_number("B6", float(overall_summary.loc[overall_summary["Metric"] == "Overall missing %", "Value"].iloc[0]), percent_format)
        for sheet_name in ("File Summary", "Sheet Summary"):
            worksheet = writer.sheets[sheet_name]
            worksheet.set_column("B:D", 16, integer_format)
            worksheet.set_column("E:F", 12, percent_format)

        dashboard = workbook.add_worksheet("Dashboard")
        dashboard.write("A1", "KKS TC Coverage Dashboard", title_format)
        dashboard.write("A3", "Total documents")
        dashboard.write("B3", int(file_summary["Total Documents"].sum()), integer_format)
        dashboard.write("A4", "Missing TC KKS")
        dashboard.write("B4", int(file_summary["Missing TC KKS"].sum()), integer_format)
        dashboard.write("A5", "Overall missing %")
        dashboard.write("B5", float(file_summary["Missing TC KKS"].sum() / file_summary["Total Documents"].sum()), percent_format)

        chart = workbook.add_chart({"type": "column"})
        chart.add_series(
            {
                "name": "Missing TC KKS",
                "categories": "='File Summary'!$A$2:$A$" + str(len(file_summary) + 1),
                "values": "='File Summary'!$C$2:$C$" + str(len(file_summary) + 1),
                "fill": {"color": "#C00000"},
            }
        )
        chart.set_title({"name": "Missing TC KKS by file"})
        chart.set_x_axis({"name": "File"})
        chart.set_y_axis({"name": "Documents"})
        chart.set_legend({"none": True})
        dashboard.insert_chart("D2", chart, {"x_scale": 1.8, "y_scale": 1.25})

        pie = workbook.add_chart({"type": "doughnut"})
        dashboard.write_row("A8", ["Status", "Documents"], header_format)
        dashboard.write_row("A9", ["Has TC KKS", int(file_summary["Has TC KKS"].sum())])
        dashboard.write_row("A10", ["Missing TC KKS", int(file_summary["Missing TC KKS"].sum())])
        pie.add_series(
            {
                "categories": "=Dashboard!$A$9:$A$10",
                "values": "=Dashboard!$B$9:$B$10",
                "points": [{"fill": {"color": "#2E75B6"}}, {"fill": {"color": "#C00000"}}],
            }
        )
        pie.set_title({"name": "Overall TC KKS status"})
        dashboard.insert_chart("D23", pie, {"x_scale": 1.2, "y_scale": 1.2})


def format_percent(value: float) -> str:
    return f"{value:.1%}"


def create_figure(file_summary: pd.DataFrame) -> go.Figure:
    sorted_summary = file_summary.sort_values("Missing %", ascending=False)
    figure = make_subplots(
        rows=2,
        cols=2,
        specs=[[{"type": "bar"}, {"type": "domain"}], [{"type": "bar", "colspan": 2}, None]],
        subplot_titles=("Missing TC KKS by file", "Overall status", "Missing percentage by file"),
        vertical_spacing=0.16,
        horizontal_spacing=0.12,
    )

    figure.add_trace(
        go.Bar(
            x=sorted_summary["Source File"],
            y=sorted_summary["Missing TC KKS"],
            marker_color="#C43B3B",
            hovertemplate="%{x}<br>Missing: %{y}<extra></extra>",
        ),
        row=1,
        col=1,
    )
    figure.add_trace(
        go.Pie(
            labels=["Has TC KKS", "Missing TC KKS"],
            values=[int(file_summary["Has TC KKS"].sum()), int(file_summary["Missing TC KKS"].sum())],
            hole=0.58,
            marker_colors=["#2F7D6D", "#C43B3B"],
            textinfo="label+percent",
        ),
        row=1,
        col=2,
    )
    figure.add_trace(
        go.Bar(
            x=sorted_summary["Source File"],
            y=sorted_summary["Missing %"],
            marker_color="#D98C2B",
            hovertemplate="%{x}<br>Missing: %{y:.1%}<extra></extra>",
        ),
        row=2,
        col=1,
    )
    figure.update_yaxes(title_text="Missing documents", row=1, col=1)
    figure.update_yaxes(title_text="Missing %", tickformat=".0%", range=[0, 1], row=2, col=1)
    figure.update_xaxes(tickangle=35)
    figure.update_layout(
        height=850,
        margin={"t": 55, "r": 24, "b": 110, "l": 70},
        paper_bgcolor="white",
        plot_bgcolor="white",
        showlegend=False,
        font={"family": "Segoe UI, Arial, sans-serif", "size": 12, "color": "#1F2933"},
    )
    return figure


def build_missing_table(missing_documents: pd.DataFrame, limit: int = 250) -> str:
    rows = []
    display_columns = ["Source File", "Sheet", "Excel Row", "Item ID", "Version", "Title"]
    for _, row in missing_documents.head(limit).iterrows():
        cells = "".join(f"<td>{html.escape(str(row[column]))}</td>" for column in display_columns)
        rows.append(f"<tr>{cells}</tr>")
    header = "".join(f"<th>{html.escape(column)}</th>" for column in display_columns)
    note = "" if len(missing_documents) <= limit else f"<p class='note'>Showing first {limit:,} of {len(missing_documents):,} missing documents. Full list is in the Excel output.</p>"
    return f"<table><thead><tr>{header}</tr></thead><tbody>{''.join(rows)}</tbody></table>{note}"


def write_dashboard(file_summary: pd.DataFrame, documents: pd.DataFrame, output_path: Path) -> None:
    total_documents = int(file_summary["Total Documents"].sum())
    missing = int(file_summary["Missing TC KKS"].sum())
    present = int(file_summary["Has TC KKS"].sum())
    missing_percent = missing / total_documents if total_documents else 0
    worst_file = file_summary.sort_values(["Missing %", "Missing TC KKS"], ascending=False).iloc[0]
    figure_html = create_figure(file_summary).to_html(full_html=False, include_plotlyjs="inline")
    missing_table = build_missing_table(documents[documents["Missing TC KKS"]])

    file_rows = []
    for _, row in file_summary.sort_values("Missing %", ascending=False).iterrows():
        file_rows.append(
            "<tr>"
            f"<td>{html.escape(str(row['Source File']))}</td>"
            f"<td>{int(row['Total Documents']):,}</td>"
            f"<td>{int(row['Missing TC KKS']):,}</td>"
            f"<td>{int(row['Has TC KKS']):,}</td>"
            f"<td>{format_percent(float(row['Missing %']))}</td>"
            "</tr>"
        )

    output_path.write_text(
        f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>KKS TC Coverage Dashboard</title>
  <style>
    :root {{
      --ink: #17212b;
      --muted: #5b6773;
      --line: #d9e1e8;
      --panel: #ffffff;
      --page: #f4f7fa;
      --accent: #2f7d6d;
      --warn: #c43b3b;
      --gold: #d98c2b;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      color: var(--ink);
      background: var(--page);
      font-family: Segoe UI, Arial, sans-serif;
    }}
    header {{
      background: #ffffff;
      border-bottom: 1px solid var(--line);
      padding: 28px 36px 22px;
    }}
    h1 {{ margin: 0 0 6px; font-size: 28px; letter-spacing: 0; }}
    h2 {{ margin: 0 0 14px; font-size: 18px; letter-spacing: 0; }}
    .subtitle {{ color: var(--muted); margin: 0; }}
    main {{ padding: 24px 36px 42px; max-width: 1440px; margin: 0 auto; }}
    .kpis {{ display: grid; grid-template-columns: repeat(4, minmax(160px, 1fr)); gap: 14px; margin-bottom: 20px; }}
    .kpi {{ background: var(--panel); border: 1px solid var(--line); border-radius: 8px; padding: 16px; }}
    .label {{ color: var(--muted); font-size: 13px; margin-bottom: 8px; }}
    .value {{ font-size: 28px; font-weight: 700; }}
    .value.warn {{ color: var(--warn); }}
    .value.accent {{ color: var(--accent); }}
    section {{ background: var(--panel); border: 1px solid var(--line); border-radius: 8px; padding: 18px; margin-top: 18px; }}
    table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
    th, td {{ padding: 9px 10px; border-bottom: 1px solid var(--line); text-align: left; vertical-align: top; }}
    th {{ background: #eef3f7; font-weight: 700; }}
    tr:hover td {{ background: #f8fafc; }}
    .note {{ color: var(--muted); font-size: 13px; margin-bottom: 0; }}
    @media (max-width: 900px) {{
      header, main {{ padding-left: 18px; padding-right: 18px; }}
      .kpis {{ grid-template-columns: repeat(2, minmax(140px, 1fr)); }}
    }}
  </style>
</head>
<body>
  <header>
    <h1>KKS TC Coverage Dashboard</h1>
    <p class="subtitle">Document rows analyzed across uploaded Excel files. Missing TC KKS values are highlighted for follow-up.</p>
  </header>
  <main>
    <div class="kpis">
      <div class="kpi"><div class="label">Excel files</div><div class="value">{len(file_summary):,}</div></div>
      <div class="kpi"><div class="label">Total documents</div><div class="value accent">{total_documents:,}</div></div>
      <div class="kpi"><div class="label">Missing TC KKS</div><div class="value warn">{missing:,}</div></div>
      <div class="kpi"><div class="label">Overall missing</div><div class="value warn">{format_percent(missing_percent)}</div></div>
    </div>
    <section>
      <h2>Executive View</h2>
      <p class="note">Highest missing rate: {html.escape(str(worst_file['Source File']))} ({format_percent(float(worst_file['Missing %']))}). Documents with TC KKS: {present:,}.</p>
      {figure_html}
    </section>
    <section>
      <h2>File Summary</h2>
      <table>
        <thead><tr><th>Source File</th><th>Total Documents</th><th>Missing TC KKS</th><th>Has TC KKS</th><th>Missing %</th></tr></thead>
        <tbody>{''.join(file_rows)}</tbody>
      </table>
    </section>
    <section>
      <h2>Missing Documents</h2>
      {missing_table}
    </section>
  </main>
</body>
</html>
""",
        encoding="utf-8",
    )


def resolve_report_paths(output_dir: Path, excel_name: str, dashboard_name: str) -> ReportPaths:
    output_dir.mkdir(parents=True, exist_ok=True)
    return ReportPaths(
        output_dir=output_dir,
        excel_path=output_dir / excel_name,
        dashboard_path=output_dir / dashboard_name,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analyze KKS Excel files and create Excel + dashboard reports.")
    parser.add_argument("input_dir", type=Path, help="Folder containing input .xlsx files.")
    parser.add_argument("--output-dir", type=Path, default=Path("output"), help="Folder for generated reports.")
    parser.add_argument("--excel-name", default="kks_analysis_results.xlsx", help="Name of the generated Excel report.")
    parser.add_argument("--dashboard-name", default="kks_dashboard.html", help="Name of the generated HTML dashboard.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    input_dir = args.input_dir.resolve()
    if not input_dir.exists() or not input_dir.is_dir():
        print(f"Input folder does not exist: {input_dir}", file=sys.stderr)
        return 1

    report_paths = resolve_report_paths(args.output_dir.resolve(), args.excel_name, args.dashboard_name)
    documents = analyze_folder(input_dir)
    file_summary = build_file_summary(documents)
    sheet_summary = build_sheet_summary(documents)
    overall_summary = build_overall_summary(file_summary)

    write_excel_report(documents, file_summary, sheet_summary, overall_summary, report_paths.excel_path)
    write_dashboard(file_summary, documents, report_paths.dashboard_path)

    missing = int(file_summary["Missing TC KKS"].sum())
    total = int(file_summary["Total Documents"].sum())
    print(f"Analyzed {len(file_summary)} Excel files and {total:,} documents.")
    print(f"Missing TC KKS: {missing:,} ({missing / total:.1%}).")
    print(f"Excel report: {report_paths.excel_path}")
    print(f"Dashboard: {report_paths.dashboard_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())