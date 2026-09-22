from tabnanny import check

import pandas as pd
from pathlib import Path

# set the path to the data directory
path = Path(__file__).parent.parent / "data"

path.mkdir(parents=True, exist_ok=True)
rejected_path = path / "rejected"

valid_path = path / "valid"

rejected_path.mkdir(parents=True, exist_ok=True)
valid_path.mkdir(parents=True, exist_ok=True)

# define a function to generate a reason string for each row based on the boolean values in the DataFrame
def get_reason(row,reasons):
        reason_per_row = []
        for col,info in reasons.items():
            if row[col]:
                reason_per_row.append(info)
        return ';'.join(reason_per_row)

#  ***  validate customers  ***
def validate_customers(path, rejected_path, valid_path):
    customer_df = pd.read_csv(path / "raw" /"customers.csv")

    # generate boolean series indicating missing values for each column
    missing_id = customer_df['cust_id'].isna() 
    missing_name = customer_df['name'].isna()
    missing_email = customer_df['email'].isna()
    missing_country = customer_df['country'].isna()


    # generate boolean series indicating duplicate values for cust_id, ignoring NaN values
    duplicate_id = (customer_df['cust_id'].duplicated(keep=False) & ~customer_df['cust_id'].isna())

    # generate a boolean series indicating invalid email addresses (not ending with '@gmail.com')
    inv_email = customer_df['email'].astype('str').str.endswith(('@gmail.com', '@yahoo.com', '@hotmail.com')) == False

    # combine the boolean series into a single DataFrame and set the column names
    df = pd.concat([missing_id,missing_name,missing_email,missing_country,duplicate_id,inv_email], ignore_index=True,axis=1)
    df.columns = ['missing_id','missing_name','missing_email','missing_country','duplicate_id','invalid_email']

    reasons = {
    'missing_id': 'missing id',
    'missing_name': 'missing name',
    'missing_email': 'missing email',
    'missing_country': 'missing country',
    'duplicate_id': 'duplicate id',
    'invalid_email': 'invalid email'
    }
    # apply the get_reason function to each row of the DataFrame 
    # and create a new column 'reason' in the customer_df DataFrame
    customer_df['reason'] = df.apply(get_reason, args=(reasons,), axis=1)

    # split the customer_df DataFrame into valid and invalid customers based on the 'reason' column
    valid_customer = customer_df[customer_df['reason'] == '']
    invalid_customer = customer_df[customer_df['reason'] != '']

    valid_customer = valid_customer.drop(columns=['reason'])
    valid_customer.to_csv(valid_path / "valid_customers.csv", index=False)
    invalid_customer.to_csv(rejected_path / "invalid_customers.csv", index=False)

    return valid_customer, invalid_customer

# ***  validate products  ***
def validate_products(path, rejected_path, valid_path):
    product_df = pd.read_csv(path / "raw" / "products.csv")

    # generate boolean series indicating missing values for each column
    missing_id = product_df['product_id'].isna()
    missing_name = product_df['product_name'].isna()
    missing_category = product_df['category'].isna()
    missing_price = product_df['price'].isna()

    # generate a boolean series indicating invalid prices (negative values)
    invalid_price = product_df['price'] <= 0 

    # generate a boolean series indicating duplicate product IDs, ignoring NaN values
    duplicate_id = product_df['product_id'].duplicated(keep=False) & ~product_df['product_id'].isna()

    # combine the boolean series into a single DataFrame and set the column names
    df = pd.concat([missing_id, missing_name, missing_category, missing_price, invalid_price, duplicate_id], ignore_index=True, axis=1)
    df.columns = ['missing_id', 'missing_name', 'missing_category', 'missing_price', 'invalid_price', 'duplicate_id']

    reasons = {
    'missing_id': 'missing id',
    'missing_name': 'missing name',
    'missing_category': 'missing category',
    'missing_price': 'missing price',
    'invalid_price': 'invalid price',
    'duplicate_id': 'duplicate id'
    }

    # apply the get_reason function to each row of the DataFrame
    product_df['reason'] = df.apply(get_reason, args=(reasons,), axis=1)

    # split the product_df DataFrame into valid and invalid products based on the 'reason' column
    valid_product = product_df[product_df['reason'] == '']
    invalid_product = product_df[product_df['reason'] != '']

    valid_product = valid_product.drop(columns=['reason'])
    valid_product.to_csv(valid_path / "valid_products.csv", index=False)
    invalid_product.to_csv(rejected_path / "invalid_products.csv", index=False)

    return valid_product, invalid_product


