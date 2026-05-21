# Skills

This directory contains the CCD skills the Account Engineer profile registers.

## v0.2.0 Skills (Phase 2 read-only migrations complete)

| Skill | Purpose |
|---|---|
| `ace-setup/` | First-time and recurring setup workflow. Captures per-ACE config (Snowflake connection, username, demo account, display name, GitHub handle and org, work email, gdrive base path) via 10 questions, auto-detecting defaults from `gh`, `snow`, and filesystem inspection. Persists to `/memories/ace-setup.md`. See [ace-setup/SKILL.md](ace-setup/SKILL.md). |
| `architecture-diagram/` | Mermaid diagram standards for Snowflake projects (data-model, data-flow, network-flow, auth-flow). See [architecture-diagram/SKILL.md](architecture-diagram/SKILL.md). |
| `asset-creation-discipline/` | Apply rigorous discipline to creation tasks (PDFs, notebooks, scripts, decks, research). See [asset-creation-discipline/SKILL.md](asset-creation-discipline/SKILL.md). |
| `gong/` | Find Gong call summaries in Snowhouse. See [gong/SKILL.md](gong/SKILL.md). |
| `pptx/` | Snowflake-branded PowerPoint deck creation with Google Drive sync. See [pptx/SKILL.md](pptx/SKILL.md). |
| `similar-use-cases/` | Find similar use cases and customer patterns using Glean search. See [similar-use-cases/SKILL.md](similar-use-cases/SKILL.md). |
| `snowflake-pdf/` | Render Markdown into Snowflake-branded PDFs with cover page, brand colors, classification footer, validated References section. See [snowflake-pdf/SKILL.md](snowflake-pdf/SKILL.md). |

## v0.3.0 Skills (demo-ops bundle)

| Skill | Purpose |
|---|---|
| `demo-ops/` | Parent dispatcher for the demo bundle. Routes to 6 sub-skills covering the full demo lifecycle (scope, build, rehearse, present, teardown). See [demo-ops/README.md](demo-ops/README.md). Sub-skills: `demo-ops:coordinator`, `demo-ops:principles`, `demo-ops:workflow`, `demo-ops:synthetic-data`, `demo-ops:snowflake-conventions`, `demo-ops:deploy`. |

## Migration Roadmap

### Phase 3: Personal-Data Skills (require sanitization) — PLANNED

These skills currently contain hardcoded connection names, user emails, gdrive paths, or account references. Each must be parameterized before migration. Sanitization pattern: replace personal values with `${ACE_*}` placeholder references that resolve via `/memories/ace-setup.md` (populated by the `ace-setup` skill) or profile envVars.

| Skill | Source | Sanitization scope |
|---|---|---|
| `gdrive-desktop` | local | Hardcoded gdrive base path; reads `gdrive_base` from memory |
| `account-context` | local | YAML config block: `user_email`, `gdrive_base` |
| `account-handoff` | local | YAML config block; example owner field |
| `account-status` | local | YAML config block; customer name examples |
| `account-team` | local | YAML config block: `user_email` |
| `activity-log` | local | Hardcoded log path; reads `gdrive_base` from memory |
| `customer-role-hierarchy` | local | Connection name literals |
| `external-account-context` | local | YAML config block; "Consumers Credit Union" examples |
| `meeting-prep` | local | YAML config block |
| `salesforce-account-intel` | local | YAML config block; SF connection literals |
| `todo-log` | local | Hardcoded log + draft folder paths |
| `use-case-data` | local | YAML config block; `config.yaml` |
| `use-case-update` | local | YAML config block |

### Phase 4: Slash Commands + Examples — PLANNED

Slash commands (`/start-asset`, `/multi-review`, `/public-repo-review`, `/audience-check`), sanitized example assets, and a pre-commit hook for the public-repo content sweep.

### Phase 5: Second-ACE Onboarding — PLANNED

Validate the profile end-to-end with a second ACE installing it cold.

### Skills That Stay Personal (NOT in Profile)

| Skill | Reason |
|---|---|
| `slack-bridge` | Personal phone, personal Slack DMs |
| `bookmanager-ops` | Project-specific to one engagement |
| `de-studies` | Personal curriculum tracking |

## Adding a New Skill

See [../CONTRIBUTING.md](../CONTRIBUTING.md). Briefly:

1. Branch: `git checkout -b feat/<skill-name>`
2. Place at `skills/<skill-name>/` with a `SKILL.md` defining triggers and workflow
3. Sanitize any personal values (connection names, usernames, account references, paths)
4. Run the public-repo grep recipe (see [../docs/public-repo-policy.md](../docs/public-repo-policy.md))
5. Update this README to list the new skill
6. Open PR
