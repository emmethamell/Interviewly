from flask_socketio import SocketIO, emit
from app import socketio
from flask import request
import random
import pprint
from app.chatbot_manager import ChatbotManager
import re
import json
from app.data_models import db, Question, DifficultyLevel, Interview, User
from app.session_manager import SessionManager

user_sessions = {}
chatbot_manager = ChatbotManager()

"""
KEY = Session ID for user   VALUE = Object containing:
- conversation: List of conversation messages: [{role: "user", "content": [{"type": "text", "text": convo message}] }, {}, {}]
- difficulty: String (Easy, Medium, Hard)
- question: String (LeetCode-style problem statement)
"""

pp = pprint.PrettyPrinter(width=1000, compact=False)

@socketio.on('connect')
def handle_connect():
    sid = request.sid
    user_sessions[sid] = {
        'conversation': []
    } 
    print("Client connected")
    emit('message', {'data': 'Welcome to the WebSocket server!'}) 

@socketio.on('disconnect')
def handle_disconnect():
    sid = request.sid
    removed_session = user_sessions.pop(sid, None)
    if removed_session:
        print(f"Session for {sid} removed.")
    else:
        print(f"No session found for {sid}.")
    print("Client disconnected")

# User selects difficulty, select question and begin by emitting question as bot_message
@socketio.on('select_difficulty')
def handle_select_difficulty(data):
    sid = request.sid
    difficulty = data.get('difficulty')
    question = getQuestion(difficulty)
    if "Invalid difficulty" in question.content or "No questions available" in question.content:
        emit('bot_message', {'message': question.content})
        return
    
    user_sessions[sid] = {
        'conversation': [
            {
                "role": "system", 
                "content": [{"type": "text", "text": SessionManager.SYSTEM_PROMPT_CONTEXT}]
            },
                {
                "role": "assistant", 
                "content": [{"type": "text", "text": f"Hello my name is Cody, I'll be your interviewer. Let's get started with your question:\n\n {question.content}" }]
            }
        ],
        'question': {
            'id': question.id,
            'content': question.content,
            'difficulty': question.difficulty.value,
            'name': question.name,
        }

    }
    
    bot_message = f"Hello my name is Cody, I'll be your interviewer. Let's get started with your question:\n\n {question.content}"
    emit('bot_message', {'first_message': True, 'message': bot_message })

# Store user message in sessions object, generate bot response, emit bot response
@socketio.on('user_message')
def handle_user_message(data):
    sid = request.sid
    user_message = data.get('message', '')
    code = data.get('code', '')
    session = user_sessions.get(sid)

    if session:
        session['conversation'].append({'role': 'user', 'content': [{"type": "text", "text": user_message}]})
        if code != '':
            session['conversation'][-1]['content'].append({"type": "text", "text": code})
        bot_reply = chatbot_manager.generate_response(session['conversation'])
        session['conversation'].append({'role': 'assistant', 'content': [{'type': 'text', 'text': bot_reply}]})
        emit('bot_message', {'first_message': False, 'message': bot_reply})
    else:
        emit('bot_message', {'message': 'Please select a difficulty to start the interview.'})

# Generate final analysis of interview, store interview in db, emit final analysis
@socketio.on('submit_solution')
def handle_submit_solution(data):
    sid = request.sid
    session = user_sessions.get(sid)
    user_id = data.get('userId')
    code = data.get("code")
    language = data.get("language")
    if session:
        final_analysis = chatbot_manager.generate_final_analysis(session['conversation'], code)
        question = session['question']
        final_analysis = re.sub(r'```json|```', '', final_analysis).strip()
        try:
            final_analysis = json.loads(final_analysis)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format after cleaning.")
        try:
            user = User.query.filter_by(auth0_user_id=user_id).first()
            if not user:
                emit('error', {'message': 'Invalid user'})
                return
            interview = Interview(
                user_id=user.id,
                auth0_user_id=user_id,
                question_id=question['id'],
                transcript=cleanConversation(session['conversation']),
                score=final_analysis.get('qualitative_score', 'No Score'),
                final_submission=code,
                feedback=final_analysis,
                language=language
            )
            db.session.add(interview)
            db.session.commit()
            emit('final_analysis', {'analysis': final_analysis, 'question': question})
        except Exception as e:
            db.session.rollback()
            emit('error', {'message': 'Failed to save interview', 'error': str(e)})
            print("FAILURE", str(e))
    else:
        emit('error', {'message': 'No session found. Please start the interview first.'})


# TODO: Select single question from database
def getQuestion(difficulty):
    """Fetch random question of given difficulty"""
    try:
        difficulty_enum = DifficultyLevel[difficulty.upper()]
    except KeyError:
        return {"error": "Invalid difficulty. Please choose Easy, Medium, or Hard."}

    questions = Question.query.filter_by(difficulty=difficulty_enum).all()

    if not questions:
        return "No questions available for the selected difficulty."

    random_question = random.choice(questions)

    return random_question 

def cleanConversation(conversation):
        new_convo = ""
        for m in conversation:
            if m["role"] == "assistant" or m["role"] == "user":
                for content in m["content"]:
                    new_convo += f"{'Interviewer' if m['role'] == 'assistant' else 'Candidate'}: {content['text']}\n"
        return new_convo