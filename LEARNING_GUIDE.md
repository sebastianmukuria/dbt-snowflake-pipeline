# Learning Guide & Interview Cheat Sheet — Coffee Shop Pipeline

One section per tool: what it is, what to *do in this project* to learn it, and a
line you can actually say in the interview. Suggested order is at the bottom.

---

## 1. SQL (preferably Snowflake)

**What it is:** the language for transforming data. Snowflake SQL ≈ standard SQL plus
a few extras (`QUALIFY`, `::` casting, semi-structured support).

**Do this:** before letting dbt do it, write these by hand in a Snowflake worksheet
against your loaded seed tables:
```sql
-- join + aggregate: revenue per category
select p.category, sum(o.quantity * p.price) as revenue
from dbt_db.dbt_schema.raw_orders o
join dbt_db.dbt_schema.raw_products p on o.product_id = p.product_id
group by p.category
order by revenue desc;

-- window function: rank products by revenue within each category
select product_name, category,
       sum(quantity * price) as revenue,
       rank() over (partition by category order by sum(quantity * price) desc) as rnk
from dbt_db.dbt_schema.raw_orders o
join dbt_db.dbt_schema.raw_products p using (product_id)
group by product_name, category;
```
**Know cold:** JOIN types, GROUP BY + aggregates, WHERE vs HAVING, CTEs (`WITH`),
window functions, `CASE WHEN`.

**Say it:** "I'm comfortable with joins, aggregations, CTEs and window functions, and
I've written them both directly in Snowflake and inside dbt models."

---

## 2. Snowflake

**What it is:** a cloud data warehouse. Big idea: **storage and compute are separate**.
Compute = a "warehouse" you size and start/stop on its own.

**Do this:** run [`snowflake_setup.sql`](data_pipeline/snowflake_setup.sql) and read each
line — warehouse, database, schema, role, grants. Notice `auto_suspend = 60` (saves credits).

**Know cold:** warehouse vs database vs schema; roles & grants (RBAC); why separating
compute from storage matters (scale independently, no contention).

**Say it:** "Snowflake splits storage from compute, so I run a small auto-suspending
warehouse for dev and only scale up for heavy jobs."

---

## 3. dbt — spend the most time here (it's the core skill)

**What it is:** you write `SELECT` statements; dbt builds them into tables/views in the
right order, with tests and docs.

**Do this — and understand each idea in the code:**
- **Seeds** — `dbt seed` loads `seeds/*.csv` into Snowflake. That's our raw layer.
- **`ref()`** — how models depend on each other; builds the **DAG** (see `fct_orders.sql`).
- **Materializations** — staging = `view`, marts = `table` (set in `dbt_project.yml`). Know why.
- **Layers** — staging (clean) → marts (business logic / joins / aggregates).
- **Tests** — generic in the `_*.yml` files (`unique`, `not_null`, `relationships`,
  `accepted_values`) and a **singular** one in `tests/assert_quantity_is_positive.sql`.
- **Macro** — `macros/calc_revenue.sql`, reused in `fct_orders`.
- **Docs** — `dbt docs generate && dbt docs serve` → searchable docs + lineage graph.

**Say it:** "I structure dbt as staging → marts, use `ref()` so dbt manages build order,
materialize staging as views and marts as tables, and cover models with generic and
singular tests. Reusable logic goes in macros."

---

## 4. Git

**What it is:** version control. Analytics SQL ships like software — branch, commit, PR.

**Do this:**
```bash
git add -A
git commit -m "Coffee shop pipeline: seeds, staging, marts, tests"
git checkout -b feature/add-customer-ltv      # branch for a change
# ...edit a model, commit...
# push and open a Pull Request on GitHub for review
```
**Know cold:** add/commit/push/pull, branches, what a PR is. `.gitignore` keeps
`target/`, `dbt_packages/`, and secrets out of the repo.

**Say it:** "I treat SQL as code — feature branch, commit, PR for review, merge — and I
never commit credentials; those live in `profiles.yml` outside the repo."

---

## 5. Sigma

**What it is:** a cloud BI tool with a spreadsheet feel that queries Snowflake **live**.
Analysts build dashboards directly on your dbt marts — no data export.

**Do this (optional, needs a Sigma trial):** connect Sigma → Snowflake, open
`dbt_db.dbt_schema.daily_sales`, make a line chart of `total_revenue` over `order_date`,
and a bar chart of revenue by `category` from `fct_orders`.

**Know cold even without a trial:** Sigma sits on **top** of the stack and reads the
tables dbt builds, so clean, well-named, tested marts make Sigma easy.

**Say it:** "Sigma queries Snowflake live, so my dbt job is to hand it tidy, tested marts
like `daily_sales` that match how the business thinks."

---

## 6. Cursor

**What it is:** a VS Code–based editor with AI built in (same extensions/shortcuts).

**Do this:** open this folder in Cursor; use `Cmd+K` to edit a SQL file from a prompt,
`Cmd+L` to chat about the code, and install the **dbt Power User** extension for
SQL/dbt autocomplete and inline `ref` navigation.

**Say it:** "I use Cursor as my editor — it's VS Code with AI, so I get inline edits and
can ask questions about the project while writing models."

---

## 7. Claude Code

**What it is:** Anthropic's terminal AI assistant (it built this project with you). It
reads your repo, edits files, and runs commands like `dbt`.

**Do this:** run `claude` in the project and try:
- "Explain `fct_orders.sql` line by line."
- "Add a `dim_customers` mart with each customer's total spend."
- "`dbt test` failed — why, and how do I fix it?"

**Say it:** "I use Claude Code to scaffold models, debug failing tests, and explain
unfamiliar SQL — it can run dbt and read the errors itself."

---

## Suggested learning order
1. **SQL** by hand in a Snowflake worksheet.
2. **Snowflake** objects via `snowflake_setup.sql`.
3. **dbt** — read every file here, then `dbt seed` / `run` / `test` / `docs serve`. *(most time)*
4. **Git** — branch, commit, push your changes.
5. **Sigma** — one chart on `daily_sales`.
6. **Cursor + Claude Code** — you pick these up just by doing 1–5 inside them.
