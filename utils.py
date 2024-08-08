import boto3
import os
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from flask import jsonify
from config import Config


def send_email(to_email, subject, body, from_email=None):
    ses_client = boto3.client('ses', region_name=Config.AWS_REGION)
    from_email = from_email or Config.MAIL_DEFAULT_SENDER

    try:
        response = ses_client.send_email(
            Source=from_email,
            Destination={'ToAddresses': [to_email]},
            Message={
                'Subject': {'Data': subject},
                'Body': {'Text': {'Data': body}}
            }
        )
        return response
    except (NoCredentialsError, PartialCredentialsError) as e:
        return jsonify({'error': 'Credentials not available', 'message': str(e)}), 403


def validate_email(email):
    # Basic email validation logic
    import re
    regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if re.match(regex, email):
        return True
    return False
