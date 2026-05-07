from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager
from auth import auth_bp
from history import history_bp
from saved import saved_bp
from reminder import reminder_bp
from quiz import quiz_bp
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database import User, Category, Session, Lesson, Quiz, UserSessionHistory, SavedLesson, DailyReminder, Base

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'divedeep-secret-key-2024'
jwt = JWTManager(app)
app.register_blueprint(auth_bp)
app.register_blueprint(history_bp)
app.register_blueprint(saved_bp)
app.register_blueprint(reminder_bp)
app.register_blueprint(quiz_bp)

engine = create_engine('sqlite:///divedeep.db')
DBSession = sessionmaker(bind=engine)

# TEST ROUTE
@app.route('/')
def home():
    return jsonify({"message": "Dive Deep backend is running!"})

# GET ALL CATEGORIES
@app.route('/categories', methods=['GET'])
def get_categories():
    db = DBSession()
    categories = db.query(Category).all()
    result = [{"id": c.id, "name": c.name} for c in categories]
    db.close()
    return jsonify(result)

# ADD A CATEGORY
@app.route('/categories', methods=['POST'])
def add_category():
    db = DBSession()
    data = request.get_json()
    new_category = Category(name=data['name'])
    db.add(new_category)
    db.commit()
    db.close()
    return jsonify({"message": "Category added successfully!"})

# GET ALL SESSIONS
@app.route('/sessions', methods=['GET'])
def get_sessions():
    db = DBSession()
    sessions = db.query(Session).all()
    result = [{"id": s.id, "title": s.title, "category_id": s.category_id} for s in sessions]
    db.close()
    return jsonify(result)

# GET LESSONS FOR A SESSION
@app.route('/sessions/<int:session_id>/lessons', methods=['GET'])
def get_lessons(session_id):
    db = DBSession()
    lessons = db.query(Lesson).filter_by(session_id=session_id).all()
    result = [{"id": l.id, "order": l.order, "content": l.content} for l in lessons]
    db.close()
    return jsonify(result)

# GET QUIZ FOR A SESSION
@app.route('/sessions/<int:session_id>/quiz', methods=['GET'])
def get_quiz(session_id):
    db = DBSession()
    quizzes = db.query(Quiz).filter_by(session_id=session_id).all()
    result = [{"id": q.id, "question": q.question, "option_a": q.option_a, "option_b": q.option_b, "option_c": q.option_c, "option_d": q.option_d} for q in quizzes]
    db.close()
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)