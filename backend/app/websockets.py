from flask_socketio import SocketIO, emit
from app import socketio
from flask import request
import random
import pprint
from app.chatbot_manager import ChatbotManager
  
user_sessions = {}
chatbot_manager = ChatbotManager()

"""""""""
Updated conversation for WOzW8_d0xMaLkeP2AAAB: 
    [{'user': 'Hello, This is my first question', 'code': ''}, {'bot': "Thank you for your response. Let's discuss your approach."}, {'user': 'Hello, this is my second question', 'code': ''}]
Bot reply added to conversation for WOzW8_d0xMaLkeP2AAAB: 
    Thank you for your response. Let's discuss your approach.

KEY = Session ID for user   VALUE = Object containing conversation:[{code, user}, {bot}...] difficulty: string, question: string
user sessions = {

    WOzW8_d0xMaLkeP2AAAB: {
        conversation: [
            {
                'code': ''
                'user': "hello"
            },
            {
                'bot': "Thank you for your response. Let's discuss your approach."
            }
            {
                'code': 'maybe some code'
                'user': "hello again"
            },
            # continues....
        ]
        'difficuly': 'Hard', 
        'question': 'Implement a binary search tree'
    }

    ...other user session objects 

}
"""""""""

# Sample questions
questions = {
    "Easy": [
        "Reverse a string",
        # Add more easy questions
    ],
    "Medium": [
        "Find the nth Fibonacci number",
        # Add more medium questions
    ],
    "Hard": [
        "Implement a binary search tree",
        # Add more hard questions
    ],
}

pp = pprint.PrettyPrinter(width=1000, compact=False)

@socketio.on('connect') #listening for an event
def handle_connect():
    sid = request.sid
    user_sessions[sid] = {
        'conversation': []
    }  # append a client identifier (if needed )
    print("Client connected")
    emit('message', {'data': 'Welcome to the WebSocket server!'}) #emitting an event (client would have to listen for message)

@socketio.on('disconnect')
def handle_disconnect():
    sid = request.sid
    removed_session = user_sessions.pop(sid, None)
    
    if removed_session:
        print(f"Session for {sid} removed.")
    else:
        print(f"No session found for {sid}.")
    
    print("Client disconnected")


@socketio.on('select_difficulty')
def handle_select_difficulty(data):
    sid = request.sid
    difficulty = data.get('difficulty')
    
    if difficulty not in questions:
        emit('bot_message', {'message': 'Invalid difficulty selected. Please choose Easy, Medium, or Hard.'})
        return

    question = random.choice(questions[difficulty])
    
    # Create session with difficulty and question, populate the conversation field with the system prompt and initial interview question
    user_sessions[sid] = {
        'conversation': [
            {
                "role": "system", 
                "content": [{"type": "text", "text": "You are a technical interviewer at a top FAANG company. Your goal is to assess a candidate's problem-solving \
                            skills through thoughtful guidance and challenges. Avoid asking overly simplistic questions like 'What is a string?' unless the \
                            candidate explicitly struggles with a concept. Focus on guiding the candidate through the problem by asking relevant follow-up \
                            questions such as 'What approach are you considering?' or 'Can you explain the trade-offs of this solution?'. Your role is to \
                            mimic a real-life FAANG interview by encouraging critical thinking and discussion without solving the problem in any way for the candidate. \
                            Follow this process:\
                            Start with the Problem: Ask the user to solve a coding problem, such as implementing a function.\
                            Analyze the Solution: When the user submits their solution: \
                            Ask them to explain the time complexity. \
                            Ask them to identify any edge cases.\
                            Ask them to optimize their solution: ONLY IF there is room for improvement in their solution: \
                            Confirm Completion: When the solution is correct and efficient, acknowledge their success." }]
            },
                {
                "role": "assistant", 
                "content": [{"type": "text", "text": f"Hello my name is cody, I'll be your interviewer. Let's get started, {question}" }]
            }
        ]

    }
    
    # emit the bot_message for the frontend
    bot_message = f"Hello my name is cody, I'll be your interviewer. Let's get started, {question}"
    emit('bot_message', {'message': bot_message})
    print(f"Session updated for {sid}: {user_sessions[sid]}")


@socketio.on('user_message')
def handle_user_message(data):
    sid = request.sid

    user_message = data.get('message', '')
    code = data.get('code', '')
    session = user_sessions.get(sid)

    if session:

        # Save user message in convo (and code if then sent some)
        session['conversation'].append({'role': 'user', 'content': [{"type": "text", "text": user_message}]})
        if code != '':
            session['conversation'][-1]['content'].append({"type": "text", "text": code})
        
        print(f"Updated conversation for {sid}:")
        pp.pprint(session["conversation"])

        print(f"PRINTING OUT THE WHOLE OBJECT IN USER_SESSIONS FOR GIVEN SID:")
        pp.pprint(user_sessions[sid])

        # GENERATE THE BOT RESPONSE
        # We pass in the entire conversation to the api
        bot_reply = chatbot_manager.generate_response(session['conversation'])

        # Save bot reply
        session['conversation'].append({'role': 'assistant', 'content': [{'type': 'text', 'reply': bot_reply}]})
        pp.pprint(f"Bot reply added to conversation for {sid}: {bot_reply}")
        emit('bot_message', {'message': bot_reply})
    else:
        emit('bot_message', {'message': 'Please select a difficulty to start the interview.'})
        print(f"No session found for {sid}. Prompting user to select difficulty.")


@socketio.on('submit_solution')
def handle_submit_solution():
    sid = request.sid
    session = user_sessions.get(sid)

    if session:
        # Store the convo in a database

        # pass the session['conversation'] along with any other prompts to chatbot for final analysis
        # something like: final_analysis = chatbot_manager.final_analysis(session['conversation'])

        # then emit the final analysis to the frontend
        # like: emit('final_analysis', {'analysis': final_analysis})

        # for now emit the conversation as the final analysis
        emit('final_analysis', {'analysis': session['conversation']})
    else:
        emit('error', {'message': 'No session found. Please start the interview first.'})
