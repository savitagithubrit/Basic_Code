from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


# PostgreSQL Connection
DATABASE_URL = "postgresql+psycopg2://postgres:postgres123@localhost:5432/postgres"
engine = create_engine(DATABASE_URL)
Base = declarative_base()

SessionLocal = sessionmaker(bind=engine)
