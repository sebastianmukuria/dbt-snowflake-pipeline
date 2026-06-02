-- =============================================================================
-- DIMENSION TABLE: dim_customers
-- One row per customer with their descriptive attributes PLUS a few rolled-up
-- metrics (total spend, order count, favorite category). Pairs with fct_orders
-- to form a classic star schema: facts you measure, dimensions you slice by.
-- =============================================================================
with customers as (
    select * from {{ ref('stg_customers') }}
),

orders as (
    select * from {{ ref('fct_orders') }}
),

-- Per-customer rollups from the fact table.
customer_orders as (
    select
        customer_id,
        count(distinct order_id) as lifetime_orders,
        sum(revenue)             as lifetime_spend,
        min(order_date)          as first_order_date,
        max(order_date)          as most_recent_order_date
    from orders
    group by customer_id
),

-- Each customer's favorite category = the one they've spent the most on.
-- QUALIFY + a window function is the clean Snowflake way to pick "top 1 per group".
favorite_category as (
    select
        customer_id,
        category as favorite_category
    from orders
    group by customer_id, category
    qualify row_number() over (
        partition by customer_id
        order by sum(revenue) desc, category
    ) = 1
)

select
    customers.customer_id,
    customers.customer_name,
    customers.city,
    customers.signup_date,
    -- coalesce so customers with zero orders show 0, not NULL:
    coalesce(customer_orders.lifetime_orders, 0) as lifetime_orders,
    coalesce(customer_orders.lifetime_spend, 0)  as lifetime_spend,
    customer_orders.first_order_date,
    customer_orders.most_recent_order_date,
    favorite_category.favorite_category
from customers
left join customer_orders on customers.customer_id = customer_orders.customer_id
left join favorite_category on customers.customer_id = favorite_category.customer_id
