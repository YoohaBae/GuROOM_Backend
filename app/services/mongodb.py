import pymongo


class MongoDB:
    def __init__(self, url, db_name):
        client = pymongo.MongoClient(url)
        self.db = client[db_name]

    def get_collections(self):
        return self.db.list_collections()

    def get_collection_names(self):
        return list(self.db.list_collection_names())

    def get_collection(self, collection_name: str):
        return self.db[collection_name]

    def drop_collection(self, collection_name):
        return self.db[collection_name].drop()

    def rename_collection(self, collection_name, new_collection_name):
        return self.db[collection_name].rename(new_collection_name)

    def get_all_documents(self, collection_name: str):
        return list(self.db[collection_name].find())

    def insert_document(self, collection_name: str, data):
        self.db[collection_name].insert_one(data)

    def insert_documents(self, collection_name: str, data):
        self.db[collection_name].insert_many(data)

    def delete_document(self, collection_name: str, query=None):
        if query is None:
            query = {}
        self.db[collection_name].delete_one(query)

    def delete_documents(self, collection_name: str, query=None):
        if query is None:
            query = {}
        self.db[collection_name].delete_many(query)

    def find_document(self, collection_name: str, query=None, filter_query=None):
        if query is None:
            query = {}
        return self.db[collection_name].find_one(query, filter_query)

    def find_documents(self, collection_name: str, query=None, filter_query=None):
        if query is None:
            query = {}
        return list(self.db[collection_name].find(query, filter_query))

    def update_document(self, collection_name: str, update_query, query=None):
        if query is None:
            query = {}
        self.db[collection_name].update_one(query, update_query)

    def update_documents(self, collection_name: str, update_query, query=None):
        if query is None:
            query = {}
        self.db[collection_name].update_one(query, update_query)

    def aggregate_documents(self, collection_name: str, pipelines: list):
        return list(self.db[collection_name].aggregate(pipelines))

    def create_index(self, collection_name: str, index: dict):
        self.db[collection_name].createIndex({index})
