import pymongo


class MongoDB:
    def __init__(self, url, db_name):
        client = pymongo.MongoClient(url)
        self.db = client[db_name]

    def get_collections(self):
        return self.db.list_collections()

    def get_collection(self, collection_name: str):
        return self.db[collection_name]

    def get_all_documents(self, collection_name: str):
        return list(self.db[collection_name].find())

    def insert_document(self, collection_name: str, data: dict):
        self.db[collection_name].insert_one(data)

    def insert_documents(self, collection_name: str, data: list):
        self.db[collection_name].insert_many(data)

    def delete_document(self, collection_name: str, query: str):
        self.db[collection_name].delectOne(query)

    def delete_documents(self, collection_name: str, query: str):
        self.db[collection_name].delectMany(query)

    def find_document(self, collection_name: str, query: str):
        return self.db[collection_name].findOne(query)

    def find_documents(self, collection_name: str, query: str):
        return list(self.db[collection_name].find(query))

    def update_document(self, collection_name: str, query: dict, new_data: dict):
        self.db[collection_name].update_one(query, new_data)

    def update_documents(self, collection_name: str, query: dict, new_data: dict):
        self.db[collection_name].update_one(query, new_data)
