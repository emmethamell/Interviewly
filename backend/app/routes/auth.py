from flask import Blueprint, jsonify, request
from app import db
from app.models.user import User
from flask_cors import cross_origin
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

auth_bp = Blueprint('auth', __name__)


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

    try:
        session = db.create_scoped_session()
        
        user = session.query(User).filter_by(auth0_user_id=auth0_user_id).first()
        
        if not user:
            user = User(
                auth0_user_id=auth0_user_id,
                name=name,
                email=email
            )
            session.add(user)
            session.commit()
            
        # Close the session
        session.close()
        
        return jsonify({
            'id': user.id,
            'auth0_user_id': user.auth0_user_id,
            'name': user.name,
            'email': user.email
        }), 200
        
    except Exception as e:
        # Make sure to rollback on error
        if 'session' in locals():
            session.rollback()
            session.close()
        return jsonify({'error': str(e)}), 500

