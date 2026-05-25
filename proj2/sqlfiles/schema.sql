CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    customer_email VARCHAR(150) NOT NULL UNIQUE,
    signup_date DATE NOT NULL,
    country VARCHAR(50),
    industry VARCHAR(50),
    company_size VARCHAR(30),
    acquisition_channel VARCHAR(50)
);

CREATE TABLE subscriptions (
    subscription_id INT PRIMARY KEY,
    customer_id INT NOT NULL,
    plan_name VARCHAR(50) NOT NULL,
    billing_cycle VARCHAR(20) NOT NULL,
    mrr_amount DECIMAL(10,2) NOT NULL,
    subscription_start_date DATE NOT NULL,
    subscription_end_date DATE NULL,
    subscription_status VARCHAR(30) NOT NULL,
    change_type VARCHAR(30) NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);
