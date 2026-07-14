# Komponen Kustom RDP UI

> **PENTING untuk AI/LLM**: Selalu baca dokumen ini sebelum membuat desain, kode, atau implementasi baru yang menyangkut UI.
> - **Gunakan komponen yang sudah ada** — jangan buat ulang HTML boilerplate yang sudah terkapsulasi di sini.
> - Jika membuat komponen baru, **wajib dokumentasikan** di sini sebelum commit.
> - Semua komponen berada di `templates/cotton/` dan dipanggil dengan sintaks `<c-{folder}.{nama}>`.

---

## Daftar Komponen Sidebar

Semua komponen sidebar berada di folder `templates/cotton/sidebar/`.

---

### `<c-sidebar.brand>`
Blok logo/brand di bagian paling atas sidebar.

- **File**: [`templates/cotton/sidebar/brand.html`](../templates/cotton/sidebar/brand.html)
- **CSS Classes**: `.rdp-sidebar__brand`, `.rdp-sidebar__brand-logo`, `.rdp-sidebar__brand-text` (di `static/css/base.css`)
- **Digunakan di**: `templates/cotton/layout/app.html`, semua halaman yang mendefinisikan ulang `<c-slot name="sidebar">`.
- **Parameter**:
  | Nama | Tipe | Default | Keterangan |
  |---|---|---|---|
  | `title` | string | `"RDP"` | Nama aplikasi/modul |
  | `href` | string | `"/"` | URL tujuan klik |
  | `initial` | string | *(kosong)* | Inisial khusus di kotak logo. Jika kosong, diambil dari huruf pertama `title` |

- **Contoh**:
  ```html
  {# Minimal #}
  <c-sidebar.brand title="Dashboard" />

  {# Dengan initial kustom dan href #}
  <c-sidebar.brand title="Design Tokens" initial="T" href="/tokens/" />
  ```
- **Kelebihan**: Konsisten secara visual; tidak ada inline CSS.
- **Kekurangan**: Hanya mendukung teks inisial — belum bisa menampilkan gambar/SVG logo kustom.

---

### `<c-sidebar.search>`
Kotak pencarian di dalam sidebar, biasanya terlihat di mode mobile drawer.

- **File**: [`templates/cotton/sidebar/search.html`](../templates/cotton/sidebar/search.html)
- **CSS Classes**: `.sidebar-search`
- **Digunakan di**: `templates/cotton/layout/app.html`, halaman dengan sidebar kustom.
- **Parameter**:
  | Nama | Tipe | Default | Keterangan |
  |---|---|---|---|
  | `placeholder` | string | `"Search…"` | Teks placeholder input |

- **Contoh**:
  ```html
  <c-sidebar.search placeholder="Search components…" />
  ```
- **Kelebihan**: Ringkas; konsisten dengan desain sidebar.
- **Kekurangan**: Belum terintegrasi dengan HTMX secara bawaan. Untuk fungsionalitas pencarian real-time, tambahkan `hx-get` secara manual pada elemen `<input>` di dalam template atau buat komponen baru.

---

### `<c-sidebar.nav>`
Wrapper navigasi sidebar (tag `<nav>`). Digunakan sebagai container untuk `<c-sidebar.section>` dan `<c-sidebar.link>`.

- **File**: [`templates/cotton/sidebar/nav.html`](../templates/cotton/sidebar/nav.html)
- **CSS Classes**: `.rdp-sidebar__nav`
- **Digunakan di**: Semua halaman dengan sidebar kustom.
- **Parameter**: *(tidak ada — gunakan `slot` untuk konten)*
- **Contoh**:
  ```html
  <c-sidebar.nav>
      <c-sidebar.section title="Menu Utama" />
      <c-sidebar.link href="/dashboard/" icon="🏠">Dashboard</c-sidebar.link>
      <c-sidebar.link href="/laporan/" icon="📊">Laporan</c-sidebar.link>
  </c-sidebar.nav>
  ```
- **Kelebihan**: Satu baris pengganti `<nav style="...">` yang panjang.
- **Kekurangan**: Tidak mendukung `aria-label` kustom (bawaan: `"Navigasi sidebar"`).

