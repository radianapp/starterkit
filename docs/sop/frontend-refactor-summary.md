# Ringkasan Perubahan Frontend — Sesi 2026-07-01

**Sesi ini:** Refaktor template layout, implementasi dark mode, perbaikan sidebar tablet
**Status:** ✅ Selesai — 10/10 tests passed

---

## Perubahan Utama

### 1. Refaktor Layout Template ke `<c-layout.base>`

**Sebelum:** Semua halaman menggunakan `{% extends xbase.html %}` dengan block system Django.
**Sesudah:** Semua halaman menggunakan komponen Cotton `<c-layout.base>` dengan slot variables.

**File yang berubah:**
- `templates/cotton/layout/base.html` — Layout dasar (dipindah dari `layouts/` ke `layout/`)
- `templates/dashboard/index.html` — Direfaktor penuh ke `<c-layout.base>`
- `templates/errors/404.html` — Direfaktor ke `<c-layout.base>`
- `templates/errors/403.html` — Direfaktor ke `<c-layout.base>`
- `templates/errors/500.html` — Direfaktor ke `<c-layout.base>`

> **PENTING:** Di dalam file komponen Cotton (layout/base.html), gunakan `{{ slot }}`, `{{ sidebar }}`, `{{ head }}`, `{{ navbar_actions }}` — BUKAN `<c-slot name=...>`. Tag `<c-slot>` hanya dipakai pada halaman yang *memanggil* komponen.

### 2. Slot tersedia di `<c-layout.base>`

| Slot | Deskripsi |
|------|-----------|
| `head` | CSS/meta tambahan di `<head>` |
| `navbar_actions` | Tombol kanan navbar |
| `sidebar` | Seluruh konten sidebar (brand + nav + footer) |
| *(default)* | Main content area — langsung di dalam tag |
| `footer` | Footer content |
| `extra_js` | Script tambahan sebelum `</body>` |

### 3. Dark Mode Toggle

- State `darkMode` + method `toggleDarkMode()` + `applyTheme()` di `layout-state.js`
- Persistensi ke `localStorage` — mode tersimpan antar sesi
- Fallback ke `prefers-color-scheme` jika belum pernah di-toggle manual
- Class `html.dark` ditambah/dihapus pada `<html>` element via JS
- Ikon toggle: 🌙 (light) / ☀️ (dark)
- Dark mode CSS di `base.css` dan `dashboard.css` menggunakan selector `html.dark .xxx`

### 4. Sidebar Tablet (768px–1024px)

- `--sidebar-width: 220px` untuk breakpoint tablet
- `rdp-sidebar__link-text` dan `rdp-sidebar__brand-text` dipaksa tampil dengan `display: inline-block !important`

---

## Cara Membuat Halaman Baru

`html
{% load static %}
{% load cotton %}

<c-layout.base title=Judul Halaman navbar_brand=Nama Brand>

    <c-slot name=head>
        <link rel=stylesheet href={% static 'css/nama-halaman.css' %}>
    </c-slot>

    <c-slot name=navbar_actions>
        <!-- tombol dark mode, notifikasi, avatar, dll -->
    </c-slot>

    <c-slot name=sidebar>
        <!-- brand + nav links + sidebar footer -->
    </c-slot>

    <!-- Main content — langsung tanpa slot name -->
    <div class=rdp-dashboard-content>
        <h1>Judul Konten</h1>
    </div>

</c-layout.base>
`
