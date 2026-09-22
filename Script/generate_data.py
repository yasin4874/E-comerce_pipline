import random
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
from pathlib import Path

path = Path(__file__).parent.parent /"data/raw"

path.mkdir(parents=True, exist_ok=True)


customer_data = {'cust_id': [], 'name': [], 'email': [], 'country': []}
product_data = {'product_id': [],
                'product_name': [], 'category': [], 'price': []}
order_data = {'order_id': [], 'cust_id': [], 'order_date': [], 'status': []}
order_items_data = {'order_item_id': [], 'order_id': [], 'product_id': [
], 'quantity': [], 'unit_price': [], 'total_price': []}


class Generate_issue:
    def __init__(self):
        pass

    def corrupt_id(self, t_ids):
        random_cor = random.randint(1, 2)

        if random_cor == 1:
            return np.nan  # return the id empty
        else:
            # return id equal a random id (to get duplicate id)
            return random.randint(1, t_ids)

    def corrupt_name(self, name):
        random_cor = random.randint(1, 2)

        if random_cor == 1:
            return np.nan  # make the name empty
        else:
            return name + "           "  # add extra spaces

    def corrupt_numbers(self, number, amount):
        random_cor = random.randint(1, 3)

        if random_cor == 1:
            number = ""
        elif random_cor == 2:
            number = random.randint(0, amount) * -1
        else:
            number = str(number)

        return number

    def customer(self, id, full_name, email, country):

        self.id = id
        self.name = full_name
        data = ['id', 'name', 'email', 'country']

        column_to_corrupt = random.choice(data)
        if (column_to_corrupt == 'id'):
            self.id = self.corrupt_id(500)

        elif (column_to_corrupt == 'name'):
            self.name = self.corrupt_name(full_name)

        elif (column_to_corrupt == 'email'):
            random_cor = random.randint(1, 3)

            if random_cor == 1:
                email = np.nan  # Make the email empty
            elif random_cor == 2:
                # Remove the "@" symbol from the email
                email = email.replace("@", "")
            else:
                # Remove the ".com" from the email
                email = email.replace("gmail", "")
        elif (column_to_corrupt == 'country'):
            random_cor = random.randint(1, 2)

            if random_cor == 1:
                country = np.nan  # Make the country empty

            else:
                country = country + "           "  # add extra spaces

        customer_data['cust_id'].append((self.id))
        customer_data['name'].append(self.name)
        customer_data['email'].append(email)
        customer_data['country'].append(country)

    def product(self, id, name, category, price):
        self.id = id
        self.name = name
        self.category = category
        self.price = price

        # randomly select a column to corrupt
        data = ['id', 'name', 'category', 'price']
        column_to_corrupt = random.choice(data)

        if (column_to_corrupt == 'id'):  # corrupt the id
            id = self.corrupt_id(50)

        elif (column_to_corrupt == 'name'):  # corrupt the name
            name = self.corrupt_name(self.name)

        elif (column_to_corrupt == 'category'):  # corrupt the category
            category = self.corrupt_name(self.category)

        elif (column_to_corrupt == 'price'):  # corrupt the price
            price = self.corrupt_numbers(self.price, 9999)

        product_data['product_id'].append(id)
        product_data['product_name'].append(name)
        product_data['category'].append(category)
        product_data['price'].append(price)

    def order(self, id, custom_id, order_date, status):
        self.id = id
        self.custom_id = custom_id
        self.order_date = order_date
        self.status = status

        data = ['id', 'custom_id', 'order_date', 'status']
        column_to_corrupt = random.choice(data)

        if column_to_corrupt == 'id':
            self.id = self.corrupt_id(2000)

        elif column_to_corrupt == 'custom_id':
            self.custom_id = self.corrupt_id(500)

        elif column_to_corrupt == 'order_date':
            random_choice = random.randint(1, 3)

            if random_choice == 1:
                self.order_date = np.nan  # make order date null
            elif random_choice == 2:
                # make order date string data type
                self.order_date = random.choice(['hello', 'welcome', 'error'])
            else:
                # make order date string data type
                self.order_date = str(self.order_date)

        else:
            self.status = self.corrupt_name(self.status)

        order_data['order_id'].append(self.id)
        order_data['cust_id'].append(self.custom_id)
        order_data['order_date'].append(self.order_date)
        order_data['status'].append(self.status)

    def order_items(self, id, order_id, product_id, quantity, unit_price, total_price):
        self.id = id
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity
        self.unit_price = unit_price
        self.total_price = total_price

        data = ['id', 'order_id', 'product_id',
                'quantity', 'unit_price', 'total_price']
        column_to_corrupt = random.choice(data)

        if column_to_corrupt == 'id':
            self.id = self.corrupt_id(2000)

        elif column_to_corrupt == 'order_id':
            self.order_id = self.corrupt_id(2000)

        elif column_to_corrupt == 'product_id':
            self.product_id = self.corrupt_id(50)

        elif column_to_corrupt == 'quantity':
            self.quantity = self.corrupt_numbers(self.quantity, 200)

        elif column_to_corrupt == 'unit_price':
            self.unit_price = self.corrupt_numbers(self.unit_price, 9999)

        else:
            self.total_price = self.corrupt_numbers(self.total_price, 9999)

        order_items_data['order_item_id'].append(self.id)
        order_items_data['order_id'].append(self.order_id)
        order_items_data['product_id'].append(self.product_id)
        order_items_data['quantity'].append(self.quantity)
        order_items_data['unit_price'].append(self.unit_price)
        order_items_data['total_price'].append(self.total_price)


