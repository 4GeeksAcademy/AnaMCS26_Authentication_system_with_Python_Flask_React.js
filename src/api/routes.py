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

@api.route("/user", methods=["POST"])
def add_user():
    email = request.json.get("email")
    password = request.json.get("password")
    is_active = True

    required_fields = [email, password, is_active]

    if any(field is None for field in required_fields):
        return jsonify({'error': 'You must provide an email and a password'}), 400
    
    user = User.query.filter_by(email=email).first()

    if user:
        return jsonify({"msg": "This user already has an account"}), 401
    
    try:
        new_user = User(email=email, password=password, is_active=is_active)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'response': 'User added successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400