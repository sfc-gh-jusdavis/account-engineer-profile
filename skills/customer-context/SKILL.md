---
name: customer-context
description: "Initialize and maintain context.md for a customer activation project.
  Use when: 'init context for [account]', 'set up context', 'new customer project',
  'update tech stack', 'log tech stack', 'update context from this chat',
  'capture findings', 'log Gong call to context', 'refresh context from GDrive'.
  Routes to init, tech-stack, or chat-update sub-skill."
---

# Customer Context

Parent skill for managing `context.md` in a customer activation project. Every customer gets their own CCD project; `context.md` lives at the project root and is the single source of truth for that engagement.

## Pre-flight (always run first)

1. **CWD** — confirm the current working directory is the customer project root.
2. **`context.md` exists?**
   - For `init`: confirm CWD before writing (warn if file already exists).
   - For `tech-stack` and `chat-update`: if `context.md` is missing, offer to run `init` first.

If either check is unclear, use `ask_user_question` before proceeding.

## Routing Table

| User intent | Sub-skill |
|---|---|
| "init context", "set up context for [account]", "new customer project" | `customer-context:init` |
| "log tech stack", "add tech stack", "update tech stack", tech mention in chat | `customer-context:tech-stack` |
| "update context from this chat", "capture findings", "log Gong call", "update from GDrive" | `customer-context:chat-update` |

## `context.md` Structure Reference

The file uses four groups ordered by **decreasing mutability** — static intel at top, living work at bottom.

```
# Context: [Account Name]
*Initialized: [date] | Last updated: [date] | Phase: Activation*
*Account Engineer: [name]*

---

## 1. Account Identity
### Overview
### Account Team
### Key Customer Contacts

---

## 2. Deal Intelligence
### Deal Timeline
### Use Cases
### Pain Points & Objections
### Competitor Landscape

---

## 3. Technical Landscape
### Current Architecture
### Target Architecture
### Tech Stack
#### Inbound to Snowflake
#### Outbound from Snowflake
#### Peripheral Services

---

## 4. Activation Work
### Activation Priorities
### Upcoming Milestones
### Chat & Call Log
```

## Section Ownership

| Skill | Groups it writes to |
|---|---|
| `customer-context:init` | All groups — full file population |
| `customer-context:tech-stack` | Group 3: Tech Stack subsections only |
| `customer-context:chat-update` | Group 4: always; Groups 1-3: surgical field/row updates only |

## Privacy Rule (HIGH PRIORITY)

- Never write real customer company names, employee names, or account IDs into skill files.
- All examples and templates use `[Account Name]`, `[Contact Name]`, `[Role]` placeholders.
- Customer-specific context belongs in the customer's CCD project, not in the profile repo.
