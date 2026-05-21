---
name: demo-ops:deploy
description: "Deploy demo surfaces to Snowflake: Streamlit-in-Snowflake, Snowflake Notebook, Cortex Agent, Semantic View, Cortex Search Service. Lightweight, no Docker. Use when shipping a demo. Triggers: deploy demo, ship demo, deploy streamlit demo, deploy demo notebook, deploy demo agent, deploy semantic view demo, snow streamlit deploy demo, snow notebook deploy demo, demo URL, publish demo."
---

Lightweight deploy patterns for demos. No Docker, no Makefile, no SPCS by default.

## When to use what

| Surface | Deploy target |
|---|---|
| Interactive UI with charts/forms | Streamlit in Snowflake |
| Step-by-step analytical narrative | Snowflake Notebook |
| Natural-language Q&A | Cortex Agent (on a Semantic View) |
| Text-to-SQL over a curated mart | Semantic View + Cortex Analyst |
| Document Q&A | Cortex Search Service |
| Containerized full-stack | SPCS — graduate to a real repo first |

## Streamlit in Snowflake

```bash
snow streamlit deploy \
    --replace \
    --connection ${ACE_DEFAULT_CONN} \
    --database DEMO_<topic> \
    --schema APP
```

`snowflake.yml`:

```yaml
definition_version: 2
entities:
  my_demo_app:
    type: streamlit
    identifier:
      name: <demo_name>
      schema: APP
      database: DEMO_<topic>
    main_file: streamlit_app.py
    query_warehouse: <your-warehouse>
    title: <Demo Title>
```

```sql
SHOW STREAMLITS IN SCHEMA DEMO_<topic>.APP;
SELECT SYSTEM$GENERATE_STREAMLIT_URL_FROM_NAME('DEMO_<topic>.APP.<demo_name>');
```

## Snowflake Notebooks

```bash
snow notebook deploy <notebook_name> \
    --connection ${ACE_DEFAULT_CONN} \
    --database DEMO_<topic> \
    --schema APP \
    --replace
```

Or via SQL:

```sql
PUT file://./notebook.ipynb @DEMO_<topic>.RAW.DEMO_STAGE/notebooks/ AUTO_COMPRESS=FALSE OVERWRITE=TRUE;
CREATE OR REPLACE NOTEBOOK DEMO_<topic>.APP.<notebook_name>
    FROM '@DEMO_<topic>.RAW.DEMO_STAGE/notebooks/'
    MAIN_FILE = 'notebook.ipynb'
    QUERY_WAREHOUSE = <your-warehouse>;
```

## Semantic View

```sql
PUT file://./semantic_model.yaml @DEMO_<topic>.RAW.DEMO_STAGE/semantic/ AUTO_COMPRESS=FALSE OVERWRITE=TRUE;

CREATE OR REPLACE SEMANTIC VIEW DEMO_<topic>.APP.<view_name>
    TABLES (...)
    DIMENSIONS (...)
    METRICS (...)
    ;
```

Validate before declaring done:

```sql
DESC SEMANTIC VIEW DEMO_<topic>.APP.<view_name>;

SELECT * FROM SEMANTIC_VIEW(
    DEMO_<topic>.APP.<view_name>
    DIMENSIONS <dim>
    METRICS <metric>
) LIMIT 10;
```

Walk every verified query in the YAML and confirm SQL compiles. Verify syntax with `snowflake_product_docs` before relying on advanced features.

## Cortex Agent

```sql
CREATE OR REPLACE AGENT DEMO_<topic>.APP.<agent_name>
WITH PROFILE='{"display_name": "<demo title>"}'
COMMENT='<short description>'
FROM SPECIFICATION $$
{
  "models": { "orchestration": "auto" },
  "instructions": {
    "response": "...",
    "orchestration": "...",
    "sample_questions": [{ "question": "..." }]
  },
  "tools": [
    { "tool_spec": { "type": "cortex_analyst_text_to_sql", "name": "Analyst1" } }
  ],
  "tool_resources": {
    "Analyst1": { "semantic_view": "DEMO_<topic>.APP.<view_name>" }
  }
}
$$;
```

Verify: open in Snowflake Intelligence; run each `sample_question`; confirm answer cites the right tool.

## Cortex Search Service

```sql
CREATE OR REPLACE CORTEX SEARCH SERVICE DEMO_<topic>.APP.<svc_name>
    ON CONTENT
    ATTRIBUTES <attr1>, <attr2>
    WAREHOUSE = <your-warehouse>
    TARGET_LAG = '1 hour'
    AS (SELECT CONTENT, <attr1>, <attr2> FROM DEMO_<topic>.CURATED.<source>);
```

## Pre-deploy checklist

- [ ] PII grep clean
- [ ] All SQL compiles (`only_compile=true`)
- [ ] Target DB.SCHEMA exists and is tagged
- [ ] Writable warehouse selected (not a read-only / shared SELECT warehouse)
- [ ] Replace mode is intentional
- [ ] Teardown SQL exists and reads end-to-end

## Post-deploy verification

| Surface | Verify |
|---|---|
| Streamlit | Open URL; click every page; check console |
| Notebook | Open in Snowsight; run all cells |
| Semantic View | Query each metric; walk verified queries |
| Cortex Agent | Run each sample question |
| Cortex Search | Run a representative query |

## Graduating to a repo

When a demo grows past one session — multi-file, shared with other SEs, regenerated frequently:

1. `git init` and push to private GitHub.
2. Create project-local `AGENTS.md`.
3. Adopt branch + PR workflow if multiple agents will work in parallel.
4. Optionally add CI gates (lint, tests, PII scan).

Until then, keep it lightweight.

## Reference

- Sibling skills: `demo-ops:coordinator`, `demo-ops:snowflake-conventions`
- Verify Snowflake CLI / SQL syntax with `snowflake_product_docs` before relying on advanced features.
