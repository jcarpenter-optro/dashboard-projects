---
description: Publish a new HTML dashboard to Jeff Carpenter's GitHub Pages project site, following the monday.com Vibe-inspired style guide.
---

# Publish Dashboard Skill

Use this skill when asked to create and publish a new dashboard or report using the **Vibe visual style** to Jeff Carpenter's project site.

## Site context

- **Live URL:** https://jcarpenter-optro.github.io/dashboard-projects/
- **Repo:** https://github.com/jcarpenter-optro/dashboard-projects.git
- **Local working copy:** /Users/jcarpenter/Git Repositories/dashboard-projects/

If /Users/jcarpenter/Git Repositories/dashboard-projects/ does not exist locally, clone it first:
```bash
git clone https://github.com/jcarpenter-optro/dashboard-projects.git "/Users/jcarpenter/Git Repositories/dashboard-projects"
```

## Steps to publish a new dashboard

### 1. Build the dashboard HTML

- Self-contained single HTML file, no external dependencies (all CSS and JS inline)
- Name it descriptively, e.g. `my-report.html`
- Place it at the root of /Users/jcarpenter/Git Repositories/dashboard-projects/
- Sub-pages go in a matching subdirectory, e.g. `my-report/page.html`
- Do NOT add a password gate: the gate lives only on index.html
- Do NOT use em dashes (—) or separator dashes (e.g. "Title - Subtitle"). Use a colon and a space instead (e.g. "Title: Subtitle")
- Derive all summary numbers from the same data source used to generate the content: never hardcode stats by hand

Apply the Vibe Style Guide below exactly. Do not invent new patterns.

### 2. Add a project card to index.html

Open /Users/jcarpenter/Git Repositories/dashboard-projects/index.html and find:
```html
<!-- ADD NEW PROJECTS ABOVE THIS LINE -->
```

Insert above it:
```html
<a href="my-report.html" class="project-card">
  <div class="left">
    <div class="title">Your Report Title</div>
    <div style="margin-top:6px">
      <span class="tag">Tag 1</span>
      <span class="tag">Tag 2</span>
    </div>
    <div class="desc">One or two sentences describing what the report covers.</div>
  </div>
  <div class="arrow">→</div>
</a>
```

### 3. Deploy

```bash
cd "/Users/jcarpenter/Git Repositories/dashboard-projects"
git add -A
git commit -m "feat: add [report name] dashboard (Vibe)"
git push origin main
```

GitHub Pages deploys automatically within ~60 seconds.

---

## Vibe Style Guide

Use the Vibe design system tokens and components. Refer to the Vibe MCP server (`@vibe/mcp`) for current specs on colors, typography, spacing, and components.

Key conventions to follow:

- **Fonts:** Poppins for headings, Figtree for body, Roboto Mono for code. Load via Google Fonts.
- **Primary color:** `#0073ea` (cobalt). Background tint: `#f6f7fb`.
- **Page header:** white panel with `border-top: 3px solid #0073ea` as the brand stripe.
- **Panels:** white, `1px solid #c3c6d4` border, `8px` radius.
- **Spacing:** 4px grid (`--space-xs` through `--space-xxxxl`).
- **No em dashes or "Title - Subtitle" separators.** Use a colon and space instead.
- **Semantic color only.** Pair color with text for status indicators.

### Required `<head>` block

Every dashboard must include this `<head>` to load Poppins and Figtree:

```html
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Report Title</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&family=Figtree:wght@300;400;500;600&family=Roboto+Mono:wght@400&display=swap" rel="stylesheet">
  <style>
    /* paste full Vibe CSS here */
  </style>
</head>
```

### Page structure template

Every dashboard follows this skeleton:

```html
<body>
  <header class="page-header">
    <div class="page-header-inner">
      <div class="breadcrumb"><a href="index.html">Projects</a> / Report Title</div>
      <h1>Report Title</h1>
      <p class="text-subdued" style="margin-top:var(--space-xs)">Short description. Generated YYYY-MM-DD.</p>
    </div>
  </header>

  <main class="page-body">

    <div class="stat-row">
      <div class="stat-card">
        <div class="stat-card__label">Metric Name</div>
        <div class="stat-card__value">123</div>
        <div class="stat-card__description">Optional context</div>
      </div>
    </div>

    <div class="panel" style="padding:var(--space-l);">
      <div class="panel-title">Section Title</div>
      <!-- content -->
    </div>

  </main>
</body>
```

---

## Password

The projects index is password-protected. Password stored as SHA-256 hash only: never in plaintext. localStorage key: `luna_auth`. To change the password: generate a new SHA-256 hash and replace the `HASH` constant in index.html.
