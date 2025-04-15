from flask import Flask
from flask_socketio import SocketIO
from app.routes.users import users_bp
from app.routes.auth import auth_bp
import os

socketio = SocketIO()


def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv("SECRET_KEY")

    app.register_blueprint(users_bp)
    app.register_blueprint(auth_bp)
    socketio.init_app(app)

    return app
