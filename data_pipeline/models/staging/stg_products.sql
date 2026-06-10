-- Staging for products. We rename `price` to `unit_price` to be explicit.
select
    product_id,
    product_name,
    category,
    price as unit_price
from {{ source('coffee_shop', 'raw_products') }}
