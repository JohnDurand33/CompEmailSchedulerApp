from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_migrate import Migrate
from config import Config
from models import db
from routes import auth_bp, recipient_bp
from utils import mail


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    mail.init_app(app)
    jwt = JWTManager(app)

    migrate = Migrate(app)

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(recipient_bp, url_prefix='/api')

    with app.app_context():
        db.create_all()

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
