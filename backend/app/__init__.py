import os
from flask import Flask
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()

socketio = SocketIO(async_mode='eventlet')
db = SQLAlchemy()

def create_app():
    flask_app = Flask(__name__)  
    flask_app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL') 
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    flask_app.config['SQLALCHEMY_ECHO'] = True

    # Initialize sqlalchemy
    db.init_app(flask_app)
    allowed_origins = os.getenv('ALLOWED_ORIGINS', 'http://localhost:5173').split(',')
    
    CORS(flask_app, resources={
        r"/*": {
            "origins": allowed_origins
        }
    })
    
    flask_app.config['CORS_HEADERS'] = 'Content-Type'
    

    # Import models in correct order
    from app.models.user import User
    from app.models.question import Question
    from app.models.tag import Tag
    from app.models.interview import Interview  # Import this last since it depends on other models
    from app.models.question import question_tag_association

    # Register routes
    from app.routes.interview import interview_bp
    from app.routes.auth import auth_bp
    from app.routes.health import health_bp
    flask_app.register_blueprint(interview_bp, url_prefix='/interview')
    flask_app.register_blueprint(auth_bp, url_prefix='/auth')
    flask_app.register_blueprint(health_bp, url_prefix='/health')
    
    # Initialize SocketIO
    socketio.init_app(
        flask_app,
        cors_allowed_origins=allowed_origins,  
    )

    import app.websockets.handlers

    with flask_app.app_context():
        db.create_all()
        
    return flask_app