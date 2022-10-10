import pymongo
import os


class MongoDB:
    def __init__(self):
        URL = os.getenv("URL")
        client = pymongo.MongoClient(URL)
        db_name = os.getenv("DB_NAME")
        self.db = client[db_name]

    def get_all_collections(self, collection_name):
        return self.db.collection_name.find().pretty()

    def insert_document(self, collection_name, data):
        self.db.collection_name.insert(data)

    def delete_collection(self, collection_name, value):
        self.db.collection_name.delectOne(value)

    def delete_multiple_collections(self, collection_name, value):
        self.db.collection_name.delectMany(value)

    def update_document(self, collection_name, original, desired):
        self.db.collection_name.update(original, desired)

    def find_document(self, collection_name, value):
        return self.db.collection_name.findOne(value).pretty()

    def find_multiple_documents(self, collection_name, value):
        return self.db.collection_name.find(value).pretty()
