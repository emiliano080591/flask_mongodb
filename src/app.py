from flask import Flask,request,jsonify,Response
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash,check_password_hash
from werkzeug.utils import secure_filename
from bson import json_util
from bson.objectid import ObjectId
from models import save_user
from flask_cors import CORS, cross_origin
import os

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app=Flask(__name__)
app.config['MONGO_URI']='mongodb://localhost/teststore'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
cors = CORS(app)


mongo=PyMongo(app)

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/users',methods=['GET'])
@cross_origin()
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
@cross_origin()
def create_user():
    res=save_user(request.form,mongo)
    if res!=0:
        response=jsonify({'mensaje':'Usuario agregado','ok':True,'user':res})
        response.status_code=200
        return response
    else:
        response=jsonify({'mensaje':'Usuario no agregado','ok':False})
        response.status_code=500
        return response


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

@app.route('/upload',methods=['POST'])
@cross_origin()
def upload_file():
    #si no hay un archivo enviado
    if 'file' not in request.files:
        resp = jsonify({'message' : 'No file part in the request'})
        resp.status_code = 400
        return resp
    file = request.files['file']
    #si el archivo esta vacio
    if file.filename == '':
        resp = jsonify({'message' : 'No file selected for uploading'})
        resp.status_code = 400
        return resp
    #si hay un archivo y contiene la extension permitida se guarda
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        resp = jsonify({'message' : 'File successfully uploaded'})
        resp.status_code = 201
        return resp
    #si no contiene una extension permitida
    else:
        resp = jsonify({'message' : 'Allowed file types are txt, pdf, png, jpg, jpeg, gif'})
        resp.status_code = 400
        return resp

if __name__=="__main__":
    app.run(debug=True)