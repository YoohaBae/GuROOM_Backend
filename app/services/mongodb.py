import pymongo


class MongoDB:
    def __init__():
        client = pymongo.MongoClient(
            "mongodb+srv://admin:<password>@guroom.bazfzg5.mongodb.net/?retryWrites=true&w=majority",
            server_api=ServerApi("1"),
        )
        db = client.test

    def get_all_dictionaries(collection_name):
        return db.collection_name.find().pretty()

    def get_larger_than(collection_name, value):
        return db.collection_name.find(value).pretty()

    def insert(collection_name, data):
        db.collection_name.insert(data)

    def delete_one(collection_name, value):
        db.collection_name.delectOne(value)

    def delete_many(collection_name, value):
        db.collection_name.delectMany(value)

    def update(collection_name, original, desired):
        db.collection_name.update(original, desired)

    def find_one(collection_name, value):
        db.collection_name.findOne(value).pretty()

    def file_folder_sharing_difference(collection_name, absolute_path):
        db.collection_name.find(absolute_path).pretty()

    def redundant_sharing(collection_name, absoulte_path):
        db.collection_name.find(absoulte_path).pretty()

    def deviant_sharing(collection_name, absolute_path):
        db.collection_name.find(absoulte_path).pretty()

    def sharing_changes(collection_name):
        db.collection_name.find(
            {"$where": "function(){" "return (this.file!=this.file)" "}"}
        ).pretty()
