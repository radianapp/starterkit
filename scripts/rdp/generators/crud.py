# scripts/rdp/generators/crud.py
# US-024: CLI rdp — generator CRUD enhanced dan page templates
#
# Perintah baru:
#   rdp new crud <nama> -a <app>              → generate full CRUD (list+create+edit+delete+detail)
#   rdp new crud <nama> -a <app> --only list,create  → pilih subset halaman
#   rdp new crud <nama> -a <app> --style table|card|simple
#   rdp new page list -a <app> --model <Model>        → satu halaman list saja
#   rdp new page create -a <app> --model <Model>      → satu halaman create saja
#   rdp new page edit -a <app> --model <Model>        → satu halaman edit saja
#   rdp new page delete -a <app> --model <Model>      → satu halaman confirm delete saja
#   rdp new page detail -a <app> --model <Model>      → satu halaman detail saja
#   rdp new page custom <nama> -a <app>               → halaman kosong custom (app layout)

import os
import sys

from ..utils import _to_class_name, get_app_from_args, get_input


# ── Halaman yang didukung CRUD ────────────────────────────────────────────────
CRUD_PAGES = ["list", "create", "edit", "delete", "detail"]

# ── Style template yang tersedia ──────────────────────────────────────────────
CRUD_STYLES = ["table", "card", "simple"]


def _parse_flags(args: list) -> dict:
    """
    TUJUAN: Parse flag CLI (--only, --style, --model) dari args.

    ALUR:
      1. Scan args untuk flag yang dikenal
      2. Return dict {only, style, model}

    DIPANGGIL DARI: run_new_crud(), run_new_page()
    """
    flags = {
        "only": None,    # list halaman yang diminta, None = semua
        "style": "table",
        "model": None,
    }

    i = 0
    while i < len(args):
        if args[i] == "--only" and i + 1 < len(args):
            flags["only"] = [p.strip() for p in args[i + 1].split(",")]
            i += 2
        elif args[i] == "--style" and i + 1 < len(args):
            style = args[i + 1].lower()
            if style not in CRUD_STYLES:
                print(f"[WARNING] Style '{style}' tidak dikenal. Pakai 'table' (default).")
            else:
                flags["style"] = style
            i += 2
        elif args[i] == "--model" and i + 1 < len(args):
            flags["model"] = args[i + 1]
            i += 2
        else:
            i += 1

    return flags


