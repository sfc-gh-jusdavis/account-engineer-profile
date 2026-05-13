# Audience Profiles

This file is read by the CoCo agent during the **Audience Workflow** of the snowflake-pdf skill. The agent uses these profiles to review a markdown document against its declared `audience` and propose rewrites where the language doesn't match the audience.

Every document **must** declare exactly one audience in front-matter:

```yaml
audience: customer-facing | internal | partner | field-only
```

---

## customer-facing

The reader is the customer (or a customer's vendor/integrator). The doc may leave Snowflake's hands.

### Voice / POV
- Address the reader in **second person**: "you", "your environment", "your account"
- **Never refer to the customer in the third person.** Replace "<example-customer> are on Business Critical" with "You are on Business Critical."
- Avoid "the customer" / "they" / "their team" — that's writing *about* the reader, not *to* them.
- "We" is acceptable when it means "Snowflake recommends..." but prefer direct verbs ("Run...", "Verify...").

### Terminology
- Spell out acronyms on first use (ADF, OCSP, NSG, IR). Subsequent uses may be the acronym alone.
- No internal Snowflake jargon: avoid TAM, SE, FE, AE, SA, AM, PS, RFE, BCR, SnowReplay, etc.
- "Snowflake Support" is the right escalation phrase — not "open a JIRA", "ping #help-...", or "case the team".

### Links
- Allowed: `docs.snowflake.com`, `community.snowflake.com`, `signature.snowflake.com`, vendor docs (Microsoft Learn, AWS docs, etc.)
- Forbidden: `go/`, internal Confluence (`snowflakecomputing.atlassian.net`), Slack (`snowflake.slack.com`), `quip.com`, internal dashboards.

### Tone
- Polished, formal-but-warm, action-oriented.
- Lead with what to do; explain why second.

### Things to remove
- Internal account IDs, internal escalation paths, internal contacts by name without title, customer slack channels, deal context, ARR/forecast info, anything from Salesforce notes.

### Cover wording
- Classification: **Customer Confidential**
- Audience badge: **CUSTOMER-FACING**
- Badge color: Mid-Blue `#29B5E8`

---

## internal

The reader is a Snowflake employee. The doc stays inside Snowflake.

### Voice / POV
- Third-person customer references are fine ("CCU's environment", "the customer's NSG").
- "We / our" refers to Snowflake.

### Terminology
- Internal acronyms are fine without expansion (TAM, SE, FE, AE, SA, AM, PS, BCR, ACE, EBC).
- Snowflake-internal product/team names are fine.

### Links
- Anything goes: `docs.snowflake.com`, `go/`, Confluence, Slack, GitHub Enterprise, internal dashboards, Quip.

### Tone
- Terse, direct, dense. Skip motivation if it's obvious to a Snowflake reader.

### Things to remove
- Customer-confidential information that the customer hasn't authorized for internal sharing — but most operational detail is fine.

### Cover wording
- Classification: **Snowflake Confidential**
- Audience badge: **INTERNAL**
- Badge color: Valencia Orange `#FF9F36`

---

## partner

The reader works at a Snowflake partner (SI, ISV, reseller). The doc travels under an MNDA-equivalent.

### Voice / POV
- Address the reader as a peer collaborator: "your team", "your customer", "we" (meaning the joint Snowflake+partner team).
- Customer references should follow what the joint engagement uses publicly.

### Terminology
- Spell out Snowflake-internal acronyms on first use — partner readers may not know TAM/SE/FE conventions.
- Partner program terms (PSA, SI, Powered-by, Ready) are fine.

### Links
- Allowed: `docs.snowflake.com`, partner portal (`partner.snowflake.com`), `community.snowflake.com`, partner-facing GitHub repos.
- Forbidden: internal `go/`, internal Confluence, internal Slack.

### Tone
- Educational + enabling. Assume Snowflake fluency but not Snowflake-internal context.

### Things to remove
- Other-partner deal context, internal forecasting, anything about Snowflake's GTM that isn't already public.

### Cover wording
- Classification: **Snowflake & Partner Confidential**
- Audience badge: **PARTNER**
- Badge color: Purple `#7B5DB8`

---

## field-only

The reader is a Snowflake field employee (SE / FE / AE / SA / AM / TAM / PS). The doc never leaves Snowflake field channels.

### Voice / POV
- SE shorthand fully acceptable. Direct, conversational.

### Terminology
- All Snowflake-internal acronyms, product code names, channel references, deal context — fine.

### Links
- Anything: `go/`, SE Confluence, `#se-help`, `#cortex-code`, account team Quips, Salesforce links.

### Tone
- SE office-hours register: blunt, jargon-rich, war-story OK.

### Things to remove
- Nothing customer-confidential without consent — but otherwise no filter beyond field channels.

### Cover wording
- Classification: **Snowflake Internal — Field**
- Audience badge: **FIELD-ONLY**
- Badge color: Slate Grey `#5C6B72`

---

## Review heuristics for the agent

When reviewing a doc against its declared audience, look for and flag:

1. **Voice mismatches** (most common): customer-facing docs that refer to the customer in third person; partner docs that say "Snowflake's customer".
2. **Terminology mismatches**: internal jargon in customer/partner docs; spelled-out acronyms cluttering an internal doc.
3. **Forbidden links**: any URL whose domain isn't on the audience's allowed list.
4. **Forbidden content**: deal context, internal escalation paths, account team names without role context, anything from PS comments, anything from Salesforce that isn't public.
5. **Classification mismatch**: front-matter `classification` set to something inconsistent with `audience` (warn — the renderer auto-derives the right one if not explicit).

For each finding produce: `line_number`, `original`, `suggestion`, `reason`. Present them to the user grouped by category. The user accepts/keeps/replaces each one before render.
