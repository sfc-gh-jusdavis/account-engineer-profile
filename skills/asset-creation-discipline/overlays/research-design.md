# Overlay: Research and Design

Research-and-design-specific application of the four creation principles. Covers feature investigations, architecture comparisons, vendor evaluations, design recommendations, and any task whose output is a written analysis.

For the underlying principles see [../creation-principles.md](../creation-principles.md). For workflow patterns see [../creation-patterns.md](../creation-patterns.md).

---

## The Four Principles for Research / Design

### 1. Think Before Creating

Research without a clear question turns into a 20-page survey nobody reads. Surface and confirm:

| Question | Why it matters |
|---|---|
| **What decision does this inform?** | Drives every subsequent choice — depth, options considered, format |
| **Who reads it?** | A 5-person leadership review needs a different shape than a 1-person engineer's notes |
| **What does the audience already know?** | Determines how much foundational explanation belongs |
| **What does "done" look like?** | A recommendation? A comparison? A list of risks? An option-narrowing? |
| **What's the deadline / time budget?** | A 2-hour writeup is a different artifact than a week-long investigation |
| **What alternatives does the audience care about?** | If they only want A vs B, don't surveying C through F |

If you can't answer these, **stop and ask**.

### 2. Minimum Viable Asset

Research anti-patterns to avoid:

- Restating the question for half a page before answering it
- Covering options the audience didn't ask about
- Three-paragraph definitions of widely-known terms
- Citation-padding (5 references where 1 authoritative source is enough)
- "Background" sections longer than the recommendation
- Adding a "future considerations" section that nobody requested
- Lengthy "methodology" prose for straightforward research

The test: would the audience rather have your 12-page report or the 3-page version with the same recommendation? Almost always: the 3-page version.

### 3. Surgical Edits

When updating existing research:

- Update only the data point or section that needs changing
- Don't rewrite the recommendation when only an input changed (unless it actually changes the recommendation — and if so, say so explicitly)
- Don't re-pull all citations when only one needs updating
- Don't reorganize sections without explicit ask

Mark what changed and why. Diffs to a research doc help the reader decide whether to re-read.

### 4. Verification-Driven Output

Define what verifiable means for research:

- Every factual claim has a citation (or an explicit "I think" / "speculation" tag)
- Every comparison criterion is observable (cost in $, latency in ms, complexity in named-rubric units — not vibes)
- The recommendation explicitly answers the question that prompted the research
- The recommendation cites the specific criterion / criteria that drove it

Strong success criteria: "After reading, the audience can decide between A, B, and C using the table on page 2."
Weak: "Help the audience think about their options."

---

## Skeleton: Decision-Supporting Research

```markdown
# <Topic> — <Question Being Answered>

**Audience:** <who reads this>
**Decision:** <the choice this informs>
**Recommendation:** <one-line; details below>
**Confidence:** high / medium / low — why

## Background

One paragraph. The minimum the audience needs to follow the rest. Skip if audience knows it.

## Options Considered

### Option A: <name>
- Pro: ...
- Con: ...
- Effort to adopt: ...
- Cost: ...

### Option B: <name>
... (same shape)

### Option C: <name>
... (same shape)

## Comparison Table

| Criterion | A | B | C |
|---|---|---|---|
| Cost (annual, $K) | ... | ... | ... |
| Setup time (weeks) | ... | ... | ... |
| Vendor lock-in (1-5) | ... | ... | ... |
| Security posture | ... | ... | ... |
| Operational complexity (1-5) | ... | ... | ... |

## Recommendation

**Option <X>**, because:

1. <criterion that drove the choice>
2. <secondary factor>

The criteria that DON'T drive the choice (and would have changed the answer if weighted differently): <explicit list>.

## Open Questions / Risks

- <thing we don't know>
- <thing that could change the answer>

## Sources

| Claim | Source |
|---|---|
| ... | <citation> |
```

---

## Skeleton: Architecture Design Doc

```markdown
# <System Name> Architecture

**Owner:** <ACE name + role>
**Audience:** <who needs to approve / understand this>
**Status:** draft / under-review / approved

## Problem

What the architecture solves. One paragraph.

## Constraints

- <hard constraint that ruled out simpler designs>
- <hard constraint>
- <soft preference>

## Proposed Architecture

A diagram (mermaid). Then a numbered list describing the data flow / control flow.

## Component Inventory

| Component | Purpose | Inputs | Outputs | Failure mode |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |

## Tradeoffs

What other shapes were considered. Why this one was chosen. What we'd do differently if a constraint changed.

## Capacity / Scale

Concrete numbers: throughput, storage, query patterns, expected growth.

## Risks

Honest list. Not "no known risks" unless that's truly true.

## Open Questions

What still needs to be decided.

## References
```

---

## Quality Checks

- [ ] The opening one-line recommendation answers the question that prompted the research
- [ ] Every factual claim has a citation OR an explicit speculation tag
- [ ] Comparison criteria are observable / measurable
- [ ] Sources are authoritative (vendor docs, public data, experts) — not random blog posts
- [ ] Audience-known content is omitted (no Snowflake-101 in a doc for a senior Snowflake architect)
- [ ] Length is proportional to the decision's stakes
- [ ] Open questions / risks are listed honestly
- [ ] Specialized reviewer subagents spawned for non-trivial research (see [reviewer-prompts.md](reviewer-prompts.md))

---

## Tradeoff Template

When the user asks "should we do A or B?", default to this structure rather than free-form prose:

```markdown
## Option A: <name>
- Pro: ...
- Con: ...
- Effort: ...

## Option B: <name>
- Pro: ...
- Con: ...
- Effort: ...

## Recommendation: <X>
Because: <one specific criterion>
Would change to <Y> if: <one specific change in inputs>
```

This format takes 5 minutes longer to draft and saves 30 minutes of follow-up clarification.

---

## Common Failure Modes

| Symptom | Cause | Fix |
|---|---|---|
| Recommendation is hedged ("it depends") | No clear decision criterion identified up front | Go back to Principle 1: what decision does this inform? Use that as the deciding criterion |
| Audience asks "but what about X?" | X wasn't surfaced as an explicit non-goal | List "Out of scope" up front |
| Research takes 3x longer than budgeted | Scope creep — investigated options the audience didn't care about | Confirm option set before drafting |
| Reviewer says "this could be half as long" | Background and methodology padding | Cut everything not driving the recommendation |

---

## Composes With

- **PDF overlay**: when research becomes a customer-facing or executive-facing PDF, apply both this overlay and the PDF overlay together
- **Notebook overlay**: when research is supported by analysis, the notebook applies the notebook overlay; this overlay governs the writeup
- **Architecture-diagram skill** (Phase 2): when an architecture doc needs a diagram, use that skill for the diagram; this overlay governs the surrounding prose
