DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS customers;



CREATE TABLE IF NOT EXISTS customers (
    customer_id INT PRIMARY KEY ,
    customer_name VARCHAR(40),
    email VARCHAR(40),
    country VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(40),
    category VARCHAR(40),
    price NUMERIC(10,2)
);

CREATE TABLE IF NOT EXISTS orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    order_date date,
    status VARCHAR(20),
    FOREIGN KEY (customer_id)
    REFERENCES customers(customer_id)
);

CREATE TABLE IF NOT EXISTS order_items (
    order_item_id INT PRIMARY KEY,
    product_id INT,
    order_id INT,
    quantity INT,
    unit_price NUMERIC(10,2),
    total_price NUMERIC(10,2),
    FOREIGN KEY (product_id)
    REFERENCES products(product_id),
    FOREIGN KEY (order_id)
    REFERENCES orders(order_id)
);




-- ALTER TABLE orders
--     ADD CONSTRAINT  fk_customer_id
--     FOREIGN KEY (customer_id) 
--     REFERENCES customers(customer_id);

-- ALTER TABLE order_items
--     ADD  CONSTRAINT  fk_product_id
    -- FOREIGN KEY (product_id)
    -- REFERENCES products(product_id),

    -- ADD CONSTRAINT  fk_order_id
    -- FOREIGN KEY (order_id)
    -- REFERENCES orders (order_id);

