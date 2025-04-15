from flask import Blueprint, jsonify, session
from app.models.lobby import Lobby

users_bp = Blueprint("users", __name__, url_prefix="/users")


@users_bp.route("/", methods=["GET"])
def get_users():
    if "username" not in session:
        return jsonify({"success": False, "message": "Unauthorized"}), 401

    lobby = Lobby()
    users = lobby.get_users()

    return jsonify({"users": users, "count": len(users)}), 200
