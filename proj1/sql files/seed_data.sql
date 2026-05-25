INSERT INTO customer_orders (
    order_id, customer_id, customer_name, customer_email, customer_city, customer_country,
    signup_date, order_date, order_status, payment_method, shipping_type,
    order_total, discount_amount, shipping_cost
) VALUES
(1001, 1, 'Arjun Mohan', 'arjun.mohan@email.com', 'Dublin', 'Ireland', '2025-01-10', '2025-02-14', 'Delivered', 'Card', 'Standard', 189.97, 10.00, 5.99),
(1002, 2, 'Neha Sharma', 'neha.sharma@email.com', 'Cork', 'Ireland', '2025-01-15', '2025-02-16', 'Delivered', 'UPI', 'Express', 79.99, 0.00, 8.99),
(1003, 3, 'Rahul Verma', 'rahul.verma@email.com', 'Galway', 'Ireland', '2025-02-01', '2025-02-20', 'Returned', 'Card', 'Standard', 129.50, 5.00, 5.99),
(1004, 1, 'Arjun Mohan', 'arjun.mohan@email.com', 'Dublin', 'Ireland', '2025-01-10', '2025-03-02', 'Delivered', 'Card', 'Express', 249.98, 15.00, 8.99),
(1005, 4, 'Sara Khan', 'sara.khan@email.com', 'Limerick', 'Ireland', '2025-02-18', '2025-03-05', 'Delivered', 'Cash on Delivery', 'Standard', 59.99, 0.00, 4.99),
(1006, 5, 'David Lee', 'david.lee@email.com', 'Belfast', 'UK', '2025-02-20', '2025-03-08', 'Cancelled', 'Card', 'Standard', 0.00, 0.00, 0.00),
(1007, 2, 'Neha Sharma', 'neha.sharma@email.com', 'Cork', 'Ireland', '2025-01-15', '2025-03-12', 'Delivered', 'UPI', 'Standard', 154.48, 10.00, 5.99),
(1008, 6, 'Priya Nair', 'priya.nair@email.com', 'Waterford', 'Ireland', '2025-03-01', '2025-03-15', 'Delivered', 'Card', 'Express', 319.97, 20.00, 8.99),
(1009, 7, 'John Murphy', 'john.murphy@email.com', 'Dublin', 'Ireland', '2025-03-03', '2025-03-20', 'Delivered', 'PayPal', 'Standard', 89.99, 0.00, 5.99),
(1010, 3, 'Rahul Verma', 'rahul.verma@email.com', 'Galway', 'Ireland', '2025-02-01', '2025-04-01', 'Delivered', 'Card', 'Standard', 210.00, 12.00, 5.99),
(1011, 8, 'Emma Walsh', 'emma.walsh@email.com', 'Kilkenny', 'Ireland', '2025-03-10', '2025-04-04', 'Delivered', 'Card', 'Express', 134.99, 0.00, 8.99),
(1012, 1, 'Arjun Mohan', 'arjun.mohan@email.com', 'Dublin', 'Ireland', '2025-01-10', '2025-04-10', 'Delivered', 'Card', 'Standard', 279.49, 25.00, 5.99);

-- order_line_items
INSERT INTO order_line_items (
    order_item_id, order_id, product_id, product_name, category, brand,
    unit_price, quantity, item_discount, returned_flag, review_rating
) VALUES
(1, 1001, 501, 'Wireless Mouse', 'Accessories', 'LogiTech', 24.99, 2, 0.00, FALSE, 4.4),
(2, 1001, 601, 'Mechanical Keyboard', 'Accessories', 'KeyPro', 129.99, 1, 10.00, FALSE, 4.7),

(3, 1002, 701, 'Bluetooth Speaker', 'Audio', 'SoundMax', 79.99, 1, 0.00, FALSE, 4.3),

(4, 1003, 801, 'Fitness Smartwatch', 'Wearables', 'FitPulse', 129.50, 1, 5.00, TRUE, 3.8),

(5, 1004, 901, 'Office Chair', 'Furniture', 'ErgoLife', 199.99, 1, 15.00, FALSE, 4.6),
(6, 1004, 501, 'Wireless Mouse', 'Accessories', 'LogiTech', 24.99, 2, 0.00, FALSE, 4.4),

(7, 1005, 1001, 'USB-C Hub', 'Accessories', 'HubWorks', 59.99, 1, 0.00, FALSE, 4.1),

(8, 1006, 1101, '27-inch Monitor', 'Monitors', 'ViewBest', 199.99, 1, 0.00, FALSE, NULL),

(9, 1007, 1201, 'Noise Cancelling Headphones', 'Audio', 'SoundMax', 99.49, 1, 10.00, FALSE, 4.8),
(10, 1007, 501, 'Wireless Mouse', 'Accessories', 'LogiTech', 24.99, 2, 0.00, FALSE, 4.4),

(11, 1008, 1301, 'Laptop Stand', 'Accessories', 'DeskFlow', 39.99, 1, 0.00, FALSE, 4.2),
(12, 1008, 1401, 'Tablet 11 inch', 'Tablets', 'TechTab', 279.98, 1, 20.00, FALSE, 4.5),

(13, 1009, 1501, 'Webcam HD', 'Accessories', 'CamVision', 89.99, 1, 0.00, FALSE, 4.0),

(14, 1010, 1601, 'Portable SSD 1TB', 'Storage', 'DataFast', 105.00, 2, 12.00, FALSE, 4.9),

(15, 1011, 1701, 'Desk Lamp', 'Home Office', 'BrightLite', 45.00, 1, 0.00, FALSE, 4.1),
(16, 1011, 1001, 'USB-C Hub', 'Accessories', 'HubWorks', 59.99, 1, 0.00, FALSE, 4.1),

(17, 1012, 1801, 'Ergonomic Desk', 'Furniture', 'ErgoLife', 249.50, 1, 25.00, FALSE, 4.7),
(18, 1012, 1301, 'Laptop Stand', 'Accessories', 'DeskFlow', 39.99, 1, 0.00, FALSE, 4.2);