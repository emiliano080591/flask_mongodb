from flask_pymongo import PyMongo
from bson.objectid import ObjectId

def save_user(data,mongo):
    if data['username'] and data['password'] and data['email']:
        id=mongo.db.users.insert({'username':data['username'],'password':data['password'],'email':data['email']})
        
        return str(id)
    else:
        return 0