from app import db
from .question import question_tag_association

class Tag(db.Model):
    """
    Tag model for categorizing questions by topics.
    
    Attributes:
        id (Integer): Primary key
        name (String): Unique name of the tag (e.g., "Arrays", "Dynamic Programming")
    
    Relationships:
        questions: Many-to-many relationship with Question model
    """
    
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    questions = db.relationship("Question", secondary=question_tag_association, back_populates="tags") 