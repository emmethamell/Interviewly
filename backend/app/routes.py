from flask import Blueprint, jsonify, request
from app.websockets import socketio, user_sessions
from app.data_models import db, Interview, User, Question
from flask_cors import cross_origin

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

# get interviews based on okta id
@bp.route('/get-interviews', methods=['GET'])
@cross_origin()
def get_interviews():
    auth0_user_id = request.args.get('auth0_user_id')
    print("AUTH0 ID", auth0_user_id)

    if not auth0_user_id:
        return jsonify({"error": "Missing required query parameter: auth0_user_id"}), 400

    user = User.query.filter_by(auth0_user_id=auth0_user_id).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    interviews = Interview.query.filter_by(auth0_user_id=auth0_user_id).all()
    interviews_data = [
        {
            "id": interview.id,
            "user_id": interview.auth0_user_id,
            "question_name": interview.question.name,
            "question_difficulty": interview.question.difficulty.value,
            "question_id": interview.question_id,
            "transcript": interview.transcript,
            "score": interview.score,
        }
        for interview in interviews
    ]

    return jsonify({"interviews": interviews_data}), 200


