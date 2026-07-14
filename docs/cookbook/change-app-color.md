# Cookbook: Mengubah Warna Aplikasi & Kustomisasi Tema

Resep ini menjelaskan bagaimana cara memodifikasi sistem warna dan variabel CSS untuk menyesuaikan tema visual aplikasi RDP Starter Kit dengan brand produk Anda.

---

## 1. Memahami Variabel CSS PicoCSS
RDP Starter Kit menggunakan **PicoCSS** sebagai fondasi styling dasar. Tema warna diatur menggunakan variabel kustom CSS pada tag root (`:root` untuk mode terang dan `[data-theme="dark"]` untuk mode gelap).

---

## 2. Kustomisasi Melalui CSS File
Untuk mengganti warna primer atau skema warna umum, modifikasi atau override variabel CSS tersebut di file stylesheet global `static/css/layout.css` atau file CSS spesifik aplikasi Anda.

```css
/* Mengganti warna primer menjadi brand color baru (misal: Indigo) */
:root {
  --pico-primary: #4f46e5;
  --pico-primary-background: #4f46e5;
  --pico-primary-hover: #4338ca;
  --pico-primary-underline: rgba(79, 70, 229, 0.5);
  --pico-primary-focus: rgba(79, 70, 229, 0.25);
  --pico-primary-inverse: #ffffff;
}

/* Modifikasi untuk mode gelap */
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --pico-primary: #6366f1;
    --pico-primary-background: #6366f1;
    --pico-primary-hover: #4f46e5;
    --pico-primary-focus: rgba(99, 102, 241, 0.25);
  }
}
```

---

## 3. Menghindari Inline CSS
- **DILARANG** melakukan modifikasi warna elemen langsung menggunakan tag `<div style="color: red;">`.
- Gunakan class-class utilitas yang telah disediakan PicoCSS atau buat class CSS kustom baru di dalam folder `static/css/components/` Anda.
- Manfaatkan variabel-variabel warna global agar tetap konsisten ketika user beralih dari Light Mode ke Dark Mode.
