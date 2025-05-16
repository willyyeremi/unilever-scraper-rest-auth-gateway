from flask import Flask
from flask_jwt_extended import JWTManager

from config import Config
from route import auth_bp, forward_bp


app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(auth_bp)
app.register_blueprint(forward_bp)

jwt = JWTManager()
jwt.init_app(app)


if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 5000, debug = True)