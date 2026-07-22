# School Landing Page — Design Instruction Set

## Project Context
- **Framework**: Django (Python)
- **Templates**: Django Template Language (DTL)
- **CSS Framework**: Bootstrap 5.3
- **Icons**: Bootstrap Icons 1.11
- **Font**: Plus Jakarta Sans (400, 600, 700, 800)
- **Base Template**: `templates/base.html`

---

## Landing Page Types

### 1. SaaS Platform Landing (`core/index.html`)
- **Route**: `/` (main domain)
- **Purpose**: Market the EduSaaS platform to schools
- **Theme**: Dark (`#0b0c10` background)
- **Accent Color**: Lime green (`#d1ff4c`)
- **Audience**: School administrators / decision makers

### 2. School Public Landing (`core/index_subdomain.html`)
- **Route**: `/` (accessed via subdomain, e.g., `academy.yourdomain.com`)
- **Purpose**: Public-facing website for an individual school
- **Theme**: Light (`#f8fafc` background)
- **Accent Color**: Navy blue (`#1a365d`) + Blue (`#2b6cb0`)
- **Audience**: Parents, students, teachers, visitors

---

## Design System

### Color Palette

| Token | SaaS Platform (Dark) | School Page (Light) |
|-------|---------------------|---------------------|
| Background | `#0b0c10` | `#f8fafc` |
| Card Background | `#1f2229` | `#ffffff` |
| Card Border | `rgba(255,255,255,0.06)` | `#e2e8f0` |
| Primary Accent | `#d1ff4c` (lime) | `#1a365d` (navy) |
| Secondary Accent | `#3b82f6` (blue) | `#2b6cb0` (blue) |
| Text Primary | `#ffffff` | `#1a202c` |
| Text Secondary | `#a9a9a9` | `#718096` |
| Input Background | `#15171c` | `#f8fafc` |

### Typography
- **Font Family**: `Plus Jakarta Sans`, sans-serif
- **Headings**: weight 800, letter-spacing `-0.04em`
- **Body**: weight 400, line-height 1.7
- **Labels/Badges**: weight 700, uppercase, letter-spacing `0.1em`

### Spacing
- **Section Padding**: `100px 0` (desktop), `50px 0` (mobile)
- **Card Padding**: `32px` - `36px`
- **Grid Gaps**: `g-4` (24px), `g-3` (16px)
- **Container Max Width**: Bootstrap default (1320px)

### Border Radius
- **Cards**: `16px` - `24px`
- **Buttons**: `12px`
- **Icons/Badges**: `14px` (square), `100px` (pill)
- **Inputs**: `12px`

### Shadows
- **Card Hover**: `0 20px 40px rgba(0,0,0,0.3)` (dark) / `0 8px 24px rgba(0,0,0,0.08)` (light)
- **Glow Effects**: `box-shadow: 0 0 20px rgba(209,255,76,0.3)` (dark accent)

---

## SaaS Platform Landing Page Sections

### 1. Hero Section
- **Height**: `92vh` min
- **Layout**: 2-column (text left, dashboard preview right)
- **Elements**:
  - Badge pill with live indicator dot (animated pulse)
  - H1 with gradient accent text (`clamp(2.5rem, 6vw, 4.5rem)`)
  - Subtitle paragraph (max-width 520px)
  - Two CTA buttons: primary (`btn-qleviq`) + ghost (`btn-ghost`)
  - Trust badge ("No credit card required")
  - Right side: mock dashboard card with stats and activity feed
- **Background**: Radial gradient glows (top-left lime, bottom-right blue)
- **Animations**: `fadeUp` with staggered delays

### 2. Stats Bar
- **Layout**: 4-column row, centered
- **Elements**: Large numbers (`2rem`, weight 800, accent color with text-shadow)
- **Borders**: Top and bottom subtle borders

### 3. Features Section
- **Layout**: 3-column grid of cards
- **Card Structure**:
  - Icon container (52x52px, accent bg + border)
  - H4 title
  - Description paragraph
- **Hover**: Lift (`translateY(-4px)`), top gradient line reveal, shadow

### 4. How It Works
- **Layout**: 2-column (text left, steps right)
- **Steps**: Numbered circles (44px) with vertical connectors
- **4 Steps**: Register → Subdomain → Invite → Manage

### 5. Pricing Section
- **Layout**: 3-column cards
- **Tiers**: Starter (Free), Pro (featured), Enterprise (Custom)
- **Featured Card**: Gradient background, accent border, "Most Popular" badge
- **Features List**: Check icons + text, divider lines

### 6. CTA Section
- **Full-width card**: Gradient background, centered text
- **Elements**: Section label, H2, subtitle, two buttons
- **Background glow**: Centered radial gradient

---

## School Public Landing Page Sections

### 1. Custom Navbar
- **Style**: White bg, bottom border, sticky
- **Elements**: School logo/initial + name, nav links (Home, About, Contact), Sign In/Dashboard button
- **Mobile**: Hamburger toggle with collapse menu

### 2. Hero Section
- **Background**: Gradient `#1a365d` → `#2b6cb0`
- **Layout**: 2-column (text left, portal cards right)
- **Left**: School name H1, tagline, Sign In button
- **Right**: 2x2 grid of portal cards (Students, Teachers, Parents, Admin)

