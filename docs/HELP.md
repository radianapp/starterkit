# Help & Troubleshooting

## UI Tidak Ter-render dengan Benar
**Masalah**: Komponen form atau tombol tidak memiliki gaya CSS.
**Solusi**: Pastikan Anda sudah memuat file CSS utama RDP UI di template base Anda. Gunakan tag `{% static 'vendor/rdp-ui/rdp.css' %}` dan pastikan folder static disajikan dengan benar oleh server pengembangan.

## Komponen Cotton Tidak Dikenali
**Masalah**: Error template "Component 'c-rdp.button' does not exist".
**Solusi**: Pastikan `django-cotton` sudah ditambahkan di `INSTALLED_APPS` pada `settings/base.py`. Komponen RDP UI harus berada di direktori `templates/cotton/rdp/`.
