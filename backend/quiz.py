from flask import Blueprint, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Quiz, UserSessionHistory
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

quiz_bp = Blueprint('quiz', __name__)

engine = create_engine('sqlite:///divedeep.db')
DBSession = sessionmaker(bind=engine)

# SUBMIT QUIZ ANSWERS
@quiz_bp.route('/quiz/submit', methods=['POST'])
@jwt_required()
def submit_quiz():
    db = DBSession()
    user_id = get_jwt_identity()
    data = request.get_json()

    session_id = data['session_id']
    user_answers = data['answers']

    # GET ALL QUIZ QUESTIONS FOR THIS SESSION
    questions = db.query(Quiz).filter_by(session_id=session_id).all()

    correct = 0
    wrong = 0
    result_details = []

    for question in questions:
        user_answer = user_answers.get(str(question.id))
        is_correct = user_answer == question.correct_option

        if is_correct:
            correct += 1
        else:
            wrong += 1

        result_details.append({
            "question_id": question.id,
            "question": question.question,
            "your_answer": user_answer,
            "correct_answer": question.correct_option,
            "is_correct": is_correct,
            "option_a": question.option_a,
            "option_b": question.option_b,
            "option_c": question.option_c,
            "option_d": question.option_d
        })

    total = correct + wrong
    score_percentage = round((correct / total) * 100) if total > 0 else 0

    # MARK SESSION AS COMPLETED IN HISTORY
    history = db.query(UserSessionHistory).filter_by(
        user_id=user_id,
        session_id=session_id
    ).first()

    if history:
        history.completed = True
    else:
        new_history = UserSessionHistory(
            user_id=user_id,
            session_id=session_id,
            completed=True,
            attended_at=datetime.utcnow()
        )
        db.add(new_history)

    db.commit()
    db.close()

    return jsonify({
        "total": total,
        "correct": correct,
        "wrong": wrong,
        "score_percentage": score_percentage,
        "result_details": result_details
    })

# GET QUIZ QUESTIONS FOR A SESSION
@quiz_bp.route('/quiz/<int:session_id>', methods=['GET'])
@jwt_required()
def get_quiz(session_id):
    db = DBSession()
    questions = db.query(Quiz).filter_by(session_id=session_id).all()
    result = []
    for q in questions:
        result.append({
            "id": q.id,
            "question": q.question,
            "option_a": q.option_a,
            "option_b": q.option_b,
            "option_c": q.option_c,
            "option_d": q.option_d
        })
    db.close()
    return jsonify(result)