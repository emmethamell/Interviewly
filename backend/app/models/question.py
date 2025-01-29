from app import db
import enum
from sqlalchemy import Integer, String, Text, Enum

class DifficultyLevel(enum.Enum):
    """Enumeration for question difficulty levels."""
    EASY = "Easy"
    MEDIUM = "Medium"
    HARD = "Hard"

# Association table for many-to-many relationship between questions and tags
question_tag_association = db.Table(
    'question_tag',
    db.Column('question_id', Integer, db.ForeignKey('questions.id'), primary_key=True),
    db.Column('tag_id', Integer, db.ForeignKey('tags.id'), primary_key=True)
)

class Question(db.Model):
    """
    Question model representing coding interview questions.
    
    Attributes:
        id (Integer): Primary key
        content (Text): The actual question text/description
        difficulty (DifficultyLevel): Enum indicating question difficulty
        name (String): Title/name of the question
    
    Relationships:
        tags: Many-to-many relationship with Tag model
        interviews: One-to-many relationship with Interview model
    """
    
    __tablename__ = 'questions'
    id = db.Column(Integer, primary_key=True)
    content = db.Column(Text, nullable=False)
    difficulty = db.Column(Enum(DifficultyLevel), nullable=False)
    name = db.Column(String(200), nullable=False)
    tags = db.relationship("Tag", secondary=question_tag_association, back_populates="questions")

    def __repr__(self):
        return f"<Question id={self.id}, content={self.content}, difficulty={self.difficulty}, name={self.name}>" 