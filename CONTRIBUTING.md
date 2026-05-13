# Contributing

Thanks for considering a contribution to the Account Engineer profile.

## The Public Repo Gate

This repository is **public**. Every PR is reviewed against [docs/public-repo-policy.md](docs/public-repo-policy.md) before merging. Content that cannot appear:

- Customer names, account IDs, ARR / forecast / deal context
- Internal Snowflake URLs (`go/`, `*.atlassian.net`, `snowflake.slack.com`, `quip.com`, internal dashboards)
- PATs, passwords, API keys, OAuth secrets, connection strings
- Internal Snowflake employee names paired with role context that wouldn't be public
- Personal connection names — use `<your-connection-name>` or `${ACE_DEFAULT_CONN}` placeholders
- Salesforce data, Gong call transcripts, MEDDPICC fields
- Internal product code names not announced publicly

Before opening a PR, run:

```bash
# From the repo root
grep -ri 'JDAVIS_AWS1\|JUSDAVIS\|j\.davis\|atlassian\.net\|snowflake\.slack\.com\|quip\.com' . \
  --exclude-dir=.git
# Should produce zero hits.
```

## Branch Naming

| Prefix | When to use |
|---|---|
| `feat/` | New skill, new command, new feature |
| `fix/` | Bug fix |
| `chore/` | Dependency / config / housekeeping |
| `docs/` | Documentation only |
| `refactor/` | Internal restructuring, no behavior change |

Format: `<prefix>/<kebab-case-short-name>`. Example: `feat/migrate-snowflake-pdf-skill`.

## Commit Messages

- Imperative mood, present tense ("add X" not "added X")
- Subject under 72 characters, no trailing period
- Blank line, then optional body explaining "why"

## Adding or Updating a Skill

When migrating an existing skill or authoring a new one:

1. Branch: `git checkout -b feat/<skill-name>`
2. Place the skill at `skills/<skill-name>/` with a `SKILL.md` defining triggers and workflow
3. Sanitize: replace personal connection names with `${ACE_DEFAULT_CONN}`, replace personal usernames with `${ACE_USER_HANDLE}`, replace customer names with placeholder examples
4. Document required env vars in the skill's `SKILL.md`
5. Run the public-repo grep above; fix any hits
6. Update `skills/README.md` to list the new skill
7. Commit, push, open PR
8. Self-review the diff against [docs/karpathy-coding-principles.md](docs/karpathy-coding-principles.md) before requesting merge

## Adding a Slash Command

1. Create `commands/<command-name>.md` with YAML front-matter:
   ```markdown
   ---
   name: command-name
   description: One-line description
   ---

   <prompt content>
   ```
2. Update `commands/README.md` to list the command
3. Test locally before opening the PR

## Updating Docs

Docs live in `docs/`. When editing:

- Apply [Karpathy Principle 3](docs/karpathy-coding-principles.md) (Surgical Changes): every changed line traces to a stated goal
- If a doc grows past ~300 lines, consider splitting it
- Cross-link liberally so readers can navigate between principles, patterns, and overlays

## Releasing

The profile uses [SemVer](https://semver.org/):

- Patch (0.1.x) — fixes, doc edits, prompt tweaks that don't change skill behavior
- Minor (0.x.0) — new skills, new commands, new overlays
- Major (x.0.0) — breaking changes to the profile manifest, skill API, or system prompt structure

Update `version` in `profile.json` and tag the release.

## Code of Conduct

See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
