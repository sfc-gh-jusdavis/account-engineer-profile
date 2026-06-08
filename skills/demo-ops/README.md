# demo-ops

Skill bundle for building lightweight, non-repo Snowflake demos. The parent skill (`demo-ops`) routes to 6 sub-skills covering the full demo lifecycle.

## Skills in this bundle

| Skill | Purpose |
|---|---|
| `demo-ops` | Parent dispatcher. Confirms scope, picks DB/schema, routes to the right sub-skill. |
| `demo-ops:coordinator` | Orchestrates the full lifecycle (Scope / Build / Rehearse / Present / Teardown). |
| `demo-ops:principles` | Karpathy P1-P4 + demo-specific anti-patterns + self-review checklist. |
| `demo-ops:workflow` | Phase-by-phase walk-through with in-session validation gates that replace CI. |
| `demo-ops:synthetic-data` | Fabricate non-PII data: SQL generators, Faker UDFs, Cortex COMPLETE, AI_EXTRACT. |
| `demo-ops:snowflake-conventions` | DB/schema naming, tagging, RBAC defaults, warehouse rules, teardown SQL. |
| `demo-ops:deploy` | Streamlit-in-Snowflake, Notebook, Cortex Agent, Semantic View, Cortex Search Service deploy. |

## When to invoke

| User intent | Invoke |
|---|---|
| "Build a demo for X" / lifecycle help | `demo-ops:coordinator` |
| "Generate fake / synthetic / mock data" | `demo-ops:synthetic-data` |
| "Demo DB / schema naming, tagging, teardown" | `demo-ops:snowflake-conventions` |
| "Deploy Streamlit / Notebook / Agent / Semantic View" | `demo-ops:deploy` |
| "Review my demo code" | `demo-ops:principles` |
| "What are the phases / gates?" | `demo-ops:workflow` |
| Ambiguous / general demo question | `demo-ops` (parent dispatches) |

## Conventions assumed

The bundle uses placeholder strings throughout and reads connection from the profile env var:

| Setting | Value |
|---|---|
| Connection | `${ACE_DEMO_CONN}` |
| Warehouse for DDL/DML | `<your-warehouse>` (any writable warehouse you own) |
| Warehouse for SELECT | `<read-only-warehouse>` (the shared SELECT warehouse on your account) |
| DB naming | `DEMO_<topic>` shared / `<USER>_DEMO_<topic>` personal |
| Schema layout | `RAW` / `STAGED` / `CURATED` / `APP`, or single `SANDBOX` |

Substitute these per your account before running any SQL.

## Privacy rule (always)

- All demo data is synthetic. Never use real customer / employee names or real account IDs.
- See `demo-ops:synthetic-data` for the PII-grep pattern that runs before any demo ships.
- The repo's [public-repo-policy](../../docs/public-repo-policy.md) applies to all examples in this bundle.
