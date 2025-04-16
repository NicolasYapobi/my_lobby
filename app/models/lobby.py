from app.models.user import User
from app.socket import socketio


class Lobby:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Lobby, cls).__new__(cls)
            cls._instance.users = {}
        return cls._instance

    def add_user(self, username):
        if username in self.users:
            return False, "Username already exists"

        if len(username) < 3 or len(username) > 20:
            return False, "Username must be between 3 and 20 characters"

        if not username.isalnum():
            return False, "Username can only contain letters and numbers"

        self.users[username] = User(username)
        return True, f"Welcome to the lobby, {username}"

    def remove_user(self, username):
        if username in self.users:
            del self.users[username]
            return True, "User removed successfully"
        return False, "User not found"

    def get_users(self, sort_by="connected_at"):
        users_list = [user.to_dict() for user in self.users.values()]
        users_list.sort(key=lambda x: x[sort_by])
        return users_list

    def share_message(self, sender, content):

        message_data = {
            "content": content,
            "sender": sender,
            "include_self": False,
        }

        socketio.emit("message", message_data)
        return True, "Message sent successfully"
