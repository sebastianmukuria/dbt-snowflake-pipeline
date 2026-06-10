-- Staging: one model per raw source. Light cleanup only (rename/cast), no joins.
-- Reads from the declared source (see _sources.yml), not the seed directly.
select
    customer_id,
    customer_name,
    city,
    signup_date
from {{ source('coffee_shop', 'raw_customers') }}
