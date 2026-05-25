CREATE TABLE ecommerce_customer_product_metrics AS
WITH base_orders AS (
    SELECT
        co.order_id,
        co.customer_id,
        co.customer_name,
        co.customer_email,
        co.customer_city,
        co.customer_country,
        co.signup_date,
        co.order_date,
        DATE_FORMAT(co.order_date, '%Y-%m-01') AS order_month,
        YEAR(co.order_date) AS order_year,
        MONTH(co.order_date) AS order_num,
        co.order_status,
        co.payment_method,
        co.shipping_type,
        co.order_total,
        co.discount_amount,
        co.shipping_cost,
        CASE WHEN co.order_status = 'Delivered' THEN 1 ELSE 0 END AS is_completed_order
    FROM customer_orders co
),
base_items AS (
    SELECT
        oli.order_id,
        oli.product_id,
        oli.product_name,
        oli.category,
        oli.brand,
        oli.unit_price,
        oli.quantity,
        oli.item_discount,
        oli.returned_flag,
        oli.review_rating,
        (oli.unit_price * oli.quantity) - COALESCE(oli.item_discount, 0) AS item_revenue
    FROM order_line_items oli
),
joined AS (
    SELECT
        o.order_id,
        o.customer_id,
        o.customer_name,
        o.customer_email,
        o.customer_city,
        o.customer_country,
        o.signup_date,
        o.order_date,
        o.order_month,
        o.order_year,
        o.order_num,
        o.order_status,
        o.payment_method,
        o.shipping_type,
        o.order_total,
        o.discount_amount,
        o.shipping_cost,
        o.is_completed_order,
        i.product_id,
        i.product_name,
        i.category,
        i.brand,
        i.unit_price,
        i.quantity,
        i.item_discount,
        i.returned_flag,
        i.review_rating,
        i.item_revenue
    FROM base_orders o
    JOIN base_items i
      ON o.order_id = i.order_id
    WHERE o.order_status <> 'Cancelled'
),
customer_first_order AS (
    SELECT
        customer_id,
        MIN(order_date) AS first_order_date
    FROM joined
    WHERE is_completed_order = 1
    GROUP BY customer_id
),
customer_monthly AS (
    SELECT
        j.customer_id,
        j.customer_name,
        j.customer_email,
        j.customer_city,
        j.customer_country,
        j.order_month,
        COUNT(DISTINCT j.order_id) AS orders_count,
        COUNT(*) AS line_items_count,
        SUM(j.quantity) AS units_sold,
        SUM(j.item_revenue) AS gross_item_revenue,
        SUM(j.item_discount) AS total_item_discount,
        SUM(CASE WHEN j.returned_flag = TRUE THEN 1 ELSE 0 END) AS returned_items,
        AVG(j.review_rating) AS avg_review_rating
    FROM joined j
    WHERE j.is_completed_order = 1
    GROUP BY
        j.customer_id, j.customer_name, j.customer_email,
        j.customer_city, j.customer_country, j.order_month
),
customer_lifetime AS (
    SELECT
        customer_id,
        CASE
            WHEN lifetime_revenue >= 500 THEN 'High Value'
            WHEN lifetime_revenue >= 200 THEN 'Mid Value'
            ELSE 'Low Value'
        END AS customer_segment,
        lifetime_orders,
        lifetime_units,
        lifetime_revenue
    FROM (
        SELECT
            customer_id,
            SUM(orders_count) AS lifetime_orders,
            SUM(units_sold) AS lifetime_units,
            SUM(gross_item_revenue) AS lifetime_revenue
        FROM customer_monthly
        GROUP BY customer_id
    ) x
),
product_monthly AS (
    SELECT
        j.order_month,
        j.category,
        j.brand,
        j.product_id,
        j.product_name,
        SUM(j.quantity) AS product_units_sold,
        SUM(j.item_revenue) AS product_revenue,
        SUM(CASE WHEN j.returned_flag = TRUE THEN 1 ELSE 0 END) AS product_returns,
        AVG(j.review_rating) AS product_avg_rating
    FROM joined j
    WHERE j.is_completed_order = 1
    GROUP BY
        j.order_month, j.category, j.brand, j.product_id, j.product_name
),
product_ranked AS (
    SELECT
        pm.*,
        ROW_NUMBER() OVER (
            PARTITION BY pm.order_month, pm.category
            ORDER BY pm.product_revenue DESC, pm.product_units_sold DESC
        ) AS product_rank_in_category
    FROM product_monthly pm
),
order_kpis AS (
    SELECT
        j.order_month,
        COUNT(DISTINCT j.order_id) AS total_orders,
        COUNT(DISTINCT j.customer_id) AS active_customers,
        SUM(j.quantity) AS total_units_sold,
        SUM(j.item_revenue) AS total_revenue,
        SUM(j.item_discount) AS total_discount,
        AVG(j.item_revenue) AS avg_item_revenue,
        SUM(CASE WHEN j.returned_flag = TRUE THEN 1 ELSE 0 END) AS total_returned_items,
        AVG(j.review_rating) AS avg_review_rating
    FROM joined j
    WHERE j.is_completed_order = 1
    GROUP BY j.order_month
),
final_table AS (
    SELECT
        cm.customer_id,
        cm.customer_name,
        cm.customer_email,
        cm.customer_city,
        cm.customer_country,
        cm.order_month,
        cfo.first_order_date,
        CASE
            WHEN DATE_FORMAT(cfo.first_order_date, '%Y-%m-01') = cm.order_month THEN 'New'
            ELSE 'Repeat'
        END AS customer_type,
        cl.customer_segment,
        cm.orders_count,
        cm.line_items_count,
        cm.units_sold,
        cm.gross_item_revenue,
        cm.total_item_discount,
        cm.returned_items,
        cm.avg_review_rating AS customer_avg_rating,
        ok.total_orders,
        ok.active_customers,
        ok.total_units_sold,
        ok.total_revenue,
        ok.total_discount,
        ok.avg_item_revenue,
        ok.total_returned_items,
        ok.avg_review_rating AS monthly_avg_rating,
        pr.category,
        pr.brand,
        pr.product_id,
        pr.product_name,
        pr.product_units_sold,
        pr.product_revenue,
        pr.product_returns,
        pr.product_avg_rating,
        pr.product_rank_in_category,
        cl.lifetime_orders,
        cl.lifetime_units,
        cl.lifetime_revenue,
        ROUND(cm.gross_item_revenue / NULLIF(ok.total_revenue, 0) * 100, 2) AS customer_revenue_share_pct,
        ROUND(cm.orders_count / NULLIF(ok.total_orders, 0), 4) AS customer_order_share
    FROM customer_monthly cm
    LEFT JOIN customer_first_order cfo
      ON cm.customer_id = cfo.customer_id
    LEFT JOIN customer_lifetime cl
      ON cm.customer_id = cl.customer_id
    LEFT JOIN order_kpis ok
      ON cm.order_month = ok.order_month
    LEFT JOIN product_ranked pr
      ON cm.order_month = pr.order_month
)
SELECT *
FROM final_table
ORDER BY order_month, customer_id, product_rank_in_category;
