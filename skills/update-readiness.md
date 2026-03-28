---
description: Refresh the Release Readiness dashboard by merging current data from luna-module-scores.json, auditboard-a11y-i18n.html, auditboard-smart-forms-report.json, and auditboard-consistency-report.json. Run this AFTER update-tokens and eval-coordinator have already committed their output.
---

# UPDATE_READINESS Skill

Use this skill when asked to refresh or republish the Release Readiness dashboard. This skill does **not** re-evaluate any code. It reads the already-updated output of the other dashboards and merges it.

---

## What this dashboard is

A combined view of A11y, i18n, Luna token adoption, Smart Forms governance, General Consistency, and Luna Consistency scores per module. Each score cell is clickable and opens a lightbox with facet-specific risks, recommendations, and a Claude Code prompt.

- **File:** `/Users/jcarpenter/Git Repositories/dashboard-projects/release-readiness.html`
- **Live URL:** https://jcarpenter-optro.github.io/dashboard-projects/release-readiness.html

---

## Prerequisites

The following files must already reflect the latest data before running this skill:

| Source | Updated by |
|---|---|
| `/Users/jcarpenter/Git Repositories/dashboard-projects/luna-module-scores.json` | `update-tokens` skill |
| `/Users/jcarpenter/Git Repositories/dashboard-projects/auditboard-a11y-i18n.html` | `update-a11y` skill |
| `/Users/jcarpenter/Git Repositories/dashboard-projects/auditboard-smart-forms-report.json` | `eval-coordinator` skill (optional) |
| `/Users/jcarpenter/Git Repositories/dashboard-projects/auditboard-consistency-report.json` | `eval-coordinator` skill (optional) |

If the tokens or a11y files are stale, run the corresponding skill first. The smart forms and consistency reports are optional: if a file does not exist, set the corresponding field to `null` for all modules.

---

## Steps

### Step 1: Read token data from luna-module-scores.json

```bash
cat /Users/jcarpenter/Git Repositories/dashboard-projects/luna-module-scores.json
```

For each module in the JSON, note: `name`, `score`, `violations`, `css_files`, `token_usages`, `by_cat`, `top_files`.

### Step 2a: Extract a11y and i18n data from auditboard-a11y-i18n.html

Read the `const MODULES = [...]` array from the `<script>` block in `/Users/jcarpenter/Git Repositories/dashboard-projects/auditboard-a11y-i18n.html`.

For each module, collect: `name`, `a11y`, `i18n`, `a11yRisks`, `a11yRecs`, `i18nRisks`, `i18nRecs`.

The 23 modules (matching both a11y and token sources):
Dashboard (module-dashboard, owner-dashboard), Controls (module-assessments, manage-hub, module-resource-planner), Risks (module-risks), CrossComply (module-compliance-assessments), Issues (module-issues), OpsAudit (module-opsaudits), WorkStream (module-tasks), BCM (module-bcm), Settings (module-admin, site-configuration), ESG (module-esg), TPRM (module-tprm), Narratives (module-narratives), RegComply (module-regulations, libraries/module-regulations), Exceptions (module-exceptions), Integrations (module-integrations), Automations (module-automations), Inventory (module-inventory), AI Governance (module-ai-governance), Files (files), Timesheets (module-timesheets), Automated Security Questionnaires (module-questionnaires), ITRM / Cyber Risk (module-itrm), Other (shared, application-chrome).

All 23 modules have both token and a11y data. Use `tokens: null` only if a module truly produced no CSS files.

### Step 2b: Extract smart forms data from auditboard-smart-forms-report.json

```bash
cat "/Users/jcarpenter/Git Repositories/dashboard-projects/auditboard-smart-forms-report.json"
```

If the file does not exist, set `smartForms: null` for all 13 modules and skip this step.

For each module entry in `modules[]`, collect: `name`, `score`, `risks`, `recommendations`.
Map to: `smartForms: { score: <n>, risks: [...], recs: [...] }` or `smartForms: null` if `score` is `null` (N/A modules).

### Step 2c: Extract consistency data from auditboard-consistency-report.json

```bash
cat "/Users/jcarpenter/Git Repositories/dashboard-projects/auditboard-consistency-report.json"
```

If the file does not exist, set `generalConsistency: null` and `lunaConsistency: null` for all 13 modules and skip this step.

