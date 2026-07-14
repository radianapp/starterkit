# RDP UI — CSS Framework Design Specification (design.md)

**Modern UI Framework for Django** · v0.1
Complete ecosystem: Design System · CSS Framework · Django Cotton components (`<c-rdp.*>`) · HTMX patterns · 11 Themes · Docs site · Example apps.

This document is the canonical written spec of the visual design defined in the project's spec sheets (`foundations.dc.html`, `theme-architecture.dc.html`, `layout-system.dc.html`, component showcases, `htmx-interaction-patterns.dc.html`, `accessibility-guidelines.dc.html`). Values below are the source-of-truth token values.

---

## 1. Philosophy (non-negotiable)

1. **HTML First** — semantic HTML; component classes (`.rdp-button`) + data attributes (`data-variant="primary"`, `data-size="sm"`); never utility-class soup.
2. **Component First** — every component ships as a Cotton template: `<c-rdp.{name}>`; attributes = props, `<c-slot name="…">` = named slots.
3. **Server First** — HTMX is the interactivity layer. No React, no bundler, zero build step. Vanilla JS only for focus traps, positioning, toast timers.
4. **Accessibility First** — WCAG AA everywhere: contrast, keyboard, focus, ARIA.
5. **Theme First** — every color/size/shadow/duration is a `--rdp-*` CSS variable. A theme is ONLY variable overrides on `[data-rdp-theme="…"]` — never extra rules.
6. **Minimal API** — one component with variants beats many components.
7. **Enterprise Ready** — density modes, tables, app shell, dashboards, print.

**Design language:** minimal, elegant, soft, premium. Warm-gray neutrals (never cold blue-gray), deep green primary, generous whitespace, hairline borders, soft ink-tinted shadows. NOT Bootstrap, NOT Material, NOT admin-template.

---

## 2. Color system

Rule: **components reference semantic tokens only.** Raw scales exist to derive themes; dark mode is a token swap, never a component change. All text/surface pairs pass WCAG AA (≥4.5:1); non-text edges ≥3:1.

### Semantic tokens (Light · Dark)

| Token | Role | Light | Dark |
|---|---|---|---|
| `--rdp-primary` | Primary actions, links, active states | `#15654E` | `#5FA98C` |
| `--rdp-primary-hover` | Hover/pressed shift of primary | `#10513F` | `#78BCA2` |
| `--rdp-primary-soft` | Tinted backgrounds, selected rows | `#EDF4F0` | `#12352A` |
| `--rdp-on-primary` | Text/icons on primary fills | `#FFFFFF` | `#082A21` |
| `--rdp-background` | App canvas | `#FAF9F7` | `#171614` |
| `--rdp-surface` | Cards, panels, table bodies | `#FFFFFF` | `#1F1E1B` |
| `--rdp-surface-raised` | Dropdowns, popovers, modals | `#FFFFFF` | `#262522` |
| `--rdp-surface-sunken` | Wells, code blocks, table headers | `#F2F0EC` | `#131210` |
| `--rdp-text` | Headings, body, values | `#1C1B18` | `#F2F0EC` |
| `--rdp-text-muted` | Descriptions, labels, meta | `#6B665E` | `#B0ABA1` |
| `--rdp-border` | Hairlines: cards, dividers, tables | `#E5E2DC` | `#33302C` |
| `--rdp-border-strong` | Input borders, interactive edges | `#D2CEC6` | `#4E4A44` |
| `--rdp-focus` | 2px focus ring, offset 2px, everywhere | `#15654E` | `#5FA98C` |
| `--rdp-success` | Confirmation, positive deltas | `#1E7A46` | `#66BE8C` |
| `--rdp-warning` | Caution, pending, degraded | `#9A6A0B` | `#D9A441` |
| `--rdp-danger` | Destructive actions, errors | `#B3382D` | `#E08273` |
| `--rdp-info` | Neutral notices, in-progress | `#2A5FA8` | `#82AEE3` |

Each status color also ships a `-soft` background tint (e.g. `--rdp-success-soft`).

### Primitive scales

**Neutral (warm gray) `--rdp-neutral-*`:**
50 `#FAF9F7` · 100 `#F2F0EC` · 200 `#E5E2DC` · 300 `#D2CEC6` · 400 `#B0ABA1` · 500 `#8A857C` · 600 `#6B665E` · 700 `#4E4A44` · 800 `#33302C` · 900 `#1C1B18`

**Primary (green) `--rdp-green-*`:**
50 `#EDF4F0` · 100 `#D6E7DF` · 200 `#ACCFC1` · 300 `#7DB3A0` · 400 `#5FA98C` · 500 `#2A7A5E` · 600 `#15654E` · 700 `#10513F` · 800 `#0C3D30` · 900 `#082A21`

Inheritance model: **primitive tokens → semantic tokens → component tokens** (e.g. `--rdp-green-600` → `--rdp-primary` → `--rdp-button-bg`).

