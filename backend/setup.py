import json
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Session, Lesson, Quiz, Category, User, Base
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///divedeep.db')
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
db = sessionmaker(bind=engine)()

# SEED CATEGORIES
categories = [
    "Finance", "Beauty", "Politics", "Science",
    "Technology", "History", "Psychology",
    "Health", "Philosophy", "Art"
]

for name in categories:
    existing = db.query(Category).filter_by(name=name).first()
    if not existing:
        db.add(Category(name=name))
db.commit()
print("Categories seeded!")

# IMPORT SESSIONS
try:
    with open('sessions_export.json', 'r') as f:
        data = json.load(f)

    count = 0
    for item in data:
        category = db.query(Category).filter_by(
            name=item['category_name']
        ).first()

        if not category:
            print(f"Category not found: {item['category_name']}")
            continue

        existing = db.query(Session).filter_by(
            title=item['title']
        ).first()

        if existing:
            print(f"Skipping: {item['title']}")
            continue

        new_session = Session(
            title=item['title'],
            category_id=category.id
        )
        db.add(new_session)
        db.flush()

        for l in item['lessons']:
            db.add(Lesson(
                session_id=new_session.id,
                order=l['order'],
                content=l['content']
            ))

        for q in item['quizzes']:
            db.add(Quiz(
                session_id=new_session.id,
                question=q['question'],
                option_a=q['option_a'],
                option_b=q['option_b'],
                option_c=q['option_c'],
                option_d=q['option_d'],
                correct_option=q['correct_option']
            ))

        count += 1

    db.commit()
    print(f"Imported {count} sessions!")

except FileNotFoundError:
    print("sessions_export.json not found!")
except Exception as e:
    print(f"Import error: {e}")

db.close()
print("Setup complete!")