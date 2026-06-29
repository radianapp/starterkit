# UI Components — RDP Starter Kit

**US-010 & US-011 — Layout dasar & Komponen UI**  
**Status**: Complete (v0.2.0-fase2)  
**Last Updated**: 2026-06-29

---

## Gambaran Umum

Modul ini mendokumentasikan semua komponen UI (Cotton components) yang tersedia di RDP Starter Kit. Semua komponen:
- ✅ Menggunakan RDP-UI Design System CDN untuk styling konsisten
- ✅ Support responsive design (mobile, tablet, desktop)
- ✅ Support dark mode otomatis via RDP-UI CSS variable
- ✅ Support HTMX attributes untuk interactivity
- ✅ Mengikuti naming convention: `<c-rdp.{module}.{name}>`

---

## Layout Components

### `<c-rdp.layout.navbar>`

Top navigation bar yang responsive dan sticky.

**Parameters:**
- `brand_text` (optional): Brand/logo text — default "RDP Starter Kit"
- `brand_url` (optional): Link untuk brand — default "/"
- `{{ attrs }}`: Pass-through untuk semua HTML attributes

**Slots:**
- `default`: Custom content di tengah navbar (setelah brand)
- `right`: Content di right side (user menu, notifications)

**Contoh:**
```django
<c-rdp.layout.navbar brand_text="My App" brand_url="/">
  <c-slot name="right">
    {% if user.is_authenticated %}
      <a href="/profile/">{{ user.username }}</a>
      <a href="/logout/">Logout</a>
    {% endif %}
  </c-slot>
</c-rdp.layout.navbar>
```

**Fitur:**
- Hamburger menu toggle untuk sidebar (di mobile)
- Navigation links responsif (hidden di mobile)
- Sticky top positioning
- Dark mode compatible

---

### `<c-rdp.layout.sidebar>`

Left navigation panel yang collapsible di mobile.

**Parameters:**
- `title` (optional): Judul section — default "Navigation"
- `collapsible` (optional): Enable collapse di mobile — default true
- `{{ attrs }}`: Pass-through attributes

**Slots:**
- `default`: Navigation items (gunakan `<a>` atau custom links)

**Contoh:**
```django
<c-rdp.layout.sidebar title="Menu">
  <a href="/dashboard/" class="rdp-sidebar__link">📊 Dashboard</a>
  <a href="/items/" class="rdp-sidebar__link">📋 Items</a>
  {% if user.is_staff %}
    <a href="/admin/" class="rdp-sidebar__link">⚙️ Admin</a>
  {% endif %}
</c-rdp.layout.sidebar>
```

**Fitur:**
- State dikelola via Alpine.js di parent (base.html)
- Auto-collapse di mobile (<768px)
- Close otomatis saat user klik link (UX improvement)
- Overlay backdrop di mobile
- State persist di localStorage

---

## UI Components

### `<c-rdp.button>`

Button dengan berbagai variant dan size.

**Parameters:**
- `variant` (optional): "primary" | "secondary" | "danger" | "ghost" — default "primary"
- `size` (optional): "xs" | "sm" | "md" | "lg" — default "md"
- `disabled` (optional): true | false — disable button
- `{{ attrs }}`: HTML attributes (bisa pakai hx-post, onclick, dll)

**Slots:**
- `default`: Button text/content

**Contoh:**
```django
<c-rdp.button variant="primary" hx-post="/save/">Save</c-rdp.button>
<c-rdp.button variant="danger" disabled>Delete</c-rdp.button>
<c-rdp.button variant="secondary" size="sm">Cancel</c-rdp.button>
```

**Fitur:**
- Support HTMX attributes
- Responsive sizing
- Accessible (proper button semantics)

---

### `<c-rdp.card>`

Container untuk grouped content dengan header, body, footer.

**Parameters:**
- `variant` (optional): "primary" | "secondary" — untuk accent border
- `clickable` (optional): true | false — add hover effect
- `{{ attrs }}`: Pass-through attributes

**Slots:**
- `default` | `body`: Main content
- `header`: Card header (optional)
- `footer`: Card footer (optional)

**Contoh:**
```django
<c-rdp.card variant="primary">
  <c-slot name="header">
    <h3>User Profile</h3>
  </c-slot>
  <p>Name: {{ user.name }}</p>
  <p>Email: {{ user.email }}</p>
  <c-slot name="footer">
    <c-rdp.button variant="primary">Edit</c-rdp.button>
  </c-slot>
</c-rdp.card>
```

**Fitur:**
- Semantic sections (header, body, footer)
- Shadow & border styling via RDP-UI
- Responsive width

