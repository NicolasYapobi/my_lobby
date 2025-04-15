from datetime import datetime

class User:    
    def __init__(self, username):
        self._username = username
        self.connected_at = datetime.now()
        
    def to_dict(self):
        return {
            'username': self.username,
            'connected_at': self.connected_at.isoformat()
        } 