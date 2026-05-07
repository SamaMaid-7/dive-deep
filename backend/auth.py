from flask import Blueprint, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import User
import bcrypt
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__)

engine = create_engine('sqlite:///divedeep.db')
DBSession = sessionmaker(bind=engine)

# REGISTER
@auth_bp.route('/register', methods=['POST'])
def register():
    db = DBSession()
    data = request.get_json()

    existing_user = db.query(User).filter_by(email=data['email']).first()
    if existing_user:
        db.close()
        return jsonify({"error": "Email already exists"}), 400

    hashed_password = bcrypt.hashpw(
        data['password'].encode('utf-8'),
        bcrypt.gensalt()
    ).decode('utf-8')

    new_user = User(
        username=data['username'],
        email=data['email'],
        password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.close()
    return jsonify({"message": "User registered successfully!"})

# LOGIN
@auth_bp.route('/login', methods=['POST'])
def login():
    db = DBSession()
    data = request.get_json()

    user = db.query(User).filter_by(email=data['email']).first()
    if not user:
        db.close()
        return jsonify({"error": "User not found"}), 404

    if not bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
        db.close()
        return jsonify({"error": "Wrong password"}), 401

    access_token = create_access_token(identity=str(user.id))
    db.close()
    return jsonify({
        "token": access_token,
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }
    })