#CREATE DATABASE ecommerce_project;
-- 2. Activate the database to start working in it
USE ecommerce_project;

CREATE TABLE orders (
    order_id VARCHAR(50) PRIMARY KEY,
    order_date VARCHAR(50),              -- We use text temporarily to 'catch' the data
    customer_name VARCHAR(100),
    state VARCHAR(50),
    city VARCHAR(50)
);

CREATE TABLE details (
    order_id VARCHAR(50),
    amount DECIMAL(10, 2),
    profit DECIMAL(10, 2),
    quantity INT,
    category VARCHAR(50),
    sub_category VARCHAR(50),
    payment_mode VARCHAR(50)
);

-- Check if all 1500 rows are present
SELECT COUNT(*) AS total_rows_orders FROM orders;
SELECT COUNT(*) AS total_rows_details FROM details;


SET SQL_SAFE_UPDATES = 1;

-- 1. Update the text to the correct SQL format
UPDATE orders 
SET order_date = STR_TO_DATE(order_date, '%d-%m-%Y');

-- 2. Change the column type from Text to Date permanently
ALTER TABLE orders 
MODIFY COLUMN order_date DATE;

SELECT * FROM orders LIMIT 10;

SELECT COUNT(*) FROM orders;

-- View a combined snapshot of your business
SELECT 
    o.order_id, 
    o.customer_name, 
    o.state, 
    d.amount, 
    d.profit, 
    d.category
FROM orders o
JOIN details d ON o.order_id = d.order_id
LIMIT 5; 

-- Page 1: Executive Overview KPIs
SELECT 
    ROUND(SUM(amount), 0) AS total_revenue,
    ROUND(SUM(profit), 0) AS total_profit,
    COUNT(DISTINCT order_id) AS total_orders,
    SUM(quantity) AS total_units_sold,
    ROUND(SUM(amount) / COUNT(DISTINCT order_id), 0) AS aov,
    ROUND((SUM(profit) / SUM(amount)) * 100, 2) AS profit_margin_pct
FROM details; 

-- Time Intelligence (The "Growth MoM %")
-- The Logic: LAG looks at the "Previous Month" value so you can compare it to the "Current Month."
WITH Monthly_Sales AS (
    SELECT 
        MONTH(o.order_date) AS month_num,
        MONTHNAME(o.order_date) AS month_name,
        SUM(d.amount) AS current_month_revenue
    FROM orders o
    JOIN details d ON o.order_id = d.order_id
    GROUP BY month_num, month_name
    ORDER BY month_num
)
SELECT 
    month_name,
    current_month_revenue,
    LAG(current_month_revenue) OVER (ORDER BY month_num) AS prev_month_revenue,
    ROUND(((current_month_revenue - LAG(current_month_revenue) OVER (ORDER BY month_num)) / 
    LAG(current_month_revenue) OVER (ORDER BY month_num)) * 100, 2) AS mom_growth_pct
FROM Monthly_Sales;

-- Page 2: Sales and Customers KPIs
SELECT 
    SUM(d.amount) AS total_revenue,
    COUNT(DISTINCT d.order_id) AS total_orders,
    ROUND(SUM(d.amount) / COUNT(DISTINCT d.order_id), 2) AS aov,
    COUNT(DISTINCT o.customer_name) AS total_customers
FROM details d
JOIN orders o ON d.order_id = o.order_id;

-- Repeat Rate%
WITH Customer_Orders AS (
    SELECT 
        customer_name, 
        COUNT(order_id) AS order_count
    FROM orders
    GROUP BY customer_name
)
SELECT 
    COUNT(*) AS total_customers,
    SUM(CASE WHEN order_count > 1 THEN 1 ELSE 0 END) AS repeat_customers,
    ROUND((SUM(CASE WHEN order_count > 1 THEN 1 ELSE 0 END) / COUNT(*)) * 100, 2) AS repeat_rate_pct
FROM Customer_Orders;


-- Page 3: Profitability KPIs
 WITH Order_Summaries AS (
    -- Step 1: Calculate total profit for every unique Order ID
    SELECT 
        order_id, 
        SUM(profit) AS total_order_profit 
    FROM details 
    GROUP BY order_id
)
SELECT 
    SUM(d.profit) AS total_profit,
    ROUND((SUM(d.profit) / SUM(d.amount)) * 100, 2) AS profit_margin_pct,
    
    -- Average Profit per Order
    ROUND(SUM(d.profit) / COUNT(DISTINCT d.order_id), 2) AS avg_profit_per_order,
    
    -- Total Loss (The sum of every individual item that lost money)
    ROUND(SUM(CASE WHEN d.profit < 0 THEN d.profit ELSE 0 END), 2) AS total_loss,
    
   -- Loss Orders % (How many orders lost money vs total orders)
    ROUND(
        (COUNT(CASE WHEN total_order_profit < 0 THEN 1 END) / COUNT(*)) * 100, 
        1
    ) AS loss_orders_pct
    
FROM details d
JOIN Order_Summaries os ON d.order_id = os.order_id;

-- Profit Changes %
WITH Monthly_Profit AS (
    SELECT 
        MONTH(o.order_date) AS month_num,
        MONTHNAME(o.order_date) AS month_name,
        SUM(d.profit) AS current_month_profit
    FROM orders o
    JOIN details d ON o.order_id = d.order_id
    GROUP BY month_num, month_name
    ORDER BY month_num
)
SELECT 
    month_name,
    current_month_profit,
    LAG(current_month_profit) OVER (ORDER BY month_num) AS prev_month_profit,
    ROUND(((current_month_profit - LAG(current_month_profit) OVER (ORDER BY month_num)) / 
    ABS(LAG(current_month_profit) OVER (ORDER BY month_num))) * 100, 2) AS profit_change_pct
FROM Monthly_Profit;
 

CREATE VIEW master_sales_report AS
SELECT 
    o.order_id,
    o.order_date,
    o.customer_name,
    o.state,
    o.city,
    d.amount,
    d.profit,
    d.quantity,
    d.category,
    d.sub_category,
    d.payment_mode
FROM orders o
JOIN details d ON o.order_id = d.order_id;

SELECT * FROM master_sales_report;