import pandas as pd
from pathlib import Path

path = Path(__file__).parent.parent / "data"
path.mkdir(parents=True, exist_ok=True)

process_path = path / "processed"
process_path.mkdir(parents=True,exist_ok=True)
def transform_customers(path):
    customer_df = pd.read_csv(path / "valid" /"valid_customers.csv")
    
    customer_df['cust_id'] = customer_df['cust_id'].astype(int)  # convert 'cust_id' to integer type

    # convert the 'name' column to str, transformed to tiltle case (capitlize first word), remove whitespace
    customer_df['name'] = customer_df['name'].str.title().str.strip() 

    # transform the 'email' column to lowercase
    customer_df['email'] = customer_df['email'].str.lower().str.strip()

    # transform the 'country' column to title case and remove  whitespace
    customer_df['country'] = customer_df['country'].str.title().str.strip()

    # save the tansformed data
    customer_df.to_csv(process_path / "customers.csv", index=False)

def transform_products(path):
    product_df = pd.read_csv(path / "valid" /"valid_products.csv")

    product_df['product_id'] = product_df['product_id'].astype(int)  # convert 'product_id' to integer type

    # convert the 'name' column to str, transformed to tiltle case (capitlize first word), remove whitespace
    product_df['product_name'] = product_df['product_name'].str.title().str.strip() 

    # transform the 'category' column to title case and remove  whitespace
    product_df['category'] = product_df['category'].str.title().str.strip()

    # transform the 'price' column to float
    product_df['price'] = product_df['price'].astype(float)

    # save the tansformed data
    product_df.to_csv(process_path / "products.csv", index=False)

def transform_orders(path):
    order_df = pd.read_csv(path / "valid" /"valid_orders.csv")

    order_df['order_id'] = order_df['order_id'].astype(int)  # convert 'order_id' to integer type
    order_df['cust_id'] = order_df['cust_id'].astype(int)  # convert 'cust_id' to integer type

    # transform the 'order_date' column to datetime format
    order_df['order_date'] = pd.to_datetime(order_df['order_date'], errors='coerce')

    #  transform the 'status' column to lowercase and remove whitespace
    order_df['status'] = order_df['status'].str.lower().str.strip()

    # save the tansformed data
    order_df.to_csv(process_path / "orders.csv", index=False)

def transform_order_items(path):
    order_items_df = pd.read_csv(path / "valid" /"valid_order_items.csv")

    # convert 'id's and quantities to integer type
    order_items_df['order_item_id'] = order_items_df['order_item_id'].astype(int)  
    order_items_df['order_id'] = order_items_df['order_id'].astype(int) 
    order_items_df['product_id'] = order_items_df['product_id'].astype(int)
    order_items_df['quantity'] = order_items_df['quantity'].astype(int)  

    # convert 'unit_price' to float type
    order_items_df['unit_price'] = order_items_df['unit_price'].astype(float)  
    order_items_df['total_price'] = round((order_items_df['unit_price'] * order_items_df['quantity']).astype(float), 2)  # calculate total price and round to 2 decimal places

    # save the tansformed data
    order_items_df.to_csv(process_path / "order_items.csv", index=False)

# call the transform functions
transform_customers(path)
transform_products(path)
transform_orders(path)
transform_order_items(path)