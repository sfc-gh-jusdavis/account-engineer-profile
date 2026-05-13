# Memory File Template: `/memories/ace-setup.md`

This is the canonical format for the ACE setup memory file. The `ace-setup` skill writes this format; other skills read from it.

If you are an agent looking for ACE config values, parse this format. If you are a skill author, write to this format when persisting profile-wide ACE config.

---

## File Path

`/memories/ace-setup.md` (managed via the CCD memory tool)

---

## Format

```markdown
# ACE Profile Setup
Last updated: <ISO date, e.g. 2026-05-13>

## Connection
- Connection name: <ACE_DEFAULT_CONN value>
- Snowflake username: <ACE_USER_HANDLE value>

## Demo Account
- Account identifier: <demo_account value>
- Region: <demo_region value>
- Default DDL/DML warehouse: <ddl_warehouse value>

## Identity
- Display name: <ace_display_name value>

## GitHub
- Handle: <github_handle value, or "not set">
- Default project org: <github_org value, or "not set">

## Notes
<free-form ACE notes; preserved across re-runs of /ace-setup>
```

---

## Field Reference

| Section | Field | Purpose | Read by |
|---|---|---|---|
| Connection | Connection name | The Snowflake CLI connection alias | Almost every SQL-running skill (also reads `${ACE_DEFAULT_CONN}` env var as primary) |
| Connection | Snowflake username | Drives `TEMP.<USER>` write scope | SQL-running skills (also reads `${ACE_USER_HANDLE}` env var as primary) |
| Demo Account | Account identifier | Cover-page metadata, runbook context | snowflake-pdf (Phase 2), briefing skills |
| Demo Account | Region | Cover-page metadata, region-specific URLs | snowflake-pdf, architecture-diagram |
| Demo Account | Default DDL/DML warehouse | Suggested warehouse for write operations | Any DDL/DML skill |
| Identity | Display name | "Author" field on PDFs and decks | snowflake-pdf, pptx, briefing skills |
| GitHub | Handle | Owner field for new repos, fork URL construction | Project-repo skills, fork workflows |
| GitHub | Default project org | Default org for new repos | Project-repo skills |

---

## Why Two Storage Locations?

`ACE_DEFAULT_CONN` and `ACE_USER_HANDLE` live in BOTH this memory file AND the CCD profile envVars. Reasons:

- **Profile envVars** are accessible at skill-execution time as `${VAR}` expansion in skill code. This is the runtime path.
- **Memory file** is human-readable, easy for the user to inspect, and consulted by skills that need the value but aren't doing `${VAR}` expansion (e.g., a skill that wants to display "you're working in connection X" in prose).

Other fields (demo account, display name, GitHub) live in memory only because:
- They're not needed by every skill — making them env vars would clutter the profile config
- They're text-rich (display name has spaces, etc.) — not natural as env vars
- They change less often than the connection or username

---

## Parsing Recipe (for skill authors)

Python example:

```python
import re
import pathlib

def read_ace_setup() -> dict:
    """Parse /memories/ace-setup.md into a dict."""
    path = pathlib.Path.home() / ".memories" / "ace-setup.md"
    if not path.exists():
        return {}

    text = path.read_text()
    fields = {}

    # Match lines like "- Connection name: SOME_VALUE"
    for line in text.splitlines():
        m = re.match(r'^- ([^:]+): (.+)$', line)
        if m:
            key = m.group(1).strip().lower().replace(' ', '_').replace('/', '_')
            value = m.group(2).strip()
            if value not in ('not set', '<not set>'):
                fields[key] = value

    return fields

# Usage
ace = read_ace_setup()
display_name = ace.get('display_name', 'Snowflake Account Engineer')
github_handle = ace.get('handle')  # may be None if "not set"
```

(The actual memory tool path may differ — adjust based on the platform's memory location.)

---

## Versioning

The format above is the v1 schema. If a future setup skill adds new fields:

- Add them to a new section (don't reshuffle existing sections)
- Existing skills reading the file ignore unrecognized sections
- Bump the `# ACE Profile Setup` line to include a version: `# ACE Profile Setup (v2)`

The setup skill should be backwards compatible: when it reads a v1 file, it preserves any sections it doesn't manage.

---

## Privacy

This memory file is local to the ACE's CCD installation. It does not get committed to the profile repo. It does not get shared between ACEs. It is per-user state.

Things that should NOT be added to this file even if a future skill is tempted:

- Customer names
- Customer account identifiers (the field is YOUR demo account, not customer accounts)
- PATs, passwords, secrets
- Salesforce data, Gong data
- Anything from the public-repo forbidden-content list

If a skill needs customer-specific context, it should write to a separate memory file scoped to that customer (`/memories/customer-<name>.md`), not pollute this profile-wide setup file.
