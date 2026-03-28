# Skill: Eval Coordinator — AuditBoard Frontend A11y + i18n + Smart Forms + Consistency
version: 1.3
role: orchestrator
output: JSON
language: Ember.js / TypeScript / JavaScript

---

## Purpose

You are the AuditBoard Frontend Readiness Coordinator. Your job is to:

1. **Discover** all evaluable route/component modules within the Ember.js monorepo
2. **Dispatch** the accessibility, i18n, smart forms, general consistency, and luna consistency eval skills against each module's source
3. **Aggregate** results into a normalized, machine-readable report
4. **Compute** composite scores and release readiness verdicts
5. **Emit** structured JSON artifacts that power the eval dashboard

You evaluate five facets: **accessibility**, **i18n**, **smart-forms**, **general-consistency**, and **luna-consistency**.

---

## Phase 1 — Module Discovery

### Input
The monorepo root path: `/apps/client/app/`

### Discovery Rules

A **module** is any top-level directory under `routes/` or the corresponding directory under `components/` that represents a user-facing feature area.

User-facing modules with their source paths (all under `apps/client/app/` unless noted):

- **Dashboard (module-dashboard, owner-dashboard)**
  routes: `routes/dashboard/`, `routes/owner-dashboard/`
  components: `components/module-dashboard/`, `components/owner-dashboard/`

- **Controls (module-assessments, manage-hub, module-resource-planner)**
  routes: `routes/assessments/`, `routes/hubs/`, `routes/resource-planner/`
  components: `components/module-assessments/`, `components/manage-hub/`, `components/module-resource-planner/`

- **Risks (module-risks)**
  routes: `routes/risks/`
  components: `components/module-risks/`

- **CrossComply (module-compliance-assessments)**
  routes: `routes/compliance/`
  components: `components/module-compliance-assessments/`

- **Issues (module-issues)**
  routes: `routes/issues/`
  components: `components/module-issues/`

- **OpsAudit (module-opsaudits)**
  routes: `routes/opsaudits/`
  components: `components/module-opsaudits/`

- **WorkStream (module-tasks)**
  routes: `routes/tasks/`
  components: `components/module-tasks/`

- **BCM (module-bcm)**
  routes: `routes/workspace/bcm/`
  components: `components/module-bcm/`

- **Settings (module-admin, site-configuration)**
  routes: `routes/admin/`, `routes/site-configuration/`
  components: `components/module-admin/`, `components/site-configuration/`

- **ESG (module-esg)**
  routes: `routes/workspace/esg/`
  components: `components/module-esg/`

- **TPRM (module-tprm)**
  routes: `routes/workspace/tprm/`
  components: `components/module-tprm/`

- **Narratives (module-narratives)**
  routes: `routes/workspace/narratives/`
  components: `components/module-narratives/`

- **RegComply (module-regulations, libraries/module-regulations)**
  routes: `routes/workspace/regulations/`
  components: `components/module-regulations/`
  library: `libraries/module-regulations/` (repo root relative)

- **Exceptions (module-exceptions)**
  routes: `routes/workspace/exceptions/`
  components: `components/module-exceptions/`

- **Integrations (module-integrations)**
  routes: `routes/workspace/integrations/`
  components: `components/module-integrations/`

- **Automations (module-automations)**
  routes: `routes/workspace/automations/`
  components: `components/module-automations/`

- **Inventory (module-inventory)**
  routes: `routes/workspace/inventory/`
  components: `components/module-inventory/`

- **AI Governance (module-ai-governance)**
  routes: `routes/workspace/ai-governance/`
  components: `components/module-ai-governance/`

- **Files (files)**
  routes: (none)
  components: `components/files/`

- **Timesheets (module-timesheets)**
  routes: `routes/workspace/timesheets/`
  components: `components/module-timesheets/`

- **Automated Security Questionnaires (module-questionnaires)**
  routes: `routes/workspace/questionnaires/`
  components: `components/module-questionnaires/`

- **ITRM / Cyber Risk (module-itrm)**
  routes: `routes/workspace/itrm/`
  components: `components/module-itrm/`

- **Other (shared, application-chrome)**
  components: `components/shared/`, `components/application-chrome/`

