# Reviewer Prompts

Copy-paste subagent prompts for the multi-reviewer pattern (Pattern F in `creation-patterns.md`). Each prompt is one specialized reviewer focused on a single dimension. Run them in parallel via `runSubagent`, then consolidate findings before presenting to the user.

The reviewer set per asset type follows. Customize the prompt details (file path, asset URL, specific questions) before invoking.

---

## How to Use

1. Identify the asset type (PDF / notebook / script / research-design)
2. Pick the reviewer set below
3. For each reviewer in the set, invoke `runSubagent` with the prompt template
4. Run reviewers in parallel — set `run_in_background: true` and use `wait_agent` to collect
5. Consolidate findings into a single deduplicated list grouped by severity (blocker / should-fix / nit)
6. Present the consolidated list to the user before declaring the asset done

---

## PDF Reviewer Set (6 reviewers)

### 1. Technical Accuracy

```
You are reviewing a PDF guide draft for technical accuracy. Asset path: <PATH>.

Your single job: find any technical claim, command, query, UI path, or screenshot that is wrong or outdated. Verify against current Snowflake product behavior using the snowflake_product_docs tool when needed.

Categories to flag:
- SQL syntax that is invalid or deprecated
- Snowflake feature names that are wrong or have changed
- UI navigation paths that no longer match the product
- Screenshot content that does not match current UI
- Cloud-vendor (AWS / Azure / GCP) commands or console paths that are outdated
- Version-specific claims without version qualification

For each finding, output: {line_or_section, claim, what_is_wrong, suggested_fix}.

If you find no issues, reply: "Technical accuracy: no issues found."
```

### 2. Audience-Fit

```
You are reviewing a PDF guide draft for audience fit. Asset path: <PATH>. The declared audience is: <AUDIENCE>.

Your single job: flag any voice, terminology, or link that does not match the declared audience profile. Reference the snowflake-pdf skill's audience-profiles.md if available.

Categories to flag:
- Voice mismatch (third-person customer references in a customer-facing doc, etc.)
- Internal jargon in customer or partner docs (TAM, SE, FE, AE, etc.)
- Forbidden links for the audience (go/, internal Confluence, Slack, in customer-facing docs)
- Spelled-out acronyms cluttering an internal doc
- Classification footer mismatched to audience

For each finding, output: {line, original, suggestion, reason}.

If you find no issues, reply: "Audience-fit: no issues found."
```

### 3. Completeness

```
You are reviewing a PDF guide draft for completeness. Asset path: <PATH>.

Your single job: find missing prerequisites, logical leaps, or assumed knowledge that breaks the reader's flow.

Categories to flag:
- Steps that assume a prerequisite not listed in Prerequisites
- Steps that reference a tool / account / permission not previously introduced
- "Verify" lines missing from procedural steps
- End-to-end test missing or weak
- Troubleshooting section missing for a guide that needs one
- Out-of-scope statements missing (so the reader knows what this guide does NOT cover)

For each finding, output: {section, what_is_missing, why_it_matters}.

If you find no issues, reply: "Completeness: no issues found."
```

### 4. Security

```
You are reviewing a PDF guide draft for security. Asset path: <PATH>.

Your single job: flag anything that could expose secrets, recommend insecure defaults, or mislead the reader on auth / TLS / privacy.

Categories to flag:
- Hardcoded secrets, PATs, passwords, connection strings in examples
- Customer-confidential content in a non-customer-confidential audience
- Insecure defaults recommended (HTTP instead of HTTPS, public network when private exists)
- Misleading auth guidance (e.g., suggesting SSO bypass without explaining the security tradeoff)
- Missing warnings on destructive operations
- Forbidden internal data: deal context, ARR, MEDDPICC, internal account IDs

For each finding, output: {line_or_section, issue, severity (blocker / should-fix / nit), suggested_fix}.

If you find no issues, reply: "Security: no issues found."
```

### 5. Clarity / Simplicity

```
You are reviewing a PDF guide draft for clarity, applying Karpathy Principle 2 (Simplicity First) to prose. Asset path: <PATH>.

Your single job: find places where the guide is over-explained, padded, or could be cut without losing reader value.

Categories to flag:
- Background sections longer than the procedural sections
- Repeated explanations (same concept described twice)
- Speculative sections (Advanced / Edge cases / Future considerations) the user did not request
- Per-step screenshots where one screenshot per logical group would suffice
- Sentences with multiple "and" clauses that could be split
- Definitions of widely-known terms

For each finding, output: {section, what_to_cut, why}.

If the guide is already at minimum viable size, reply: "Clarity: no cuts recommended."
```

