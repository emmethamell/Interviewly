from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_cors import CORS
import os

load_dotenv()
db = SQLAlchemy()

def create_app():
    flask_app = Flask(__name__)  
    flask_app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(flask_app)
    
    allowed_origins = os.getenv('ALLOWED_ORIGINS').split(',')
    CORS(flask_app, origins=allowed_origins)

    # Import models
    from app.models.user import User
    from app.models.question import Question
    from app.models.tag import Tag
    from app.models.interview import Interview
    from app.models.question import question_tag_association

    # Register routes
    from app.routes.interview import interview_bp
    from app.routes.auth import auth_bp
    from app.routes.health import health_bp
    flask_app.register_blueprint(interview_bp, url_prefix='/interview')
    flask_app.register_blueprint(auth_bp, url_prefix='/auth')
    flask_app.register_blueprint(health_bp, url_prefix='/health')

    with flask_app.app_context():
        db.create_all()
        
    return flask_app