def _inject_url(app: str, name: str, pages: list[str]):
    """
    TUJUAN: Inject URL patterns ke apps/{app}/urls.py.

    ALUR:
      1. Baca urls.py yang ada (atau buat baru jika belum ada)
      2. Tambahkan import dan path untuk setiap halaman yang di-generate
      3. Tulis ulang file

    DIPANGGIL DARI: run_new_crud()
    """
    urls_path = os.path.join("apps", app, "urls.py")
    name_lower = name.lower()
    class_name = _to_class_name(name)

    # Mapping halaman → view class dan URL pattern
    page_map = {
        "list":   (f"{class_name}ListView",   f'path("{name_lower}/", {class_name}ListView.as_view(), name="{name_lower}-list"),'),
        "detail": (f"{class_name}DetailView", f'path("{name_lower}/<int:pk>/", {class_name}DetailView.as_view(), name="{name_lower}-detail"),'),
        "create": (f"{class_name}CreateView", f'path("{name_lower}/baru/", {class_name}CreateView.as_view(), name="{name_lower}-create"),'),
        "edit":   (f"{class_name}UpdateView", f'path("{name_lower}/<int:pk>/edit/", {class_name}UpdateView.as_view(), name="{name_lower}-update"),'),
        "delete": (f"{class_name}DeleteView", f'path("{name_lower}/<int:pk>/hapus/", {class_name}DeleteView.as_view(), name="{name_lower}-delete"),'),
    }

    view_classes = [page_map[p][0] for p in pages if p in page_map]
    url_patterns = [page_map[p][1] for p in pages if p in page_map]

    if not os.path.exists(urls_path):
        # Buat urls.py baru
        imports_str = ",\n    ".join(view_classes)
        patterns_str = "\n    ".join(url_patterns)
        content = f"""\
# apps/{app}/urls.py

from django.urls import path

from .views import (
    {imports_str},
)

app_name = "{app}"

urlpatterns = [
    {patterns_str}
]
"""
        with open(urls_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  [OK] urls.py baru dibuat: {urls_path}")
        return

    # Inject ke urls.py yang sudah ada
    with open(urls_path, 'r', encoding='utf-8') as f:
        existing = f.read()

    # Tambah import view yang belum ada
    new_imports = [vc for vc in view_classes if vc not in existing]
    if new_imports:
        # Cari blok from .views import ... dan tambahkan
        if "from .views import" in existing:
            # Append ke import yang ada — cari baris terakhir blok import
            import_line = f"from .views import (\n"
            if import_line in existing:
                # Multi-line import — inject sebelum penutup )
                sep = ",\n    "
                new_imports_str = sep.join(new_imports)
                existing = existing.replace(
                    ")\n\napp_name",
                    "    " + new_imports_str + ",\n)\n\napp_name",
                    1,
                )
            else:
                # Single-line import — konversi ke multi-line
                for vc in new_imports:
                    existing = existing.replace(
                        "from .views import",
                        "from .views import " + vc + ",\nfrom .views import",
                        1,
                    )
        else:
            sep = ",\n    "
            new_imports_str = sep.join(new_imports)
            existing = "from .views import (\n    " + new_imports_str + ",\n)\n\n" + existing

    # Tambah URL patterns yang belum ada
    new_patterns = [p for p in url_patterns if p.split(",")[0].split("(")[1] not in existing]
    if new_patterns and "urlpatterns = [" in existing:
        patterns_block = "\n    ".join(new_patterns)
        existing = existing.replace(
            "urlpatterns = [",
            "urlpatterns = [\n    " + patterns_block,
            1,
        )

    with open(urls_path, 'w', encoding='utf-8') as f:
        f.write(existing)
    print(f"  [OK] URL patterns ditambahkan ke {urls_path}")


def _inject_views(app: str, name: str, pages: list[str]):
    """
    TUJUAN: Generate view file dan inject ke views/__init__.py.

    DIPANGGIL DARI: run_new_crud()
    """
    name_lower = name.lower()
    class_name = _to_class_name(name)
    views_dir = os.path.join("apps", app, "views")
    os.makedirs(views_dir, exist_ok=True)

    view_path = os.path.join(views_dir, f"{name_lower}.py")
    if os.path.exists(view_path):
        print(f"  [WARNING] View '{name_lower}.py' sudah ada, dilewati.")
        return []  # caller harus cek — jangan inject URL untuk view yang tidak dibuat

    # Buat open() untuk views/__init__.py jika belum ada
    init_path = os.path.join(views_dir, "__init__.py")
    if not os.path.exists(init_path):
        with open(init_path, 'w', encoding='utf-8') as f:
            f.write("")

    # Build view class content berdasarkan halaman yang diminta
    view_lines = [
        f"# apps/{app}/views/{name_lower}.py\n",
        "from django.contrib.auth.mixins import LoginRequiredMixin",
        "from django.urls import reverse_lazy",
        "from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView\n",
        f"from ..models import {class_name}",
        f"from ..forms import {class_name}Form\n\n",
    ]

    exported = []

    if "list" in pages:
        view_lines.append(f"""\
class {class_name}ListView(LoginRequiredMixin, ListView):
    \"\"\"
    TUJUAN: Tampilkan daftar semua {class_name}.

    DIPANGGIL DARI: urls.py → name="{name_lower}-list"
    DEPENDENSI: {class_name} model, templates/apps/{app}/{name_lower}_list.html
    \"\"\"

    model = {class_name}
    template_name = "apps/{app}/{name_lower}_list.html"
    context_object_name = "items"
    paginate_by = 20

""")
        exported.append(f"{class_name}ListView")

    if "detail" in pages:
        view_lines.append(f"""\
class {class_name}DetailView(LoginRequiredMixin, DetailView):
    \"\"\"
    TUJUAN: Tampilkan detail satu {class_name}.

    DIPANGGIL DARI: urls.py → name="{name_lower}-detail"
    \"\"\"

    model = {class_name}
    template_name = "apps/{app}/{name_lower}_detail.html"

""")
        exported.append(f"{class_name}DetailView")

    if "create" in pages:
        view_lines.append(f"""\
class {class_name}CreateView(LoginRequiredMixin, CreateView):
    \"\"\"
    TUJUAN: Buat {class_name} baru.

    DIPANGGIL DARI: urls.py → name="{name_lower}-create"
    \"\"\"

    model = {class_name}
    form_class = {class_name}Form
    template_name = "apps/{app}/{name_lower}_form.html"
    success_url = reverse_lazy("{app}:{name_lower}-list")

""")
        exported.append(f"{class_name}CreateView")

    if "edit" in pages:
        view_lines.append(f"""\
class {class_name}UpdateView(LoginRequiredMixin, UpdateView):
    \"\"\"
    TUJUAN: Edit {class_name} yang sudah ada.

    DIPANGGIL DARI: urls.py → name="{name_lower}-update"
    \"\"\"

    model = {class_name}
    form_class = {class_name}Form
    template_name = "apps/{app}/{name_lower}_form.html"
    success_url = reverse_lazy("{app}:{name_lower}-list")

""")
        exported.append(f"{class_name}UpdateView")

    if "delete" in pages:
        view_lines.append(f"""\
class {class_name}DeleteView(LoginRequiredMixin, DeleteView):
    \"\"\"
    TUJUAN: Hapus {class_name}.

    DIPANGGIL DARI: urls.py → name="{name_lower}-delete"
    \"\"\"

    model = {class_name}
    template_name = "apps/{app}/{name_lower}_confirm_delete.html"
    success_url = reverse_lazy("{app}:{name_lower}-list")

""")
        exported.append(f"{class_name}DeleteView")

    with open(view_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(view_lines))

    # Inject ke __init__.py
    import_line = f"from .{name_lower} import {', '.join(exported)}\n"
    with open(init_path, 'a', encoding='utf-8') as f:
        f.write(import_line)

    print(f"  [OK] Views dibuat di {view_path}")
    return exported


def _inject_form(app: str, name: str):
    """
    TUJUAN: Generate ModelForm jika belum ada.

    DIPANGGIL DARI: run_new_crud()
    """
    name_lower = name.lower()
    class_name = _to_class_name(name)
    forms_dir = os.path.join("apps", app, "forms")
    os.makedirs(forms_dir, exist_ok=True)

    form_path = os.path.join(forms_dir, f"{name_lower}_forms.py")
    if os.path.exists(form_path):
        print(f"  [INFO] Form '{name_lower}_forms.py' sudah ada, dilewati.")
        return

    init_path = os.path.join(forms_dir, "__init__.py")
    if not os.path.exists(init_path):
        with open(init_path, 'w', encoding='utf-8') as f:
            f.write("")

    form_content = f"""\
# apps/{app}/forms/{name_lower}_forms.py

from django import forms

from ..models import {class_name}


class {class_name}Form(forms.ModelForm):
    \"\"\"
    TUJUAN: Form untuk create dan update {class_name}.

    DIPANGGIL DARI: views/{name_lower}.py ({class_name}CreateView, {class_name}UpdateView)
    DEPENDENSI: {class_name} model
    \"\"\"

    class Meta:
        model = {class_name}
        fields = "__all__"
"""
    with open(form_path, 'w', encoding='utf-8') as f:
        f.write(form_content)

    with open(init_path, 'a', encoding='utf-8') as f:
        f.write(f"from .{name_lower}_forms import {class_name}Form\n")

    print(f"  [OK] Form dibuat di {form_path}")


def _generate_list_template(app: str, name: str, verbose: str, style: str) -> str:
    """Generate template list sesuai style (table/card/simple)."""
    name_lower = name.lower()

    if style == "card":
        return f"""\
{{# templates/apps/{app}/{name_lower}_list.html #}}
<c-layout.app title="Daftar {verbose}">

    <div class="rdp-page-header">
        <h2 class="rdp-page-header__title">Daftar {verbose}</h2>
        <div class="rdp-page-header__actions">
            <c-rdp.button variant="primary" href="{{% url '{app}:{name_lower}-create' %}}">+ Tambah {verbose}</c-rdp.button>
        </div>
    </div>

    {{% if items %}}
    <div class="rdp-grid rdp-grid--3col">
        {{% for item in items %}}
        <c-rdp.card>
            <div class="rdp-card__body">
                <h3>{{{{ item.name }}}}</h3>
                {{% if item.description %}}<p>{{{{ item.description|truncatewords:20 }}}}</p>{{% endif %}}
            </div>
            <div class="rdp-card__footer">
                <a href="{{% url '{app}:{name_lower}-detail' item.pk %}}" class="rdp-btn rdp-btn--sm rdp-btn--ghost">Detail</a>
                <a href="{{% url '{app}:{name_lower}-update' item.pk %}}" class="rdp-btn rdp-btn--sm rdp-btn--secondary">Edit</a>
                <a href="{{% url '{app}:{name_lower}-delete' item.pk %}}" class="rdp-btn rdp-btn--sm rdp-btn--danger">Hapus</a>
            </div>
        </c-rdp.card>
        {{% endfor %}}
    </div>

    {{% if is_paginated %}}
    <div class="rdp-pagination">
        {{% if page_obj.has_previous %}}<a href="?page={{{{ page_obj.previous_page_number }}}}" class="rdp-btn rdp-btn--ghost">← Sebelumnya</a>{{% endif %}}
        <span>Halaman {{{{ page_obj.number }}}} dari {{{{ page_obj.paginator.num_pages }}}}</span>
        {{% if page_obj.has_next %}}<a href="?page={{{{ page_obj.next_page_number }}}}" class="rdp-btn rdp-btn--ghost">Berikutnya →</a>{{% endif %}}
    </div>
    {{% endif %}}

    {{% else %}}
    <div class="rdp-empty-state">
        <p class="rdp-empty-state__text">Belum ada data {verbose}.</p>
        <c-rdp.button variant="primary" href="{{% url '{app}:{name_lower}-create' %}}">+ Tambah {verbose}</c-rdp.button>
    </div>
    {{% endif %}}

</c-layout.app>
"""

    elif style == "simple":
        return f"""\
{{# templates/apps/{app}/{name_lower}_list.html #}}
<c-layout.app title="Daftar {verbose}">

    <h2>Daftar {verbose}</h2>
    <p><a href="{{% url '{app}:{name_lower}-create' %}}" class="rdp-btn rdp-btn--primary">+ Tambah {verbose}</a></p>

    <ul>
        {{% for item in items %}}
        <li>
            <a href="{{% url '{app}:{name_lower}-detail' item.pk %}}">{{{{ item.name }}}}</a>
            — <a href="{{% url '{app}:{name_lower}-update' item.pk %}}">Edit</a>
            | <a href="{{% url '{app}:{name_lower}-delete' item.pk %}}">Hapus</a>
        </li>
        {{% empty %}}
        <li>Belum ada data.</li>
        {{% endfor %}}
    </ul>

</c-layout.app>
"""

    else:  # table (default)
        return f"""\
{{# templates/apps/{app}/{name_lower}_list.html #}}
<c-layout.app title="Daftar {verbose}">

    <div class="rdp-page-header">
        <h2 class="rdp-page-header__title">Daftar {verbose}</h2>
        <div class="rdp-page-header__actions">
            <c-rdp.button variant="primary" href="{{% url '{app}:{name_lower}-create' %}}">+ Tambah {verbose}</c-rdp.button>
        </div>
    </div>

    <c-rdp.card>
        {{% if items %}}
        <table class="rdp-table">
            <thead>
                <tr>
                    <th>Nama</th>
                    <th>Status</th>
                    <th>Dibuat</th>
                    <th style="width:140px">Aksi</th>
                </tr>
            </thead>
            <tbody>
                {{% for item in items %}}
                <tr>
                    <td><a href="{{% url '{app}:{name_lower}-detail' item.pk %}}">{{{{ item.name }}}}</a></td>
                    <td>
                        {{% if item.is_active %}}
                            <span class="rdp-badge rdp-badge--success">Aktif</span>
                        {{% else %}}
                            <span class="rdp-badge rdp-badge--neutral">Nonaktif</span>
                        {{% endif %}}
                    </td>
                    <td>{{{{ item.created_at|date:"d M Y" }}}}</td>
                    <td class="rdp-table__actions">
                        <a href="{{% url '{app}:{name_lower}-detail' item.pk %}}" class="rdp-btn rdp-btn--sm rdp-btn--ghost">Detail</a>
                        <a href="{{% url '{app}:{name_lower}-update' item.pk %}}" class="rdp-btn rdp-btn--sm rdp-btn--secondary">Edit</a>
                        <a href="{{% url '{app}:{name_lower}-delete' item.pk %}}" class="rdp-btn rdp-btn--sm rdp-btn--danger">Hapus</a>
                    </td>
                </tr>
                {{% endfor %}}
            </tbody>
        </table>

        {{% if is_paginated %}}
        <div class="rdp-pagination">
            {{% if page_obj.has_previous %}}<a href="?page={{{{ page_obj.previous_page_number }}}}" class="rdp-btn rdp-btn--ghost">← Sebelumnya</a>{{% endif %}}
            <span>Halaman {{{{ page_obj.number }}}} dari {{{{ page_obj.paginator.num_pages }}}}</span>
            {{% if page_obj.has_next %}}<a href="?page={{{{ page_obj.next_page_number }}}}" class="rdp-btn rdp-btn--ghost">Berikutnya →</a>{{% endif %}}
        </div>
        {{% endif %}}

        {{% else %}}
        <div class="rdp-empty-state">
            <p class="rdp-empty-state__text">Belum ada data {verbose}.</p>
            <c-rdp.button variant="primary" href="{{% url '{app}:{name_lower}-create' %}}">+ Tambah {verbose}</c-rdp.button>
        </div>
        {{% endif %}}
    </c-rdp.card>

</c-layout.app>
"""


def _generate_form_template(app: str, name: str, verbose: str) -> str:
    """Generate template form (dipakai create & edit)."""
    name_lower = name.lower()
    return f"""\
{{# templates/apps/{app}/{name_lower}_form.html #}}
<c-layout.app title="{{% if object %}}Edit{{% else %}}Tambah{{% endif %}} {verbose}">

    <div class="rdp-page-header">
        <h2 class="rdp-page-header__title">{{% if object %}}Edit{{% else %}}Tambah{{% endif %}} {verbose}</h2>
        <div class="rdp-page-header__actions">
            <c-rdp.button variant="ghost" href="{{% url '{app}:{name_lower}-list' %}}">← Kembali</c-rdp.button>
        </div>
    </div>

    <c-rdp.card>
        <form method="POST" class="rdp-form">
            {{% csrf_token %}}
            {{{{ form.as_p }}}}
            <div class="rdp-form__actions">
                <c-rdp.button type="submit" variant="primary">Simpan</c-rdp.button>
                <c-rdp.button variant="ghost" href="{{% url '{app}:{name_lower}-list' %}}">Batal</c-rdp.button>
            </div>
        </form>
    </c-rdp.card>

</c-layout.app>
"""


def _generate_detail_template(app: str, name: str, verbose: str) -> str:
    """Generate template detail."""
    name_lower = name.lower()
    return f"""\
{{# templates/apps/{app}/{name_lower}_detail.html #}}
<c-layout.app title="{{{{ object.name }}}}">

    <div class="rdp-page-header">
        <h2 class="rdp-page-header__title">{{{{ object.name }}}}</h2>
        <div class="rdp-page-header__actions">
            <c-rdp.button variant="secondary" href="{{% url '{app}:{name_lower}-update' object.pk %}}">Edit</c-rdp.button>
            <c-rdp.button variant="danger" href="{{% url '{app}:{name_lower}-delete' object.pk %}}">Hapus</c-rdp.button>
        </div>
    </div>

    <c-rdp.card>
        <dl class="rdp-dl">
            <dt>Nama</dt>
            <dd>{{{{ object.name }}}}</dd>

            <dt>Deskripsi</dt>
            <dd>{{{{ object.description|default:"-" }}}}</dd>

            {{% if object.is_active is not None %}}
            <dt>Status</dt>
            <dd>
                {{% if object.is_active %}}
                    <span class="rdp-badge rdp-badge--success">Aktif</span>
                {{% else %}}
                    <span class="rdp-badge rdp-badge--neutral">Nonaktif</span>
                {{% endif %}}
            </dd>
            {{% endif %}}

            <dt>Dibuat pada</dt>
            <dd>{{{{ object.created_at|date:"d M Y H:i" }}}}</dd>
        </dl>
    </c-rdp.card>

    <div style="margin-top:16px">
        <a href="{{% url '{app}:{name_lower}-list' %}}" class="rdp-btn rdp-btn--ghost">← Kembali ke Daftar</a>
    </div>

</c-layout.app>
"""


def _generate_delete_template(app: str, name: str, verbose: str) -> str:
    """Generate template konfirmasi hapus."""
    name_lower = name.lower()
    return f"""\
{{# templates/apps/{app}/{name_lower}_confirm_delete.html #}}
<c-layout.app title="Hapus {verbose}">

    <div class="rdp-page-header">
        <h2 class="rdp-page-header__title">Hapus {verbose}</h2>
    </div>

    <c-rdp.card>
        <p>Yakin ingin menghapus <strong>{{{{ object.name }}}}</strong>?</p>
        <p style="color: var(--rdp-color-danger); font-size: 0.9em;">⚠️ Tindakan ini tidak bisa dibatalkan.</p>
        <form method="POST" style="margin-top:16px; display:flex; gap:8px">
            {{% csrf_token %}}
            <c-rdp.button type="submit" variant="danger">Ya, Hapus</c-rdp.button>
            <c-rdp.button variant="ghost" href="{{% url '{app}:{name_lower}-list' %}}">Batal</c-rdp.button>
        </form>
    </c-rdp.card>

</c-layout.app>
"""


def run_new_crud(args):
    """
    TUJUAN: Generate CRUD views + templates + form + URL entries.

    Penggunaan:
      rdp new crud <nama> -a <app>
      rdp new crud <nama> -a <app> --only list,create
      rdp new crud <nama> -a <app> --style card|table|simple

    ALUR:
      1. Parse nama, app, dan flags
      2. Tentukan halaman yang akan di-generate
      3. Generate views, form, templates
      4. Inject URL patterns ke urls.py

    DIPANGGIL DARI: main()
    """
    name, app = get_app_from_args(args)
    if not name or not app:
        print("[ERROR] Penggunaan: rdp new crud <nama> -a <nama-app>")
        sys.exit(1)

    app_dir = os.path.join("apps", app)
    if not os.path.exists(app_dir):
        print(f"[ERROR] Aplikasi '{app}' tidak ditemukan.")
        sys.exit(1)

    flags = _parse_flags(args)

    # Tentukan halaman yang akan di-generate
    if flags["only"]:
        pages = [p for p in flags["only"] if p in CRUD_PAGES]
        invalid = [p for p in flags["only"] if p not in CRUD_PAGES]
        if invalid:
            print(f"  [WARNING] Halaman tidak dikenal: {', '.join(invalid)}. Pilihan valid: {', '.join(CRUD_PAGES)}")
        if not pages:
            print("[ERROR] Tidak ada halaman valid yang dipilih.")
            sys.exit(1)
    else:
        pages = list(CRUD_PAGES)

    name_lower = name.lower()
    class_name = _to_class_name(name)
    verbose = " ".join(x.capitalize() for x in name.split("_"))
    style = flags["style"]

    print(f"\nGenerate CRUD '{class_name}' untuk app '{app}'...")
    print(f"  Halaman : {', '.join(pages)}")
    print(f"  Style   : {style}")
    print()

    # 1. Views — return [] jika file sudah ada (skip)
    written_views = _inject_views(app, name, pages) or []

    # 2. Form (butuh untuk create/edit, dan hanya jika view baru ditulis)
    if written_views and ("create" in pages or "edit" in pages):
        _inject_form(app, name)

    # 3. Templates
    tpl_dir = os.path.join("templates", "apps", app)
    os.makedirs(tpl_dir, exist_ok=True)

    tpl_map = {
        "list":   (f"{name_lower}_list.html",           _generate_list_template(app, name, verbose, style)),
        "create": (f"{name_lower}_form.html",            _generate_form_template(app, name, verbose)),
        "edit":   (f"{name_lower}_form.html",            _generate_form_template(app, name, verbose)),  # sama dengan create
        "detail": (f"{name_lower}_detail.html",          _generate_detail_template(app, name, verbose)),
        "delete": (f"{name_lower}_confirm_delete.html",  _generate_delete_template(app, name, verbose)),
    }

    written_templates = set()
    for page in pages:
        if page not in tpl_map:
            continue
        tpl_file, tpl_content = tpl_map[page]
        if tpl_file in written_templates:
            continue  # create dan edit share form.html — tulis sekali
        tpl_path = os.path.join(tpl_dir, tpl_file)
        if os.path.exists(tpl_path):
            print(f"  [WARNING] Template '{tpl_file}' sudah ada, dilewati.")
        else:
            with open(tpl_path, 'w', encoding='utf-8') as f:
                f.write(tpl_content)
            print(f"  [OK] Template: templates/apps/{app}/{tpl_file}")
        written_templates.add(tpl_file)

    # 4. URL injection — hanya untuk view yang benar-benar ditulis
    if written_views:
        _inject_url(app, name, pages)

    print()
    print(f"  [OK] CRUD '{class_name}' selesai.")
    print(f"  [INFO] Pastikan model {class_name} sudah ada. Jika belum: rdp new model {name_lower} -a {app}")


def run_new_page(args):
    """
    TUJUAN: Generate satu halaman UI spesifik atau halaman custom kosong.

    Penggunaan:
      rdp new page list -a <app> --model <Model>
      rdp new page create -a <app> --model <Model>
      rdp new page edit -a <app> --model <Model>
      rdp new page delete -a <app> --model <Model>
      rdp new page detail -a <app> --model <Model>
      rdp new page custom <nama> -a <app>

    ALUR:
      1. Parse tipe halaman (list/create/edit/delete/detail/custom)
      2. Jika CRUD page: generate template + view + form (jika perlu) + URL
      3. Jika custom: buat template kosong dengan layout app

    DIPANGGIL DARI: main()
    """
    if not args:
        print("[ERROR] Penggunaan: rdp new page <tipe|custom <nama>> -a <app> [--model <Model>] [--style table|card|simple]")
        sys.exit(1)

    page_type = args[0].lower()

    # Handle "rdp new page custom <nama> -a <app>"
    if page_type == "custom":
        if len(args) < 2:
            print("[ERROR] Penggunaan: rdp new page custom <nama> -a <app>")
            sys.exit(1)
        custom_name = args[1]
        _, app = get_app_from_args(args[1:])
        if not app:
            print("[ERROR] Tambahkan -a <nama-app>")
            sys.exit(1)

        tpl_dir = os.path.join("templates", "apps", app)
        os.makedirs(tpl_dir, exist_ok=True)
        page_path = os.path.join(tpl_dir, f"{custom_name.lower()}.html")

        if os.path.exists(page_path):
            print(f"[ERROR] Page '{custom_name}' sudah ada di {page_path}.")
            sys.exit(1)

        page_content = f"""\
{{# templates/apps/{app}/{custom_name.lower()}.html #}}
<c-layout.app title="{custom_name.capitalize()}">

    <div class="rdp-page-header">
        <h2 class="rdp-page-header__title">{custom_name.capitalize()}</h2>
    </div>

    <c-rdp.card>
        <p>Konten halaman {custom_name}.</p>
    </c-rdp.card>

</c-layout.app>
"""
        with open(page_path, 'w', encoding='utf-8') as f:
            f.write(page_content)
        print(f"  [OK] Page custom '{custom_name}' dibuat di {page_path}")
        return

    # Handle CRUD page types
    if page_type not in CRUD_PAGES:
        print(f"[ERROR] Tipe halaman '{page_type}' tidak dikenal.")
        print(f"  Pilihan: {', '.join(CRUD_PAGES)}, custom")
        sys.exit(1)

    # Untuk CRUD page, butuh -a dan --model
    _, app = get_app_from_args(args)
    if not app:
        print("[ERROR] Tambahkan -a <nama-app>")
        sys.exit(1)

    flags = _parse_flags(args)
    model_name = flags.get("model")

    if not model_name:
        # Tanya interaktif
        model_name = get_input(f"Nama model untuk halaman {page_type}", default="Item")

    style = flags.get("style", "table")
    name = model_name
    name_lower = name.lower()
    verbose = " ".join(x.capitalize() for x in name.split("_"))

    app_dir = os.path.join("apps", app)
    if not os.path.exists(app_dir):
        print(f"[ERROR] Aplikasi '{app}' tidak ditemukan.")
        sys.exit(1)

    print(f"\nGenerate halaman '{page_type}' untuk model '{name}' di app '{app}'...")

    # Generate hanya halaman yang diminta
    written_views = _inject_views(app, name, [page_type]) or []
    if written_views and page_type in ("create", "edit"):
        _inject_form(app, name)
    if written_views:
        _inject_url(app, name, [page_type])

    tpl_dir = os.path.join("templates", "apps", app)
    os.makedirs(tpl_dir, exist_ok=True)

    tpl_map = {
        "list":   (f"{name_lower}_list.html",           _generate_list_template(app, name, verbose, style)),
        "create": (f"{name_lower}_form.html",            _generate_form_template(app, name, verbose)),
        "edit":   (f"{name_lower}_form.html",            _generate_form_template(app, name, verbose)),
        "detail": (f"{name_lower}_detail.html",          _generate_detail_template(app, name, verbose)),
        "delete": (f"{name_lower}_confirm_delete.html",  _generate_delete_template(app, name, verbose)),
    }

    tpl_file, tpl_content = tpl_map[page_type]
    tpl_path = os.path.join(tpl_dir, tpl_file)
    if os.path.exists(tpl_path):
        print(f"  [WARNING] Template '{tpl_file}' sudah ada, dilewati.")
    else:
        with open(tpl_path, 'w', encoding='utf-8') as f:
            f.write(tpl_content)
        print(f"  [OK] Template: templates/apps/{app}/{tpl_file}")

    print(f"\n  [OK] Halaman '{page_type}' untuk {name} selesai.")


def run_make(args):
    """Wizard interaktif untuk berbagai generator."""
    from .app import run_new_app, run_new_api
    from .code import (
        run_new_component, run_new_model, run_new_task,
        run_new_service, run_new_test,
    )

    print("=" * 60)
    print("  RDP CLI - Interactive Wizard")
    print("=" * 60)
    print("Apa yang ingin dibuat?")
    print("  1. App")
    print("  2. Model")
    print("  3. CRUD (full: list, create, edit, delete, detail)")
    print("  4. API Skeleton")
    print("  5. Component Cotton")
    print("  6. Background Task (Celery)")
    print("  7. Service")
    print("  8. Test (Pytest)")
    print("  9. Satu halaman (list/create/edit/delete/detail/custom)")

    choice = get_input("Pilih opsi (1-9)")
    if choice not in [str(i) for i in range(1, 10)]:
        print("[ERROR] Pilihan tidak valid.")
        return

    if choice == "1":
        name = get_input("Nama App")
        run_new_app([name])
    elif choice == "4":
        app = get_input("Nama Aplikasi target")
        run_new_api([app])
    elif choice == "5":
        name = get_input("Nama Component")
        run_new_component([name])
    elif choice == "9":
        app = get_input("Nama Aplikasi target (-a)")
        print(f"  Tipe halaman: {', '.join(CRUD_PAGES)}, custom")
        page_type = get_input("Tipe halaman")
        if page_type == "custom":
            nama = get_input("Nama halaman custom")
            run_new_page([page_type, nama, "-a", app])
        else:
            model = get_input("Nama model (contoh: Produk)")
            style = get_input("Style (table/card/simple)", default="table")
            run_new_page([page_type, "-a", app, "--model", model, "--style", style])
    else:
        app = get_input("Nama Aplikasi target (-a)")
        name = get_input("Nama Entitas")
        if choice == "2":
            run_new_model([name, "-a", app])
        elif choice == "3":
            style = get_input("Style template (table/card/simple)", default="table")
            run_new_crud([name, "-a", app, "--style", style])
        elif choice == "6":
            run_new_task([name, "-a", app])
        elif choice == "7":
            run_new_service([name, "-a", app])
        elif choice == "8":
            run_new_test([name, "-a", app])


def run_scaffold(args):
    """Membuat modul lengkap dari model, view, hingga API dan test."""
    from .app import run_new_api
    from .code import run_new_model, run_new_test

    name, app = get_app_from_args(args)
    if not name or not app:
        print("[ERROR] Penggunaan: rdp scaffold <nama> -a <nama-app>")
        sys.exit(1)

    print(f"\n> Scaffold '{name}' untuk app '{app}' dimulai...")

    try:
        run_new_model([name, "-a", app])
    except SystemExit:
        pass

    try:
        run_new_crud([name, "-a", app])
    except SystemExit:
        pass

    try:
        run_new_api([app])
    except SystemExit:
        pass

    try:
        run_new_test([name, "-a", app])
    except SystemExit:
        pass

    print(f"\n  [OK] Scaffold '{name}' selesai!")
