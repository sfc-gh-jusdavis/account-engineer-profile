# ACE Onboarding

Welcome. You've installed the Account Engineer profile in Cortex Code Desktop. This page is a 15-minute walkthrough to get you productive.

## Prerequisites Check

Before starting:

- [ ] Cortex Code Desktop is installed and authenticated
- [ ] At least one Snowflake connection is configured locally (verify with `snow connection list`)
- [ ] The Account Engineer profile shows in your CCD profile picker
- [ ] You've set the env vars `ACE_DEFAULT_CONN`, `ACE_DEMO_CONN`, and `ACE_USER_HANDLE` either on the profile or in your shell

## Step 1: Switch to the Profile

Open the profile picker. Select **Account Engineer**. The system prompt loads on your next chat.

## Step 2: Run First-Time Setup

In your first chat under the new profile, type:

> /ace-setup

The skill walks you through 8 questions and produces:

- A populated `/memories/ace-setup.md` file (your demo account, demo connection, display name, GitHub identity)
- A JSON snippet to paste into your CCD profile envVars (your `ACE_DEFAULT_CONN`, `ACE_DEMO_CONN`, and `ACE_USER_HANDLE` values)

Where it can, the skill auto-detects sensible defaults from `snow connection list`, `gh api user`, and your OS user info — you mostly confirm rather than type.

After running setup, paste the printed envVar JSON into the CCD profile picker (Edit Account Engineer -> JSON tab -> set `envVars`). Save.

Re-run `/ace-setup` anytime your demo account changes, you switch teams, or you want to update your display name. The skill preserves any free-form notes across re-runs.

## Step 4: Read the Discipline Layers

Spend 10 minutes on these two documents — they govern how the agent behaves when you ask it to create things:

1. [karpathy-coding-principles.md](karpathy-coding-principles.md) — four principles for individual changes
2. [ai-dev-patterns.md](ai-dev-patterns.md) — workflow patterns for multi-step / multi-agent work

You don't need to memorize them. You need to recognize when the agent is applying them and when it isn't.

## Step 5: Read the Profile's Specific Defaults

Skim [system-prompt.md](../system-prompt.md). The key defaults to internalize:

- The agent verifies Snowflake feature syntax against `snowflake_product_docs` before suggesting it
- Writes are scoped to `TEMP.<USER>` schema unless you give explicit permission for elsewhere
- `SNOWADHOC` is SELECT-only; the agent will refuse DDL/DML on it
- Salesforce is read-only by default

## Step 6: Try the Asset Creation Discipline

In a fresh chat, try:

> "Help me draft a notebook to analyze use case progress for an account."

Expected agent behavior:

1. Agent surfaces clarifying questions: which account? what columns matter? what's the success criterion? what audience?
2. Agent doesn't write any cells until you've answered the questions
3. Agent proposes the smallest notebook that meets the criterion
4. For non-trivial asks, the agent suggests spawning specialized reviewers

If the agent jumps straight to writing cells, the skill is not active — open an issue.

## Step 7: Try a Customer-Facing PDF Workflow (Phase 2 once snowflake-pdf is migrated)

In v0.1.0 the snowflake-pdf skill is not yet in the profile. Continue using your local installation. Phase 2 will move it here.

## Step 8: Set Up Your Personal Layer

Things that DO NOT belong in this profile but you'll want locally:

- Memory files for customer context (use the memory tool in CCD)
- Project-specific repos (create one per customer engagement / per internal project)
- Personal slack-bridge or notification skills
- Personal scratch directories

Keep these in your home dir or in repos you own. The profile is the role baseline.

## Step 9: Provide Feedback

This profile is at v0.1.0 and the v1 audience is just the maintainer. If you're a second-or-later ACE installing it:

- Open issues for anything confusing
- Open PRs for fixes (passing the [public-repo-policy.md](public-repo-policy.md) gate)
- Suggest skills to migrate next via discussion threads

## What's Next

| Phase | What you can expect |
|---|---|
| 2 | snowflake-pdf, architecture-diagram, gdrive-desktop, gong, similar-use-cases, pptx skills land |
| 3 | account-context, account-handoff, meeting-prep, salesforce-account-intel, use-case-data, use-case-update skills land (sanitized) |
| 4 | Slash commands: `/start-asset`, `/multi-review`, `/public-repo-review` |
| 5 | Onboarding refinements based on second-ACE feedback |

Until those phases land, your personal CCD setup remains your primary toolkit. The profile narrows defaults and adds the discipline layer on top.

## Common Issues

| Symptom | Likely cause | Fix |
|---|---|---|
| Agent ignores `snowflake_product_docs` rule | Profile not active | Confirm profile picker shows "Account Engineer" |
| Agent jumps to writing cells without surfacing assumptions | asset-creation-discipline skill not loaded | Re-save profile in CCD form to refresh skill repos |
| Agent writes to a non-TEMP schema | system-prompt.md not loaded | Verify `_systemPromptUrl` in the profile JSON points at the correct file |
| `${ACE_DEFAULT_CONN}` literal appears instead of expanded | env var not set | Set on profile via JSON `envVars` or in `~/.zshrc` |
| `${ACE_DEMO_CONN}` literal appears instead of expanded | env var not set | Set on profile via JSON `envVars` or in `~/.zshrc`; run `/ace-setup` Q2 if skipped earlier |
| Skill repo update doesn't propagate | CCD cached the old version | Edit profile, re-save, restart CCD session |

## Get in Touch

Open a GitHub issue. Profile maintenance is best-effort while the profile is in v0.1.0.
