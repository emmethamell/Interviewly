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

    CORS(flask_app)
    flask_app.config['CORS_HEADERS'] = 'Content-Type'

    from app.data_models import User, Question, Tag, Interview, question_tag_association

    # Register routes
    from app.routes import bp
    from app.auth import auth_bp
    flask_app.register_blueprint(bp, url_prefix='/api')
    flask_app.register_blueprint(auth_bp, url_prefix='/auth')

    # Initialize SocketIO
    socketio.init_app(
        flask_app,
        cors_allowed_origins="*",  
    )

    import app.websockets

    with flask_app.app_context():
        db.create_all()
        
    return flask_app