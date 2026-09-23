```*************      Anlytical questions      *************```
-- 4. What is the average number of orders per day??
-- 5. What are the 10 products with the highest quantity sold, and which customers purchased them?
-- 6. What is the total revenue for each month?
-- 7. What is the total revenue for each product category?
-- 8. Which products costing more than $500 have been ordered, and which customers ordered them?
-- 9. What is the average number of orders per customer in each country?
--10. Show the customer name, order ID, product name, quantity, and total price for each order item.

-- 1. How many customers have placed at least one order?
SELECT 
    COUNT(DISTINCT(c.customer_id)) AS "total customer"
FROM 
    customers as c
INNER JOIN
    orders as o
ON c.customer_id = o.customer_id;

-- 2. What are the 10 most-ordered products?
SELECT 
	oi.product_id,
	p.product_name,
    COUNT(oi.product_id) AS total_order
FROM 
    products AS p
INNER JOIN 
    order_items as oi
ON 
    p.product_id = oi.product_id
GROUP BY
    oi.product_id,p.product_name
ORDER BY t_order DESC
LIMIT 10;

-- 3. Which country has the most customers?
SELECT
	country,
	COUNT(country) AS "total customer"
FROM 
	customers
GROUP BY
	country
ORDER BY "total customer" DESC
LIMIT 1;