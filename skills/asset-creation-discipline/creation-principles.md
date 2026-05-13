# Creation Principles

The four principles for creating any asset. Generalized from Andrej Karpathy's coding observations to apply to PDFs, notebooks, scripts, decks, research summaries, design documents — anywhere an agent helps you produce something for someone else.

The original coding-specific version lives in [docs/karpathy-coding-principles.md](../../docs/karpathy-coding-principles.md). This document re-frames the same four principles for any creative work.

---

## Principle 1: Think Before Creating

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before producing anything:

- **State assumptions explicitly.** Audience, scope, depth, success criteria, prerequisites. If uncertain, ask.
- **Present multiple interpretations.** When a request is ambiguous, surface the alternatives — don't pick silently.
- **Push back when warranted.** If a simpler asset would meet the goal, propose it.
- **Stop when confused.** Name what is unclear. Ask.

### How this looks per asset type

| Asset | What to surface |
|---|---|
| PDF | Audience (customer / internal / partner / field), scope (what's IN, what's OUT), prerequisite knowledge level, what success looks like for the reader |
| Notebook | Target dataset, success criterion (an answer? a chart? a model?), runtime constraints, who will run it |
| Script | Idempotent or one-shot? Destructive? Auth source? What's the failure mode? Who runs it where? |
| Research / Design | The decision this informs, the audience's existing knowledge, the deadline, alternative options the audience cares about |

---

## Principle 2: Minimum Viable Asset

**Smallest deliverable that meets the goal. Nothing speculative.**

- No sections beyond what was asked.
- No abstractions for single-use code.
- No "configurability" or "flexibility" that wasn't requested.
- No error handling for impossible scenarios.
- If 200 lines could be 50, rewrite it.
- If a 10-page PDF could be 3, cut it.

The test: *Would a senior practitioner say this is overcomplicated?* If yes, simplify.

### How this looks per asset type

| Asset | Common over-builds to avoid |
|---|---|
| PDF | "Advanced" sections nobody asked for; speculative troubleshooting (only document failure modes you've actually observed); 8-page intro before the first procedure |
| Notebook | Setup cells with 15 imports when 4 would do; commented-out experimental code left in; warmup cells that don't contribute to the result |
| Script | `--verbose` flag when there's only one log level; config file for a one-shot; abstractions for "future flexibility" |
| Research | Over-citation; covering options the audience didn't ask about; restating the question for half a page |

The mindset: good output solves *today's* problem simply. It does not pre-solve tomorrow's hypothetical problem.

---

## Principle 3: Surgical Edits

**Touch only what you must. Clean up only your own mess.**

When updating an existing asset:

- Don't "improve" adjacent sections, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style and structure, even if you'd do it differently.
- If you notice unrelated dead content, mention it — don't delete it.

When your changes create orphans:

- Remove imports/variables/sections that *your* changes made unused.
- Don't remove pre-existing dead content unless asked.

The test: *Every changed line/cell/section should trace directly to the user's request.*

### How this looks per asset type

| Asset | Drive-by behaviors to avoid |
|---|---|
| PDF | Re-flowing whole sections to fix a typo; "improving" prose adjacent to a procedure update; reordering chapters without explicit ask |
| Notebook | Regenerating the whole notebook to add a single cell; reformatting all cells while editing one; renaming variables to "improve clarity" |
| Script | Adding type hints / docstrings while fixing a bug; reformatting whitespace; renaming functions during a one-line patch |
| Research | Rewriting the recommendation section while updating a single data point; re-pulling all citations when only one needs updating |

---

## Principle 4: Verification-Driven Output

**Define success criteria. Loop until verified.**

Transform vague requests into verifiable goals:

| Vague | Verifiable |
|---|---|
| "Add a section on troubleshooting" | "Document the three failure modes I've observed (X, Y, Z), each with the diagnostic command and expected output" |
| "Make the notebook clearer" | "After my edits, a reader who has never seen this dataset can run it top-to-bottom and produce the chart" |
| "Fix the script" | "Reproduce the failure with input X, fix it, verify the script now exits 0 with input X and still exits 0 with the original happy-path inputs" |
| "Research SCIM" | "Compare three approaches (A, B, C) on five criteria (cost, complexity, time, vendor lock-in, security). End with a recommendation citing the criterion that drove it." |

For multi-step assets, state a brief plan with verification at each step:

```
1. [Step] -> verify: [check]
2. [Step] -> verify: [check]
3. [Step] -> verify: [check]
```

Strong success criteria let the agent loop independently. Weak criteria force the human into constant clarification.

### How this looks per asset type

| Asset | Verification |
|---|---|
| PDF guide | Reader follows steps, runs the verification command at each step, ends with the canonical "is it working" check |
| Notebook | Restart kernel, run all, see expected output without error |
| Script | Run with test input, exit code 0 and expected stdout; run with bad input, exit non-zero with helpful error |
| Research | Each claim has a citation; recommendation explicitly answers the question that prompted the research |

---

## Worked Examples (Cross-Asset)

### Example A: Hidden Assumptions in a PDF Request

**User:** "Build me a guide for setting up SCIM."

**Undisciplined response:** Starts writing a 30-page guide covering all major IdPs.

**Disciplined response:**

> Before drafting, a few clarifications:
> 1. Which IdP? (Entra / Okta / OneLogin / Ping / other) — the procedures differ
> 2. Audience? (customer-facing self-serve, partner integrator, internal field reference) — affects voice and depth
> 3. Scope: just SCIM provisioning, or also SAML SSO + SCIM together?
> 4. Customer's Snowflake edition? (Enterprise has SCIM; lower editions don't)
> 5. Approximate length target? (1-page quickref vs full 15-page runbook)
>
> If I had to guess the most useful default: Entra-to-Snowflake, customer-facing, SCIM-only, ~5 pages with verification per step.
>
> Confirm or adjust?

