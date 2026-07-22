# Subdomain School Landing Page — Section-by-Section Instructions

> **File**: `templates/core/index_subdomain.html`
> **Purpose**: Public-facing website for an individual school (accessed via subdomain)
> **Theme**: Light (`#f8fafc` background), Navy Blue (`#1a365d`) + Blue (`#2b6cb0`) accents
> **Template**: `templates/core/index.html`

---

## Section 1: Navbar (`.school-navbar`)

**Line Range**: 264–303

### Purpose
Custom school-branded navigation bar that replaces the base template navbar.

### Layout
- **Position**: Sticky at top (`z-index: 1020`)
- **Background**: White with bottom border (`#e2e8f0`)
- **Padding**: `16px 0`
- **3 Zones**: Brand (left), Nav Links (center), Auth Button (right)

### Elements

| Element | Class/Tag | Description |
|---------|-----------|-------------|
| Brand | `.school-nav-brand` | School logo image (40x40px, rounded 10px) OR fallback div with first letter. Next to it: school name in H6, weight 800, color `#1a365d` |
| Nav Links | `.school-nav-link` | "Home", "About Us", "Contact Us" — smooth scroll anchors. Hover: blue bg `#ebf8ff`, text `#1a365d`. Active state same as hover |
| Auth Button | `.btn-signin` | Conditional — "Sign In" if not authenticated, "Dashboard" if authenticated |
| Mobile Toggle | `button` | Hidden on `≥md`. Toggles `#schoolMenu` collapse with hamburger icon |
| Mobile Menu | `#schoolMenu` | Collapse menu with stacked nav links, visible only on `<md` |

### CSS Classes
```
.school-navbar          → white bg, sticky, bottom border
.school-nav-link         → gray text, rounded pills, hover blue bg
.school-nav-brand        → flex row, logo + name
.btn-signin              → white bg, navy text, rounded 12px
```

### Dynamic Data
- `{{ school.logo.url }}` — school logo image (conditional)
- `{{ school.name }}` — school name displayed in brand
- `{{ school.name|slice:":1" }}` — first letter for fallback avatar
- `{% if user.is_authenticated %}` — toggles Sign In vs Dashboard button

### Rules
1. Must override `{% block navbar %}{% endblock %}` to hide base navbar
2. Logo: if exists, show `<img>`, else show div with first letter
3. Nav links use anchor scroll (`#home`, `#about`, `#contact`)
4. Mobile menu collapses via Bootstrap `data-bs-toggle="collapse"`

---

## Section 2: Hero / Home (`.hero-section`)

**Line Range**: 306–358
**ID**: `#home`

### Purpose
Main hero banner with school welcome message and portal quick-access cards.

### Layout
- **2-column row** (`col-lg-7` left, `col-lg-5` right)
- **Background**: Linear gradient `#1a365d` → `#2b6cb0`
- **Pseudo-element**: Radial glow at top-right (`600x600px`, `rgba(255,255,255,0.06)`)
- **Padding**: `py-5` on container

### Left Column (Text)

| Element | Style |
|---------|-------|
| H1 | "Welcome to<br>{{ school.name }}" — weight 800, white, `clamp(2.2rem, 5vw, 3.5rem)` |
| Paragraph | Tagline — `rgba(255,255,255,0.85)`, 1.1rem, max-width 540px, line-height 1.7 |
| Button | `.btn-signin` — white bg, navy text — "Sign In to Portal" or "Go to Dashboard" |

### Right Column (Portal Cards)
**Grid**: 2x2 (`col-6` each), `g-3` gap

| Card | Icon | Title | Description |
|------|------|-------|-------------|
| Students | `bi-person-fill` | Students | Grades, attendance & assignments |
| Teachers | `bi-journal-text` | Teachers | Classes, marks & reports |
| Parents | `bi-people-fill` | Parents | Track progress & connect |
| Admin | `bi-shield-lock-fill` | Admin | Manage everything |

### Portal Card Structure (`.portal-card`)
```
┌─────────────────────────┐
│ [icon container 52x52]  │
│ Title (h5, 0.95rem)     │
│ Description (p, 0.82rem)│
└─────────────────────────┘
```
- **Bg**: White, border `#e2e8f0`, radius 16px, padding 32px
- **Hover**: Border `#4299e1`, shadow `0 8px 24px rgba(0,0,0,0.08)`, lift `translateY(-3px)`
- **Icon Container**: `#ebf8ff` bg, radius 14px, icon color `#2b6cb0`, 1.4rem

