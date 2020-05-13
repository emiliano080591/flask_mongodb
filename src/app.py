from flask import Flask,request,jsonify,Response
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash,check_password_hash
from bson import json_util
from bson.objectid import ObjectId
from models import save_user

app=Flask(__name__)
app.config['MONGO_URI']='mongodb://localhost/teststore'

mongo=PyMongo(app)

@app.route('/users',methods=['GET'])
def get_users():
    users=mongo.db.users.find()
    response=json_util.dumps(users)
    return Response(response,mimetype='application/json')

@app.route('/users/<id>',methods=['GET'])
def get_user(id):
    user=mongo.db.users.find_one({'_id':ObjectId(id)})
    response=json_util.dumps(user)
    return Response(response,mimetype='application/json')

@app.route('/users',methods=['POST'])
def create_user():
    username=request.json['username']
    password=request.json['password']
    email=request.json['email']

    if username and password and email:
        hashed_pass=generate_password_hash(password)
        id=mongo.db.users.insert({"username":username,"password":hashed_pass,"email":email})
        response={
            'id':str(id),
            'username':username,
            'email':email,
            'password':hashed_pass,
            'ok':True,
            'mensaje':'Usuario creado'
        }
        return response
    else:
        return not_found()

@app.route('/users/<id>',methods=['PUT'])
def update_user(id):
    username=request.json['username']
    password=request.json['password']
    email=request.json['email']

    if username and password and email:
        hashed_pass=generate_password_hash(password)
        mongo.db.users.update_one({'_id':ObjectId(id)},{'$set':{
            'username':username,
            'password':hashed_pass,
            'email':email
            }
        })
        response=jsonify({
            'id':str(id),
            'username':username,
            'email':email,
            'password':hashed_pass,
            'ok':True,
            'mensaje':'Usuario actualizado'
        })
        response.status_code=200
        return response
    else:
        return not_found()

@app.route('/users/<id>',methods=['DELETE'])
def delete_user(id):
    mongo.db.users.delete_one({'_id':ObjectId(id)})
    response=jsonify({'mensaje':'Usuario eliminado','ok':True})
    response.status_code=200
    return response

@app.errorhandler(404)
def not_found(error=None):
    mensaje=jsonify({
        'mensaje':'Recurso no encontrado '+request.url,
        'status':404,
        'ok':False
    })
    mensaje.status_code=404
    return mensaje

@app.route('/registro',methods=['POST'])
def registrar_usuario():
    res=save_user(request.form,mongo)
    if res!=0:
        response=jsonify({'mensaje':'Usuario agregado','ok':True,'id':res})
        response.status_code=200
        return response
    else:   
        response=jsonify({'mensaje':'Usuario no agregado','ok':False})
        response.status_code=500
        return response

if __name__=="__main__":
    app.run(debug=True)