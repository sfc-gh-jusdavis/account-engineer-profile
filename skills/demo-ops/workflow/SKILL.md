---
name: demo-ops:workflow
description: "Demo lifecycle phases and in-session validation gates that replace CI for non-repo demos. Use when planning, rehearsing, or validating a demo before presenting. Triggers: demo workflow, demo lifecycle, rehearse demo, demo gates, demo validation, demo phases, demo CI replacement, non-repo demo workflow, validate demo."
---

Lifecycle for demos. Replaces the GitHub PR/CI loop with in-session validation.

## The 5 phases

| Phase | Action | Exit criteria |
|---|---|---|
| **Scope** | Define audience, success criteria, runtime budget. Plan mode. | User has approved a written plan. |
| **Build** | Create DB/schema first, then objects. `system_todo_write` for >3 steps. | All objects created and individually validated. |
| **Rehearse** | Dry-run end-to-end. Time it. Capture screenshots. | End-to-end runs cleanly within runtime budget. |
| **Present** | Live execution with prepared narrative. | Audience saw the demo. |
| **Teardown** | Drop schema or preserve with tag. Archive. | Objects removed or explicitly preserved. |

## Phase 1: Scope

1. Confirm audience, takeaway, runtime budget.
2. Confirm Snowflake connection (default `${ACE_DEFAULT_CONN}`), DB.SCHEMA, cleanup intent.
3. Plan synthetic-data sources up front (see `demo-ops:synthetic-data`).
4. Switch to plan mode for non-trivial work. Wait for explicit user approval.

## Phase 2: Build

1. Create DB and schema first; tag with `DEMO_OWNER` and `DEMO_CREATED`.
2. `system_todo_write` for >3 steps.
3. Compile-check destructive SQL: `snowflake_sql_execute(only_compile=true, ...)`.
4. Checkpoint at milestones: `~/Documents/<demo>/checkpoints/<YYYY-MM-DD>/`.
5. Never use a read-only / shared SELECT warehouse for DDL/DML. Use a writable warehouse (e.g. `<your-warehouse>`).

## Phase 3: Rehearse — validation gates (replaces CI)

| Gate | How to verify |
|---|---|
| SQL compiles | Run statements; or `only_compile=true` |
| Cortex Agent answers verified queries | Walk every VQR; check returned SQL and response |
| Streamlit page loads | `streamlit run` locally OR deployed Streamlit-in-Snowflake URL |
| Notebook executes | `notebook_run_cell` mode=all; check no errors |
| Semantic view returns rows | `SELECT * FROM SEMANTIC_VIEW(... DIMENSIONS ... METRICS ...) LIMIT 10` |
| No real PII | grep for internal email domains and known real names |
| Teardown reads end-to-end | Read line by line; safe to paste |

If any gate fails -> back to Phase 2.

## Phase 4: Present

Run rehearsed flow exactly. Don't improvise new SQL on stage.

## Phase 5: Teardown

- Hard: `DROP DATABASE IF EXISTS DEMO_<topic>` (use templates in `demo-ops:snowflake-conventions`).
- Soft: tag with `DEMO_PRESERVE='true'`, drop only `RAW`.
- Archive: copy final to `~/Documents/<demo>/final/`; summary to `/memories/<demo-name>.md`.

## Working conventions (lightweight)

- Optional git. `git init` is fine; PRs not required.
- Explicit `git add` paths only. Never `git add .`.
- Imperative commit subjects under 72 chars.
- No branches unless demo grows past one session — then graduate to a real repo and adopt project-local `AGENTS.md`.

## Special cases

| Situation | Action |
|---|---|
| Demo grew past one session | Graduate: `git init`, real repo, project-local `AGENTS.md`. |
| Multiple agents on same DB | Each uses distinct `<USER>_DEMO_<topic>` schema. No shared writes. |
| Reused by other SEs | Document connection/role/warehouse/DB/re-run steps in `README.md`. |
| Cross-vendor or peer review | `cross-model-review` skill. No GitHub PR needed. |
| Need to undo a mistaken DROP | `UNDROP DATABASE` / `UNDROP SCHEMA` within Time Travel retention. |

## Reference

- Sibling skills: `demo-ops:coordinator`, `demo-ops:snowflake-conventions`, `demo-ops:synthetic-data`, `demo-ops:deploy`
