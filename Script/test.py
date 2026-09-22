import random
import pandas as pd
from datetime import datetime as dt, timedelta
import os
import pathlib

path = pathlib.Path(__file__).parent.parent 
# with open(path, 'r') as f:
#         sql = f.read()

data = path / "data" / "processed"

df = pd.read_csv(data / "customers.csv").values.tolist()

# data = df.values.tolist()
# print(df)
# print(data)


# print( df.loc[df['product_id'] == 1456])

# tuples to string
p = ("y","d","f")

# print(df.loc[df['order_id'] == 1488])

def test(name):
    p = (('%s',) * len(name) )
    print(','.join(p))


test(("yasin","ali","ahmad"))