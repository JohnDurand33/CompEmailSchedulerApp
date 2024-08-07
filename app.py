from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from models import db
import routes
import config


def create_app():
    app = Flask(__name__)
    app.config.from_object(config.Config)

    db.init_app(app)
    Migrate(app, db)
    JWTManager(app)
    CORS(app)

    app.register_blueprint(routes.bp)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
