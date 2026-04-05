{{ config(
    materialized='table'
) }}

SELECT
    DATE(created_at) AS order_date,
    COUNT(*) AS total_orders,
    SUM(amount) AS revenue,
    CURRENT_TIMESTAMP AS updated_at
FROM {{ ref('silver_orders') }}  
GROUP BY 1
ORDER BY order_date DESC