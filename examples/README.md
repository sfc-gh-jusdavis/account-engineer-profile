# Examples

Sanitized exemplar assets contributors can read for inspiration.

## v0.1.0 Status

This directory is a placeholder in v0.1.0. Examples land in **Phase 4** of the rollout, after the asset-creation-discipline skill has been used in real ACE work and patterns emerge worth documenting.

## Planned Examples (Phase 4)

| Example | Asset type | Purpose |
|---|---|---|
| `pdf-setup-guide-skeleton.md` | PDF | A blank fill-in-the-skeleton for a setup guide (no real customer) |
| `pdf-troubleshooting-skeleton.md` | PDF | A blank skeleton for a troubleshooting doc |
| `notebook-analysis-template.ipynb` | Notebook | A clean analysis-notebook starter with discipline applied |
| `script-snowflake-utility.sh` | Script | A clean idempotent script template |
| `research-decision-doc.md` | Research | A clean decision-supporting research template |

## Sanitization Standard

Every example in this directory:

- Uses `<example-customer>` placeholder for any customer reference
- Uses `${ACE_DEFAULT_CONN}` / `${ACE_USER_HANDLE}` for any connection / user reference
- Uses generic Snowflake account placeholders (`<account_name>`, `<region>`)
- Has zero references to internal Snowflake URLs (`go/`, Confluence, Slack, Quip)
- Has zero references to Justin's or any specific ACE's tooling

See [../docs/public-repo-policy.md](../docs/public-repo-policy.md) for full policy.

## Why Empty in v0.1.0

Premature examples crystallize patterns that may not survive contact with real use. Phase 4 picks up examples after the discipline has been exercised on actual ACE deliverables.
