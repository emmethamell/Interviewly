from .interview_service import InterviewService
from .ai_service import ChatbotManager
from app.repositories.interview_repo import InterviewRepository

# Create instances
interview_repo = InterviewRepository()
ai_service = ChatbotManager()
interview_service = InterviewService(
    interview_repo=interview_repo,
    ai_service=ai_service
)

__all__ = ['interview_service']