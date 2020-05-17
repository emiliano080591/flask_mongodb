from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash,check_password_hash

def save_user(data,mongo):
    if data['username'] and data['password'] and data['email']:
        hashed_pass=generate_password_hash(data['password'])
        id=mongo.db.users.insert({'username':data['username'],'password':hashed_pass,'email':data['email']})
        
        return {'id':str(id),
                'username':data['username'],
                'email':data['email']}
    else:
        return 0