from flask_socketio import SocketIO, emit
from app import socketio
from flask import request
from app.services.websocket_service import WebSocketService

websocket_service = WebSocketService()

@socketio.on('connect')
def handle_connect():
    welcome_message = websocket_service.create_session(request.sid)
    print("Client connected")
    emit('message', {'data': welcome_message})

@socketio.on('disconnect')
def handle_disconnect():
    removed_session = websocket_service.remove_session(request.sid)
    if removed_session:
        print(f"Session for {request.sid} removed.")
    else:
        print(f"No session found for {request.sid}.")
    print("Client disconnected")

@socketio.on('select_difficulty')
def handle_select_difficulty(data):
    response = websocket_service.handle_difficulty_selection(request.sid, data.get('difficulty'))
    if 'error' in response:
        emit('bot_message', {'message': response['error']})
    else:
        emit('bot_message', {'first_message': True, 'message': response})

@socketio.on('user_message')
def handle_user_message(data):
    response = websocket_service.handle_user_message(
        request.sid,
        data.get('message', ''),
        data.get('code', '')
    )
    emit('bot_message', {'first_message': False, 'message': response})

@socketio.on('submit_solution')
def handle_submit_solution(data):
    response = websocket_service.handle_solution_submission(
        request.sid,
        data.get('userId'),
        data.get('code'),
        data.get('language')
    )
    
    if 'error' in response:
        emit('error', {'message': response['error']})
    else:
        emit('final_analysis', response)