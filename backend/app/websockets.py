from flask_socketio import SocketIO, emit
from app import socketio
from flask import request
import random

user_sessions = {}

# Sample questions
questions = {
    "Easy": [
        "Reverse a string",
        # Add more easy questions
    ],
    "Medium": [
        "Find the nth Fibonacci number",
        # Add more medium questions
    ],
    "Hard": [
        "Implement a binary search tree",
        # Add more hard questions
    ],
}

@socketio.on('connect')
def handle_connect():
    sid = request.sid
    user_sessions[sid] = {
        'conversation': []
    }  # append a client identifier (if needed )
    print("Client connected")
    emit('message', {'data': 'Welcome to the WebSocket server!'})

@socketio.on('disconnect')
def handle_disconnect():
    if user_sessions:
        user_sessions.pop()  # remove a client identifier (if needed)
    print("Client disconnected")

@socketio.on('select_difficulty')
def handle_select_difficulty(data):
    sid = request.sid
    difficulty = data.get('difficulty')
    if difficulty not in questions:
        emit('bot_message', {'message': 'Invalid difficulty selected. Please choose Easy, Medium, or Hard.'})
        return

    question = random.choice(questions[difficulty])
    # Initialize session
    user_sessions[sid] = {
        'difficulty': difficulty,
        'question': question,
        'conversation': [],
    }
    bot_message = f"Hello, I'm your interviewer. Here's your {difficulty} question:\n{question}"
    emit('bot_message', {'message': bot_message})

@socketio.on('user_message')
def handle_user_message(data):
    sid = request.sid
    user_message = data.get('message', '')
    code = data.get('code', '')
    session = user_sessions.get(sid)

    if session:
        # Save user message and code
        session['conversation'].append({'user': user_message, 'code': code})

        # Generate bot response (simple placeholder)
        bot_reply = "Thank you for your response. Let's discuss your approach."
        # Save bot reply
        session['conversation'].append({'bot': bot_reply})
        emit('bot_message', {'message': bot_reply})
    else:
        emit('bot_message', {'message': 'Please select a difficulty to start the interview.'})