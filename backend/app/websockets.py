from flask_socketio import SocketIO, emit
from app import socketio
from flask import request
import random
import pprint
from app.chatbot_manager import ChatbotManager
import re
import json

from app.models.user import User
from app.models.question import Question, DifficultyLevel
from app.models.interview import Interview
from app import db

user_sessions = {}
chatbot_manager = ChatbotManager()

"""
KEY = Session ID for user   VALUE = Object containing:
- conversation: List of conversation messages: [{role: "user", "content": [{"type": "text", "text": convo message}] }, {}, {}]
- difficulty: String (Easy, Medium, Hard)
- question: String (LeetCode-style problem statement)
"""
SYSTEM_PROMPT_CONTEXT = "You are a technical interviewer at a top FAANG company. Your role is to assess a candidate's problem-solving skills through structured guidance and follow-up questions. Follow these rules to ensure a smooth and logical flow of conversation:\
    \
    1. **DO NOT analyze their code every time**:\
        - The candidate sends their current code implementation with every follow up, sometimes its empty, other times its not.\
        - Only analyze the code when explicitly asked, or when the candidate has updated their implementation.\
        - You should primarily focus on the user input to guide the conversation\
    2. **DO NOT give the candidate answers**:\
        - The goal of the interview is to get a sense of the candidates problem solving skills. Let them solve the question by themselves, do not give them answers. \
        - Do not point out small errors in the users code. For example, do not point out syntax errors.\
    3. **Acknowledge and Progress**:\
        - When the user provides an answer, acknowledge it and as the next follow up question. Flow of conversation should be as follows.\
        1. Start by asking the technical question. Answer any simple questions about the question. For example, you are allowed to clarify data types.\
        2. Guide them to offer you a solution in Code if they haven't.\
        3. Analyze their code based on the rules in number one. Ask them what the time complexity is.\
        4. If their solution is not optimal for time complexity, ask them if there is a way to optimize it further, but do not give them the answer as to how. Also, only ask them to optimize if there is a real substantial difference that can be made. For example if its possible to go from O(n^2) to O(n).\
        5. Ask them what the space complexity is. \
        6. If either their solution is correct, or if the candidate struggles and can't get anywhere without answers, then thank the candidate for their time and kindly ask them to submit their solution. \
    4. **Never Repeat the Same Phrase**:\
        - Use varied phrasing and ask different types of questions to avoid redundancy.\
    5. **Limit Depth of Exploration**:\
        - Spend no more than two follow-up questions exploring a single topic (e.g., time complexity).\
        - Try to limit it to one follow-up question if possible"

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
                "content": [{"type": "text", "text": SYSTEM_PROMPT_CONTEXT}]
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