from flask import Flask
from flask_socketio import SocketIO
from app.routes.users import users_bp


socketio = SocketIO()

def create_app():
    app = Flask(__name__)        

    app.register_blueprint(users_bp)
    socketio.init_app(app)
    
    return app
