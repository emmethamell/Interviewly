from app import db

class LeetCodeQuestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    difficulty = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    solution = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<LeetCodeQuestion {self.title}>'