---

### `<c-rdp.alert>`

Inline message dengan tipe (success, error, warning, info).

**Parameters:**
- `type` (required): "success" | "error" | "warning" | "info"
- `dismissible` (optional): true | false — show close button
- `title` (optional): Alert title
- `{{ attrs }}`: Pass-through attributes

**Slots:**
- `default`: Alert message content

**Contoh:**
```django
<c-rdp.alert type="success" title="Saved!">
  Your changes have been saved successfully.
</c-rdp.alert>

<c-rdp.alert type="error" dismissible>
  Something went wrong. Please try again.
</c-rdp.alert>
```

**Fitur:**
- Color-coded per type (success=green, error=red, dll)
- Dismissible via Alpine.js
- Auto-close functionality (optional)
- Accessible color + icon

---

### `<c-rdp.modal>`

Popup dialog dengan overlay dan trigger button.

**Parameters:**
- `trigger_text` (optional): Button text — default "Open Modal"
- `title` (optional): Modal title
- `size` (optional): "sm" | "md" | "lg" — default "md"
- `{{ attrs }}`: Pass-through attributes

**Slots:**
- `default`: Modal body content
- `trigger`: Custom trigger button (override trigger_text)
- `header`: Custom header (override title)
- `footer`: Modal footer (buttons, actions)

**Contoh:**
```django
<c-rdp.modal title="Delete Item?" trigger_text="Delete" size="sm">
  <p>Are you sure? This cannot be undone.</p>
  <c-slot name="footer">
    <c-rdp.button variant="secondary" @click="modalOpen = false">Cancel</c-rdp.button>
    <c-rdp.button variant="danger" hx-delete="/items/{{ id }}/">Delete</c-rdp.button>
  </c-slot>
</c-rdp.modal>
```

**Fitur:**
- Alpine.js state management
- Close on escape key
- Close on outside click (overlay)
- Responsive sizing
- Accessible focus management

---

### `<c-rdp.table>`

Responsive data table dengan striped rows, hover effect.

**Parameters:**
- `striped` (optional): true | false — alternate row colors
- `hover` (optional): true | false — highlight row on hover
- `bordered` (optional): true | false — show borders
- `{{ attrs }}`: Pass-through attributes

**Slots:**
- `default`: Table content (`<thead>`, `<tbody>`, `<tfoot>`)

**Contoh:**
```django
<c-rdp.table striped hover>
  <thead>
    <tr>
      <th>Name</th>
      <th>Email</th>
      <th>Status</th>
    </tr>
  </thead>
  <tbody>
    {% for user in users %}
      <tr>
        <td>{{ user.name }}</td>
        <td>{{ user.email }}</td>
        <td>{{ user.status }}</td>
      </tr>
    {% endfor %}
  </tbody>
</c-rdp.table>
```

**Fitur:**
- Horizontal scroll di mobile
- Striped rows untuk readability
- Hover highlight untuk better UX
- Responsive column layout

---

### `<c-rdp.form.input>`

Text input dengan label, help text, error display.

**Parameters:**
- `name` (required): Input name attribute
- `label` (optional): Label text
- `type` (optional): Input type (text, email, password, number, etc) — default "text"
- `placeholder` (optional): Input placeholder
- `value` (optional): Input value
- `error` (optional): Error message untuk validation error
- `help_text` (optional): Helper text di bawah input
- `required` (optional): true | false
- `disabled` (optional): true | false
- `{{ attrs }}`: HTML attributes (bisa pakai hx-*, oninput, dll)

**Slots:**
- `label`: Custom label content
- `help`: Custom help text

**Contoh:**
```django
<c-rdp.form.input
  name="email"
  type="email"
  label="Email Address"
  placeholder="you@example.com"
  help_text="We'll never share your email"
  required />

<c-rdp.form.input
  name="password"
  type="password"
  label="Password"
  error="Password must be at least 8 characters" />
```

**Fitur:**
- Error styling (red border + error message)
- Required asterisk automatic
- Help text styling
- Accessible label + aria attributes
- Focus styling

---

### `<c-rdp.form.select>`

Dropdown select dengan label, help text, error display.

**Parameters:**
- `name` (required): Select name attribute
- `label` (optional): Label text
- `placeholder` (optional): First placeholder option
- `options` (optional): Dict of {value: label} untuk auto-generate options
- `value` (optional): Selected value
- `error` (optional): Error message
- `help_text` (optional): Helper text
- `required` (optional): true | false
- `disabled` (optional): true | false
- `{{ attrs }}`: Pass-through attributes

