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

    DIPANGGIL DARI: views/{name_lower}.py ({class_name}CreateModalView, {class_name}EditModalView)
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


def _inject_views(app: str, name: str, pages: list):
    """
    TUJUAN: Generate view file dan inject ke views/__init__.py.
    Menggunakan modal views untuk HTMX (CreateModalView, EditModalView, DeleteModalView).

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

    # Buat views/__init__.py jika belum ada
    init_path = os.path.join(views_dir, "__init__.py")
    if not os.path.exists(init_path):
        with open(init_path, 'w', encoding='utf-8') as f:
            f.write("")

    # Build view class content berdasarkan halaman yang diminta
    view_lines = [
        f"# apps/{app}/views/{name_lower}.py\n",
        "from django.contrib.auth.mixins import LoginRequiredMixin",
        "from django.http import HttpResponse",
        "from django.urls import reverse_lazy",
        "from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView",
        "from django.template.loader import render_to_string\n",
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

    def get_queryset(self):
        \"\"\"Filter queryset berdasarkan parameter q (pencarian).\"\"\"
        qs = super().get_queryset()
        q = self.request.GET.get("q", "").strip()
        if q:
            qs = qs.filter(name__icontains=q)
        return qs

""")
        exported.append(f"{class_name}ListView")

    if "create" in pages:
        view_lines.append(f"""\
class {class_name}CreateModalView(LoginRequiredMixin, CreateView):
    \"\"\"
    TUJUAN: Tampilkan modal form tambah {class_name} (HTMX partial).

    DIPANGGIL DARI: urls.py → name="{name_lower}-create-modal" (GET)
                    urls.py → name="{name_lower}-create" (POST)
    \"\"\"

    model = {class_name}
    form_class = {class_name}Form
    template_name = "apps/{app}/{name_lower}_create_modal.html"

    def get(self, request, *args, **kwargs):
        \"\"\"Tampilkan modal create — response partial HTML.\"\"\"
        form = self.form_class()
        html = render_to_string(self.template_name, {{"form": form}}, request=request)
        return HttpResponse(html)

    def form_valid(self, form):
        \"\"\"Simpan data, trigger reload halaman via HX-Refresh.\"\"\"
        self.object = form.save()
        response = HttpResponse("")
        response["HX-Refresh"] = "true"
        return response

    def form_invalid(self, form):
        \"\"\"Kembalikan modal dengan error — HTTP 422 agar HTMX tahu ini error.\"\"\"
        html = render_to_string(self.template_name, {{"form": form}}, request=self.request)
        return HttpResponse(html, status=422)

""")
        exported.append(f"{class_name}CreateModalView")

    if "edit" in pages:
        view_lines.append(f"""\
class {class_name}EditModalView(LoginRequiredMixin, UpdateView):
    \"\"\"
    TUJUAN: Tampilkan modal form edit {class_name} (HTMX partial).

    DIPANGGIL DARI: urls.py → name="{name_lower}-edit-modal" (GET)
                    urls.py → name="{name_lower}-edit" (POST)
    \"\"\"

    model = {class_name}
    form_class = {class_name}Form
    template_name = "apps/{app}/{name_lower}_edit_modal.html"

    def get(self, request, *args, **kwargs):
        \"\"\"Tampilkan modal edit dengan data yang ada — response partial HTML.\"\"\"
        self.object = self.get_object()
        form = self.form_class(instance=self.object)
        html = render_to_string(self.template_name, {{"form": form, "object": self.object}}, request=request)
        return HttpResponse(html)

    def form_valid(self, form):
        \"\"\"Simpan perubahan, trigger reload halaman.\"\"\"
        self.object = form.save()
        response = HttpResponse("")
        response["HX-Refresh"] = "true"
        return response

    def form_invalid(self, form):
        \"\"\"Kembalikan modal dengan error — HTTP 422.\"\"\"
        html = render_to_string(self.template_name, {{"form": form, "object": self.object}}, request=self.request)
        return HttpResponse(html, status=422)

""")
        exported.append(f"{class_name}EditModalView")

    if "delete" in pages:
        view_lines.append(f"""\
class {class_name}DeleteModalView(LoginRequiredMixin, DeleteView):
    \"\"\"
    TUJUAN: Tampilkan modal konfirmasi hapus (GET) dan proses hapus (DELETE/POST).

    DIPANGGIL DARI: urls.py → name="{name_lower}-delete-modal" (GET)
                    urls.py → name="{name_lower}-delete" (DELETE/POST)
    \"\"\"

    model = {class_name}
    template_name = "apps/{app}/{name_lower}_delete_modal.html"
    success_url = reverse_lazy("{app}:{name_lower}-list")

    def get(self, request, *args, **kwargs):
        \"\"\"Tampilkan modal konfirmasi hapus — response partial HTML.\"\"\"
        self.object = self.get_object()
        html = render_to_string(self.template_name, {{"object": self.object}}, request=request)
        return HttpResponse(html)

    def delete(self, request, *args, **kwargs):
        \"\"\"Hapus object, tutup modal + refresh halaman.\"\"\"
        self.object = self.get_object()
        self.object.delete()
        response = HttpResponse("")
        response["HX-Refresh"] = "true"
        return response

    # Alias untuk POST (karena HTMX form pakai hx-delete → method override)
    post = delete

""")
        exported.append(f"{class_name}DeleteModalView")

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

    with open(view_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(view_lines))

    # Inject ke __init__.py
    import_line = f"from .{name_lower} import {', '.join(exported)}\n"
    with open(init_path, 'a', encoding='utf-8') as f:
        f.write(import_line)

    print(f"  [OK] Views dibuat di {view_path}")
    return exported


