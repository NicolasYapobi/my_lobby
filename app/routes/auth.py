from flask import Blueprint, request, jsonify, session
from app.models.lobby import Lobby

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data or "username" not in data:
        return jsonify({"success": False, "message": "Username required"}), 400

    username = data["username"]
    lobby = Lobby()

    success, message = lobby.add_user(username)

    if success:
        session["username"] = username
        return jsonify({"success": True, "message": message}), 200
    else:
        return jsonify({"success": False, "message": message}), 400


@auth_bp.route("/logout", methods=["POST"])
def logout():
    username = session.get("username")

    if not username:
        return jsonify({"success": False, "message": "User not connected"}), 401

    lobby = Lobby()
    success, message = lobby.remove_user(username)

    if success:
        session.pop("username", None)
        return jsonify({"success": True, "message": message}), 200
    else:
        return jsonify({"success": False, "message": message}), 400
