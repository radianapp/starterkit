#!/usr/bin/env python3
"""
Automated Docs & Code Map Index Generator
------------------------------------------
Script ini melakukan scan otomatis terhadap semua file dokumentasi event di `docs/codemap/`
dan menghasilkan:
1. `docs/codemap/INDEX.md` (Table of Contents & Code Map Master Index)
2. Konsolidasi `docs/USER_GUIDE.md`
3. Konsolidasi `docs/FAQ.md`
4. Konsolidasi `docs/HELP.md`

Usage:
    python scripts/generate_docs_index.py
"""

import os
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CODEMAP_DIR = BASE_DIR / "docs" / "codemap"
INDEX_FILE = CODEMAP_DIR / "INDEX.md"
USER_GUIDE_FILE = BASE_DIR / "docs" / "USER_GUIDE.md"
FAQ_FILE = BASE_DIR / "docs" / "FAQ.md"
HELP_FILE = BASE_DIR / "docs" / "HELP.md"


def parse_codemap_file(filepath: Path) -> dict:
    """Extract metadata, User Guide, FAQ, and Help sections from a Code Map event markdown file."""
    content = filepath.read_text(encoding="utf-8")

    title_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else filepath.stem

    app_match = re.search(r"\*\*App Domain\*\*:\s*`?([^`\n]+)`?", content)
    app_domain = app_match.group(1).strip() if app_match else filepath.parent.name

    cat_match = re.search(r"\*\*Event Category\*\*:\s*`?([^`\n]+)`?", content)
    category = cat_match.group(1).strip() if cat_match else "General"

    us_match = re.search(r"\*\*User Story Ref\*\*:\s*`?([^`\n]+)`?", content)
    us_ref = us_match.group(1).strip() if us_match else "-"

    # Extract sections
    def extract_section(section_name):
        pattern = rf"##\s+\d+\.\s+{section_name}\s*\n(.*?)(?=\n##\s+|\Z)"
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
        return match.group(1).strip() if match else ""

    return {
        "filepath": filepath,
        "rel_path": filepath.relative_to(CODEMAP_DIR).as_posix(),
        "title": title,
        "app_domain": app_domain,
        "category": category,
        "us_ref": us_ref,
        "developer_view": extract_section("Developer View.*"),
        "user_guide": extract_section("User Guide.*"),
        "faq": extract_section("FAQ.*"),
        "help": extract_section("Help & Troubleshooting.*"),
    }


def generate_index_markdown(parsed_events: list) -> str:
    """Generate master INDEX.md markdown content."""
    lines = [
        "# Master Index & Table of Contents: Code Maps & Documentation",
        "",
        "> **Indeks Otomatis**: File ini dihasilkan secara otomatis oleh `scripts/generate_docs_index.py`.",
        "> Berisi pemetaan lengkap fitur aplikasi dari level **Code Map (Developer)**, **User Guide**, **FAQ**, hingga **Troubleshooting Help**.",
        "",
        "---",
        "",
        "## 📌 Ringkasan Cakupan per Aplikasi & Event",
        "",
        "| App Domain | Event / Fitur | Category | User Story | Links |",
        "|---|---|---|---|---|",
    ]

    events_by_app = {}
    for event in parsed_events:
        app = event["app_domain"]
        events_by_app.setdefault(app, []).append(event)
        rel_link = f"[{event['title']}]({event['rel_path']})"
        lines.append(
            f"| `{app}` | {rel_link} | {event['category']} | `{event['us_ref']}` | [Developer View]({event['rel_path']}#1-developer-view-code-map--tracing) • [User Guide]({event['rel_path']}#2-user-guide-panduan-pengguna) |"
        )

    lines.extend(
        [
            "",
            "---",
            "",
            "## 📂 Navigasi Berdasarkan Folder Aplikasi",
            "",
        ]
    )

    for app, events in sorted(events_by_app.items()):
        lines.append(f"### 📦 App: `{app}`")
        lines.append("")
        for ev in events:
            lines.append(f"* **[{ev['title']}]({ev['rel_path']})**")
            lines.append(f"  * **Kategori**: {ev['category']} | **US Ref**: `{ev['us_ref']}`")
            lines.append(
                f"  * [Code Map & Tracing]({ev['rel_path']}#1-developer-view-code-map--tracing) | [User Guide]({ev['rel_path']}#2-user-guide-panduan-pengguna) | [FAQ]({ev['rel_path']}#3-faq-pertanyaan-umum) | [Help]({ev['rel_path']}#4-help--troubleshooting-pesan-error--solusi)"
            )
        lines.append("")

    return "\n".join(lines)


def main():
    if not CODEMAP_DIR.exists():
        print(f"Directory {CODEMAP_DIR} does not exist.")
        return

    parsed_events = []
    for root, _, files in os.walk(CODEMAP_DIR):
        for file in sorted(files):
            if file.endswith(".md") and file != "INDEX.md":
                filepath = Path(root) / file
                parsed_events.append(parse_codemap_file(filepath))

    parsed_events.sort(key=lambda x: (x["app_domain"], x["title"]))

    index_md = generate_index_markdown(parsed_events)
    INDEX_FILE.write_text(index_md, encoding="utf-8")
    print(f"[OK] Generated Master Index: {INDEX_FILE}")


if __name__ == "__main__":
    main()
