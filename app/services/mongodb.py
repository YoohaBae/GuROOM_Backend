import pymongo
import os


class MongoDB:
    def __init__(self):
        URL = "mongodb://127.0.0.1:27017"
        client = pymongo.MongoClient(URL)
        db_name = os.getenv("DB_NAME")
        self.db = client[db_name]

    def get_all_dictionaries(self, collection_name):
        return self.db.collection_name.find().pretty()

    def get_larger_than(self, collection_name, value):
        return self.db.collection_name.find(value).pretty()

    def insert(self, collection_name, data):
        self.db.collection_name.insert(data)

    def delete_one(self, collection_name, value):
        self.db.collection_name.delectOne(value)

    def delete_many(self, collection_name, value):
        self.db.collection_name.delectMany(value)

    def update(self, collection_name, original, desired):
        self.db.collection_name.update(original, desired)

    def find_one(self, collection_name, value):
        return self.db.collection_name.findOne(value).pretty()

    def file_folder_sharing_difference(self, collection_name, absolute_path):
        return self.db.collection_name.find(absolute_path).pretty()

    def redundant_sharing(self, collection_name, absolute_path):
        return self.db.collection_name.find(absolute_path).pretty()

    def deviant_sharing(self, collection_name, absolute_path):
        return self.db.collection_name.find(absolute_path).pretty()

    def sharing_changes(self, collection_name):
        self.db.collection_name.find(
            {"$where": "function(){" "return (this.file!=this.file)" "}"}
        ).pretty()
