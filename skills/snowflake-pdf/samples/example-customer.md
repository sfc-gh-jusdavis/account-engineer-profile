---
title: "snowflake-pdf Customer-Facing Sample"
subtitle: "Sample document used to verify customer-facing rendering"
customer: "Acme Corp"
author: "Snowflake Solution Engineering"
audience: "customer-facing"
date: "May 6, 2026"
---

# Customer-Facing Sample

Welcome. This document is written **to you**, not about you.

## What you'll do

1. Sign in to your Snowflake account using your **PrivateLink Account URL**.
2. Run the following in a worksheet:

   ```sql
   SELECT SYSTEM$GET_PRIVATELINK_CONFIG();
   ```

3. Copy the output for use during DNS configuration.

## Why this matters

You verified earlier that DNS resolves the privatelink hostnames to your Private Endpoint. This step gives you the canonical list of URLs that must resolve privately.

> If anything is unclear, contact Snowflake Support.
