---
name: demo-ops:principles
description: "Karpathy 4 coding principles applied to demo work. Use when reviewing demo code, before declaring a demo done, or when asked about coding standards for demos. Triggers: demo principles, demo coding principles, review my demo, self-review demo, karpathy principles demo, demo code quality, demo coding standards."
---

Apply these to every code change in a demo. Distilled from Andrej Karpathy's observations on LLM coding pitfalls.

## The Four Principles

### P1: Think Before Coding
**Don't assume. Don't hide confusion. Surface tradeoffs.**
- State assumptions explicitly. If uncertain, ask.
- Present multiple interpretations when a request is ambiguous; don't pick silently.
- Push back when a simpler approach exists.

### P2: Simplicity First
**Minimum code that solves the problem. Nothing speculative.**
- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" that wasn't requested.
- **Demo addendum**: no speculative views, no abstractions for hypothetical future demos. One demo, one schema, one purpose. If a future demo needs the same data, fork and rename — don't generalize.

### P3: Surgical Changes
**Touch only what you must.**
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style.
- Every changed line traces to the user's request.

### P4: Goal-Driven Execution
**Define success criteria. Loop until verified.**

| Vague | Verifiable |
|---|---|
| "Build a demo" | "Streamlit on stage X loads, top-3 queries return in <5s, teardown drops the schema" |
| "Generate data" | "100k rows in TABLE_X, distributions match spec, no real PII strings" |
| "Add an agent" | "Agent answers each verified query in the semantic model" |

## Self-Review Checklist (before "done")

- **P1:** Silent assumptions? Were they correct?
- **P2:** Could 100 lines be 50?
- **P3:** Every changed line traces to the request?
- **P4:** Each change verifiable (test? smoke check? manual run?)
- **Privacy:** Any real names / internal email domains / real account IDs? Replace with synthetic.
- **Teardown:** Documented `DROP DATABASE` / cleanup path?
- **Determinism:** Seeded all randomness (`RANDOM(42)`, `Faker.seed(42)`, `np.random.seed(42)`)?

## Anti-Pattern Cheat Sheet

| Anti-pattern | Fix |
|---|---|
| Silently assumes file format, scope, fields | List assumptions explicitly, ask |
| Strategy pattern for a single calculation | One function until complexity is real |
| Reformats while fixing a bug | Only change lines that fix the issue |
| Generates data without a seed | Always seed |
| Names tables `T1`, `FOO` | Names tell the story |
| Demo schema in `PUBLIC` | Use `DEMO_<topic>` and tag |
| Adds Faker / dbt / Snowpark "just because" | Use the simplest tool that works |
| "I'll review and improve" | "Write a verifiable check, run it" |

## When to Apply Full Rigor

| Task | Rigor? |
|---|---|
| Typo, one-line, obvious rename | No |
| New demo, multi-file, refactor | Yes |
| DDL on a shared `DEMO_*` DB | Yes — confirm with user first |
| "I think this is what they meant" appears in your reasoning | Yes — clarify first |

## Reference

- Sibling skill: `asset-creation-discipline` for non-demo creation work
- Public-repo policy: `docs/public-repo-policy.md`
