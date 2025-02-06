from flask import Blueprint, jsonify, request
from app import db
from app.models.user import User
from flask_cors import cross_origin
from contextlib import contextmanager

auth_bp = Blueprint('auth', __name__)

@contextmanager
def db_transaction():
    try:
        yield
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise
    finally:
        db.session.remove()  

@auth_bp.route('/signup', methods=['POST'])
@cross_origin()
def signup():
    data = request.get_json()
    auth0_user_id = data.get('auth0_user_id')
    name = data.get('name')
    email = data.get('email')

    if not auth0_user_id:
        return jsonify({"error": "Auth0 user ID is required"}), 400

    try:
        with db_transaction():
            user = User.query.filter_by(auth0_user_id=auth0_user_id).first()
            
            if not user:
                user = User(
                    auth0_user_id=auth0_user_id,
                    name=name,
                    email=email
                )
                db.session.add(user)
            
            response_data = {
                'id': user.id,
                'auth0_user_id': user.auth0_user_id,
                'name': user.name,
                'email': user.email
            }
        
        return jsonify(response_data), 200
        
    except Exception as e:
        print(f"Signup error: {str(e)}")
        return jsonify({'error': str(e)}), 500

