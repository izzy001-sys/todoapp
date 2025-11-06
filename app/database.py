import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

APP_ENV = os.getenv("APP_ENV", "dev")

if APP_ENV == "test":
    DB_FILE = "test_e2e.db"
    # start each e2e session clean
    try:
        os.remove(DB_FILE)
    except FileNotFoundError:
        pass
    SQLALCHEMY_DATABASE_URL = f"sqlite:///./{DB_FILE}"
else:
    SQLALCHEMY_DATABASE_URL = "sqlite:///./todo_app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
