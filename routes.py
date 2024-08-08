from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from utils import send_email, validate_email
from models import db, User, Recipient, Event, Message

auth = Blueprint('auth', __name__)
api = Blueprint('api', __name__)


@auth.route('/register', methods=['POST'])
def register():
    data = request.json
    if not validate_email(data['email']):
        return jsonify({'message': 'Invalid email format'}), 400
    user = User.query.filter_by(email=data['email']).first()
    if user:
        return jsonify({'message': 'User already exists'}), 400
    new_user = User(email=data['email'])
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201


@auth.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()
    if user and user.check_password(data['password']):
        access_token = create_access_token(
            identity={'id': user.id, 'email': user.email})
        return jsonify({'token': access_token}), 200
    return jsonify({'message': 'Invalid credentials'}), 401


@api.route('/send-email', methods=['POST'])
@jwt_required()
def send_email_route():
    data = request.json
    if not validate_email(data['to']):
        return jsonify({'message': 'Invalid email format'}), 400
    response = send_email(data['from'], data['to'],
                          data['subject'], data['body'])
    return jsonify(response)


@api.route('/recipients', methods=['POST'])
@jwt_required()
def create_recipient():
    user_id = get_jwt_identity()['id']
    data = request.json
    new_recipient = Recipient(
        user_id=user_id,
        name=data['name'],
        relationship=data.get('relationship', ''),
        email=data['email'],
        address=data.get('address', ''),
        avatar=data.get('avatar', '')
    )
    db.session.add(new_recipient)
    db.session.commit()
    return jsonify({'message': 'Recipient created successfully'})


@api.route('/recipients', methods=['GET'])
@jwt_required()
def get_recipients():
    user_id = get_jwt_identity()['id']
    recipients = Recipient.query.filter_by(user_id=user_id).all()
    return jsonify([recipient.as_dict() for recipient in recipients])


@api.route('/recipients/<int:id>', methods=['PUT'])
@jwt_required()
def update_recipient(id):
    data = request.json
    recipient = Recipient.query.get(id)
    if not recipient:
        return jsonify({'message': 'Recipient not found'}), 404
    recipient.name = data['name']
    recipient.relationship = data['relationship']
    recipient.email = data['email']
    recipient.address = data['address']
    recipient.avatar = data['avatar']
    db.session.commit()
    return jsonify({'message': 'Recipient updated successfully'})