### 6. Reproducibility

```
You are reviewing a PDF guide draft for reproducibility. Asset path: <PATH>.

Your single job: simulate being a fresh reader and check whether following the steps EXACTLY would produce the documented success criterion.

Categories to flag:
- Commands that depend on shell state or env vars not listed in Prerequisites
- UI paths that depend on a specific Snowsight layout / role
- Steps with order dependencies not stated explicitly
- "Run X, then Y" where X has variable runtime and the reader can't tell when it's done
- Verification commands that don't actually verify what the step did

For each finding, output: {step, gap, what_a_fresh_reader_would_get_wrong}.

If you find no issues, reply: "Reproducibility: no issues found."
```

---

## Notebook Reviewer Set (4 reviewers)

### 1. Reproducibility

```
You are reviewing a notebook for reproducibility. Asset path: <PATH>.

Your single job: simulate "restart kernel + run all" and flag anything that would break for someone other than the author.

Categories to flag:
- Hidden state from REPL (variables defined out of cell order, manual edits to in-memory data)
- Hardcoded paths that won't exist on another machine
- Missing imports relative to first-use
- Hardcoded credentials, connection names, or PATs
- Cell order that requires non-linear execution
- Package versions not pinned where reproducibility matters

For each finding, output: {cell_number, issue, fix}.

If notebook would run cleanly from scratch, reply: "Reproducibility: clean."
```

### 2. Output Cleanliness

```
You are reviewing a notebook for output safety and cleanliness. Asset path: <PATH>.

Your single job: flag outputs that should not be shared or that obscure rather than illustrate.

Categories to flag:
- Customer PII visible in cell outputs
- Secrets accidentally printed (API keys, tokens, env values)
- Stale outputs that don't match the current code in the cell
- Massive dataframe dumps that should be summaries
- Empty / error outputs where success was supposed to happen

For each finding, output: {cell_number, issue, recommendation}.

If outputs are clean, reply: "Outputs: clean."
```

### 3. Cell Cohesion

```
You are reviewing a notebook for cell-level discipline. Asset path: <PATH>.

Your single job: check that each cell has one clear purpose and the narrative flows.

Categories to flag:
- Cells that do multiple unrelated things
- Cells with no output where output would help verify success
- Markdown cells longer than the code cells they introduce
- Code cells missing markdown context that explains WHY
- Helper functions defined far from where they are used
- Commented-out experimental code left in

For each finding, output: {cell_number, issue, suggestion}.

If cohesion is fine, reply: "Cell cohesion: fine."
```

### 4. Dependency Hygiene

```
You are reviewing a notebook for dependency and environment hygiene. Asset path: <PATH>.

Your single job: flag anything that makes the notebook hard to set up cleanly.

Categories to flag:
- Imports for packages not in a documented requirements file
- pip install commands inline that don't note the version
- Required env vars not documented in a markdown cell at the top
- Connection logic that assumes a specific user setup
- References to local files / stages without setup instructions

For each finding, output: {issue, fix}.

If hygiene is fine, reply: "Dependencies: fine."
```

---

## Script Reviewer Set (4 reviewers)

### 1. Failure Modes

```
You are reviewing a script for failure-mode handling. Asset path: <PATH>.

Your single job: think through what happens on partial failure, on rerun, on bad input, and on missing dependencies.

Categories to flag:
- Missing `set -euo pipefail` (bash) or equivalent strict mode
- Operations that can partially succeed without rollback or detection
- Bad-input handling that produces a confusing error
- Re-run behavior unclear (idempotent? safe? destructive?)
- Operations that depend on external state without checking it (network, auth, file existence)

For each finding, output: {line, scenario, current_behavior, recommended_behavior}.

If failure-mode handling is solid, reply: "Failure modes: handled."
```

### 2. Secrets Hygiene

```
You are reviewing a script for secrets hygiene. Asset path: <PATH>.

Your single job: catch any way a secret could be committed, leaked, or mishandled.

Categories to flag:
- Hardcoded passwords, PATs, API keys, OAuth secrets
- Connection strings with embedded credentials
- Logging that might print secret values
- .env files committed or referenced via committable paths
- Secrets passed as command-line arguments (visible in process list)
- README or comments referencing specific secret values

For each finding, output: {line, issue, fix}.

If hygiene is clean, reply: "Secrets: clean."
```

### 3. Idempotency

