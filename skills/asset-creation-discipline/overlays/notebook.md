# Overlay: Notebook

Notebook-specific application of the four creation principles, plus a recommended skeleton for analysis notebooks.

For the underlying principles see [../creation-principles.md](../creation-principles.md). For workflow patterns see [../creation-patterns.md](../creation-patterns.md).

---

## The Four Principles for Notebooks

### 1. Think Before Creating

Before writing any cells, surface and confirm:

| Question | Why it matters |
|---|---|
| **Target dataset?** Which database / schema / tables / time range? | Drives connection choice and queries |
| **Success criterion?** A specific answer? A chart? A model? A summary table? | Drives the final cell — start there and work backwards |
| **Runtime constraints?** Local laptop / Snowflake notebook / SPCS? | Drives package choices, compute size, kernel selection |
| **Who runs it?** Just you / shared with colleagues / runs as a scheduled task? | Drives reproducibility requirements (env vars vs hardcoded, secrets handling) |
| **Sensitivity?** Customer data / synthetic / public sample? | Drives output handling (clear cell outputs before sharing, etc.) |

If you can't answer these, **stop and ask**.

### 2. Minimum Viable Asset

Notebook anti-patterns to avoid:

- More than one import cell (consolidate)
- Setup cells that don't contribute to the final output
- Commented-out experimental code left in cells
- "Helper" cells that define a function used once 50 lines later (inline it)
- Six different chart styles trying to find the right one (pick one)
- Markdown cells longer than the code cells they describe

The test: starting from a blank kernel, what is the **minimum sequence of cells** that produces the success criterion? That's your notebook. Anything else is decoration.

### 3. Surgical Edits

When updating an existing notebook:

- Use `notebook_edit_cell` (or equivalent) on specific cells; don't regenerate the whole notebook
- Don't reformat unrelated cells while editing one
- Don't re-pull data unnecessarily (preserve cached outputs if they're still relevant)
- Don't rename variables unless required by your change

If the user asks for a small tweak, deliver a small tweak.

### 4. Verification-Driven Output

Each cell's verification is its **output**. Cells that produce no output (pure side effects) should:

- Print a confirmation (`print(f"Loaded {len(df)} rows")`)
- Or assert their post-condition (`assert df.shape[0] > 0`)

The notebook's overall verification is: **restart the kernel, run all cells, observe the success criterion in the final cell's output**.

If "restart and run all" doesn't produce the desired result, the notebook is not done.

---

## Skeleton: Analysis Notebook

```python
# Cell 1 (markdown): Title and one-paragraph purpose
# What this notebook does, who it's for, what success looks like.

# Cell 2 (code): Imports
import os
import pandas as pd
import snowflake.connector
import matplotlib.pyplot as plt

# Cell 3 (code): Connection
conn = snowflake.connector.connect(
    connection_name=os.getenv("ACE_DEFAULT_CONN")
)
print(f"Connected as {conn.user} to {conn.account}")

# Cell 4 (markdown): Section header — Load data

# Cell 5 (code): Load
query = """
SELECT ...
FROM ...
WHERE ...
"""
df = pd.read_sql(query, conn)
print(f"Loaded {len(df):,} rows")
df.head()

# Cell 6 (markdown): Section header — Analysis

# Cells 7-N: Analysis steps, each with output that verifies the step

# Final cell (code or markdown): The success criterion
# If a chart: plot it.
# If a number: print it.
# If a recommendation: state it in markdown citing the data above.
```

---

## Quality Checks (Before Sharing)

After drafting and before sharing the notebook:

- [ ] Restart kernel + run all completes without error
- [ ] Final cell shows the success criterion clearly
- [ ] No hardcoded credentials, PATs, or connection strings
- [ ] Connection name uses `os.getenv("ACE_DEFAULT_CONN")` not a literal value
- [ ] No customer PII in cell outputs that will be shared (clear or aggregate)
- [ ] No secrets in cell outputs (API keys printed during debug)
- [ ] Package versions pinned if reproducibility matters (in markdown or `pip install` cell)
- [ ] Markdown cells explain WHY, code cells do WHAT
- [ ] Specialized reviewer subagents spawned for non-trivial notebooks (see [reviewer-prompts.md](reviewer-prompts.md))

---

## Common Failure Modes

| Symptom | Cause | Fix |
|---|---|---|
| "Works in my session, breaks for someone else" | Hidden state from REPL — variables defined in deleted cells, manual edits to in-memory data | Restart kernel + run all; if it breaks, fix the dependency chain |
| "Notebook runs but the output doesn't look right" | Weak verification (no asserts, no sanity prints) | Add row-count prints, shape asserts, distribution checks |
| "Notebook is 80 cells long" | No outline-first; explored on the fly | Start over with the success criterion (final cell) and work backwards; cut anything that doesn't contribute |
| "Customer accidentally saw raw account names in outputs" | Outputs not cleared before sharing | Clear all outputs OR aggregate before display; consider parquet output to a stage instead |

---

## Composes With

- For Snowflake-native notebooks (deployed via Snowsight): the discipline applies the same; deployment uses CCD's notebook tooling.
- For shared customer-facing notebooks: pair this overlay with the **PDF overlay** for any prose-heavy sections that get extracted into a delivery doc.
- For analysis that informs a decision: the **research-design overlay** governs the writeup; this overlay governs the notebook itself.
