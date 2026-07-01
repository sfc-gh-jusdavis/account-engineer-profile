---
name: refresh-profile
description: "Refresh the Account Engineer profile so CoCo Desktop picks up new or updated skills that were pushed to the profile's GitHub repo. Runs ALTER GIT REPOSITORY ... FETCH on the Snowflake-backed profile repo, then tells the user to restart CoCo to reload. Use when: user wants to pull the latest ACE skills after a GitHub push. Triggers: refresh my ace profile, refresh ace profile, refresh profile, update my ace profile, update ace skills, sync ace profile, pull latest ace skills, my ace skills are out of date, update account engineer profile."
---

# Refresh ACE Profile

Pulls the latest Account Engineer profile skills from GitHub into your local CoCo Desktop.

## Why this is needed

CoCo Desktop does **not** read GitHub directly. The profile's `skillRepos` points at a Snowflake stage backed by a Snowflake Git Repository:

```
@ACCOUNT_ENGINEERING.COCO.AE_PROFILE_REPO/branches/main/skills/
```

That stage serves a **cached snapshot** of the GitHub repo. A push to GitHub does not reach your desktop until:

1. The Snowflake Git Repository is told to `FETCH` the latest commits, **and**
2. CoCo re-reads the stage — which happens when you start a new session / restart.

This skill automates step 1 and reminds you to do step 2.

## Fixed values

| Value | Setting |
|---|---|
| Git Repository | `ACCOUNT_ENGINEERING.COCO.AE_PROFILE_REPO` |
| Connection | `${ACE_DEFAULT_CONN}` profile envVar (the internal Snowhouse connection) |
| Branch | `main` |

If `ACE_DEFAULT_CONN` is not set, ask the user which connection reaches Snowhouse (or point them at the `ace-setup` skill), then proceed.

## Workflow

### Step 1: Fetch the latest commits

Run this on the `${ACE_DEFAULT_CONN}` connection using `snowflake_sql_execute` (pass `connection` = the env var value):

```sql
ALTER GIT REPOSITORY ACCOUNT_ENGINEERING.COCO.AE_PROFILE_REPO FETCH;
```

**If this fails with an insufficient-privileges error:** the shared repo is owned by `ACCOUNT_ENGINEERING_ADMIN_RL`, so only profile maintainers can `FETCH`. Tell the user:
> Only a profile maintainer can fetch the shared repo. If a maintainer has already fetched, just restart CoCo (Step 3) — the stage snapshot is already current. Otherwise ping the profile maintainer to run the FETCH.

Do not treat a privilege error as a hard failure — route the user to the restart step.

### Step 2: Confirm the new skills landed

List the skills currently on the stage so the user can see what will load:

```sql
LS @ACCOUNT_ENGINEERING.COCO.AE_PROFILE_REPO/branches/main/skills/;
```

Summarize the result (e.g. "14 skills on the stage, including the new `<name>`"). If the user expected a specific new skill, confirm its directory is present.

### Step 3: Tell the user to restart CoCo

The FETCH updates the Snowflake-side snapshot, but your **running** CoCo session still holds the old skill set (and a local stage cache). Instruct clearly:

> Fetched. Now **start a new CoCo chat session / restart CoCo Desktop** to load the refreshed skills. The current session keeps the old set until then.

## Output

Report back concisely:
- Whether the FETCH succeeded (or was skipped due to privileges)
- The skill count / any newly present skills from the `LS`
- The restart reminder

## Anti-Patterns to Avoid

- **Don't run DDL on the wrong connection.** The git repo lives in Snowhouse; always use `${ACE_DEFAULT_CONN}`, never a demo connection.
- **Don't claim skills are live after only FETCH.** FETCH updates the stage snapshot; the running session still needs a restart to pick them up.
- **Don't hard-fail on privilege errors.** Consumers without ALTER on the repo can still get current skills after a maintainer fetches — send them to the restart step.
- **Don't edit skill files here.** This skill only refreshes; authoring/pushing skills is a separate maintainer workflow (edit local clone → `git push` → then run this).

## Composes With

- **ace-setup** — supplies `ACE_DEFAULT_CONN`. If it's missing, suggest running `ace-setup` first.
