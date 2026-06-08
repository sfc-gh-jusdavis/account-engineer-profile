---
name: ace-setup
description: First-time and recurring setup workflow for the Account Engineer profile. Captures per-ACE config (primary connection, demo connection, username, demo account details, display name, GitHub handle and org, work email, Google Drive base path) via 11 questions, auto-detecting sensible defaults from `gh`, `snow`, and filesystem inspection. Persists answers to /memories/ace-setup.md and outputs the CCD profile envVar JSON snippet for paste-back. Triggers: ace-setup, /ace-setup, run setup, run profile setup, configure profile, first-time setup, set up account engineer, update my setup, configure ace-setup.
---

# ACE Setup Workflow

This skill collects per-ACE configuration values and persists them so other skills can read them on subsequent sessions. It is safe to run at first install and safe to re-run anytime values change.

## When to Activate

- User explicitly types `/ace-setup`, "run setup", "configure profile", or any of the trigger phrases above
- User asks how to install / configure / set up the Account Engineer profile
- Another skill encounters a missing required value (`ACE_DEFAULT_CONN`, `ACE_USER_HANDLE`, or a demo-account detail) AND `/memories/ace-setup.md` does not exist — in that case, suggest running this skill before proceeding rather than guessing

Do NOT activate this skill on every session-start. Only when a value is needed and unavailable, or when the user asks for it.

## Workflow

### Step 1: Detect prior setup

Read `/memories/ace-setup.md`. Three branches:

| State | Action |
|---|---|
| File exists, all 9 fields populated | This is a re-run. Show the current values in a table. Ask which to update (offer "all" / "specific fields" / "just notes" / "cancel"). |
| File exists, some fields blank or "not set" | Continue from where the prior run left off; only ask the unanswered questions. |
| File does not exist | First-time setup. Ask all 9 questions. |

### Step 2: Auto-detect defaults

Before asking, run these read-only commands to populate sensible defaults the user can confirm rather than type:

```bash
# Default Snowflake connection name (first entry in the user's snow CLI config)
snow connection list --format json 2>/dev/null | head -n 50

# Snowflake current user (if connection works)
snow sql -q "SELECT CURRENT_USER() AS user, CURRENT_REGION() AS region" --format json 2>/dev/null

# GitHub handle (if gh is authenticated)
gh api user --jq '.login' 2>/dev/null

# Work email (auto-detect from gdrive folder name or git config)
ls -d ~/Library/CloudStorage/GoogleDrive-* 2>/dev/null | head -1 | sed 's|.*GoogleDrive-||'  # macOS
git config user.email 2>/dev/null  # fallback

# Google Drive base for activation accounts (auto-detect)
ls -d ~/Library/CloudStorage/GoogleDrive-*/My\ Drive/Current\ Activation\ Accounts 2>/dev/null | head -1

# OS user full name (for display-name suggestion)
osascript -e 'long user name of (system info)' 2>/dev/null   # macOS
getent passwd "$USER" | cut -d: -f5 | cut -d, -f1 2>/dev/null # Linux
```

If a command fails or is unavailable, that question simply has no default — fall back to asking with no pre-filled value.

### Step 3: Ask the 11 questions

Use `ask_user_question`, one question at a time, with `type: "text"` and the auto-detected value as `defaultValue` where available.

| # | Question header | Question | Field | Default source | Notes |
|---|---|---|---|---|---|
| 1 | Connection | What's the name of your primary work Snowflake connection? (e.g. `snowhouse` for internal tooling) | `ACE_DEFAULT_CONN` (envVar) | `snow connection list` first entry | Used for account research, read-only queries, and internal-tool SQL |
| 2 | Demo connection | What's the name of your demo Snowflake connection? (your personal demo account) | `ACE_DEMO_CONN` (envVar) | `snow connection list` second entry if present, otherwise none | Used by demo-ops skills for DDL/DML and deploys; skippable if the ACE doesn't build demos |
| 3 | Username | What's your Snowflake username? | `ACE_USER_HANDLE` (envVar) | `SELECT CURRENT_USER()` from Q1's connection | Drives `TEMP.<USER>` write scope |
| 4 | Demo account | What's your demo account identifier? | `demo_account` (memory) | none | The personal-testing account you use; not your customer's account |
| 5 | Demo region | What region is your demo account in (e.g. AWS_US_WEST_2, AZURE_EAST_US_2)? | `demo_region` (memory) | `SELECT CURRENT_REGION()` from Q2's connection if set | Used in PDF metadata and skill defaults |
| 6 | DDL warehouse | What warehouse do you use for DDL/DML in your demo account? | `ddl_warehouse` (memory) | `SE_XS_WH` | Skills suggest this for writes; the system prompt forbids DDL on `SNOWADHOC` |
| 7 | Display name | What's your name as it should appear on customer-facing PDF cover pages? | `ace_display_name` (memory) | OS full name | Used in PDF metadata, briefing authorship, deck cover slides |
| 8 | GitHub handle | What's your GitHub handle? Used when you fork this profile, create project repos for customer engagements, or work with GitHub-based assets in skills | `github_handle` (memory) | `gh api user --jq .login` | If the ACE genuinely doesn't use GitHub, accept "skip" — but flag that fork/project workflows will require it later |
| 9 | GitHub org | What GitHub org do you create project repos under? (Often the same as your handle for personal namespace; sometimes a team org like `sfc-gh-team-x`) | `github_org` (memory) | same as Q8 answer | Skip if Q8 was skipped |
| 10 | Work email | What's your work email address? | `user_email` (memory) | parsed from `~/Library/CloudStorage/GoogleDrive-*` folder name; falls back to `git config user.email` | Used in path conventions and document metadata across many skills |
| 11 | Drive base | What's the absolute path to your activation-accounts Google Drive folder? | `gdrive_base` (memory) | `~/Library/CloudStorage/GoogleDrive-<email>/My Drive/Current Activation Accounts` if exactly one match | Used by gdrive-desktop, account-context, account-handoff, meeting-prep, salesforce-account-intel, use-case-data, use-case-update, activity-log, todo-log, external-account-context |

