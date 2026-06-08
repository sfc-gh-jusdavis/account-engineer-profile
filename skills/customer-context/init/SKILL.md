---
name: customer-context:init
description: "Initialize context.md for a new customer activation project. Use when:
  'init context for [account]', 'set up context', 'new customer project', 'create
  context.md'. Calls Raven (Glean AI) with the activation prompt, supplements with
  Gong and Salesforce intel, then writes a structured context.md to the project root."
---

# Customer Context: Init

Generates `./context.md` for a newly-closed account. One-shot initialization — run once per customer project at the start of activation.

## Workflow

### Step 1: Confirm Account Name and CWD

If the account name was not in the trigger, ask:
```
Which account are we initializing context for?
```

Also confirm:
```
I'll write context.md to: [CWD path]
Is this the right project root? (y/n)
```

If `context.md` already exists in CWD, warn and ask before overwriting:
```
context.md already exists. Overwrite with a fresh init? (y/n)
Existing file will be replaced entirely.
```

---

### Step 2: Run Raven via Glean

Call `mcp_glean_chat` with the following prompt (substitute `<ACCOUNT_NAME>`):

```
Context:
I am the Account Engineer (activation SE) newly assigned to <ACCOUNT_NAME>. The deal
has recently closed won and I'm preparing to lead the post-sale activation. I have no
prior involvement with this account.

Constraint:
Cover the full journey from prospect to close.
Focus on actionable intel for activation — skip general Snowflake product descriptions.
Organize the output into clearly labeled sections: Account Overview, Account Team,
Key Customer Contacts (with roles and emails), Deal Timeline, Use Cases, Current
Architecture, Target Architecture, Pain Points & Objections, Competitor Landscape,
Upcoming Milestones, and Activation Priorities.
Cite the source engagement (date, type, subject) for each key finding.
```

If Raven returns empty or clearly truncated output, warn the user and do NOT write the file:
```
Raven returned insufficient output for [Account Name].
Options:
1. Retry Raven
2. Proceed with stubs and fill manually
3. Cancel
```

---

### Step 3: Supplement (run in parallel)

**3a. Gong — recent calls**
Run `gong` skill for the account (last 30 days). Note any call titles/dates not already cited in the Raven output — these will be added as additional source citations in the Deal Timeline.

**3b. Salesforce intel**
Run `salesforce-account-intel` skill for the account. Extract:
- Technical champion name/role
- MEDDPICC identified pain (if richer than Raven's output)
- Competitors

Use the Salesforce data to fill gaps in Raven's output, not to overwrite it.

---

### Step 4: Map Raven Sections to `context.md` Groups

| Raven section | `context.md` destination |
|---|---|
| Account Overview | Group 1 — `### Overview` |
| Account Team | Group 1 — `### Account Team` |
| Key Customer Contacts | Group 1 — `### Key Customer Contacts` (table format) |
| Deal Timeline | Group 2 — `### Deal Timeline` |
| Use Cases | Group 2 — `### Use Cases` (table format) |
| Pain Points & Objections | Group 2 — `### Pain Points & Objections` |
| Competitor Landscape | Group 2 — `### Competitor Landscape` |
| Current Architecture | Group 3 — `### Current Architecture` |
| Target Architecture | Group 3 — `### Target Architecture` |
| Upcoming Milestones | Group 4 — `### Upcoming Milestones` (table format) |
| Activation Priorities | Group 4 — `### Activation Priorities` |

**Tech Stack** (`### Tech Stack` subsections): If Raven's architecture sections contain specific tool names, extract them into the Tech Stack subsections. If not, stub with:
```
*To be populated — run `customer-context:tech-stack` after reviewing architecture details.*
```

---

### Step 5: Write `./context.md`

Use the template below. Populate each section from the mapped Raven output + Salesforce supplement. Gong calls not already cited by Raven are appended as additional entries in `### Deal Timeline`.

**Template:**

```markdown
# Context: [Account Name]
*Initialized: [YYYY-MM-DD] | Last updated: [YYYY-MM-DD] | Phase: Activation*
*Account Engineer: [Your Name]*

---

## 1. Account Identity

### Overview
[Company description, industry, size, region, contract value, close date — from Raven: Account Overview]

### Account Team
[Snowflake-side team — AE, CSM, ACE, SA — from Raven: Account Team]

| Role | Name | Email |
|------|------|-------|
| Account Executive | | |
| Customer Success Manager | | |
| Account Engineer | | |

### Key Customer Contacts
*Source: [Raven — date cited]*

| Name | Role | Email | Notes |
|------|------|-------|-------|

---

## 2. Deal Intelligence

### Deal Timeline
*Source citations per entry — from Raven: Deal Timeline*

- **[Date]** — [Event] *(source: [engagement type, subject])*

### Use Cases
*From Raven: Use Cases*

| Name | Priority | Status | Notes |
|------|----------|--------|-------|

### Pain Points & Objections
*From Raven: Pain Points & Objections*

### Competitor Landscape
*From Raven: Competitor Landscape*

---

## 3. Technical Landscape

### Current Architecture
*From Raven: Current Architecture*

### Target Architecture
*From Raven: Target Architecture*

### Tech Stack

#### Inbound to Snowflake
*Tools and pipelines moving data into Snowflake*

#### Outbound from Snowflake
*BI tools, reverse ETL, APIs consuming Snowflake data*

#### Peripheral Services
*Orchestration, transformation, CI/CD, infrastructure*

---

## 4. Activation Work

### Activation Priorities
*From Raven: Activation Priorities — ordered by immediate impact*

1.
2.
3.

### Upcoming Milestones
*From Raven: Upcoming Milestones*

| Milestone | Owner | Target Date | Status |
|-----------|-------|-------------|--------|

### Chat & Call Log
*Append-only — newest first. Maintained by `customer-context:chat-update`.*
```

---

### Step 6: Confirm and Offer Next Step

After writing, print a summary:
```
context.md written to ./context.md

Sections populated: [list]
Sections stubbed:   [list — e.g., Tech Stack if no specifics found]

Run `customer-context:tech-stack` to populate the Tech Stack section?
```

---

## Stopping Points

- Ask for account name if not provided in trigger
- Confirm CWD is the correct project root before writing
- Warn and ask before overwriting an existing `context.md`
- Do NOT write if Raven returns empty/truncated output — offer retry or stub options
- Ask which Gong call to reference if multiple matches on account name

## Skills Called

| Skill | Purpose |
|---|---|
| `mcp_glean_chat` | Raven activation prompt |
| `gong` | Supplement with recent call dates/titles |
| `salesforce-account-intel` | Supplement with MEDDPICC, tech champion, competitors |
