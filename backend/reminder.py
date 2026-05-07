from flask import Blueprint, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import DailyReminder, UserSessionHistory
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from collections import Counter

reminder_bp = Blueprint('reminder', __name__)

engine = create_engine('sqlite:///divedeep.db')
DBSession = sessionmaker(bind=engine)

# SET MANUAL REMINDER
@reminder_bp.route('/reminder/set', methods=['POST'])
@jwt_required()
def set_reminder():
    db = DBSession()
    user_id = get_jwt_identity()
    data = request.get_json()

    # CHECK IF REMINDER ALREADY EXISTS
    existing = db.query(DailyReminder).filter_by(user_id=user_id).first()

    if existing:
        existing.reminder_time = data['reminder_time']
        existing.is_auto = False
    else:
        new_reminder = DailyReminder(
            user_id=user_id,
            reminder_time=data['reminder_time'],
            is_auto=False
        )
        db.add(new_reminder)

    db.commit()
    db.close()
    return jsonify({"message": "Reminder set successfully!"})

# GET REMINDER
@reminder_bp.route('/reminder', methods=['GET'])
@jwt_required()
def get_reminder():
    db = DBSession()
    user_id = get_jwt_identity()

    reminder = db.query(DailyReminder).filter_by(user_id=user_id).first()
    if not reminder:
        db.close()
        return jsonify({"message": "No reminder set"})

    db.close()
    return jsonify({
        "reminder_time": reminder.reminder_time,
        "is_auto": reminder.is_auto
    })

# GET AUTO SUGGESTED REMINDER TIME
@reminder_bp.route('/reminder/suggest', methods=['GET'])
@jwt_required()
def suggest_reminder():
    db = DBSession()
    user_id = get_jwt_identity()

    # GET ALL HISTORY
    history = db.query(UserSessionHistory).filter_by(user_id=user_id).all()

    if len(history) < 10:
        db.close()
        return jsonify({
            "message": "Not enough data yet",
            "days_remaining": 10 - len(history)
        })

    # FIND MOST COMMON HOUR
    hours = [h.attended_at.hour for h in history]
    most_common_hour = Counter(hours).most_common(1)[0][0]
    suggested_time = f"{most_common_hour:02d}:00"

    # AUTO SET THE REMINDER
    existing = db.query(DailyReminder).filter_by(user_id=user_id).first()
    if existing:
        existing.reminder_time = suggested_time
        existing.is_auto = True
    else:
        new_reminder = DailyReminder(
            user_id=user_id,
            reminder_time=suggested_time,
            is_auto=True
        )
        db.add(new_reminder)

    db.commit()
    db.close()
    return jsonify({
        "message": "Auto reminder suggested!",
        "suggested_time": suggested_time
    })

# DELETE REMINDER
@reminder_bp.route('/reminder/delete', methods=['DELETE'])
@jwt_required()
def delete_reminder():
    db = DBSession()
    user_id = get_jwt_identity()

    reminder = db.query(DailyReminder).filter_by(user_id=user_id).first()
    if not reminder:
        db.close()
        return jsonify({"message": "No reminder found"})

    db.delete(reminder)
    db.commit()
    db.close()
    return jsonify({"message": "Reminder deleted successfully!"})