def _inject_url(app: str, name: str, pages: list):
    """
    TUJUAN: Inject URL patterns ke apps/{app}/urls.py.
    Sekarang juga inject URL untuk modal views (create-modal, edit-modal, delete-modal).

    DIPANGGIL DARI: run_new_crud()
    """
    urls_path = os.path.join("apps", app, "urls.py")
    name_lower = name.lower()
    class_name = _to_class_name(name)

    # Mapping halaman → view class dan URL pattern (termasuk modal views)
    page_map = {
        "list": (
            f"{class_name}ListView",
            (f'path("{name_lower}/", {class_name}ListView.as_view(), name="{name_lower}-list"),\n    '
             f'path("", {class_name}ListView.as_view(), name="list"),'),
        ),
        "detail": (
            f"{class_name}DetailView",
            f'path("{name_lower}/<int:pk>/", {class_name}DetailView.as_view(), name="{name_lower}-detail"),',
        ),
        "create": (
            f"{class_name}CreateModalView",
            (f'path("{name_lower}/baru/", {class_name}CreateModalView.as_view(), name="{name_lower}-create"),\n    '
             f'path("{name_lower}/baru/modal/", {class_name}CreateModalView.as_view(), name="{name_lower}-create-modal"),'),
        ),
        "edit": (
            f"{class_name}EditModalView",
            (f'path("{name_lower}/<int:pk>/edit/", {class_name}EditModalView.as_view(), name="{name_lower}-edit"),\n    '
             f'path("{name_lower}/<int:pk>/edit/modal/", {class_name}EditModalView.as_view(), name="{name_lower}-edit-modal"),'),
        ),
        "delete": (
            f"{class_name}DeleteModalView",
            (f'path("{name_lower}/<int:pk>/hapus/", {class_name}DeleteModalView.as_view(), name="{name_lower}-delete"),\n    '
             f'path("{name_lower}/<int:pk>/hapus/modal/", {class_name}DeleteModalView.as_view(), name="{name_lower}-delete-modal"),'),
        ),
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
        if "from .views import" in existing:
            import_line = "from .views import (\n"
            if import_line in existing:
                sep = ",\n    "
                new_imports_str = sep.join(new_imports)
                existing = existing.replace(
                    ")\n\napp_name",
                    "    " + new_imports_str + ",\n)\n\napp_name",
                    1,
                )
            else:
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


# ── Template Generators ───────────────────────────────────────────────────────


def _generate_list_template(app: str, name: str, verbose: str, style: str) -> str:
    """
    Generate template list sesuai style (table/card/simple).
    Table style mengikuti design Produk List.dc.html — tabel + modal inline HTMX.

    DIPANGGIL DARI: run_new_crud(), run_new_page()
    """
    name_lower = name.lower()

    if style == "card":
        return f"""\
{{# templates/apps/{app}/{name_lower}_list.html #}}
<c-layout.app title="Daftar {verbose}">

    <ul class="rdp-breadcrumb"><li><a href="{{% url 'dashboard:index' %}}">Dashboard</a></li><li>Daftar {verbose}</li></ul>
    <div class="rdp-page-header" style="margin-top:10px;margin-bottom:16px">
        <h1 class="rdp-page-header__title">Daftar {verbose}</h1>
    </div>

    <div id="toast-area" aria-live="polite"></div>

    <div style="display:flex;justify-content:flex-end;margin-bottom:12px">
        <button id="btn-tambah-{name_lower}" class="rdp-btn rdp-btn--primary rdp-btn--sm"
                hx-get="{{% url '{app}:{name_lower}-create-modal' %}}"
                hx-target="#modal-container" hx-swap="innerHTML">
            + Tambah {verbose}
        </button>
    </div>

    <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:16px">
        {{% for item in items %}}
        <div class="rdp-card" style="padding:16px;display:flex;flex-direction:column;gap:12px">
            <div style="font-weight:600;font-size:14px">{{{{ item.name }}}}</div>
            {{% if item.is_active %}}
                <span class="rdp-badge rdp-badge--success">Aktif</span>
            {{% else %}}
                <span class="rdp-badge rdp-badge--neutral">Nonaktif</span>
            {{% endif %}}
            <div style="display:flex;gap:6px;margin-top:auto">
                <button id="btn-edit-{name_lower}-{{{{ item.pk }}}}" class="rdp-btn rdp-btn--ghost rdp-btn--sm"
                        hx-get="{{% url '{app}:{name_lower}-edit-modal' item.pk %}}"
                        hx-target="#modal-container" hx-swap="innerHTML">Edit</button>
                <button id="btn-hapus-{name_lower}-{{{{ item.pk }}}}" class="rdp-btn rdp-btn--ghost rdp-btn--sm" style="color:var(--rdp-danger)"
                        hx-get="{{% url '{app}:{name_lower}-delete-modal' item.pk %}}"
                        hx-target="#modal-container" hx-swap="innerHTML">Hapus</button>
            </div>
        </div>
        {{% empty %}}
        <div style="grid-column:1/-1;padding:64px 24px;text-align:center;border:1.5px dashed var(--rdp-border-strong);border-radius:14px;display:flex;flex-direction:column;align-items:center;gap:10px">
            <span style="font-size:17px;font-weight:600">Belum ada {verbose}</span>
            <button class="rdp-btn rdp-btn--primary rdp-btn--sm" style="margin-top:6px"
                    hx-get="{{% url '{app}:{name_lower}-create-modal' %}}"
                    hx-target="#modal-container" hx-swap="innerHTML">+ Tambah {verbose}</button>
        </div>
        {{% endfor %}}
    </div>

    {{% if is_paginated %}}
    <div style="display:flex;align-items:center;justify-content:space-between;margin-top:14px">
        <span style="font-size:12.5px;color:var(--rdp-text-muted)">Halaman {{{{ page_obj.number }}}} dari {{{{ page_obj.paginator.num_pages }}}}</span>
        <div style="display:flex;gap:6px">
            {{% if page_obj.has_previous %}}<a href="?page={{{{ page_obj.previous_page_number }}}}" class="rdp-btn rdp-btn--sm">Sebelumnya</a>{{% endif %}}
            {{% if page_obj.has_next %}}<a href="?page={{{{ page_obj.next_page_number }}}}" class="rdp-btn rdp-btn--sm">Berikutnya</a>{{% endif %}}
        </div>
    </div>
    {{% endif %}}

    <div id="modal-container"></div>

</c-layout.app>
"""

    elif style == "simple":
        return f"""\
{{# templates/apps/{app}/{name_lower}_list.html #}}
<c-layout.app title="Daftar {verbose}">

    <ul class="rdp-breadcrumb"><li><a href="{{% url 'dashboard:index' %}}">Dashboard</a></li><li>Daftar {verbose}</li></ul>
    <div class="rdp-page-header" style="margin-top:10px;margin-bottom:16px">
        <h1 class="rdp-page-header__title">Daftar {verbose}</h1>
    </div>

    <div id="toast-area" aria-live="polite"></div>

    <button id="btn-tambah-{name_lower}" class="rdp-btn rdp-btn--primary rdp-btn--sm" style="margin-bottom:12px"
            hx-get="{{% url '{app}:{name_lower}-create-modal' %}}"
            hx-target="#modal-container" hx-swap="innerHTML">+ Tambah {verbose}</button>

    <ul>
        {{% for item in items %}}
        <li style="padding:8px 0;border-bottom:1px solid var(--rdp-border)">
            {{{{ item.name }}}}
            <button id="btn-edit-{name_lower}-{{{{ item.pk }}}}" class="rdp-btn rdp-btn--ghost rdp-btn--xs" style="margin-left:8px"
                    hx-get="{{% url '{app}:{name_lower}-edit-modal' item.pk %}}"
                    hx-target="#modal-container" hx-swap="innerHTML">Edit</button>
            <button id="btn-hapus-{name_lower}-{{{{ item.pk }}}}" class="rdp-btn rdp-btn--ghost rdp-btn--xs" style="margin-left:4px;color:var(--rdp-danger)"
                    hx-get="{{% url '{app}:{name_lower}-delete-modal' item.pk %}}"
                    hx-target="#modal-container" hx-swap="innerHTML">Hapus</button>
        </li>
        {{% empty %}}
        <li style="color:var(--rdp-text-muted);padding:16px 0">Belum ada data {verbose}.</li>
        {{% endfor %}}
    </ul>

    <div id="modal-container"></div>

</c-layout.app>
"""

    else:  # table (default) — presisi 1:1 dengan Produk List.dc.html
        return f"""\
{{# templates/apps/{app}/{name_lower}_list.html #}}
{{# US: RDP Dashboard Shell — Tabel Presisi 1:1 Produk List design #}}
<c-layout.app title="Daftar {verbose}">

    {{# ── Breadcrumb ─────────────────────────────────────── #}}
    <ul class="rdp-breadcrumb">
        <li><a href="{{% url 'dashboard:index' %}}">Katalog</a></li>
        <li>Daftar {verbose}</li>
    </ul>

    {{# ── Page Header ────────────────────────────────────── #}}
    <div class="rdp-page-header" style="margin-top:10px;margin-bottom:16px">
        <h1 class="rdp-page-header__title">{verbose}</h1>
    </div>

    {{# ── Toast feedback area ────────────────────────────── #}}
    <div id="toast-area" aria-live="polite"></div>

    {{# ── Filter & Search Bar ─────────────────────────────── #}}
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:14px;flex-wrap:wrap">
        <form method="GET" style="display:flex;align-items:center;gap:8px;flex:1;min-width:280px;margin:0">
            <div style="position:relative;width:260px;flex-shrink:0">
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="position:absolute;left:10px;top:50%;transform:translateY(-50%);color:var(--rdp-text-muted);pointer-events:none"><circle cx="11" cy="11" r="8"></circle><path d="m21 21-4.3-4.3"></path></svg>
                <input class="rdp-input" name="q" placeholder="Cari {verbose}..." value="{{% if request.GET.q %}}{{{{ request.GET.q }}}}{{% endif %}}" style="width:100%;height:36px;padding:0 12px 0 32px;margin:0;font-size:13.5px;box-sizing:border-box">
            </div>
            <button type="submit" class="rdp-btn rdp-btn--sm" style="height:36px">Filter</button>
        </form>
        <div style="flex:1"></div>
        <button id="btn-tambah-{name_lower}" class="rdp-btn rdp-btn--primary rdp-btn--sm" style="height:36px"
                hx-get="{{% url '{app}:{name_lower}-create-modal' %}}"
                hx-target="#modal-container"
                hx-swap="innerHTML">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"></path><path d="M12 5v14"></path></svg>
            Tambah {verbose}
        </button>
    </div>

    {{# ── Tabel Data ──────────────────────────────────────── #}}
    {{% if items %}}
    <div class="rdp-table-wrapper" style="background:var(--rdp-surface,#FFFFFF);border:1px solid var(--rdp-border);border-radius:12px;overflow:hidden">
        <table class="rdp-table" style="width:100%;border-collapse:collapse">
            <thead>
                <tr style="border-bottom:1px solid var(--rdp-border)">
                    <th style="padding:10px 14px;font-size:12px;font-weight:600;color:var(--rdp-text-muted);text-transform:uppercase;letter-spacing:0.04em">Nama</th>
                    <th style="padding:10px 14px;font-size:12px;font-weight:600;color:var(--rdp-text-muted);text-transform:uppercase;letter-spacing:0.04em">Status</th>
                    <th style="padding:10px 14px;font-size:12px;font-weight:600;color:var(--rdp-text-muted);text-transform:uppercase;letter-spacing:0.04em">Dibuat</th>
                    <th style="padding:10px 14px;text-align:right"></th>
                </tr>
            </thead>
            <tbody>
                {{% for item in items %}}
                <tr class="pos-row" style="border-bottom:1px solid var(--rdp-border);transition:background 0.1s;cursor:pointer">
                    <td style="padding:12px 14px;font-weight:500;font-size:13.5px;color:var(--rdp-text)">{{{{ item.name }}}}</td>
                    <td style="padding:12px 14px">
                        {{% if item.is_active %}}
                            <span class="rdp-badge rdp-badge--success" style="font-size:11px">Aktif</span>
                        {{% else %}}
                            <span class="rdp-badge rdp-badge--neutral" style="font-size:11px">Nonaktif</span>
                        {{% endif %}}
                    </td>
                    <td style="padding:12px 14px;font-family:var(--rdp-font-mono,'IBM Plex Mono',monospace);font-size:12.5px;color:var(--rdp-text-muted)">{{{{ item.created_at|date:"d M Y" }}}}</td>
                    <td style="padding:6px 14px;text-align:right;width:100px">
                        <span class="row-actions" style="display:inline-flex;gap:4px;justify-content:flex-end">
                            <button id="btn-edit-{name_lower}-{{{{ item.pk }}}}" title="Edit"
                                    class="rdp-btn rdp-btn--ghost rdp-btn--icon rdp-btn--xs"
                                    style="width:28px;height:28px"
                                    hx-get="{{% url '{app}:{name_lower}-edit-modal' item.pk %}}"
                                    hx-target="#modal-container"
                                    hx-swap="innerHTML">
                                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M17 3a2.85 2.83 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5Z"></path></svg>
                            </button>
                            <button id="btn-hapus-{name_lower}-{{{{ item.pk }}}}" title="Hapus"
                                    class="rdp-btn rdp-btn--ghost rdp-btn--icon rdp-btn--xs"
                                    style="width:28px;height:28px;color:var(--rdp-danger)"
                                    hx-get="{{% url '{app}:{name_lower}-delete-modal' item.pk %}}"
                                    hx-target="#modal-container"
                                    hx-swap="innerHTML">
                                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M3 6h18"></path><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6"></path><path d="M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path></svg>
                            </button>
                        </span>
                    </td>
                </tr>
                {{% endfor %}}
            </tbody>
        </table>
    </div>

    {{# ── Pagination ─────────────────────────────────────── #}}
    {{% if is_paginated %}}
    <div style="display:flex;align-items:center;justify-content:space-between;margin-top:14px">
        <span style="font-size:12.5px;color:var(--rdp-text-muted)">Menampilkan {{{{ page_obj.start_index }}}}–{{{{ page_obj.end_index }}}} dari {{{{ page_obj.paginator.count }}}}</span>
        <div style="display:flex;gap:6px">
            <button class="rdp-btn rdp-btn--sm" {{% if not page_obj.has_previous %}}disabled{{% endif %}}>
                {{% if page_obj.has_previous %}}<a href="?{{% if request.GET.q %}}q={{{{ request.GET.q }}}}&{{% endif %}}page={{{{ page_obj.previous_page_number }}}}" style="color:inherit;text-decoration:none">Sebelumnya</a>{{% else %}}Sebelumnya{{% endif %}}
            </button>
            <button class="rdp-btn rdp-btn--sm" {{% if not page_obj.has_next %}}disabled{{% endif %}}>
                {{% if page_obj.has_next %}}<a href="?{{% if request.GET.q %}}q={{{{ request.GET.q }}}}&{{% endif %}}page={{{{ page_obj.next_page_number }}}}" style="color:inherit;text-decoration:none">Berikutnya</a>{{% else %}}Berikutnya{{% endif %}}
            </button>
        </div>
    </div>
    {{% endif %}}

    {{% else %}}
    {{# ── Empty State ─────────────────────────────────────── #}}
    {{% if request.GET.q %}}
    <div style="border:1.5px dashed var(--rdp-border-strong);border-radius:14px;padding:48px 24px;display:flex;flex-direction:column;align-items:center;gap:8px">
        <span style="font-size:14px;font-weight:600">Tidak ada {verbose} yang cocok</span>
        <span style="font-size:13px;color:var(--rdp-text-muted)">Coba kata kunci lain.</span>
        <a href="{{% url '{app}:{name_lower}-list' %}}" class="rdp-btn rdp-btn--ghost rdp-btn--sm">Hapus pencarian</a>
    </div>
    {{% else %}}
    <div style="background:var(--rdp-surface,#FFFFFF);border:1px solid var(--rdp-border);border-radius:14px;padding:72px 24px;display:flex;flex-direction:column;align-items:center;gap:10px">
        <span style="width:56px;height:56px;border-radius:28px;background:var(--rdp-primary-soft,#EDF4F0);color:var(--rdp-primary,#15654E);display:inline-flex;align-items:center;justify-content:center">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="m7.5 4.27 9 5.15"></path><path d="M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16Z"></path><path d="M12 22V12"></path><path d="m3.3 7 8.7 5 8.7-5"></path></svg>
        </span>
        <span style="font-size:17px;font-weight:600;color:var(--rdp-text)">Belum ada {verbose}</span>
        <span style="font-size:13.5px;color:var(--rdp-text-muted);max-width:42ch;text-align:center;line-height:1.55">{verbose} yang kamu tambahkan akan tampil di sini. Mulai dengan menambahkan yang pertama.</span>
        <button class="rdp-btn rdp-btn--primary rdp-btn--sm" style="margin-top:6px"
                hx-get="{{% url '{app}:{name_lower}-create-modal' %}}"
                hx-target="#modal-container"
                hx-swap="innerHTML">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"></path><path d="M12 5v14"></path></svg>
            Tambah {verbose}
        </button>
    </div>
    {{% endif %}}
    {{% endif %}}

    {{# ── Modal container ─────────────────────────────────── #}}
    <div id="modal-container"></div>

</c-layout.app>
"""


def _generate_create_modal_template(app: str, name: str, verbose: str) -> str:
    """
    Generate partial template modal Tambah (Create) — mengikuti Tambah Produk Dialog.dc.html.
    Ini adalah HTMX partial response, bukan full page.

    DIPANGGIL DARI: run_new_crud, run_new_page
    """
    name_lower = name.lower()
    return f"""\
{{# templates/apps/{app}/{name_lower}_create_modal.html #}}
{{# Partial HTMX — dirender oleh {name}CreateModalView, di-inject ke #modal-container #}}
<div class="rdp-modal-backdrop"
     style="position:fixed;inset:0;z-index:200;background:rgba(28,27,24,0.5);backdrop-filter:blur(2px);display:flex;align-items:center;justify-content:center;padding:24px"
     onclick="if(event.target===this)document.getElementById('modal-container').innerHTML=''">
    <div class="rdp-modal rdp-modal--md"
         style="position:relative;width:100%;max-width:560px;max-height:calc(100vh - 96px);display:flex;flex-direction:column;background:var(--rdp-surface)"
         onclick="event.stopPropagation()">

        <div class="rdp-modal__header">
            <h2 class="rdp-modal__title">Tambah {verbose} Baru</h2>
            <button title="Tutup" class="rdp-modal__close"
                    onclick="document.getElementById('modal-container').innerHTML=''">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M18 6 6 18"></path><path d="m6 6 12 12"></path></svg>
            </button>
        </div>

        <div class="rdp-modal__body" style="overflow-y:auto;overflow-x:hidden">
            <form id="form-create-{name_lower}"
                  hx-post="{{% url '{app}:{name_lower}-create' %}}"
                  hx-target="#modal-container"
                  hx-swap="innerHTML"
                  style="display:flex;flex-direction:column;gap:16px">
                {{% csrf_token %}}

                {{{{ form.as_p }}}}

                <div class="rdp-modal__footer" style="display:flex;justify-content:flex-end;gap:8px;margin-top:8px;padding-top:16px;border-top:1px solid var(--rdp-border)">
                    <button type="button" class="rdp-btn rdp-btn--secondary"
                            onclick="document.getElementById('modal-container').innerHTML=''">Batal</button>
                    <button type="submit" id="btn-submit-create-{name_lower}" class="rdp-btn rdp-btn--primary" style="min-width:110px">
                        Simpan {verbose}
                    </button>
                </div>
            </form>
        </div>
    </div>
</div>
"""


def _generate_edit_modal_template(app: str, name: str, verbose: str) -> str:
    """
    Generate partial template modal Edit — mengikuti Edit Produk Modal.dc.html.
    Ini adalah HTMX partial response, bukan full page.

    DIPANGGIL DARI: run_new_crud, run_new_page
    """
    name_lower = name.lower()
    return f"""\
{{# templates/apps/{app}/{name_lower}_edit_modal.html #}}
{{# Partial HTMX — dirender oleh {name}EditModalView, di-inject ke #modal-container #}}
<div class="rdp-modal-backdrop"
     style="position:fixed;inset:0;z-index:200;background:rgba(28,27,24,0.5);backdrop-filter:blur(2px);display:flex;align-items:center;justify-content:center;padding:24px"
     onclick="if(event.target===this)document.getElementById('modal-container').innerHTML=''">
    <div class="rdp-modal rdp-modal--md"
         style="position:relative;width:100%;max-width:560px;max-height:calc(100vh - 96px);display:flex;flex-direction:column;background:var(--rdp-surface)"
         onclick="event.stopPropagation()">

        <div class="rdp-modal__header">
            <h2 class="rdp-modal__title">Edit {verbose}: {{{{ object.name }}}}</h2>
            <button title="Tutup" class="rdp-modal__close"
                    onclick="document.getElementById('modal-container').innerHTML=''">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M18 6 6 18"></path><path d="m6 6 12 12"></path></svg>
            </button>
        </div>

        <div class="rdp-modal__body" style="overflow-y:auto;overflow-x:hidden">
            <form id="form-edit-{name_lower}-{{{{ object.pk }}}}"
                  hx-post="{{% url '{app}:{name_lower}-edit' object.pk %}}"
                  hx-target="#modal-container"
                  hx-swap="innerHTML"
                  style="display:flex;flex-direction:column;gap:16px">
                {{% csrf_token %}}

                {{{{ form.as_p }}}}

                <div class="rdp-modal__footer" style="display:flex;justify-content:flex-end;gap:8px;margin-top:8px;padding-top:16px;border-top:1px solid var(--rdp-border)">
                    <button type="button" class="rdp-btn rdp-btn--secondary"
                            onclick="document.getElementById('modal-container').innerHTML=''">Batal</button>
                    <button type="submit" id="btn-submit-edit-{name_lower}" class="rdp-btn rdp-btn--primary" style="min-width:110px">
                        Simpan Perubahan
                    </button>
                </div>
            </form>
        </div>
    </div>
</div>
"""


def _generate_form_template(app: str, name: str, verbose: str) -> str:
    """
    Alias ke _generate_create_modal_template.
    Dipertahankan untuk backward compatibility.

    DIPANGGIL DARI: run_new_crud, run_new_page
    """
    return _generate_create_modal_template(app, name, verbose)


def _generate_delete_template(app: str, name: str, verbose: str) -> str:
    """
    Generate partial template modal Hapus — mengikuti Hapus Produk Dialog.dc.html.
    Dialog compact dengan preview item dan konfirmasi eksplisit.

    DIPANGGIL DARI: run_new_crud, run_new_page
    """
    name_lower = name.lower()
    return f"""\
{{# templates/apps/{app}/{name_lower}_delete_modal.html #}}
{{# Partial HTMX — dirender oleh {name}DeleteModalView, di-inject ke #modal-container #}}
<div class="rdp-modal-backdrop"
     style="position:fixed;inset:0;z-index:200;background:rgba(28,27,24,0.5);backdrop-filter:blur(2px);display:flex;align-items:center;justify-content:center;padding:24px"
     onclick="if(event.target===this)document.getElementById('modal-container').innerHTML=''">
    <div class="rdp-modal rdp-modal--sm"
         style="position:relative;width:100%;max-width:400px;display:flex;flex-direction:column;background:var(--rdp-surface)"
         onclick="event.stopPropagation()">

        <div class="rdp-modal__body" style="padding:24px 24px 20px;display:flex;flex-direction:column;gap:12px;overflow-x:hidden">
            <span style="width:44px;height:44px;border-radius:22px;background:var(--rdp-danger-soft,#FBEDEB);color:var(--rdp-danger);display:inline-flex;align-items:center;justify-content:center;flex-shrink:0">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M3 6h18"></path><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6"></path><path d="M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path></svg>
            </span>
            <h2 style="font-size:17px;font-weight:700;margin:0;letter-spacing:-0.01em;line-height:1.35">Hapus {verbose} "{{{{ object.name }}}}"?</h2>
            <p style="margin:0;font-size:13px;line-height:1.55;color:var(--rdp-text-muted)">Tindakan ini tidak bisa dibatalkan. Data akan dihapus secara permanen.</p>

            <div style="display:flex;align-items:center;gap:10px;background:var(--rdp-surface-sunken,#F3F1EC);border:1px solid var(--rdp-border);border-radius:10px;padding:10px 12px">
                <span style="display:flex;flex-direction:column;line-height:1.4;min-width:0;flex:1">
                    <span style="font-size:13px;font-weight:600">{{{{ object.name }}}}</span>
                    <span style="font-size:11.5px;font-family:'IBM Plex Mono',monospace;color:var(--rdp-text-muted)">ID: {{{{ object.pk }}}}</span>
                </span>
            </div>
        </div>

        <div class="rdp-modal__footer" style="display:flex;justify-content:flex-end;gap:8px;background:var(--rdp-background,#FAF9F7);border-radius:0 0 var(--rdp-radius-lg,14px) var(--rdp-radius-lg,14px)">
            <button class="rdp-btn rdp-btn--secondary"
                    onclick="document.getElementById('modal-container').innerHTML=''">Batal</button>
            <form hx-delete="{{% url '{app}:{name_lower}-delete' object.pk %}}"
                  hx-target="#modal-container"
                  hx-swap="innerHTML"
                  style="margin:0">
                {{% csrf_token %}}
                <button type="submit" id="btn-confirm-hapus-{name_lower}" class="rdp-btn rdp-btn--danger" style="min-width:96px">
                    <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M3 6h18"></path><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6"></path><path d="M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path></svg>
                    Hapus
                </button>
            </form>
        </div>
    </div>
</div>
"""


def _generate_detail_template(app: str, name: str, verbose: str) -> str:
    """Generate template detail view."""
    name_lower = name.lower()
    return f"""\
{{# templates/apps/{app}/{name_lower}_detail.html #}}
<c-layout.app title="{{{{ object.name }}}}">

    <ul class="rdp-breadcrumb">
        <li><a href="{{% url 'dashboard:index' %}}">Dashboard</a></li>
        <li><a href="{{% url '{app}:{name_lower}-list' %}}">Daftar {verbose}</a></li>
        <li>{{{{ object.name }}}}</li>
    </ul>

    <div class="rdp-page-header" style="margin-top:10px;margin-bottom:16px">
        <h1 class="rdp-page-header__title">{{{{ object.name }}}}</h1>
        <div class="rdp-page-header__actions">
            <button class="rdp-btn rdp-btn--secondary rdp-btn--sm"
                    hx-get="{{% url '{app}:{name_lower}-edit-modal' object.pk %}}"
                    hx-target="#modal-container"
                    hx-swap="innerHTML">Edit</button>
            <button class="rdp-btn rdp-btn--ghost rdp-btn--sm" style="color:var(--rdp-danger)"
                    hx-get="{{% url '{app}:{name_lower}-delete-modal' object.pk %}}"
                    hx-target="#modal-container"
                    hx-swap="innerHTML">Hapus</button>
        </div>
    </div>

    <div style="background:var(--rdp-surface);border:1px solid var(--rdp-border);border-radius:12px;padding:24px;max-width:640px">
        <dl style="display:grid;grid-template-columns:140px 1fr;gap:12px 16px;margin:0;font-size:13px">
            <dt style="font-weight:600;color:var(--rdp-text-muted)">Nama</dt>
            <dd style="margin:0;font-weight:600">{{{{ object.name }}}}</dd>

            <dt style="font-weight:600;color:var(--rdp-text-muted)">Deskripsi</dt>
            <dd style="margin:0">{{{{ object.description|default:"-" }}}}</dd>

            <dt style="font-weight:600;color:var(--rdp-text-muted)">Status</dt>
            <dd style="margin:0">
                {{% if object.is_active %}}
                    <span class="rdp-badge rdp-badge--success">Aktif</span>
                {{% else %}}
                    <span class="rdp-badge rdp-badge--neutral">Nonaktif</span>
                {{% endif %}}
            </dd>

            <dt style="font-weight:600;color:var(--rdp-text-muted)">Dibuat pada</dt>
            <dd style="margin:0;font-family:'IBM Plex Mono',monospace;font-size:12px">{{{{ object.created_at|date:"d M Y H:i" }}}}</dd>
        </dl>
    </div>

    <div style="margin-top:16px">
        <a href="{{% url '{app}:{name_lower}-list' %}}" class="rdp-btn rdp-btn--ghost rdp-btn--sm">← Kembali ke Daftar</a>
    </div>

    <div id="modal-container"></div>

</c-layout.app>
"""


# ── Runner Functions ──────────────────────────────────────────────────────────


def run_new_crud(args):
    """
    TUJUAN: Generate CRUD views (modal HTMX) + templates + form + URL entries.

    Penggunaan:
      rdp new crud <nama> -a <app>
      rdp new crud <nama> -a <app> --only list,create
      rdp new crud <nama> -a <app> --style card|table|simple

    ALUR:
      1. Parse nama, app, dan flags
      2. Tentukan halaman yang akan di-generate
      3. Generate views (modal), form, templates
      4. Inject URL patterns ke urls.py

    DIPANGGIL DARI: main()
    """
    name, app = get_app_from_args(args)
    if not name or not app:
        available_apps = []
        if os.path.exists("apps"):
            available_apps = [
                d for d in os.listdir("apps")
                if os.path.isdir(os.path.join("apps", d)) and not d.startswith("__") and not d.startswith(".")
            ]
        print("\n[ERROR] Aplikasi target belum ditentukan.")
        print("  Gunakan format: rdp new crud <nama> -a <nama-app>")
        if available_apps:
            print(f"  Aplikasi yang tersedia di apps/: {', '.join(available_apps)}")
            print(f"  Contoh: rdp new crud {name or 'item'} -a {available_apps[0]}")
        else:
            print("  Belum ada aplikasi yang dibuat. Buat aplikasi terlebih dahulu dengan:")
            print(f"    rdp new app {name or 'billing'}")
        sys.exit(1)

    app_dir = os.path.join("apps", app)
    if not os.path.exists(app_dir):
        print(f"\n[ERROR] Aplikasi '{app}' tidak ditemukan di folder apps/{app}.")
        print(f"  Buat aplikasi '{app}' terlebih dahulu dengan perintah:")
        print(f"    rdp new app {app}")
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

    # 3. Templates — mapping template file ke generator
    tpl_dir = os.path.join("templates", "apps", app)
    os.makedirs(tpl_dir, exist_ok=True)

    tpl_map = {
        "list":   (f"{name_lower}_list.html",          _generate_list_template(app, name, verbose, style)),
        "create": (f"{name_lower}_create_modal.html",  _generate_create_modal_template(app, name, verbose)),
        "edit":   (f"{name_lower}_edit_modal.html",    _generate_edit_modal_template(app, name, verbose)),
        "detail": (f"{name_lower}_detail.html",        _generate_detail_template(app, name, verbose)),
        "delete": (f"{name_lower}_delete_modal.html",  _generate_delete_template(app, name, verbose)),
    }

    written_templates = set()
    for page in pages:
        if page not in tpl_map:
            continue
        tpl_file, tpl_content = tpl_map[page]
        if tpl_file in written_templates:
            continue
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

    <ul class="rdp-breadcrumb"><li>Dashboard</li><li>{custom_name.capitalize()}</li></ul>
    <div class="rdp-page-header" style="margin-top:10px;margin-bottom:16px">
        <h1 class="rdp-page-header__title">{custom_name.capitalize()}</h1>
    </div>

    <div style="background:var(--rdp-surface);border:1px solid var(--rdp-border);border-radius:12px;padding:24px">
        <p style="color:var(--rdp-text-muted);font-size:14px">Konten halaman {custom_name}.</p>
    </div>

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

    _, app = get_app_from_args(args)
    if not app:
        print("[ERROR] Tambahkan -a <nama-app>")
        sys.exit(1)

    flags = _parse_flags(args)
    model_name = flags.get("model")

    if not model_name:
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

    written_views = _inject_views(app, name, [page_type]) or []
    if written_views and page_type in ("create", "edit"):
        _inject_form(app, name)
    if written_views:
        _inject_url(app, name, [page_type])

    tpl_dir = os.path.join("templates", "apps", app)
    os.makedirs(tpl_dir, exist_ok=True)

    tpl_map = {
        "list":   (f"{name_lower}_list.html",          _generate_list_template(app, name, verbose, style)),
        "create": (f"{name_lower}_create_modal.html",  _generate_create_modal_template(app, name, verbose)),
        "edit":   (f"{name_lower}_edit_modal.html",    _generate_edit_modal_template(app, name, verbose)),
        "detail": (f"{name_lower}_detail.html",        _generate_detail_template(app, name, verbose)),
        "delete": (f"{name_lower}_delete_modal.html",  _generate_delete_template(app, name, verbose)),
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
