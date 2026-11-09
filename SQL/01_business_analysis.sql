
-- 1. Total Orders
SELECT COUNT(*) AS total_orders
FROM orders;


-- 2. Orders by Status
SELECT
    order_status,
    COUNT(*) AS total_orders
FROM orders
GROUP BY order_status
ORDER BY total_orders DESC;



-- 3. Monthly Order Trends
SELECT
    DATE_TRUNC('month', order_purchase_timestamp) AS order_month,
    COUNT(*) AS total_orders
FROM orders
GROUP BY order_month
ORDER BY order_month;



-- 4. Total Revenue
SELECT
    ROUND(SUM(price), 2) AS total_revenue
FROM order_items;



-- 5. Total Freight Charges
SELECT
    ROUND(SUM(freight_value), 2) AS total_freight
FROM order_items;


-- 6. Average Order Value
SELECT
    ROUND(
        SUM(price) / COUNT(DISTINCT order_id),
        2
    ) AS average_order_value
FROM order_items;



-- 7. Total Delivered Orders
SELECT
    COUNT(*) AS total_delivered_orders
FROM orders
WHERE order_status = 'delivered';



-- 8. Late Delivery Analysis
SELECT
    COUNT(*) AS total_delivered_orders,

    COUNT(*) FILTER (
        WHERE order_delivered_customer_date >
              order_estimated_delivery_date
    ) AS late_orders,

    COUNT(*) FILTER (
        WHERE order_delivered_customer_date <=
              order_estimated_delivery_date
    ) AS on_time_orders

FROM orders
WHERE order_status = 'delivered';


-- 9. Late Delivery Percentage
SELECT
    ROUND(
        COUNT(*) FILTER (
            WHERE order_delivered_customer_date >
                  order_estimated_delivery_date
        ) * 100.0 /
        COUNT(*) FILTER (
            WHERE order_delivered_customer_date IS NOT NULL
              AND order_estimated_delivery_date IS NOT NULL
        ),
        2
    ) AS late_delivery_percentage
FROM orders
WHERE order_status = 'delivered';


-- 10. Average Delivery Time
SELECT
    ROUND(
        AVG(
            EXTRACT(
                EPOCH FROM (
                    order_delivered_customer_date -
                    order_purchase_timestamp
                )
            ) / 86400
        )::NUMERIC,
        2
    ) AS average_delivery_days
FROM orders
WHERE order_status = 'delivered'
  AND order_delivered_customer_date IS NOT NULL;



-- 11. Top 10 Sellers by Revenue
SELECT
    seller_id,
    ROUND(SUM(price), 2) AS total_revenue,
    COUNT(DISTINCT order_id) AS total_orders
FROM order_items
GROUP BY seller_id
ORDER BY total_revenue DESC
LIMIT 10;


-- 12. Top 10 Product Categories by Revenue
SELECT
    p.product_category_name,
    ROUND(SUM(oi.price), 2) AS total_revenue,
    COUNT(*) AS total_items_sold
FROM order_items oi
JOIN products p
    ON oi.product_id = p.product_id
GROUP BY p.product_category_name
ORDER BY total_revenue DESC
LIMIT 10;


-- 13. Average Customer Review Score
SELECT
    ROUND(AVG(review_score), 2) AS average_review_score,
    COUNT(*) AS total_reviews
FROM order_reviews;


-- 14. Review Score Distribution
SELECT
    review_score,
    COUNT(*) AS total_reviews
FROM order_reviews
GROUP BY review_score
ORDER BY review_score;
