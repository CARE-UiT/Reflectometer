import unittest
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker

from fastapi.testclient import TestClient
from main import app, get_db
from database import engine

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

class TestReflectometer(unittest.TestCase):
    def setUp(self):

        app.dependency_overrides[get_db] = override_get_db
        self.client = TestClient(app)

    def test_createReflectometer(self):
        self.client.post(
            "/api/auth/new",
            {}
        )
        self.assertEqual(1,1)

if __name__ == "__main__":
    unittest.main()