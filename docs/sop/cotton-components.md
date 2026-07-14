# SOP Komponen Django-Cotton

Dokumen ini mendefinisikan standar pembuatan dan penggunaan komponen **Django-Cotton** dalam proyek Radian Data Platform (RDP).

## 1. Naming & Struktur Folder
- Semua komponen global berada di folder `templates/cotton/`.
- Komponen spesifik framework RDP berada di bawah namespace `rdp/` (dapat dipanggil menggunakan `<c-rdp.nama_komponen>`).
- Gunakan format **kebab-case** untuk nama file komponen:
  - Contoh file: `templates/cotton/rdp/stat-card.html`
  - Contoh penggunaan: `<c-rdp.stat-card />`

---

## 2. Penggunaan Props & Slots
Setiap komponen harus dirancang agar fleksibel menggunakan atribut `props` untuk parameter variabel dan `{{ slot }}` untuk konten HTML yang dinamis.

### Contoh Definisi Komponen (`templates/cotton/rdp/card.html`):
```html
<div class="card {% if class %}{{ class }}{% endif %}">
    {% if title %}
        <header>
            <strong>{{ title }}</strong>
        </header>
    {% endif %}
    
    <div class="card-body">
        {{ slot }}
    </div>
</div>
```

### Contoh Pemanggilan Komponen:
```html
<c-rdp.card title="Statistik Bulanan" class="custom-card">
    <p>Ini adalah konten di dalam slot.</p>
</c-rdp.card>
```

---

## 3. Menghindari Inline CSS
- **DILARANG** menggunakan atribut `style="..."` inline di dalam komponen Cotton.
- Jika komponen membutuhkan styling kustom di luar PicoCSS, pisahkan style tersebut ke dalam file stylesheet terpisah pada `static/css/components/{nama-komponen}.css`.
- Muat file stylesheet tersebut secara modular pada halaman terkait atau melalui stylesheet bundle jika diperlukan.
