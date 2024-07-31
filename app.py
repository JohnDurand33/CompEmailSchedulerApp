from flask import Flask, jsonify
from utils import send_email
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from config import Config
from models import db
from routes import auth_bp, recipient_bp
from flask_mail import Mail


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize Flask extensions
    db.init_app(app)
    jwt = JWTManager(app)
    migrate = Migrate(app, db)
    mail = Mail(app)

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(recipient_bp, url_prefix='/api')

    @app.route('/send-test-email')
    def send_test_email():
        try:
            send_email('You Are THE BEST!!!!!', 'john.durand1@gmail.com','You are amazing, and I love you for everything you do every day.  Thanks for being my Best Friend-    John')
            return jsonify({"msg": "Email sent successfully"}), 200
        except Exception as e:
            return jsonify({"msg": str(e)}), 500

    with app.app_context():
        db.create_all()

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
