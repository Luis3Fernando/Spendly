from pymongo import MongoClient

def get_db():
    """Obtiene la conexión a la base de datos MongoDB"""
    client = MongoClient("mongodb://root:example@localhost:27017/")
    db = client["spendly"]
    return db
