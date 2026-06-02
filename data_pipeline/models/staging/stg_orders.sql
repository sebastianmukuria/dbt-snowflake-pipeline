-- Staging for orders (one row per line on a ticket).
select
    order_id,
    customer_id,
    product_id,
    order_date,
    quantity
from {{ ref('raw_orders') }}
