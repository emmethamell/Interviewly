from app.repositories.interview_repo import InterviewRepository

from app.services.ai_service import ChatbotManager
from typing import Dict, List
from app.models.interview import Interview

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