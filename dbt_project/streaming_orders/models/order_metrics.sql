{{ config(
    materialized='table',      -- Create as a table for faster queries
    primary_key='order_date'    -- Set order_date as primary key for upserts
) }}

SELECT
    DATE(created_at) AS order_date,    -- Extract date from timestamp
    COUNT(*) AS total_orders,           -- Count number of orders per day
    SUM(amount) AS revenue              -- Calculate total daily revenue
FROM public.staging_orders
GROUP BY 1                               -- Group by order_date
ORDER BY order_date DESC                  -- Show most recent days first