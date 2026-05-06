from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Category

engine = create_engine('sqlite:///divedeep.db')
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