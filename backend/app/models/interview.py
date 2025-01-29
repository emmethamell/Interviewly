from datetime import datetime, timezone
from app import db

class Interview(db.Model):
    """
    Interview model representing coding interview sessions.
    
    Attributes:
        id (Integer): Primary key
        user_id (Integer): Foreign key to User model
        auth0_user_id (String): Auth0 identifier for the user
        question_id (Integer): Foreign key to Question model
        transcript (Text): Complete interview conversation
        feedback (JSON): Structured feedback and ratings
        final_submission (Text): Final code submission
        score (Text): Interview score/rating
        language (Text): Programming language used
        date (DateTime): UTC timestamp of the interview
    
    Relationships:
        user: Many-to-one relationship with User model
        question: Many-to-one relationship with Question model
    """
    
    __tablename__ = 'interviews'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    auth0_user_id = db.Column(db.String(255), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    transcript = db.Column(db.Text, nullable=True)
    feedback = db.Column(db.JSON, nullable=False)
    final_submission = db.Column(db.Text, nullable=False)
    score = db.Column(db.Text, nullable=False)
    language = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    # Define both relationships here
    user = db.relationship("User", backref=db.backref("interviews", lazy=True))
    question = db.relationship("Question")