import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # Flask Configuration
    FLASK_APP = os.environ.get('FLASK_APP')
    FLASK_DEBUG = os.environ.get('FLASK_DEBUG')
    SECRET_KEY = os.environ.get('SECRET_KEY')

    # SQLAlchemy / Supabase Configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get(
        'SQLALCHEMY_TRACK_MODIFICATIONS') == 'True'

    # AWS SES Configuration
    AWS_REGION = os.environ.get('AWS_REGION')
    SES_SMTP_USERNAME = os.environ.get('SES_SMTP_USERNAME')
    SES_SMTP_PASSWORD = os.environ.get('SES_SMTP_PASSWORD')
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'True').lower() in [
        'true', '1', 't']
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')

    # JWT Configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
