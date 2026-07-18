# Panduan RDP-UI

Design System dan CSS Framework untuk semua produk Radian Data Platform (RDP).

---

## Struktur Repo

```text
ui.radian.web.id/
├── index.html                  ← Landing page + theme preview
├── assets/                     ← "Latest" alias — selalu isi versi terbaru
│   ├── rdp.css
│   ├── rdp.js
│   ├── themes/*.css
│   └── components/*.css
├── v1.0/assets/                ← Snapshot versi 1.0 (immutable setelah rilis)
├── v2.0/assets/                ← Snapshot versi 2.0 (dibuat saat breaking change)
├── docs/
│   ├── panduan-rdp-ui.md       ← file ini
│   └── design/handover/        ← design handoff docs (*.dc.html)
└── CLAUDE.md                   ← context untuk AI assistant
```

---

## Source of Truth

**Source asli ada di starterkit**, bukan di repo ini.

```
Starterkit (develop di sini)         →   UI Repo (publish ke sini)
────────────────────────────────────────────────────────────────────
static/vendor/rdp-ui/rdp.css        →   assets/rdp.css + v{X}/assets/rdp.css
static/vendor/rdp-ui/rdp.js         →   assets/rdp.js  + v{X}/assets/rdp.js
static/vendor/rdp-ui/themes/*.css   →   assets/themes/ + v{X}/assets/themes/
static/css/components/*.css         →   assets/components/ + v{X}/assets/components/
templates/cotton/rdp/{nama}.html    →   docs/components/{nama}.html (contoh)
```

Jangan edit file di `assets/` atau `v{X}/` langsung — perubahan akan tertimpa saat sync berikutnya.

---

## Cara Pakai

### 1. Via CDN (production)

```html
<!-- Core CSS -->
<link rel="stylesheet" href="https://ui.radian.web.id/v1.0/assets/rdp.css">

<!-- Tema (pilih salah satu) -->
<link rel="stylesheet" href="https://ui.radian.web.id/v1.0/assets/themes/default.css">

<!-- Core JS -->
<script type="module" src="https://ui.radian.web.id/v1.0/assets/rdp.js" defer></script>
```

Tema tersedia: `default`, `light`, `dark`, `midnight`, `nord`, `dracula`, `forest`, `ocean`, `corporate`, `github`, `terminal`

### 2. Load komponen tertentu saja

```html
<link rel="stylesheet" href="https://ui.radian.web.id/v1.0/assets/components/toast.css">
<link rel="stylesheet" href="https://ui.radian.web.id/v1.0/assets/components/drawer.css">
```

### 3. Self-hosted / offline (lokal di starterkit)

Set env var di `.env` starterkit:

```bash
RDP_UI_SELF_HOST=True
```

`base.html` otomatis load dari `static/vendor/rdp-ui/` — tidak butuh koneksi internet.

### 4. Django + Cotton (RDP Starter Kit)

```django
{# Set versi di .env: RDP_UI_VERSION=v1.0 #}
{# base.html otomatis load CDN atau self-host tergantung RDP_UI_SELF_HOST #}

<c-rdp.button variant="primary">Simpan</c-rdp.button>
<c-rdp.card>Konten</c-rdp.card>
```

---

## Env Var Starterkit

| Var | Default | Keterangan |
|---|---|---|
| `RDP_UI_VERSION` | `v1.0` | Versi CDN yang dimuat |
| `RDP_UI_SELF_HOST` | `False` | `True` = pakai `static/vendor/rdp-ui/` (offline) |

---

## Membuat Komponen Baru

1. **Buat CSS** di starterkit:
   ```
   static/css/components/{nama}.css
   ```

2. **Buat template Cotton** di starterkit:
   ```
   templates/cotton/rdp/{nama}.html
   ```

3. **Daftarkan di `components.css`** starterkit:
   ```css
   @import 'components/{nama}.css';
   ```

4. **Sync ke UI repo** (lihat bagian Sync di bawah).

5. **Buat halaman contoh** di UI repo:
   ```
   docs/components/{nama}.html
   ```

6. **Dokumentasikan** di `docs/modules/ui-components.md` starterkit.

---

## Sync Starterkit → UI Repo

Jalankan dari folder starterkit:

