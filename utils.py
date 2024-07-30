from flask_mail import Mail, Message
from flask import current_app

mail = Mail()


def send_email(subject, recipient, body):
    msg = Message(subject, recipients=[recipient])
    msg.body = body
    mail.send(msg)
