import socketio
import requests
import sys
from dotenv import load_dotenv
import os

load_dotenv()

server_url = os.getenv("API_URL")
session = requests.Session()


def command_help():
    print("/help: show this help")
    print("/list: list all users")
    print("/quit: exit the program")


def command_list():
    response = session.get(f"{server_url}/users/")

    if response.status_code == 200:
        data = response.json()
        users = data["users"]
        count = data["count"]

        print("-" * 50)
        print(f"\nNumber of users: {count}")

        for user in users:
            username = user["username"]
            connected_at = user["connected_at"]
            print(f"{username} - connected at: {connected_at}")
        print("-" * 50)
    else:
        print(f"Error: Impossible to retrieve the list of users")


def command_quit():
    response = session.post(f"{server_url}/auth/logout")
    if response.status_code == 200:
        print("\nExit the client")
        sys.exit(0)
    else:
        print(f"Error: Impossible to logout")


def command_send(message):
    try:
        response = session.post(f"{server_url}/messages/", json={"message": message})
        if response.status_code != 200:
            print(f"Error: {response.json()['message']}")
    except Exception as e:
        print(f"Error: {e}")


commands = {
    "/help": command_help,
    "/list": command_list,
    "/quit": command_quit,
    "/send": command_send,
}


def parse_input(user_input):
    command = user_input.split(" ")[0]
    if command in commands:
        if command == "/send":
            message = user_input.split(" ")[1]
            command_send(message)
        else:
            commands[command]()
    else:
        print("[Invalid command]: type /help to see the list of commands")


def event_handler(cookies):
    sio = socketio.Client()

    sio.connect(server_url, headers={"Cookie": f"session={cookies}"})

    @sio.event
    def message(data):
        print(f"Message from {data['sender']}: {data['content']}")

    try:
        while True:
            user_input = input(f"\n<{username}> ")
            if user_input.startswith("/"):
                parse_input(user_input)
            else:
                print("[Invalid command]: type /help to see the list of commands")
    except KeyboardInterrupt:
        command_quit()


def connection(username):
    login_response = session.post(
        f"{server_url}/auth/login", json={"username": username}
    )

    if login_response.status_code == 200:
        return login_response.cookies
    else:
        print({"error": login_response.text})
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Missing argument: username")
        sys.exit(1)

    username = sys.argv[1]
    cookies = connection(username)
    if cookies:
        print("Connected to WebSocket!")
        event_handler(cookies)
