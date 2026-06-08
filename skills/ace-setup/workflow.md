# ACE Setup Workflow — Detailed Walkthrough

This document is the long-form companion to [SKILL.md](SKILL.md). It explains each question in depth, what value it drives, what to do if the ACE doesn't know an answer, and how the skill handles partial / repeated runs.

Read this if you are an agent invoking the skill or a human ACE confused about why a question is being asked.

---

## Pre-Flight: Auto-Detection

Before asking any questions, the skill runs a few read-only commands to populate sensible defaults. Each is wrapped to fail silently — if the underlying CLI isn't available or isn't authenticated, the question simply has no default.

### Default Snowflake connection name

```bash
snow connection list --format json 2>/dev/null
```

This returns the user's `~/.snowflake/config.toml` connection entries. The skill picks the first one as the default. If the user has multiple connections, they confirm or override.

### Snowflake username + region

```bash
snow sql -c "<chosen-connection>" -q "SELECT CURRENT_USER() AS user, CURRENT_REGION() AS region" --format json 2>/dev/null
```

Run AFTER the connection name is confirmed (Q1). Populates Q2 and Q4 defaults.

### GitHub handle

```bash
gh api user --jq '.login' 2>/dev/null
```

Requires `gh` CLI authenticated. Populates Q7 default. If unauthenticated, the question has no default and the skill notes that the user can run `gh auth login` first if they want auto-detection.

### OS full name (for display name)

```bash
# macOS
osascript -e 'long user name of (system info)' 2>/dev/null

# Linux
getent passwd "$USER" | cut -d: -f5 | cut -d, -f1 2>/dev/null
```

Populates Q6 default. The user almost always wants a different value (e.g., "Jane Doe" instead of "jane.doe"), but the auto-detected name is a useful starting point.

---

## The 8 Questions

### Q1: Connection name

**Asked:** "What's the name of your Snowflake connection?"

**Drives:** `ACE_DEFAULT_CONN` env var. Every skill that runs SQL uses this.

**Format:** A string matching one of the connection names in `~/.snowflake/config.toml`. Case-sensitive.

**If the ACE doesn't know:**

> Run `snow connection list` in your terminal. The output shows configured connections. Pick your primary work connection (e.g. `snowhouse` for internal Snowflake tooling). If you don't have one configured yet, run `snow connection add` and come back.

**Common pitfalls:**
- Connection names in Snowflake's CLI are case-sensitive
- A connection name and an account identifier are different things — the connection name is your local alias, the account identifier is the Snowflake-side name

### Q2: Demo connection name

**Asked:** "What's the name of your demo Snowflake connection?"

**Drives:** `ACE_DEMO_CONN` env var. All demo-ops skills use this when running SQL, deploying assets, or creating DDL in your personal demo org.

**Format:** A string matching a connection name in `~/.snowflake/config.toml`. Case-sensitive.

**Default:** auto-detected as the second entry in `snow connection list` (after the primary work connection); or no default if only one connection exists.

**If the ACE doesn't have a demo connection:**

> Run `snow connection add` to configure one, then re-run `/ace-setup`. You can also skip this for now — the demo-ops skills will fall back to asking each session.

**Can this be skipped?** Yes — if the ACE does only read-only work and never builds demos. Type "skip" to leave `ACE_DEMO_CONN` unset.

**Common pitfalls:**
- Don't use the same value as Q1. If you only have one connection, you likely need to add a second one pointing at your demo org.
- The demo connection account and the primary work connection account are different Snowflake accounts — the primary is typically `snowhouse` (Snowflake internal), the demo is your personal/SE-owned Snowflake account.

### Q2 (former): Snowflake username

**Asked:** "What's your Snowflake username?"

**Drives:** `ACE_USER_HANDLE` env var. Used to scope writes to `TEMP.<USER>` schema. Used in PDF metadata in some skills.

**Format:** Bare username, no domain. Case-sensitive on the Snowflake side; convention is uppercase.

**If the ACE doesn't know:**

> Run `snow sql -c <your-connection> -q "SELECT CURRENT_USER()"`. The result is your username.

**Common pitfalls:**
- Don't confuse username with email — Snowflake usernames are typically `JANE_DOE` or `jane.doe@company.com` depending on auth config; both work but they're different
- Lowercase / uppercase matters for some systems; default to what `CURRENT_USER()` returns

### Q3: Demo account identifier

**Asked:** "What's your demo account identifier?"

**Drives:** Documentation context, PDF cover-page metadata. NOT used as a connection target — that's Q1.

**Format:** Either the org-account form (`MY_ORG.MY_ACCOUNT`) or the legacy locator form (`xy12345.us-east-1`). Whichever your account team uses internally.

