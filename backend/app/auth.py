from flask import Blueprint, jsonify, request

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/health', methods=['GET'])
def health_check():
    return {"status": "auth ok"}, 200

@auth_bp.route('/signup', methods=['POST'])
def signup():
    return {"status": "auth ok"}, 200

@auth_bp.route('/login', methods=['POST'])
def login():
    return {"status": "auth ok"}, 200

@auth_bp.route('/me', methods=['GET'])
def get_user_data():
    return {"status": "auth ok"}, 200

@auth_bp.route('/logout', methods=['POST'])
def logout():
    return {"status": "auth ok"}, 200