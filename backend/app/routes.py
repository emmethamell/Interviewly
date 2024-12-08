from flask import Blueprint, jsonify, request
from app.websockets import socketio, user_sessions
from app.data_models import db, Interview, User, Question

bp = Blueprint('routes', __name__)

@bp.route('/health', methods=['GET'])
def health_check():
    return {"status": "routes ok"}, 200

@bp.route('/active-clients', methods=['GET'])
def active_clients():
    return {"active_clients": user_sessions}, 200


@bp.route('/socket-status', methods=['GET'])
def socket_status():
    return {"active_clients": len(user_sessions)}, 200

