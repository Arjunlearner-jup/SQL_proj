CREATE TABLE customer_orders (
    order_id         INT PRIMARY KEY,
    customer_id      INT NOT NULL,
    customer_name    VARCHAR(100),
    customer_email   VARCHAR(150),
    customer_city    VARCHAR(80),
    customer_country VARCHAR(80),
    signup_date      DATE,
    order_date       DATE NOT NULL,
    order_status     VARCHAR(30),
    payment_method   VARCHAR(30),
    shipping_type    VARCHAR(30),
    order_total      DECIMAL(10,2),
    discount_amount  DECIMAL(10,2),
    shipping_cost    DECIMAL(10,2)
);
CREATE TABLE order_line_items (
    order_item_id      INT PRIMARY KEY,
    order_id           INT NOT NULL,
    product_id         INT NOT NULL,
    product_name       VARCHAR(150),
    category           VARCHAR(80),
    brand              VARCHAR(80),
    unit_price         DECIMAL(10,2),
    quantity           INT,
    item_discount      DECIMAL(10,2),
    returned_flag      BOOLEAN,
    review_rating      DECIMAL(3,2)
);
