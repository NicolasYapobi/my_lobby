from flask import Flask
from app.routes.users import users_bp
from app.routes.auth import auth_bp
from app.socket import socketio
from app.routes.messaging import messaging_bp

import os


def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv("SECRET_KEY")

    app.register_blueprint(users_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(messaging_bp)

    socketio.init_app(app)

    return app
