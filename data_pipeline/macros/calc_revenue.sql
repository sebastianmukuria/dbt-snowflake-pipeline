-- A macro is reusable SQL. Define the revenue math once, call it anywhere with
-- double curly braces, e.g.  calc_revenue('quantity', 'unit_price')  wrapped in {{ }}.
-- Keeps the logic consistent across every model that needs it.
{% macro calc_revenue(quantity_col, price_col) %}
    ({{ quantity_col }} * {{ price_col }})::number(10, 2)
{% endmacro %}
