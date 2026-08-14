"""
Django Management Command: generate_erd
---------------------------------------
Membuat secara otomatis dokumen ERD (Entity Relationship Diagram) berbasis Django Models.
Menghasilkan output format Markdown terstruktur yang dilengkapi dengan diagram Mermaid (`erDiagram`).

Usage:
    python manage.py generate_erd [options]

Options:
    --output, -o      Path file Markdown target (Default: docs/architecture/database.md)
    --apps, -a        Daftar nama app Django dipisahkan koma (misal: inventory,accounts)
    --exclude-apps, -e Daftar nama app yang dikeualikan
    --stdout          Tampilkan output Markdown langsung ke terminal (tanpa menulis file)
    --title           Judul kustom untuk dokumen ERD

Examples:
    python manage.py generate_erd
    python manage.py generate_erd --apps inventory,accounts --stdout
    python manage.py generate_erd --output docs/architecture/database.md
"""

import sys
from pathlib import Path
from typing import Any

from django.apps import apps
from django.core.management.base import BaseCommand, CommandError
from django.db import models


class Command(BaseCommand):
    help = "Analisis Django Models dan hasilkan dokumentasi ERD lengkap (Markdown + Mermaid)."

    def add_arguments(self, parser):
        parser.add_argument(
            "-o",
            "--output",
            type=str,
            default="docs/architecture/database.md",
            help="Path file Markdown target (default: docs/architecture/database.md).",
        )
        parser.add_argument(
            "-a",
            "--apps",
            type=str,
            default="",
            help="Daftar nama app dipisahkan koma untuk dianalisis (contoh: accounts,inventory).",
        )
        parser.add_argument(
            "-e",
            "--exclude-apps",
            type=str,
            default="admin,auth,contenttypes,sessions,messages,staticfiles,account,socialaccount",
            help="Daftar nama app yang dikecualikan (default: admin,auth,contenttypes,sessions,messages,staticfiles,account,socialaccount).",
        )
        parser.add_argument(
            "--to-stdout",
            action="store_true",
            help="Cetak hasil Markdown ke stdout tanpa menulis ke file.",
        )
        parser.add_argument(
            "--title",
            type=str,
            default="ERD & Database Architecture Specification",
            help="Judul dokumen ERD yang dihasilkan.",
        )

    def handle(self, *args, **options):
        output_path_str = options["output"]
        target_apps_raw = options["apps"]
        exclude_apps_raw = options["exclude_apps"]
        to_stdout = options["to_stdout"]
        title = options["title"]

        target_apps = [a.strip().lower() for a in target_apps_raw.split(",") if a.strip()]
        exclude_apps = [a.strip().lower() for a in exclude_apps_raw.split(",") if a.strip()]

        # Ambil daftar model yang akan dianalisis
        target_models = self._get_target_models(target_apps, exclude_apps)

        if not target_models:
            raise CommandError("Tidak ada model Django yang ditemukan sesuai kriteria filter.")

        # Hasilkan dokumen Markdown
        markdown_content = self.build_erd_markdown(target_models, title=title)

        if to_stdout:
            try:
                self.stdout.write(markdown_content)
            except UnicodeEncodeError:
                safe_content = markdown_content.encode(
                    sys.stdout.encoding or "utf-8", errors="replace"
                ).decode(sys.stdout.encoding or "utf-8", errors="replace")
                self.stdout.write(safe_content)
            return

        # Tulis ke file
        try:
            output_file = Path(output_path_str)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            output_file.write_text(markdown_content, encoding="utf-8")
            self.stdout.write(
                self.style.SUCCESS(
                    f"[OK] Dokumentasi ERD berhasil dibuat/diperbarui di '{output_file}'"
                )
            )
        except Exception as e:
            raise CommandError(f"Gagal menulis file dokumentasi ERD: {e}")

    def _get_target_models(self, target_apps: list[str], exclude_apps: list[str]) -> list[Any]:
        """Mengambil daftar model Django berdasarkan filter app."""
        all_models = apps.get_models(include_auto_created=False)
        selected = []

        for model in all_models:
            app_label = model._meta.app_label.lower()
            if target_apps and app_label not in target_apps:
                continue
            if app_label in exclude_apps and not target_apps:
                continue
            selected.append(model)

        return selected

    def build_erd_markdown(
        self, model_list: list[Any], title: str = "ERD & Database Architecture Specification"
    ) -> str:
        """Membuat string dokumen Markdown berisi Mermaid ERD dan Spesifikasi Schema."""
        lines = []
        lines.append(f"# {title}")
        lines.append("")
        lines.append(
            "> Dokumen ini dibuat secara otomatis oleh management command `python manage.py generate_erd`."
        )
        lines.append("")

        # Statistik Singkat
        total_models = len(model_list)
        app_names = sorted({m._meta.app_label for m in model_list})
        lines.append("## 📌 Ringkasan Skema")
        lines.append("")
        lines.append(f"- **Total Aplikasi**: {len(app_names)} (`{', '.join(app_names)}`)")
        lines.append(f"- **Total Model/Tabel**: {total_models}")
        lines.append("")

        # Section 1: Mermaid ERD
        mermaid_code, relationships = self._generate_mermaid_erd(model_list)
        lines.append("## 📐 Diagram ERD (Mermaid)")
        lines.append("")
        lines.append("```mermaid")
        lines.append(mermaid_code)
        lines.append("```")
        lines.append("")

        # Section 2: Detailed Schema per Model
        lines.append("## 🗂️ Rincian Tabel Database")
        lines.append("")

        # Group models by app
        models_by_app: dict[str, list[Any]] = {}
        for m in model_list:
            app = m._meta.app_label
            models_by_app.setdefault(app, []).append(m)

        for app_label in sorted(models_by_app.keys()):
            lines.append(f"### Domain App: `{app_label}`")
            lines.append("")

            for model in sorted(models_by_app[app_label], key=lambda x: x._meta.object_name):
                model_name = model._meta.object_name
                db_table = model._meta.db_table
                docstring = (model.__doc__ or "").strip().split("\n")[0]
                if docstring.startswith(model_name + "("):
                    docstring = ""

                lines.append(f"#### Model: `{model_name}` (`{db_table}`)")
                if docstring:
                    lines.append(f"_{docstring}_")
                lines.append("")

                lines.append(
                    "| Kolom / Field | Tipe Data | Key | Nullable | Default | Deskripsi / Help Text |"
                )
                lines.append("|---|---|---|---|---|---|")

                # Concrete Fields
                for field in model._meta.fields:
                    fname = field.name
                    if field.is_relation and hasattr(field, "attname"):
                        fname = field.attname  # e.g. user_id instead of user

                    internal_type = field.get_internal_type()

                    key_type = ""
                    if field.primary_key:
                        key_type = "PK"
                    elif field.is_relation and (field.many_to_one or field.one_to_one):
                        key_type = "FK"
                    key_display = f"**{key_type}**" if key_type else "-"

                    is_null = "Ya" if field.null else "Tidak"

                    default_val = "-"
                    if field.has_default() and field.default != models.NOT_PROVIDED:
                        def_repr = str(field.default)
                        if callable(field.default):
                            def_repr = (
                                field.default.__name__
                                if hasattr(field.default, "__name__")
                                else "callable"
                            )
                        default_val = f"`{def_repr}`"

                    help_txt = field.help_text or field.verbose_name or "-"
                    if field.is_relation and field.related_model:
                        rel_target = field.related_model._meta.object_name
                        help_txt += f" (Relasi ke `{rel_target}`)"

                    lines.append(
                        f"| `{fname}` | `{internal_type}` | {key_display} | {is_null} | {default_val} | {help_txt} |"
                    )

                # Many to Many Fields
                for m2m in model._meta.many_to_many:
                    target_model = m2m.related_model._meta.object_name
                    lines.append(
                        f"| `{m2m.name}` | `ManyToManyField` | **M2M** | Ya | - | Relasi Many-to-Many ke `{target_model}` |"
                    )

                lines.append("")

        # Section 3: Summary of Relationships
        lines.append("## 🔗 Daftar Relasi Antar Tabel")
        lines.append("")
        if relationships:
            lines.append("| Model Asal | Tipe Relasi | Model Target | Nama Field |")
            lines.append("|---|---|---|---|")
            for source, rel_type, target, field_name in relationships:
                lines.append(f"| `{source}` | {rel_type} | `{target}` | `{field_name}` |")
            lines.append("")
        else:
            lines.append("_Tidak ada relasi antar-tabel yang terdeteksi._")
            lines.append("")

        return "\n".join(lines)

    def _generate_mermaid_erd(
        self, model_list: list[Any]
    ) -> tuple[str, list[tuple[str, str, str, str]]]:
        """Menghasilkan sintaks Mermaid erDiagram dan daftar relasi."""
        mermaid_lines = ["erDiagram"]
        relationships: list[tuple[str, str, str, str]] = []
        model_names = {m._meta.object_name: m for m in model_list}

        # 1. Generate Entity definitions
        for model in sorted(model_list, key=lambda x: x._meta.object_name):
            entity_name = model._meta.object_name
            mermaid_lines.append(f"    {entity_name} {{")

            for field in model._meta.fields:
                fname = (
                    field.attname if field.is_relation and hasattr(field, "attname") else field.name
                )
                ftype = self._simplify_type(field.get_internal_type())

                pk_fk = ""
                if field.primary_key:
                    pk_fk = "PK"
                elif field.is_relation:
                    pk_fk = "FK"

                comment = field.verbose_name or ""
                if isinstance(comment, str) and comment:
                    comment_str = f' "{comment}"'
                else:
                    comment_str = ""

                mermaid_lines.append(f"        {ftype} {fname} {pk_fk}{comment_str}".rstrip())

            mermaid_lines.append("    }")
            mermaid_lines.append("")

        # 2. Generate Relationships
        seen_rels = set()

        for model in model_list:
            source_name = model._meta.object_name

            # Foreign Keys & One-to-One
            for field in model._meta.fields:
                if not field.is_relation or not field.related_model:
                    continue

                target_name = field.related_model._meta.object_name
                # Hanya buat relasi jika target model termasuk dalam scope diagram
                if target_name not in model_names:
                    continue

                rel_key = (source_name, field.name, target_name)
                if rel_key in seen_rels:
                    continue
                seen_rels.add(rel_key)

                if field.one_to_one:
                    # One to One: TARGET ||--|| SOURCE
                    mermaid_lines.append(f'    {target_name} ||--|| {source_name} : "{field.name}"')
                    relationships.append(
                        (source_name, "One-to-One (`||--||`)", target_name, field.name)
                    )
                elif field.many_to_one:
                    # Foreign Key (One to Many): TARGET ||--o{ SOURCE
                    mermaid_lines.append(
                        f'    {target_name} ||--o{{ {source_name} : "{field.name}"'
                    )
                    relationships.append(
                        (source_name, "Foreign Key (`||--o{`)", target_name, field.name)
                    )

            # Many to Many
            for m2m in model._meta.many_to_many:
                target_name = m2m.related_model._meta.object_name
                if target_name not in model_names:
                    continue

                rel_key = (*sorted([source_name, target_name]), m2m.name)
                if rel_key in seen_rels:
                    continue
                seen_rels.add(rel_key)

                mermaid_lines.append(f'    {source_name} }}o--o{{ {target_name} : "{m2m.name}"')
                relationships.append(
                    (source_name, "Many-to-Many (`}o--o{`)", target_name, m2m.name)
                )

        return "\n".join(mermaid_lines), relationships

    def _simplify_type(self, internal_type: str) -> str:
        """Menyederhanakan nama internal type Django ke tipe umum untuk diagram Mermaid."""
        mapping = {
            "AutoField": "bigint",
            "BigAutoField": "bigint",
            "SmallAutoField": "int",
            "IntegerField": "int",
            "SmallIntegerField": "int",
            "BigIntegerField": "bigint",
            "PositiveIntegerField": "int",
            "CharField": "string",
            "TextField": "text",
            "BooleanField": "bool",
            "DateTimeField": "datetime",
            "DateField": "date",
            "TimeField": "time",
            "DecimalField": "decimal",
            "FloatField": "float",
            "EmailField": "string",
            "UUIDField": "uuid",
            "ForeignKey": "bigint",
            "OneToOneField": "bigint",
            "FileField": "string",
            "ImageField": "string",
            "JSONField": "json",
        }
        return mapping.get(internal_type, internal_type.lower())
