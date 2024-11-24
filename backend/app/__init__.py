from flask import Flask
from flask_socketio import SocketIO
import os

socketio = SocketIO()

def create_app():
    flask_app = Flask(__name__)  
    
    flask_app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


    # Register routes
    from app.routes import bp
    flask_app.register_blueprint(bp)


    # Initialize SocketIO
    socketio.init_app(flask_app)

    import app.websockets

    return flask_app