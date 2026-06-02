-- =============================================================================
-- FACT TABLE: fct_orders
-- The business-ready table. One row per item ordered, enriched with the
-- customer and product details and the revenue for that line.
-- This is where JOINs and business logic belong (not in staging).
-- =============================================================================
with orders as (
    select * from {{ ref('stg_orders') }}
),

customers as (
    select * from {{ ref('stg_customers') }}
),

products as (
    select * from {{ ref('stg_products') }}
)

select
    orders.order_id,
    orders.order_date,
    customers.customer_id,
    customers.customer_name,
    customers.city,
    products.product_id,
    products.product_name,
    products.category,
    orders.quantity,
    products.unit_price,
    -- reuse the macro instead of writing quantity * unit_price inline:
    {{ calc_revenue('orders.quantity', 'products.unit_price') }} as revenue
from orders
left join customers on orders.customer_id = customers.customer_id
left join products  on orders.product_id  = products.product_id
