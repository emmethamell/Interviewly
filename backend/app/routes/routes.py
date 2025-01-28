from flask import Blueprint, jsonify, request
from app.websockets import socketio, user_sessions
from app.data_models import db, Interview, User, Question
from flask_cors import cross_origin

interview_bp = Blueprint('routes', __name__)


@interview_bp.route('/active-clients', methods=['GET'])
def active_clients():
    return {"active_clients": user_sessions}, 200


# Fetches basic information for all interviews done by the user
@interview_bp.route('/get-interviews', methods=['GET'])
@cross_origin()
def get_interviews():
    auth0_user_id = request.args.get('auth0_user_id')
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 15))

    offset = (page - 1) * limit

    if not auth0_user_id:
        return jsonify({"error": "Missing required query parameter: auth0_user_id"}), 400

    user = User.query.filter_by(auth0_user_id=auth0_user_id).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    total_interviews = Interview.query.filter_by(auth0_user_id=auth0_user_id).count()
    interviews = Interview.query.filter_by(auth0_user_id=auth0_user_id).offset(offset).limit(limit).all()
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

    return jsonify({"interviews": interviews_data, "total": total_interviews}), 200

# Fetch detailed information on a single interview
@interview_bp.route('/get-single-interview', methods=['GET'])
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