---

### `<c-sidebar.section>`
Judul pemisah kelompok menu (section heading) di dalam `<c-sidebar.nav>`.

- **File**: [`templates/cotton/sidebar/section.html`](../templates/cotton/sidebar/section.html)
- **CSS Classes**: `.rdp-sidebar__section-title`
- **Digunakan di**: Di dalam `<c-sidebar.nav>`.
- **Parameter**:
  | Nama | Tipe | Default | Keterangan |
  |---|---|---|---|
  | `title` | string | *(kosong)* | Judul grup menu |

- **Contoh**:
  ```html
  <c-sidebar.section title="Pengaturan" />
  ```
- **Kelebihan**: Menghilangkan inline style dari `<div class="rdp-sidebar__section-title" style="...">` yang berulang.
- **Kekurangan**: Tidak mendukung ikon atau elemen tambahan di sebelah judul.

---

### `<c-sidebar.link>`
Item tautan navigasi individual di dalam sidebar.

- **File**: [`templates/cotton/sidebar/link.html`](../templates/cotton/sidebar/link.html)
- **CSS Classes**: `.sidebar-link`
- **Digunakan di**: Di dalam `<c-sidebar.nav>`.
- **Parameter**:
  | Nama | Tipe | Default | Keterangan |
  |---|---|---|---|
  | `href` | string | `"#"` | URL tujuan tautan |
  | `icon` | string | *(kosong)* | Emoji atau karakter ikon yang ditampilkan |
  | `active` | bool | `False` | Jika `True`, menambahkan kelas `active` |
  | `id` | string | *(kosong)* | Atribut `id` HTML |
  | `onclick` | string | *(kosong)* | Atribut `onclick` HTML |
  | *(slot)* | HTML | — | Teks label menu |

- **Contoh**:
  ```html
  {# Link biasa #}
  <c-sidebar.link href="/settings/" icon="⚙️">Pengaturan</c-sidebar.link>

  {# Link aktif #}
  <c-sidebar.link href="/dashboard/" icon="🏠" active>Dashboard</c-sidebar.link>

  {# Link dinamis dengan active dari Django #}
  <c-sidebar.link href="{% url 'dashboard:index' %}" icon="🏠"
      active="{{ request.resolver_match.url_name == 'index' }}">
      Dashboard
  </c-sidebar.link>
  ```
- **Kelebihan**: Menstandarkan semua item menu; mendukung `active` state, ikon, dan `id`.
- **Kekurangan**: Untuk menu dengan *onclick* JavaScript yang kompleks (seperti theme switcher dinamis), lebih baik tetap menggunakan `<button class="sidebar-link">` secara manual.

---

## Pola Penggunaan Lengkap (Sidebar Kustom)

Berikut contoh lengkap mendefinisikan ulang sidebar di halaman tertentu:

```html
<c-layout.app title="Judul Halaman" navbar_brand="Nama App">
    <c-slot name="sidebar">
        {# 1. Brand/Logo #}
        <c-sidebar.brand title="Nama App" initial="N" href="/" />

        {# 2. Search (opsional, tampil di mobile) #}
        <c-sidebar.search placeholder="Cari menu…" />

        {# 3. Navigasi #}
        <c-sidebar.nav>
            <c-sidebar.section title="Menu Utama" />
            <c-sidebar.link href="{% url 'dashboard:index' %}" icon="🏠">Dashboard</c-sidebar.link>
            <c-sidebar.link href="{% url 'laporan:index' %}" icon="📊">Laporan</c-sidebar.link>

            <c-sidebar.section title="Pengaturan" />
            <c-sidebar.link href="{% url 'settings:index' %}" icon="⚙️">Pengaturan</c-sidebar.link>

            {# Menu dinamis dari database/context #}
            {% for item in menu_items %}
            <c-sidebar.link href="{{ item.url }}" icon="{{ item.icon }}">{{ item.label }}</c-sidebar.link>
            {% endfor %}
        </c-sidebar.nav>
    </c-slot>

    {# Konten halaman ... #}
</c-layout.app>
```
