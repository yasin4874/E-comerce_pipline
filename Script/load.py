import psycopg2     
import pathlib
import pandas as pd
import os
    
path = pathlib.Path(__file__).parent.parent 
password = os.environ.get('POSTGRES_PASSWORD')  # Get password from environment variable or use default
conn = None
data_path = path / "data" / "processed"
cur = None

def insert_data(file_path,table_name, cols= tuple ):

    df = pd.read_csv(data_path / file_path).values.tolist()

    values = (len(cols) * ('%s',))

    sql = f"INSERT INTO {table_name} ({','.join(cols)}) VALUES ({','.join(values)})"
    cur.executemany(sql, df)

# connect to the local postgres database
try:
    conn = psycopg2.connect(
        user = "postgres",
        password = password,
        host = 'localhost',
        port = 5433,
        database = 'postgres'
    )

    print("Successfully connecting to the database.")
    cur = conn.cursor()
    with open(path / "sql" / "create_tables.sql", 'r') as f:
        sql = f.read()

    cur.execute(sql)
    conn.commit()

    # insert data into customers table
    insert_data("customers.csv", "customers", ('customer_id','customer_name','email','country'))

    # insert data into products table
    insert_data("products.csv", "products", ('product_id','product_name','category','price'))

    # insert data into orders table
    insert_data("orders.csv", "orders", ('order_id','customer_id','order_date','status'))

    # insert data into order_items table
    insert_data("order_items.csv", "order_items", ('order_item_id', 'order_id','product_id','quantity','unit_price','total_price'))

    conn.commit()
    print("Data inserted successfully into the tables.")

except Exception as e:
    # print("Error connecting to the database.")
    print(f'error: {e}')
    if conn:
        conn.rollback()
    
finally:
    if conn:
        conn.close()
    print('connection closed!')
