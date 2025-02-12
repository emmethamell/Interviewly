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

interview_bp = Blueprint('routes', __name__)
interview_service = InterviewService(InterviewRepository(), ChatbotManager())

# Create a message queue dictionary to store queues for each session
message_queues = {} # user_id
message_queue_lock = threading.Lock()

def cors_headers():
    return {
        'Access-Control-Allow-Origin': 'http://localhost:5173',
        'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Credentials': 'true'
    }

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

@interview_bp.route('/start-interview', methods=['OPTIONS'])
def start_interview_options():
    return Response('', headers=cors_headers())

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
        for key, value in cors_headers().items():
            response.headers[key] = value
        return response, 500


"""
# Queue structure for a user:
message_queues = {
    "auth0|123": Queue([
        {
            "type": "ai_response",
            "message": "That's a good approach! Have you considered edge cases?",
            "session_data": {...}
        },
        {
            "type": "ai_response",
            "message": "Let's analyze your solution...",
            "session_data": {...}
        }
    ]),
    "auth0|456": Queue([...])  # another users queue
}
"""
@interview_bp.route('/stream', methods=['GET'])
def stream():
    """
    Long-lived SSE endpoint that maintains an open connection with the client.
    Currently used only to:
    1. Establish initial connection
    2. Maintain connection with heartbeats
    3. Handle clean disconnection
    
    Message Types:
    - connected: Initial connection confirmation
    - heartbeat: Keep-alive signal
    - error: Any error messages
    """
    
    auth0_user_id = request.args.get('auth0_user_id')
    if not auth0_user_id:
        return jsonify({"error": "Missing auth0_user_id"}), 400
    
    print(f"Starting stream for user {auth0_user_id}")
    
    def generate():
        try:
            # Send initial connection message
            yield f"data: {json.dumps({'type': 'connected'})}\n\n"
            
            while True:
                try:
                    # Check if client is still connected
                    if request.environ.get('wsgi.input_terminated', False):
                        print(f"Client disconnected for user {auth0_user_id}")
                        break
                        
                    # Send heartbeat
                    yield f"data: {json.dumps({'type': 'heartbeat'})}\n\n"
                    
                    # Add a small delay to prevent CPU spinning
                    time.sleep(0.1)
                    
                except GeneratorExit:
                    print(f"Generator exited for user {auth0_user_id}")
                    break
                except Exception as e:
                    print(f"Error in stream loop: {str(e)}")
                    yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"
                    break
                    
        except Exception as e:
            print(f"Error in stream generator: {str(e)}")
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"

    headers = {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'X-Accel-Buffering': 'no',
        **cors_headers()
    }
    
    return Response(
        stream_with_context(generate()),
        headers=headers
    )

@interview_bp.route('/chat', methods=['OPTIONS'])
def chat_options():
    return Response('', headers=cors_headers())


@interview_bp.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        code = data.get('code', '')
        session_data = data.get('session_data', {})
        
        # Store the conversation in session data
        conversation = session_data.get('conversation', [])
        
        # Add the users message to the conversation
        if code:
            prompt = f"Message: {user_message}\nCode: {code}"
        else:
            prompt = user_message
            
        conversation.append({
            "role": "user",
            "content": [{"type": "text", "text": prompt}]
        })
        
        def generate():
            try:
                # Get streaming response from OpenAI
                response_stream = interview_service.ai_service.generate_response(conversation)
                
                collected_message = ""
                
                for chunk in response_stream:
                    if chunk.choices[0].delta.content:
                        content = chunk.choices[0].delta.content
                        collected_message += content
                        
                        yield f"data: {json.dumps({'type': 'chunk', 'content': content})}\n\n"
                
                # After collecting the full message, update the conversation
                conversation.append({
                    "role": "assistant",
                    "content": [{"type": "text", "text": collected_message}]
                })
                
                # Send the final message with updated session data
                yield f"data: {json.dumps({'type': 'done', 'session_data': {'question_id': session_data.get('question_id'), 'conversation': conversation}})}\n\n"
                
            except Exception as e:
                print(f"Error in stream: {str(e)}")
                yield f"data: {json.dumps({'error': str(e)})}\n\n"

        headers = {
            'Content-Type': 'text/event-stream',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            **cors_headers() 
        }
        
        return Response(
            stream_with_context(generate()),
            headers=headers
        )
        
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        response = jsonify({"error": str(e)})
        for key, value in cors_headers().items():
            response.headers[key] = value
        return response, 500

