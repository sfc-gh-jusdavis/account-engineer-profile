# Roadmap

The Account Engineer profile rolls out in five phases. v0.1.0 (this release) is Phase 1.

## Phase 1: Bootstrap (v0.1.0) — DONE

Established repo, system prompt, asset-creation-discipline skill.

| Item | Status |
|---|---|
| Repo skeleton (LICENSE, README, INSTALL, CONTRIBUTING, CODE_OF_CONDUCT, SECURITY) | Done |
| profile.json manifest | Done |
| system-prompt.md (ACE persona + default policies) | Done |
| docs/ (ai-dev-patterns, karpathy, onboarding, architecture, public-repo-policy) | Done |
| skills/asset-creation-discipline (principles, patterns, 4 overlays, reviewer-prompts) | Done |
| Public GitHub repo created and pushed | Done |
| Profile installed in CCD via form | User action |
| Smoke test (notebook draft request triggers discipline) | User action |

## Phase 2: Read-Only Skill Migration (v0.2.0) — DONE

Migrate skills that have no hardcoded personal references — straight copy + light cleanup.

| Skill | Source | PR scope | Status |
|---|---|---|---|
| `snowflake-pdf` | `~/.snowflake/cortex/skills/snowflake-pdf/` | Light scrub (Consumers Credit Union and Justin Davis examples) | Migrated |
| `architecture-diagram` | local | Direct migration | Migrated |
| `gong` | local | Direct migration | Migrated |
| `similar-use-cases` | local | Direct migration | Migrated |
| `pptx` (renamed from `CoCo_pptx_Skill`) | local | Folder rename + dropped `~$` Office lock file | Migrated |

Reclassified: `gdrive-desktop` moved from Phase 2 to Phase 3 because it has hardcoded gdrive paths that require sanitization.

Also shipped in v0.2.0: extended `ace-setup` with Q9 (`user_email`) and Q10 (`gdrive_base`) so Phase 3 sanitized skills can read those values from `/memories/ace-setup.md`.

One PR per skill. Each PR:
1. Copies the skill to `skills/<name>/`
2. Runs the public-repo content sweep
3. Updates `skills/README.md` to mark it migrated
4. Smoke-tests the skill works under the profile

## Phase 3: Personal-Data Skill Migration (v0.3.0)

Higher-risk: each skill has hardcoded personal info that must be parameterized.

| Skill | Sanitization |
|---|---|
| `account-context` | Replace connection names, user handles |
| `account-handoff` | Replace personal references, customer names |
| `account-status` | Replace customer account list |
| `account-team` | Generalize team membership data lookup |
| `activity-log` | Replace personal log path with env var |
| `customer-role-hierarchy` | Replace connection names |
| `external-account-context` | Generalize context store |
| `meeting-prep` | Replace personal references |
| `salesforce-account-intel` | Generalize SF auth + connection |
| `todo-log` | Replace personal todo store path |
| `use-case-data` | Replace personal use case ids |
| `use-case-update` | Replace personal use case ids |

Per-skill recipe:
1. Branch in profile repo
2. Copy + sanitize (replace personal values with `${ACE_DEFAULT_CONN}`, `${ACE_USER_HANDLE}`)
3. Document required env vars in skill's SKILL.md
4. Test against your local env (env vars set) — skill behaves identically
5. Public-repo content sweep
6. PR with before/after sanitization summary

## Phase 4: Slash Commands + Examples (v0.4.0)

| Command | Purpose |
|---|---|
| `/start-asset` | Bootstrap a new asset with discipline applied |
| `/multi-review` | Run the full multi-reviewer subagent set on an asset |
| `/public-repo-review` | Run public-repo content sweep on a working tree |
| `/audience-check` | Re-run snowflake-pdf audience workflow on demand |

| Example | Asset type |
|---|---|
| `pdf-setup-guide-skeleton.md` | PDF |
| `pdf-troubleshooting-skeleton.md` | PDF |
| `notebook-analysis-template.ipynb` | Notebook |
| `script-snowflake-utility.sh` | Script |
| `research-decision-doc.md` | Research |

Pre-commit hook for the public-repo content sweep also lands in this phase.

## Phase 5: Second-ACE Onboarding (v1.0.0)

Validate the profile end-to-end with a second ACE installing it cold.

Steps:
1. Pick a volunteer ACE
2. They install via INSTALL.md without help
3. They walk through ace-onboarding.md
4. They produce one PDF and one notebook using the discipline
5. Capture friction in GitHub issues
6. Iterate; ship v1.0.0 when the workflow holds for someone other than the maintainer

## Things Explicitly Out of Scope

| Item | Reason |
|---|---|
| `slack-bridge` skill | Personal phone, personal Slack DMs |
| `bookmanager-ops` skill | Project-specific to one engagement |
| `de-studies` skill | Personal curriculum tracking |
| Customer-specific skills | Stay in customer-specific repos |
| Memory files | Personal context, not generalizable |

## Versioning

| Phase | Version |
|---|---|
| 1: Bootstrap | 0.1.0 |
| 2: Read-only skills | 0.2.0 |
| 3: Personal-data skills | 0.3.0 |
| 4: Commands + examples | 0.4.0 |
| 5: Second-ACE validation | 1.0.0 |

Patch versions (0.x.y) bump for fixes within a phase.

## How to Track

Each phase becomes a GitHub Project / milestone. PRs reference the phase. Status updates land here.
