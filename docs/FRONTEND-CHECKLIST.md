# 🎯 Frontend Development Checklist

**Gunakan checklist ini sebelum submit setiap fitur frontend.**

Berlaku untuk: Template HTML, CSS, JavaScript, Komponen Cotton  
Versi: 1.0 (2026-07-01)

---

## ✅ Pre-Code Checklist

- [ ] Read `CLAUDE.md` rules untuk frontend (rule #9: inline CSS/JS)
- [ ] Read `docs/SOP-FRONTEND-STRUCTURE.md` untuk struktur file
- [ ] Identifikasi: halaman baru atau perubahan halaman existing?
- [ ] Identifikasi: komponen baru atau reuse existing components?

---

## ✅ During Development Checklist

### HTML/Template

- [ ] **Gunakan Cotton layout:** Template extend `<c-layouts.base>` atau `{% extends "base.html" %}`
- [ ] **Tidak ada inline CSS:** Semua `style=` attributes sudah di-extract
- [ ] **Tidak ada inline JS:** Semua `<script>` blocks sudah di-extract
- [ ] **Gunakan Cotton components:** Semua UI elements pakai `<c-rdp.{nama}>` bukan `{% include %}`
- [ ] **Gunakan class names:** Styling lewat CSS classes, bukan inline styles
- [ ] **Responsive:** Template tested di mobile (480px), tablet (768px), desktop (1200px)
- [ ] **Referensi US:** Komentar `{# US-xxx #}` di top of file
- [ ] **Load static files correctly:** Gunakan `{% load static %}` dan `{% static 'path' %}`

### CSS

- [ ] **Extracted to file:** Semua CSS di `static/css/{page-name}.css`, bukan di template
- [ ] **Naming convention:** Classes follow BEM pattern (`.page-name-component`)
- [ ] **Mobile-first:** CSS dimulai dari mobile, media queries untuk desktop
- [ ] **Responsive breakpoints:** Tested di 480px, 768px, 1200px
- [ ] **No hardcoded colors:** Gunakan CSS variables dari RDP-UI atau define di `:root`
- [ ] **Linked correctly:** CSS di-link via `<link rel="stylesheet" href="{% static 'css/...' %}">`
- [ ] **Commented:** Section headers `/* ============================================================ */`
- [ ] **Referensi US:** Comment di top `/* US-xxx: ... */`

### JavaScript

- [ ] **Extracted to file:** Semua JS di `static/js/{component}.js`, bukan di template
- [ ] **Modular:** Satu file = satu concern (sidebar state, form validation, dll)
- [ ] **Documented:** Function punya JSDoc atau comment menjelaskan purpose
- [ ] **Error handling:** Try-catch untuk potential errors, console logging untuk debug
- [ ] **Linked correctly:** Script di-load via `<script src="{% static 'js/...' %}"></script>`
- [ ] **Load order:** Base utilities (`base.js`) sebelum feature-specific JS
- [ ] **No globals:** Gunakan IIFE atau modules untuk avoid global namespace pollution
- [ ] **Referensi US:** Comment di top `/* US-xxx: ... */`

### Components (Cotton)

- [ ] **DRY principle:** Template tidak repeat sama code 2x atau lebih
- [ ] **Cotton format:** Gunakan `<c-rdp.nama>` bukan `{% include %}`
- [ ] **Named slots:** Support untuk fleksibilitas (header, footer, default, dll)
- [ ] **Documented:** Parameter/slot dijelaskan di comment top of component file
- [ ] **Responsive:** Component responsif di semua breakpoints
- [ ] **Reusable:** Component bisa di-pakai di multiple pages

---

## ✅ Before Commit Checklist

### Code Quality

- [ ] **No console errors:** Buka DevTools, tidak ada JS errors
- [ ] **No console warnings:** Tidak ada warnings (terutama CSRF, resource loading)
- [ ] **Responsive on mobile:** Test di mobile browser atau `max-width: 480px`
- [ ] **Responsive on tablet:** Test di tablet or `max-width: 768px`
- [ ] **Responsive on desktop:** Test di laptop/desktop (1200px+)
- [ ] **CSS minified ready:** No unnecessary spaces/lines (formatting optional, minify on deploy)
- [ ] **JS tested:** Try feature manually, no errors

### Documentation

- [ ] **CHANGELOG.md updated:** Entry format `US-{nomor}: {judul} — {deskripsi}`
- [ ] **database.md updated:** Jika ada model changes
- [ ] **Module doc created:** `docs/modules/{feature-name}.md` jika fitur kompleks
- [ ] **Inline comments:** Logika kompleks punya comment Bahasa Indonesia
- [ ] **Docstring for JS:** Function/component punya dokumentasi

### Naming & Structure

- [ ] **Files in correct location:** CSS di `static/css/`, JS di `static/js/`
- [ ] **Filenames consistent:** `{feature-name}.css`, `{feature-name}.js`
- [ ] **Class names consistent:** `.{feature}-{component}` pattern
- [ ] **No typos:** Cek file names, variable names, class names

### Accessibility & Performance

- [ ] **Semantic HTML:** Use `<button>` not `<div>`, `<nav>` for navigation, etc.
- [ ] **ARIA labels:** Form inputs have `<label>`, images have `alt` text
- [ ] **Keyboard navigation:** Tab through page, enter untuk submit
- [ ] **Color contrast:** Text readable on background (use DevTools accessibility)
- [ ] **Image optimization:** Images compressed (JPEG/WebP, <100KB ideally)
- [ ] **No unused CSS:** Remove unused classes before commit

---

## ✅ Post-Commit Checklist

- [ ] **PR/Branch:** Code di-push ke feature branch, not directly to main
- [ ] **Tests:** `uv run pytest` passing (jika ada)
- [ ] **Lint:** `uv run ruff check .` passing
- [ ] **Format:** `uv run ruff format .` applied
- [ ] **Review:** Minimal satu orang review sebelum merge
- [ ] **Staging:** Deploy ke staging, test end-to-end

---

## 🚨 Common Mistakes (Don't!)

❌ **Inline style attributes**
```html
<div style="display: grid; gap: 20px;">
```

❌ **Inline script blocks**
```html
<script>
  document.addEventListener(...);
</script>
```

❌ **Using {% include %} for components**
```html
{% include "partials/card.html" %}
```

❌ **Hardcoded values in CSS**
```css
.card { border: 1px solid #0066cc; } /* Instead of CSS var */
```

❌ **Generic class names**
```html
<div class="container"> <!-- Too generic -->
```

❌ **No mobile-first**
```css
@media (min-width: 1200px) { ... }
@media (max-width: 767px) { ... } /* Desktop rules first */
```

---

## 📝 Template: Pre-Commit Checklist Comment

Paste this di PR description:

```markdown
## Frontend Checklist

- [ ] No inline CSS in templates
- [ ] No inline JS in templates  
- [ ] All CSS extracted to static/css/
- [ ] All JS extracted to static/js/
- [ ] Cotton components used for UI elements
- [ ] Mobile responsive (tested at 480px, 768px, 1200px)
- [ ] CHANGELOG.md updated
- [ ] No console errors/warnings
- [ ] Naming conventions followed
```

---

## 🔗 Related Documents

- [`CLAUDE.md`](../CLAUDE.md) — Aturan utama project
- [`SOP-FRONTEND-STRUCTURE.md`](SOP-FRONTEND-STRUCTURE.md) — Struktur file & workflow
- [`docs/modules/ui-components.md`](modules/ui-components.md) — Cotton component reference

---

**Questions?** Refer to the related documents atau ask in team.

*Last updated: 2026-07-01*
