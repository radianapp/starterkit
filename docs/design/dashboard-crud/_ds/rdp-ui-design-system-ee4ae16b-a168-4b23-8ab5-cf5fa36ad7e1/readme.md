# RDP-UI Design System

**RDP-UI** is the design system and CSS framework for the **Radian Data Platform (RDP)** — a family of server-rendered business tools (admin dashboards, CRM, invoicing, HRM, auth) built on **Django + django-cotton + HTMX**. Its philosophy is HTML-first, server-first, zero build step: plain CSS, component classes (`.rdp-btn`, `.rdp-card`), Cotton template components (`<c-rdp.*>`), and HTMX as the interactivity layer. No React in production, no utility-class soup, WCAG AA throughout, and 11 swappable themes implemented purely as CSS-variable overrides on `[data-rdp-theme]`.

## Sources
- Codebase (mounted): `ui.radian.web.id/` — the CDN/docs repo. `assets/rdp.css` (~2,700 lines, the whole framework), `assets/components/*.css` (21 add-on component files), `assets/themes/*.css` (11 themes), plus a full design-handoff spec in `docs/design/handover/`.
- GitHub: https://github.com/radianapp/ui (same content; auto-deployed to https://ui.radian.web.id via Cloudflare Pages). Explore it — especially `docs/design/handover/README.md` and the `.dc.html` spec sheets — to design deeper against this product. Related: https://github.com/radianapp/starterkit (the upstream source of truth for the CSS).
- The real stylesheet is copied verbatim into this project at `assets/` and shipped via `styles.css`. Consumers get the exact production CSS, not a recreation.

## Products represented
1. **RDP application UI** — the app shell (dark sidebar + topbar + content), dashboards, tables, forms; used by all RDP example apps (admin dashboard, auth, CRM, invoicing, HRM).
2. **RDP-UI docs/marketing site** (ui.radian.web.id) — landing page with hero, step cards, docs grid, dark examples band, theme switcher.

