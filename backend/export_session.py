import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Session, Lesson, Quiz, Category

engine = create_engine('sqlite:///divedeep.db')
db = sessionmaker(bind=engine)()

data = []

sessions = db.query(Session).all()
for s in sessions:
    category = db.query(Category).filter_by(id=s.category_id).first()
    lessons = db.query(Lesson).filter_by(session_id=s.id).all()
    quizzes = db.query(Quiz).filter_by(session_id=s.id).all()

    data.append({
        "title": s.title,
        "category_name": category.name if category else "Unknown",
        "lessons": [
            {"order": l.order, "content": l.content}
            for l in lessons
        ],
        "quizzes": [
            {
                "question": q.question,
                "option_a": q.option_a,
                "option_b": q.option_b,
                "option_c": q.option_c,
                "option_d": q.option_d,
                "correct_option": q.correct_option
            }
            for q in quizzes
        ]
    })

db.close()

with open('sessions_export.json', 'w') as f:
    json.dump(data, f, indent=2)

print(f"Exported {len(data)} sessions successfully!")