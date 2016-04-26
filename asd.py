from pymongo import MongoClient

client = MongoClient()
db = client.test
test = db.test

b = {
    'author': 'cat',
    'yeah': 'no',
    'asd':'asd'
}

a = test.insert_one(b)