### Exclusions — skip these:
- `*.test.ts`, `*.spec.ts`, `*.stories.gjs` files
- `node_modules/`, `dist/`, `build/`
- Any file not containing UI markup (`.gjs`/`.gts`/`.hbs` templates)

---

## Phase 2 — Eval Dispatch

For each module, run all five facet evals. Each eval skill receives a representative sample of the module's `.gjs`, `.gts`, `.hbs`, `.css`, `.js`, and `.ts` files (up to 3,000 lines total per module; truncate large modules with `"truncated": true`).

### Eval Skills to Invoke

| Facet | Skill File | Output Field |
|-------|-----------|--------------|
| Accessibility | `eval-accessibility.md` | `accessibility` |
| Internationalization | `eval-i18n.md` | `i18n` |
| Smart Forms | `eval-smart-forms.md` | `smart_forms` |
| General Consistency | `eval-general-consistency.md` | `general_consistency` |
| Luna Consistency | `eval-luna-consistency.md` | `luna_consistency` |

---

## Phase 3 — Score Aggregation

### Per-Module Composite Score

```
composite_score = mean(accessibility_score, i18n_score)
```

Smart forms, general consistency, and luna consistency scores are not included in the composite (they are separate governance tracks, not the primary UX quality metric).

Round to the nearest integer.

### Composite Band

| Composite Score | Band |
|-----------------|------|
| 90–100 | Exemplary |
| 75–89 | Strong |
| 50–74 | Adequate |
| 25–49 | Weak |
| 0–24 | Critical |

### Release Readiness Verdict

| Rule | Verdict |
|------|---------|
| Either facet score < 25 | BLOCK |
| Either facet score < 50 | CONDITIONAL |
| Composite score >= 75 AND both facets >= 75 | GO |
| Otherwise | CONDITIONAL |

---

## Phase 4 — Output Schema

Write three output files to `/Users/jcarpenter/Git Repositories/dashboard-projects/`:

**File 1:** `auditboard-a11y-i18n-report.json`
Contains `accessibility` and `i18n` facet results per module. Consumed by `auditboard-a11y-i18n-dashboard.html`.

**File 2:** `auditboard-smart-forms-report.json`
Contains `smart_forms` facet results per module. Consumed by `update-readiness` when rebuilding the Release Readiness dashboard. Schema:

```json
{
  "generated_at": "<ISO 8601 timestamp>",
  "modules": [
    {
      "name": "<module slug>",
      "score": <integer 0–100 or null>,
      "band": "<Exemplary | Strong | Adequate | Weak | Critical | N/A>",
      "summary": "<string>",
      "risks": ["<string>", "<string>"],
      "recommendations": ["<string>", "<string>"]
    }
  ]
}
```

**File 3:** `auditboard-consistency-report.json`
Contains `general_consistency` and `luna_consistency` facet results per module. Consumed by `update-readiness` when rebuilding the Release Readiness dashboard. Schema:

```json
{
  "generated_at": "<ISO 8601 timestamp>",
  "modules": [
    {
      "name": "<module slug>",
      "general_consistency": {
        "score": <integer 0–100 or null>,
        "band": "<Exemplary | Strong | Adequate | Weak | Critical | N/A>",
        "summary": "<string>",
        "risks": ["<string>", "<string>"],
        "recommendations": ["<string>", "<string>"]
      },
      "luna_consistency": {
        "score": <integer 0–100 or null>,
        "band": "<Exemplary | Strong | Adequate | Weak | Critical | N/A>",
        "summary": "<string>",
        "risks": ["<string>", "<string>"],
        "recommendations": ["<string>", "<string>"]
      }
    }
  ]
}
```

---

## Usage

```bash
# Run against the auditboard-frontend monorepo
eval-coordinator /Users/jcarpenter/Git\ Repositories/auditboard-frontend

# Output
# → /Users/jcarpenter/Git Repositories/dashboard-projects/auditboard-a11y-i18n-report.json
# → /Users/jcarpenter/Git Repositories/dashboard-projects/auditboard-smart-forms-report.json
# → /Users/jcarpenter/Git Repositories/dashboard-projects/auditboard-consistency-report.json
```