### CSS Classes
```
.hero-section            → gradient bg, white text, relative overflow
.hero-section h1         → large heading, white, responsive size
.hero-section p          → subtitle, semi-transparent white
.btn-signin              → white button, navy text
.portal-card             → white card, hover effects
.portal-icon             → blue-tinted icon container
```

### Dynamic Data
- `{{ school.name }}` — in hero heading

### Rules
1. Background gradient is always navy → blue (school colors can be customized later)
2. Portal cards are decorative only (not clickable links currently)
3. Button text changes based on authentication state
4. Pseudo-element glow adds depth — do not remove

---

## Section 3: About Us (`.about-section`)

**Line Range**: 361–424
**ID**: `#about`

### Purpose
School information, statistics, and core values/mission/vision.

### Layout
- **Background**: White (`.about-section { background: white; }`)
- **Padding**: `.section-padding` → `80px 0` (50px on mobile)
- **2-column row** (`col-lg-6` each), `g-5` gap, vertically aligned

### Left Column (School Info + Stats)

| Element | Details |
|---------|---------|
| Badge | `.about-badge` — `#ebf8ff` bg, `#2b6cb0` text, pill shape, uppercase, weight 700 |
| H2 | "Building the Future of Education" — weight 800, `#1a202c`, `clamp(1.8rem, 3vw, 2.4rem)` |
| Paragraph | `{{ school.address\|linebreaks }}` — renders school address/description with line breaks |
| Stat Boxes | 3-column row (`col-4` each), `g-3` gap |

### Stat Box Structure (`.stat-box`)
```
┌──────────────┐
│   500+       │  ← .number (2rem, weight 800, #2b6cb0)
│   Students   │  ← .label (0.85rem, #718096)
└──────────────┘
```
- **Bg**: `#f8fafc`, border `#e2e8f0`, radius 16px, padding 28px, centered text

**Current Stats**:
| Number | Label |
|--------|-------|
| 500+ | Students |
| 40+ | Teachers |
| 20+ | Years |

### Right Column (Values Grid)
**Grid**: 2x2 (`col-md-6` each), `g-3` gap, `h-100` for equal height

| Card | Icon | Title | Description |
|------|------|-------|-------------|
| Mission | `bi-bullseye` | Our Mission | Provide world-class education... |
| Vision | `bi-eye` | Our Vision | Be a leading institution... |
| Values | `bi-heart` | Our Values | Integrity, excellence... |
| Achievements | `bi-trophy` | Achievements | Award-winning programs... |

### Value Card Structure (`.value-card`)
```
┌────────────────────────┐
│ [icon 44x44]           │
│ Title (h6, weight 700) │
│ Description (p, 0.88rem)│
└────────────────────────┘
```
- **Bg**: `#f8fafc`, border `#e2e8f0`, radius 14px, padding 24px
- **Icon Container**: `#ebf8ff` bg, radius 12px, icon color `#2b6cb0`, 1.2rem

### CSS Classes
```
.about-section           → white background
.about-badge             → blue pill badge
.stat-box                → light bg stat counter
.stat-box .number        → large blue number
.stat-box .label         → small gray label
.value-card              → light bg value card
.value-card .icon        → blue icon container
```

### Dynamic Data
- `{{ school.address|linebreaks }}` — school description with line break formatting
- Stats are currently hardcoded (500+, 40+, 20+) — should pull from database in future

### Rules
1. Badge text is static ("About Us") — can be changed per section
2. Paragraph uses `|linebreaks` filter to convert newlines to `<p>` tags
3. Values (Mission/Vision/Values/Achievements) are hardcoded — consider making them editable fields
4. Stat numbers are hardcoded — consider pulling from actual Teacher/Student counts

---

## Section 4: Contact Us (`.contact-section`)

**Line Range**: 427–500
**ID**: `#contact`

### Purpose
School contact information and a message form for visitors.

