# SOP: Frontend Code Organization (CSS, JS, Templates)

**Berlaku untuk:** Semua fitur baru di RDP Starter Kit  
**Versi:** 1.0 (2026-07-01)  
**Author:** AI Assistant (based on CLAUDE.md rules)

---

## 📋 Ringkasan

Pedoman wajib untuk memastikan semua CSS, JavaScript, dan template terorganisir rapi, reusable, dan mudah dimaintain. Semua inline CSS dan inline JavaScript **HARUS diextract** ke file terpisah.

---

## 🗂️ Struktur Folder Static Files

```
static/
├── css/
│   ├── base.css                 ← Layout dasar (navbar, sidebar, footer, responsiveness)
│   ├── dashboard.css            ← Dashboard page specific styling
│   ├── errors.css               ← Error pages (403, 404, 500) styling
│   ├── components.css           ← Komponen-specific CSS overrides (opsional)
│   └── [feature-name].css       ← Per-feature: buat file terpisah jika kompleks
│
├── js/
│   ├── base.js                  ← Base utilities (CSRF token setup, dll)
│   ├── layout-state.js          ← Alpine.js layout component (sidebar toggle)
│   └── components/
│       ├── modal.js             ← Modal component behavior (opsional)
│       ├── dropdown.js          ← Dropdown component behavior (opsional)
│       └── [feature].js         ← Per-feature component JS
│
└── images/
    └── [logo, icons, dll]
```

---

## ✅ Aturan Wajib

### 1. **Inline CSS = Tidak Boleh ❌**

❌ **JANGAN:**
```html
<div style="display: grid; gap: 20px; margin: 30px 0;">
  Content here
</div>
```

✅ **HARUS:**
```html
{# templates/dashboard/index.html #}
<div class="dashboard-cards-grid">
  Content here
</div>
```

```css
/* static/css/dashboard.css */
.dashboard-cards-grid {
  display: grid;
  gap: 20px;
  margin: 30px 0;
}
```

**Alasan:**
- CSS tidak bisa diminim/optimize
- CSS tidak bisa di-reuse di halaman lain
- Sulit di-debug di DevTools
- Melanggar separation of concerns

---

### 2. **Inline JavaScript = Tidak Boleh ❌**

❌ **JANGAN:**
```html
<script>
  document.addEventListener("htmx:configRequest", (e) => {
    e.detail.headers["X-CSRFToken"] = 
      document.querySelector("meta[name=csrf-token]").content;
  });
</script>
```

✅ **HARUS:**
```html
{# templates/cotton/layouts/base.html #}
<script src="{% static 'js/base.js' %}"></script>
```

```javascript
/* static/js/base.js */
document.addEventListener('htmx:configRequest', function(event) {
  const csrfToken = document.querySelector('meta[name="csrf-token"]');
  if (csrfToken) {
    event.detail.headers['X-CSRFToken'] = csrfToken.content;
  }
});
```

**Alasan:**
- JS tidak bisa di-cache dengan baik
- JS inline tidak bisa di-minify
- Sulit untuk unit test
- Namespace collision risks

---

### 3. **Template = Gunakan Komponen Reusable ✅**

❌ **JANGAN:** Hardcode HTML di banyak tempat
```html
{# Berulang di multiple pages #}
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px;">
  <card>...</card>
</div>
```

✅ **HARUS:** Buat komponen Cotton atau partial reusable
```html
{# templates/cotton/rdp/card-grid.html #}
<template>
  <div class="card-grid">
    <c-slot name="default"></c-slot>
  </div>
</template>
```

```html
{# Usage di multiple pages #}
<c-rdp.card-grid>
  <c-rdp.card>...</c-rdp.card>
</c-rdp.card-grid>
```

**Alasan:**
- DRY principle: don't repeat yourself
- Single source of truth untuk styling
- Mudah maintenance & updates
- Consistent UX di semua halaman

---

### 4. **Naming Convention**

#### CSS Files
- **Global/base:** `base.css`, `layout.css`, `typography.css`
- **Per-page:** `{page-name}.css` → `dashboard.css`, `errors.css`
- **Per-feature:** `{feature}.css` → `user-profile.css`, `billing.css`
- **Components:** `components.css` untuk override RDP-UI components

#### CSS Classes
- **Prefix app:** `.rdp-*` untuk layout, `.dashboard-*` untuk dashboard-specific
- **BEM pattern:** `.dashboard-cards-grid`, `.dashboard-card-title`, `.dashboard-card-content`
- **Avoid:** Generic names seperti `.container`, `.box`, `.item` (gunakan RDP-UI classes)