def validate_orders(path, rejected_path, valid_path, validate_customer):

    orders_df = pd.read_csv(path / "raw" / "orders.csv")

    missing_id = orders_df['order_id'].isna()

    missing_cust_id =  orders_df['cust_id'].isna() 

    orders_df['order_date'] = pd.to_datetime(orders_df['order_date'],errors='coerce')

    missing_date = orders_df['order_date'].isna()

    missing_status = orders_df['status'].isna()

    dupl_id = orders_df['order_id'].duplicated(keep=False) & ~orders_df['order_id'].isna()

    inv_cust_id = ~orders_df['cust_id'].isin(validate_customer['cust_id']) & orders_df['cust_id'].notna()

    ivl_status = ~orders_df['status'].str.strip().str.lower().isin(['pending','shipped','delivered','cancelled']) & ~orders_df['status'].isna()

    df = pd.concat([missing_id,missing_cust_id,missing_date,missing_status,dupl_id,inv_cust_id,ivl_status], ignore_index=True, axis=1)
    df.columns = ['missing_id','missing_cust_id','missing_date','missing_status','dupl_id','inv_cust_id','ivl_status']

    reasons = {
        'missing_id': 'missing id',
        'missing_cust_id': 'missing cust_id',
        'missing_date': 'missing date',
        'missing_status': 'missing status',
        'dupl_id': 'duplicate id',
        'inv_cust_id': 'invalid cust_id',
        'ivl_status': 'invalid status'
    }

    orders_df['reason'] = df.apply(get_reason, args=(reasons,), axis=1)

    valid_orders = orders_df[orders_df['reason'] == '']
    invalid_orders = orders_df[orders_df['reason'] != '']

    # delete the 'reason' column from the valid_orders DataFrame
    valid_orders = valid_orders.drop(columns=['reason'])
    valid_orders.to_csv(valid_path / "valid_orders.csv", index=False)
    invalid_orders.to_csv(rejected_path / "invalid_orders.csv", index=False)

    # print(orders_df['status'].unique())
    return valid_orders, invalid_orders

   
def validate_order_items(path, rejected_path, valid_path, vld_orders, vld_product):
    order_items_df = pd.read_csv(path / "raw" / "order_items.csv")

    missing_id = order_items_df['order_item_id'].isna()

    missing_order_id = order_items_df['order_id'].isna() 

    missing_product_id = order_items_df['product_id'].isna() 

    missing_quantity = order_items_df['quantity'].isna()

    missing_price = order_items_df['unit_price'].isna()

    # missing_tot_price = order_items_df['total_price'].isna()

    dupl_id = order_items_df['order_item_id'].duplicated(keep=False) & ~order_items_df['order_item_id'].isna()

    inv_order_id = ~order_items_df['order_id'].isin(vld_orders['order_id']) & ~order_items_df['order_id'].isna()

    inv_product_id = ~order_items_df['product_id'].isin(vld_product['product_id']) & ~order_items_df['product_id'].isna()

    inv_price = order_items_df['unit_price'] <= 0 

    inv_quantity = order_items_df['quantity'] <= 0

    # inv_tot_price = order_items_df['total_price'] <= 0

    # inconsistent_tot_price = order_items_df['unit_price'] * order_items_df['quantity'] != order_items_df['total_price']

    df = pd.concat([missing_id,missing_order_id,missing_product_id,missing_quantity,missing_price,dupl_id,inv_order_id,inv_product_id,inv_price,inv_quantity], ignore_index=True, axis=1)
    df.columns = ['missing_id','missing_order_id','missing_product_id','missing_quantity','missing_price','dupl_id','inv_order_id','inv_product_id','inv_price','inv_quantity']

    reasons = {
        'missing_id': 'missing id',
        'missing_order_id': 'missing order_id',
        'missing_product_id': 'missing product_id',
        'missing_quantity': 'missing quantity',
        'missing_price': 'missing price',
        'dupl_id': 'duplicate id',
        'inv_order_id': 'invalid order_id',
        'inv_product_id': 'invalid product_id',
        'inv_price': 'invalid price',
        'inv_quantity': 'invalid quantity'
    }

    order_items_df['reason'] = df.apply(get_reason,args=(reasons,), axis=1)

    valid_order_items = order_items_df[order_items_df['reason'] == '']
    invalid_order_items = order_items_df[order_items_df['reason'] != '']

    valid_order_items = valid_order_items.drop(columns=['reason'])
    valid_order_items.to_csv(valid_path / "valid_order_items.csv", index=False)
    invalid_order_items.to_csv(rejected_path / "invalid_order_items.csv", index=False)

    return valid_order_items, invalid_order_items


vld_customer,inv_customer =validate_customers(path, rejected_path, valid_path)

vld_product, inv_product = validate_products(path, rejected_path, valid_path)

vld_orders, inv_orders = validate_orders(path, rejected_path, valid_path, vld_customer)

validate_order_items(path, rejected_path, valid_path, vld_orders, vld_product)
 
print("valid orders:",vld_orders.info())

print(vld_orders.head())