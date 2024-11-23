from flask import Blueprint, jsonify, request
from app.websockets import socketio, connected_clients

bp = Blueprint('routes', __name__)

@bp.route('/health', methods=['GET'])
def health_check():
    return {"status": "ok"}, 200

@bp.route('/active-clients', methods=['GET'])
def active_clients():
    return {"active_clients": connected_clients}, 200

@bp.route('/send-message', methods=['POST'])
def send_message():
    data = request.json
    user_message = data.get('message', '')
    socketio.emit('message', {'data': user_message})
    return {"status": "message sent"}, 200

@bp.route('/questions', methods=['GET'])
def get_questions():
    questions = [
        {"id": 1, "difficulty": "Easy", "text": "Reverse a string"},
        {"id": 2, "difficulty": "Medium", "text": "Find the nth Fibonacci number"},
        {"id": 3, "difficulty": "Hard", "text": "Implement a binary search tree"}
    ]
    return {"questions": questions}, 200

@bp.route('/socket-status', methods=['GET'])
def socket_status():
    return {"active_clients": len(connected_clients)}, 200