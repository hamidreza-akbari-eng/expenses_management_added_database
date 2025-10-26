from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from core.config import settings

DATABASE_URL = "sqlite:///./database.db"

engine = create_engine(
    url=settings.SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)


SessoinLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)


Base = declarative_base()


def get_db():
    db = SessoinLocal()
    try:
        yield db
    finally:
        db.close()
