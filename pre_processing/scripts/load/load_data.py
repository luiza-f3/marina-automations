from pymongo import MongoClient
from pre_processing.config.settings import *
import asyncio

async def load_mongodb(data=None, coll_name=None):
    if data is None or coll_name is None:
        raise ValueError("Data and collection name are required")

    client = MongoClient(DATABASE_URI)
    db = client[DB_NAME]
    collection = db[coll_name]

    try:
        collection.insert_many(data.to_dict('records'))
        print(f"Data loaded to {coll_name}")
    except Exception as e:
        print(f"Error loading data: {e}")
    finally:
        client.close()

def load_autopatrocinado(data):
    ...
    # asyncio.run(load_mongodb(data, AUTOPATROCINADO_COLL))

def load_reservas(data):
    asyncio.run(load_mongodb(data, RESERVAS_COLL))

def load_folha_beneficios(data):
    ...
    # asyncio.run(load_mongodb(data, FOLHA_BENEFICIOS_COLL))

def load_folha_pagamento(data):
    asyncio.run(load_mongodb(data, FOLHA_PAGAMENTO_COLL))