---

## 3. Typography

System-first (zero-request); **Instrument Sans** is the optional premium webfont. 1rem = 16px, scale is rem-based.

```css
--rdp-font-sans: "Instrument Sans", ui-sans-serif, system-ui, -apple-system, "Segoe UI", sans-serif;
--rdp-font-mono: "IBM Plex Mono", ui-monospace, "SF Mono", Menlo, monospace;
--rdp-weight-regular: 400; --rdp-weight-medium: 500;
--rdp-weight-semibold: 600; --rdp-weight-bold: 700;
```

Type scale (size / line-height / weight / letter-spacing):

- `--rdp-text-display` — 3rem / 1.1 / 700 / −0.025em · hero & marketing only
- `--rdp-text-h1` — 2.25rem / 1.15 / 700 / −0.02em · one per page
- `--rdp-text-h2` — 1.75rem / 1.2 / 700 / −0.015em · section heading
- `--rdp-text-h3` — 1.375rem / 1.3 / 600 / −0.01em · card & panel heading
- `--rdp-text-h4` — 1.125rem / 1.4 / 600 · subsection
- `--rdp-text-h5` — 1rem / 1.5 / 600 · widget heading
- `--rdp-text-h6` — 0.8125rem / 1.5 / 600 / +0.08em UPPERCASE · group label
- `--rdp-text-body` — 1rem / 1.6 / 400 · default reading size
- `--rdp-text-small` — 0.875rem / 1.55 / 400 · dense UI, table cells, sidebars
- `--rdp-text-caption` — 0.75rem / 1.45 / 500 · timestamps, helper text — never smaller
- `--rdp-text-code` — 0.875rem / 1.6 / 500 mono · code, tokens, kbd

Rules: max two weights per view beyond regular · body text ≥0.875rem in app UI · prose measure 45–75ch · headings use `text-wrap: balance`.

---

## 4. Spacing

4px base, nine tokens. If a design needs a value between steps, snap it.

`--rdp-space-1..9` = 4, 8, 12, 16, 24, 32, 48, 64, 96 px

Usage rules:
- **Component padding** — compact controls 8×12 · buttons/inputs 12×16 · cards/panels 24 · modals/drawers 32
- **Stack gaps** — label→control 8 · form fields 16 · cards in grid 24 · unrelated blocks 32
- **Section rhythm** — page gutter 24–32 · between page sections 48 · marketing sections 64–96
- Rule: space **between** groups > space **within** them.

---

## 5. Radius

Soft, never bubbly. Nesting rule: inner radius = outer radius − padding, floored at `xs`.

- `--rdp-radius-xs` 4px — checkboxes, tags, kbd, nested elements
- `--rdp-radius-sm` 6px — buttons, inputs, selects, menu items
- `--rdp-radius-md` 10px — cards, alerts, popovers, dropdowns
- `--rdp-radius-lg` 14px — modals, drawers, command palette
- `--rdp-radius-xl` 20px — hero panels, feature tiles, empty states
- `--rdp-radius-pill` 999px — badges, avatars, switches, filter chips

Themes may shift the whole system via `--rdp-radius-scale`: 0 sharp enterprise · 1 default · 1.5 friendly consumer.

---

## 6. Elevation

Two-layer shadows — tight contact + wide soft ambient — tinted with the ink color `#1C1B18`, never pure black. Elevation = layer, not importance.

```css
--rdp-shadow-1: 0 1px 2px rgba(28,27,24,.05);                              /* Rest: cards, inputs */
--rdp-shadow-2: 0 1px 2px rgba(28,27,24,.04), 0 4px 12px rgba(28,27,24,.07);  /* Raised: dropdowns, hover lift */
--rdp-shadow-3: 0 2px 6px rgba(28,27,24,.05), 0 12px 32px rgba(28,27,24,.10); /* Overlay: modals, drawers */
--rdp-shadow-4: 0 4px 12px rgba(28,27,24,.06), 0 24px 56px rgba(28,27,24,.14);/* Peak: toasts, spotlight */
--rdp-elevation-border: 0 0 0 1px var(--rdp-border);                       /* flat contexts: dense tables, sidebars, print */
```

Dark mode: shadows barely read — elevation switches to **surface steps** (`surface` → `surface-raised`) + `--rdp-border`. Same tokens, remapped by the theme.

---

## 7. Iconography

Quiet line icons; they are text — `stroke: currentColor`, tinted by the same tokens.

- Grid **24×24**, 2px safe area · stroke **1.75px** non-scaling · round caps & joins · 2px optical corner rounding · fill: none (`-fill` suffix for solid variants)
- Naming: kebab-case `object-modifier` (`arrow-right`, `chevron-down`)
- Cotton: `<c-rdp.icon name="bell" />` · sizes 16 / 20 / 24 only · always `aria-hidden="true"` beside a visible label
- Metaphor rules: one concept per icon · no perspective/3D/fills at rest · >3 strokes needed → use a word instead.

