from pymongo import MongoClient
from backend.controllers.file_access import secret_reader

def get_database():
    connection_string = f'mongodb+srv://{str(secret_reader("database","username"))}:{str(secret_reader("database","password"))}@{str(secret_reader("database","cluster"))}.mongodb.net/?retryWrites=true&w=majority'
    client = MongoClient(connection_string)
    mydb = client[f"{str(secret_reader('database','cluster_name'))}"]
    mycol = mydb["market"]

    x = mycol.insert_many()