gen_issue = Generate_issue()
# ****************  customer data  ************************


def customers():
    fname = ['yasin', 'abdi', 'ali', 'cumar', 'siyaad', 'xasan', 'faarah', 'maryam', 'danial', 'jorch', 'anna', 'miski', 'xafso', 'faadumo', "James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda",
             "William", "Elizabeth", "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica", "Thomas", "Sarah", "Charles", "Karen", "Christopher", "Lisa", "Daniel", "Nancy", "Matthew", "Betty", "Anthony", "Sandra", "Mark", "Ashley"]
    lname = ['cumar', 'cabbaas', 'maxamed', 'zakariye', 'liibaan',
             'xersi', 'anas', 'farxaan', 'cabdullaahi', 'mucaad', 'mucaawiye']

    countries = ['somalia', 'US', 'UK', 'Canada', 'China', 'Kenya', 'Egypt',
                 'Libya', 'Yamen', 'Sweden', 'Algeria', 'Maroco', 'Jappan', 'Korea']

    for id in range(1, 501):
        firstN = random.choice(fname)
        lastN = random.choice(lname)
        fullname = firstN + " " + lastN
        email = firstN + str(random.randint(1, 99999999)) + "@gmail.com"
        country = random.choice(countries)

        # 10% chance to introduce data issues
        random_corruption = random.randint(1, 10)
        if random_corruption == 1:

            gen_issue.customer(id, fullname, email, country)
        else:
            customer_data['cust_id'].append(id)
            customer_data['name'].append(fullname)
            customer_data['email'].append(email)
            customer_data['country'].append(country)

    df = pd.DataFrame(customer_data)

    df.to_csv(path / "customers.csv", index=False)

    return df

 #  *************  Product data  ***************


def products():
    categories = {
        'Electronics': ['Laptop', 'Wireless', 'Mouse', 'Mechanical', 'Keyboard', '4K Monitor 27-inch', 'Noise-Canceling Headphones'],
        'Furniture': ['Ergonomic Office Chair', 'Adjustable Standing Desk', '5-Tier Bookshelf', 'LED Desk Lamp', '3-Drawer File Cabinet'],
        'Stationery': ['Hardcover Grid Notebook', 'Gel Ink Pens (12-Pack)', 'Heavy-Duty Desktop Stapler', 'Dry Erase Markers (8-Pack)', 'A4 Multipurpose Paper Ream'],
        'Apparel': ["Men's Running Shoes", "Women's Yoga Pants", 'Unisex Cotton T-Shirt', 'Classic Denim Jacket', 'Merino Wool Beanie'],
        'Home & Kitchen': ['Espresso Coffee Machine', 'Digital Air Fryer 5-Quart', 'High-Speed Countertop Blender', 'Robot Vacuum Cleaner', 'Stainless Steel Cookware Set'],
        'Beauty & Personal Care': ['Sonic Electric Toothbrush', 'Hydrating Facial Cleanser', 'Broad Spectrum Sunscreen SPF 50', 'Ionic Hair Dryer', 'Waterproof Beard Trimmer'],
        'Sports & Outdoors': ['Non-Slip Yoga Mat', 'Adjustable Dumbbell Set', '2-Person Backpacking Tent', 'Insulated Stainless Steel Bottle', 'Resistance Exercise Bands'],
        'Books': ['Designing Data-Intensive Applications', 'Clean Code', 'Atomic Habits', 'The Pragmatic Programmer', 'Database System Concepts'],
        'Automotive': ['Digital Tire Pressure Gauge', 'Car Phone Mount Holder', 'Portable Car Jump Starter', 'Microfiber Cleaning Cloths (12-Pack)', 'OBD2 Bluetooth Scanner'],
        'Toys & Games': ['Catan Board Game', "Rubik's Cube 3x3 Speed", 'Remote Control Quadcopter Drone', '1000-Piece Jigsaw Puzzle', 'Building Blocks Classic Set']
    }
    flat_list = [(category, product) for category,
                 products in categories.items() for product in products]

    for id in range(1, 51):
        category, product_name = random.choice(flat_list)
        # Remove the selected product to avoid duplicates
        flat_list.remove((category, product_name))
        price = round(random.uniform(10, 1000), 2)

        random_corrupt = random.randint(1, 10)

        if (random_corrupt == 1):
            gen_issue.product(id=id, name=product_name,
                              category=category, price=price)
        else:

            product_data['product_id'].append(id)
            product_data['product_name'].append(product_name)
            product_data['category'].append(category)
            product_data['price'].append(price)

    df = pd.DataFrame(product_data)

    df.to_csv(path / "products.csv", index=False)

    return df

 #  *************  Order data  ***************