@interview_bp.route('/submit', methods=['POST'])
def submit_solution():
    try:
        data = request.get_json()
        print("Received data:", data)
        
        # Get auth0_user_id from request
        auth0_user_id = data.get('userId')
        
        # First, get the user's database ID
        user = User.query.filter_by(auth0_user_id=auth0_user_id).first()
        if not user:
            return jsonify({"error": "User not found"}), 404
            
        # Now use the user's numeric ID
        user_id = user.id  # This is the integer ID we need
        question_id = int(data.get('questionId'))  # Convert to int
        code = data.get('code', '')
        conversation = data.get('conversation', [])
        
        # Get AI analysis
        feedback = interview_service.ai_service.generate_final_analysis(
            conversation=conversation,
            final_code=code
        )
        
        # Create interview with numeric user_id
        interview = Interview(
            user_id=user_id,  # Use numeric ID
            auth0_user_id=auth0_user_id,  # Keep auth0 ID as string
            question_id=question_id,
            final_submission=code,
            language=data.get('language', 'python'),
            date=datetime.datetime.now(datetime.timezone.utc),
            score=feedback.get('qualitative_score', 'No Score'),
            transcript=json.dumps(conversation),
            feedback=feedback
        )

        db.session.add(interview)
        db.session.commit()
        interview_id = interview.id
 
        return jsonify({
            "success": True,
            "feedback": feedback,
            "interview_id": interview_id
        }), 200

    except Exception as e:
        print(f"Error in submit endpoint: {str(e)}")
        return jsonify({"error": str(e)}), 500

@interview_bp.route('/submit-solution', methods=['OPTIONS'], endpoint='submit_solution_options')
def submit_solution_options():
    return Response('', headers=cors_headers())

@interview_bp.route('/submit-solution', methods=['POST'], endpoint='submit_solution_post')
def submit_solution():
    try:
        data = request.get_json()
        code = data.get('code', '')
        session_data = data.get('session_data', {})
        conversation = session_data.get('conversation', [])
        
        # Create a prompt for solution analysis
        analysis_prompt = [
            *conversation,
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"Please analyze this solution code and provide detailed feedback:\n\n{code}"
                    }
                ]
            }
        ]
        
        def generate():
            try:
                response_stream = interview_service.ai_service.generate_response(analysis_prompt)
                collected_message = ""
                
                for chunk in response_stream:
                    if chunk.choices[0].delta.content:
                        content = chunk.choices[0].delta.content
                        collected_message += content
                        message = json.dumps({'type': 'chunk', 'content': content})
                        yield f"data: {message}\n\n"
                
                # After collecting the full message, update the conversation
                conversation.append({
                    "role": "assistant",
                    "content": [{"type": "text", "text": collected_message}]
                })
                
                # Send the final message with updated session data
                final_message = json.dumps({
                    'type': 'done',
                    'session_data': {
                        'question_id': session_data.get('question_id'),
                        'conversation': conversation
                    }
                })
                yield f"data: {final_message}\n\n"
                
            except Exception as e:
                print(f"Error in solution analysis stream: {str(e)}")
                error_message = json.dumps({'error': str(e)})
                yield f"data: {error_message}\n\n"

        headers = {
            'Content-Type': 'text/event-stream',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            **cors_headers()
        }
        
        return Response(
            stream_with_context(generate()),
            headers=headers
        )
        
    except Exception as e:
        print(f"Error in submit solution endpoint: {str(e)}")
        response = jsonify({"error": str(e)})
        for key, value in cors_headers().items():
            response.headers[key] = value
        return response, 500