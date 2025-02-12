from app.repositories.interview_repo import InterviewRepository

from app.services.ai_service import ChatbotManager
from typing import Dict, List
from app.models.interview import Interview
from app.models.question import Question, DifficultyLevel
import random

class InterviewService:
    def __init__(self, interview_repo: InterviewRepository, ai_service: ChatbotManager):
        self.interview_repo = interview_repo
        self.ai_service = ai_service

    def get_user_interviews(self, auth0_user_id: str, page: int, limit: int):
        interviews, total = self.interview_repo.get_user_interviews(
            auth0_user_id=auth0_user_id,
            page=page,
            limit=limit
        )
        
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
        
        return interviews_data, total

    def get_interview_details(self, interview_id: int) -> Dict:
        interview = self.interview_repo.get_by_id(interview_id)
        return {
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
        
    def calculate_interview_stats(self, user_id: str) -> Dict:
        """
        Calculate interview statistics for a user.
        returns: {success_rate, easy_successes, medium_successes, hard_successes}
        """
        return self.interview_repo.get_interview_stats(user_id)
        
    def process_user_message(self, session_id: str, user_message: str, 
                           code: str, session_data: Dict) -> str:
        if not session_data:
            return 'Please select a difficulty to start the interview.'
            
        session_data['conversation'].append({
            'role': 'user', 
            'content': [{"type": "text", "text": user_message}]
        })
        
        if code:
            session_data['conversation'][-1]['content'].append(
                {"type": "text", "text": code}
            )
            
        bot_reply = self.ai_service.generate_response(session_data['conversation'])
        session_data['conversation'].append({
            'role': 'assistant', 
            'content': [{'type': 'text', 'text': bot_reply}]
        })
        
        return bot_reply

    def get_random_question(self, difficulty: str):
        try:
            difficulty_enum = DifficultyLevel[difficulty.upper()]
        except KeyError:
            return "Invalid difficulty. Please choose Easy, Medium, or Hard."

        questions = Question.query.filter_by(difficulty=difficulty_enum).all()
        if not questions:
            return "No questions available for the selected difficulty."

        return random.choice(questions)

    def submit_solution(self, user_id: str, question_id: int, code: str, 
                       language: str, conversation: List) -> Dict:
        try:
            final_analysis = self.ai_service.generate_final_analysis(conversation, code)
            
            # Default score to 0 for now - you can implement scoring logic later
            score = 0
            
            interview = self.interview_repo.create_interview(
                user_id=user_id,
                auth0_user_id=user_id,
                question_id=question_id,
                transcript=self._clean_conversation(conversation),
                final_submission=code,
                feedback=final_analysis,
                language=language,
                score=score  # Add the required score parameter
            )
            
            return {
                'analysis': final_analysis,
                'interview_id': interview.id
            }
            
        except Exception as e:
            raise Exception(f'Failed to save interview: {str(e)}')

    def _clean_conversation(self, conversation: List) -> str:
        new_convo = ""
        for m in conversation:
            if m["role"] in ["assistant", "user"]:
                for content in m["content"]:
                    new_convo += f"{'Interviewer' if m['role'] == 'assistant' else 'Candidate'}: {content['text']}\n"
        return new_convo