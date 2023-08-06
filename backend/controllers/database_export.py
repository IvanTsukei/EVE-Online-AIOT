from pymongo import MongoClient
from datetime import datetime
from backend.controllers.file_access import secret_reader
from backend.controllers.market_generator import all_orders

def get_database():
    connection_string = f'mongodb+srv://{str(secret_reader("database","username"))}:{str(secret_reader("database","password"))}@{str(secret_reader("database","cluster"))}.mongodb.net/?retryWrites=true&w=majority'
    client = MongoClient(connection_string)
    mydb = client[f"{str(secret_reader('database','cluster_name'))}"]
    mycol = mydb["market"]
    mycol.insert_many(all_orders())
    print(f"Done. Output to MongoDB at: {datetime.today().strftime('%Y-%m-%d %H:%M')}")