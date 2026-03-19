# CSS Framework Guide

This guide explains the custom class-based CSS framework used in this project.

## How To Use

- `u-*` classes are **utility classes**. Use them to style layout, spacing, typography, and common UI pieces.
- `k-*` classes are **Kanban component classes**. Use them for board/page structure.
- You can combine classes on one element (example: `class="u-row u-items-center u-gap-sm"`).

---

## Design Tokens (`:root`)

These are reusable variables for colors, spacing feel, and shadows.

- `--app-bg`: app background base color
- `--surface`, `--surface-strong`: translucent card/panel backgrounds
- `--line`: border color
- `--text-primary`, `--text-muted`: text colors
- `--brand`, `--brand-strong`: brand accent colors
- `--danger`: destructive/alert color
- `--todo`, `--doing`, `--done`: status colors
- `--energy-*`: chip colors by energy level
- `--radius-md`, `--radius-lg`: border radii
- `--shadow-md`, `--shadow-lg`: shadow styles

Example:

```css
.my-card {
  background: var(--surface-strong);
  border: 1px solid var(--line);
  border-radius: var(--radius-md);
}
```

---

## Base Styles

- `* { box-sizing: border-box; }`: easier size calculations
- `body`: sets global font, min height, and base layout behavior
- `h1,h2,h3,p` margin reset
- `a` inherits color and removes default underline

---

## Utility Classes (`u-*`)

### Background and Visual Effects

- `u-bg-app`: applies full-page gradient background
- `u-bg-shape`: base class for soft floating blur shapes
- `u-bg-shape-a`, `u-bg-shape-b`: positioned variants of background shapes

Example:

```html
<body class="u-bg-app">
  <div class="u-bg-shape u-bg-shape-a" aria-hidden="true"></div>
  <div class="u-bg-shape u-bg-shape-b" aria-hidden="true"></div>
</body>
```

### Typography

- `u-text-primary`: primary text color
- `u-text-muted`: secondary/muted text color
- `u-text-sm`: small text
- `u-text-lg`: large text
- `u-text-xl`: responsive extra-large text
- `u-font-display`: display heading font style
- `u-label`: small uppercase section label

Example:

```html
<p class="u-label">Overview</p>
<h2 class="u-font-display u-text-xl">Board Title</h2>
<p class="u-text-sm u-text-muted">Helper text</p>
```

### Layout Helpers

- `u-row`: `display: flex`
- `u-items-center`: vertically center items in flex
- `u-justify-between`: push items to edges in flex
- `u-gap-sm`: small gap
- `u-gap-md`: medium gap
- `u-hide-mobile`: hidden at smaller breakpoints (via media query)

Example:

```html
<div class="u-row u-items-center u-justify-between u-gap-md">
  <span>Left</span>
  <span>Right</span>
</div>
```

### Surfaces and Pills

- `u-glass`: frosted glass panel style (border + blur + shadow)
- `u-chip`: rounded inline badge/chip
- `u-pill`: compact count badge

Example:

```html
<header class="u-glass">
  <span class="u-chip">v1.1</span>
  <span class="u-pill">12</span>
</header>
```

### Links and Buttons

- `u-link`: nav/link style
- `is-active`: active state modifier for `u-link`
- `u-btn`: base button style
- `u-btn-primary`: primary gradient button style
- `u-card-link`: action link style inside cards
- `u-card-link-danger`: danger variant for destructive action

Example:

```html
<a class="u-link is-active" href="#">Projects</a>
<button class="u-btn u-btn-primary">Create Board</button>
<a class="u-card-link u-card-link-danger" href="#">Clear</a>
```

### Energy Tags

- `u-energy`: base energy chip style
- `u-energy-1`: easy
- `u-energy-2`: medium
- `u-energy-3`: deep work

Example:

```html
<span class="u-energy u-energy-1">Easy</span>
<span class="u-energy u-energy-2">Medium</span>
<span class="u-energy u-energy-3">Deep Work</span>
```

### Accessibility and Motion

- `u-sr-only`: visually hide text but keep it for screen readers
- `u-fade-in`: entrance animation helper

Example:

```html
<label for="board_name" class="u-sr-only">Board name</label>
<section class="u-fade-in">...</section>
```

---

## Kanban Component Classes (`k-*`)

### Page Structure

- `k-shell`: centered page container
- `k-topbar`: sticky top navigation/header area
- `k-logo-mark`: square gradient logo block
- `k-hero`: top hero section grid
- `k-quick-add`: quick form grid layout

Example:

```html
<header class="k-topbar u-glass">...</header>
<main class="k-shell">
  <section class="k-hero u-glass">...</section>
</main>
```

### Board Layout

- `k-board`: main board grid (3 columns desktop)
- `k-column`: column container
- `k-column-head`: column title + counter row
- `k-dropzone`: card container area (drop target for drag/drop)
- `k-dropzone is-over`: highlighted dropzone state

Example:

```html
<section class="k-board">
  <article class="k-column">
    <header class="k-column-head">...</header>
    <div class="k-dropzone">...</div>
  </article>
</section>
```

### Card Styles

- `k-card`: base card
- `k-card-title`: card text/title style
- `k-card-active`: in-progress card accent
- `k-card-done`: done card accent
- `k-card is-dragging`: style while being dragged

Example:

```html
<div class="k-card k-card-active">
  <p class="k-card-title">Implement drag and drop</p>
</div>
```

---

## Responsive Behavior

- At `max-width: 980px`:
  - `k-topbar` simplifies layout
  - `u-hide-mobile` is hidden
  - `k-hero` becomes single-column
  - `k-board` becomes 2 columns
- At `max-width: 680px`:
  - shell/topbar width adjusts
  - `k-board` becomes 1 column
  - `k-quick-add` stacks vertically

---

## Quick Build Pattern

Use this order when building a new page:

1. `body` with `u-bg-app u-text-primary`
2. top navigation using `k-topbar u-glass`
3. content container with `k-shell`
4. intro section with `k-hero u-glass`
5. board grid with `k-board` and `k-column`
6. cards with `k-card` + utility text/link classes
