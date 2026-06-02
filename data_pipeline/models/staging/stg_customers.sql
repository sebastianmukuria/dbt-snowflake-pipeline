-- Staging: one model per raw table. Light cleanup only (rename/cast), no joins.
-- We read from the seed with the ref() function, just like any other model.
select
    customer_id,
    customer_name,
    city,
    signup_date
from {{ ref('raw_customers') }}
