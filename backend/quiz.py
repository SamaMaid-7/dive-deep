import os
from flask import Blueprint, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Quiz, UserSessionHistory, SESSION_LOCAL
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

quiz_bp = Blueprint('quiz', __name__)

DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///divedeep.db')
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)
DBSession = sessionmaker(bind=engine)

groq_client = Groq(api_key=os.environ.get('GROQ_API_KEY'))

# SUBMIT QUIZ ANSWERS
@quiz_bp.route('/quiz/submit', methods=['POST'])
@jwt_required()
def submit_quiz():
    db = DBSession()
    user_id = get_jwt_identity()
    data = request.get_json()

    session_id = data['session_id']
    user_answers = data['answers']

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

# GET QUIZ QUESTIONS
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

# GENERATE AI SUMMARY USING GROQ
@quiz_bp.route('/quiz/summary', methods=['POST'])
def generate_summary():
    data = request.get_json()
    result_details = data.get('result_details', [])

    wrong_questions = [r for r in result_details if not r['is_correct']]

    if not wrong_questions:
        return jsonify({"summary": "Outstanding! You got everything correct. You have a strong understanding of this topic!"})

    wrong_text = ""
    for w in wrong_questions:
        wrong_text += f"Question: {w['question']}\n"
        wrong_text += f"Correct Answer: {w['correct_answer']}\n\n"

    prompt = f"""
    A student just completed a quiz and got these questions wrong:
    {wrong_text}
    Write a very short beginner friendly summary (max 5 sentences) that:
    1. Identifies what concept the student is struggling with
    2. Gives one simple real life example to explain it
    3. Highlights the key thing they need to remember
    Write in a warm encouraging tone. No bullet points. Just simple paragraph.
    """

    try:
        response = groq_client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{'role': 'user', 'content': prompt}]
        )
        summary = response.choices[0].message.content
    except Exception as e:
        print(f"Groq error: {e}")
        summary = "Great effort! Review the incorrect answers above to strengthen your understanding."

    return jsonify({"summary": summary})