### 3. About Us Section
- **Background**: White
- **Layout**: 2-column (content left, values right)
- **Left**: Badge, H2, school address/description, 3 stat boxes
- **Right**: 2x2 grid of value cards (Mission, Vision, Values, Achievements)

### 4. Contact Section
- **Background**: `#f8fafc`
- **Layout**: 2-column (info left, form right)
- **Left**: Contact cards (address, email, phone, hours) with icons
- **Right**: Contact form with styled inputs

### 5. Footer
- **Background**: `#1a365d` (navy)
- **Elements**: School logo + name, nav links, copyright

---

## Component Patterns

### Buttons
```css
/* Primary (SaaS) */
.btn-qleviq {
  background: #d1ff4c;
  color: #0b0c10;
  font-weight: 700;
  border-radius: 12px;
  padding: 14px 32px;
  border: none;
}

/* Ghost (SaaS) */
.btn-ghost {
  background: transparent;
  border: 2px solid rgba(255,255,255,0.15);
  color: #fff;
  border-radius: 12px;
  padding: 14px 32px;
  font-weight: 700;
}

/* Sign In (School) */
.btn-signin {
  background: white;
  color: #1a365d;
  font-weight: 700;
  padding: 14px 36px;
  border-radius: 12px;
  border: none;
}

/* Send (School) */
.btn-send {
  background: #1a365d;
  color: white;
  font-weight: 700;
  padding: 14px 36px;
  border-radius: 12px;
  border: none;
  width: 100%;
}
```

### Cards
- Always include: background, border, border-radius, padding, transition
- Hover: `translateY(-3px)` or `translateY(-4px)` + shadow
- Featured variant: accent border + gradient background

### Icons
- Container: 44px-52px square, accent bg, accent border, rounded corners
- Icon size: `1.2rem` - `1.4rem`
- Bootstrap Icons classes: `bi bi-*`

---

## Animation Patterns

### Fade Up (on load)
```css
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(30px); }
  to   { opacity: 1; transform: translateY(0); }
}
.fade-up { animation: fadeUp 0.7s ease both; }
.delay-1 { animation-delay: 0.1s; }
.delay-2 { animation-delay: 0.2s; }
.delay-3 { animation-delay: 0.3s; }
.delay-4 { animation-delay: 0.4s; }
```

### Pulse Glow (live indicator)
```css
@keyframes pulse-glow {
  0%, 100% { box-shadow: 0 0 0 0 rgba(209,255,76,0.3); }
  50% { box-shadow: 0 0 0 8px rgba(209,255,76,0); }
}
.pulse { animation: pulse-glow 2.5s infinite; }
```

### Hover Transitions
- Cards: `transition: all 0.3s ease`
- Buttons: `transition: all 0.3s`
- Links: `transition: all 0.2s`

---

## Responsive Breakpoints

| Breakpoint | Behavior |
|------------|----------|
| `≥ 992px` (lg) | 2-column layouts, 3-column grids |
| `≥ 768px` (md) | 2-column grids, nav links visible |
| `< 768px` | Single column, hamburger nav, reduced padding |
| `< 576px` (sm) | Full-width cards, stacked buttons |

---

## Template Structure Rules

1. **Always extend base.html**: `{% extends "base.html" %}`
2. **Load static**: `{% load static %}`
3. **Override navbar for subdomain**: `{% block navbar %}{% endblock %}` (school page replaces it)
4. **Override footer for subdomain**: `{% block footer %}{% endblock %}` (school page replaces it)
5. **Inline CSS in `{% block extra_css %}`**: Keep styles scoped to the template
6. **Use Django context variables**: `{{ school.name }}`, `{{ school.address }}`, etc.

---

## Adding a New Section

Follow this pattern:
```html
<!-- ═══ SECTION NAME ═══ -->
<section style="padding: 100px 0;">
  <div class="container">
    <div class="text-center mb-5">
      <div class="section-label">Label</div>
      <h2 class="section-title">Section Title</h2>
      <p class="mt-3" style="color:#a9a9a9;">Subtitle text.</p>
    </div>
    <!-- Section content here -->
  </div>
</section>
```

---

## Key Files Reference

| File | Purpose |
|------|---------|
| `templates/base.html` | Base layout, navbar, footer, CDN links |
| `templates/core/index.html` | SaaS platform landing page |
| `templates/core/index_subdomain.html` | Individual school public page |
| `core/views.py` | IndexView handles routing based on subdomain |
| `core/urls.py` | URL configuration |
| `static/css/style.css` | Global custom styles |

---

## Checklist Before Publishing

- [ ] All sections have proper padding (100px desktop, 50px mobile)
- [ ] Cards have hover effects (lift + shadow)
- [ ] Buttons have consistent border-radius (12px)
- [ ] Typography uses Plus Jakarta Sans
- [ ] Mobile responsive (test at 375px, 768px, 1024px)
- [ ] Django template variables render correctly
- [ ] No hardcoded school data in subdomain template
- [ ] Accessibility: sufficient color contrast, semantic HTML
