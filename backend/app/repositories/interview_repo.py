from app.models.interview import Interview
from app.models.user import User
from app import db
from typing import Dict, Tuple
from sqlalchemy import func, case
from app.models.question import Question, DifficultyLevel

class InterviewRepository:
    def get_by_id(self, interview_id: int) -> Interview:
        return Interview.query.get_or_404(interview_id)
    
    def get_user_interviews(self, auth0_user_id: str, page: int, limit: int) -> Tuple[list, int]:
        offset = (page - 1) * limit
        total = Interview.query.filter_by(auth0_user_id=auth0_user_id).count()
        interviews = Interview.query.filter_by(auth0_user_id=auth0_user_id)\
            .offset(offset).limit(limit).all()
        return interviews, total

    def create_interview(self, user_id: int, auth0_user_id: str, question_id: int,
                        transcript: str, score: str, final_submission: str,
                        feedback: dict, language: str) -> Interview:
        interview = Interview(
            user_id=user_id,
            auth0_user_id=auth0_user_id,
            question_id=question_id,
            transcript=transcript,
            score=score,
            final_submission=final_submission,
            feedback=feedback,
            language=language
        )
        db.session.add(interview)
        db.session.commit()
        return interview
    
    def get_interview_stats(self, auth0_user_id: str) -> Dict:
        """Get interview statistics using joins instead of loading full objects"""
        stats = db.session.query(
            func.count(Interview.id).label('total_interviews'),
            func.count(case(
                (Interview.score.in_(["Hire", "Strong Hire"]), 1)
            )).label('successful_interviews'),
            func.count(case(
                (
                    (Question.difficulty == DifficultyLevel.EASY) & 
                    Interview.score.in_(["Hire", "Strong Hire"]),
                    1
                )
            )).label('easy_successes'),
            func.count(case(
                (
                    (Question.difficulty == DifficultyLevel.MEDIUM) & 
                    Interview.score.in_(["Hire", "Strong Hire"]),
                    1
                )
            )).label('medium_successes'),
            func.count(case(
                (
                    (Question.difficulty == DifficultyLevel.HARD) & 
                    Interview.score.in_(["Hire", "Strong Hire"]),
                    1
                )
            )).label('hard_successes')
        ).join(
            Question,
            Interview.question_id == Question.id
        ).filter(
            Interview.auth0_user_id == auth0_user_id
        ).first()

        return {
            'success_rate': stats.successful_interviews / stats.total_interviews,
            'easy_successes': stats.easy_successes,
            'medium_successes': stats.medium_successes,
            'hard_successes': stats.hard_successes
        }