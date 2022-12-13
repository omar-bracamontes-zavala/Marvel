from flask_pymongo import pymongo

client = pymongo.MongoClient('mongodb+srv://admin:admin123@cluster0.bdsgvtx.mongodb.net/?retryWrites=true&w=majority')
mongo = client.get_database('Marvel')