```
You are reviewing a script for idempotency. Asset path: <PATH>.

Your single job: determine whether the script is safe to rerun and, if it claims to be, verify each side effect uses an idempotent pattern.

Categories to flag:
- INSERT statements without MERGE / IF NOT EXISTS guards
- File writes without overwrite or existence check
- Notification sends without sent-state tracking
- CREATE statements without OR REPLACE / IF NOT EXISTS where appropriate
- Mutations to external systems without checking current state first

For each finding, output: {line, side_effect, idempotency_concern, recommended_pattern}.

If idempotency is fine (or N/A for a one-shot script), reply: "Idempotency: <fine | one-shot, intentional>."
```

### 4. Observability

```
You are reviewing a script for observability and operator UX. Asset path: <PATH>.

Your single job: check whether someone running this script for the first time understands what's happening.

Categories to flag:
- No progress output during long-running operations
- Final success state ambiguous (no clear "OK" or non-zero exit)
- Errors swallowed (caught and ignored without logging)
- Logs missing key context (which input, which step, which target)
- Verbose output cluttered with unhelpful internals

For each finding, output: {issue, suggestion}.

If observability is fine, reply: "Observability: fine."
```

---

## Research / Design Reviewer Set (4 reviewers)

### 1. Assumption Surfacing

```
You are reviewing a research / design document for assumption transparency. Asset path: <PATH>.

Your single job: find every implicit assumption the author made and flag any that should be made explicit.

Categories to flag:
- Recommendations that depend on unstated assumptions about budget, timeline, or risk tolerance
- Comparisons that assume a specific cloud / IdP / Snowflake edition without saying so
- Claims about audience knowledge without verifying it
- "Best practice" assertions without naming the practice or why it applies here
- Hedge words ("typically", "usually", "in most cases") that should be qualified or made specific

For each finding, output: {section, implicit_assumption, why_it_should_be_explicit}.

If assumptions are well-surfaced, reply: "Assumptions: surfaced."
```

### 2. Tradeoff Coverage

```
You are reviewing a research / design document for tradeoff completeness. Asset path: <PATH>.

Your single job: check that the document considers viable alternatives, not just the chosen path.

Categories to flag:
- Recommendations without alternatives considered
- Alternatives mentioned without honest pros/cons (one-sided framing)
- Decision criteria implied but not stated
- Cases where reasonable people would disagree, presented as if there's a clear answer
- Out-of-scope alternatives not labeled as such

For each finding, output: {section, missing_alternative_or_tradeoff, why_it_matters}.

If tradeoff coverage is good, reply: "Tradeoffs: covered."
```

### 3. Source Quality

```
You are reviewing a research / design document for source quality. Asset path: <PATH>.

Your single job: verify every factual claim is cited and that the cited sources are authoritative.

Categories to flag:
- Claims without citations
- Citations to non-authoritative sources (random blogs, outdated forum posts) where authoritative sources exist
- Claims attributed to "we tested" without actual test data
- Numbers without source (cost figures, latency claims, market share)
- Speculation not labeled as such

For each finding, output: {claim, current_source_or_lack, recommended_source}.

If sources are solid, reply: "Sources: solid."
```

### 4. Bias Check

```
You are reviewing a research / design document for bias. Asset path: <PATH>.

Your single job: take the perspective of a thoughtful skeptic and find what they would push back on.

Categories to flag:
- Cherry-picked data supporting the recommendation
- Strawman versions of alternatives
- Confirmation-bias framing ("As expected, ...", "Naturally, ...")
- Missing risks / open questions on the recommended option
- Tone that advocates rather than informs

For each finding, output: {what_a_skeptic_would_say, where_in_doc, suggested_revision}.

If bias is well-managed, reply: "Bias: well-managed."
```

---

## Consolidation Pattern

After all reviewers return, consolidate:

```markdown
# Multi-Reviewer Consolidated Report

**Asset:** <path>
**Asset type:** <type>
**Reviewers run:** <list>

## Blockers (must fix before delivery)
| Reviewer | Finding | Fix |
|---|---|---|
| ... | ... | ... |

## Should-fix
| Reviewer | Finding | Fix |
|---|---|---|
| ... | ... | ... |

## Nits (optional)
| Reviewer | Finding | Fix |
|---|---|---|
| ... | ... | ... |

## Reviewers with no findings
- <list>
```

Present this report to the user. The user accepts / rejects / defers each finding before the asset is finalized.

---

## When to Skip Multi-Review

The discipline is not free — multi-review takes 30-90 seconds and burns subagent runs. Skip it for:

- Trivial assets (one-page summary, one-cell notebook, 10-line script)
- Drafts the user has explicitly asked to be quick
- Iterations that change a single parameter or rewording

Apply it when stakes warrant: customer-facing, security-relevant, multi-section, multi-file.