For each module entry in `modules[]`, collect from `general_consistency` and `luna_consistency` objects: `score`, `risks`, `recommendations`.
Map to:
- `generalConsistency: { score: <n>, risks: [...], recs: [...] }` or `generalConsistency: null` if `score` is `null`
- `lunaConsistency: { score: <n>, risks: [...], recs: [...] }` or `lunaConsistency: null` if `score` is `null`

### Step 3: Rebuild the const MODULES array

Open `/Users/jcarpenter/Git Repositories/dashboard-projects/release-readiness.html`. Find the `const MODULES = [` block in the `<script>` section. Replace the entire array (from `const MODULES = [` through the closing `];`) with the freshly merged data, using this format per entry:

```js
{ name:'<name>', display:'<Display Name>',
  a11y:<score>, i18n:<score>,
  a11yRisks:['<risk1>','<risk2>'],
  a11yRecs:['<rec1>','<rec2>'],
  i18nRisks:['<risk1>'],
  i18nRecs:['<rec1>'],
  tokens:{ score:<n>, violations:<n>, css_files:<n>, token_usages:<n>,
    by_cat:{color:<n>,space:<n>,radius:<n>,typography:<n>},
    top_files:[{path:'<path>',violations:<n>}, ...]
  },
  smartForms:{ score:<n>, risks:['<risk1>'], recs:['<rec1>'] },
  generalConsistency:{ score:<n>, risks:['<risk1>'], recs:['<rec1>'] },
  lunaConsistency:{ score:<n>, risks:['<risk1>'], recs:['<rec1>'] }
},
```

For modules with no token data, use `tokens: null`.
For modules with no smart forms data (file absent or score is null/N/A), use `smartForms: null`.
For modules with no consistency data (file absent or score is null/N/A), use `generalConsistency: null` and/or `lunaConsistency: null`.

**Display name mapping** (name field to display label):
The `name` field in both JSON sources is now the full user-facing label including code modules in parens. Use it directly as `display` — no transformation needed. Examples:
- "Dashboard (module-dashboard, owner-dashboard)": Dashboard
- "Controls (module-assessments, manage-hub, module-resource-planner)": Controls
- "Risks (module-risks)": Risks
- "CrossComply (module-compliance-assessments)": CrossComply
- "Issues (module-issues)": Issues
- "OpsAudit (module-opsaudits)": OpsAudit
- "WorkStream (module-tasks)": WorkStream
- "BCM (module-bcm)": BCM
- "Settings (module-admin, site-configuration)": Settings
- "ESG (module-esg)": ESG
- "TPRM (module-tprm)": TPRM
- "Narratives (module-narratives)": Narratives
- "RegComply (module-regulations, libraries/module-regulations)": RegComply
- "Exceptions (module-exceptions)": Exceptions
- "Integrations (module-integrations)": Integrations
- "Automations (module-automations)": Automations
- "Inventory (module-inventory)": Inventory
- "AI Governance (module-ai-governance)": AI Governance
- "Files (files)": Files
- "Timesheets (module-timesheets)": Timesheets
- "Automated Security Questionnaires (module-questionnaires)": Automated Security Questionnaires
- "ITRM / Cyber Risk (module-itrm)": ITRM / Cyber Risk
- "Other (shared, application-chrome)": Other

Use the full string as `name` and the short label (before the first parenthesis) as `display`.

### Step 4: Update the date

In the `<header>` subtitle of `release-readiness.html`, update the "Generated YYYY-MM-DD" date to today.

### Step 5: Rules

- **Do not change style or layout.** Only update the `const MODULES = [...]` array and the date. The CSS, HTML structure, lightbox code, and all rendering functions are the canonical versions. Touch nothing else.
- No em dashes anywhere in string values. Use ": " or "; " instead.
- All stat card values (avg scores, modules at risk) are derived programmatically from the MODULES array. Never hardcode them.
- Always include the `smartForms`, `generalConsistency`, and `lunaConsistency` keys on every module entry (use `null` if not yet evaluated).

### Step 6: Commit and push

```bash
cd "/Users/jcarpenter/Git Repositories/dashboard-projects"
git add release-readiness.html
git commit -m "chore: refresh Release Readiness scores $(date +%Y-%m-%d)"
git push origin main
```

---

## Confirm

Report:
- How many modules changed any score vs. the prior run
- New avg A11y, avg i18n, avg tokens, avg Smart Forms (if data was available)
- Live URL: https://jcarpenter-optro.github.io/dashboard-projects/release-readiness.html