**Slots:**
- `default`: Custom option elements (override options parameter)
- `label`: Custom label
- `help`: Custom help text

**Contoh:**
```django
<c-rdp.form.select
  name="status"
  label="Status"
  placeholder="Choose status..."
  options="{{ status_choices }}"
  required />

<c-rdp.form.select name="category" label="Category">
  <option value="">-- Select --</option>
  <option value="1">Option 1</option>
  <option value="2">Option 2</option>
</c-rdp.form.select>
```

**Fitur:**
- Custom arrow styling
- Placeholder option
- Error styling
- Accessible focus/label
- Supports grouped options

---

### `<c-rdp.pagination>`

Page navigation untuk list views dengan HTMX support.

**Parameters:**
- `page_obj` (required): Django paginator page object
- `url_pattern` (optional): URL pattern untuk pagination — default "#"
- `query_params` (optional): Additional query parameters

**Slots:**
- `default`: Custom pagination content

**Contoh:**
```django
<c-rdp.pagination page_obj="{{ page_obj }}" url_pattern="/items/?page=" />

{# Di view: #}
paginator = Paginator(items, 10)
page = paginator.get_page(request.GET.get('page', 1))
```

**Fitur:**
- Previous/Next buttons
- Page number links
- Current page highlight
- HTMX integration (hx-get untuk partial refresh)
- Responsive link hiding di mobile

---

### `<c-rdp.breadcrumb>`

Navigation trail menunjukkan page location.

**Parameters:**
- `items` (optional): List of dicts `[{url, label}, ...]` untuk breadcrumb items
- `{{ attrs }}`: Pass-through attributes

**Slots:**
- `default`: Custom breadcrumb items

**Contoh:**
```django
<c-rdp.breadcrumb items="[
  {'url': '/', 'label': 'Home'},
  {'url': '/items/', 'label': 'Items'},
  {'url': '', 'label': 'Detail'}
]" />

{# atau #}
<c-rdp.breadcrumb>
  <li><a href="/">Home</a></li>
  <li><a href="/items/">Items</a></li>
  <li>Detail</li>
</c-rdp.breadcrumb>
```

**Fitur:**
- Last item tidak link (current page)
- Hide intermediate items di mobile
- Slash separator styling
- Accessible nav semantics

---

### `<c-rdp.dropdown>`

Toggle dropdown menu dengan click-outside close.

**Parameters:**
- `trigger_text` (optional): Dropdown button text — default "Menu"
- `align` (optional): "left" | "center" | "right" — alignment — default "left"
- `{{ attrs }}`: Pass-through attributes

**Slots:**
- `trigger`: Custom trigger button
- `default`: Dropdown items (`<a>` atau `<button>` elements)

**Contoh:**
```django
<c-rdp.dropdown trigger_text="Actions">
  <a href="/edit/">Edit</a>
  <a href="/delete/">Delete</a>
  <button @click="share()">Share</button>
</c-rdp.dropdown>
```

**Fitur:**
- Alpine.js state management
- Click-outside close
- Escape key close
- Positioned arrow down icon
- Accessible focus management

---

## Base Template

### `templates/base.html`

Base template yang di-extend oleh semua halaman.

**Features:**
- Proper doctype, meta tags, charset
- RDP-UI CSS + HTMX + Alpine.js loading
- Layout wrapper dengan navbar + sidebar + content (3-column flexible)
- Sidebar state management via Alpine.js
- Block structure untuk customization:
  - `navbar_block`: Navbar (can override)
  - `sidebar_block`: Sidebar (can override)
  - `content_wrapper_block`: Content wrapper
  - `content`: Main content area
  - `footer_block`: Footer
  - `extra_css`, `extra_js`: Hook untuk child templates

**Contoh penggunaan:**
```django
{% extends "base.html" %}

{% block title %}My Page{% endblock %}

{% block content %}
  <h1>Page content here</h1>
  <p>...</p>
{% endblock %}
```

**Fitur:**
- Sidebar collapsible di mobile
- Alpine.js state persist ke localStorage
- Dark mode otomatis (RDP-UI handles it)
- Responsive 3-column layout
- HTMX ready

---

## Error Pages

### `templates/errors/{403,404,500}.html`

Error pages yang extend base.html dan menggunakan Cotton components.

**Fitur:**
- Navbar + footer konsisten dengan main layout
- Friendly error messages
- Call-to-action buttons
- Emoji icons untuk visual distinction
- Responsive centered card design
- Dark mode compatible

**Testing error pages:**
```bash
# Development (set DEBUG=False di .env)
uv run python manage.py runserver

# Test 404
curl http://localhost:8000/nonexistent/

# Test 403
# Create view dengan @login_required, akses tanpa login

# Test 500
# Temporarily raise Exception di view, trigger
```

