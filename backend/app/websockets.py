from flask_socketio import SocketIO, emit
from app import socketio
from flask import request
import random
import pprint
from app.chatbot_manager import ChatbotManager
import re
import json
  
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
        "Write a function that takes in a string and reverses it",

    ],
    "Medium": [
        "Write a function that finds the n'th fibonacci number",
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
                "content": [{"type": "text", "text": "You are a technical interviewer at a top FAANG company. Your role is to assess a candidate's problem-solving skills through structured guidance and follow-up questions. Follow these rules to ensure a smooth and logical flow of conversation:\
              \
              1. **Acknowledge and Progress**:\
                 - When the candidate provides an answer, acknowledge it once and avoid repeating the same question.\
                 - Progress the conversation by asking the next logical follow-up question based on their response. For example:\
                   - If they give a wrong time complexity, ask, 'What specific steps in your approach lead you to this complexity?' or 'Is there a way to verify this complexity?'\
                   - If they struggle, offer gentle guidance: 'Would you like me to explain how recursion affects the time complexity here?'\
                 \
              2. **Avoid Repetition**:\
                 - Track the user's responses within the conversation and avoid asking the same question multiple times unless the user provides conflicting answers.\
                 - If the user repeats an incorrect answer, guide them toward self-correction:\
                   'You've mentioned O(n^2). Do you think the number of calls might grow exponentially rather than quadratically?'\
                 \
              3. **Dynamic Follow-Ups**:\
                 - Tailor your response to the user's last statement. Do not reiterate the same question verbatim.\
                 - Use varied prompts to guide their thought process: 'Can you clarify what you mean by 'two calls each time'? How does this affect the overall growth of the recursion tree?'\
                 \
              4. **Error Identification**:\
                 - If the user provides an incorrect answer and doesn't recognize their mistake, guide them by pointing out specific parts of their logic:\
                   'When you mention 'two calls each time,' could that suggest an exponential rather than a quadratic pattern?'\
                 \
              5. **Never Repeat the Same Phrase**:\
                 - Use varied phrasing and ask different types of questions to avoid redundancy.\
              \
              6. **Facilitate Learning**:\
                 - Encourage critical thinking and self-correction instead of providing direct answers, unless explicitly asked.\
                 2. **Limit Depth of Exploration**:\
                 - Spend no more than two follow-up questions exploring a single topic (e.g., time complexity).\
                 - If the candidate shows understanding or provides a reasonable explanation after two follow-ups, move to the next topic.\
                 - If the candidate struggles significantly, gently offer a high-level explanation and transition to the next area of focus."}]
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
        session['conversation'].append({'role': 'assistant', 'content': [{'type': 'text', 'text': bot_reply}]})
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
        # TODO: Store the convo in a database

        # pass the session['conversation'] along with any other prompts to chatbot for final analysis
        # something like: final_analysis = chatbot_manager.final_analysis(session['conversation'])
        final_analysis = chatbot_manager.generate_final_analysis(session['conversation'])

        # gpt returns markdown formatting of json, so remove before sending to frontend
        final_analysis = re.sub(r'```json|```', '', final_analysis).strip()
    
        # make sure that the json is valid
        try:
            final_analysis = json.loads(final_analysis)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format after cleaning.")
        print("FINAL ANALYSIS PARSED JSON: " + str(final_analysis))

        # emit final analysis for frontend
        emit('final_analysis', {'analysis': final_analysis})
    else:
        emit('error', {'message': 'No session found. Please start the interview first.'})
