from flask import Blueprint, jsonify, session, request
from app.models.lobby import Lobby
from app.utils.error import APIError

users_bp = Blueprint("users", __name__, url_prefix="/users")


@users_bp.route("/", methods=["GET"])
def get_users():
    if "username" not in session:
        return APIError(401, "Unauthorized").to_response()

    valid_sort_fields = ["username", "connected_at"]
    sort_by = request.args.get("sort_by", default="connected_at")

    if sort_by not in valid_sort_fields:
        return APIError(
            400,
            f"Invalid sort field. you can use only use these fields: {', '.join(valid_sort_fields)}",
        ).to_response()

    lobby = Lobby()
    users = lobby.get_users(sort_by=sort_by)

    return jsonify({"users": users, "count": len(users)}), 200
