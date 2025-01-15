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

# Fetches basic information for all interviews done by the user
@bp.route('/get-interviews', methods=['GET'])
@cross_origin()
def get_interviews():
    auth0_user_id = request.args.get('auth0_user_id')

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
            "score": interview.score,
            "date": interview.date,
        }
        for interview in interviews
    ]

    return jsonify({"interviews": interviews_data}), 200

# Fetch detailed information on a single interview
@bp.route('/get-single-interview', methods=['GET'])
@cross_origin()
def get_single_interview():
    interviewId = request.args.get('interviewId')
    interview = Interview.query.get(interviewId)
    if interview is None:
        return jsonify({"error": "Interview not found"}), 404
    
    interview_data = {
        "id": interview.id,
        "user_id": interview.user_id,
        "question_id": interview.question_id,
        "transcript": interview.transcript,
        "score": interview.score,
        "date": interview.date,
        "final_submission": interview.final_submission,
        "technical_ability": interview.feedback["ratings"]["technical_ability"],
        "problem_solving_score": interview.feedback["ratings"]["problem_solving_skills"],
        "summary": interview.feedback["summary"],
        "language": interview.language
    }

    return jsonify(interview_data), 200
