---
name: demo-ops:synthetic-data
description: "Fabricate realistic non-PII data for demos. SQL generators, Faker UDFs, Cortex COMPLETE for narrative text, AI_EXTRACT for documents, time-series patterns, mandatory PII grep. Use whenever a demo needs data and real data isn't appropriate. Triggers: synthetic data, fake data, mock data, demo data, generate data, fabricate data, faker, test data, sample data, dummy data, generator, populate demo tables, create fake users, fake accounts, fake transactions."
---

Fabricate realistic non-PII data for demos. The privacy rule is absolute: no real names, no real account IDs, no real internal email domains.

## Core principles

1. **Schema first**. Define target table DDL before generating data.
2. **Determinism**. Always seed: `RANDOM(42)`, `Faker.seed(42)`, `np.random.seed(42)`.
3. **Volume awareness**. Cortex `COMPLETE` per-row is expensive — reserve for narrative columns. Use SQL generators for bulk numerics/categoricals.
4. **Names tell the story**. Pick column names a stranger could read once.
5. **Anti-PII grep before publish**.

## Pattern 1: Pure SQL volume

```sql
CREATE OR REPLACE TABLE DEMO_<topic>.RAW.ACCOUNTS AS
SELECT
    SEQ4() + 1                                                AS ACCOUNT_ID,
    'ACCT-' || LPAD(SEQ4()::STRING, 8, '0')                   AS ACCOUNT_CODE,
    CASE MOD(ABS(RANDOM(42 + SEQ4())), 4)
        WHEN 0 THEN 'Enterprise'
        WHEN 1 THEN 'Mid-Market'
        WHEN 2 THEN 'SMB'
        ELSE 'Startup'
    END                                                       AS SEGMENT,
    ROUND(ABS(NORMAL(500000, 250000, RANDOM(43 + SEQ4()))), 2) AS ARR_USD,
    DATEADD('day', UNIFORM(-720, 0, RANDOM(44 + SEQ4())), CURRENT_DATE()) AS CREATED_DATE
FROM TABLE(GENERATOR(ROWCOUNT => 100000));
```

| Function | Use |
|---|---|
| `TABLE(GENERATOR(ROWCOUNT => N))` | Bulk row factory |
| `SEQ4()` | Deterministic monotonic ID |
| `RANDOM(seed)` | Seeded random int |
| `UNIFORM(lo, hi, RANDOM(seed))` | Uniform draw |
| `NORMAL(mean, stddev, RANDOM(seed))` | Normal draw |
| `MOD(ABS(RANDOM(seed)), N)` | Bucketed categorical |

## Pattern 2: Faker via Python UDF

```sql
CREATE OR REPLACE FUNCTION DEMO_<topic>.RAW.FAKE_PERSON(seed INT)
RETURNS VARIANT
LANGUAGE PYTHON
RUNTIME_VERSION = '3.11'
PACKAGES = ('faker')
HANDLER = 'fake_person'
AS
$$
from faker import Faker
def fake_person(seed: int):
    Faker.seed(seed)
    fake = Faker('en_US')
    return {
        'first_name': fake.first_name(),
        'last_name':  fake.last_name(),
        'email':      fake.email(domain='example.com'),
        'city':       fake.city(),
        'state':      fake.state_abbr(),
    }
$$;
```

**Always pin email domain to `example.com` / `example.org` / `mailinator.com`** — Faker default may produce real-looking corp domains.

## Pattern 3: Narrative text via Cortex COMPLETE

> Account constraint: `SNOWFLAKE.CORTEX.COMPLETE` may only support **string format** on this account (not messages array). Verify before relying on multi-turn.

```sql
CREATE OR REPLACE TABLE DEMO_<topic>.RAW.SUPPORT_TICKETS AS
SELECT
    SEQ4() + 1                                                            AS TICKET_ID,
    a.ACCOUNT_ID,
    DATEADD('day', UNIFORM(-90, 0, RANDOM(SEQ4())), CURRENT_DATE())       AS CREATED_DATE,
    SNOWFLAKE.CORTEX.COMPLETE(
        'mistral-7b',
        'Write a 3-sentence fictional support ticket from a fictional B2B SaaS customer. ' ||
        'Account segment: ' || a.SEGMENT || '. ' ||
        'Do NOT use any real company or person names.'
    )                                                                     AS BODY
FROM (SELECT * FROM DEMO_<topic>.RAW.ACCOUNTS SAMPLE (500 ROWS)) a;
```

Cost guardrails: sample first; pick the smallest model that produces acceptable text; cache by inserting once.

## Pattern 4: Documents via AI_EXTRACT

```sql
SELECT
    relative_path,
    AI_EXTRACT(
        TO_FILE('@demo_stage', relative_path),
        ['invoice_number', 'vendor_name', 'total_amount', 'invoice_date']
    ) AS EXTRACTED
FROM DIRECTORY('@demo_stage')
WHERE relative_path ILIKE 'fake_invoice_%.pdf';
```

## Pattern 5: Time-series with seasonality

```sql
SELECT
    DATEADD('day', SEQ4(), DATE '2024-01-01')                              AS DAY,
    ROUND(
        10000
        + 50 * SEQ4()
        + 1500 * SIN(2 * 3.14159 * SEQ4() / 7)
        + NORMAL(0, 500, RANDOM(SEQ4()))
    , 2)                                                                   AS REVENUE_USD
FROM TABLE(GENERATOR(ROWCOUNT => 365));
```

## Pre-publish PII grep (mandatory)

```bash
# Replace <internal-domain> and <known-real-name> with the literal patterns
# you need to forbid in your environment (e.g. your company email domain,
# real customer account names).
grep -rEi '@<internal-domain>|<known-real-name>' .
# Expected: zero matches.
```

## Anti-patterns

| Anti-pattern | Fix |
|---|---|
| Faker default email domains | Pin to `example.com` |
| Real customer names "for realism" | Seeded Faker |
| Cortex COMPLETE over 100k rows | Sample <1k; smallest model |
| No seed | `RANDOM(42)`, `Faker.seed(42)` |
| Synthetic data outside demo schema | Live under `DEMO_<topic>.RAW` |
| Skipped PII grep | Always run before declaring done |

## Reference

- Sibling skill: `demo-ops:snowflake-conventions` for DB/schema setup
- Verify Cortex syntax via `snowflake_product_docs` before relying on advanced patterns.
