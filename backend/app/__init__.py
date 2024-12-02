import os
from flask import Flask
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy


socketio = SocketIO(async_mode='eventlet')


def create_app():
    flask_app = Flask(__name__)  
    flask_app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')  # PostgreSQL database URL
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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

    return flask_app