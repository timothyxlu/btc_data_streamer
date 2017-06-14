from pymongo import MongoClient
from persistance.default import DefaultPersister


class MongoPersister(DefaultPersister):
    def __init__(self, db, collection):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client[db]
        self.collection = self.db[collection]

    def __call__(self, data):
        for item in data:
            print(item)
            self.collection.insert_one(item)

    @classmethod
    def get_persister(cls, db, collection):
        p = cls(db, collection)
        return p