If Q2 is skipped, still auto-detect region from Q1's connection for Q5 if possible.
If Q8 is skipped, skip Q9 automatically; don't make the user click through it.

If the auto-detect for Q10 or Q11 returns multiple matches, present them as options and let the user pick.

### Step 4: Persist to memory

Use the `memory` tool to write `/memories/ace-setup.md` following the canonical format in [setup-template.md](setup-template.md). If a "Notes" section existed in a prior memory file, preserve it.

### Step 5: Output the envVar JSON snippet

Print this for the user to paste into their CCD profile envVars (form -> JSON tab -> envVars object):

```json
"envVars": {
  "ACE_DEFAULT_CONN": "<answer to Q1>",
  "ACE_DEMO_CONN": "<answer to Q2, or omit if skipped>",
  "ACE_USER_HANDLE": "<answer to Q3>"
}
```

Tell the user explicitly: "Open the CCD profile picker -> Edit Account Engineer -> JSON tab -> set the `envVars` object to the above. Save. The next chat session will pick up the new values."

### Step 6: Suggest a smoke test

After setup completes, suggest:

> Try a smoke test: in a fresh chat, type "draft a notebook for analyzing account churn".
>
> Expected behavior: the agent surfaces clarifying questions (audience, dataset, success criterion) before writing any cells. That confirms the asset-creation-discipline skill is active.

### Step 7: Confirm

Show the user a summary of what was written:

```
ACE Setup complete:
- Connection: <value>
- Demo connection: <value, or "not set">
- Username: <value>
- Demo account: <value> in <region>
- DDL warehouse: <value>
- Display name: <value>
- GitHub: <handle>/<org>

Memory file: /memories/ace-setup.md
Profile envVars to update: ACE_DEFAULT_CONN, ACE_DEMO_CONN, ACE_USER_HANDLE
```

## Anti-Patterns to Avoid

- **Don't guess values silently.** If `gh` is unauthenticated, ask the user — don't fabricate a handle.
- **Don't ignore "skip".** If the user says skip on Q2 or Q8, respect it. Don't badger.
- **Don't auto-trigger on session start.** Only run when explicitly invoked or when another skill genuinely needs a value.
- **Don't write to memory until all questions are answered or the user explicitly cancels.** Partial state is fine to persist; partial silently-defaulted state is not.
- **Don't ask about secrets.** Connection auth (PATs, passwords) belongs in `~/.snowflake/config.toml`, not memory. The skill captures the connection NAME, not credentials.

## Re-Run Behavior

When the user invokes the skill and `/memories/ace-setup.md` exists:

1. Print the current values
2. Offer four paths:
   - **Update all fields** (re-ask all 9)
   - **Update specific fields** (ask which, then ask only those)
   - **Update notes only** (skip questions, just open the Notes section for editing)
   - **Cancel** (do nothing, exit)

Always preserve fields the user did not explicitly update.

## Files

- [SKILL.md](SKILL.md) - this file
- [workflow.md](workflow.md) - detailed prose walkthrough of each question
- [setup-template.md](setup-template.md) - canonical format for `/memories/ace-setup.md` other skills can read

## Composes With

- **system-prompt.md** references this skill from its "First-Run Setup" section. When the agent encounters a missing ACE-specific value, it suggests running this skill rather than guessing.
- **Any skill that needs `ACE_DEFAULT_CONN` / `ACE_USER_HANDLE`** reads them from profile envVars (not from memory). This skill produces the values the ACE pastes into envVars.
- **Any skill that needs demo-account details, display name, or GitHub handle/org** reads them from `/memories/ace-setup.md` directly.
