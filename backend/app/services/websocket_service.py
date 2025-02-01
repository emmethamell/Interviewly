from app import db
from app.models.user import User
from app.models.question import Question, DifficultyLevel
from app.models.interview import Interview
from app.services.ai_service import ChatbotManager
from app.utils.prompts import Prompts
import random
import json
import re


class WebSocketService:
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
                    "content": [{"type": "text", "text": Prompts.SYSTEM_PROMPT_CONTEXT}]
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
            return {'analysis': final_analysis, 'question': session['question'], 'interview_id': interview.id}
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