# Public Repo Policy

This repository is **public**. Anyone on the internet can read every commit forever, including content removed by later commits (git history retains it). This document is the contract: what can appear here, what cannot, and how to verify before pushing.

---

## What Cannot Appear

### Customer information

- Customer company names (real, abbreviated, or codenamed)
- Customer Salesforce account IDs
- Customer-specific configuration values (account IDs, region codes, deployment names)
- ARR, TCV, ACV, forecast figures, deal stage, MEDDPICC fields
- Anything sourced from Salesforce, Gong, or Snowflake's internal CRM

### Snowflake-internal URLs

- `go/` shortlinks
- `*.atlassian.net` (Confluence, Jira)
- `snowflake.slack.com`, internal Slack message links, channel-name URLs
- `quip.com`
- Internal dashboards, internal observability tools
- Internal-only GitHub Enterprise repos

### Snowflake-internal-only content

- Product code names not announced publicly
- Internal team / org names below department level (specific squad names, etc.)
- Internal escalation paths
- Internal-only acronyms (TAM/SE/FE/AE/SA in code samples — fine in prose explaining ACE roles, not fine in skill code that other roles might run)

### Personal data

- Personal email addresses (other than commit author metadata)
- Personal phone numbers
- Personal Slack DM histories
- Personal home/work addresses

### Personal connection / identity values

- `JDAVIS_AWS1`, `JUSDAVIS`, `j.davis`, `j_davis` — replace with `${ACE_DEFAULT_CONN}` and `${ACE_USER_HANDLE}` placeholders
- Any individual user's connection-config values
- Any individual user's PAT
- Any individual user's API tokens

### Secrets — never, ever

- PATs, passwords, API keys, OAuth client secrets, signed JWTs
- Connection strings with embedded credentials
- Private SSH keys, GPG private keys, certificates with private material
- Database connection strings

### Project-specific content

- BookManager-specific paths, schemas, table names
- Other internal-project specifics that don't generalize

---

## What CAN Appear

For clarity, here's what is fine:

- Public Snowflake documentation links (`docs.snowflake.com`)
- Public community links (`community.snowflake.com`)
- Generic Snowflake feature names that are publicly announced
- Generic ACE workflow descriptions that don't tie to specific accounts
- Placeholder examples: `<example-customer>`, `<your-connection-name>`, `<account_id>`
- Code examples using public-doc field names and public-API patterns
- Open-source dependency references (Apache 2.0, MIT, etc.)
- Apache 2.0 boilerplate, standard CoC, standard SECURITY.md

---

## Pre-Push Verification

Before pushing any branch, run these greps from the repo root:

```bash
# Personal handles / connection leaks
grep -ri 'JDAVIS_AWS1\|JUSDAVIS\|j\.davis\|j_davis' . --exclude-dir=.git
grep -ri 'BookManager\|bkmng' . --exclude-dir=.git

# Internal Snowflake URLs
grep -ri 'atlassian\.net\|snowflake\.slack\.com\|quip\.com' . --exclude-dir=.git
grep -ri '^go/\|[^a-zA-Z]go/' . --exclude-dir=.git

# Common secret patterns
grep -riE 'password\s*=\s*["\x27][^"\x27<]+["\x27]' . --exclude-dir=.git
grep -riE 'api[_-]?key\s*=\s*["\x27][^"\x27<]+["\x27]' . --exclude-dir=.git
grep -riE 'token\s*=\s*["\x27][a-zA-Z0-9]{20,}["\x27]' . --exclude-dir=.git

# PAT patterns
grep -riE 'gho_[a-zA-Z0-9]{20,}|ghp_[a-zA-Z0-9]{20,}' . --exclude-dir=.git
```

All of these must return zero hits.

A future Phase 4 work item is to encode this as a pre-commit hook so the check runs automatically. For now, contributors run it manually.

---

## Sanitization Patterns for Migrated Skills

When migrating a skill from a personal CCD instance into this repo:

| Personal value | Replace with |
|---|---|
| Specific connection name (e.g. `MY_CONN`) | `${ACE_DEFAULT_CONN}` env var reference |
| Specific username | `${ACE_USER_HANDLE}` env var reference |
| Specific email | Reader's responsibility to configure; document in skill SKILL.md |
| Customer account name | `<example-customer>` in prose, omit from code |
| Specific Salesforce ID | `<account_id>` placeholder |
| Hardcoded local path | Document as "user configures" in SKILL.md; never ship hardcoded |
| Specific GitHub repo | Either keep if public + relevant, or replace with `<your-repo>` placeholder |

---

## What to Do After Accidentally Committing Forbidden Content

1. **If a secret was committed:** rotate it immediately. Treat it as compromised the moment the commit landed in the public repo.
2. **Open a GitHub issue** tagged `security`.
3. **Do not just delete the file in a follow-up commit.** Git history retains the original. The content is still public.
4. **Coordinate with the maintainer:**
   - If no one has cloned the repo since the bad commit: a force-push history rewrite may be viable
   - Otherwise: accept that the content is public, document the rotation, and improve the pre-commit gates so it does not happen again
5. **Update this policy** if the incident reveals a category of content not currently flagged.

---

## Why a Public Repo

The CCD profile mechanism reads from Git URLs. Internal Git hosting would require additional auth setup for every ACE installing the profile. A public GitHub repo with strict content hygiene is the lowest-friction distribution path. The tradeoff is that the content discipline must be tight from commit one — which is what this document is for.
