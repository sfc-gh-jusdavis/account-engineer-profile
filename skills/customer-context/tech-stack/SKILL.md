---
name: customer-context:tech-stack
description: "Track and update the Tech Stack section of context.md for a customer
  activation project. Use when: 'log tech stack', 'add tech stack', 'update tech
  stack', or when a new tool/platform/connector is mentioned in conversation and
  should be captured. Updates Group 3 Tech Stack subsections only."
---

# Customer Context: Tech Stack

Updates the `### Tech Stack` subsections of `./context.md`. Can be called mid-conversation whenever a new tool or integration is mentioned, or at any point to do a structured tech audit.

**Scope:** Group 3 (`### Tech Stack`) only. All other sections of `context.md` are untouched.

---

## Workflow

### Step 1: Orient

1. Read `./context.md` — confirm account name from the `# Context: [Account Name]` header.
2. Read the current state of all three Tech Stack subsections:
   - `#### Inbound to Snowflake`
   - `#### Outbound from Snowflake`
   - `#### Peripheral Services`
3. Note what is already listed (to avoid duplicates).

If `context.md` is not found in CWD:
```
context.md not found. Run `customer-context:init` first to initialize the project context.
```

---

### Step 2: Gather New Tech Info

Pull from all available sources in the current session:

| Source | How |
|---|---|
| **User input** | Parse tool/platform names from the current message or pasted notes |
| **Current conversation** | Scan conversation context for tool/integration mentions |
| **Recent Gong calls** | Run `gong` skill for account, scan call briefs for tech keywords |

**Keywords to watch for:** connector, pipeline, ETL, ELT, integration, ingest, load, sync, export, transform, orchestrate, warehouse, BI, dashboard, reporting, API, stream, CDC, trigger, schedule, deploy, infra.

---

### Step 3: Categorize Findings

Sort each new item into one of three categories:

| Category | Belongs here if it... | Examples |
|---|---|---|
| **Inbound to Snowflake** | Moves data INTO Snowflake | Fivetran, Airbyte, Kafka, AWS Glue, Spark, dbt (as ELT source), Snowpipe, custom ETL scripts |
| **Outbound from Snowflake** | Consumes data FROM Snowflake | Tableau, Power BI, Sigma, Looker, Census, Hightouch, Streamlit, APIs served from Snowflake, data shares |
| **Peripheral Services** | Supports the pipeline but doesn't move data directly | Airflow, Prefect, dbt Cloud, Databricks (orchestration role), GitHub Actions, Terraform, Secrets Manager |

If a tool could be in more than one category, note both uses:
```
- Databricks (Inbound: raw data processing before load; Peripheral: orchestration)
```

---

### Step 4: Show Diff Before Writing

Always present the proposed changes before touching the file:

```
Tech Stack update for [Account Name]:

[ADD] Inbound:    Fivetran            (source: Gong 2026-06-05)
[ADD] Inbound:    Apache Kafka        (source: user input)
[ADD] Peripheral: dbt Cloud           (source: current conversation)
[SKIP] Tableau — already listed under Outbound
```

- If > 5 new items: ask confirmation before writing.
- If ≤ 5 new items: write directly (no confirmation needed — user already provided the input).

---

### Step 5: Update Tech Stack Subsections

Write the updated subsections in place. Format each entry as a bullet with an inline source comment:

```markdown
#### Inbound to Snowflake
- Fivetran <!-- source: Gong 2026-06-05 -->
- Apache Kafka <!-- source: user input, 2026-06-08 -->

#### Outbound from Snowflake
- Tableau <!-- source: Raven init -->

#### Peripheral Services
- dbt Cloud <!-- source: current conversation, 2026-06-08 -->
```

Also update the `*Last updated: [date]*` header line in `context.md`.

Only the `### Tech Stack` section (and the header date) changes. All other sections remain byte-for-byte identical.

---

### Step 6: Print Summary

```
Tech Stack updated in ./context.md

Added:   [count] items
Skipped: [count] already present
Section: Group 3 / Tech Stack
```

---

## Stopping Points

- If `context.md` not found: offer to run `customer-context:init` first
- Ask for confirmation before writing if > 5 new items
- If a tool's category is genuinely ambiguous, ask the user which category fits their use case

## Skills Called

| Skill | Purpose |
|---|---|
| `gong` | Optional — pull recent Gong call briefs to scan for tech mentions |
