# Handoff: RDP UI — Modern UI Framework for Django

## Overview
RDP UI is a complete UI ecosystem natively built for **Django + django-cotton + HTMX**:
a design system, a classless-leaning CSS framework, a Cotton component library
(`<c-rdp.*>`), 11 themes, HTMX interaction patterns, a documentation site, and 5
example applications. This handoff contains the full product design specification.

## About the Design Files
Every `.dc.html` file in this bundle is a **design reference created in HTML** — a
high-fidelity spec sheet or screen mockup, NOT production code. Your task in Claude
Code is to **implement RDP UI as a real, pip-installable Django package** using the
specs as the source of truth. Do not copy the HTML directly; recreate the components,
tokens, and screens following the contracts defined in the specs.

## Fidelity
**High-fidelity.** Colors, type scale, spacing, radii, shadows, component states, and
ARIA/keyboard behavior in the spec sheets are final. Implement pixel-perfectly.

## Core Philosophy (non-negotiable constraints)
1. **HTML first** — semantic HTML; no utility-class soup. Components are styled by
   component classes (`.rdp-button`) + data attributes (`data-variant="primary"`).
2. **Component first** — every component ships as a Cotton template callable as
   `<c-rdp.{name}>`, attributes = props, `<c-slot name="…">` = named slots.
3. **Server first** — HTMX is the interactivity layer. No React. Vanilla JS only for
   focus traps, dropdown positioning, toast timers.
4. **Accessibility first** — WCAG AA. Follow `accessibility-guidelines.dc.html`
   exactly: keyboard maps, ARIA attributes per component, focus management.
5. **Theme first** — every color/size/shadow comes from a CSS variable. A theme is
   ONLY a set of variable overrides on `[data-rdp-theme="…"]` — never extra rules.
6. **Minimal API** — small surface; prefer one component with variants over many.
7. **Enterprise ready** — density options, tables, app shell, dashboards.

## Recommended Repository Structure
```
rdp-ui/
├── pyproject.toml                  # package name: rdp-ui, app: rdp_ui
├── rdp_ui/
│   ├── static/rdp/
│   │   ├── rdp.css                 # the full framework (tokens + components)
│   │   ├── themes/*.css            # 11 theme files (variable overrides only)
│   │   ├── rdp.js                  # tiny vanilla helpers (focus trap, toast, menu)
│   │   └── icons/*.svg             # 24px grid, 1.5px stroke, rounded caps
│   └── templates/cotton/rdp/       # Cotton components → <c-rdp.*>
│       ├── button.html  card.html  input.html  modal.html  table.html  …
├── docs/                           # documentation site (Django or static)
└── examples/                       # admin dashboard, auth, crm, invoicing, hrm
```

## Implementation Order (suggested Claude Code phases)
1. **Tokens** (`foundations.dc.html`) — write the `:root` variable layer:
   `--rdp-*` color/type/space/radius/shadow/duration/ease tokens.
2. **Themes** (`theme-architecture.dc.html`) — primitive → semantic → component
   token inheritance; 11 themes as `[data-rdp-theme]` overrides.
3. **Layout** (`layout-system.dc.html`) — container, 12-col grid, app shell
   (collapsible sidebar, navbar, drawer on mobile), breakpoints.
4. **Core components** (`component-showcase.dc.html`, `forms-showcase.dc.html`,
   `overlays-and-navigation.dc.html`, `data-display.dc.html`) — CSS + Cotton
   template per component. Each spec sheet lists variants, states, and the CSS
   variables each component consumes.
5. **Component contracts** (`component-architecture.dc.html`) — anatomy,
   slots, props naming. This defines the `<c-rdp.*>` API; freeze it.
6. **HTMX patterns** (`htmx-interaction-patterns.dc.html`) — modal via hx-get,
   422 validation re-render, active search, infinite scroll, toasts, indicators;
   plus motion tokens and `prefers-reduced-motion` behavior.
7. **Accessibility pass** (`accessibility-guidelines.dc.html`) — keyboard maps,
   ARIA per component, focus rules. Treat as acceptance criteria.
8. **Docs site** (`docs-site-landing.dc.html`, `docs-site-structure.dc.html`,
   `index.dc.html`) — landing + component-page template (preview, code tabs
   HTML/Cotton/HTMX, API table, a11y notes).
9. **Examples** (`admin-dashboard-example.dc.html`, `auth-example.dc.html`,
   `crm-example.dc.html`, `invoice-example.dc.html`, `hrm-example.dc.html`) —
   build using ONLY the published components; they double as integration tests.

## Design Tokens (canonical values live in foundations.dc.html)
- Spacing: 4px base scale → `--rdp-space-1 … --rdp-space-16`
- Radius: subtle → pill → `--rdp-radius-xs … --rdp-radius-full`
- Type: system-first stack + optional webfont; display, h1–h6, body, small,
  caption, code — all as variables
- Shadows: soft layered, never Material; border-based elevation for flat contexts
- Motion: `--rdp-duration-*`, `--rdp-ease-*`; animate opacity/transform only

## Acceptance Criteria
- Zero build step: plain CSS + Cotton templates work with `{% static %}` alone.
- Every color combination passes WCAG AA in all 11 themes.
- All overlays keyboard-reachable: Tab cycle, Escape close, focus trap + return.
- Switching `data-rdp-theme` restyles the entire app with no other change.
- No React, no bundler, no utility classes in userland HTML.

## Files in This Bundle
| File | Contents |
|---|---|
| `index.dc.html` | Official landing page linking all docs & examples |
| `product-foundation.dc.html` | Positioning, personas, 7 design principles |
| `foundations.dc.html` | Color/type/space/radius/elevation/icon tokens |
| `theme-architecture.dc.html` | Token inheritance + 11-theme gallery |
| `layout-system.dc.html` | Grid, app shell, responsive strategy |
| `component-showcase.dc.html` | Buttons, badges, alerts, toasts, progress… |
| `forms-showcase.dc.html` | Inputs, selects, validation, 422 state |
| `overlays-and-navigation.dc.html` | Modal, drawer, dropdown, tabs, sidebar… |
| `data-display.dc.html` | Tables, cards, stats, timeline, empty states |
| `component-architecture.dc.html` | Component anatomy + Cotton mapping |
| `htmx-interaction-patterns.dc.html` | 12 HTMX patterns + motion guidelines |
| `accessibility-guidelines.dc.html` | WCAG AA, keyboard maps, ARIA, focus |
| `docs-site-landing.dc.html`, `docs-site-structure.dc.html` | Docs site design |
| `admin-dashboard-example.dc.html` + auth/crm/invoice/hrm | Example apps |
| `roadmap-and-vision.dc.html` | v0.x → v2.0 roadmap |

Note: `.dc.html` files reference a `support.js` runtime (included) — open them in a
browser to view; the runtime is a preview aid only and is not part of RDP UI.

## Suggested First Prompt for Claude Code
> Read design_handoff_rdp_ui/README.md. Implement RDP UI as a pip-installable
> Django package following the Implementation Order. Start with Phase 1 (tokens)
> and Phase 2 (themes), rendering a test page that shows the token sheet in all
> 11 themes before moving on.
