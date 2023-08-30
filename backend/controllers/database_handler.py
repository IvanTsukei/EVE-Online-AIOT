from pymongo import MongoClient
from datetime import datetime
from file_access import secret_reader
from market_generator import all_orders
import pandas as pd

def get_database():
    connection_string = f'mongodb+srv://{str(secret_reader("database","username"))}:{str(secret_reader("database","password"))}@{str(secret_reader("database","cluster"))}.mongodb.net/?retryWrites=true&w=majority'
    client = MongoClient(connection_string)
    mydb = client[f"{str(secret_reader('database','cluster_name'))}"]
    mycol = mydb["market"]
    mycol.insert_many(all_orders())
    print(f"Done. Output to MongoDB at: {datetime.today().strftime('%Y-%m-%d %H:%M')}")

def fetch_database():
    connection_string = f'mongodb+srv://{str(secret_reader("database","username"))}:{str(secret_reader("database","password"))}@{str(secret_reader("database","cluster"))}.mongodb.net/?retryWrites=true&w=majority'
    client = MongoClient(connection_string)
    mydb = client[f"{str(secret_reader('database','cluster_name'))}"]
    mycol = mydb["market"].find()
    return mycol

def fetch_database_latest(pipeline, create_indx, indx_nme, itm):
    connection_string = f'mongodb+srv://{str(secret_reader("database","username"))}:{str(secret_reader("database","password"))}@{str(secret_reader("database","cluster"))}.mongodb.net/?retryWrites=true&w=majority'
    client = MongoClient(connection_string)
    mydb = client[f"{str(secret_reader('database','cluster_name'))}"]
    # Creating passed index for quick query.
    if create_indx == True: mydb["market"].create_index(f'{indx_nme}', name=f'{indx_nme}_index')
    mycol = mydb["market"].find(pipeline)
    items_df = pd.DataFrame(mycol)
    if create_indx == True: mydb["market"].drop_indexes()
    return items_df