from flask import Blueprint, request, jsonify, session
from app.models.lobby import Lobby
from app.utils.error import APIError
from app.socket import socketio

messaging_bp = Blueprint("messaging", __name__, url_prefix="/messages")


@socketio.on("message")
def handle_message(data):
    print(data)


@messaging_bp.route("/", methods=["POST"])
def send_message():
    if "username" not in session:
        return APIError(401, "Unauthorized").to_response()

    username = session["username"]
    lobby = Lobby()

    data = request.get_json()

    if not data:
        return APIError(400, "Content required").to_response()

    content = data["message"].strip()
    if not content:
        return APIError(400, "Empty message").to_response()

    success, message = lobby.share_message(username, content)

    if success:
        return jsonify({"message": "Message sent successfully"}), 200
    else:
        return APIError(400, message).to_response()
