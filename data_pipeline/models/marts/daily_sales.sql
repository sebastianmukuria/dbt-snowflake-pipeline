-- =============================================================================
-- MART: daily_sales
-- A simple aggregate for dashboards: revenue and order counts per day.
-- This is the kind of table you'd chart in Sigma (revenue over time).
-- =============================================================================
select
    order_date,
    count(distinct order_id) as num_orders,
    sum(quantity)            as items_sold,
    sum(revenue)             as total_revenue
from {{ ref('fct_orders') }}
group by order_date
order by order_date
