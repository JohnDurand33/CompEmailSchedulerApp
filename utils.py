from flask_mail import Message
from flask import current_app


def send_email(subject, recipient, body):
    mail = current_app.extensions.get('mail')
    if not mail:
        raise RuntimeError('Mail extension not initialized')
    msg = Message(subject, recipients=[recipient], body=body, sender="john.durand1@gmail.com")
    mail.send(msg)
