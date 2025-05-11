from pymongo import MongoClient

def get_db():
    client = MongoClient("mongodb://root:example@localhost:27017/")
    db = client["spendly"]
    return db