### Layout
- **Background**: `#f8fafc` (`.contact-section { background: #f8fafc; }`)
- **Padding**: `.section-padding` → `80px 0`
- **Section Header**: Centered — badge, H2, subtitle paragraph
- **2-column row** (`col-lg-5` left, `col-lg-7` right), `g-4` gap

### Section Header

| Element | Style |
|---------|-------|
| Badge | `.about-badge` — "Contact Us" |
| H2 | "Get in Touch" — inline style, weight 800, `#1a202c`, `clamp(1.8rem,3vw,2.4rem)` |
| Paragraph | Subtitle — `#718096`, max-width 500px, centered |

### Left Column: Contact Info Card (`.contact-card`)
```
┌─────────────────────────────────┐
│ Our Information (h4)            │
│ ─────────────────────────────── │
│ [icon] Address                  │
│        {{ school.address }}     │
│ [icon] Email                    │
│        {{ school.contact_email }}│
│ [icon] Phone                    │
│        {{ school.contact_phone }}│
│ [icon] Office Hours             │
│        Mon-Fri, 8AM-4PM        │
└─────────────────────────────────┘
```

**Card Style**: White bg, border `#e2e8f0`, radius 16px, padding 36px

### Contact Item Structure (`.contact-item`)
- Flex row, gap 16px, padding `18px 0`
- Bottom border `#f0f0f0` (last item has no border)

| Item | Icon | Dynamic Data |
|------|------|--------------|
| Address | `bi-geo-alt-fill` | `{{ school.address }}` |
| Email | `bi-envelope-fill` | `{{ school.contact_email }}` |
| Phone | `bi-telephone-fill` | `{{ school.contact_phone }}` |
| Office Hours | `bi-clock-fill` | Hardcoded: "Monday – Friday, 8:00 AM – 4:00 PM" |

### Right Column: Contact Form (`.contact-form-card`)
```
┌──────────────────────────────────┐
│ Send a Message (h4)              │
│ ──────────────────────────────── │
│ [Full Name    ] [Email          ]│
│ [Subject                       ] │
│ [Message                       ] │
│ [        Send Message           ]│
└──────────────────────────────────┘
```

### Form Fields

| Field | Type | Placeholder | Layout |
|-------|------|-------------|--------|
| Full Name | text | "Your name" | `col-md-6` |
| Email | email | "Your email" | `col-md-6` |
| Subject | text | "What is this about?" | `col-12` |
| Message | textarea | "Write your message..." | `col-12`, 5 rows |
| Submit | button | "Send Message" | `col-12`, full-width |

### Form Input Styling
- **Bg**: `#f8fafc`, border `#e2e8f0`, radius 12px, padding `14px 18px`
- **Focus**: Border `#2b6cb0`, shadow `0 0 0 0.2rem rgba(43,108,176,0.15)`

### Submit Button (`.btn-send`)
- **Bg**: `#1a365d`, white text, weight 700, radius 12px, full-width
- **Hover**: Bg `#2b6cb0`, lift `translateY(-2px)`

### CSS Classes
```
.contact-section         → light gray background
.contact-card            → white info card
.contact-item            → row with icon + text, bottom border
.contact-icon            → blue icon container (48x48px)
.contact-form-card       → white form card
.btn-send                → navy submit button, full-width
```

### Dynamic Data
- `{{ school.address }}` — address in contact info
- `{{ school.contact_email }}` — email in contact info
- `{{ school.contact_phone }}` — phone in contact info

### Rules
1. Form currently has no action/method — needs backend endpoint
2. Office hours are hardcoded — consider adding to School model
3. Contact card items separated by thin borders, last item border removed
4. Form inputs use `!important` on some styles to override Bootstrap defaults
5. Add CSRF token and form submission handling before going live

---

## Section 5: Footer (`.school-footer`)

**Line Range**: 503–518

### Purpose
School-branded footer with logo, navigation links, and copyright.

### Layout
- **Background**: `#1a365d` (navy)
- **Text Color**: `rgba(255,255,255,0.7)`
- **Padding**: `40px 0`
- **Alignment**: Centered, 3 rows

### Elements

