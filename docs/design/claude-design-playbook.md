# Playbook: Mendesain RDP UI dengan Claude Design

> Panduan langkah demi langkah + prompt siap copy-paste untuk membuat Product Design Specification RDP UI di Claude Design (claude.ai/design).

## Cara Kerja Claude Design (ringkas)

Claude Design punya dua area: chat (kiri) dan canvas (kanan). Anda mendeskripsikan yang diinginkan lewat chat, Claude menghasilkan desain di canvas, lalu Anda iterasi lewat chat (perubahan besar), inline comment (perubahan spesifik di satu elemen), atau edit langsung di canvas (geser/resize). Hasil bisa di-export ke standalone HTML, PDF, PPTX, atau di-handoff langsung ke Claude Code.

**Aturan utama**: jangan kirim brief besar sekaligus. Dokumentasi resmi Anthropic menyarankan *"start simple, then layer in complexity"*. Playbook ini memecah brief RDP UI menjadi 12 fase — satu project, banyak sesi.

**Kapan pakai apa saat iterasi:**

| Cara | Untuk |
|---|---|
| Chat | Perubahan struktural, section baru, minta alternatif ("show me 2–3 layouts") |
| Inline comment | Perubahan targeted per komponen ("make this padding larger") |
| Edit langsung di canvas | Geser, resize, align cepat |

---

## Fase 0 — Setup Project & Konteks

1. Buka **claude.ai/design** (atau dari sidebar Claude Desktop) → buat project baru: **RDP UI**.
2. Lampirkan konteks (semakin lengkap, semakin baik hasilnya):
   - File CSS RDP-UI yang sudah ada dari `cdn.radian.web.id` (unduh dulu).
   - Komponen cotton dari starterkit: `templates/cotton/rdp/`.
   - Screenshot inspirasi: shadcn/ui, Tailwind UI, GitHub Primer, PicoCSS, Linear, Vercel dashboard — sebagai referensi *mood*, bukan untuk dicontek.
3. **Alternatif dari terminal**: jalankan `/design-sync` dari Claude Code di repo starterkit untuk mengimpor design system yang sudah ada. Repo besar lebih baik di-link lewat Claude Code daripada di-upload di browser.
4. Paste **Prompt 0** di bawah sebagai pesan pertama. Ini menetapkan konteks project — belum minta output apa pun.

### Prompt 0 — Master Context

```text
You are helping me design "RDP UI" — a modern UI framework dedicated to Django.
Tagline: "Modern UI Framework for Django".

This is a complete ecosystem, not just CSS: Design System, CSS Framework,
Django Cotton components, HTMX integration patterns, Themes, Templates,
Documentation website, and Example Applications.

Target users: Django developers, backend engineers, startups, SaaS builders,
enterprise software teams.

Core philosophy (apply to everything you design in this project):
1. HTML First — semantic HTML, no utility-class soup.
2. Component First — everything reusable; every component has a Django Cotton
   version called as <c-rdp.{name}>.
3. Server First — HTMX is the interactive layer; no React; JS only when necessary.
4. Accessibility First — WCAG AA, keyboard navigation, focus states, ARIA.
5. Theme First — every color/size comes from CSS variables; never hardcoded.
6. Minimal API — easy to learn, small surface, small docs.
7. Enterprise Ready — dashboards, ERP, CRM, HRM, CMS, POS, admin panels, SaaS.

Design language: minimal, elegant, modern, soft, professional, premium.
Comfortable spacing, rounded corners, beautiful typography, excellent whitespace
and visual hierarchy — like a modern SaaS product.
AVOID: the Bootstrap look, Material Design clones, old admin-template styling.
Inspired by (philosophy, NOT visual style): PicoCSS, shadcn/ui, Tailwind UI,
Radix UI, GitHub Primer, DaisyUI. RDP UI must have its own identity.

Mobile-first responsive. Do not generate application source code — we are
producing a product design specification and visual artifacts only.

Acknowledge this context. I will then send design tasks one phase at a time.
```

---

## Fase 1 — Product Foundation (one-pager)

Deliverables: **1. Product Positioning, 2. User Personas, 3. Design Principles**.

