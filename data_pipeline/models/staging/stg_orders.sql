-- Staging for orders. Grain = one row per LINE ITEM on a ticket.
-- An order_id can appear on several rows (one per item), so we build a
-- surrogate key from (order_id, line_number) that IS unique per row.
select
    order_id || '-' || line_number as order_line_id,  -- unique per line
    order_id,
    line_number,
    customer_id,
    product_id,
    order_date,
    quantity
from {{ source('coffee_shop', 'raw_orders') }}