| Row | Content |
|-----|---------|
| 1 | School logo (32x32px, inverted filter for dark bg) + school name (white, weight 800) |
| 2 | Nav links: "Home", "About", "Contact" — `rgba(255,255,255,0.6)`, hover white |
| 3 | Copyright: "© 2026 {{ school.name }}. All rights reserved." — 0.82rem |

### Logo Handling
```html
{% if school.logo %}
  <img src="{{ school.logo.url }}" alt="{{ school.name }}"
       style="width:32px;height:32px;border-radius:8px;object-fit:cover;filter:brightness(0) invert(1);">
{% endif %}
```
- Logo has `filter: brightness(0) invert(1)` to convert to white for dark background
- No fallback letter shown in footer (only if logo exists)

### CSS Classes
```
.school-footer           → navy bg, centered, light text
.school-footer a         → semi-transparent white, hover full white
```

### Dynamic Data
- `{{ school.logo.url }}` — logo image (conditional)
- `{{ school.name }}` — school name in brand + copyright

### Rules
1. Must override `{% block footer %}{% endblock %}` to hide base template footer
2. Logo uses CSS filter to appear white on navy background
3. Copyright year is hardcoded as 2026
4. Nav links are anchor scrolls (same as navbar)

---

## Section Summary Table

| # | Section | ID | Background | Key Classes | Column Layout |
|---|---------|----|------------|-------------|---------------|
| 1 | Navbar | — | White `#ffffff` | `.school-navbar` | 3-zone flex |
| 2 | Hero/Home | `#home` | Gradient `#1a365d`→`#2b6cb0` | `.hero-section` | 7/5 split |
| 3 | About Us | `#about` | White `#ffffff` | `.about-section` | 6/6 split |
| 4 | Contact Us | `#contact` | Light `#f8fafc` | `.contact-section` | 5/7 split |
| 5 | Footer | — | Navy `#1a365d` | `.school-footer` | Centered |

---

## Color Reference

| Token | Value | Usage |
|-------|-------|-------|
| Primary Navy | `#1a365d` | Headings, buttons, footer bg, brand |
| Primary Blue | `#2b6cb0` | Icons, links, stat numbers, hover states |
| Light Blue | `#4299e1` | Card hover borders |
| Icon Bg | `#ebf8ff` | Icon containers, badge bg |
| Page Bg | `#f8fafc` | Body, contact section, stat/value card bg |
| Card Bg | `#ffffff` | Cards, navbar, form inputs |
| Card Border | `#e2e8f0` | Card borders, input borders |
| Text Primary | `#1a202c` | Headings, form labels |
| Text Secondary | `#718096` | Body text, descriptions |
| Text Muted | `#4a5568` | Nav link default state |
| Divider | `#f0f0f0` | Contact item separators |

---

## Adding a New Section

Follow this pattern:

```html
<!-- ═══ SECTION NAME ═══ -->
<section id="section-id" class="section-name section-padding">
  <div class="container">
    <div class="text-center mb-5">
      <div class="about-badge">Label</div>
      <h2 style="font-size:clamp(1.8rem,3vw,2.4rem);font-weight:800;color:#1a202c;">Section Title</h2>
      <p class="mt-2" style="color:#718096;max-width:500px;margin:12px auto 0;">Subtitle text.</p>
    </div>
    <!-- Section content here -->
  </div>
</section>
```

And add corresponding CSS in `{% block extra_css %}`:
```css
.section-name { background: #f8fafc; }
/* or */
.section-name { background: white; }
```

---

## Responsive Behavior

| Breakpoint | Changes |
|------------|---------|
| `≥992px` (lg) | 2-column layouts active (7/5, 6/6, 5/7) |
| `≥768px` (md) | Nav links visible, mobile menu hidden, desktop nav shown |
| `<768px` | `.section-padding` → `50px 0`, all columns stack to full width |
| `<576px` (sm) | Stat boxes stack (col-4 → col-12), value cards stack |

---

## File References

| File | Purpose |
|------|---------|
| `templates/core/index_subdomain.html` | This landing page |
| `templates/base.html` | Base template (navbar/footer overridden) |
| `core/views.py:11-34` | `IndexView` — routes to this template on subdomain |
| `core/models.py` | `School` model — provides `name`, `address`, `contact_email`, `contact_phone`, `logo` |
| `static/css/style.css` | Global styles (minimal override needed) |