```text
Create a product foundation one-pager for RDP UI with three sections:

1. Product positioning — positioning statement, competitive landscape vs
   Tailwind UI, shadcn/ui, PicoCSS, Bootstrap, Chakra UI, and DaisyUI, and the
   unique wedge: "the only complete UI ecosystem natively built for
   Django + Cotton + HTMX".
2. User personas — 4 personas: solo Django developer, backend engineer with no
   design skills, startup founder shipping a SaaS, enterprise team lead
   standardizing internal tools. Each: goals, pains, what RDP UI gives them.
3. Design principles — expand the 7 core philosophies into actionable
   principles with a one-line "this means / this never means" for each.

Layout: clean editorial one-pager, strong typographic hierarchy.
```

---

## Fase 2 — Visual Language & Foundations

Deliverables: **4. Visual Language, 5. Color, 6. Typography, 7. Spacing, 8. Radius, 9. Elevation, 10. Iconography**.

```text
Design the "RDP UI Foundations" specification as a series of styled sheets:

1. Color system — semantic tokens as CSS variables (--rdp-primary, --rdp-surface,
   --rdp-text, --rdp-border, --rdp-success/warning/danger/info, etc.) with a
   10-step neutral scale and accent scales. Show light and dark values side by
   side. All combinations must pass WCAG AA contrast.
2. Typography system — a modern, readable font stack (system-first with an
   optional premium webfont), type scale (display, h1–h6, body, small, caption,
   code), weights, line heights — all as CSS variables.
3. Spacing system — a 4px-based scale exposed as --rdp-space-* tokens, with
   usage rules (component padding, stack gaps, section rhythm).
4. Radius system — --rdp-radius-* scale from subtle to pill; show which
   components use which.
5. Elevation system — layered shadows (--rdp-shadow-*) that look soft and
   premium, not Material; include border-based elevation for flat contexts.
6. Iconography — SVG icon guidelines: grid size, stroke width, corner style,
   naming convention, and 20 sample icons in the RDP style.

Render each as a visual reference sheet a developer could pin on the wall.
```

Iterasi yang disarankan: minta 2–3 alternatif arah warna (`Show me 3 alternative primary color directions: one confident blue, one sophisticated neutral, one distinctive brand color`) sebelum mengunci.

---

## Fase 3 — Theme Architecture

Deliverable: **13. Theme Architecture**.

```text
Design the RDP UI theme architecture:

1. An architecture sheet showing how themes work: every theme is ONLY a set of
   CSS variable overrides on [data-rdp-theme="..."] — no extra CSS rules.
   Show the token inheritance model: primitive tokens → semantic tokens →
   component tokens.
2. A theme gallery page previewing the same card + form + button composition
   rendered in all 11 built-in themes: Default, Light, Dark, Corporate, Ocean,
   Forest, Midnight, Terminal, Nord, Dracula, GitHub.
3. An interactive theme switcher on that page so I can flip through themes live.

Nord, Dracula and GitHub should respect their well-known palettes; the others
are original RDP palettes consistent with our design language.
```

---

## Fase 4 — Layout System & Responsive Strategy

Deliverables: **11. Layout System, 12. Responsive Strategy**.

```text
Design the RDP UI layout system:

1. Container & grid — container widths, a 12-column grid, and common content
   layouts (single column, sidebar+content, holy grail, centered auth).
2. App shell — the canonical admin shell: collapsible sidebar, top navbar with
   search/notifications/user menu, content area, optional right panel.
3. Responsive strategy sheet — mobile-first breakpoints, how the app shell
   collapses (sidebar → drawer, navbar → hamburger), touch target rules, and a
   side-by-side preview of the shell at mobile / tablet / desktop / large.
```

---

## Fase 5 — Component Showcase (5 batch)

Deliverables: **14. Component Architecture, 21. Component Showcase**. Kirim satu batch per pesan; review dan iterasi sebelum lanjut batch berikutnya.

### Batch A — Actions & Feedback

```text
Design a component showcase page for RDP UI covering: Buttons (variants: primary,
secondary, outline, ghost, danger; sizes; icon buttons; loading state), Badges,
Alerts, Toast, Tooltip, Popover, Progress, Loading spinners, Skeleton.
For every component show: all variants, hover/focus/active/disabled states, and
the CSS variables it consumes. Use only our foundation tokens from Phase 2.
```

### Batch B — Forms

```text
Same format. Cover: Form layout, Input (with prefix/suffix, validation states),
Textarea, Checkbox, Radio, Switch, Select, File upload, field help text and
error messaging. Show a complete "Create account" form composed from these,
including an invalid-submission state (this is what an HTMX 422 partial
re-render will look like).
```

