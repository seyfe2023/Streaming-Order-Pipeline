{{ config(
    materialized='table'
) }}

SELECT
    DATE(created_at) AS order_date,
    COUNT(*) AS total_orders,
    SUM(amount) AS revenue
FROM public.staging_orders
GROUP BY 1
ORDER BY order_date DESC