### Example B: Over-Build in a Script Request

**User:** "Write a script to dump table row counts to a CSV."

**Undisciplined response:** A 200-line script with config file, multiple output formats, async parallelism, and a Click CLI.

**Disciplined response:**

```bash
# count-rows.sh
set -euo pipefail
: "${ACE_DEFAULT_CONN:?Set ACE_DEFAULT_CONN env var}"
TABLES="${1:?Usage: count-rows.sh <database.schema>}"

snow sql -c "$ACE_DEFAULT_CONN" -q "
  SELECT TABLE_NAME, ROW_COUNT
  FROM ${TABLES}.INFORMATION_SCHEMA.TABLES
  WHERE TABLE_TYPE = 'BASE TABLE'
  ORDER BY TABLE_NAME
" --format csv > "${TABLES//./_}.csv"

echo "Wrote ${TABLES//./_}.csv"
```

15 lines. Idempotent. Single output format because that's what was asked. Add complexity later only if needed.

### Example C: Drive-By Edits in a Doc Update

**User:** "Update step 4 of the runbook to use the new CLI flag."

**Undisciplined diff:** Updates step 4 AND tightens grammar in step 3 AND reformats the "References" section AND adds a new "Common Mistakes" callout.

**Disciplined diff:** Changes only step 4. Tells the user "I noticed step 3 has a typo and the References list could be alphabetized — want me to fix those in a follow-up edit?" but does not change them in this request.

### Example D: Verifiable Research Goal

**User:** "Research private endpoint options for our customer."

**Undisciplined response:** A 10-page survey of every cloud provider's private connectivity story.

**Disciplined response:**

> A few clarifications first:
> 1. Which cloud is the customer on? (AWS / Azure / GCP) — the options differ entirely
> 2. What decision is this informing? (Architecture sign-off, sizing exercise, security review)
> 3. Does the customer require zero-public-internet, or is "TLS over public" acceptable?
>
> Once you confirm, I'll structure the output as: 3 viable options, each with cost / setup complexity / latency / lock-in / security tradeoffs, ending with a single recommendation tied to the decision in (2).

---

## Anti-Pattern Cheat Sheet

| Principle | Anti-pattern | Fix |
|---|---|---|
| Think Before Creating | Silently picks an audience / scope / depth | List assumptions explicitly, ask if uncertain |
| Minimum Viable Asset | Adds "Advanced" / "Edge cases" / "Future considerations" sections nobody asked for | Cut to what was requested; offer extras as follow-ups |
| Surgical Edits | Reformats / improves / refactors adjacent content while making the requested change | Only change lines/sections that fix the reported issue |
| Verification-Driven | "Add a section on X" without defining what makes that section successful | Restate as "the section succeeds when reader can do Y after reading it" |

---

## When to Apply Full Rigor

These principles bias toward caution over speed.

| Situation | Apply rigor? |
|---|---|
| Typo fix, one-line bug, single number update | No — just do it |
| New asset, multi-section doc, anything spanning multiple files | Yes |
| Customer-facing or shared-externally asset | Yes (especially Principle 1 audience question) |
| Anything where "I think this is what they meant" appears in your reasoning | Yes — stop and clarify first |
| Quick draft explicitly requested as quick | Lighter — surface the most important assumption, skip the rest |

The goal is reducing costly mistakes on non-trivial work, not slowing down trivial tasks.

---

## How to Know These Are Working

You should see:

- **Fewer surprises in delivered assets.** What you asked for is what you got.
- **Clarifying questions arrive before output, not after delivery.** Cheaper to fix early.
- **Smaller, cleaner deliverables.** No drive-by additions or speculative content.
- **Verification steps are part of every artifact.** Asset and verification ship together.

---

## Cross-References

- [creation-patterns.md](creation-patterns.md) — workflow patterns at the macro level
- [overlays/pdf.md](overlays/pdf.md) — PDF-specific application
- [overlays/notebook.md](overlays/notebook.md) — notebook-specific application
- [overlays/script.md](overlays/script.md) — script-specific application
- [overlays/research-design.md](overlays/research-design.md) — research-specific application
- [overlays/reviewer-prompts.md](overlays/reviewer-prompts.md) — multi-reviewer subagent prompts