### Batch C — Overlay & Navigation

```text
Same format. Cover: Modal, Dialog (confirm), Drawer, Dropdown, Menu, Tabs,
Accordion, Navbar, Sidebar, Breadcrumb, Pagination. Show open/closed states
and keyboard/focus-trap behavior notes for each overlay.
```

### Batch D — Data Display

```text
Same format. Cover: Table (sortable headers, row selection, row actions, dense
and comfortable density), Cards, Stat cards, Metric cards, Avatar, Timeline,
Charts placeholder (styled container the developer drops any chart lib into),
Empty states, Error states, Loading states.
```

### Batch E — Component Architecture sheet

```text
Create the component architecture specification: anatomy of an RDP component
(wrapper, slots, states, tokens), the composition model, and the Django Cotton
mapping — how each component becomes <c-rdp.{name}> with attributes as props
and named slots for composition, e.g.:

<c-rdp.card>
  <c-slot name="header">…</c-slot>
  …body…
  <c-slot name="footer"><c-rdp.button variant="primary">Save</c-rdp.button></c-slot>
</c-rdp.card>

Show 5 worked examples of composition (card, modal, table row actions, form
field, sidebar item). No backend code — just the component contract.
```

---

## Fase 6 — HTMX Patterns + Interaction & Motion Guidelines

Deliverables: **15. Interaction Guidelines, 16. Motion Guidelines** + pola HTMX dari brief.

```text
Design the "RDP UI × HTMX Interaction Patterns" spec — one panel per pattern,
each showing the UI states (idle → loading → success/error) and which RDP
components are involved:

Modal via hx-get, Delete confirmation dialog, Inline edit, Active search,
Filtering, Pagination, Infinite scroll, Toast notifications after actions,
Loading indicators (hx-indicator), Form validation with HTTP 422 partial
re-render, File upload with progress, Server-pushed notifications.

Also include:
1. Interaction guidelines — feedback timing, optimistic vs server-confirmed UI,
   disabled-while-pending rules, error recovery.
2. Motion guidelines — duration/easing tokens (--rdp-duration-*, --rdp-ease-*),
   what animates (opacity, transform only), what never animates, and
   prefers-reduced-motion behavior.
```

---

## Fase 7 — Accessibility Review

Deliverable: **17. Accessibility Guidelines**. Dua langkah:

```text
Review everything designed so far in this project for accessibility: contrast
ratios per theme, focus visibility, touch targets, keyboard reachability of
overlays. List concrete fixes, then apply them.
```

```text
Now produce the RDP UI accessibility guidelines sheet: WCAG AA commitments,
keyboard interaction map per component (Tab/Escape/Arrow behavior), ARIA
attributes each component must render, focus management rules for modal/drawer/
toast, and color-independence rules.
```

---

## Fase 8 — Landing Page

Deliverable: **19. Landing Page Wireframe** (langsung sebagai desain hi-fi).

```text
Design the RDP UI documentation website landing page, in order:

Hero with tagline "Modern UI Framework for Django" + primary CTA (Get Started)
and secondary CTA (GitHub) → feature highlights (HTML first, Cotton components,
HTMX native, 11 themes, accessible, zero build step) → live component preview
strip → interactive theme switcher → full dashboard preview screenshot section →
"Why RDP UI" comparison vs writing custom CSS / Bootstrap / React component
libs → code example section showing the same component as plain HTML, Django
Cotton, and with HTMX → documentation preview → community/GitHub section →
footer.

Must feel like a modern open-source product site (the caliber of shadcn/ui or
Tailwind's sites) but with RDP UI's own visual identity. Mobile-first.
```

---

## Fase 9 — Documentation Website

Deliverables: **18. Documentation Structure, 20. Documentation Wireframe**.

```text
Design the documentation site for RDP UI:

1. Information architecture sheet — sidebar nav covering: Getting Started,
   Installation, Quick Start, Components, Layouts, Patterns, Templates, Themes,
   Icons, Examples, Cookbook, Migration, Roadmap, Changelog, FAQ, Blog; plus
   global search (Cmd+K) and version/theme switchers.
2. The component-page template, designed once and reused for all components,
   containing: Overview, interactive preview with theme switcher, code tabs
   (HTML / Django Cotton / HTMX), API table (attributes, slots, events),
   Accessibility notes, Variants, Customization via CSS variables, Best
   practices.
3. Render one real instance: the full documentation page for the Button
   component.
```

