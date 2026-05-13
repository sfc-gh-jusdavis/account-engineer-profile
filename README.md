# Account Engineer

A Cortex Code profile for Snowflake Account Engineers.

> **Status:** v0.1.0 — bootstrap. Phase 1 of a phased rollout. v1 audience: profile owner only.

## What This Is

This repository is a [Cortex Code Desktop](https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code) profile that bundles:

- A system prompt tuned for Account Engineer (ACE) work
- An "asset creation discipline" skill that applies coding-grade rigor to PDFs, notebooks, scripts, and research/design tasks
- (Coming in later phases) A library of account-workflow skills migrated from individual ACE workstations

## Who This Is For

Snowflake Account Engineers using Cortex Code Desktop. The profile assumes:

- You have CCD installed and authenticated
- You have at least one Snowflake connection configured locally
- You operate as a field engineer on customer accounts

The repository is public so it can be linked from CCD's profile form, but the workflows it implements are Snowflake-internal.

## What Makes This Different from Default CCD

Default CCD is a general-purpose code agent. This profile narrows it toward ACE work:

- **Asset creation discipline:** before drafting a PDF / notebook / script, the agent surfaces assumptions, defines verification, and (for non-trivial work) spawns specialized review subagents.
- **Public-doc citation default:** the system prompt requires `snowflake_product_docs` lookup before suggesting Snowflake feature syntax.
- **Default safe-write policy:** the agent writes to `TEMP.<USER>` schema only, never DDL on `SNOWADHOC`, never modifies Salesforce without explicit permission.
- **Account-workflow skills (later phases):** account research, meeting prep, use case updates, briefing generation.

## Install

See [INSTALL.md](INSTALL.md).

## Layout

```
account-engineer-profile/
├── profile.json              # CCD manifest
├── system-prompt.md          # global system prompt overlay
├── docs/                     # principles, patterns, onboarding
├── skills/                   # CCD skills the profile registers
├── commands/                 # slash commands (placeholder in v0.1.0)
└── examples/                 # sanitized example assets (placeholder in v0.1.0)
```

## Roadmap

| Phase | Scope | Status |
|---|---|---|
| 1 | Bootstrap repo + asset-creation-discipline skill + system prompt | This release |
| 2 | Migrate read-only skills (snowflake-pdf, architecture-diagram, gdrive-desktop, gong, similar-use-cases, pptx) | Planned |
| 3 | Migrate + sanitize personal-data skills (account-context, account-handoff, etc.) | Planned |
| 4 | Slash commands (multi-review, start-asset, public-repo-review) + sanitized examples | Planned |
| 5 | Onboard a second ACE; iterate on feedback | Planned |

See [docs/architecture.md](docs/architecture.md) for how the pieces compose.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). All contributions pass through the **public repo gate**: every PR is reviewed against [docs/public-repo-policy.md](docs/public-repo-policy.md) before merging.

## Security

See [SECURITY.md](SECURITY.md). No secrets, PATs, customer names, internal URLs, or personal data may appear in this repository, ever.

## License

Apache 2.0 — see [LICENSE](LICENSE).