```powershell
$SRC = "C:\Users\rahad\Work\org\rdp\beta\starterkit"
$UI  = "C:\Users\rahad\Work\org\rdp\publish\ui.radian.web.id"
$VER = "v1.0"   # ganti sesuai versi aktif

# Core
Copy-Item "$SRC\static\vendor\rdp-ui\rdp.css" "$UI\assets\rdp.css" -Force
Copy-Item "$SRC\static\vendor\rdp-ui\rdp.js"  "$UI\assets\rdp.js"  -Force

# Themes
Copy-Item "$SRC\static\vendor\rdp-ui\themes\*.css" "$UI\assets\themes\" -Force

# Components
Copy-Item "$SRC\static\css\components\*.css" "$UI\assets\components\" -Force

# Mirror ke folder versi
Copy-Item "$UI\assets\rdp.css"         "$UI\$VER\assets\rdp.css" -Force
Copy-Item "$UI\assets\rdp.js"          "$UI\$VER\assets\rdp.js"  -Force
Copy-Item "$UI\assets\themes\*.css"    "$UI\$VER\assets\themes\"  -Force
Copy-Item "$UI\assets\components\*.css" "$UI\$VER\assets\components\" -Force
```

Lalu commit di UI repo:

```powershell
cd $UI
git add .
git commit -m "chore: sync assets from starterkit"
git push
```

---

## Update Versi

### Patch / minor fix — tetap versi sama (misal `v1.0`)

Jalankan sync di atas. Tidak perlu ubah `RDP_UI_VERSION` di starterkit.

Consumer tidak terdampak — URL tidak berubah.

---

### Breaking change — naik versi (misal `v1.0` → `v2.0`)

Breaking change = rename/hapus class CSS, ubah struktur HTML komponen, hapus JS API.

**Langkah:**

1. Sync assets ke `assets/` (latest alias):
   ```powershell
   # ... jalankan sync seperti biasa ke assets/
   ```

2. Buat folder versi baru:
   ```powershell
   $UI = "C:\Users\rahad\Work\org\rdp\publish\ui.radian.web.id"
   Copy-Item -Recurse "$UI\assets" "$UI\v2.0\assets"
   ```

3. Commit + push:
   ```powershell
   cd $UI
   git add v2.0/ assets/
   git commit -m "feat: release v2.0 — breaking changes (rename/remove ...)"
   git push
   ```

4. Update starterkit `.env`:
   ```bash
   RDP_UI_VERSION=v2.0
   ```

5. `v1.0/` tetap di repo — consumer lama yang masih pakai `v1.0` tidak rusak.

---

## Aturan Versi

| Perubahan | Tindakan versi |
|---|---|
| Fix typo CSS, tweak warna/spacing | Update `assets/` + `v{current}/assets/` |
| Tambah komponen baru | Update `assets/` + `v{current}/assets/` |
| Tambah tema baru | Update `assets/` + `v{current}/assets/` |
| Rename class CSS | Naik versi major → `v{next}/` |
| Hapus komponen/class | Naik versi major → `v{next}/` |
| Ubah struktur HTML komponen Cotton | Naik versi major → `v{next}/` |
| Hapus/rename JS API publik | Naik versi major → `v{next}/` |

---

## Deploy

- **Platform**: Cloudflare Pages
- **Repo**: [radianapp/ui](https://github.com/radianapp/ui)
- **Branch**: `main` → auto-deploy
- **Domain**: `ui.radian.web.id` (CNAME ke Cloudflare Pages)
- **Build command**: *(kosong — static files)*
- **Build output**: `/`

Setiap `git push` ke `main` → Cloudflare Pages auto-deploy dalam ~1 menit.

---

## Checklist Rilis Versi Baru

- [ ] Sync semua file dari starterkit ke `assets/`
- [ ] Mirror ke `v{X}/assets/`
- [ ] Update `index.html` jika ada perubahan cara pakai
- [ ] Buat/update `docs/components/{nama}.html` untuk komponen baru
- [ ] Commit + push → verifikasi deploy Cloudflare Pages berhasil
- [ ] Test URL: `https://ui.radian.web.id/v{X}/assets/rdp.css`
- [ ] Update `RDP_UI_VERSION` di starterkit `.env` (kalau naik versi)
- [ ] Update `RDP_UI_VERSION` di starterkit `.env.example`
