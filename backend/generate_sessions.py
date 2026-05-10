import ollama
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Category, Session, Lesson, Quiz

engine = create_engine('sqlite:///divedeep.db')
DBSession = sessionmaker(bind=engine)
db = DBSession()

def generate_session(category_name, topic):
    prompt = f"""
    Create a learning session about "{topic}" in the category "{category_name}".
    Respond in pure JSON only. No extra text. No markdown. Just JSON.
    Use this exact format:
    {{
        "title": "session title here",
        "lesson1": "detailed explanation of first lesson here in 4 to 6 sentences",
        "lesson2": "detailed explanation of second lesson here in 4 to 6 sentences",
        "quiz": [
            {{
                "question": "question here",
                "option_a": "option a here",
                "option_b": "option b here",
                "option_c": "option c here",
                "option_d": "option d here",
                "correct_option": "a"
            }},
            {{
                "question": "question here",
                "option_a": "option a here",
                "option_b": "option b here",
                "option_c": "option c here",
                "option_d": "option d here",
                "correct_option": "b"
            }},
            {{
                "question": "question here",
                "option_a": "option a here",
                "option_b": "option b here",
                "option_c": "option c here",
                "option_d": "option d here",
                "correct_option": "c"
            }}
        ]
    }}
    """

    response = ollama.chat(
        model='llama3.2',
        messages=[{'role': 'user', 'content': prompt}]
    )

    raw = response['message']['content']
    data = json.loads(raw)
    return data

def save_session(category_name, topic):
    try:
        category = db.query(Category).filter_by(name=category_name).first()
        if not category:
            print(f"Category {category_name} not found")
            return

        data = generate_session(category_name, topic)

        new_session = Session(
            title=data['title'],
            category_id=category.id
        )
        db.add(new_session)
        db.flush()

        lesson1 = Lesson(
            session_id=new_session.id,
            order=1,
            content=data['lesson1']
        )
        lesson2 = Lesson(
            session_id=new_session.id,
            order=2,
            content=data['lesson2']
        )
        db.add(lesson1)
        db.add(lesson2)

        for q in data['quiz']:
            quiz = Quiz(
                session_id=new_session.id,
                question=q['question'],
                option_a=q['option_a'],
                option_b=q['option_b'],
                option_c=q['option_c'],
                option_d=q['option_d'],
                correct_option=q['correct_option']
            )
            db.add(quiz)

        db.commit()
        print(f"Session saved: {data['title']}")

    except Exception as e:
        db.rollback()
        print(f"Error: {e}")

# GENERATE SESSIONS FOR EACH CATEGORY
topics = [
    ("Beauty", "How Skincare Ingredients Work"),
    ("Beauty", "The Science Behind Hair Growth"),
    ("Beauty", "What is the Glass Skin Routine"),
    ("Politics", "How Democracy Works"),
    ("Politics", "What is Geopolitics"),
    ("Politics", "How United Nations Works"),
    ("Art", "How Color Theory Works"),
    ("Art", "The History of Street Art"),
    ("Art", "What is the Bauhaus Movement"),
    ("Science", "What is Quantum Physics"),
    ("Science", "How Vaccines Work"),
    ("History", "How World War 1 Started"),
    ("History", "The Roman Empire Rise and Fall"),
    ("Health", "How Stress Affects Your Body"),
    ("Health", "Why Hydration Matters"),
    ("Philosophy", "What is Existentialism"),
    ("Philosophy", "The Ethics of Artificial Intelligence"),
    ("Finance", "How Stock Markets Work"),
    ("Technology", "How the Internet Works"),
    ("Psychology", "The Placebo Effect"),

]

for category, topic in topics:
    print(f"Generating: {topic}...")
    save_session(category, topic)

db.close()
print("All sessions generated successfully!")