---

## Fase 10 — Dashboard Showcase & Example Applications

Deliverables: **22. Dashboard Showcase, 23. Example Applications**. Mulai dari 4 prioritas; sisanya pakai prompt template yang sama.

```text
Design the flagship "RDP Admin Dashboard" example application: KPI stat cards,
revenue chart placeholder, recent activity table, quick actions, notifications
— using only RDP UI components and the app shell from Phase 4. Show desktop and
mobile. This is the screenshot that sells the framework.
```

```text
Design the Authentication example: login, register, forgot password, and
profile/settings pages using RDP UI components.
```

```text
Design the CRM example: contact list with search/filter/pagination, contact
detail with tabs and timeline, and a pipeline kanban board.
```

```text
Design the Invoice example: invoice list, invoice detail (print-friendly), and
create-invoice form with line items.
```

Template untuk sisanya (ERP, Inventory, POS, Blog, CMS, Analytics, Project Management, Calendar, Email, Chat, Kanban, File Manager):

```text
Design the {NAME} example application using only RDP UI components and existing
patterns from this project. Screens: {2–4 key screens}. Desktop and mobile.
```

---

## Fase 11 — Roadmap & Future Vision

Deliverables: **24. Roadmap, 25. Future Vision**.

```text
Create the final one-pager: RDP UI roadmap and future vision.
Roadmap phases: v0.x foundations & core components → v1.0 stable API + docs
site + 5 example apps → v1.x full theme gallery + cookbook + Django package
(pip installable) → v2.0 ecosystem (community themes, template marketplace,
CLI scaffolding, Figma kit).
Future vision: RDP UI as the default answer to "how do I make my Django app
beautiful without a frontend team".
```

---

## Fase 12 — Export & Handoff

1. Tombol **Export** (kanan atas) per artefak:
   - **Standalone HTML / Download .zip** → arsipkan ke `docs/design/rdp-ui/` di repo ini sebagai referensi hidup.
   - **PDF / PPTX** → untuk review stakeholder.
2. **Handoff to Claude Code** saat siap implementasi — Claude Code melanjutkan dari desain, bukan dari screenshot. Bisa juga lewat MCP:
   `claude mcp add --scope user --transport http claude-design https://api.anthropic.com/v1/design/mcp` lalu `/design-login`.
3. Simpan versi sebelum eksplorasi arah baru: bilang saja *"Save what we have and try a completely different approach."*

---

## Checklist: 25 Deliverables → Fase

| # | Deliverable | Fase |
|---|---|---|
| 1–3 | Positioning, Personas, Design Principles | 1 |
| 4–10 | Visual Language, Color, Typography, Spacing, Radius, Elevation, Iconography | 2 |
| 13 | Theme Architecture | 3 |
| 11–12 | Layout System, Responsive Strategy | 4 |
| 14, 21 | Component Architecture, Component Showcase | 5 |
| 15–16 | Interaction & Motion Guidelines (+ pola HTMX) | 6 |
| 17 | Accessibility Guidelines | 7 |
| 19 | Landing Page | 8 |
| 18, 20 | Documentation Structure & Wireframe | 9 |
| 22–23 | Dashboard Showcase, Example Applications | 10 |
| 24–25 | Roadmap, Future Vision | 11 |

## Tips (dari dokumentasi resmi)

- Feedback harus spesifik: "tighten spacing between form fields to 8px", bukan "kurang bagus".
- Sebut nama komponen/token yang sudah dibuat: "use --rdp-space-4 here", "apply the Card pattern".
- Ragu arah? Minta 2–3 variasi, bandingkan, baru pilih.
- Minta Claude me-review desainnya sendiri (aksesibilitas, hierarki, kontras) — perlakukan sebagai kolaborator, bukan generator.
- Jika inline comment tidak terbaca (bug intermiten), paste isi komentar ke chat.
- Jika kena "chat upstream error", buka tab chat baru di project yang sama.
- Pemakaian Claude Design memotong kuota usage yang sama dengan chat/Claude Code/Cowork — project besar & banyak iterasi = kuota lebih cepat habis. Selesaikan satu fase per sesi.
