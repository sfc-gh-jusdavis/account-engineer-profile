# Architecture Diagrams Examples

## Example 1: Data Model Diagram

```markdown
# Data Model - Cortex Agent Demo

Author: SE Community
Last Updated: 2025-01-15
Expires: 2025-02-14

## Diagram

\`\`\`mermaid
erDiagram
    RAW_CUSTOMERS ||--o{ RAW_ORDERS : places
    RAW_CUSTOMERS ||--o{ RAW_FEEDBACK : provides
    STG_CUSTOMERS ||--|| RAW_CUSTOMERS : "cleaned from"
    
    RAW_CUSTOMERS {
        int customer_id PK
        string name
        string email UK
        timestamp created_at
    }
    
    RAW_ORDERS {
        int order_id PK
        int customer_id FK
        decimal total_amount
        timestamp order_date
    }
    
    RAW_FEEDBACK {
        int feedback_id PK
        int customer_id FK
        string feedback_text
        int rating
    }
    
    STG_CUSTOMERS {
        int customer_id PK
        string name
        string email UK
        string customer_segment
    }
\`\`\`

## Component Descriptions

### RAW_CUSTOMERS
- Purpose: Raw customer data from source system
- Location: SNOWFLAKE_EXAMPLE.CORTEX_AGENT.RAW_CUSTOMERS
```

## Example 2: Data Flow Diagram

```markdown
# Data Flow - Cortex Agent Demo

## Diagram

\`\`\`mermaid
graph LR
    subgraph Sources
        CSV[CSV Upload]
        API[REST API]
    end
    
    subgraph Ingestion
        Stage[Internal Stage]
        Copy[COPY INTO]
    end
    
    subgraph Processing
        Raw[(RAW_ Tables)]
        Stg[(STG_ Tables)]
        Analytics[(Analytics)]
    end
    
    subgraph Consumption
        Agent[Cortex Agent]
        Dashboard[Streamlit]
    end
    
    CSV --> Stage
    API --> Stage
    Stage --> Copy
    Copy --> Raw
    Raw --> Stg
    Stg --> Analytics
    Analytics --> Agent
    Analytics --> Dashboard
\`\`\`
```

