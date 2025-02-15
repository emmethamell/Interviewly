from app import db
from flask import Blueprint, jsonify, request, Response, stream_with_context, g
from app.models.user import User
from app.models.question import Question
from app.models.interview import Interview

from flask_cors import cross_origin
from app.services import interview_service
from app.services.interview_service import InterviewService
from app.repositories.interview_repo import InterviewRepository
from app.services.ai_service import ChatbotManager

import json
import time
import threading
import datetime
import os

interview_bp = Blueprint('routes', __name__)
interview_service = InterviewService(InterviewRepository(), ChatbotManager())

# Create a message queue dictionary to store queues for each session
message_queues = {} # user_id
message_queue_lock = threading.Lock()

# Add constants at the top after imports
SSE_HEADERS = {
    'Content-Type': 'text/event-stream',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'X-Accel-Buffering': 'no'
}

def create_sse_response(generator_func):
    """Helper function to create SSE responses"""
    return Response(
        stream_with_context(generator_func()),
        headers=SSE_HEADERS
    )

def send_sse_message(data):
    """Helper function to format SSE messages"""
    return f"data: {json.dumps(data)}\n\n"

def handle_streaming_response(response_stream, conversation=None):
    """Helper function to handle streaming responses"""
    collected_message = ""
    try:
        for chunk in response_stream:
            content = chunk.choices[0].delta.content if hasattr(chunk, 'choices') else chunk
            if content:
                collected_message += content
                yield send_sse_message({'type': 'chunk', 'content': content})
        
        if conversation is not None:
            conversation.append({
                "role": "assistant",
                "content": [{"type": "text", "text": collected_message}]
            })
            yield send_sse_message({
                'type': 'done',
                'session_data': {
                    'conversation': conversation
                }
            })
    except Exception as e:
        print(f"Error in stream: {str(e)}")
        yield send_sse_message({'error': str(e)})

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
        "score": interview.feedback["qualitative_score"],
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

@interview_bp.route('/start-interview', methods=['POST'])
def start_interview():
    try:
        data = request.get_json()
        difficulty = data.get('difficulty')
        if not difficulty:
            return jsonify({"error": "Difficulty is required"}), 400
            
        question = interview_service.get_random_question(difficulty)
        if isinstance(question, str):  # Error message
            return jsonify({"error": question}), 400
            
        return jsonify({
            "message": f"Hello my name is Cody, I'll be your interviewer. Let's get started with your question:\n\n {question.content}",
            "question": {
                "id": question.id,
                "content": question.content,
                "difficulty": question.difficulty.value,
                "name": question.name
            }
        }), 200
        
    except Exception as e:
        print(f"Error in start_interview: {str(e)}")
        response = jsonify({"error": str(e)})
        return response, 500

@interview_bp.route('/stream', methods=['GET'])
def stream():
    auth0_user_id = request.args.get('auth0_user_id')
    if not auth0_user_id:
        return jsonify({"error": "Missing auth0_user_id"}), 400

    def generate():
        yield send_sse_message({'type': 'connected'})
        while True:
            if request.environ.get('wsgi.input_terminated', False):
                break
            yield send_sse_message({'type': 'heartbeat'})
            time.sleep(0.1)

    return create_sse_response(generate)

@interview_bp.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        conversation = data.get('session_data', {}).get('conversation', [])
        
        # Construct prompt
        prompt = f"Message: {data.get('message', '')}\nCode: {data.get('code', '')}" if data.get('code') else data.get('message', '')
        conversation.append({
            "role": "user",
            "content": [{"type": "text", "text": prompt}]
        })
        
        response_stream = interview_service.ai_service.generate_response(conversation)
        return create_sse_response(lambda: handle_streaming_response(response_stream, conversation))
        
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        return jsonify({"error": str(e)}), 500

@interview_bp.route('/submit', methods=['POST'])
def submit_solution():
    try:
        data = request.get_json()
        
        # If code analysis is requested
        if 'session_data' in data:
            conversation = data['session_data'].get('conversation', [])
            analysis_prompt = [
                *conversation,
                {
                    "role": "user",
                    "content": [{"type": "text", "text": f"Please analyze this solution code and provide detailed feedback:\n\n{data.get('code', '')}"}]
                }
            ]
            response_stream = interview_service.ai_service.generate_response(analysis_prompt)
            return create_sse_response(lambda: handle_streaming_response(response_stream, conversation))
            
        # If final submission
        user = User.query.filter_by(auth0_user_id=data.get('userId')).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        feedback = interview_service.ai_service.generate_final_analysis(
            conversation=data.get('conversation', []),
            final_code=data.get('code', '')
        )
        
        interview = Interview(
            user_id=user.id,
            auth0_user_id=data.get('userId'),
            question_id=int(data.get('questionId')),
            final_submission=data.get('code', ''),
            language=data.get('language', 'python'),
            date=datetime.datetime.now(datetime.timezone.utc),
            score=feedback.get('qualitative_score', 'No Score'),
            transcript=json.dumps(data.get('conversation', [])),
            feedback=feedback
        )

        db.session.add(interview)
        db.session.commit()
        
        return jsonify({
            "success": True,
            "feedback": feedback,
            "interview_id": interview.id
        }), 200

    except Exception as e:
        print(f"Error in submit endpoint: {str(e)}")
        return jsonify({"error": str(e)}), 500