#### JavaScript Files
- **Global/base:** `base.js`, `utils.js`, `constants.js`
- **Alpine components:** `{component-name}.js` → `layout-state.js`, `modal.js`
- **Per-feature:** `{feature}.js` → `user-profile.js`, `billing.js`

#### Template Files
- **Page templates:** `templates/{app}/{page-name}.html`
- **Components:** `templates/cotton/rdp/{component-name}.html`
- **Partials (shared):** `templates/partials/{partial-name}.html` (gunakan Cotton preferred)

---

### 5. **Hindari CSS Specificity Conflict pada Komponen**

**Masalah Umum:** Teks pada komponen (seperti Button) tidak terlihat karena warna teks sama dengan warna background. Hal ini sering terjadi ketika base styling untuk tag `<a>` menimpa styling khusus class button.

❌ **JANGAN:** Menggunakan tag selector telanjang yang menimpa komponen UI.
```css
/* Ini akan menang melawan class button biasa karena spesifisitas struktur DOM jika diletakkan di scope parent */
.landing-page a {
    color: var(--primary-color);
}
```

✅ **HARUS:** Gunakan `:not()` pseudo-class untuk mengecualikan komponen, atau gunakan *compound selector* untuk meningkatkan spesifisitas class komponen.

**Solusi 1: Pengecualian pada Base Selector (Direkomendasikan)**
```css
/* Hanya style plain links, kecualikan elemen yang berperilaku seperti button/card */
.landing-page a:not([class*="btn"]):not([class*="cta"]):not([class*="card"]) {
    color: var(--primary-color);
    text-decoration: none;
}
```

**Solusi 2: Compound Selector untuk Komponen**
```css
/* Tingkatkan spesifisitas button dari (0,1,0) menjadi (0,1,1) dengan tag selector + class selector */
a.btn-primary {
    color: #ffffff;
    background: var(--primary-color);
}
```

**Alasan:**
- Mencegah *regression bug* di mana perubahan style global merusak komponen UI di halaman tertentu.
- Memastikan teks komponen selalu kontras dan terbaca.

---

## 🔄 Workflow: Dari Aturan CLAUDE.md ke Kode

### Skenario: Buat Fitur Baru (Misal: User Profile Page)

#### **Step 1: Identifikasi Komponen & Styling**
```
Fitur: User Profile
- Layout: Form vertikal + sidebar dengan user info
- Components: Card, Button, Input, Avatar
- Behavior: Form submit, Avatar upload, Toggle edit mode
```

#### **Step 2: Buat CSS File**
```bash
# static/css/user-profile.css
```

```css
/* US-009: User profile page styling */

.profile-container {
  display: grid;
  grid-template-columns: 1fr 300px;
  gap: 30px;
  max-width: 1200px;
  margin: 0 auto;
}

.profile-form { ... }
.profile-sidebar { ... }
.profile-avatar { ... }

/* Responsive — mobile stacks vertically */
@media (max-width: 768px) {
  .profile-container {
    grid-template-columns: 1fr;
    gap: 20px;
  }
}
```

#### **Step 3: Buat Template**
```html
{# templates/accounts/profile.html #}
{% load static %}
<c-layouts.base with title="My Profile">
  <c-slot name="head">
    <link rel="stylesheet" href="{% static 'css/user-profile.css' %}">
  </c-slot>

  <div class="profile-container">
    {# Main form #}
    <div class="profile-form">
      <c-rdp.card>
        <c-slot name="header"><h2>Edit Profile</h2></c-slot>
        {% include "accounts/partials/profile-form.html" %}
      </c-rdp.card>
    </div>

    {# Sidebar #}
    <div class="profile-sidebar">
      <c-rdp.card>
        <div class="profile-avatar">
          <img src="{{ user.profile.avatar.url }}" alt="">
        </div>
        <p><strong>{{ user.get_full_name }}</strong></p>
      </c-rdp.card>
    </div>
  </div>
</c-layouts.base>
```

#### **Step 4: Jika Ada Behavior Kompleks, Buat JS File**
```javascript
/* static/js/user-profile.js */
/* US-009: User profile form behavior */

document.addEventListener('DOMContentLoaded', function() {
  const profileForm = document.querySelector('.profile-form form');
  const editBtn = document.querySelector('[data-profile-edit]');

  if (editBtn) {
    editBtn.addEventListener('click', function() {
      profileForm.classList.toggle('is-editing');
    });
  }

  if (profileForm) {
    profileForm.addEventListener('submit', function(e) {
      e.preventDefault();
      // HTMX will handle this automatically
    });
  }
});
```

```html
{# Link di template #}
<c-slot name="extra_js">
  <script src="{% static 'js/user-profile.js' %}"></script>
</c-slot>
```

