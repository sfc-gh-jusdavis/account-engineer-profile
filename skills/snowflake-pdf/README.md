# snowflake-pdf

CoCo skill that renders Markdown documents into Snowflake-branded PDFs with verified documentation references.

## Features

- Snowflake-branded cover page (Midnight `#11487A`, Mid-Blue `#29B5E8`, Valencia Orange `#FF9F36`)
- Cover meta (title, customer, author, date, classification)
- Validation gate: scans the markdown for SYSTEM$ functions, DDL/DML keywords, ACCOUNT_USAGE / INFORMATION_SCHEMA views, CLI tools, and Snowflake feature names; the agent verifies each against `docs.snowflake.com` before rendering
- Appended **References** section grouped by category with hyperlinks to primary Snowflake docs
- WeasyPrint-preferred / Chrome-headless fallback rendering

## Install (via CoCo)

In CoCo, say:

> **Install the snowflake-pdf skill from `https://github.com/<org>/snowflake-pdf`**

CoCo will follow [INSTALL.md](INSTALL.md) and ask you to approve each command (clone + pip install + optional brew). Restart CoCo when it finishes.

## Use (via CoCo)

> **Render `path/to/doc.md` as a Snowflake PDF for `<customer>`**

CoCo will:
1. Run the validation workflow (extract candidates, look up each in Snowflake docs)
2. Stop and ask you to resolve anything it can't verify
3. Write `path/to/doc.references.json`
4. Render `path/to/doc.pdf`

Add YAML front-matter to the markdown:

```yaml
---
title: ADF Private Link Troubleshooting
subtitle: Diagnostics for SqlState 08006 over Azure Private Link
customer: <example-customer>
author: <your-name>
classification: Customer Confidential
date: May 6, 2026
---
```

## Direct CLI usage (advanced)

```bash
python ~/.snowflake/cortex/skills/snowflake-pdf/render.py --check
python ~/.snowflake/cortex/skills/snowflake-pdf/extract_candidates.py INPUT.md
python ~/.snowflake/cortex/skills/snowflake-pdf/render.py INPUT.md OUTPUT.pdf --references INPUT.references.json
python ~/.snowflake/cortex/skills/snowflake-pdf/render.py INPUT.md OUTPUT.pdf --no-validate    # for non-Snowflake docs
```

The renderer **refuses to run** without `--references` or `--no-validate`. This is the validation gate.

## Files

| File | Role |
|---|---|
| `SKILL.md` | Agent-facing skill definition (load on import, drives the workflow) |
| `render.py` | Markdown → branded HTML → PDF |
| `extract_candidates.py` | Scan markdown for Snowflake references |
| `template.html.j2` | Jinja2 brand template (cover + body + running header + references) |
| `brand.css` | Snowflake brand styling (CSS Paged Media + body + references) |
| `INSTALL.md` | Steps the agent runs to install/upgrade the skill |
| `samples/` | Minimal example doc and reference JSON for self-test |
| `VERSION` | Semver string |
| `LICENSE` | Apache-2.0 |

## License

Apache-2.0. See [LICENSE](LICENSE).
