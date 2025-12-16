from __future__ import annotations

import json
from pathlib import Path


def write_json(report: dict, path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)  # create folders if they don’t exist
    path.write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    )


def write_markdown(report: dict, path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    columns = report.get("columns", {})

    lines: list[str] = []
    lines.append("# CSV Profiling Report\n")
    lines.append(f"- Rows: **{report.get('rows', 0)}**\n")
    lines.append(f"- Columns: **{len(columns)}**\n")

    lines.append("\n| Column | Missing |\n|--------|---------|")
    for col, stats in columns.items():
        lines.append(f"| {col} | {stats.get('missing', 0)} |")

    text = "\n".join(lines) + "\n"
    path.write_text(text)
