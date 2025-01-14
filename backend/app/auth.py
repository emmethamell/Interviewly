from flask import Blueprint, jsonify, request
from app.data_models import db, User
from flask_cors import cross_origin

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/health', methods=['GET'])
@cross_origin()
def health_check():
    return {"status": "auth ok"}, 200

@auth_bp.route('/signup', methods=['POST'])
@cross_origin()
def signup():
    data = request.get_json()
    print("DATA: ", data)
    auth0_user_id = data.get('auth0_user_id')
    name = data.get('name')
    email = data.get('email')

    if not auth0_user_id:
        return jsonify({"error": "Auth0 user ID is required"}), 400

    user = User.query.filter_by(auth0_user_id=auth0_user_id).first()
    if user:
        return jsonify({"status": "user already exists"}), 200

    user = User(auth0_user_id=auth0_user_id, name=name, email=email)
    db.session.add(user)
    db.session.commit()

    return jsonify({"status": "user created"}), 201