def orders(customers_id):
    # Starting date and time for orders
    day_order = datetime(2025, 1, 1, 0, 0, 0)

    statuses = ['Pending', 'Shipped', 'Delivered']

    for i in range(1, 2001):
        cust_id = random.choice(customers_id)
        # randomly select a status for the order
        status_ = random.choice(statuses)

        # number of minutes between orders
        minutes_range = random.randint(1, 100)
        # number of seconds between orders
        seconds_range = random.randint(1, 60)
        # Increment the order date by a random number of minutes and seconds
        day_order = day_order + \
            timedelta(minutes=minutes_range, seconds=seconds_range)
        id = i + 100

        # 10% chance to introduce data issues
        random_corrupt = random.randint(1, 10)
        if random_corrupt == 1:
            gen_issue.order(id=id, custom_id=cust_id,
                            order_date=day_order, status=status_)
        else:
            order_data['order_id'].append(id)
            order_data['cust_id'].append(cust_id)
            order_data['order_date'].append(day_order)
            order_data['status'].append(status_)

    df = pd.DataFrame(order_data)

    df.to_csv(path / "orders.csv", index=False)

    return df

 #  *************  Order Items  ***************


def order_items(products_id, orders_id, products):

    for i in range(1, 2001):

        product_id = random.choice(products_id)
        order_id = random.choice(orders_id)
        # Quantity ordered (number between 1 and 6)
        quantity = random.randint(1, 6)

        
        # get the price of the specific product
        price_result = products.loc[products["product_id"]
                                        == product_id, "price"]
        if len(price_result) == 0:
            # Product not found, skip this iteration
            continue
        
        product_price = price_result.values[0]
        
        if product_price == "":
            # Product price is empty, skip this iteration
            continue
        # Calculate total price based on quantity
        total_price = round(float(product_price) * (quantity), 2)
        id = i + 100  # Generate a unique order item ID

        # 10% chance to introduce data issues
        random_corrupt = random.randint(1, 10)
        if random_corrupt == 6:
            gen_issue.order_items(id=id, order_id=order_id, product_id=product_id,
                                    quantity=quantity, unit_price=product_price, total_price=total_price)
        else:
            order_items_data['order_item_id'].append(id)
            order_items_data['order_id'].append(order_id)
            order_items_data['product_id'].append(product_id)
            order_items_data['quantity'].append(quantity)
            order_items_data['unit_price'].append(product_price)
            order_items_data['total_price'].append(total_price)
        
    df = pd.DataFrame(order_items_data)

    df.to_csv(path / "order_items.csv", index=False)
    
    return df


# *** Generate the datasets ***
if __name__ == "__main__":
    # Generate customers data
    generate_customers = customers()

    # Generate products data
    generate_products = products()

    # Generate orders data
    generate_orders = orders(generate_customers['cust_id'])

    # Generate order items data
    generate_order_items = order_items(
        generate_products['product_id'], generate_orders['order_id'], generate_products)
