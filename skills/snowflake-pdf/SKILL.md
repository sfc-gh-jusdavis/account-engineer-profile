# snowflake-pdf

Render Markdown documents into Snowflake-branded PDFs with a cover page, brand colors (Midnight `#11487A`, Mid-Blue `#29B5E8`, Valencia Orange `#FF9F36`), running header, page numbers, classification footer, and a verified References section.

## Description

Use this skill when the user asks to:
- generate a PDF, create a PDF, render a PDF
- produce a "Snowflake-branded" / "on-brand" / "customer-facing" document
- convert markdown / a doc into a polished PDF

Triggers: pdf, branded pdf, snowflake pdf, customer-facing document, troubleshooting doc, runbook pdf, deliverable pdf.

## Files

- `render.py`              — main renderer (markdown → HTML → PDF)
- `extract_candidates.py`  — scans markdown for Snowflake references (system functions, DDL keywords, views, CLI/SnowCD, feature names)
- `template.html.j2`       — Jinja2 brand template (cover + body + running header + references)
- `brand.css`              — Snowflake brand styling (CSS Paged Media + body)
- `assets/`                — logos / images referenced by the template

## Audience Workflow (REQUIRED — runs BEFORE Validation)

Every document must declare exactly one audience. The renderer **refuses to run** if `audience` is missing or invalid. Allowed values:

- `customer-facing` — customer-readable, polished, second-person
- `internal` — Snowflake-only, terse, third-person customer references OK
- `partner` — Snowflake + Partner under MNDA, peer collaborator tone
- `field-only` — Snowflake field organization only, SE-shorthand OK

The agent **must** execute this workflow before the Validation Workflow:

### Step A1 — Read or ask for the audience

1. Parse YAML front-matter for `audience:`
2. If absent or not in the allowed set, **ask the user**:
   ```
   Who is this document for?
     1) customer-facing  (external-readable)
     2) internal         (Snowflake-only)
     3) partner          (Snowflake + Partner)
     4) field-only       (Snowflake field org)
   ```
3. Write the chosen value back into the markdown front-matter.

### Step A2 — Review the doc against the audience profile

1. Load `audience-profiles.md` and the corresponding profile section.
2. Read the markdown body. Produce findings of the form:
   ```
   { "line": 8, "category": "voice", "original": "...", "suggestion": "...", "reason": "..." }
   ```
   Categories: `voice`, `terminology`, `link`, `content`, `classification`.
3. Stop and present the findings to the user, grouped by category. For each finding offer:
   - **Accept** the suggested rewrite
   - **Keep** as-is (with reason)
   - **Replace** with custom text the user provides
   Bulk options: "accept all", "skip all in this category".

### Step A3 — Apply accepted rewrites

Edit the markdown in place. Re-read the file before continuing.

### Step A4 — Continue

Proceed to the existing Validation Workflow.

---

## Validation Workflow (REQUIRED)

The renderer **refuses to run** unless one of the following is true:
- `--references PATH` is supplied (validated references exist), OR
- `--no-validate` is explicitly passed (escape hatch for non-Snowflake docs)

The agent **must** execute this workflow before invoking `render.py` for any Snowflake content:

### Step 1 — Extract candidates

```bash
/opt/anaconda3/bin/python3 ~/.snowflake/cortex/skills/snowflake-pdf/extract_candidates.py INPUT.md
```

Returns JSON with five categories:
- `system_functions` (SYSTEM$XXX)
- `ddl_dml_keywords` (SHOW/ALTER/CREATE/DESC/DESCRIBE/GRANT/REVOKE)
- `usage_views` (ACCOUNT_USAGE.* / INFORMATION_SCHEMA.* / ORGANIZATION_USAGE.*)
- `cli_tools` (SnowCD, snow CLI subcommands)
- `feature_names` (Azure Private Link, network policy, Tri-Secret Secure, etc.)

### Step 2 — Resolve each candidate via `snowflake_product_docs`

For every candidate, call `snowflake_product_docs` with the `label` as the query. Pick the **best primary-documentation URL** (`docs.snowflake.com/...`). Discard knowledge-base / community results unless no primary doc exists.

### Step 3 — Surface unresolved candidates to the user

Build the list of candidates that returned no high-confidence primary-doc URL. **Stop and present them to the user** with three options each:
1. **Drop** — the reference is incidental; remove it from the doc body
2. **Keep unlinked** — user confirms the reference is correct as written; exclude from References
3. **Replace** — user supplies a different label / correction

Do **not** generate the PDF until the user has decided on every unresolved item.

### Step 4 — Persist `<doc>.references.json`

Write a JSON array next to the input markdown:

```json
[
  {"label":"SYSTEM$AUTHORIZE_PRIVATELINK","url":"https://docs.snowflake.com/en/sql-reference/functions/system_authorize_privatelink","category":"System Function"},
  {"label":"Azure Private Link & Snowflake","url":"https://docs.snowflake.com/en/user-guide/privatelink-azure","category":"Feature"}
]
```

Allowed `category` values: `System Function`, `SQL Command`, `Usage View`, `CLI / Tool`, `Feature`.

### Step 5 — Render

```bash
/opt/anaconda3/bin/python3 ~/.snowflake/cortex/skills/snowflake-pdf/render.py \
    INPUT.md  OUTPUT.pdf \
    --references INPUT.references.json
```

The PDF will include a "References" section grouped by category with hyperlinked entries.

## Usage (no validation, e.g. for non-Snowflake content)

```bash
/opt/anaconda3/bin/python3 ~/.snowflake/cortex/skills/snowflake-pdf/render.py \
    INPUT.md  OUTPUT.pdf \
    --no-validate \
    --meta title="My Doc" \
    --meta customer="<example-customer>" \
    --meta author="<your-name>" \
    --meta classification="Customer Confidential"
```

YAML front-matter is honored:

```markdown
---
title: ADF Private Link Troubleshooting
subtitle: Diagnostics for SqlState 08006 over Azure Private Link
customer: <example-customer>
author: <your-name>
classification: Customer Confidential
date: May 6, 2026
---
```

## Diagnostics

```bash
python render.py --check
```

Prints which Python is in use, whether WeasyPrint is importable, and which Chrome binary is found. Read-only; writes nothing.

## Rendering backends

WeasyPrint is preferred (real running headers, page counters, classification footer via CSS Paged Media). Chrome headless is the fallback.

For full WeasyPrint support on macOS:
```
brew install pango cairo gdk-pixbuf libffi
```

## Required Python packages

```
pip install jinja2 markdown pyyaml weasyprint
```

The skill defaults to `/opt/anaconda3/bin/python3` which already has `jinja2`, `markdown`, and `weasyprint` available.

## Brand reference

| Token | Hex |
|---|---|
| Midnight (primary) | `#11487A` |
| Mid-Blue (accent) | `#29B5E8` |
| Valencia Orange (highlight) | `#FF9F36` |
| Windy City Grey | `#8A999E` |
| Light Surface | `#F4F7FA` |

Typography: Inter → Helvetica Neue → Arial. Code: JetBrains Mono → Menlo.
