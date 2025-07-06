from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt
import requests
import bcrypt
from sqlalchemy import create_engine

from db_connection import create_url
from db_crud import create_tr_users, read_tr_users, update_tr_users, read_ms_roles


##############################
# common used variable
##############################

FORWARD_BASE_URL = "http://localhost:5001"

url = create_url(ordinal = 1, database_product = "postgresql")
engine = create_engine(url)

auth_bp = Blueprint("auth", __name__, url_prefix = "/auth")
forward_bp = Blueprint("forward", __name__)


##############################
# routing function
##############################

@auth_bp.route("/register", methods = ["POST"])
def register():
    try:
        data = request.get_json()
        user = read_ms_roles(connection_engine = engine, username = data["username"])
        if user:
            return jsonify({"msg": "User already created"}), 409
        roles = read_ms_roles(connection_engine = engine, roles = data["roles"])
        if not roles:
            return jsonify({"msg": "Roles not exists"}), 409
        data["password_salt"] = bcrypt.gensalt(12).decode('utf-8')
        data["password_hash"] = bcrypt.hashpw(data["password"].encode('utf-8'), data["password_salt"].encode('utf-8')).decode('utf-8')
        del data["password"]
        data["roles_id"] = roles.id
        del data["roles"]
        create_tr_users(connection_engine = engine, data = data)
        additional_claims = {"roles_id": data["roles_id"]}
        access_token = create_access_token(identity = data["username"], additional_claims = additional_claims)
        refresh_token = create_refresh_token(identity = data["username"])
        return jsonify(access_token = access_token, refresh_token = refresh_token), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@auth_bp.route("/login", methods = ["POST"])
def login():
    try:
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        user = read_tr_users(connection_engine = engine, username = username)
        if not user:
            return jsonify({"msg": "User not found"}), 401
        password_hash = bcrypt.hashpw(password.encode('utf-8'), user.password_salt.encode('utf-8')).decode('utf-8')
        if user.password_hash != password_hash:
            return jsonify({"msg": "Invalid password"}), 401
        additional_claims = {"roles_id": user.roles_id}
        access_token = create_access_token(identity = username, additional_claims = additional_claims)
        refresh_token = create_refresh_token(identity = username)
        return jsonify(access_token = access_token, refresh_token = refresh_token), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@auth_bp.route("/update", methods = ["POST"])
@jwt_required()
def update():
    try:
        additional_claims = get_jwt()
        roles_id = additional_claims.get("roles_id")
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        if data.get("username_update") and data.get("password_update"):
            return jsonify({"msg": "Cannot change username and password simultaneously"}), 401
        new_data = {}
        if data.get("username_update"):
            username_update = data.get("username_update")
            user = read_tr_users(connection_engine = engine, username = username_update)
            if user:
                return jsonify({"msg": "Username is exist, choose another one"}), 401
            new_data["username"] = username_update
        if data.get("password_update"):
            password_update = data.get("password_update")
            user = read_tr_users(connection_engine = engine, username = username)
            password_hash = bcrypt.hashpw(password.encode('utf-8'), user.password_salt.encode('utf-8')).decode('utf-8')
            if user.password_hash != password_hash:
                return jsonify({"msg": "Invalid old password"}), 401
            new_data["password_update"] = bcrypt.gensalt(12).decode('utf-8')
            new_data["password_hash"] = bcrypt.hashpw(password_update.encode('utf-8'), new_data["password_salt"].encode('utf-8')).decode('utf-8')
        if data.get("is_active_update"):
            new_data["is_active"] = data.get("is_active_update")
        update_tr_users(connection_engine = engine, written_username = username, **new_data)
        additional_claims = {"roles_id": f"{roles_id}"}
        access_token = create_access_token(identity = username, additional_claims = additional_claims)
        refresh_token = create_refresh_token(identity = username)
        return jsonify(access_token = access_token, refresh_token = refresh_token), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@auth_bp.route("/refresh", methods = ["POST"])
@jwt_required(refresh = True)
def refresh():
    try:
        identity = get_jwt_identity()
        user = read_tr_users(connection_engine = engine, username = identity)
        if not user:
            return jsonify({"msg": "User not found"}), 401
        additional_claims = {"roles_id": user.roles_id}
        access_token = create_access_token(identity = identity, additional_claims = additional_claims)
        return jsonify(access_token = access_token), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@forward_bp.route("/<path:path>", methods = ["POST", "GET", "PUT", "PATCH", "DELETE"])
@jwt_required()
def forward(path):
    try:
        method = request.method
        target_url = f"{FORWARD_BASE_URL}/{path}"
        headers = dict(request.headers)
        headers.pop("Host", None) # hilangkan header Host supaya nanti diganti dengan host tempat tujuan saat sampai
        resp = requests.request(
            method = method,
            url = target_url,
            params = request.args.to_dict(),
            headers = headers, # kirim informasi client ke backend untuk autentikasi berbasis JWT (RBAC, logging)
            data = request.get_data() # data dalam body dari client yang ingin diproses
        )
        return (resp.content, resp.status_code, resp.headers.items())
    except Exception as e:
        return jsonify({"error": str(e)}), 500
