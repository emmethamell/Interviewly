from app import db

class User(db.Model):
    """
    User model representing application users authenticated through Auth0.
    
    Attributes:
        id (Integer): Primary key
        auth0_user_id (String): Unique identifier from Auth0
        name (String): User's display name
        email (String): User's email address (unique)
    
    Relationships:
        interviews: Automatically created through backref in Interview model
    """
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    auth0_user_id = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(100))
    email = db.Column(db.String(255), unique=True, nullable=False)
    
    def __repr__(self):
        return f'<User {self.email}>' 