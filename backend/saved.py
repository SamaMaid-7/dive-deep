from flask import Blueprint, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import SavedLesson, Lesson, Session
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

saved_bp = Blueprint('saved', __name__)

import os
from dotenv import load_dotenv
load_dotenv()
DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///divedeep.db')
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
engine = create_engine(DATABASE_URL)
DBSession = sessionmaker(bind=engine)

# SAVE A LESSON
@saved_bp.route('/saved/add', methods=['POST'])
@jwt_required()
def save_lesson():
    db = DBSession()
    user_id = get_jwt_identity()
    data = request.get_json()

    # CHECK IF ALREADY SAVED
    existing = db.query(SavedLesson).filter_by(
        user_id=user_id,
        lesson_id=data['lesson_id']
    ).first()

    if existing:
        db.close()
        return jsonify({"message": "Lesson already saved!"})

    new_saved = SavedLesson(
        user_id=user_id,
        lesson_id=data['lesson_id'],
        saved_at=datetime.utcnow()
    )
    db.add(new_saved)
    db.commit()
    db.close()
    return jsonify({"message": "Lesson saved successfully!"})

# UNSAVE A LESSON
@saved_bp.route('/saved/remove', methods=['POST'])
@jwt_required()
def unsave_lesson():
    db = DBSession()
    user_id = get_jwt_identity()
    data = request.get_json()

    saved = db.query(SavedLesson).filter_by(
        user_id=user_id,
        lesson_id=data['lesson_id']
    ).first()

    if not saved:
        db.close()
        return jsonify({"message": "Lesson not saved!"})

    db.delete(saved)
    db.commit()
    db.close()
    return jsonify({"message": "Lesson unsaved successfully!"})

# GET ALL SAVED LESSONS FOR A USER
@saved_bp.route('/saved', methods=['GET'])
@jwt_required()
def get_saved():
    db = DBSession()
    user_id = get_jwt_identity()

    saved_lessons = db.query(SavedLesson).filter_by(user_id=user_id).all()
    result = []
    for s in saved_lessons:
        lesson = db.query(Lesson).filter_by(id=s.lesson_id).first()
        if lesson:
            session = db.query(Session).filter_by(id=lesson.session_id).first()
            result.append({
                "lesson_id": lesson.id,
                "lesson_content": lesson.content,
                "session_title": session.title if session else "Unknown",
                "saved_at": s.saved_at.strftime("%Y-%m-%d %H:%M:%S")
            })
    db.close()
    return jsonify(result)