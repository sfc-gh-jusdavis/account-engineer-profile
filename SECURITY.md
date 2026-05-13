# Security Policy

## Reporting Concerns

This is a public repository for a Snowflake-internal Cortex Code profile. If you discover content that violates the policies below, open a GitHub issue tagged `security` (or contact the maintainer directly if the content involves credentials).

## Forbidden Content

This repository must never contain:

- **Secrets:** PATs, passwords, API keys, OAuth client secrets, signed JWTs, connection strings with embedded credentials
- **Customer data:** customer names, account IDs, ARR / forecast data, MEDDPICC fields, deal context, Salesforce records, Gong call transcripts
- **Personally Identifiable Information:** email addresses outside contributor commit metadata, phone numbers, home addresses
- **Internal Snowflake URLs:** `go/`, `*.atlassian.net`, `snowflake.slack.com`, `quip.com`, internal dashboards, Confluence pages
- **Internal-only product code names** that have not been announced publicly
- **Personal connection names** (use `${ACE_DEFAULT_CONN}` placeholder)
- **Personal usernames** in skill code (use `${ACE_USER_HANDLE}` placeholder)

## Pre-Commit Checks (Manual for Now)

Before pushing, run:

```bash
# Personal handle / connection leaks
grep -ri 'JDAVIS_AWS1\|JUSDAVIS\|j\.davis\|j_davis' . --exclude-dir=.git

# Internal URL leaks
grep -ri 'atlassian\.net\|snowflake\.slack\.com\|quip\.com\|^go/' . --exclude-dir=.git

# Common secret patterns
grep -riE 'password\s*=\s*["\x27]|api[_-]?key\s*=\s*["\x27]|secret\s*=\s*["\x27]' . --exclude-dir=.git
```

All three must return zero hits.

## What to Do If You Accidentally Commit a Secret

1. **Rotate the secret immediately** — assume it is public the moment it lands in a public commit.
2. Open a GitHub issue tagged `security`.
3. Do NOT just delete the file in a follow-up commit — the secret remains in git history forever.
4. Coordinate with the maintainer to either:
   - Force-rewrite history (only viable if no one has cloned the bad commit)
   - Accept that the secret is burned and document the rotation

## Scope

The maintainer's response time is best-effort. This is a side-project profile, not a supported product. For Snowflake product security issues, report via Snowflake's official security channels.
