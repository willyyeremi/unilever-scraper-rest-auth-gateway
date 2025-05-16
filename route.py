from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt
import bcrypt
from sqlalchemy import create_engine

from db_connection import create_url
from db_crud import read_users, create_users


##############################
# common used variable
##############################

url = create_url(ordinal = 1, database_product = "postgresql")
engine = create_engine(url)
auth_bp = Blueprint("auth", __name__, url_prefix = "/auth")


##############################
# routing function
##############################

@auth_bp.route("/register", methods = ["POST"])
def register():
    data = request.get_json()
    data["password_salt"] = bcrypt.gensalt(12).decode('utf-8')
    data["password_hash"] = bcrypt.hashpw(data["password"].encode('utf-8'), data["password_salt"].encode('utf-8')).decode('utf-8')
    del data["password"]
    user = read_users(connection_engine = engine, username = data["username"])
    if user:
        return jsonify({"msg": "User already created"}), 409
    create_users(connection_engine = engine, data = data)
    additional_claims = {"role": data["role"]}
    access_token = create_access_token(identity = data["username"], additional_claims = additional_claims)
    refresh_token = create_refresh_token(identity = data["username"])
    return jsonify(access_token = access_token, refresh_token=refresh_token), 200

@auth_bp.route("/login", methods = ["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    user_list = read_users(connection_engine = engine, username = username)
    if not user_list:
        return jsonify({"msg": "User not found"}), 401
    user = user_list[0]
    password_hash = bcrypt.hashpw(password.encode('utf-8'), user.password_salt.encode('utf-8')).decode('utf-8')
    if user.password_hash != password_hash:
        return jsonify({"msg": "Invalid password"}), 401
    additional_claims = {"role": user.role}
    access_token = create_access_token(identity = username, additional_claims = additional_claims)
    refresh_token = create_refresh_token(identity = username)
    return jsonify(access_token = access_token, refresh_token = refresh_token), 200

@auth_bp.route("/refresh", methods = ["POST"])
@jwt_required(refresh = True)
def refresh():
    identity = get_jwt_identity()
    user_list = read_users(connection_engine = engine, username = identity)
    if not user_list:
        return jsonify({"msg": "User not found"}), 401
    user = user_list[0]
    additional_claims = {"role": user.role}
    access_token = create_access_token(identity = identity, additional_claims = additional_claims)
    return jsonify(access_token = access_token), 200

@auth_bp.route("/protected", methods = ["GET"])
@jwt_required()
def protected():
    identity = get_jwt_identity()
    role = get_jwt().get("role")
    return jsonify(logged_in_as = identity, role = role), 200
