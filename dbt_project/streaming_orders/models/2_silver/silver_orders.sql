{{ config(materialized='table') }}

SELECT 
    order_id,
    customer_id,
    product_id,
    amount,
    created_at,
    CURRENT_TIMESTAMP as processed_at
FROM {{ source('public', 'staging_orders') }}  
WHERE amount > 0 
  AND customer_id IS NOT NULL