**Why we ask:**
- ACE-generated PDFs and runbooks often reference "your demo account" — without this value, skills have to either ask each time or use generic placeholders
- This is YOUR personal-test account. Customer accounts are entered per-engagement, not in setup.

**If the ACE doesn't know:**

> Run `snow sql -c <conn> -q "SELECT CURRENT_ACCOUNT_NAME(), CURRENT_REGION()"`. The first column is the account name in legacy locator form. For org-account form, run `SELECT CURRENT_ORGANIZATION_NAME() || '.' || CURRENT_ACCOUNT_NAME()`.

### Q4: Demo region

**Asked:** "What region is your demo account in?"

**Drives:** Documentation context, region-specific URL construction in some skills.

**Format:** Snowflake region label (e.g., `AWS_US_WEST_2`, `AZURE_EAST_US_2`, `GCP_US_CENTRAL1`).

**If the ACE doesn't know:**

> Run `snow sql -c <conn> -q "SELECT CURRENT_REGION()"`. Returns the region in the format Snowflake uses internally.

### Q5: DDL/DML warehouse

**Asked:** "What warehouse do you use for DDL/DML in your demo account?"

**Drives:** Default warehouse skills use when generating DDL or DML. The system prompt forbids `SNOWADHOC` for writes; this question captures what the ACE uses instead.

**Format:** A warehouse name. Case-sensitive on Snowflake's side; convention is uppercase.

**Default suggestion:** `SE_XS_WH` (a common ACE default). If your account doesn't have that warehouse, override with one you do have.

**If the ACE doesn't know:**

> Run `snow sql -c <conn> -q "SHOW WAREHOUSES"` and pick a small warehouse you have USAGE on. If you don't have any, you'll need to either create one or get one granted before DDL/DML skills will work.

**Common pitfalls:**
- Granted USAGE doesn't mean granted MODIFY. Some ACEs have read-only access to warehouses. Confirm you can actually run DDL with the chosen warehouse.

### Q6: Display name

**Asked:** "What's your name as it should appear on customer-facing PDF cover pages?"

**Drives:** PDF metadata in `snowflake-pdf` skill (Phase 2), briefing authorship, deck cover slides.

**Format:** A human-readable name. "Jane Doe" not "jane.doe".

**Default:** auto-detected from OS user info — usually correct, sometimes needs minor cleanup ("J Doe" vs "Jane Doe").

### Q7: GitHub handle

**Asked:** "What's your GitHub handle? Used when you fork this profile, create project repos for customer engagements, or work with GitHub-based assets in skills."

**Drives:**
- URL construction when forking the profile (`github.com/<handle>/account-engineer-profile`)
- Default owner when skills create new repos for customer engagements
- Author tag in CONTRIBUTING-style metadata

**Format:** Bare GitHub username (no `@`, no URL).

**Default:** auto-detected via `gh api user --jq .login`.

**If the ACE doesn't use GitHub:**

> If you genuinely don't use GitHub for ACE work, type "skip". Be aware that fork workflows and project-repo skills will prompt you for the handle each time they need it. You can re-run `/ace-setup` later to add it.

**Common pitfalls:**
- GitHub Enterprise accounts use the same handle as github.com if SSO'd. If you have separate accounts, use the one tied to ACE work (typically the `sfc-gh-*` enterprise handle).

### Q8: GitHub org

**Asked:** "What GitHub org do you create project repos under?"

**Drives:**
- Default `org` parameter when skills create new repos
- URL construction for project-repo skills

**Format:** Bare org slug. Often the same as the user's GitHub handle (for personal-namespace repos), sometimes a team org.

**Default:** Same as Q7's answer (personal namespace).

**Skip behavior:** If Q7 was skipped, Q8 is skipped automatically.

**Common pitfalls:**
- The org and the handle are different things in GitHub. Repos under your handle are personal; repos under an org are owned by that org. Make sure you have create-repo rights on whatever org you specify.

### Q9: Work email

**Asked:** "What's your work email address?"

**Drives:**
- Path conventions in skills that reference Google Drive (the gdrive folder name embeds the email)
- Document metadata (author email in some PDF / handoff outputs)
- Default fallback for git commit author identity in workflows that auto-create repos

**Format:** Full email address.

**Default:** auto-detected by parsing `~/Library/CloudStorage/GoogleDrive-<email>` folder name; falls back to `git config user.email`.

**Common pitfalls:**
- If you have multiple Google accounts mounted via Drive desktop, multiple folders exist. The skill presents them as options if more than one match exists.
- Personal vs work email matters here — use the work email tied to your Snowflake-internal Google Drive.

### Q10: Google Drive base path

**Asked:** "What's the absolute path to your activation-accounts Google Drive folder?"

