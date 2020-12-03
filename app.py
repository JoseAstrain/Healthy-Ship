from flask import Flask, escape, request, jsonify, abort
from flask_restplus import Api, Resource, fields
import os.path
from datetime import datetime, date
from werkzeug.contrib.fixers import ProxyFix
import db
import hashlib
from bson.objectid import ObjectId
import json
from licenses_reader.b64 import Converter


flask_app = Flask(__name__)
flask_app.config.SWAGGER_UI_OAUTH_APP_NAME = 'API Healthy Ship'
flask_app.wsgi_app = ProxyFix(flask_app.wsgi_app)

app = Api(app=flask_app, title=flask_app.config.SWAGGER_UI_OAUTH_APP_NAME, 
    version='1.0', description='API Healthy Ship', validate=True)

###################################
#     LICENSE PLATE READER        #
###################################

code_img = app.model('Image code', {
    'code_img': fields.String(required=True, default=False, description='Image base64 coded'),
})

code_text = app.model(
    'License plate reader', {'code': fields.String(required=True, description='Text'), }) 		

name_space = app.namespace(
    'license-plate', description='Servicio que descifra el código contenido en la imagen capturada de una placa vehicular')

@name_space.route('/reader', endpoint='license-reader')
class LicenseReader(Resource):
    @name_space.expect(code_img, validate=False)
    @name_space.response(404, 'Resource not found.')
    @name_space.response(200, 'License plate read successfully.', code_text)
    @name_space.response(500, 'Resource incorrect')
    def post(self):
        requestValue = request.get_json()
        text = requestValue['code_img']

        code_text = Converter.getPNGFromBase64(text)
        # Returns text of the license plate code reader
        return jsonify({"code": code_text})



###################################
#  API HEALTHY SHIP PLATFORM      #
###################################
name_space = app.namespace(
    'healthy-ship', description='Servicios para la administración de los usuarios que interactua en la plataforma')

@name_space.route('/vehicle')
class HealthyShip(Resource):
    
    vehicle = app.model('VehicleModel', {
        'license': fields.String(required=True, default=False, description='Número de placa vehicular'),
        'modelo': fields.String(required=True, default=False, description='Modelo del vehiculo'),
        'date_updated': fields.DateTime(dt_format='rfc822'),
    })
    @name_space.expect(vehicle, validate=False)
    @name_space.response(404, 'Resource not found.')
    @name_space.response(200, 'Vehicle has been registered successfully.')
    @name_space.response(500, 'Resource incorrect')
    def post(self):
        requestValue = request.get_json()
        db.db.vehicles.insert_one(requestValue)

        return jsonify("Register sucessfully")
        
@name_space.route('/vehicle/<string:license>')
class HealthyShipVehicle(Resource):
    @name_space.response(404, 'Resource not found.')
    @name_space.response(200, 'Vehicle found successfully.')
    @name_space.response(500, 'Resource incorrect')
    def get(self, license):
        response = str(db.db.vehicles.find_one({"license": license}))
        return jsonify(response)

@name_space.route('/user')
class HealthyShipUser(Resource):
    
    user = app.model('UserModel', {
        'first_name': fields.String(required=True, default=False, description='Nombre del usuario'),
        'last_name': fields.String(required=True, default=False, description='Apellido del usuario'),
        'email': fields.String(required=True, default=False, description='Correo electrónico del usuario'),
        'password': fields.String(required=True, default=False, description='Contraseña del usuario'),
        'type': fields.String(required=True, default=False, description='Tipo de usuario: OW \(Dueño\), OP \(Operador\), GE \(General\) '),
        'password': fields.String(required=True, default=False, description='Contraseña del usuario'),
        'vehicles': fields.List(fields.String, required=True, default=False, description='Lista de autotransporte'),        
        'created_at': fields.DateTime(dt_format='rfc822'),
    })
    @name_space.expect(user, validate=False)
    @name_space.response(404, 'Resource not found.')
    @name_space.response(200, 'User has been registered successfully.')
    @name_space.response(500, 'Resource incorrect')
    def post(self):
        requestValue = request.get_json()
        h = hashlib.md5(requestValue['password'].encode())
        requestValue['password'] = h.hexdigest()
       
        db.db.users.insert_one(requestValue)

        return jsonify("Register sucessfully")

@name_space.route('/login/<string:email>/<string:password>')
class HealthyShipUser(Resource):
    @name_space.response(404, 'Resource not found.')
    @name_space.response(200, 'Vehicle found successfully.')
    @name_space.response(500, 'Resource incorrect')
    def get(self, email, password):
        response = db.db.users.find_one({"email": email})
        h = hashlib.md5(password.encode())
        password = h.hexdigest()
        if(response==None or (response['password'] != password)):
            abort(404, description="Resource not found")
        return jsonify(str(response))


@name_space.route('/bahia')
class HealthyShipBahia(Resource):
    
    bahia = app.model('BahiaModel', {
        'altitude': fields.String(required=True, default=False, description='Nombre del usuario'),
        'longitude': fields.String(required=True, default=False, description='Apellido del usuario'),
        'latitude': fields.String(required=True, default=False, description='Correo electrónico del usuario'),
        'created_at': fields.DateTime(dt_format='rfc822'),
    })
    @name_space.expect(bahia, validate=False)
    @name_space.response(404, 'Resource not found.')
    @name_space.response(200, 'Bahia has been registered successfully.')
    @name_space.response(500, 'Resource incorrect')
    def post(self):
        requestValue = request.get_json()
       
        db.db.bahias.insert_one(requestValue)

        return jsonify("Register sucessfully")

if __name__ == "__main__":
    flask_app.run(host='0.0.0.0', port=4000)