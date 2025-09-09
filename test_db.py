# test_db.py
from sqlmodel import Session, select
from app.database import engine
from app.models import User, Todo

print("Attempting to query tables...")

with Session(engine) as session:
    # Check for users
    users = session.exec(select(User)).all()
    print(f"Found {len(users)} users.")

    # Check for todos
    todos = session.exec(select(Todo)).all()
    print(f"Found {len(todos)} todos.")

print("Success! Both tables can be queried.")