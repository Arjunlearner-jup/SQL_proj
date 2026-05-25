INSERT INTO customers (
    customer_id,
    customer_name,
    customer_email,
    signup_date,
    country,
    industry,
    company_size,
    acquisition_channel
) VALUES
(1, 'Nimbus Labs', 'ops@nimbuslabs.com', '2025-01-10', 'USA', 'SaaS', 'SMB', 'Organic Search'),
(2, 'BluePeak Analytics', 'finance@bluepeak.io', '2025-01-18', 'UK', 'Analytics', 'Mid-Market', 'LinkedIn Ads'),
(3, 'Northstar Health', 'admin@northstarhealth.com', '2025-02-05', 'Canada', 'HealthTech', 'Enterprise', 'Referral'),
(4, 'Orbit Commerce', 'hello@orbitcommerce.com', '2025-02-14', 'USA', 'E-commerce', 'SMB', 'Paid Search'),
(5, 'Vertex AI Studio', 'team@vertexai.studio', '2025-03-01', 'India', 'AI', 'Startup', 'Product Hunt'),
(6, 'Cedar Ops', 'support@cedarops.com', '2025-03-12', 'Germany', 'IT Services', 'SMB', 'Organic Search'),
(7, 'Atlas Freight', 'data@atlasfreight.com', '2025-04-03', 'UAE', 'Logistics', 'Mid-Market', 'Referral'),
(8, 'Luma Creative', 'contact@lumacreative.co', '2025-04-18', 'Australia', 'Marketing', 'Startup', 'Instagram'),
(9, 'Pulse Retail', 'analytics@pulseretail.com', '2025-05-02', 'USA', 'Retail', 'SMB', 'Paid Search'),
(10, 'Quantum Docs', 'info@quantumdocs.ai', '2025-05-11', 'Singapore', 'Productivity', 'Startup', 'Organic Search');

INSERT INTO subscriptions (
    subscription_id,
    customer_id,
    plan_name,
    billing_cycle,
    mrr_amount,
    subscription_start_date,
    subscription_end_date,
    subscription_status,
    change_type
) VALUES
(101, 1, 'Starter', 'Monthly', 100.00, '2025-01-10', '2025-03-31', 'Ended', 'new'),
(102, 1, 'Growth',  'Monthly', 180.00, '2025-04-01', NULL, 'Active', 'upgrade'),

(103, 2, 'Growth',  'Monthly', 220.00, '2025-01-18', '2025-04-30', 'Ended', 'new'),
(104, 2, 'Starter', 'Monthly', 140.00, '2025-05-01', NULL, 'Active', 'downgrade'),
(105, 3, 'Pro',     'Monthly', 300.00, '2025-02-05', '2025-04-30', 'Ended', 'new'),
(106, 3, 'Pro',     'Monthly', 300.00, '2025-06-01', NULL, 'Active', 'reactivation'),
(107, 4, 'Starter', 'Monthly', 120.00, '2025-02-14', NULL, 'Active', 'new'),
(108, 5, 'Starter', 'Monthly', 90.00,  '2025-03-01', '2025-05-31', 'Ended', 'new'),
(109, 5, 'Growth',  'Monthly', 160.00, '2025-06-01', NULL, 'Active', 'upgrade'),
(110, 6, 'Starter', 'Monthly', 110.00, '2025-03-12', '2025-05-31', 'Churned', 'churn'),
(111, 7, 'Growth',  'Monthly', 210.00, '2025-04-03', NULL, 'Active', 'new'),
(112, 8, 'Starter', 'Monthly', 95.00,  '2025-04-18', '2025-05-31', 'Ended', 'new'),
(113, 8, 'Growth',  'Monthly', 150.00, '2025-06-01', NULL, 'Active', 'upgrade'),
(114, 9, 'Starter', 'Monthly', 130.00, '2025-05-02', NULL, 'Active', 'new'),
(115, 10, 'Pro',    'Monthly', 260.00, '2025-05-11', NULL, 'Active', 'new');