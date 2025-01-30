from app import db
from app.models.user import User
from app.models.question import Question, DifficultyLevel
from app.models.interview import Interview
from app.services.ai_service import ChatbotManager
import random
import json
import re

class WebSocketService:
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
        
    def __init__(self):
        self.chatbot_manager = ChatbotManager()
        self.user_sessions = {}

    def create_session(self, sid):
        self.user_sessions[sid] = {
            'conversation': []
        }
        return "Welcome to the WebSocket server!"

    def remove_session(self, sid):
        return self.user_sessions.pop(sid, None)

    def handle_difficulty_selection(self, sid, difficulty):
        question = self._get_question(difficulty)
        if isinstance(question, str):  
            return {'error': question}
            
        session_data = {
            'conversation': [
                {
                    "role": "system", 
                    "content": [{"type": "text", "text": self.SYSTEM_PROMPT_CONTEXT}]
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
        
        self.user_sessions[sid] = session_data
        return f"Hello my name is Cody, I'll be your interviewer. Let's get started with your question:\n\n {question.content}"

    def handle_user_message(self, sid, user_message, code=''):
        session = self.user_sessions.get(sid)
        if not session:
            return 'Please select a difficulty to start the interview.'

        session['conversation'].append({'role': 'user', 'content': [{"type": "text", "text": user_message}]})
        if code:
            session['conversation'][-1]['content'].append({"type": "text", "text": code})
            
        bot_reply = self.chatbot_manager.generate_response(session['conversation'])
        session['conversation'].append({'role': 'assistant', 'content': [{'type': 'text', 'text': bot_reply}]})
        return bot_reply

    def handle_solution_submission(self, sid, user_id, code, language):
        session = self.user_sessions.get(sid)
        if not session:
            return {'error': 'No session found. Please start the interview first.'}

        try:
            final_analysis = self._process_final_analysis(session, code)
            interview = self._save_interview(session, user_id, code, language, final_analysis)
            return {'analysis': final_analysis, 'question': session['question']}
        except Exception as e:
            db.session.rollback()
            return {'error': f'Failed to save interview: {str(e)}'}

    def _get_question(self, difficulty):
        try:
            difficulty_enum = DifficultyLevel[difficulty.upper()]
        except KeyError:
            return "Invalid difficulty. Please choose Easy, Medium, or Hard."

        questions = Question.query.filter_by(difficulty=difficulty_enum).all()
        if not questions:
            return "No questions available for the selected difficulty."

        return random.choice(questions)

    def _process_final_analysis(self, session, code):
        final_analysis = self.chatbot_manager.generate_final_analysis(session['conversation'], code)
        final_analysis = re.sub(r'```json|```', '', final_analysis).strip()
        return json.loads(final_analysis)

    def _save_interview(self, session, user_id, code, language, final_analysis):
        user = User.query.filter_by(auth0_user_id=user_id).first()
        if not user:
            raise ValueError("Invalid user")

        interview = Interview(
            user_id=user.id,
            auth0_user_id=user_id,
            question_id=session['question']['id'],
            transcript=self._clean_conversation(session['conversation']),
            score=final_analysis.get('qualitative_score', 'No Score'),
            final_submission=code,
            feedback=final_analysis,
            language=language
        )
        db.session.add(interview)
        db.session.commit()
        return interview

    def _clean_conversation(self, conversation):
        new_convo = ""
        for m in conversation:
            if m["role"] in ["assistant", "user"]:
                for content in m["content"]:
                    new_convo += f"{'Interviewer' if m['role'] == 'assistant' else 'Candidate'}: {content['text']}\n"
        return new_convo