---

## CSS Classes

Semua komponen menggunakan RDP-UI CSS classes yang tersedia di CDN:

| Element | RDP-UI Class | Deskripsi |
|---|---|---|
| Navbar | `.rdp-topnav`, `.rdp-topnav__brand`, `.rdp-topnav__links` | Top navigation |
| Sidebar | `.rdp-sidebar`, `.rdp-sidebar__link`, `.rdp-sidebar__nav` | Left navigation |
| Button | `.rdp-btn`, `.rdp-btn--primary`, `.rdp-btn--danger`, `.rdp-btn--sm` | Call-to-action |
| Card | `.rdp-card`, `.rdp-card__header`, `.rdp-card__body`, `.rdp-card__footer` | Container |
| Alert | `.rdp-alert`, `.rdp-alert--success`, `.rdp-alert--error` | Messages |
| Modal | `.rdp-modal`, `.rdp-modal__header`, `.rdp-modal__body` | Dialog |
| Table | `.rdp-table`, `.rdp-table--striped`, `.rdp-table--hover` | Data display |
| Form | `.rdp-form-field`, `.rdp-form-field__input`, `.rdp-form-field__label` | Form elements |

---

## Best Practices

### 1. Always Extend Base

Semua page templates harus extend `base.html` untuk konsistensi navbar, sidebar, footer.

```django
{% extends "base.html" %}
{% block content %}...{% endblock %}
```

### 2. Use Components Instead of Custom HTML

Gunakan Cotton components daripada menulis custom HTML.

```django
{# ✅ BAIK #}
<c-rdp.button variant="primary">Save</c-rdp.button>

{# ❌ BURUK #}
<button class="btn btn-primary">Save</button>
```

### 3. Pass-Through Attributes

Support `{{ attrs }}` untuk fleksibilitas maksimal.

```django
{# ✅ BAIK — supports HTMX #}
<c-rdp.button hx-post="/action/">Action</c-rdp.button>

{# ❌ BURUK — tidak support custom attributes #}
<button>Action</button>
```

### 4. Dark Mode

Jangan pakai hardcoded colors. Rely RDP-UI CSS variable untuk dark mode otomatis.

```django
{# ✅ BAIK — RDP-UI handles dark mode #}
<c-rdp.card>Content</c-rdp.card>

{# ❌ BURUK — hardcoded color #}
<div style="background: white">Content</div>
```

### 5. Responsive Design

Test semua komponen di mobile breakpoint (<768px).

```django
{# Sidebar auto-collapsible di mobile via base.html Alpine.js #}
{# Table auto-scroll di mobile #}
{# Modal responsive sizing #}
```

---

## Integration dengan HTMX

Semua komponen support HTMX attributes untuk partial page updates tanpa full reload.

**Contoh:**
```django
{# Button dengan HTMX untuk POST request #}
<c-rdp.button variant="primary" hx-post="/items/" hx-target="#items-list">
  Add Item
</c-rdp.button>

{# Form dengan HTMX untuk form submission #}
<form hx-post="/items/" hx-target="#items-list">
  <c-rdp.form.input name="name" label="Item Name" required />
  <c-rdp.button type="submit">Add</c-rdp.button>
</form>
```

---

## Testing Components

Lihat `templates/test_components.html` untuk contoh rendering semua komponenzn.

**Jalankan test:**
```bash
uv run python manage.py runserver
# Buka http://localhost:8000/test-components/
```

---

## Troubleshooting

### Komponen tidak render
- Pastikan RDP-UI CDN accessible (check browser Network tab)
- Verify django-cotton installed di INSTALLED_APPS
- Check Django template error di console

### Dark mode tidak kerja
- Verify RDP-UI CSS loaded
- Set OS theme ke dark mode (Windows Settings / Preferences)
- Clear browser cache

### HTMX tidak trigger
- Verify HTMX script loaded (`unpkg.com/htmx.org`)
- Check browser console untuk errors
- Verify hx-* attributes syntax benar

### Sidebar tidak collapse
- Verify Alpine.js loaded dan layoutState() function defined
- Check localStorage tidak disabled
- Verify window width < 768px untuk mobile

---

## Next Steps

- Fase 3: Gunakan komponen form untuk authentication views
- Fase 4: Extend components dengan custom styling per project
- Add more components as needed (tabs, stepper, wizard, dll)

---

*Dokumentasi ini sesuai dengan Fase 2 — US-010 & US-011.*  
*Last sync: 2026-06-29 — versi 0.2.0*
