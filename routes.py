from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
import requests
import bcrypt
from sqlalchemy import create_engine

from db_connection import create_url
from db_crud import read_users, create_users


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
        return jsonify(access_token = access_token, refresh_token = refresh_token), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@auth_bp.route("/login", methods = ["POST"])
def login():
    try:
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        user = read_users(connection_engine = engine, username = username)
        if not user:
            return jsonify({"msg": "User not found"}), 401
        password_hash = bcrypt.hashpw(password.encode('utf-8'), user.password_salt.encode('utf-8')).decode('utf-8')
        if user.password_hash != password_hash:
            return jsonify({"msg": "Invalid password"}), 401
        additional_claims = {"role": user.role}
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
        user = read_users(connection_engine = engine, username = identity)
        if not user:
            return jsonify({"msg": "User not found"}), 401
        additional_claims = {"role": user.role}
        access_token = create_access_token(identity = identity, additional_claims = additional_claims)
        return jsonify(access_token = access_token), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@forward_bp.route("/<path:path>", methods = ["GET"])
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
            data = request.get_data() # data dari client yang ingin diproses
        )
        return (resp.content, resp.status_code, resp.headers.items())
    except Exception as e:
        return jsonify({"error": str(e)}), 500
