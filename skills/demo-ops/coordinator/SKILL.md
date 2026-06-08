---
name: demo-ops:coordinator
description: "Orchestrates the full demo lifecycle: scope, build, rehearse, present, teardown. Use when the user asks for a demo end-to-end. Triggers: build a demo for, orchestrate demo, demo plan, demo lifecycle, full demo, end-to-end demo, plan a demo, scope a demo, walk me through building a demo."
---

Owns the demo lifecycle. Walks the user through 5 phases and dispatches to the right sub-skill at each step.

## Phase 1: Scope

1. Use `ask_user_question` to confirm any of these that are unspecified:
   - Audience (internal SE, customer, executive?)
   - Takeaway / "wow" moment
   - Runtime budget (5 / 15 / 30 min)
   - DB/schema name (`DEMO_<topic>` vs `<USER>_DEMO_<topic>`)
   - Cleanup intent (drop / preserve)
   - Snowflake connection (default `${ACE_DEMO_CONN}`)
2. Identify which sub-skills will be needed:
   - Synthetic data? -> plan to invoke `demo-ops:synthetic-data`
   - Streamlit / Notebook / Agent / Semantic View? -> plan to invoke `demo-ops:deploy`
3. **Switch to plan mode** for non-trivial work; present the plan and wait for user approval before agent mode.

## Phase 2: Build

1. Invoke `demo-ops:snowflake-conventions` to set up the DB, schemas, and tags first.
2. Run any synthetic-data generation via `demo-ops:synthetic-data`. Schema-first, seed all randomness.
3. Build downstream objects (semantic view, agent, Streamlit) in `<DEMO_DB>.APP`.
4. Use `system_todo_write` for build sequences with >3 steps; mark complete in real time.
5. Compile-check destructive SQL with `snowflake_sql_execute(only_compile=true, ...)` before running.
6. Checkpoint at milestones: snapshot working SQL/Python/YAML to `~/Documents/<demo>/checkpoints/<YYYY-MM-DD>/`.

## Phase 3: Rehearse (in-session validation, replaces CI)

Invoke `demo-ops:workflow` for the validation gate ladder. Required gates:

- All SQL compiles
- Cortex Agent answers each verified query
- Streamlit page loads (no console errors)
- Notebook executes top-to-bottom without errors
- Semantic view returns rows for each metric
- No real PII in any artifact (run grep)
- Teardown SQL exists and reads end-to-end

If any gate fails -> back to Phase 2.

## Phase 4: Present

- Run the rehearsed flow exactly. Do not improvise new SQL on stage.
- Keep teardown handy but do NOT run it during the demo.

## Phase 5: Teardown

- Invoke `demo-ops:snowflake-conventions` for the teardown SQL templates.
- Hard teardown: `DROP DATABASE IF EXISTS DEMO_<topic>`.
- Soft teardown: tag with `DEMO_PRESERVE='true'`, drop only `RAW`.
- Archive: copy final artifacts to `~/Documents/<demo>/final/` and write a summary to `/memories/<demo-name>.md`.

## Self-review before declaring done

Invoke `demo-ops:principles` for the Karpathy P1-P4 checklist + Privacy + Teardown + Determinism gates.

## References

- Sibling skills: `demo-ops:workflow`, `demo-ops:snowflake-conventions`, `demo-ops:synthetic-data`, `demo-ops:deploy`, `demo-ops:principles`
- ACE profile system prompt: `system-prompt.md` at repo root
