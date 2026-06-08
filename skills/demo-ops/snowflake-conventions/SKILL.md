---
name: demo-ops:snowflake-conventions
description: "Demo-scoped Snowflake patterns: DB and schema naming, tagging for cleanup, RBAC defaults, warehouse rules, account quirks, teardown SQL templates. Use when creating, organizing, or tearing down Snowflake objects for a demo. Triggers: demo snowflake, demo database, demo schema, demo cleanup, demo teardown, demo db naming, demo tagging, demo RBAC, demo warehouse, drop demo, cleanup demo objects, demo schema layout."
---

Reusable patterns for demo-scoped Snowflake objects.

## Database & schema naming

| Pattern | When |
|---|---|
| `DEMO_<topic>` | Shared demo run by multiple SEs. e.g. `DEMO_RETAIL_INTELLIGENCE`. |
| `<USER>_DEMO_<topic>` | Personal scratch / in-progress. |
| `SANDBOX_<USER>` | One-off exploration, not a real demo. |

Avoid: writing demo objects to `PUBLIC`, `INFORMATION_SCHEMA`, or production-style DBs.

## Schema layout (3-stage demo)

```
DEMO_<topic>
├── RAW          -- generated synthetic data
├── STAGED       -- cleaned, conformed
├── CURATED      -- analytics-ready
└── APP          -- Streamlit, Notebooks, Cortex Agents, Semantic Views
```

For one-off demos: a single `SANDBOX` schema is fine.

## Required tags

```sql
-- One-time per account: create your own tag namespace (DB and schema)
CREATE TAG IF NOT EXISTS <governance_db>.<governance_schema>.DEMO_OWNER;
CREATE TAG IF NOT EXISTS <governance_db>.<governance_schema>.DEMO_CREATED;
CREATE TAG IF NOT EXISTS <governance_db>.<governance_schema>.DEMO_PRESERVE;

-- Per-DB at creation
ALTER DATABASE DEMO_<topic> SET TAG
    <governance_db>.<governance_schema>.DEMO_OWNER   = '<your-handle>',
    <governance_db>.<governance_schema>.DEMO_CREATED = '<YYYY-MM-DD>';
```

Find your demo objects:

```sql
SELECT OBJECT_DATABASE, OBJECT_SCHEMA, OBJECT_NAME, TAG_VALUE
FROM SNOWFLAKE.ACCOUNT_USAGE.TAG_REFERENCES
WHERE TAG_NAME = 'DEMO_OWNER' AND TAG_VALUE = '<your-handle>'
  AND OBJECT_DELETED IS NULL;
```

## Warehouse rules

| Warehouse | Allowed for |
|---|---|
| `<your-warehouse>` (writable) | DDL, DML, INSERT, COPY, CALL stored procs |
| `<read-only-warehouse>` (shared SELECT) | SELECT, SHOW, DESCRIBE only |

Never use a read-only / shared SELECT warehouse for DDL/DML.

## RBAC defaults

Use a single demo role (whichever role you build under, e.g. `<your-role>`). Don't create roles unless the demo is **about** RBAC.

```sql
GRANT USAGE ON DATABASE DEMO_<topic> TO ROLE <your-role>;
GRANT USAGE ON ALL SCHEMAS IN DATABASE DEMO_<topic> TO ROLE <your-role>;
GRANT SELECT ON ALL TABLES IN SCHEMA DEMO_<topic>.CURATED TO ROLE <your-role>;
GRANT SELECT ON FUTURE TABLES IN SCHEMA DEMO_<topic>.CURATED TO ROLE <your-role>;
```

## Object placement

| Object | Schema |
|---|---|
| Generated raw data | `RAW` |
| Cleaned/staged | `STAGED` |
| Facts/dims/aggregates | `CURATED` |
| Semantic Views, Cortex Agents, Search Services, Streamlit, Notebooks | `APP` |
| File stages | `RAW` (`@RAW.DEMO_STAGE`) |
| Functions/procedures | Same schema as the data they operate on |

## Account quirks (verify with snowflake_product_docs before relying)

- `CONCAT_WS` returns NULL if any arg is NULL → use `ARRAY_TO_STRING(ARRAY_COMPACT(ARRAY_CONSTRUCT(...)), '<sep>')`.
- `SNOWFLAKE.CORTEX.COMPLETE` may only support string format (not messages array) on some accounts.
- `SNOWFLAKE.CORTEX.SUMMARIZE` can fail on very long inputs — truncate to ~8000 chars.
- All SPs use `$$` delimiter, not `AS '...'`.
- `TASK_HISTORY()` lookback is bounded; check current docs for the exact retention.

## Teardown templates

### Hard teardown
```sql
SELECT CURRENT_USER(), CURRENT_ROLE();  -- verify ownership
USE WAREHOUSE <your-warehouse>;
DROP DATABASE IF EXISTS DEMO_<topic>;
```

### Soft teardown
```sql
ALTER DATABASE DEMO_<topic> SET TAG <governance_db>.<governance_schema>.DEMO_PRESERVE = 'true';
DROP SCHEMA IF EXISTS DEMO_<topic>.RAW;
```

### Bulk orphan candidates (lists only, never auto-drops)
```sql
SELECT OBJECT_DATABASE, OBJECT_NAME, TAG_VALUE
FROM SNOWFLAKE.ACCOUNT_USAGE.TAG_REFERENCES
WHERE TAG_NAME = 'DEMO_CREATED'
  AND TRY_TO_DATE(TAG_VALUE) < DATEADD('day', -30, CURRENT_DATE())
  AND OBJECT_DELETED IS NULL
  AND OBJECT_DATABASE NOT IN (
      SELECT OBJECT_DATABASE FROM SNOWFLAKE.ACCOUNT_USAGE.TAG_REFERENCES
      WHERE TAG_NAME = 'DEMO_PRESERVE' AND TAG_VALUE = 'true'
  );
```

## Pre-build checklist

- [ ] Connection confirmed (default `${ACE_DEMO_CONN}`)
- [ ] Role confirmed
- [ ] Writable warehouse selected for DDL/DML
- [ ] DB/schema name follows convention
- [ ] Tags applied at DB creation
- [ ] Teardown SQL drafted before any object created

## Reference

- Sibling skills: `demo-ops:coordinator`, `demo-ops:workflow`, `demo-ops:deploy`
