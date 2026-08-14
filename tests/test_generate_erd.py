"""
Unit Test: Django Management Command generate_erd
US: US-043 — ERD Analyzer & Generator
"""

import io

import pytest
from django.apps import apps
from django.core.management import call_command

from apps.core.management.commands.generate_erd import Command as GenerateErdCommand


@pytest.mark.django_db
def test_generate_erd_command_to_stdout():
    """Memastikan generate_erd berjalan sukses dengan --to-stdout dan menghasilkan sintaks Mermaid."""
    out = io.StringIO()
    call_command("generate_erd", "--to-stdout", stdout=out)
    output = out.getvalue()

    assert "# ERD & Database Architecture Specification" in output
    assert "```mermaid" in output
    assert "erDiagram" in output
    assert "Rincian Tabel Database" in output
    assert "User" in output or "Produk" in output


@pytest.mark.django_db
def test_generate_erd_command_app_filter():
    """Memastikan filter --apps hanya menganalisis app yang dipilih."""
    out = io.StringIO()
    call_command("generate_erd", "--apps", "inventory", "--to-stdout", stdout=out)
    output = out.getvalue()

    assert "Domain App: `inventory`" in output
    assert "Produk" in output
    assert "Domain App: `accounts`" not in output


@pytest.mark.django_db
def test_generate_erd_command_output_file(tmp_path):
    """Memastikan generate_erd menulis file Markdown ke path yang ditentukan oleh --output."""
    target_file = tmp_path / "test_erd.md"
    call_command("generate_erd", "--output", str(target_file))

    assert target_file.exists()
    content = target_file.read_text(encoding="utf-8")
    assert "# ERD & Database Architecture Specification" in content
    assert "```mermaid" in content


@pytest.mark.django_db
def test_generate_erd_build_erd_markdown_structure():
    """Memastikan metode build_erd_markdown menyusun struktur diagram dan relasi dengan benar."""
    cmd = GenerateErdCommand()
    inventory_models = [m for m in apps.get_models() if m._meta.app_label == "inventory"]
    assert len(inventory_models) > 0

    markdown = cmd.build_erd_markdown(inventory_models, title="Uji Coba ERD Inventory")

    assert "# Uji Coba ERD Inventory" in markdown
    assert "Produk" in markdown
    assert "Kategori" in markdown
    assert "Pemasok" in markdown
    assert "Foreign Key (`||--o{`)" in markdown or "One-to-One" in markdown
