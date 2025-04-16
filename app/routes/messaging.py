from flask import Blueprint, request, jsonify, session
from app.models.lobby import Lobby
from app.socket import socketio

messaging_bp = Blueprint("messaging", __name__, url_prefix="/messages")


@socketio.on("message")
def handle_message(data):
    print(data)


@messaging_bp.route("/", methods=["POST"])
def send_message():
    if "username" not in session:
        return jsonify({"message": "Unauthorized"}), 401

    username = session["username"]
    lobby = Lobby()

    data = request.get_json()

    if not data:
        return jsonify({"message": "Content required"}), 400

    content = data["message"].strip()
    if not content:
        return jsonify({"message": "Empty message"}), 400

    success, message = lobby.share_message(username, content)

    if success:
        return jsonify({"message": "Message sent successfully"}), 200
    else:
        return jsonify({"message": message}), 400
