# Skills

This directory contains the CCD skills the Account Engineer profile registers.

## v0.1.0 Skills

| Skill | Purpose |
|---|---|
| `asset-creation-discipline/` | Apply rigorous discipline to creation tasks (PDFs, notebooks, scripts, decks, research). Active in v0.1.0 — see [asset-creation-discipline/SKILL.md](asset-creation-discipline/SKILL.md). |

## Migration Roadmap

The profile starts thin and grows in phases. Each phase adds a category of skills.

### Phase 2: Read-Only Skills (no personal data)

These skills have no hardcoded personal references — straight migration into the profile.

| Skill | Source | Status |
|---|---|---|
| `snowflake-pdf` | `~/.snowflake/cortex/skills/snowflake-pdf/` | Planned |
| `architecture-diagram` | local | Planned |
| `gdrive-desktop` | local | Planned |
| `gong` | local | Planned |
| `similar-use-cases` | local | Planned |
| `pptx` | local | Planned |

### Phase 3: Personal-Data Skills (require sanitization)

These skills currently contain hardcoded connection names, usernames, account references — must be parameterized before migration.

| Skill | Source | Sanitization needed |
|---|---|---|
| `account-context` | local | Connection names, user handles |
| `account-handoff` | local | Personal references |
| `account-status` | local | Customer account names |
| `account-team` | local | Team membership data |
| `activity-log` | local | Personal log path |
| `customer-role-hierarchy` | local | Connection names |
| `external-account-context` | local | Personal context |
| `meeting-prep` | local | Personal references |
| `salesforce-account-intel` | local | SF auth + connection |
| `todo-log` | local | Personal todos |
| `use-case-data` | local | Personal use case ids |
| `use-case-update` | local | Personal use case ids |

Sanitization pattern: replace personal values with `${ACE_DEFAULT_CONN}` / `${ACE_USER_HANDLE}` env var references; document required env vars in the skill's SKILL.md.

### Skills That Stay Personal (NOT in Profile)

| Skill | Reason |
|---|---|
| `slack-bridge` | Personal phone, personal Slack DMs |
| `bookmanager-ops` | Project-specific, not ACE-general |
| `de-studies` | Personal curriculum tracking |

## Adding a New Skill

See [../CONTRIBUTING.md](../CONTRIBUTING.md). Briefly:

1. Branch: `git checkout -b feat/<skill-name>`
2. Place at `skills/<skill-name>/` with a `SKILL.md` defining triggers and workflow
3. Sanitize any personal values (connection names, usernames, account references)
4. Run the public-repo grep recipe (see [../docs/public-repo-policy.md](../docs/public-repo-policy.md))
5. Update this README to list the new skill
6. Open PR