**Drives:**
- The base path many skills append to when looking up customer engagement folders
- The "where do logs live" anchor for `activity-log` and `todo-log`
- Where `account-context`, `account-handoff`, `meeting-prep`, `external-account-context`, `salesforce-account-intel`, `use-case-data`, `use-case-update` look for per-customer files

**Format:** Absolute path. On macOS this is typically:
`/Users/<you>/Library/CloudStorage/GoogleDrive-<email>/My Drive/Current Activation Accounts`

**Default:** auto-detected via `ls -d ~/Library/CloudStorage/GoogleDrive-*/My\ Drive/Current\ Activation\ Accounts` — if exactly one match, use it.

**If the ACE doesn't have this folder structure:**

> Some teams use a different folder organization (per-quarter, per-business-unit, etc.). Type the path that's the equivalent of "where customer engagement folders live for me." Skills that depend on this can be re-pointed by re-running `/ace-setup` later.

**Common pitfalls:**
- Trailing slash matters less than you'd think — most skills handle either form. Default to no trailing slash.
- Spaces in the path require quoting when used in shell commands; the skills that need this path quote it correctly.

---

## Persistence

After all questions are answered, the skill writes `/memories/ace-setup.md` using the canonical format in [setup-template.md](setup-template.md).

The memory file is the source of truth for everything except `ACE_DEFAULT_CONN`, `ACE_DEMO_CONN`, and `ACE_USER_HANDLE`, which are also (and primarily) read from CCD profile envVars at runtime.

---

## Re-Run Logic

When the skill is invoked and `/memories/ace-setup.md` already exists:

1. Read the file
2. Display current values in a table
3. Ask which fields to update via `ask_user_question` with options:
   - "Update all fields" (re-asks all 9)
   - "Update specific fields" (asks WHICH fields, then asks only those)
   - "Update notes only" (skips questions, opens Notes section for editing)
   - "Cancel" (exits without changes)
4. For "Update specific fields", present a multi-select list of the 8 fields plus "notes". Ask each selected field's question with the current value as the default.
5. Re-write the memory file, preserving all unchanged fields including Notes.
6. Re-print the envVar JSON snippet (only if Q1 or Q2 changed).

---

## Edge Cases

| Situation | Behavior |
|---|---|
| User cancels mid-flow | Don't write anything to memory. Existing file (if any) untouched. |
| User says "skip" on a non-skippable question (Q1 or Q3) | Politely refuse: explain that connection name and username are required for the profile to function. Re-ask. (Q2 demo connection IS skippable.) |
| Auto-detect command fails | The question has no default. Ask without one. Don't error. |
| `snow` CLI not installed | Skip auto-detection for Q1, Q2, Q4, Q5. Ask manually. |
| `gh` CLI not installed or not authed | Skip auto-detection for Q7. Ask manually. |
| Memory file is corrupted (not valid markdown) | Treat as "doesn't exist" — start fresh. |
| User runs setup but never pastes envVars into CCD | Memory persists; profile envVars stay default placeholders. Skills that need `ACE_DEFAULT_CONN` will fall through to "ask the user" because the env var is unset. The skill should remind the user at completion to paste the JSON. |

---

## What This Skill Does NOT Do

- Does NOT modify CCD profile envVars directly. CCD doesn't expose a write API for those; the user pastes the JSON manually.
- Does NOT modify `~/.snowflake/config.toml`. The skill captures the connection NAME but doesn't create or edit connections.
- Does NOT validate that the connection actually works. If Q1's value points at a non-existent connection, that's a Snowflake CLI problem the user discovers when they next run a SQL skill.
- Does NOT collect customer data. Customer accounts and engagement context are entered per-engagement, never in setup.
- Does NOT collect secrets. PATs, passwords, OAuth tokens belong in the user's secret store, not in `/memories/ace-setup.md`.

---

## How Other Skills Read These Values

| Value | How another skill reads it |
|---|---|
| Connection name | `os.environ.get("ACE_DEFAULT_CONN")` (Python) or `$ACE_DEFAULT_CONN` (shell) |
| Demo connection name | `os.environ.get("ACE_DEMO_CONN")` (Python) or `$ACE_DEMO_CONN` (shell) |
| Username | `os.environ.get("ACE_USER_HANDLE")` |
| Demo account, region, DDL warehouse, display name, GitHub handle/org | Read `/memories/ace-setup.md` and parse the relevant section |

If a skill needs a value not yet captured (e.g., the ACE's preferred chart color palette), the skill author either:
- Adds a question to this workflow (PR), OR
- Asks the ACE inline and persists to `/memories/<feature>.md` as a separate memory file

The setup skill is the canonical place for **profile-wide** ACE config. Skill-specific config can live in skill-specific memory files.
