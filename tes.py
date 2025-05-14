import json

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token

from db_connection import engine
from db_crud import read_users, create_users


auth_bp = Blueprint("auth", __name__, url_prefix = "/auth")

@auth_bp.route("/register", methods = ["POST"])
def login():
    data = json.loads(request.get_json())
    user = read_users(engine, data["username"])
    if not user:
        return jsonify({"msg": "User already created"}), 401
    create_users(connection_engine = engine, data = data)
    additional_claims = {"role": data["role"]}
    access_token = create_access_token(identity = data["username"], additional_claims = additional_claims)
    refresh_token = create_refresh_token(identity = data["username"])
    return jsonify(access_token=access_token, refresh_token=refresh_token), 200