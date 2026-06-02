# ☕ Coffee Shop Analytics — Beginner Data Pipeline

A from-scratch project to learn the tools in the job description:

> SQL (preferably Snowflake) · Git · Sigma · dbt · Snowflake · Claude Code · Cursor

We model a tiny coffee shop. Three raw CSVs (customers, products, orders) get
loaded into **Snowflake**, transformed with **dbt** into clean tables, tested,
and rolled up into a `daily_sales` table you can chart in **Sigma**. All the SQL
lives in **Git**; you write it in **Cursor** with **Claude Code** assisting.

---

## How the tools fit together

```
  raw CSV seeds        Snowflake            dbt                    Sigma
 ┌─────────────┐     ┌──────────┐    ┌────────────────┐     ┌──────────────┐
 │ customers    │     │ warehouse │    │ staging models  │     │ chart        │
 │ products     │──▶ │ + storage │──▶│ fact + daily    │──▶ │ revenue/day  │
 │ orders       │     │ (dbt seed)│    │ tests + macro   │     │ on the marts │
 └─────────────┘     └──────────┘    └────────────────┘     └──────────────┘
       written in Cursor (editor) with Claude Code (AI assistant in terminal),
       versioned in Git the whole way.
```

## The data flow (dbt works out the build order itself)

```
raw_customers → stg_customers ┐
raw_products  → stg_products  ┤→ fct_orders → daily_sales
raw_orders    → stg_orders    ┘
```

- **staging/** — one model per raw table, light cleanup only, built as **views**.
- **fct_orders** — the fact table: joins orders+customers+products, adds revenue.
- **daily_sales** — revenue/orders per day, built as a **table** for dashboards.

---

## Project layout

```
data_pipeline/
├── snowflake_setup.sql        ← run once in Snowflake (warehouse/db/role)
├── dbt_project.yml            ← project config + seed column types
├── seeds/                     ← the RAW data (CSV) -> `dbt seed` loads to Snowflake
│   ├── raw_customers.csv
│   ├── raw_products.csv
│   └── raw_orders.csv
├── models/
│   ├── staging/               ← stg_customers / stg_products / stg_orders (+ _staging.yml tests)
│   └── marts/                 ← fct_orders, daily_sales (+ _marts.yml tests)
├── macros/
│   └── calc_revenue.sql       ← reusable SQL (a macro)
└── tests/
    └── assert_quantity_is_positive.sql   ← a custom (singular) test
```

---

## Run it (step by step)

### 1. Create a free Snowflake trial
https://signup.snowflake.com — Standard edition, any cloud, no credit card
(30 days / $400 credits). Note your **account identifier** (looks like `abcd-xy12345`).

### 2. Create the warehouse/db/role
Open a Snowflake **Worksheet**, paste in [`snowflake_setup.sql`](data_pipeline/snowflake_setup.sql),
replace `<YOUR_USERNAME>`, run it.

### 3. Point dbt at your account
Edit `~/.dbt/profiles.yml` → set `account`, `user`, `password`. Then:
```bash
cd data_pipeline
dbt debug      # expect "All checks passed!"
```

### 4. Build the pipeline
```bash
dbt seed       # load the 3 CSVs into Snowflake as tables
dbt run        # build staging + marts
dbt test       # run all 14 data tests
dbt build      # (shortcut) seed + run + test in dependency order
```
Then peek at the result in a Snowflake worksheet:
```sql
select * from dbt_db.dbt_schema.daily_sales order by order_date;
```

### 5. See the lineage graph + docs
```bash
dbt docs generate && dbt docs serve
```

### 6. (Optional) Chart it in Sigma
Connect Sigma to Snowflake, open `dbt_db.dbt_schema.daily_sales`, plot
`total_revenue` by `order_date`.

---

## Everyday dbt commands

| Command | Does |
|---|---|
| `dbt seed` | Load the CSVs in `seeds/` into the warehouse |
| `dbt run` | Build all models |
| `dbt run --select fct_orders+` | Build fct_orders and everything downstream |
| `dbt test` | Run all tests |
| `dbt build` | seed + run + test, in order |
| `dbt docs generate && dbt docs serve` | Docs site + lineage graph |

➡️ **New here? Read [`LEARNING_GUIDE.md`](LEARNING_GUIDE.md)** — one section per tool
with what to practice and what to say in the interview.
