"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, Blueprint
from api.models import db, User
from flask_cors import CORS
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api, resources={r"/api/*": {"origins": "https://didactic-xylophone-q7qggvp74pxqh6q-3000.app.github.dev"}})

@api.route('/token', methods=['POST'])
def create_token():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    user = User.query.filter_by(email=email).first()

    if not user or user.password != password:
        print('Credenciales inválidas')
        return jsonify({"msg": "Credenciales inválidas"}), 401

    # Create a new token with the user id inside
    access_token = create_access_token(identity=email)
    print('Token creado:', access_token)
    return jsonify({ "token": access_token, "user_id": user.id })

@api.after_request
def add_cors_headers(response):
   response.headers['Access-Control-Allow-Origin'] = "https://didactic-xylophone-q7qggvp74pxqh6q-3000.app.github.dev/"
   response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
   response.headers['Access-Control-Allow-Methods'] = 'GET,PUT,POST,DELETE'
   return response

##@api.route('/users', methods=['GET'])
##@jwt_required()
##def handle_user():
    ##current_user = get_jwt_identity()
    ##user = User.query.filter_by(email=current_user).first()
    ##if not user:
       ## return jsonify({"msg": "Usuario no encontrado"}), 404

    ##users = User.query.all()
   ## serialized_users = [user.serialize() for user in users]
    ##return jsonify(serialized_users)
