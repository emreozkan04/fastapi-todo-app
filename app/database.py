from sqlmodel import SQLModel, Session, create_engine
import os


database_url = os.environ.get("DATABASE_URL", "sqlite:///database.db")

connect_args = {"check_same_thread": False} if database_url.startswith("sqlite") else {}
engine = create_engine(database_url, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

