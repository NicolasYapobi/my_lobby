# My Lobby

A real-time chat application using Flask and Socket.IO (Websocket)

## Installation

### Prerequisites
- Python 3.8+
- pip

### Installation Steps

1. Create a virtual environment
```bash
python -m venv venv
```

2. Activate the virtual environment
```bash
source venv/bin/activate
```
3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root

```
SECRET_KEY=your_secret_key
API_URL=your_localhost
```

## Start the server

```bash
flask run
```

## API Documentation

### Authentication

#### Login
- **Endpoint**: `POST /auth/login`
- **Body**: `{"username": "your_username"}`
- **Rules**: 
  - Username between 3 and 20 characters
  - Only letters and numbers
- **Success response**: `{"success": true, "message": "Welcome to the lobby, your_username"}`

#### Logout
- **Endpoint**: `POST /auth/logout`
- **Success response**: `{"success": true, "message": "User removed successfully"}`

### Users

#### List users
- **Endpoint**: `GET /users/`
- **Optional parameters**:
  - `sort_by`: `username` or `connected_at` (default)
- **Response**: `{"users": [...], "count": n}`

### Messaging

#### Send message
- **Endpoint**: `POST /messages/`
- **Body**: `{"message": "your message"}`
- **Success response**: `{"message": "Message sent successfully"}`

## Client

### Running the client

```bash
python client.py your_username
```

### Available commands

- `/help` - Display list of commands
- `/list` - Display list of connected users
- `/quit` - Exit the program and disconnect the user
- `/send <message>` send a message

### Usage example

## Tests

To run tests:

```bash
pytest
```

## Technologies used

- **Real-time communication**: Flask-SocketIO
- **Client**: socketio