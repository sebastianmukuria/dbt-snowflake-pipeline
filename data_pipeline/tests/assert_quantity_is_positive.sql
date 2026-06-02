-- A singular test is just a query that should return ZERO rows.
-- If any row comes back, the test fails and shows you the offending data.
-- Rule: you can't order a negative or zero quantity of coffee.
select
    order_id,
    quantity
from {{ ref('fct_orders') }}
where quantity <= 0
