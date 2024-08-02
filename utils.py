from flask_mail import Message
from flask import current_app
import os


def send_email(subject, recipient, body, attachment_path=None):
    mail = current_app.extensions.get('mail')
    if not mail:
        raise RuntimeError('Mail extension not initialized')
    msg = Message(subject, recipients=[recipient], body=body, sender="john.durand1@gmail.com")

    if attachment_path and os.path.exists(attachment_path):
        with current_app.open_resource(attachment_path) as fp:
            msg.attach(os.path.basename(attachment_path),
                       "application/pdf", fp.read())

    mail.send(msg)
