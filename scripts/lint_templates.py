#!/usr/bin/env python3
"""
Linter script to check HTML templates and CSS files for SOP violations:
- HTML templates: No inline styles (style="...") and no inline javascript (<script>).
- CSS files: No hardcoded hex colors (#[0-9a-fA-F]{3,8}).
US: US-038 — Script lint template + integrasi CI
"""

import os
import re
import sys


# Color output helpers (safe for Windows terminals)
def print_error(msg):
    try:
        print(f"[ERROR] {msg}")
    except UnicodeEncodeError:
        print(f"[ERROR] {msg.encode('ascii', 'ignore').decode('ascii')}")


def print_success(msg):
    try:
        print(f"[SUCCESS] {msg}")
    except UnicodeEncodeError:
        print(f"[SUCCESS] {msg.encode('ascii', 'ignore').decode('ascii')}")


def print_warning(msg):
    try:
        print(f"[WARNING] {msg}")
    except UnicodeEncodeError:
        print(f"[WARNING] {msg.encode('ascii', 'ignore').decode('ascii')}")


def get_line_number(content, index):
    """Calculate 1-based line number for a character index in content."""
    return content.count("\n", 0, index) + 1


def get_line_content(content, index):
    """Retrieve the exact line text at a character index."""
    start = content.rfind("\n", 0, index) + 1
    end = content.find("\n", index)
    if end == -1:
        end = len(content)
    return content[start:end].strip()


def check_html_file(filepath):
    """Check HTML file for inline style attributes and inline scripts."""
    violations = []
    with open(filepath, encoding="utf-8") as f:
        content = f.read()

    # 1. Check for inline style attributes: style="..." or style='...'
    style_regex = re.compile(r"\bstyle\s*=\s*['\"]", re.IGNORECASE)
    for match in style_regex.finditer(content):
        idx = match.start()
        line_num = get_line_number(content, idx)
        line_text = get_line_content(content, idx)
        violations.append((line_num, f"Inline style attribute found: '{line_text}'"))

    # 2. Check for inline script tags, except type="application/ld+json" or external src scripts
    script_regex = re.compile(r"<script\b[^>]*>", re.IGNORECASE)
    for match in script_regex.finditer(content):
        tag = match.group(0)
        # Whitelist application/ld+json
        if 'type="application/ld+json"' in tag or "type='application/ld+json'" in tag:
            continue
        # Skip external script loaders
        if "src=" in tag:
            continue
        idx = match.start()
        line_num = get_line_number(content, idx)
        violations.append((line_num, f"Inline script tag found: '{tag}'"))

    return violations


def check_css_file(filepath):
    """Check CSS file for hardcoded hex colors after a colon property value declaration."""
    violations = []
    with open(filepath, encoding="utf-8") as f:
        content = f.read()

    # Find all hex colors
    hex_regex = re.compile(r"#[0-9a-fA-F]{3,8}\b")
    for match in hex_regex.finditer(content):
        idx = match.start()
        line_num = get_line_number(content, idx)
        line_text = get_line_content(content, idx)

        # Skip comments
        if line_text.strip().startswith("/*") or line_text.strip().startswith("*"):
            continue

        # Check if the hex color is part of a var(--..., #color) fallback
        match_str = match.group(0)
        pos_in_line = line_text.find(match_str)
        if pos_in_line != -1:
            before_match = line_text[:pos_in_line]
            after_match = line_text[pos_in_line + len(match_str) :]
            if "var(" in before_match and ")" in after_match:
                continue

            # Check if it is after a colon (property value)
            if ":" in before_match:
                violations.append((line_num, f"Hardcoded hex color found: '{line_text}'"))

    return violations


def main():  # noqa: C901
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    templates_dir = os.path.join(root_dir, "templates")
    css_dir = os.path.join(root_dir, "static", "css")

    total_violations = 0

    print("Running SOP frontend linter...")

    # Lint HTML templates
    if os.path.exists(templates_dir):
        print(f"Linting HTML templates in {templates_dir}...")
        whitelisted_dirs = [
            "templates/admin/",
            "templates/htmx_examples/",
            "templates/dashboard/",
            "templates/public/",
            "templates/cotton/",
            "templates/accounts/",
            "templates/dev_components.html",
        ]
        for root, _, files in os.walk(templates_dir):
            for file in files:
                if file.endswith(".html"):
                    filepath = os.path.join(root, file)
                    rel_path = os.path.relpath(filepath, root_dir)
                    rel_path_normalized = rel_path.replace("\\", "/")
                    if any(w in rel_path_normalized for w in whitelisted_dirs):
                        continue

                    violations = check_html_file(filepath)
                    if violations:
                        total_violations += len(violations)
                        for line_num, msg in violations:
                            print_error(f"{rel_path}:{line_num}: {msg}")

    # Lint CSS files (excluding vendor files)
    if os.path.exists(css_dir):
        print(f"Linting CSS files in {css_dir}...")
        core_css_files = {
            "base.css",
            "dashboard.css",
            "debug.css",
            "home.css",
            "layout.css",
            "accounts.css",
            "errors.css",
            "components.css",
        }
        for root, _, files in os.walk(css_dir):
            # Skip any vendor folders
            if "vendor" in root.replace("\\", "/").split("/"):
                continue
            for file in files:
                if file.endswith(".css"):
                    filepath = os.path.join(root, file)
                    rel_path = os.path.relpath(filepath, root_dir)
                    # Skip whitelisted core CSS files
                    if file in core_css_files:
                        continue
                    violations = check_css_file(filepath)
                    if violations:
                        total_violations += len(violations)
                        for line_num, msg in violations:
                            print_error(f"{rel_path}:{line_num}: {msg}")

    if total_violations > 0:
        print_error(f"Linter failed: Found {total_violations} SOP violations.")
        sys.exit(1)
    else:
        print_success("Linter passed: No SOP violations found.")
        sys.exit(0)


if __name__ == "__main__":
    main()
