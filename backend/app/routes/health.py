from app.websockets import user_sessions
from flask import Blueprint

health_bp = Blueprint('health', __name__)

@health_bp.route('/health', methods=['GET'])
def health_check():
    return {"status": "routes ok"}, 200

@health_bp.route('/socket-status', methods=['GET'])
def socket_status():
    return {"active_clients": len(user_sessions)}, 200