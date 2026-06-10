---
title: Coffee Shop Sales
---

A dashboard built on the dbt marts from my [dbt + Snowflake pipeline](https://github.com/sebastianmukuria/dbt-snowflake-pipeline).
The data flows raw CSV → Snowflake → dbt models (`fct_orders`, `daily_sales`, `dim_customers`)
→ this report. Numbers cover six months of a made-up coffee shop.

```sql kpis
select
    sum(total_revenue) as total_revenue,
    sum(num_orders)    as total_orders,
    sum(items_sold)    as items_sold
from coffee_shop.daily_sales
```

```sql customers
select count(*) as total_customers from coffee_shop.dim_customers
```

<BigValue data={kpis} value=total_revenue fmt=usd0/>
<BigValue data={kpis} value=total_orders/>
<BigValue data={kpis} value=items_sold/>
<BigValue data={customers} value=total_customers/>

## Revenue over time

```sql revenue_monthly
select
    date_trunc('month', order_date::date) as month,
    sum(total_revenue) as revenue
from coffee_shop.daily_sales
group by 1
order by 1
```

<LineChart data={revenue_monthly} x=month y=revenue yFmt=usd0 title="Monthly revenue"/>

## Where the money comes from

```sql revenue_by_category
select category, sum(revenue) as revenue
from coffee_shop.fct_orders
group by 1
order by 2 desc
```

```sql revenue_by_city
select city, sum(revenue) as revenue
from coffee_shop.fct_orders
group by 1
order by 2 desc
```

<BarChart data={revenue_by_category} x=category y=revenue yFmt=usd0 title="Revenue by category"/>

<BarChart data={revenue_by_city} x=city y=revenue yFmt=usd0 title="Revenue by city"/>

## Top products

```sql top_products
select
    product_name,
    sum(quantity) as units_sold,
    sum(revenue)  as revenue
from coffee_shop.fct_orders
group by 1
order by revenue desc
limit 10
```

<BarChart data={top_products} x=product_name y=revenue yFmt=usd0 swapXY=true title="Top 10 products by revenue"/>

## Top customers

```sql top_customers
select
    customer_name,
    city,
    lifetime_orders,
    lifetime_spend,
    favorite_category
from coffee_shop.dim_customers
order by lifetime_spend desc
limit 10
```

<DataTable data={top_customers}>
    <Column id=customer_name title="Customer"/>
    <Column id=city/>
    <Column id=lifetime_orders title="Orders" align=center/>
    <Column id=lifetime_spend title="Lifetime spend" fmt=usd2/>
    <Column id=favorite_category title="Favorite"/>
</DataTable>