---

## 8. Motion

Animate **opacity and transform only** — never width/height/top/left; never animate color of large surfaces.

- `--rdp-duration-fast` 120ms — hover, focus ring, chevrons
- `--rdp-duration-base` 200ms — HTMX swaps, dropdowns, toasts
- `--rdp-duration-slow` 300ms — modal, drawer, accordion
- `--rdp-ease-out` `cubic-bezier(0.16, 1, 0.3, 1)` — entrances (default)
- `--rdp-ease-in` `cubic-bezier(0.7, 0, 0.84, 0)` — exits (faster than entrances)

`prefers-reduced-motion: reduce` → all durations drop to 0ms; state changes remain instant, nothing depends on animation to be understood.

---

## 9. Theming

A theme = **only** variable overrides:

```css
[data-rdp-theme="ocean"] { --rdp-primary: …; --rdp-surface: …; }
```

11 built-in themes: Default (light, green/warm-gray as above), Light, Dark, Corporate, Ocean, Forest, Midnight, Terminal, Nord, Dracula, GitHub. Nord/Dracula/GitHub follow their canonical palettes; the rest are original RDP palettes. Switching `data-rdp-theme` on `<html>` restyles the entire app with no other change. Every theme must keep all AA contrast pairs.

---

## 10. Layout

- Container widths: sm 640 / md 768 / lg 1024 / xl 1280 / max 1440, centered, gutter `--rdp-space-5..6`.
- 12-column grid (`display: grid` + `gap: var(--rdp-space-5)`).
- Canonical app shell: collapsible sidebar (260px → 64px icon rail) · top navbar 64px with search / notifications / user menu · content area on `--rdp-background` · optional right panel.
- Mobile-first breakpoints; below `lg` the sidebar becomes a drawer (focus-trapped), navbar collapses to hamburger.
- Touch targets ≥ 44×44px; interactive rows ≥ 40px tall.

---

## 11. Component conventions

- Class naming: `.rdp-{component}`; variants/sizes/states via data attributes: `data-variant`, `data-size`, `data-state`, `data-density`.
- Every component documents the **component tokens it consumes** (e.g. button: `--rdp-primary`, `--rdp-on-primary`, `--rdp-radius-sm`, `--rdp-space-3/4`, `--rdp-shadow-1`, `--rdp-duration-fast`).
- States for every interactive component: rest, hover, focus-visible (2px `--rdp-focus` ring, 2px offset), active, disabled (opacity .5, `cursor: not-allowed`, still AA-readable), loading (spinner replaces label, width preserved, `aria-busy`).
- Buttons: variants primary / secondary / outline / ghost / danger; sizes sm 32px / md 40px / lg 48px height; icon buttons square with `aria-label`.
- Inputs: 40px height md, `--rdp-border-strong` border, `--rdp-radius-sm`; validation via `data-state="invalid"` + `--rdp-danger` border + error text linked by `aria-describedby` (this is the HTMX 422 partial re-render contract).
- Overlays (modal/drawer/dropdown): `--rdp-surface-raised`, `--rdp-shadow-3`, focus trap, Escape closes, focus returns to trigger; backdrop `rgba(28,27,24,.5)`.
- Tables: header on `--rdp-surface-sunken`, hairline `--rdp-border` rows, densities comfortable (52px rows) and dense (40px).
- Density and theme never change markup — tokens only.

### Cotton contract example

```html
<c-rdp.card>
  <c-slot name="header">Team members</c-slot>
  …body…
  <c-slot name="footer"><c-rdp.button variant="primary">Save</c-rdp.button></c-slot>
</c-rdp.card>
```

---

## 12. Accessibility commitments

- WCAG AA: text ≥4.5:1, large text & non-text ≥3:1 — verified per theme.
- Visible focus everywhere: `outline: 2px solid var(--rdp-focus); outline-offset: 2px`.
- Full keyboard maps: Tab/Shift+Tab through all controls; Escape closes overlays; Arrow keys within menus, tabs, radio groups; Home/End at extremes.
- ARIA per component: `role="dialog"` + `aria-modal`, `aria-expanded`/`aria-controls` on disclosure triggers, `aria-live="polite"` toasts, `aria-sort` on sortable headers, `aria-current` on nav.
- Color independence: status always paired with icon or text, never color alone.

---

## 13. Voice & aesthetic checklist (per screen)

- Warm-gray neutrals, one green accent; 1–2 background colors max.
- Hairline borders + shadow-1 for structure; whitespace does the hierarchy.
- Sentence-case labels; concise, verb-first buttons ("Save changes", not "Submit").
- No gradients-as-decoration, no emoji, no rounded-corner-with-left-accent boxes.
- Every color/size traced to a `--rdp-*` token — zero hardcoded values.
