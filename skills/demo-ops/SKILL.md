---
name: demo-ops
description: "Parent skill for building Snowflake demos and lightweight non-repo work. Use when the user wants to build, scope, deploy, or tear down a demo, generate synthetic data, or set up a demo-scoped Snowflake DB. Triggers: demo, build a demo, create a demo, demo for, demo project, scratch demo, lightweight demo, non-repo demo, synthetic data, fake data, mock data, generate demo data, demo schema, demo database, deploy demo, ship demo, teardown demo, sales engineering demo, SE demo."
---

Parent skill for the demo-ops bundle. Routes the agent to the right sub-skill for the current phase of demo work.

## Pre-flight (always run first)

Before invoking any sub-skill, confirm:

1. **Snowflake connection** — default `${ACE_DEFAULT_CONN}` (or whichever the user has configured). Confirm out loud.
2. **Audience and goal** — who is the demo for, what is the takeaway?
3. **Runtime budget** — how long is the live presentation (5 / 15 / 30 min)?
4. **DB/schema** — `DEMO_<topic>` (shared) or `<USER>_DEMO_<topic>` (personal scratch). Pick before any DDL.
5. **Cleanup intent** — drop after demo, or preserve for re-runs?

If any of the above are unclear, use `ask_user_question` before doing work.

For non-trivial demos (>3 build steps, multiple objects, shared DB writes), switch to plan mode and get user approval before agent mode.

## Routing table

| User intent | Invoke |
|---|---|
| "Build a demo" / "I need a demo for X" / lifecycle help | `demo-ops:coordinator` |
| "How should I structure / review my demo code?" | `demo-ops:principles` |
| "What are the phases / gates? How do I rehearse?" | `demo-ops:workflow` |
| "Generate fake / synthetic / mock data" | `demo-ops:synthetic-data` |
| "Demo DB / schema naming, tagging, RBAC, teardown" | `demo-ops:snowflake-conventions` |
| "Deploy Streamlit / Notebook / Cortex Agent / Semantic View for the demo" | `demo-ops:deploy` |

## Defaults this bundle assumes

| Setting | Default |
|---|---|
| Connection | `${ACE_DEFAULT_CONN}` |
| Warehouse for DDL/DML | `<your-warehouse>` (never the read-only / shared SELECT warehouse) |
| Warehouse for SELECT | `<read-only-warehouse>` |
| DB naming | `DEMO_<topic>` shared, `<USER>_DEMO_<topic>` personal |
| Schema layout | `RAW` / `STAGED` / `CURATED` / `APP`, or single `SANDBOX` |
| Tagging | `DEMO_OWNER`, `DEMO_CREATED` on every demo DB |

## Privacy rule (HIGH PRIORITY)

- Never use real internal company email domains in fabricated data.
- Never use real customer / employee names or real account IDs.
- All demo data is synthetic. See `demo-ops:synthetic-data`.

## References

- ACE profile system prompt: `system-prompt.md` at the repo root
- Public-repo policy: `docs/public-repo-policy.md`
