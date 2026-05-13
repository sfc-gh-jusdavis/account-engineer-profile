---
name: similar-use-cases
description: "Find similar use cases and customer patterns using Glean search. Use when: 'find similar use cases', 'who else has done [use case]', 'similar customers to [account]', 'patterns for [industry/use case]', 'reference customers for [technology]'."
---

# Similar Use Cases

## When to Use

- Finding reference customers with similar use cases
- Looking for patterns in how other customers solved similar problems
- Preparing for a new use case by learning from past wins
- "find similar use cases to [description]"
- "who else has done [use case type]"
- "reference customers for [technology]"

## Workflow

### Step 1: Gather Search Criteria

**Ask if not provided:**
```
What should I search for? (examples)
- Industry: "financial services data warehouse migration"
- Technology: "Redshift migration to Snowflake"
- Use case type: "real-time data sharing"
- Pain point: "HIPAA compliance data platform"
```

### Step 2: Search with Glean

Use `mcp__glean__search` tool with targeted keywords:

**For use case patterns:**
```
Query: "[use case type] snowflake customer win"
```

**For industry patterns:**
```
Query: "[industry] snowflake implementation success"
```

**For technology migrations:**
```
Query: "[source technology] migration snowflake lessons learned"
```

### Step 3: Search Salesforce Use Cases

Also query Snowhouse for internal use case data:

```sql
SELECT 
    ACCOUNT_NAME,
    USE_CASE_NAME,
    INDUSTRY_USE_CASE,
    TECHNICAL_USE_CASE,
    USE_CASE_DESCRIPTION,
    USE_CASE_STAGE,
    COMPETITORS,
    USE_CASE_LEAD_SE_NAME
FROM MDM.MDM_INTERFACES.DIM_USE_CASE
WHERE USE_CASE_STATUS = 'Active'
  AND USE_CASE_STAGE IN ('4 - Use Case Won / Migration Plan', '5 - Implementation In Progress', '6 - Live in Production')
  AND (
    UPPER(TECHNICAL_USE_CASE) LIKE UPPER('%<search term>%')
    OR UPPER(USE_CASE_DESCRIPTION) LIKE UPPER('%<search term>%')
    OR UPPER(INDUSTRY_USE_CASE) LIKE UPPER('%<search term>%')
  )
ORDER BY USE_CASE_STAGE DESC
LIMIT 20
```

### Step 4: Format Results

```markdown
# Similar Use Cases: [Search Term]
*Generated: [timestamp]*

## Internal SFDC Matches

### [Account Name] - [Use Case Name]
- **Stage**: [Stage]
- **Industry**: [INDUSTRY_USE_CASE]
- **Technical**: [TECHNICAL_USE_CASE]
- **Lead SE**: [Name] (contact for reference)
- **Competitors**: [COMPETITORS]

**Description:**
[USE_CASE_DESCRIPTION]

---

## Glean Results

### [Document Title]
**Source**: [App/Location]
**Summary**: [Key points from document]
**Link**: [URL]

---
```

### Step 5: Save to Google Drive (if requested)

If searching for a specific account's benefit:
```bash
mkdir -p "<gdrive_base>/<Account>/cortex-context"
```

Write to: `<account>/cortex-context/similar-use-cases.md`

## Tips for Better Results

| Looking for... | Search terms |
|----------------|--------------|
| Migration patterns | "[source] migration snowflake" |
| Industry examples | "[industry] snowflake success story" |
| Technical patterns | "[feature] implementation customer" |
| Competitive wins | "[competitor] displacement snowflake" |

## Stopping Points

- **Ask** for search criteria if vague
- **Confirm** search terms before executing

## Output

- Console: Formatted list of similar use cases with contacts
- File (optional): `<account>/cortex-context/similar-use-cases.md`
