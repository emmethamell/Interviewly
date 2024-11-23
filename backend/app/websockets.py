from flask_socketio import SocketIO, emit
from app import socketio

connected_clients = []

@socketio.on('connect')
def handle_connect():
    connected_clients.append("client")  # append a client identifier (if needed )
    print("Client connected")
    emit('message', {'data': 'Welcome to the WebSocket server!'})

@socketio.on('disconnect')
def handle_disconnect():
    if connected_clients:
        connected_clients.pop()  # remove a client identifier (if needed)
    print("Client disconnected")

@socketio.on('user_message')
def handle_user_message(data):
    user_message = data.get('message')
    print(f"Received message: {user_message}")
    emit('bot_reply', {'reply': f"You said: {user_message}"})