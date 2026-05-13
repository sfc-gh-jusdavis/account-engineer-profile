# Commands

CCD slash commands the Account Engineer profile registers.

## v0.1.0 Status

This directory is a placeholder in v0.1.0. Slash commands land in **Phase 4** of the rollout.

## Planned Commands (Phase 4)

| Command | Purpose |
|---|---|
| `/start-asset` | Bootstrap a new asset with the asset-creation-discipline applied. Prompts for asset type, asks the assumption-surfacing questions, then drafts the matching skeleton. |
| `/multi-review` | Run the full multi-reviewer subagent set on an asset. Picks the reviewer set based on asset type, runs in parallel, consolidates findings. |
| `/public-repo-review` | Run the public-repo content sweep on a working tree. Greps for connection names, customer names, internal URLs, secret patterns. Reports findings before commit. |
| `/audience-check` | Re-run the snowflake-pdf audience workflow on demand (after the snowflake-pdf skill is migrated in Phase 2). |

## Adding a Command

See [../CONTRIBUTING.md](../CONTRIBUTING.md). Briefly:

1. Create `commands/<command-name>.md` with YAML front-matter:
   ```markdown
   ---
   name: command-name
   description: One-line description that appears in the slash-command picker
   ---

   <prompt content the agent receives when invoked>
   ```
2. Update this README to list the command
3. Test locally before opening the PR

## Why Empty in v0.1.0

The discipline layer (asset-creation-discipline skill) and system prompt cover the most important workflows. Slash commands are syntactic sugar — useful but not foundational. Phase 4 picks them up once the skill set is mature.
