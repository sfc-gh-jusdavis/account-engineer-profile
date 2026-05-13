# Overlay: Script

Script-specific application of the four creation principles. Covers shell scripts, Python scripts, SQL pipelines, and small automation utilities.

For the underlying principles see [../creation-principles.md](../creation-principles.md). For workflow patterns see [../creation-patterns.md](../creation-patterns.md).

---

## The Four Principles for Scripts

### 1. Think Before Creating

Before writing any code, surface and confirm:

| Question | Why it matters |
|---|---|
| **Idempotent or one-shot?** | Idempotent scripts must handle "already done" state; one-shots can assume a clean slate |
| **Destructive?** | Destructive scripts need dry-run mode, confirmation prompts, and explicit safety rails |
| **Auth source?** | Connection name from env var, PAT from secret manager, OAuth — affects portability and security |
| **Failure mode?** | What happens on partial failure, on bad input, on rerun |
| **Who runs it where?** | One-off local laptop run vs scheduled cron vs CI/CD pipeline — drives logging, exit codes, dependency assumptions |
| **Data sensitivity?** | If it touches customer data, what stays local vs travels |

If you can't answer these, **stop and ask** before writing.

### 2. Minimum Viable Asset

Script anti-patterns to avoid:

- A `--verbose` flag when there's only one log level
- A config file for a one-shot script (env vars or args are simpler)
- Click / Argparse with five subcommands when one positional arg would do
- "Helper" abstractions for code used once
- Type hints / docstrings on a 10-line script
- Logging frameworks when `print()` would do
- Async / threading for inherently sequential work

The test: would a senior engineer say this script is overcomplicated? If yes, simplify.

### 3. Surgical Edits

When updating an existing script:

- Don't add type hints while fixing a bug
- Don't refactor functions adjacent to your change
- Don't reformat whitespace
- Don't change quote style or import order
- Don't rename utilities to "improve clarity"

If you notice unrelated dead code, mention it — don't delete it.

### 4. Verification-Driven Output

Every script either:

- Prints a final unambiguous success message and exits 0, OR
- Exits non-zero with a useful error message

No silent partial success. No "completed" message when the work didn't actually complete.

For non-trivial scripts, the verification is a test command the user can run that reproduces a known-good outcome.

---

## Standard Skeleton (Bash)

```bash
#!/usr/bin/env bash
#
# Purpose: <one-line>
# Usage:   ./script.sh <args>
# Env:     ACE_DEFAULT_CONN  - Snowflake connection name (required)
# Verify:  <command + expected output>

set -euo pipefail

# Required env / args
: "${ACE_DEFAULT_CONN:?Set ACE_DEFAULT_CONN env var}"
INPUT="${1:?Usage: $0 <input>}"

# Optional dry-run for destructive operations
DRY_RUN="${DRY_RUN:-false}"

# Work
echo "Processing $INPUT..."
if [[ "$DRY_RUN" == "true" ]]; then
  echo "DRY RUN - would execute: snow sql ..."
else
  snow sql -c "$ACE_DEFAULT_CONN" -q "..."
fi

# Final unambiguous success line
echo "OK: <what was done>"
```

## Standard Skeleton (Python)

```python
#!/usr/bin/env python3
"""<one-line purpose>

Usage: python script.py <args>
Env:   ACE_DEFAULT_CONN  - Snowflake connection name (required)
"""
import os
import sys
import snowflake.connector


def main(input_arg: str) -> int:
    conn_name = os.environ.get("ACE_DEFAULT_CONN")
    if not conn_name:
        print("ERROR: Set ACE_DEFAULT_CONN env var", file=sys.stderr)
        return 1

    with snowflake.connector.connect(connection_name=conn_name) as conn:
        # Work here
        pass

    print(f"OK: processed {input_arg}")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <input>", file=sys.stderr)
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
```

---

## Quality Checks (Before Delivering)

- [ ] Shell scripts start with `set -euo pipefail`
- [ ] Required env vars validated at the top with helpful error messages
- [ ] Required positional args validated with usage message
- [ ] No hardcoded credentials, PATs, paths, or connection strings
- [ ] No hardcoded customer or account references
- [ ] Destructive operations have a dry-run mode
- [ ] Idempotent scripts handle "already done" gracefully (use `IF NOT EXISTS`, check before insert, etc.)
- [ ] Final success message is unambiguous
- [ ] Failure modes return non-zero exit codes
- [ ] Tested with at least: happy path, missing required env var, bad input
- [ ] Specialized reviewer subagents spawned for non-trivial scripts (see [reviewer-prompts.md](reviewer-prompts.md))

---

## Idempotency Patterns

| Operation | Idempotent pattern |
|---|---|
| Create a Snowflake object | `CREATE OR REPLACE` or `CREATE ... IF NOT EXISTS` |
| Add a row to a table | `MERGE INTO ... USING (...) ON ... WHEN NOT MATCHED INSERT` |
| Grant a privilege | `GRANT` is naturally idempotent in Snowflake |
| Write a file | Check existence first, or always overwrite with deterministic content |
| Send an alert | Track sent state in a table; check before sending again |

If a script is supposed to be safe to rerun, every external side effect must follow one of these patterns.

---

## Common Failure Modes

| Symptom | Cause | Fix |
|---|---|---|
| Script "succeeded" but didn't actually do the work | Missing `set -euo pipefail`; commands fail silently | Add the safety preamble; check exit codes explicitly |
| Script burns credits even when input is wrong | Validation happens after expensive work starts | Validate inputs and env up front; fail fast |
| Re-running the script breaks state | Not idempotent | Use idempotency patterns above |
| Script works for the author, breaks for others | Hardcoded paths or env-dependent assumptions | Move all environment-specific values to env vars or args |
| Secret leaked into commit | Credentials hardcoded "for testing" then forgotten | Always use env / secret manager from line one |

---

## Composes With

- **PDF overlay**: when shipping a script as part of a customer-facing guide, the surrounding doc applies the PDF overlay; the script itself applies this overlay.
- **Notebook overlay**: a script extracted from a notebook (productionizing exploration) applies this overlay; the original notebook keeps the notebook overlay.
