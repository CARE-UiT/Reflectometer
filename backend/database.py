from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from environment import DB_HOST, DB_PORT


if DB_HOST != "":
    SQLALCHEMY_DATABASE_URL = f'postgresql+psycopg://postgres:Reflectometer@{DB_HOST}:{DB_PORT}'
else:
    import testing.postgresql
    #Setup test database
    TEST_DB = testing.postgresql.Postgresql()
    SQLALCHEMY_DATABASE_URL = TEST_DB.url()
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
