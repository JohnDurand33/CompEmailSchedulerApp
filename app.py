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
            attachment_path = os.path.join(app.root_path, 'path_to_your_miro_workflow_file.pdf')
            send_email('OMG I LOVE YOUUUUUUUUUUUUUUUU', 'john.durand1@gmail.com',
                       "Today I built about half of the application logic.  I'm mapping it al out so doing the front and back end at the same time.  Learning sooooo much.  If I could attach it here it would be awesome-   John", attachment_path=attachment_path)
            return jsonify({"msg": "Email sent successfully"}), 200
        except Exception as e:
            return jsonify({"msg": str(e)}), 500

    with app.app_context():
        db.create_all()

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
