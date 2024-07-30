from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity
)
from app import db
from models import User, Recipient, Compliment
from utils import send_email

auth_bp = Blueprint('auth', __name__)
recipient_bp = Blueprint('recipient', __name__)


@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
        return jsonify({"msg": "User already exists"}), 400

    new_user = User(username=username, email=email)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "User created successfully"}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200

    return jsonify({"msg": "Invalid credentials"}), 401


@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    return jsonify({"msg": "Logout successful"}), 200


@recipient_bp.route('/recipients', methods=['POST'])
@jwt_required()
def add_recipient():
    current_user_id = get_jwt_identity()
    data = request.json
    email = data.get('email')
    timezone = data.get('timezone', None)
    days_of_week = data.get('days_of_week')

    new_recipient = Recipient(
        user_id=current_user_id, email=email, timezone=timezone, days_of_week=days_of_week)
    db.session.add(new_recipient)
    db.session.commit()

    return jsonify({"msg": "Recipient added successfully"}), 201


@recipient_bp.route('/recipients/<int:id>', methods=['PUT'])
@jwt_required()
def update_recipient(id):
    current_user_id = get_jwt_identity()
    data = request.json
    recipient = Recipient.query.filter_by(
        id=id, user_id=current_user_id).first()

    if not recipient:
        return jsonify({"msg": "Recipient not found"}), 404

    recipient.email = data.get('email', recipient.email)
    recipient.timezone = data.get('timezone', recipient.timezone)
    recipient.days_of_week = data.get('days_of_week', recipient.days_of_week)

    db.session.commit()

    return jsonify({"msg": "Recipient updated successfully"}), 200


@recipient_bp.route('/recipients/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_recipient(id):
    current_user_id = get_jwt_identity()
    recipient = Recipient.query.filter_by(
        id=id, user_id=current_user_id).first()

    if not recipient:
        return jsonify({"msg": "Recipient not found"}), 404

    db.session.delete(recipient)
    db.session.commit()

    return jsonify({"msg": "Recipient deleted successfully"}), 200


@recipient_bp.route('/compliments', methods=['POST'])
@jwt_required()
def add_compliment():
    current_user_id = get_jwt_identity()
    data = request.json
    recipient_id = data.get('recipient_id')
    compliment_text = data.get('compliment_text')

    recipient = Recipient.query.filter_by(
        id=recipient_id, user_id=current_user_id).first()
    if not recipient:
        return jsonify({"msg": "Recipient not found"}), 404

    existing_compliment = Compliment.query.filter_by(
        recipient_id=recipient_id, compliment_text=compliment_text).first()
    if existing_compliment:
        return jsonify({"msg": "Compliment already sent"}), 400

    new_compliment = Compliment(
        recipient_id=recipient_id, compliment_text=compliment_text)
    db.session.add(new_compliment)
    db.session.commit()

    send_email("You've got a compliment!", recipient.email, compliment_text)

    return jsonify({"msg": "Compliment sent and archived successfully"}), 201
