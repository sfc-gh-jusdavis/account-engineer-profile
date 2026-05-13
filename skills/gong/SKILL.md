---
name: gong
description: "Find Gong call summaries in Snowhouse. Use when: user asks about Gong, Gong calls, call summaries, meeting briefs, what was discussed in a call. Triggers: gong, gong call, call summary, meeting summary, what was discussed."
---

# Gong Call Summaries

Retrieve Gong call data from Snowhouse for any account.

## Data Available

| Data | Available | Location |
|------|-----------|----------|
| Call summaries/briefs | Yes | `GONG_CALL_BRIEF_C` |
| Call metadata (date, title, duration) | Yes | Various columns |
| Full transcripts | No | Stay in Gong platform |

## Data Flow

```
Gong → Salesforce (custom objects) → Fivetran → Snowhouse
```

## Key Tables (Snowhouse)

| Table | Purpose |
|-------|---------|
| `FIVETRAN.SALESFORCE.GONG_GONG_CALL_C` | Primary call data with summaries |
| `FIVETRAN.SALESFORCE.ACCOUNT` | Account name → ID lookup |

### Important Columns in GONG_GONG_CALL_C

- `GONG_CALL_BRIEF_C` - Call summary text
- `GONG_CALL_START_C` - Call timestamp
- `GONG_TITLE_C` - Call title
- `GONG_PRIMARY_ACCOUNT_C` - Salesforce Account ID (foreign key)

## Workflow

### Step 1: Get Account ID

Query Salesforce accounts with fuzzy match:

```sql
SELECT ID, NAME 
FROM FIVETRAN.SALESFORCE.ACCOUNT 
WHERE LOWER(NAME) LIKE '%<account_name>%'
LIMIT 10
```

If multiple matches, present options to user.

### Step 2: Query Gong Calls

```sql
SELECT 
    GONG_CALL_START_C AS call_date,
    GONG_TITLE_C AS call_title,
    GONG_CALL_BRIEF_C AS summary
FROM FIVETRAN.SALESFORCE.GONG_GONG_CALL_C
WHERE GONG_PRIMARY_ACCOUNT_C = '<account_id>'
ORDER BY GONG_CALL_START_C DESC
LIMIT 10
```

**With date filter:**
```sql
WHERE GONG_PRIMARY_ACCOUNT_C = '<account_id>'
  AND GONG_CALL_START_C::DATE = '<date>'
```

### Step 3: Present Results

Return:
- Call title
- Call date/time
- Summary (if available - some older calls have NULL summaries)

## Stopping Points

- **Step 1**: If multiple account matches, ask user to clarify which account

## Connection

Use `SNOWHOUSE_AWS_US_WEST_2` connection (read-only).

## Output

Call summary text and metadata. Note: Full transcripts are not available in Snowhouse.
