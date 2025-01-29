from app.models.interview import Interview
from app.models.user import User
from app import db

class InterviewRepository:
    def get_by_id(self, interview_id: int) -> Interview:
        return Interview.query.get_or_404(interview_id)
    
    def get_user_interviews(self, auth0_user_id: str, page: int, limit: int):
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