#### **Step 5: Update CHANGELOG.md**
```markdown
## [Unreleased]

### Added
- US-009: User profile page — display user info, edit form, avatar upload
```

---

## 📱 Mobile-First Responsive Design

**Aturan:** Selalu tuliskan CSS untuk mobile terlebih dahulu, baru media queries untuk desktop.

✅ **BENAR:**
```css
/* Default: mobile (0px—767px) */
.profile-container {
  display: flex;
  flex-direction: column;
}

/* Tablet & desktop (768px—) */
@media (min-width: 768px) {
  .profile-container {
    display: grid;
    grid-template-columns: 1fr 300px;
  }
}
```

❌ **SALAH:** Mulai dari desktop, media query untuk mobile
```css
.profile-container {
  grid-template-columns: 1fr 300px;
}

@media (max-width: 767px) {
  .profile-container {
    flex-direction: column;
  }
}
```

---

## 🧪 Testing & QA Checklist

Sebelum commit fitur baru, pastikan:

- [ ] **CSS extractions:**
  - [ ] Tidak ada `style=` attributes di template
  - [ ] Tidak ada `<style>` tags di template
  - [ ] Semua CSS ada di `static/css/{page-name}.css`
  - [ ] CSS file di-link dengan `{% static %}` tag

- [ ] **JavaScript extractions:**
  - [ ] Tidak ada `<script>` tags dengan inline code di template
  - [ ] Semua JS ada di `static/js/{component}.js`
  - [ ] JS file di-load dengan `<script src="{%static%}">` tag
  - [ ] Script load order benar (base.js sebelum feature JS)

- [ ] **Component reusability:**
  - [ ] Grid layout di-extract ke class (`.dashboard-cards-grid`)
  - [ ] Form styling di-extract ke class (`.profile-form`)
  - [ ] Tidak ada hardcoded margin/padding di template (gunakan classes)

- [ ] **Mobile responsiveness:**
  - [ ] Tested di mobile (max-width: 480px)
  - [ ] Tested di tablet (max-width: 768px)
  - [ ] Tested di desktop (1200px+)
  - [ ] Sidebar collapse di mobile
  - [ ] Buttons stack di mobile

- [ ] **Naming & conventions:**
  - [ ] CSS classes follow BEM pattern
  - [ ] Files named sesuai feature/page
  - [ ] File paths follow `static/css/`, `static/js/` structure
  - [ ] Referensi US ada di komentar file

---

## 🔗 Link ke Template Files Wajib Update

Jika template/CSS/JS baru dibuat, **WAJIB update**:

1. **CHANGELOG.md** — tambahkan entry `US-{nomor}: {judul} — {deskripsi}`
2. **docs/architecture/database.md** — jika ada perubahan model
3. **docs/modules/{feature-name}.md** — dokumentasi modul baru (lihat skill 07)

---

## 💡 Contoh Real: Error Pages Refactoring

**Sebelum (inline CSS):**
```html
{% extends "base.html" %}
{% block content %}
<div class="error-page">
  ...content...
</div>
<style>
  .error-page { display: flex; ... }
  .error-icon { font-size: 4rem; ... }
  ...50 lines of CSS...
</style>
{% endblock %}
```

**Sesudah (extracted CSS):**
```html
{# templates/errors/404.html #}
{% extends "base.html" %}
{% load static %}
{% block title %}404 - Page Not Found{% endblock %}
{% block extra_css %}
<link rel="stylesheet" href="{% static 'css/errors.css' %}">
{% endblock %}
{% block content %}
<div class="error-page">
  ...content...
</div>
{% endblock %}
```

```css
/* static/css/errors.css */
.error-page { display: flex; ... }
.error-icon { font-size: 4rem; ... }
...50 lines of CSS...
```

**Benefit:**
- ✅ CSS bisa di-reuse di 403.html, 500.html
- ✅ CSS bisa di-minify & cache
- ✅ Template lebih readable
- ✅ Mudah di-maintain

---

## 🚀 Next Steps

1. **Untuk fitur baru:** Ikuti workflow di atas (Step 1—5)
2. **Untuk fitur lama yang masih inline:** Refactor gradually saat touch point
3. **Untuk team:** Gunakan SOP ini sebagai checklist pre-commit

---

**Questions?** Refer to `CLAUDE.md` aturan #9 (Hal yang Wajib — CSS/JS separation).

---

*Dokumen ini dikelola di: `docs/SOP-FRONTEND-STRUCTURE.md`  
Last updated: 2026-07-01  
Berlaku mulai: Fase 3 dan seterusnya*
