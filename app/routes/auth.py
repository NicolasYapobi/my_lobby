from flask import Blueprint, request, jsonify, session
from app.models.lobby import Lobby
from app.utils.error import APIError

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data or "username" not in data:
        return APIError(400, "Username required").to_response()

    username = data["username"]
    lobby = Lobby()

    success, message = lobby.add_user(username)

    if success:
        session["username"] = username
        return jsonify({"message": message}), 200
    else:
        return APIError(400, message).to_response()


@auth_bp.route("/logout", methods=["POST"])
def logout():
    username = session.get("username")

    if not username:
        return APIError(401, "User not connected").to_response()

    lobby = Lobby()
    success, message = lobby.remove_user(username)

    if success:
        session.pop("username", None)
        return jsonify({"message": message}), 200
    else:
        return APIError(400, message).to_response()
