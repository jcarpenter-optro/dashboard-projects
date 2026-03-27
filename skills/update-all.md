---
description: Refresh and republish all four project dashboards on Jeff Carpenter's GitHub Pages site. Orchestrates update-ember-react, update-tokens, and the a11y + i18n + smart-forms + consistency eval-coordinator in parallel, then update-readiness sequentially last.
---

# UPDATE_ALL Skill

Use this skill when asked to "update all dashboards", "refresh everything", or "republish all reports."

---

## What this skill does

Runs the first three dashboard update workflows in parallel, waits for all three to complete, then runs the Release Readiness dashboard last so it can read from their fresh output.

| Dashboard | Skill | Live URL |
|---|---|---|
| Release Readiness | `update-readiness.md` | `.../release-readiness.html` |
| Luna Design System: Ember vs React | `update-ember-react.md` | `.../luna-components.html` |
| Luna Token Adoption: Module Scores | `update-tokens.md` | `.../luna-module-scores.html` |
| AuditBoard: A11y + i18n Audit | `eval-coordinator.md` | `.../auditboard-a11y-i18n.html` |

The eval-coordinator (Agent 3) evaluates five facets: **a11y**, **i18n**, **smart-forms**, **general-consistency**, and **luna-consistency**. It writes three output files: `auditboard-a11y-i18n-report.json`, `auditboard-smart-forms-report.json`, and `auditboard-consistency-report.json`. update-readiness reads all four data sources.

Base URL: https://jcarpenter-optro.github.io/dashboard-projects/

---

## Prerequisites

Pull the latest source before launching any updates:

```bash
cd "/Users/jcarpenter/Git Repositories/auditboard-frontend"
git pull origin develop
```

Also ensure `/Users/jcarpenter/Git Repositories/dashboard-projects/` exists (clone if not):

```bash
git clone https://github.com/jcarpenter-optro/dashboard-projects.git "/Users/jcarpenter/Git Repositories/dashboard-projects"
```

---

## Phase 1: launch the first three in parallel

Use the Agent tool to spawn three subagents simultaneously. Do not wait for one to finish before starting the next.

**Agent 1 — Ember vs React parity:**
> Follow the update-ember-react skill: run `/Users/jcarpenter/Git Repositories/dashboard-projects/scripts/generate-luna-report.py`, check the summary, commit and push luna-components.html and all component sub-pages to `/Users/jcarpenter/Git Repositories/dashboard-projects/`.

**Agent 2 — Luna token scores:**
> Follow the update-tokens skill: run `/Users/jcarpenter/Git Repositories/dashboard-projects/scripts/luna-module-audit.py --out /Users/jcarpenter/Git Repositories/dashboard-projects/luna-module-scores.html` from the auditboard-frontend repo root, then commit and push luna-module-scores.html and luna-module-scores.json to `/Users/jcarpenter/Git Repositories/dashboard-projects/`.

**Agent 3 — A11y + i18n + Smart Forms + Consistency audit:**
> Follow the eval-coordinator skill (v1.3): evaluate the a11y, i18n, smart-forms, general-consistency, AND luna-consistency facets for each module. Write `auditboard-a11y-i18n-report.json`, `auditboard-smart-forms-report.json`, and `auditboard-consistency-report.json` to `/Users/jcarpenter/Git Repositories/dashboard-projects/`. Generate `auditboard-a11y-i18n.html` using the optro-dashboard template, then commit and push all four files to `/Users/jcarpenter/Git Repositories/dashboard-projects/`.

---

## Notes on Agent 3

The A11y + i18n + Smart Forms + Consistency audit is significantly slower than the other two — it reads source files and generates AI-driven analysis per module across five facets. Agents 1 and 2 will finish first. Wait for all three before proceeding.

---

## Phase 2: update Release Readiness (after all three are done)

Only after Agents 1, 2, and 3 have all committed their output, follow the `update-readiness` skill to merge fresh data from `luna-module-scores.json`, `auditboard-a11y-i18n.html`, and `auditboard-smart-forms-report.json` into `release-readiness.html` and push.

This step must run last. Running it before the others would pull stale data from their previous run.

---

## After all four complete

Report a summary table showing which dashboards were updated, any changes in key stats (e.g. component counts, module scores), and the base URL. Flag any agent that failed or produced unexpected output.
