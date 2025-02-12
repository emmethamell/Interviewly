from app.models.interview import Interview
from app.models.user import User
from app import db
from typing import Dict, Tuple
from sqlalchemy import text

class InterviewRepository:
    def get_by_id(self, interview_id: int) -> Interview:
        return Interview.query.get_or_404(interview_id)
    
    def get_user_interviews(self, auth0_user_id: str, page: int, limit: int) -> Tuple[list, int]:
        offset = (page - 1) * limit
        total = Interview.query.filter_by(auth0_user_id=auth0_user_id).count()
        interviews = Interview.query.filter_by(auth0_user_id=auth0_user_id)\
            .order_by(Interview.date.desc()).offset(offset).limit(limit).all()
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
        total_interviews_sql = text("""
        SELECT COUNT(*)
        FROM interviews
        WHERE auth0_user_id = :auth0_user_id
        """)
        
        total_successful_interviews_sql = text("""
        SELECT COUNT(*)
        FROM interviews
        WHERE auth0_user_id = :auth0_user_id 
        AND (score = 'Hire' OR score = 'Strong Hire')
        """)
        
        total_easy_successes_sql = text("""
        SELECT COUNT(*)
        FROM interviews i
        JOIN questions q ON i.question_id = q.id
        WHERE i.auth0_user_id = :auth0_user_id 
        AND (i.score = 'Hire' OR i.score = 'Strong Hire')
        AND q.difficulty = 'EASY'
        """)
        
        total_medium_successes_sql = text("""
        SELECT COUNT(*)
        FROM interviews i
        JOIN questions q ON i.question_id = q.id
        WHERE i.auth0_user_id = :auth0_user_id 
        AND (i.score = 'Hire' OR i.score = 'Strong Hire')
        AND q.difficulty = 'MEDIUM'
        """)
        
        total_hard_successes_sql = text("""
        SELECT COUNT(*)
        FROM interviews i
        JOIN questions q ON i.question_id = q.id
        WHERE i.auth0_user_id = :auth0_user_id 
        AND (i.score = 'Hire' OR i.score = 'Strong Hire')
        AND q.difficulty = 'HARD'
        """)
        
        total_interviews = db.session.execute(total_interviews_sql, {"auth0_user_id": auth0_user_id}).scalar() or 0
        
        total_successful_interviews = db.session.execute(total_successful_interviews_sql, {"auth0_user_id": auth0_user_id}).scalar() or 0
        total_easy_successes = db.session.execute(total_easy_successes_sql, {"auth0_user_id": auth0_user_id}).scalar() or 0
        total_medium_successes = db.session.execute(total_medium_successes_sql, {"auth0_user_id": auth0_user_id}).scalar() or 0
        total_hard_successes = db.session.execute(total_hard_successes_sql, {'auth0_user_id': auth0_user_id}).scalar() or 0
        
        success_rate = (total_successful_interviews / total_interviews) if total_interviews > 0 else 0
        
        return {
            'success_rate': success_rate,
            'easy_successes': total_easy_successes,
            'medium_successes': total_medium_successes,
            'hard_successes': total_hard_successes
        }