from flask import Blueprint, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import UserSessionHistory, Session
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

history_bp = Blueprint('history', __name__)

engine = create_engine('sqlite:///divedeep.db')
DBSession = sessionmaker(bind=engine)

# RECORD A SESSION ATTENDED
@history_bp.route('/history/add', methods=['POST'])
@jwt_required()
def add_history():
    db = DBSession()
    user_id = get_jwt_identity()
    data = request.get_json()

    new_history = UserSessionHistory(
        user_id=user_id,
        session_id=data['session_id'],
        completed=data.get('completed', False),
        attended_at=datetime.utcnow()
    )
    db.add(new_history)
    db.commit()
    db.close()
    return jsonify({"message": "History recorded successfully!"})

# GET ALL HISTORY FOR A USER
@history_bp.route('/history', methods=['GET'])
@jwt_required()
def get_history():
    db = DBSession()
    user_id = get_jwt_identity()

    history = db.query(UserSessionHistory).filter_by(user_id=user_id).all()
    result = []
    for h in history:
        session = db.query(Session).filter_by(id=h.session_id).first()
        result.append({
            "session_id": h.session_id,
            "session_title": session.title if session else "Unknown",
            "completed": h.completed,
            "attended_at": h.attended_at.strftime("%Y-%m-%d %H:%M:%S")
        })
    db.close()
    return jsonify(result)

# GET CALENDAR DATA FOR A USER
@history_bp.route('/history/calendar', methods=['GET'])
@jwt_required()
def get_calendar():
    db = DBSession()
    user_id = get_jwt_identity()

    history = db.query(UserSessionHistory).filter_by(user_id=user_id).all()
    active_days = list(set([
        h.attended_at.strftime("%Y-%m-%d") for h in history
    ]))
    db.close()
    return jsonify({"active_days": active_days})