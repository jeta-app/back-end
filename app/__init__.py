# app/__init__.py
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO, emit
from flask_migrate import Migrate
from flask_cors import CORS

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()
socketio = SocketIO(cors_allowed_origins="*")
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    socketio.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    from app.controllers.admin_controller import admin_bp
    from app.controllers.user_controller import user_bp
    from app.controllers.angkutan_controller import angkutan_bp
    from app.controllers.location_driver_controller import location_bp
    from app.controllers.location_passenger_controller import location_passenger_bp

    app.register_blueprint(admin_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(location_bp)
    app.register_blueprint(location_passenger_bp)
    app.register_blueprint(angkutan_bp)

    return app

# def jwt_required_socket(f):
#     def wrapper(*args, **kwargs):
#         try:
#             verify_jwt_in_request()
#         except Exception as e:
#             emit('error', {'message': str(e)})
#             return False
#         return f(*args, **kwargs)
#     return wrapper
