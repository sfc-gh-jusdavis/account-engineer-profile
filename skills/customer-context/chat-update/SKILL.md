---
name: customer-context:chat-update
description: "Update context.md from ongoing activation work — agent chat sessions,
  Gong calls, and Google Drive notes. Use when: 'update context from this chat',
  'capture findings', 'log Gong call to context', 'update from GDrive', 'end of
  session update'. Appends to Chat & Call Log and surgically updates Groups 1-3."
---

# Customer Context: Chat Update

Called at the end of a CCD session (or on demand) to capture new learnings and append them to `./context.md`. Always appends to the Chat & Call Log and makes surgical updates to Groups 1-3 only when there is new, specific intel.

**Group 4 Chat & Call Log is strictly append-only — never edit or delete existing entries.**

---

## Workflow

### Step 1: Confirm Account and Sources

Read `./context.md` header to confirm account name and the `Last updated` date.

If `context.md` is not found in CWD:
```
context.md not found. Run `customer-context:init` first.
```

**Ask which sources to pull from** (if not clear from the trigger):

```
What should I pull new findings from? (select all that apply)
1. This conversation — extract findings from the current chat session
2. New Gong calls — pull calls since [last updated date]
3. Google Drive — check account folder for new docs
```

Can pull from multiple sources in one run.

---

### Step 2: Extract Findings Per Source

For each selected source, extract findings and tag each with its origin.

**Source: Current Conversation**
Review what was discussed in this CCD session. Extract:
- New contacts or role clarifications
- Architecture decisions or confirmations
- New tools or integrations mentioned (flag for `tech-stack` skill)
- New or updated pain points / objections surfaced
- Milestone updates (new items, status changes, date shifts)
- Activation priority changes
- Action items or open questions

**Source: New Gong Calls**
Run `gong` skill for the account, filtered to calls after `[Last updated date]`. For each new call:
- Extract call title and date
- Extract key findings from the call brief

**Source: Google Drive**
Run `gdrive-desktop` skill. Check the account's folder for documents created or modified since `[Last updated date]`. Extract key findings from new/changed docs.

---

### Step 3: Map Findings to `context.md` Sections

| Finding type | Maps to |
|---|---|
| New contact or role update | Group 1 — `### Key Customer Contacts` |
| Snowflake account team change | Group 1 — `### Account Team` |
| Architecture decision or update | Group 3 — `### Current Architecture` or `### Target Architecture` |
| New tool / integration (3+ items) | Route to `customer-context:tech-stack` sub-skill |
| New tool / integration (1-2 items) | Group 3 — `### Tech Stack` (inline, with source tag) |
| New pain point or objection | Group 2 — `### Pain Points & Objections` (append) |
| Use case status change | Group 2 — `### Use Cases` (update Status column) |
| Milestone update | Group 4 — `### Upcoming Milestones` (update Status; add new rows) |
| Activation priority shift | Group 4 — `### Activation Priorities` (replace list — ask explicitly) |
| General session findings | Group 4 — `### Chat & Call Log` only |

---

### Step 4: Show Preview Before Writing

Always present a diff-style preview before touching the file:

```
Context update preview for [Account Name]:

[APPEND] Group 4 / Chat & Call Log: Session 2026-06-08
[UPDATE] Group 1 / Key Customer Contacts: Adding Sarah Chen, Data Platform Lead
[UPDATE] Group 2 / Use Cases: "Real-Time Pipeline" status → In Progress
[UPDATE] Group 4 / Upcoming Milestones: Row 1 status → Complete
[ROUTE]  Group 3 / Tech Stack: 3 new items — will invoke customer-context:tech-stack

Proceed? (y/n)
```

Do NOT write until the user confirms.

**Special case — Activation Priorities replacement:**
If the session revealed a clear shift in priorities, show the proposed new list explicitly and ask:
```
Activation Priorities have shifted. Replace the current list with:
1. [new priority 1]
2. [new priority 2]
3. [new priority 3]
Replace? (y/n)
```

---

### Step 5: Apply Updates

**Rules per section:**

| Section | Update rule |
|---|---|
| Group 1 — Contacts table | Add new rows; update Notes column for existing contacts |
| Group 1 — Account Team | Update individual cells only |
| Group 2 — Use Cases table | Update Status/Notes columns only; do not change Name or Priority |
| Group 2 — Pain Points | Append new items under existing content; never delete |
| Group 3 — Architecture | Append or replace paragraphs; preserve Raven source citations |
| Group 3 — Tech Stack (1-2 items) | Add bullets with source tag |
| Group 4 — Activation Priorities | Replace full list only if user confirmed in Step 4 |
| Group 4 — Milestones table | Update Status column; append new rows at bottom |
| Group 4 — Chat & Call Log | **Append only** — new entry at TOP of section, above previous entries |

**Then update the header:**
Replace `*Last updated: [old date]*` with today's date.

---

### Step 6: Write Log Entry

Append a new entry to `### Chat & Call Log` (newest first):

```markdown
---

### [YYYY-MM-DD] — [Source: Chat Session | Gong: "Call Title" | GDrive: "Doc Title"]

**Findings:**
- [key finding 1]
- [key finding 2]
- [key finding 3]

**Sections updated:** [e.g., Group 1 / Contacts, Group 4 / Milestones]

**Open items:**
- [ ] [follow-up or action item]
```

If multiple sources were pulled, write one log entry per source (separate `---` blocks).

---

### Step 7: Print Summary

```
context.md updated — [Account Name]

Log entries added: [count]
Sections updated:  [list]
Last updated:      [today's date]
```

---

## Stopping Points

- If `context.md` not found: offer to run `customer-context:init` first
- Ask which sources to pull if not specified in trigger
- Always show preview diff before writing
- Ask explicitly before replacing `### Activation Priorities`
- Route to `customer-context:tech-stack` if > 2 new tech items are found
- Never edit or delete existing Chat & Call Log entries

## Skills Called

| Skill | Purpose |
|---|---|
| `gong` | Pull new call briefs since last context update |
| `gdrive-desktop` | Check account folder for new or changed docs |
| `customer-context:tech-stack` | Handle tech stack updates if > 2 new items found |
