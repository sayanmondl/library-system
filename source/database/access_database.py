from pymongo import MongoClient
import os
import json


class MongoDatabase:
    def __init__(self) -> None:
        uri = os.environ.get("CONNECTION_STRING")
        self.client = MongoClient(uri)

    def connect_database(self, dbname):
        try:
            self.database = self.client.get_database(dbname)
        except Exception as e:
            raise Exception(
                "Unable to find the document due to the following error: ", e
            )

    def create_collection(self, collection_name):
        try:
            self.collection = self.database.create_collection(collection_name)
        except Exception as e:
            raise Exception(
                "Unable to find the document due to the following error: ", e
            )

    def access_collection(self, collection_name):
        try:
            self.collection = self.database[collection_name]
        except Exception as e:
            raise Exception(
                "Unable to find the document due to the following error: ", e
            )

    def delete_collection(self, collection_name):
        try:
            self.collection = self.database.drop_collection(collection_name)
        except Exception as e:
            raise Exception(
                "Unable to find the document due to the following error: ", e
            )

    def delete_database(self, dbname):
        try:
            self.collection = self.client.drop_database(dbname)
        except Exception as e:
            raise Exception(
                "Unable to find the document due to the following error: ", e
            )

    def list_all_collections(self):
        try:
            collection_list = self.database.list_collections()
            for c in collection_list:
                print(c)
        except Exception as e:
            raise Exception(
                "Unable to find the document due to the following error: ", e
            )

    def get_user_data(self, username):
        self.access_collection("users")
        return self.collection.find_one({"username": username})

    def delete_user(self, username):
        self.connect_database("library_database")
        self.access_collection("users")
        self.collection.delete_one({"username": username})

    def clear_issues(self):
        self.connect_database("library_database")
        self.delete_collection("issues")
        self.create_collection("issues")


# For temporary modifications
if __name__ == "__main__":
    db = MongoDatabase()
    db.connect_database("library_database")
    db.access_collection("books")
    # with open("books.json", "r") as file:
    #     books = json.loads(file.read())
    #     db.collection.insert_many(books)
    db.collection.update_many({}, {"$set": {"available": True}})
