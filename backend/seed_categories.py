from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Category

import os
from dotenv import load_dotenv
load_dotenv()
DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///divedeep.db')
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
engine = create_engine(DATABASE_URL)
DBSession = sessionmaker(bind=engine)
db = DBSession()

categories = [
    "Finance",
    "Beauty",
    "Politics",
    "Science",
    "Technology",
    "History",
    "Psychology",
    "Health",
    "Philosophy",
    "Art"
]

for name in categories:
    existing = db.query(Category).filter_by(name=name).first()
    if not existing:
        db.add(Category(name=name))

db.commit()
db.close()
print("Categories added successfully!")