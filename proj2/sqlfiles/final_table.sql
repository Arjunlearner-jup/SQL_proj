CREATE TABLE saas_subscription_metrics AS
WITH RECURSIVE month_series AS (
    SELECT DATE('2025-01-01') AS metric_month
    UNION ALL
    SELECT DATE_ADD(metric_month, INTERVAL 1 MONTH)
    FROM month_series
    WHERE metric_month < DATE('2025-08-01')
),

customer_months AS (
    SELECT
        c.customer_id,
        c.customer_name,
        c.customer_email,
        c.signup_date,
        DATE_FORMAT(c.signup_date, '%Y-%m-01') AS cohort_month,
        c.country,
        c.industry,
        c.company_size,
        c.acquisition_channel,
        ms.metric_month
    FROM customers c
    CROSS JOIN month_series ms
    WHERE ms.metric_month >= DATE_FORMAT(c.signup_date, '%Y-%m-01')
),

active_subscription_mrr AS (
    SELECT
        cm.metric_month,
        cm.customer_id,
        s.subscription_id,
        s.plan_name,
        s.billing_cycle,
        s.change_type,
        s.mrr_amount
    FROM customer_months cm
    LEFT JOIN subscriptions s
        ON cm.customer_id = s.customer_id
       AND s.subscription_start_date <= LAST_DAY(cm.metric_month)
       AND (s.subscription_end_date IS NULL OR s.subscription_end_date >= cm.metric_month)
),

customer_monthly_mrr AS (
    SELECT
        cm.metric_month,
        cm.customer_id,
        cm.customer_name,
        cm.customer_email,
        cm.signup_date,
        cm.cohort_month,
        cm.country,
        cm.industry,
        cm.company_size,
        cm.acquisition_channel,
        COALESCE(SUM(asm.mrr_amount), 0) AS current_mrr,
        COUNT(DISTINCT CASE WHEN asm.subscription_id IS NOT NULL THEN asm.subscription_id END) AS active_subscriptions,
        MAX(CASE WHEN asm.subscription_id IS NOT NULL THEN 1 ELSE 0 END) AS is_active_customer
    FROM customer_months cm
    LEFT JOIN active_subscription_mrr asm
        ON cm.customer_id = asm.customer_id
       AND cm.metric_month = asm.metric_month
    GROUP BY
        cm.metric_month,
        cm.customer_id,
        cm.customer_name,
        cm.customer_email,
        cm.signup_date,
        cm.cohort_month,
        cm.country,
        cm.industry,
        cm.company_size,
        cm.acquisition_channel
),

mrr_with_lag AS (
    SELECT
        cmm.*,
        LAG(cmm.current_mrr) OVER (
            PARTITION BY cmm.customer_id
            ORDER BY cmm.metric_month
        ) AS prev_mrr
    FROM customer_monthly_mrr cmm
),

classified_mrr AS (
    SELECT
        metric_month,
        customer_id,
        customer_name,
        customer_email,
        signup_date,
        cohort_month,
        country,
        industry,
        company_size,
        acquisition_channel,
        active_subscriptions,
        is_active_customer,
        current_mrr,
        COALESCE(prev_mrr, 0) AS prev_mrr,

        CASE
            WHEN COALESCE(prev_mrr, 0) = 0 AND current_mrr > 0 THEN current_mrr
            ELSE 0
        END AS new_mrr,

        CASE
            WHEN COALESCE(prev_mrr, 0) > 0 AND current_mrr > prev_mrr THEN current_mrr - prev_mrr
            ELSE 0
        END AS expansion_mrr,

        CASE
            WHEN COALESCE(prev_mrr, 0) > 0 AND current_mrr < prev_mrr AND current_mrr > 0 THEN prev_mrr - current_mrr
            ELSE 0
        END AS contraction_mrr,

        CASE
            WHEN COALESCE(prev_mrr, 0) > 0 AND current_mrr = 0 THEN prev_mrr
            ELSE 0
        END AS churned_mrr,

        CASE
            WHEN COALESCE(prev_mrr, 0) = 0 AND current_mrr > 0 THEN 'new'
            WHEN COALESCE(prev_mrr, 0) > 0 AND current_mrr > prev_mrr THEN 'expansion'
            WHEN COALESCE(prev_mrr, 0) > 0 AND current_mrr < prev_mrr AND current_mrr > 0 THEN 'contraction'
            WHEN COALESCE(prev_mrr, 0) > 0 AND current_mrr = 0 THEN 'churn'
            WHEN COALESCE(prev_mrr, 0) > 0 AND current_mrr = prev_mrr THEN 'retained'
            ELSE 'inactive'
        END AS revenue_change_type
    FROM mrr_with_lag
),

monthly_rollup AS (
    SELECT
        metric_month,
        SUM(current_mrr) AS total_mrr,
        SUM(new_mrr) AS total_new_mrr,
        SUM(expansion_mrr) AS total_expansion_mrr,
        SUM(contraction_mrr) AS total_contraction_mrr,
        SUM(churned_mrr) AS total_churned_mrr,
        SUM(is_active_customer) AS total_active_customers
    FROM classified_mrr
    GROUP BY metric_month
)

SELECT
    cm.metric_month,
    cm.customer_id,
    cm.customer_name,
    cm.customer_email,
    cm.signup_date,
    cm.cohort_month,
    cm.country,
    cm.industry,
    cm.company_size,
    cm.acquisition_channel,
    cm.active_subscriptions,
    cm.is_active_customer,
    cm.current_mrr,
    cm.prev_mrr,
    cm.new_mrr,
    cm.expansion_mrr,
    cm.contraction_mrr,
    cm.churned_mrr,
    cm.revenue_change_type,
    mr.total_mrr,
    mr.total_new_mrr,
    mr.total_expansion_mrr,
    mr.total_contraction_mrr,
    mr.total_churned_mrr,
    mr.total_active_customers
FROM classified_mrr cm
LEFT JOIN monthly_rollup mr
    ON cm.metric_month = mr.metric_month
ORDER BY cm.metric_month, cm.customer_id;