## CONTENT FUNDAMENTALS
- Product copy is **English**; internal dev docs are Indonesian. Design deliverables use English.
- Tone: **technical, confident, compressed**. Feature triads and em-dash chains: "HTML first, server first, zero build step." "A complete ecosystem — design system, CSS framework, Django Cotton components, and HTMX patterns."
- Benefit lines are plain and slightly wry: "Beautiful Django apps without a frontend team." "If you can write a Django template, you already know how to use it."
- Sentence case everywhere except tiny overline labels (ALL-CAPS, letterspaced: "GET STARTED", "DOCS", "v0.x · DESIGN SPEC COMPLETE").
- Speaks to the reader as "you"; the product is named ("RDP-UI"), never "we".
- **No emoji.** Checkmarks are ✓ glyphs; card glyphs are geometric unicode (▦ ◈ ◎ ▤ ◐).
- Numbers and code are shown in mono (IBM Plex Mono); code samples are syntax-tinted on near-black (#1C1B18) panels.

## VISUAL FOUNDATIONS
- **Color**: "warm paper" default theme. Background `#FAF9F7` (warm off-white), surfaces white, ink `#1C1B18` (warm near-black, never pure black). Primary is deep green `#15654E` (hover `#10513F`, tint `#EDF4F0`). Full 10-step scales for green, warm neutral, blue (info), red (danger), yellow (warning), emerald (success). Strict 3-layer token architecture: primitive scales → semantic tokens (`--rdp-primary`, `--rdp-surface`) → components. Themes override ONLY semantic tokens.
- **Type**: Instrument Sans (400/500/600/700) for everything; IBM Plex Mono for code/timestamps/tabular data. Display 3rem/1.1 bold, h1 2.25rem, body 1rem/1.6, small .875rem, caption .75rem medium. Negative tracking on headings (-0.02em h1) and +0.08–0.10em on uppercase labels. No serif.
- **Spacing**: 4px base scale (`--rdp-space-1..10`: 4→128px) with xs/sm/md/lg/xl aliases (8/12/16/24/32).
- **Radii**: xs 4, sm 6 (buttons/inputs), md 10 (cards, alerts), lg 14 (modals, large cards), xl 20, full pill. Nesting rule: inner = outer − padding.
- **Shadows**: two-layer (tight contact + soft ambient), always tinted with warm ink `rgba(28,27,24,…)`, never pure black, never Material. Flat contexts use border-based elevation (`0 0 0 1px border`).
- **Borders**: 1px `#E5E2DC` everywhere; `#D2CEC6` for strong/inputs. Dashed 1.5–2px borders for dropzones/empty states.
- **Backgrounds**: flat solid colors only — **no gradients, no textures, no imagery, no illustrations**. Full-bleed dark bands (`#1C1B18`) for footers/example sections. Sidebar is warm near-black with white-alpha text layers.
- **Motion**: 100/200/300/500ms; standard cubic-bezier(.4,0,.2,1) plus a spring (.34,1.56,.64,1). Animate opacity/transform only; fade-in, slide-up 1rem, shimmer for skeletons. Respects prefers-reduced-motion.
- **Hover states**: background tint shifts (surface→sunken), border darkens, link underline fades in via text-decoration-color. **Press**: buttons translateY(1px) or scale(.98). **Focus**: 2px green outline, offset 2px (or double ring box-shadow).
- **Cards**: white, 1px border, radius 10–14px, shadow-1; hoverable cards lift 1px with shadow-2.
- **Transparency/blur**: only modal backdrops (ink at 50% + 2–4px blur). No glassmorphism.
- **Density**: enterprise-compact; 14px body in app UI, 40px input/button heights (32 sm, 48 lg), 44px+ touch targets.

## ICONOGRAPHY
- The spec mandates SVG icons on a **24px grid, 1.5px stroke, rounded caps/joins** — exactly the Lucide style. The repo ships no icon files yet; the CSS embeds inline data-URI SVGs (chevron-down for selects, checkmark for checkboxes) in that same style.
- **Use Lucide from CDN** in kits and mocks (`lucide` UMD or inline copied paths, 1.5px stroke). This is a flagged substitution until the real `icons/*.svg` set exists.
- Decorative glyphs on marketing surfaces are unicode geometric shapes (▦ ◈ ◎ ▤ ◐) and ✓ — never emoji.
- **No logo asset exists.** The brand mark in the source is a CSS-drawn 28px green (#15654E) rounded square (6px) containing a bold white "R", next to the wordmark "RDP-UI" in bold Instrument Sans. Recreate it with CSS/type (see `components/layout/`), never draw a logo.

## Index
- `styles.css` — global entry; imports fonts + the verbatim production CSS.
- `assets/` — `rdp.css` (framework), `rdp.js` (vanilla helpers), `components/*.css` (21 add-ons), `themes/*.css` (11 themes: default, light, dark, midnight, nord, dracula, forest, ocean, corporate, github, terminal).
- `tokens/fonts.css` — Google Fonts loading (Instrument Sans, IBM Plex Mono).
- `components/` — React wrappers over the real `.rdp-*` classes, grouped: `primitives/` (Icon, Button, Badge, Avatar, Spinner, Loader, Skeleton, Progress, Rating), `forms/` (FormField, Input, Textarea, Select, Checkbox, Radio, Switch, SearchBox, FileUpload), `feedback/` (Alert, Toast, Modal, Confirm, Drawer, Tooltip, EmptyState), `navigation/` (Tabs, Dropdown, Pagination, Breadcrumb, Steps), `data/` (Card, StatCard, Table, Accordion, Timeline, FilterBar), `layout/` (Sidebar, Topbar, PageHeader, BrandMark).
- `guidelines/` — foundation specimen cards shown in the Design System tab.
- `ui_kits/dashboard/` — RDP admin app shell recreation (interactive).
- `ui_kits/website/` — ui.radian.web.id landing recreation.
- `SKILL.md` — agent skill entry point.

## Intentional additions
- React wrapper components (`components/`) — RDP-UI itself is React-free; wrappers exist only so design tools can compose the real CSS classes. Class names, values, and states are copied from source.
- Lucide CDN icons — stand-in matching the spec's icon rules until real SVGs ship.
