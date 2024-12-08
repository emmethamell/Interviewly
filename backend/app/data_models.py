from app import db
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Enum, Float
from sqlalchemy.orm import relationship
import enum


class DifficultyLevel(enum.Enum):
    EASY = "Easy"
    MEDIUM = "Medium"
    HARD = "Hard"

question_tag_association = db.Table(
    'question_tag',
    db.Column('question_id', Integer, db.ForeignKey('questions.id'), primary_key=True),
    db.Column('tag_id', Integer, db.ForeignKey('tags.id'), primary_key=True)
)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(Integer, primary_key=True)
    auth0_user_id = db.Column(String(255), unique=True, nullable=False)

    name = db.Column(String(100))
    email = db.Column(db.String(255), unique=True, nullable=False)
    interviews = db.relationship("Interview", back_populates="user")

class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(Integer, primary_key=True)
    content = db.Column(Text, nullable=False)
    difficulty = db.Column(Enum(DifficultyLevel), nullable=False)
    name = db.Column(String(200), nullable=False)
    tags = db.relationship("Tag", secondary=question_tag_association, back_populates="questions")

    def __repr__(self):
        return f"<Question id={self.id}, content={self.content}, difficulty={self.difficulty}, name={self.name}>"

class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(50), unique=True, nullable=False)
    questions = db.relationship("Question", secondary=question_tag_association, back_populates="tags")

class Interview(db.Model):
    __tablename__ = 'interviews'
    id = db.Column(Integer, primary_key=True)
    user_id = db.Column(Integer, db.ForeignKey('users.id'), nullable=False)
    auth0_user_id = db.Column(String(255), nullable=False)
    question_id = db.Column(Integer, db.ForeignKey('questions.id'), nullable=False)
    transcript = db.Column(Text, nullable=True)
    score = db.Column(Text, nullable=False)
    user = db.relationship("User", back_populates="interviews")
    question = db.relationship("Question")