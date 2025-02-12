from app import db
from flask import Blueprint, jsonify, request
from app.services.websocket_service import WebSocketService
from app.models.user import User
from app.models.question import Question
from app.models.interview import Interview

from flask_cors import cross_origin
from app.services import interview_service

interview_bp = Blueprint('routes', __name__)


@interview_bp.route('/active-clients', methods=['GET'])
@cross_origin()
def active_clients():
    return {"active_clients": WebSocketService.user_sessions}, 200


@interview_bp.route('/get-interviews', methods=['GET'])
@cross_origin()
def get_interviews():
    try:
        auth0_user_id = request.args.get('auth0_user_id')
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 15))

        if not auth0_user_id:
            return jsonify({"error": "Missing required query parameter: auth0_user_id"}), 400

        interviews_data, total = interview_service.get_user_interviews(
            auth0_user_id=auth0_user_id,
            page=page,
            limit=limit
        )
        print("INTERVIEWS: ", interviews_data)
        print("TOTAL: ", total)
        return jsonify({
            "interviews": interviews_data, 
            "total": total
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

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
        "summary": interview.feedback["summary"],
        "language": interview.language,
        "question_name": interview.question.name,
        "question_difficulty": interview.question.difficulty.value,
        "question_id": interview.question_id,
        "question_content": interview.question.content,
    }

    return jsonify(interview_data), 200

@interview_bp.route('/get-interview-stats', methods=['GET'])
@cross_origin()
def get_interview_stats():
    """
    Get interview statistics for a user.
    returns: {success_rate, easy_successes, medium_successes, hard_successes}
    """
    try:
        auth0_user_id = request.args.get('auth0_user_id')
        stats = interview_service.calculate_interview_stats(auth0_user_id)
        print("STATS: ", stats)
        return jsonify(stats), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500